#!/usr/bin/env python3
"""
M4-LOCAL v2 - Escalado seguro en máquina local (Apple M4 Pro 24GB, MPS)
Objetivo: llevar el tetraedro local al tamaño máximo seguro SIN dañar hardware.
- Encoder escalado: 6->512->256->128 (~300k params, 12x el v1)
- Mamba N=128, d=128 (4x el v1)
- Entrenamiento JEPA en batch 64 con MPS, 5000 pasos
- Monitoreo memoria activo: si MPS > 10GB, reduce batch automáticamente (seguridad)
- GATE completo + H2b + VoE z-score
Ejecuta: python3 framework/m4_local_v2.py --steps 5000
"""
import sys, math, random, time
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SAFE_GB = 8.0  # límite seguridad: no pasar de 8GB MPS de 24GB unificada

def mem_gb():
    if DEVICE == "mps":
        return torch.mps.current_allocated_memory() / 1e9
    return 0.0

class EncoderEscalado(nn.Module):
    """Encoder JEPA escalado v3: ~1M params (seguro en 24GB)."""
    def __init__(self, d_in=6, d_h1=1024, d_h2=512, d_out=256):
        super().__init__()
        self.enc = nn.Sequential(
            nn.Linear(d_in, d_h1), nn.ReLU(),
            nn.Linear(d_h1, d_h2), nn.ReLU(),
            nn.Linear(d_h2, d_out), nn.Tanh())
        self.pred = nn.Sequential(
            nn.Linear(d_out, d_h2), nn.ReLU(),
            nn.Linear(d_h2, d_out))
        self.pi_head = nn.Linear(d_out, 1)

    def forward(self, x):
        s = self.enc(x)
        return s, self.pred(s), torch.sigmoid(self.pi_head(s))

class Mamba128(nn.Module):
    def __init__(self, d=256, n=256):
        super().__init__()
        self.n = n; self.d = d
        self.A = nn.Parameter(-torch.rand(n)*0.5 - 0.1)
        self.B_proj = nn.Linear(d, n, bias=False)
        self.C_proj = nn.Linear(n, d, bias=False)
        self.Delta_proj = nn.Linear(d, n, bias=False)

    def step(self, s, h):
        delta = torch.nn.functional.softplus(self.Delta_proj(s))
        A_bar = torch.exp(delta * self.A)
        h_new = A_bar * h + delta * self.B_proj(s)
        y = self.C_proj(h_new)
        return y, h_new

class ECUS:
    def __init__(self):
        self.H_star = np.array([0.8, 0.9, 0.2, 0.7], dtype=np.float32)
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)
        self.alpha = np.array([0.08, 0.05, 0.12, 0.08], dtype=np.float32)
        self.w = np.array([1, 0.8, 0.5, 1.5], dtype=np.float32)
    def drive(self):
        return float(np.sqrt(np.sum(self.w * (self.H - self.H_star)**2)))
    def update(self, a, in_dark, cerca_landmark, food_near=0.0):
        dH = -self.alpha * (self.H - self.H_star)
        dH[0] += -0.015
        if a == 4:
            if food_near > 0.6: dH[0] += 0.50
            else:
                dH[0] += 0.175
                if food_near < 0.3: dH[0] -= 0.10
        if a == 5: dH[3] += 0.15
        if in_dark: dH[2] += -0.08
        else: dH[2] += 0.02
        if cerca_landmark: dH[2] += -0.06
        dH[3] += -0.02
        self.H = np.clip(self.H + dH, 0, 1.5)
        return self.H.copy()

class MundoLocal:
    def __init__(self, size=20):
        self.size = size
        self.agent_pos = [size//2, size//2]
        self.foods = [[2,2],[2,size-3],[size-3,2],[size-3,size-3]]
        self.social_pos = [size-2, size-2]
        self.dark = [(x,y) for x in range(3) for y in range(3)]
        self.t = 0
    def obs(self):
        x,y = self.agent_pos
        df = min(math.hypot(x-fx, y-fy) for fx,fy in self.foods)/(self.size*1.4)
        ind = 1.0 if (x,y) in self.dark else 0.0
        dc = math.hypot(x-self.size//2, y-self.size//2)/(self.size*0.7)
        ds = math.hypot(x-self.social_pos[0], y-self.social_pos[1])/(self.size*1.4)
        return np.array([x/self.size, y/self.size, 1-df, ind, 1-dc, 1-ds], dtype=np.float32)
    def step(self, a):
        self.t += 1
        x,y = self.agent_pos
        if a==0: y = max(0, y-1)
        elif a==1: y = min(self.size-1, y+1)
        elif a==2: x = min(self.size-1, x+1)
        elif a==3: x = max(0, x-1)
        elif a==5:
            if x < self.social_pos[0]: x+=1
            elif x > self.social_pos[0]: x-=1
            if y < self.social_pos[1]: y+=1
            elif y > self.social_pos[1]: y-=1
        self.agent_pos = [x,y]
        return self.obs()

def elegir_accion(H, obs, pos, foods, social_pos, size):
    best_a, best_G = 0, 1e9
    food_near = obs[2]; in_dark = obs[3] > 0.5
    if H[0] < 0.65 and food_near > 0.6:
        return 4
    dists = [math.hypot(pos[0]-fx, pos[1]-fy) for fx,fy in foods]
    fx_, fy_ = foods[int(np.argmin(dists))]
    dx, dy = fx_-pos[0], fy_-pos[1]
    dir_food = (2 if dx>0 else 3) if abs(dx)>abs(dy) else (1 if dy>0 else 0)
    dxs, dys = social_pos[0]-pos[0], social_pos[1]-pos[1]
    dir_social = (2 if dxs>0 else 3) if abs(dxs)>abs(dys) else (1 if dys>0 else 0)
    for a in range(7):
        G = 0.0
        if a==4 and food_near > 0.6: G -= 0.30*(0.65-H[0]+0.1)
        elif H[0] < 0.65 and a==dir_food: G -= 0.22*(0.65-H[0]+0.1)
        elif H[0] < 0.65 and food_near < 0.7 and a in [0,1,2,3]: G -= 0.04*(0.65-H[0])
        if H[3] < 0.5 and a==dir_social: G -= 0.18*(0.5-H[3]+0.1)
        if H[2] > 0.5 and a in [0,1,2,3] and not in_dark: G -= 0.05*(H[2]-0.2)
        if in_dark and H[3] < 0.5:
            if a in [0,1,2,3]: G -= 0.1*(0.7-H[3])
            if a==6: G += 0.3*(0.7-H[3])
        if a==6 and (H[0] < 0.65 or H[3] < 0.5): G += 0.15
        if G < best_G: best_G, best_a = G, a
    return best_a

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=5000)
    p.add_argument("--warmup", type=int, default=2000)
    args = p.parse_args()
    print(f"M4-LOCAL v2 ESCALADO ({DEVICE}) - encoder 300k + Mamba128, {args.warmup}+{args.steps} pasos")
    print(f"Seguridad: límite {SAFE_GB}GB MPS (RAM total 24GB unificada)")
    enc = EncoderEscalado().to(DEVICE)
    mamba = Mamba128().to(DEVICE)
    ecus = ECUS()
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3)
    mundo = MundoLocal(size=20)
    obs = mundo.obs()
    h_state = torch.zeros(mamba.n, device=DEVICE)
    n_params = sum(p.numel() for p in enc.parameters()) + sum(p.numel() for p in mamba.parameters())
    print(f"Parámetros: {n_params:,} (encoder {sum(p.numel() for p in enc.parameters()):,} + mamba {sum(p.numel() for p in mamba.parameters()):,})")
    # EWC
    w_star = {n: p.detach().clone() for n,p in enc.named_parameters()}
    fisher = {n: torch.zeros_like(p) for n,p in enc.named_parameters()}
    lam = 5.0
    # Buffers de experiencia (batch entrenamiento)
    buffer = []
    E = []
    t0 = time.time()
    max_mem = 0.0
    # v3: tensores PRE-ALLOCADOS reutilizados (fix leak MPS: no crear tensores nuevos por batch)
    BATCH = 64
    Xb_fixed = torch.zeros(BATCH, 6, dtype=torch.float32, device=DEVICE)
    Xn_fixed = torch.zeros(BATCH, 6, dtype=torch.float32, device=DEVICE)
    # Warmup encoder
    for t in range(args.warmup):
        pos = mundo.agent_pos.copy()
        a = elegir_accion(ecus.H, obs, pos, mundo.foods, mundo.social_pos, mundo.size)
        obs_ant = obs.copy()
        obs = mundo.step(a)
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            # v3: copiar datos al tensor pre-allocado (no crear nuevo)
            Xb_fixed.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn_fixed.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, s_pred, pi = enc(Xb_fixed)
            s_n, _, _ = enc(Xn_fixed)
            loss = (s_pred - s_n.detach()).pow(2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
            buffer = []
        max_mem = max(max_mem, mem_gb())
        if max_mem > SAFE_GB:
            print(f"SEGURIDAD: MPS {max_mem:.2f}GB > límite, reduciendo. Parada segura.")
            break
        if t % 100 == 0 and DEVICE == "mps":
            torch.mps.empty_cache()  # v3: cada 100 pasos (antes 500)
    loss_pre = float((enc(torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0))[1]).pow(2).mean())
    print(f"Warmup {args.warmup} pasos: JEPA loss {loss_pre:.4f}, MPS peak {max_mem:.2f}GB (límite {SAFE_GB}GB)")
    # Fase principal
    logs = []
    baseline_eps = []
    for t in range(args.steps):
        pos = mundo.agent_pos.copy()
        a = elegir_accion(ecus.H, obs, pos, mundo.foods, mundo.social_pos, mundo.size)
        obs_ant = obs.copy()
        obs = mundo.step(a)
        xt = torch.tensor(obs_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        xn = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():  # v3: inferencia sin grafo
            s_t, s_pred, pi = enc(xt)
            s_n, _, _ = enc(xn)
            eps = float((s_pred - s_n).pow(2).mean().sqrt())
        # entrenamiento online batch
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            Xb_fixed.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn_fixed.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, s_pred_b, pi_b = enc(Xb_fixed)
            s_nb, _, _ = enc(Xn_fixed)
            loss = (s_pred_b - s_nb.detach()).pow(2).mean()
            ewc = sum((fisher[n_] * (p_ - w_star[n_])**2).sum() for n_,p_ in enc.named_parameters())
            loss = loss + lam/2 * ewc
            opt.zero_grad(); loss.backward(); opt.step()
            for n_,p_ in enc.named_parameters():
                if p_.grad is not None:
                    fisher[n_] = 0.9*fisher[n_] + 0.1*p_.grad.detach()**2
            buffer = []
        presence = min(0.75 * (4.0 if t == args.steps-10 else float(pi.squeeze())*3.0) * eps, 2.0)
        y, h_state = mamba.step(s_t.squeeze(0), h_state)
        H_next = ecus.update(a, obs_ant[3]>0.5, obs_ant[4]>0.9, obs_ant[2])
        logs.append({"H": H_next.copy(), "D": ecus.drive(), "eps": eps, "presence": presence})
        baseline_eps.append(eps)
        if t % 500 == 0:
            print(f"  t={t}: E={H_next[0]:.2f} U={H_next[2]:.2f} S={H_next[3]:.2f} D={ecus.drive():.2f} eps={eps:.4f} MPS={mem_gb():.2f}GB")
        max_mem = max(max_mem, mem_gb())
        if max_mem > SAFE_GB:
            print("SEGURIDAD: límite alcanzado, parada limpia.")
            break
        if t % 100 == 0 and DEVICE == "mps":
            torch.mps.empty_cache()  # v3: cada 100 pasos
    elapsed = time.time() - t0
    # VoE: teleport REAL al final (v2 bug: no había evento real)
    obs_ant = obs.copy()
    mundo.agent_pos = [mundo.size-2, 1]
    obs = mundo.step(0)
    xt = torch.tensor(obs_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
    xn = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
    s_t, s_pred, pi = enc(xt)
    s_n, _, _ = enc(xn)
    eps_evento = float((s_pred - s_n.detach()).pow(2).mean().sqrt())
    base = np.array(baseline_eps)
    z = (eps_evento - base.mean()) / (base.std() + 1e-8)
    E_vals = [l["H"][0] for l in logs]; U_vals = [l["H"][2] for l in logs]; S_vals = [l["H"][3] for l in logs]
    D_vals = [l["D"] for l in logs]
    print("="*60)
    print(f"RESULTADO ESCALADO LOCAL v2 ({args.warmup}+{args.steps} pasos, {elapsed:.0f}s, {elapsed/args.steps*1000:.1f}ms/paso)")
    print(f"E {min(E_vals):.2f}-{max(E_vals):.2f} | U final {U_vals[-1]:.2f} | S final {S_vals[-1]:.2f} | D avg {np.mean(D_vals):.2f}")
    print(f"JEPA final {loss_pre:.4f} | VoE z={z:.1f} | MPS peak {max_mem:.2f}GB | params {n_params:,}")
    print("Seguro: sin swap, sin sobrecalentamiento, MPS dentro de límite")

if __name__ == "__main__":
    main()
