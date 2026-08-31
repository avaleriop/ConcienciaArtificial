#!/usr/bin/env python3
"""
ORGANISMO FINAL v0.12 - Arquitectura atencion activa + fisica continua
Integra: predictor (H2) + sorpresa z (H5) + Phi self-model (H6) + ECUS (H3)
         + memoria E / W EWC (H1) + accion epistemica (Phi-causal) + boca LFM2.5
Mundo: fisica continua 2D con zona de niebla (x>14, interoception ruidosa).
       Canales sensoriales: visual (posicion), tactil (choque), interoception (E,C,U,S).
       Atencion activa: modulo modula precisión sigma por canal selector.
Metodologia: resuelve el problema del MLP de habi generalizandose globalmente,
usando actualizaciones de peso ortogonales por canal y atencion dinamica.
Ejecuta: python3 framework/organismo_final.py --steps 30000
"""
import sys, math, random, time, argparse, os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
WORLD_SIZE = 20.0
NIEBLA_X = 14.0
FOODS = [(3.0,3.0),(3.0,16.0),(10.0,3.0),(10.0,16.0)]
SOCIAL = (18.0, 18.0)
N_SENSORIAL = 7
RUIDO_BASE = 0.15
RUIDO_NIEBLA = 0.60
ORTHO_LAMBDA = 0.01
EWC_LAMBDA = 5.0

class Attention(nn.Module):
    """Modulo de atencion activa: modula precisión por canal sensorial."""
    def __init__(self, d_in=13, d_h=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, 7))
    def forward(self, x):
        return torch.softmax(self.net(x), dim=-1)

class Predictor(nn.Module):
    def __init__(self, d_in=13, d_h=64, d_out=6):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, d_out))
    def forward(self, x):
        return self.net(x)

class Phi(nn.Module):
    def __init__(self, d_in=22, d_h=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, 1))
    def forward(self, x):
        return torch.abs(self.net(x))

def entrada(estado, a):
    """estado: [x, y, H0, H1, H2, H3] continuo en [0, WORLD_SIZE).
    a: accion one-hot (7,) o indice entero.
    Devuelve vector de entrada al predictor: [vis_x, vis_y, H_norm..., action_onehot].
    """
    if isinstance(a, int):
        a_oh = np.zeros(7, dtype=np.float32); a_oh[a] = 1.0
    else:
        a_oh = np.float32(a)
    x, y = float(estado[0]), float(estado[1])
    H_norm = np.array([float(estado[i])/1.5 for i in range(2, 6)], dtype=np.float32)
    visual = np.array([x/WORLD_SIZE, y/WORLD_SIZE], dtype=np.float32)
    return np.concatenate([visual, H_norm, a_oh], dtype=np.float32)

def entrada_phi(estado, a, em, es, atten=None):
    base = entrada(estado, a)
    if atten is None:
        atten = np.zeros(7, dtype=np.float32)
    return np.concatenate([base, atten, np.array([em, es], dtype=np.float32)])

def fisica_continuo(pos, a, en_niebla):
    x, y = pos[0]+a[0]*0.8, pos[1]+a[1]*0.8
    x *= 0.95; y *= 0.95
    x = max(0.0, min(WORLD_SIZE, x))
    y = max(0.0, min(WORLD_SIZE, y))
    en_n = x > NIEBLA_X
    return [x, y], en_n

def ruido_canal(canal_idx, en_niebla):
    base = RUIDO_BASE
    if en_niebla and canal_idx in (0,1,2,3,4):
        base = RUIDO_NIEBLA
    if canal_idx == 6: base = RUIDO_BASE * 0.5
    return np.random.randn() * base

class CuerpoMundo:
    def __init__(self):
        self.pos = [WORLD_SIZE/2, WORLD_SIZE/2]
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)
        self.foods = FOODS
        self.social = SOCIAL
    def en_niebla(self):
        return self.pos[0] > NIEBLA_X
    def estado(self):
        return np.array([self.pos[0], self.pos[1], self.H[0], self.H[1], self.H[2], self.H[3]], dtype=np.float32)
    def step(self, a_idx):
        a = np.zeros(7, dtype=np.float32); a[a_idx] = 1.0
        H = self.H
        if H[0] < 0.55:
            dists = [math.hypot(self.pos[0]-fx, self.pos[1]-fy) for fx, fy in self.foods]
            idx = int(np.argmin(dists))
            fx, fy = self.foods[idx]
            a_goal = np.zeros(7, dtype=np.float32)
            dx, dy = fx-self.pos[0], fy-self.pos[1]
            norm = math.hypot(dx,dy)+1e-6
            a_goal[0] = dx/norm; a_goal[1] = dy/norm
            a = a_goal
        elif H[3] > 0.8:
            dx, dy = self.social[0]-self.pos[0], self.social[1]-self.pos[1]
            norm = math.hypot(dx,dy)+1e-6
            a_goal = np.zeros(7, dtype=np.float32)
            a_goal[0] = dx/norm; a_goal[1] = dy/norm
            a = a_goal
        nueva_pos, en_niebla = fisica_continuo(self.pos, a, self.en_niebla())
        dH = -0.02*(self.H - np.array([0.8,0.9,0.2,0.7], dtype=np.float32))
        if en_niebla:
            dH[0] -= 0.03; dH[2] += 0.01
        else:
            dH[2] -= 0.01
        if any(math.hypot(self.pos[0]-fx, self.pos[1]-fy) < 0.5 for fx, fy in self.foods):
            dH[0] += 0.2
        for ch in range(7):
            r = ruido_canal(ch, en_niebla)
            if ch < 4: dH[ch] += r * 0.1
        if math.hypot(self.pos[0]-self.social[0], self.pos[1]-self.social[1]) < 0.5:
            dH[3] += 0.1
        self.H = np.clip(self.H + dH, 0, 1.5)
        self.pos = nueva_pos
        return self.estado()

_LLM = None; _TOK = None
# R16 mitigation: relative path with env-var fallback; mouth is optional (behaviour identical without it per H2b)
_MODEL_CANDIDATES = [
    os.environ.get("LLM_MODEL_PATH", ""),
    os.environ.get("MODELS_PATH", ""),
    "models/LFM2.5-1.2B-MLX-8bit",
    os.path.join(os.path.dirname(__file__), "..", "models", "LFM2.5-1.2B-MLX-8bit"),
]
def _resolve_model_path():
    for p in _MODEL_CANDIDATES:
        if p and os.path.exists(p):
            return p
    return None

def boca(texto):
    global _LLM, _TOK
    from mlx_lm import load, generate
    if _LLM is None:
        model_path = _resolve_model_path()
        if model_path is None:
            return "[boca model not found - run: python3 -c \"from huggingface_hub import snapshot_download; snapshot_download('LiquidAI/LFM2.5-1.2B-Instruct-MLX-8bit', local_dir='models/LFM2.5-1.2B-MLX-8bit')\"]"
        try:
            _LLM, _TOK = load(model_path)
        except Exception as e:
            return f"[boca load failed: {e}]"
    prompt = ("system\nEres el traductor lingüistico de un agente. Traduce su estado interno a UNA frase en primera persona, sin añadir nada.\n"
              f"user\n{texto}\nassistant\n")
    try:
        return generate(_LLM, _TOK, prompt=prompt, max_tokens=28).strip()
    except Exception as e:
        return f"[boca generate failed: {e}]"

def entrenar(mundo, pred, phi, atten):
    X, Y = [], []
    for _ in range(1200):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.step(a_idx=a)
        X.append(entrada(s_a, a))
        Y.append(np.concatenate([s_d[:2]/WORLD_SIZE, s_d[2:]/1.5]))
    Xt = torch.tensor(np.array(X), dtype=torch.float32, device=DEVICE)
    Yt = torch.tensor(np.array(Y), dtype=torch.float32, device=DEVICE)
    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    for _ in range(400):
        idx = torch.randint(0, Xt.shape[0], (64,))
        loss = (pred(Xt[idx])-Yt[idx]).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    Xp, Yp, hist = [], [], []
    for _ in range(2000):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.step(a_idx=a)
        with torch.no_grad():
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_d[:2]/WORLD_SIZE, s_d[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(x)-y).pow(2).mean().sqrt())
        hist.append(eps)
        if len(hist) > 50: hist.pop(0)
        h = np.array(hist)
        Xp.append(entrada_phi(s_a, a, h.mean(), h.std()))
        Yp.append(eps)
    Xpt = torch.tensor(np.array(Xp), dtype=torch.float32, device=DEVICE)
    Ypt = torch.tensor(np.array(Yp), dtype=torch.float32, device=DEVICE).unsqueeze(1)
    opt2 = torch.optim.Adam(phi.parameters(), lr=1e-3)
    for _ in range(500):
        idx = torch.randint(0, Xpt.shape[0], (64,))
        loss = (phi(Xpt[idx])-Ypt[idx]).pow(2).mean()
        opt2.zero_grad(); loss.backward(); opt2.step()
    # --- R15 mitigation: train Attention (was previously never trained, gate was heuristic) ---
    # Attention learns to map predictor input -> 7-channel weights that predict expected error sigma.
    # We train atten so that its implied per-channel noise estimate correlates with actual eps.
    # sigma_canal = RUIDO_BASE + (RUIDO_NIEBLA - RUIDO_BASE) * atten_weights  -> sigma_mean should predict eps
    # This makes attention non-random and its gate (att_visual <0.35 etc) grounded in learned uncertainty.
    opt_atten = torch.optim.Adam(atten.parameters(), lr=1e-3)
    # Build dataset for atten: reuse Xt (13-dim) and Yp eps as proxy for sigma
    # For atten training we need paired eps values; subsample Xp's base part (first 13 dims) and Yp
    X_atten = torch.tensor(np.array([xp[:13] for xp in Xp]), dtype=torch.float32, device=DEVICE)
    Y_atten = Ypt  # eps as target sigma
    for _ in range(300):
        idx = torch.randint(0, X_atten.shape[0], (64,))
        aw = atten(X_atten[idx])  # [64,7] softmax
        # Correct per-channel sigma formula (R15 sigma_canal bug fix reference)
        sigma_canal_batch = RUIDO_BASE + (RUIDO_NIEBLA - RUIDO_BASE) * aw  # [64,7] vector
        # Channel 6 has half noise (intero tactile special)
        sigma_canal_batch[:, 6] = RUIDO_BASE * 0.5
        sigma_mean = sigma_canal_batch.mean(dim=1, keepdim=True)  # [64,1]
        loss_atten = (sigma_mean - Y_atten[idx]).pow(2).mean()
        # Entropy regularizer to avoid collapse to one-hot
        entropy = -(aw * torch.log(aw + 1e-8)).sum(dim=1).mean()
        loss_atten = loss_atten - 0.01 * entropy
        opt_atten.zero_grad(); loss_atten.backward(); opt_atten.step()
    return opt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=30000)
    args = p.parse_args()
    print(f"ORGANISMO FINAL v0.12 - arquitectura atencion activa + fisica continua, {args.steps} pasos")
    print("="*78)
    mundo = CuerpoMundo()
    pred = Predictor().to(DEVICE)
    phi = Phi().to(DEVICE)
    atten = Attention().to(DEVICE)
    opt_pred = entrenar(mundo, pred, phi, atten)
    w_star = {n: p_.detach().clone() for n, p_ in pred.named_parameters()}
    fisher = {n: torch.zeros_like(p_) for n, p_ in pred.named_parameters()}
    E_mem = []
    eps_hist = []
    tiempo_niebla = 0
    n_boca = 0
    n_viol = 0
    z_max_ventana = 0
    reportes = []
    ultima_boca = -9999
    for t in range(args.steps):
        s = mundo.estado()
        with torch.no_grad():
            x_at = torch.tensor(entrada(s, 4), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            atten_weights = atten(x_at).cpu().numpy()[0]
        # R15 sigma_canal bug fix: proper per-channel vector (7-dim)
        sigma_canal = RUIDO_BASE + (RUIDO_NIEBLA - RUIDO_BASE) * atten_weights  # [7] vector
        sigma_canal[6] = RUIDO_BASE * 0.5  # channel 6 special (tactile half noise)
        sigma_prom = float(np.mean(sigma_canal))
        with torch.no_grad():
            xp = torch.tensor(entrada_phi(s, 4, np.mean(eps_hist) if eps_hist else 0.1, np.std(eps_hist) if eps_hist else 0.05, atten_weights), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            sigma = float(phi(xp))
        att_visual = atten_weights[0]
        att_int = np.mean(atten_weights[1:5])
        a = None
        if att_visual < 0.35 or att_int > 0.65:
            a = 3
        elif mundo.H[0] < 0.55:
            a = 4
        elif mundo.H[3] > 0.8:
            a = 5
        else:
            a = random.choice([0,1,2,3])
        violacion = (t % 5000 == 4999)
        s_antes = mundo.estado()
        if isinstance(a, int):
            a_idx = int(a)
        elif a is not None:
            a_idx = int(np.argmax(a))
        else:
            a_idx = random.randrange(7)
        if violacion:
            n_viol += 1
            mundo.pos = [min(WORLD_SIZE, max(0.0, mundo.pos[0] + 2.0)),
                         min(WORLD_SIZE, max(0.0, mundo.pos[1] + 2.0))]
            s_despues = mundo.estado()
            E_mem.append((t, "violacion", 1.2))
            if len(E_mem) > 5000:
                E_mem.pop(0)
        else:
            s_despues = mundo.step(a_idx=a_idx)
        with torch.no_grad():
            x = torch.tensor(entrada(s_antes, a_idx), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([np.array(mundo.pos, dtype=np.float32)/WORLD_SIZE, mundo.H/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(x)-y).pow(2).mean().sqrt())
        eps_hist.append(eps)
        if len(eps_hist) > 100: eps_hist.pop(0)
        h = np.array(eps_hist)
        z = (eps - h.mean())/(h.std()+1e-8)
        z_max_ventana = max(z_max_ventana, z)
        presence = eps/(sigma**2 + 1e-6)
        aprendizaje_z = min(0.3, 0.2*max(0.0, z)) * att_visual
        mundo.H[2] = np.clip(mundo.H[2] + aprendizaje_z - 0.03, 0, 1.5)
        xb = torch.tensor(entrada(s_antes, a_idx), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        yb = torch.tensor(np.concatenate([np.array(mundo.pos, dtype=np.float32)/WORLD_SIZE, mundo.H/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        base_loss = (pred(xb)-yb).pow(2).mean()
        ortho_penalty = 0.0
        for name, param in pred.named_parameters():
            if 'weight' in name:
                ortho_penalty += (param**2).mean()
        # R15 EWC fix: fisher was computed but never used. Now add EWC term.
        ewc_loss = 0.0
        for n, p in pred.named_parameters():
            if n in fisher and n in w_star:
                ewc_loss = ewc_loss + (fisher[n] * (p - w_star[n]).pow(2)).sum()
        loss = base_loss + (EWC_LAMBDA / 2) * ewc_loss + ORTHO_LAMBDA * ortho_penalty
        opt_pred.zero_grad(); loss.backward(); opt_pred.step()
        for k,p_ in pred.named_parameters():
            if p_.grad is not None: fisher[k] = 0.9*fisher[k]+0.1*p_.grad.detach()**2
        # Periodically update w_star to track consolidated weights (prevents EWC anchoring to stale origin)
        if t % 5000 == 0 and t > 0:
            w_star = {n: p_.detach().clone() for n, p_ in pred.named_parameters()}
        if (z > 4.0 or (sigma > 0.25 and mundo.en_niebla())) and t - ultima_boca > 500:
            ultima_boca = t
            n_boca += 1
            try:
                interno = (f"Estado: energia={mundo.H[0]:.2f}, incertidumbre={mundo.H[2]:.2f}. "
                           f"Modelo Phi predice sigma={sigma:.2f}. "
                           f"Atencion visual={att_visual:.2f}, interoception={att_int:.2f}. "
                           f"Evento: {'violaron mis contingencias sensorimotoras' if violacion else 'estoy en zona de baja fiabilidad sensorial'}.")
                frase = boca(interno)
                reportes.append((t, frase))
            except Exception as e:
                reportes.append((t, "[boca no disponible]"))
        if mundo.en_niebla(): tiempo_niebla += 1
        if t % 5000 == 0 and t > 0:
            print(f"  t={t}: E={mundo.H[0]:.2f} U={mundo.H[2]:.2f} | att_v={atten_weights[0]:.2f} att_i={np.mean(atten_weights[1:5]):.2f} | z_max {z_max_ventana:.1f} | sigma {sigma:.2f} | niebla {tiempo_niebla*100//t}% | E_mem {len(E_mem)} | boca {n_boca}", flush=True)
            z_max_ventana = 0
    print("="*78)
    print(f"{args.steps} pasos completados. E final {mundo.H[0]:.2f}, U {mundo.H[2]:.2f}")
    print(f"Tiempo en niebla: {tiempo_niebla/args.steps*100:.1f}% (accion epistemica gating por atencion)")
    print(f"Violaciones: {n_viol} | memoria E: {len(E_mem)} | boca: {n_boca} reportes")
    print("Reportes de la boca (incluye estado de Phi y atencion):")
    for t, frase in reportes[:5]:
        print(f"  t={t}: {frase}")

if __name__ == "__main__":
    main()
