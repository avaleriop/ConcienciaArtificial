#!/usr/bin/env python3
"""
ORGANISMO FINAL v0.12 - Todo integrado en UN loop continuo (consolidación)
Integra: predictor del cuerpo (H2) + sorpresa z (H5) + Φ self-model (H6) + ECUS (H3)
         + memoria E / W EWC (H1) + acción epistémica (Φ-causal) + boca LFM2.5
Mundo: 20x20 con zona de niebla (x>14, interocepción ruidosa) + comidas + violaciones ocasionales.
Métricas de continuidad: E oscila, Φ calibrado, acción epistémica (abandona niebla),
z alto en violaciones, habituación, E no satura, boca reporta (incluye estado de Φ).
Ejecuta: python3 framework/organismo_final.py --steps 30000
"""
import sys, math, random, time, argparse
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SIZE = 20
NIEBLA_X = 14
MODELO_LLM = "/Users/adrianvalerio/Desktop/ConcienciaArtificial/models/LFM2.5-1.2B-MLX-8bit"

class CuerpoMundo:
    def __init__(self):
        self.pos = [10, 10]
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)
        self.foods = [(3,3),(3,16),(10,3),(10,16)]  # comida FUERA de la zona de niebla (x>14)
        # (así la acción epistémica no compite con el forrajeo: la niebla no tiene comida)
        self.social = (18, 18)
        self.t = 0
    def en_niebla(self):
        return self.pos[0] > NIEBLA_X
    def estado(self):
        return np.concatenate([np.array(self.pos, dtype=np.float32), self.H])
    def fisica_normal(self, a):
        x, y = self.pos
        if a == 0: y = max(0, y-1)
        elif a == 1: y = min(SIZE-1, y+1)
        elif a == 2: x = min(SIZE-1, x+1)
        elif a == 3: x = max(0, x-1)
        elif a == 5:
            dx = np.sign(self.social[0]-x); dy = np.sign(self.social[1]-y)
            x = min(SIZE-1, max(0, x+dx)); y = min(SIZE-1, max(0, y+dy))
        self.pos = [x, y]
        ruido = 0.6 if self.en_niebla() else 0.0
        dH = -0.05*(self.H - np.array([0.8,0.9,0.2,0.7], dtype=np.float32))
        if a == 4 and tuple(self.pos) in self.foods: dH[0] += 0.5
        elif a == 4: dH[0] -= 0.1
        self.H = np.clip(self.H + dH + ruido*np.random.randn(4).astype(np.float32), 0, 1.5)
        return self.estado()

class Predictor(nn.Module):
    def __init__(self, d_in=13, d_h=64, d_out=6):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, d_out))
    def forward(self, x):
        return self.net(x)

class Phi(nn.Module):
    def __init__(self, d_in=15, d_h=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, 1))
    def forward(self, x):
        return torch.abs(self.net(x))

def entrada(estado, a):
    a_oh = np.zeros(7, dtype=np.float32); a_oh[a] = 1.0
    return np.concatenate([estado[:2]/SIZE, estado[2:]/1.5, a_oh])

def entrada_phi(estado, a, em, es):
    return np.concatenate([entrada(estado, a), np.array([em, es], dtype=np.float32)])

def entrenar(mundo, pred, phi):
    X, Y = [], []
    for _ in range(1200):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.fisica_normal(a)
        X.append(entrada(s_a, a)); Y.append(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]))
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
        s_a = mundo.estado(); s_d = mundo.fisica_normal(a)
        with torch.no_grad():
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
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
    return opt

_LLM = None; _TOK = None
def boca(texto):
    global _LLM, _TOK
    from mlx_lm import load, generate
    if _LLM is None:
        _LLM, _TOK = load(MODELO_LLM)
    prompt = ("<|im_start|>system\nEres el traductor lingüístico de un agente. Traduce su estado interno a UNA frase en primera persona, sin añadir nada.<|im_end|>"
              f"<|im_start|>user\n{texto}<|im_end|><|im_start|>assistant\n")
    return generate(_LLM, _TOK, prompt=prompt, max_tokens=28).strip()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=30000)
    args = p.parse_args()
    print(f"ORGANISMO FINAL v0.12 - todo integrado (predictor+sorpresa+Φ+ECUS+memoria+boca), {args.steps} pasos")
    print("="*78)
    mundo = CuerpoMundo()
    pred = Predictor().to(DEVICE)
    phi = Phi().to(DEVICE)
    opt_pred = entrenar(mundo, pred, phi)
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
        # política: comida si E baja; acción epistémica si Φ dice poco confiable; social; explora
        x0, y0 = mundo.pos
        dists = [math.hypot(x0-fx, y0-fy) for fx, fy in mundo.foods]
        en_comida = min(dists) == 0.0
        H = mundo.H
        a = None
        # Φ: predice σ actual
        with torch.no_grad():
            xp = torch.tensor(entrada_phi(mundo.estado(), 4, np.mean(eps_hist) if eps_hist else 0.1, np.std(eps_hist) if eps_hist else 0.05), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            sigma = float(phi(xp))
        if H[0] < 0.65 and en_comida:
            a = 4
        elif sigma > 0.25 and mundo.en_niebla():
            a = 3  # acción epistémica: abandono la niebla (no me fío de mis sentidos)
        elif H[0] < 0.70:
            fx_, fy_ = mundo.foods[int(np.argmin(dists))]
            dx, dy = fx_-x0, fy_-y0
            a = (2 if dx>0 else 3) if abs(dx)>abs(dy) else (1 if dy>0 else 0)
        elif H[3] < 0.5:
            a = 5
        else:
            a = random.choice([4,0,1,2,3])
        # eventos de violación ocasional
        violacion = (t % 5000 == 4999)
        s_antes = mundo.estado()
        if violacion:
            n_viol += 1
            mundo.pos = [(mundo.pos[0]+5)%SIZE, (mundo.pos[1]+5)%SIZE]
            s_despues = mundo.estado()
            E_mem.append((t, "violacion", 1.2))
        else:
            s_despues = mundo.fisica_normal(a)
        # ε y z
        with torch.no_grad():
            x = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(x)-y).pow(2).mean().sqrt())
        eps_hist.append(eps)
        if len(eps_hist) > 100: eps_hist.pop(0)
        h = np.array(eps_hist)
        z = (eps - h.mean())/(h.std()+1e-8)
        z_max_ventana = max(z_max_ventana, z)
        # Φ funcional: sorpresa ponderada por precisión (presence) + U acoplada
        presence = eps/(sigma**2 + 1e-6)
        mundo.H[2] = np.clip(mundo.H[2] + min(0.2, 0.15*max(0.0, z)) - 0.05, 0, 1.5)
        # aprendizaje EWC
        xb = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        yb = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        loss = (pred(xb)-yb).pow(2).mean() + 5.0/2*sum((fisher[k]*(p_-w_star[k])**2).sum() for k,p_ in pred.named_parameters())
        opt_pred.zero_grad(); loss.backward(); opt_pred.step()
        for k,p_ in pred.named_parameters():
            if p_.grad is not None: fisher[k] = 0.9*fisher[k]+0.1*p_.grad.detach()**2
        # boca: en sorpresa fuerte o incertidumbre alta (cooldown)
        if (z > 4.0 or (sigma > 0.25 and mundo.en_niebla())) and t - ultima_boca > 500:
            ultima_boca = t
            n_boca += 1
            try:
                interno = (f"Estado: energía={mundo.H[0]:.2f}, incertidumbre={mundo.H[2]:.2f}. "
                           f"Mi modelo predice que mi percepción es poco confiable (σ={sigma:.2f}). "
                           f"Evento: {'mi cuerpo cambió de posición de forma inconsistente con mi modelo' if violacion else 'me encuentro en una zona donde mis sentidos fallan'}.")
                frase = boca(interno)
                reportes.append((t, frase))
            except Exception as e:
                reportes.append((t, f"[boca no disponible]"))
        if mundo.en_niebla():
            tiempo_niebla += 1
        if t % 5000 == 0 and t > 0:
            print(f"  t={t}: E={mundo.H[0]:.2f} U={mundo.H[2]:.2f} S={mundo.H[3]:.2f} | z_max {z_max_ventana:.1f} | σ {sigma:.2f} | niebla {tiempo_niebla*100//t}% | E_mem {len(E_mem)} | boca {n_boca}", flush=True)
            z_max_ventana = 0
    print("="*78)
    print(f"{args.steps} pasos completados. E final {mundo.H[0]:.2f}, U {mundo.H[2]:.2f}, S {mundo.H[3]:.2f}")
    print(f"Tiempo en niebla: {tiempo_niebla/args.steps*100:.1f}% (con Φ acoplado, esperado ~15-20%: acción epistémica)")
    print(f"Violaciones: {n_viol} | memoria E: {len(E_mem)} | boca: {n_boca} reportes")
    print("Reportes de la boca (incluye estado de Φ):")
    for t, frase in reportes[:5]:
        print(f"  t={t}: {frase}")

if __name__ == "__main__":
    main()
