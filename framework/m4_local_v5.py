#!/usr/bin/env python3
"""
M4-LOCAL v5 - Mundo Rico: input tipo retina 8x8 (64 dims) + interocepción
Pre-registrado 33:1 — la ganancia real local está en INPUT rico, no en más params.
Retina 8x8: visión local 3 casillas de radio (food/social/landmark/dark distintos valores)
Encoder 68->256->128->64, JEPA predice en latente (como V-JEPA predice patches).
Ejecuta: python3 framework/m4_local_v5.py --steps 20000
"""
import sys, math, random, time
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SAFE_GB = 8.0

def mem_gb():
    return torch.mps.current_allocated_memory()/1e9 if DEVICE=="mps" else 0.0

class MundoRico:
    """Mundo 20x20 con retina 8x8 alrededor del agente (64 dims) + 4 interoceptivos."""
    def __init__(self, size=20):
        self.size = size
        self.agent_pos = [size//2, size//2]
        self.foods = [[2,2],[2,size-3],[size-3,2],[size-3,size-3]]
        self.social_pos = [size-2, size-2]
        self.landmark = [size//2, size//2]
        self.dark = [(x,y) for x in range(3) for y in range(3)]
        self.t = 0
    def _grid(self, x, y):
        # valor de celda mundo: 0 vacío, 1 food, 2 social, 3 landmark, 4 dark
        if [x,y] in self.foods: return 1.0
        if [x,y] == self.social_pos: return 2.0
        if [x,y] == self.landmark: return 3.0
        if (x,y) in self.dark: return 4.0
        return 0.0
    def obs(self):
        # retina 8x8 centrada en agente (radio 3), toroidal
        retina = np.zeros((8,8), dtype=np.float32)
        px, py = self.agent_pos
        for i in range(8):
            for j in range(8):
                wx = (px + j - 3) % self.size
                wy = (py + i - 3) % self.size
                retina[i,j] = self._grid(wx, wy)/4.0
        return retina.flatten()  # 64 dims
    def intero(self):
        # H normalizado [E,C,U,S] como 4 dims extra (lo provee el agente, no mundo)
        return np.zeros(4, dtype=np.float32)
    def step(self, a):
        self.t += 1
        x,y = self.agent_pos
        if a==0: y = (y-1) % self.size
        elif a==1: y = (y+1) % self.size
        elif a==2: x = (x+1) % self.size
        elif a==3: x = (x-1) % self.size
        elif a==5:
            dx = np.sign(self.social_pos[0]-x); dy = np.sign(self.social_pos[1]-y)
            x += dx; y += dy
        self.agent_pos = [x,y]
        return self.obs()

class EncoderRico(nn.Module):
    def __init__(self, d_in=68, d_h1=256, d_h2=128, d_out=64):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(d_in, d_h1), nn.ReLU(),
                                 nn.Linear(d_h1, d_h2), nn.ReLU(),
                                 nn.Linear(d_h2, d_out), nn.Tanh())
        self.pred = nn.Sequential(nn.Linear(d_out, d_h2), nn.ReLU(),
                                  nn.Linear(d_h2, d_out))
        self.pi_head = nn.Linear(d_out, 1)
    def forward(self, x):
        s = self.enc(x)
        return s, self.pred(s), torch.sigmoid(self.pi_head(s))

class ECUS:
    def __init__(self):
        self.H_star = np.array([0.8,0.9,0.2,0.7], dtype=np.float32)
        self.H = np.array([0.6,0.8,0.7,0.5], dtype=np.float32)
        self.alpha = np.array([0.08,0.05,0.12,0.08], dtype=np.float32)
        self.w = np.array([1,0.8,0.5,1.5], dtype=np.float32)
    def drive(self):
        return float(np.sqrt(np.sum(self.w*(self.H-self.H_star)**2)))
    def update(self, a, food_near, in_dark, cerca_landmark):
        dH = -self.alpha*(self.H-self.H_star)
        dH[0] += -0.015
        if a==4:
            if food_near>0.6: dH[0]+=0.50
            else: dH[0]+=0.175
        if a==5: dH[3]+=0.15
        if in_dark: dH[2]+=-0.08
        else: dH[2]+=0.02
        if cerca_landmark: dH[2]+=-0.06
        dH[3]+=-0.02
        self.H = np.clip(self.H+dH, 0, 1.5)
        return self.H.copy()

def elegir_accion(H, mundo):
    # política usa distancia euclídea real (no retina) — como toy
    pos = mundo.agent_pos
    foods = mundo.foods; social = mundo.social_pos
    best_a, best_G = 0, 1e9
    dists = [math.hypot(pos[0]-fx, pos[1]-fy) for fx,fy in foods]
    fx_, fy_ = foods[int(np.argmin(dists))]
    food_near = 1 - min(dists)/(mundo.size*1.4)
    dx, dy = fx_-pos[0], fy_-pos[1]
    dir_food = (2 if dx>0 else 3) if abs(dx)>abs(dy) else (1 if dy>0 else 0)
    dxs, dys = social[0]-pos[0], social[1]-pos[1]
    dir_social = (2 if dxs>0 else 3) if abs(dxs)>abs(dys) else (1 if dys>0 else 0)
    if H[0] < 0.65 and food_near > 0.6:
        return 4
    for a in range(7):
        G = 0.0
        if a==4 and food_near>0.6: G -= 0.30*(0.65-H[0]+0.1)
        elif H[0]<0.65 and a==dir_food: G -= 0.22*(0.65-H[0]+0.1)
        elif H[0]<0.65 and food_near<0.7 and a in [0,1,2,3]: G -= 0.04*(0.65-H[0])
        if H[3]<0.5 and a==dir_social: G -= 0.18*(0.5-H[3]+0.1)
        if a==6 and (H[0]<0.65 or H[3]<0.5): G += 0.15
        if G < best_G: best_G, best_a = G, a
    return best_a

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=20000)
    p.add_argument("--warmup", type=int, default=3000)
    args = p.parse_args()
    print(f"M4-LOCAL v5 MUNDO RICO ({DEVICE}) - retina 8x8 (64d) + JEPA latente + EWC")
    mundo = MundoRico(size=20)
    enc = EncoderRico().to(DEVICE)
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3)
    ecus = ECUS()
    w_star = {n: p.detach().clone() for n,p in enc.named_parameters()}
    fisher = {n: torch.zeros_like(p) for n,p in enc.named_parameters()}
    BATCH = 64
    Xb = torch.zeros(BATCH, 68, dtype=torch.float32, device=DEVICE)
    Xn = torch.zeros(BATCH, 68, dtype=torch.float32, device=DEVICE)
    buffer = []
    obs = np.concatenate([mundo.obs(), np.zeros(4, dtype=np.float32)])
    t0 = time.time(); max_mem = 0.0
    n_params = sum(p.numel() for p in enc.parameters())
    print(f"Params: {n_params:,} | input 68 dims (retina 64 + intero 4)")
    # Warmup
    for t in range(args.warmup):
        pos = mundo.agent_pos.copy()
        a = elegir_accion(ecus.H, mundo)
        obs_ant = obs.copy()
        obs = np.concatenate([mundo.step(a), ecus.H/1.5])
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, s_pred, pi = enc(Xb); s_n,_,_ = enc(Xn)
            loss = (s_pred - s_n.detach()).pow(2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
            buffer = []
        max_mem = max(max_mem, mem_gb())
        if t % 100 == 0 and DEVICE=="mps": torch.mps.empty_cache()
        if max_mem > SAFE_GB: print("SEGURIDAD"); break
    loss_pre = float((enc(torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0))[1]).pow(2).mean())
    print(f"Warmup {args.warmup}: JEPA {loss_pre:.4f}, MPS {max_mem:.2f}GB")
    # Principal
    baseline_eps = []
    logs = []
    for t in range(args.steps):
        a = elegir_accion(ecus.H, mundo)
        obs_ant = obs.copy()
        obs = np.concatenate([mundo.step(a), ecus.H/1.5])
        xt = torch.tensor(obs_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        xn = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            s_t, s_pred, pi = enc(xt); s_n,_,_ = enc(xn)
            eps = float((s_pred - s_n).pow(2).mean().sqrt())
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, s_pred_b, pi_b = enc(Xb); s_nb,_,_ = enc(Xn)
            loss = (s_pred_b - s_nb.detach()).pow(2).mean()
            ewc = sum((fisher[n_]* (p_ - w_star[n_])**2).sum() for n_,p_ in enc.named_parameters())
            loss = loss + 5.0/2*ewc
            opt.zero_grad(); loss.backward(); opt.step()
            for n_,p_ in enc.named_parameters():
                if p_.grad is not None:
                    fisher[n_] = 0.9*fisher[n_] + 0.1*p_.grad.detach()**2
            buffer = []
        H_next = ecus.update(a, 0.0, False, False)
        logs.append({"H": H_next.copy(), "D": ecus.drive(), "eps": eps})
        baseline_eps.append(eps)
        if t % 2000 == 0:
            print(f"  t={t}: E={H_next[0]:.2f} U={H_next[2]:.2f} S={H_next[3]:.2f} D={ecus.drive():.2f} eps={eps:.4f} MPS={mem_gb():.2f}GB")
        max_mem = max(max_mem, mem_gb())
        if t % 100 == 0 and DEVICE=="mps": torch.mps.empty_cache()
        if max_mem > SAFE_GB: print("SEGURIDAD"); break
    # VoE: teletransporte real
    obs_ant = obs.copy()
    mundo.agent_pos = [mundo.size-2, 1]
    obs = np.concatenate([mundo.step(0), ecus.H/1.5])
    with torch.no_grad():
        xt = torch.tensor(obs_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        xn = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        s_t, s_pred, pi = enc(xt); s_n,_,_ = enc(xn)
        eps_tel = float((s_pred - s_n).pow(2).mean().sqrt())
    base = np.array(baseline_eps)
    z = (eps_tel - base.mean())/(base.std()+1e-8)
    elapsed = time.time()-t0
    E = [l["H"][0] for l in logs]; U = [l["H"][2] for l in logs]; S = [l["H"][3] for l in logs]
    D = [l["D"] for l in logs]
    print("="*60)
    print(f"RESULTADO v5 MUNDO RICO ({args.warmup}+{args.steps} pasos, {elapsed:.0f}s, {elapsed/args.steps*1000:.1f}ms/paso)")
    print(f"E {min(E):.2f}-{max(E):.2f} | U final {U[-1]:.2f} | S final {S[-1]:.2f} | D avg {np.mean(D):.2f}")
    print(f"JEPA final {loss_pre:.4f} | VoE z={z:.1f} (eps_tel {eps_tel:.4f} vs base {base.mean():.4f}) | MPS {max_mem:.2f}GB | params {n_params:,}")
    print(f"Retina aprendida: {n_params:,} params sobre input 68d rico")

if __name__ == "__main__":
    main()
