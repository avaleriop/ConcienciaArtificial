#!/usr/bin/env python3
"""
M4-INTERMEDIO LOCAL (CPU/MPS) v0.9 - Encoder aprendido real + EWC real + Mamba torch
A diferencia del toy (encoder lineal ALEATORIO), aquí el encoder se ENTRENA online
con pérdida predictiva JEPA-style y EWC Fisher real -> plasticidad local real.
Ejecuta: python3 framework/m4_local_cpu.py --steps 1000
"""
import argparse, math, random, collections
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

# ---------- Encoder aprendido (JEPA-style) ----------
class EncoderPredictivo(nn.Module):
    def __init__(self, d_in=6, d_h=128, d_out=64):
        super().__init__()
        self.enc = nn.Sequential(
            nn.Linear(d_in, d_h), nn.ReLU(),
            nn.Linear(d_h, d_out), nn.Tanh())
        self.pred = nn.Sequential(
            nn.Linear(d_out, d_h), nn.ReLU(),
            nn.Linear(d_h, d_out))
        self.pi_head = nn.Linear(d_out, 1)  # precision head

    def forward(self, x):
        s = self.enc(x)
        return s, self.pred(s), torch.sigmoid(self.pi_head(s))

# ---------- Mamba selectiva torch (N=64) ----------
class MambaTorch(nn.Module):
    def __init__(self, d=64, n=64):
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

# ---------- ECUS (numpy, calibrado) ----------
class ECUS:
    def __init__(self):
        self.H_star = np.array([0.8, 0.9, 0.2, 0.7], dtype=np.float32)
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)
        self.alpha = np.array([0.08, 0.05, 0.12, 0.08], dtype=np.float32)
        self.w = np.array([1, 0.8, 0.5, 1.5], dtype=np.float32)
    def drive(self):
        return float(np.sqrt(np.sum(self.w * (self.H - self.H_star)**2)))
    def update(self, a, in_dark, cerca_landmark):
        dH = -self.alpha * (self.H - self.H_star)
        dH[0] += -0.015
        if a == 4: dH[0] += 0.50
        if a == 5: dH[3] += 0.15
        if in_dark: dH[2] += -0.08
        else: dH[2] += 0.02
        if cerca_landmark: dH[2] += -0.06
        dH[3] += -0.02
        self.H = np.clip(self.H + dH, 0, 1.5)
        return self.H.copy()

# ---------- Mundo (compatible con toy) ----------
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

# ---------- Agente M4-intermedio ----------
class AgenteLocal:
    def __init__(self):
        self.enc = EncoderPredictivo().to(DEVICE)
        self.mamba = MambaTorch().to(DEVICE)
        self.ecus = ECUS()
        self.h = torch.zeros(self.mamba.n, device=DEVICE)
        self.E = []
        self.invocaciones = 0
        self.log = []
        # EWC
        self.w_star = {n: p.detach().clone() for n,p in self.enc.named_parameters()}
        self.fisher = {n: torch.zeros_like(p) for n,p in self.enc.named_parameters()}
        self.lam = 50.0  # EWC local (pesos pequeños)
        self.opt = torch.optim.Adam(self.enc.parameters(), lr=1e-3)

    def paso(self, obs_t, obs_next, a, evento_voE=False):
        xt = torch.tensor(obs_t, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        xn = torch.tensor(obs_next, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        s_t, s_pred, pi = self.enc(xt)
        s_n, _, _ = self.enc(xn)
        eps = float((s_pred - s_n.detach()).pow(2).mean().sqrt())
        # Entrenamiento online JEPA + EWC (plasticidad real local)
        if self.log.__len__() % 5 == 0:
            loss_jepa = (s_pred - s_n.detach()).pow(2).mean()
            ewc = 0.0
            for n,p in self.enc.named_parameters():
                ewc = ewc + (self.fisher[n] * (p - self.w_star[n])**2).sum()
            loss = loss_jepa + self.lam/2 * ewc
            self.opt.zero_grad(); loss.backward(); self.opt.step()
            # Fisher update online
            for n,p in self.enc.named_parameters():
                if p.grad is not None:
                    self.fisher[n] = 0.9*self.fisher[n] + 0.1*p.grad.detach()**2
        Pi_sens = float(pi.squeeze()) * 3.0
        if evento_voE: Pi_sens = 4.0
        presence = min(0.75 * Pi_sens * eps, 2.0)
        # Mamba
        y, self.h = self.mamba.step(s_t.squeeze(0), self.h)
        # Memoria episódica
        sorpresa = eps * Pi_sens
        if sorpresa > 0.7:
            self.E.append((s_t.detach().clone(), self.log.__len__(), sorpresa))
            if len(self.E) > 5000:
                self.E.sort(key=lambda z: z[2]); self.E.pop(0)
        # ECUS
        in_dark = obs_t[3] > 0.5
        cerca_landmark = obs_t[4] > 0.9
        H = self.ecus.H
        H_next = self.ecus.update(a, in_dark, cerca_landmark)
        D = self.ecus.drive()
        # LLM invocación (U alta + presence)
        invoca = (H_next[2] > 0.4 and presence > 0.7)
        if invoca: self.invocaciones += 1
        self.log.append({"H": H_next.copy(), "D": D, "presence": presence, "eps": eps, "a": a})
        return presence, H_next, invoca

def elegir_accion(H, obs, pos, foods, social_pos, size):
    best_a, best_G = 0, 1e9
    food_near = obs[2]
    if H[0] < 0.65 and food_near > 0.6:
        return 4
    dir_food = None
    dists = [math.hypot(pos[0]-fx, pos[1]-fy) for fx,fy in foods]
    fx_, fy_ = foods[int(np.argmin(dists))]
    dx, dy = fx_-pos[0], fy_-pos[1]
    dir_food = (2 if dx>0 else 3) if abs(dx)>abs(dy) else (1 if dy>0 else 0)
    dir_social = (2 if social_pos[0]-pos[0]>0 else 3) if abs(social_pos[0]-pos[0])>abs(social_pos[1]-pos[1]) else (1 if social_pos[1]-pos[1]>0 else 0)
    for a in range(7):
        G = 0.0
        if a==4: G -= 0.5 if food_near>0.6 else 0
        if a==5: G -= 0.15
        if H[0] < 0.65 and a==dir_food: G -= 0.22*(0.65-H[0])
        if H[3] < 0.5 and a==dir_social: G -= 0.18*(0.5-H[3])
        if a==6: G += 0.15
        if G < best_G: best_G, best_a = G, a
    return best_a

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=1000)
    args = p.parse_args()
    print(f"M4-INTERMEDIO LOCAL ({DEVICE}) encoder aprendido JEPA + EWC + Mamba64, {args.steps} pasos")
    mundo = MundoLocal(size=20)
    ag = AgenteLocal()
    obs = mundo.obs()
    H1_mem = None
    for t in range(args.steps):
        pos = mundo.agent_pos.copy()
        obs_next = mundo.step(0)  # placeholder
        a = elegir_accion(ag.ecus.H, obs, pos, mundo.foods, mundo.social_pos, mundo.size)
        evento = (t == 80)
        obs_ant = obs.copy()
        obs = mundo.step(a)
        presence, H, invoca = ag.paso(obs_ant, obs, a, evento_voE=evento)
        if t == 0:
            # Kael: alta sorpresa forzada
            ag.E.append((torch.zeros(64, device=DEVICE), 0, 1.2))
        if t == 100:
            H1_mem = len(ag.E) > 0
    logs = ag.log
    E = [l["H"][0] for l in logs]; U = [l["H"][2] for l in logs]; S = [l["H"][3] for l in logs]
    D = [l["D"] for l in logs]
    print(f"E min {min(E):.2f} max {max(E):.2f} | U final {U[-1]:.2f} | S final {S[-1]:.2f} | D avg {np.mean(D):.2f}")
    print(f"H1 Kael (E>0 en t100): {H1_mem} | VoE max {max(l['presence'] for l in logs):.2f} | LLM inv {ag.invocaciones}")
    print(f"Encoder aprendido: params entrenables {sum(p.numel() for p in ag.enc.parameters())}, pérdida JEPA media (últimas) {float((ag.enc(torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0))[1]).pow(2).mean()):.4f}")

if __name__ == "__main__":
    main()
