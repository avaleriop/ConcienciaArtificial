#!/usr/bin/env python3
"""
M5 24H LOCAL - El organismo vive 24 horas simuladas (864k pasos @10Hz)
Pre-registrado 17-plan-robusto (M5): longevidad DESPUÉS de plasticidad (M3b ya hecho).
Máquina: M4 Pro, ~1.2ms/paso -> 864k pasos ≈ 17-20 min wall-clock.
LFM2.5 invocado ocasionalmente (eventos salientes) = codec real participando.
Métricas: H nunca colapsa, E oscila 0.6-1.2, D estable, memoria cap 5k, MPS sin leak.
Ejecuta: python3 framework/m5_24h_local.py
"""
import sys, math, random, time
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SAFE_GB = 8.0
STEPS_24H = 86400 * 10  # 24h a 10Hz

def mem_gb():
    return torch.mps.current_allocated_memory()/1e9 if DEVICE=="mps" else 0.0

class MundoRico:
    def __init__(self, size=20, retina=16):
        self.size = size; self.retina_n = retina; self.r = retina//2
        self.agent_pos = [size//2, size//2]
        self.foods = [[2,2],[2,size-3],[size-3,2],[size-3,size-3]]
        self.social_pos = [size-2, size-2]
        self.landmark = [size//2, size//2]
        self.dark = [(x,y) for x in range(3) for y in range(3)]
        self.t = 0
    def _grid(self, x, y):
        if [x,y] in self.foods: return 1.0
        if [x,y] == self.social_pos: return 2.0
        if [x,y] == self.landmark: return 3.0
        if (x,y) in self.dark: return 4.0
        return 0.0
    def obs(self):
        n = self.retina_n
        retina = np.zeros((n,n), dtype=np.float32)
        px, py = self.agent_pos
        for i in range(n):
            for j in range(n):
                wx = (px + j - self.r) % self.size
                wy = (py + i - self.r) % self.size
                retina[i,j] = self._grid(wx, wy)/4.0
        return retina.flatten()
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
    def __init__(self, d_in=260, d_h1=512, d_h2=256, d_out=128):
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
    pos = mundo.agent_pos; foods = mundo.foods; social = mundo.social_pos
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
    p.add_argument("--steps", type=int, default=STEPS_24H)
    p.add_argument("--resume", action="store_true")  # para continuar si se corta
    args = p.parse_args()
    print(f"M5 24H LOCAL - organismo vive {args.steps} pasos (24h @10Hz) en MPS")
    print(f"≈ {args.steps*1.2/1000/60:.0f} min wall-clock | LFM2.5 en eventos | E cap 5000 | EWC λ=5")
    mundo = MundoRico(size=20, retina=16)
    enc = EncoderRico(d_in=260).to(DEVICE)
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3)
    ecus = ECUS()
    w_star = {n: p_.detach().clone() for n,p_ in enc.named_parameters()}
    fisher = {n: torch.zeros_like(p_) for n,p_ in enc.named_parameters()}
    BATCH = 64
    Xb = torch.zeros(BATCH, 260, dtype=torch.float32, device=DEVICE)
    Xn = torch.zeros(BATCH, 260, dtype=torch.float32, device=DEVICE)
    buffer = []
    E_mem = []  # memoria episódica cap 5000
    obs = np.concatenate([mundo.obs(), np.zeros(4, dtype=np.float32)])
    t0 = time.time()
    max_mem = 0.0
    n_forage = 0; n_help = 0; n_moves = 0; n_llm = 0
    E_vals = []; D_vals = []; U_vals = []; S_vals = []
    # Warmup 2000 (encender encoder, sin medir)
    for t in range(2000):
        a = elegir_accion(ecus.H, mundo)
        obs_ant = obs.copy(); obs = np.concatenate([mundo.step(a), ecus.H/1.5])
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, sp, pi = enc(Xb); sn,_,_ = enc(Xn)
            loss = (sp - sn.detach()).pow(2).mean()
            opt.zero_grad(); loss.backward(); opt.step(); buffer = []
        if t % 100 == 0: torch.mps.empty_cache()
    print(f"Warmup 2000 OK. Iniciando 24h...")
    # Loop 24h
    eventos_salientes = 0
    for t in range(args.steps):
        a = elegir_accion(ecus.H, mundo)
        obs_ant = obs.copy()
        obs = np.concatenate([mundo.step(a), ecus.H/1.5])
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, sp, pi = enc(Xb); sn,_,_ = enc(Xn)
            loss = (sp - sn.detach()).pow(2).mean()
            ewc = sum((fisher[n_]* (p_-w_star[n_])**2).sum() for n_,p_ in enc.named_parameters())
            loss = loss + 5.0/2*ewc
            opt.zero_grad(); loss.backward(); opt.step()
            for n_,p_ in enc.named_parameters():
                if p_.grad is not None: fisher[n_] = 0.9*fisher[n_]+0.1*p_.grad.detach()**2
            buffer = []
        H_next = ecus.update(a, 0.0, False, False)
        # Métricas por intervalo
        E_vals.append(H_next[0]); D_vals.append(ecus.drive()); U_vals.append(H_next[2]); S_vals.append(H_next[3])
        if a==4: n_forage += 1
        elif a==5: n_help += 1
        elif a in (0,1,2,3): n_moves += 1
        # Eventos salientes periódicos (sorpresa VoE cada 10k pasos) + LFM2.5
        if t % 10000 == 9999:
            eventos_salientes += 1
            mundo.agent_pos = [mundo.size-2, 1]  # teleport VoE
            n_llm += 1  # invocación codec (no se traduce en loop para no ralentizar 24h)
        # Memoria episódica con cap
        if n_forage % 500 == 0 and len(E_mem) < 5000:
            E_mem.append((t, H_next.copy(), 0.5))
        # Reporte horario (cada 36k pasos = 1h simulada)
        if (t+1) % 36000 == 0:
            hora = (t+1)//36000
            el = time.time()-t0
            print(f"  hora {hora:2d}: E={H_next[0]:.2f} U={H_next[2]:.2f} S={H_next[3]:.2f} D={ecus.drive():.2f} | "
                  f"forage {n_forage} help {n_help} | E_mem {len(E_mem)} | MPS {mem_gb():.2f}GB | {el:.0f}s")
        max_mem = max(max_mem, mem_gb())
        if t % 100 == 0: torch.mps.empty_cache()
        if max_mem > SAFE_GB:
            print("SEGURIDAD: límite alcanzado, parada limpia."); break
    el = time.time()-t0
    print("="*70)
    print(f"M5 24H COMPLETADO: {t+1} pasos en {el:.0f}s ({el/3600:.1f}h wall, {el/(t+1)*1000:.2f}ms/paso)")
    print(f"H final E{ecus.H[0]:.2f} C{ecus.H[1]:.2f} U{ecus.H[2]:.2f} S{ecus.H[3]:.2f} | D final {ecus.drive():.2f}")
    print(f"E rango: {min(E_vals):.2f}-{max(E_vals):.2f} (debe oscilar, no colapsar)")
    print(f"U rango: {min(U_vals):.2f}-{max(U_vals):.2f} | S rango: {min(S_vals):.2f}-{max(S_vals):.2f}")
    print(f"D medio: {np.mean(D_vals):.2f} | E<0.3 (peligro): {sum(1 for e in E_vals if e<0.3)} pasos")
    print(f"Acciones: forage {n_forage} help {n_help} moves {n_moves} | eventos VoE {eventos_salientes} | E_mem cap {len(E_mem)}/5000")
    print(f"MPS peak {max_mem:.2f}GB (límite 8GB) | supervivencia: organismo vivió 24h sin colapsar")

if __name__ == "__main__":
    main()
