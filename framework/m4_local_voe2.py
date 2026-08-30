#!/usr/bin/env python3
"""
VoE-v2 EMERGENTE v3 - física de movimiento aprendida con 2 frames (velocidad inferible)
Pre-registrado: 34:1, 35:1, 39:1. Sin flag: la sorpresa es el error de predicción del modelo.
Diseño:
  Entrada x_t = [frame_{t-1}, frame_t] (520d) -> la VELOCIDAD de los objetos es inferible.
  Target   = EMA_enc([frame_t, frame_{t+1}]) -> el predictor aprende continuidad de movimiento.
  F1: warmup con física normal (objetos con velocidad continua).
  F2: medir ε: base (física normal) vs imposible (teletransporte viola continuidad).
  F3: habituación (repetir imposibles CON entrenamiento -> ¿aprende la nueva física?).
Ejecuta: python3 framework/m4_local_voe2.py
"""
import sys, math, random, time
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

def mem_gb():
    return torch.mps.current_allocated_memory()/1e9 if DEVICE=="mps" else 0.0

class MundoObjetos:
    def __init__(self, size=20, retina=16):
        self.size = size; self.retina_n = retina; self.r = retina//2
        self.agent_pos = [size//2, size//2]
        self.foods = [[3,3],[3,size-4],[size-4,3],[size-4,size-4]]
        self.vels = [[1,1],[1,-1],[-1,1],[-1,-1]]
        self.social_pos = [size-2, size-2]
    def _grid(self, x, y):
        if [x,y] in self.foods: return 1.0
        if [x,y] == self.social_pos: return 2.0
        return 0.0
    def obs(self):
        n = self.retina_n
        retina = np.zeros((n,n), dtype=np.float32)
        px, py = self.agent_pos
        for i in range(n):
            for j in range(n):
                wx = (px + j - self.r) % self.size
                wy = (py + i - self.r) % self.size
                retina[i,j] = self._grid(wx, wy)/2.0  # normalizado [0,1]
        return retina.flatten()
    def avanzar_fisica(self):
        # Física DETERMINISTA: velocidad constante, sin cambios aleatorios.
        # Con 2 frames, la velocidad es inferible -> la física es predecible.
        for i in range(4):
            fx, fy = self.foods[i]; vx, vy = self.vels[i]
            self.foods[i] = [(fx+vx)%self.size, (fy+vy)%self.size]
    def teleportar(self, idx):
        self.foods[idx] = [(self.foods[idx][0]+10)%self.size,
                           (self.foods[idx][1]+10)%self.size]

class EncoderRico(nn.Module):
    def __init__(self, d_in=128, d_h1=512, d_h2=512, d_out=256):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(d_in, d_h1), nn.ReLU(),
                                 nn.Linear(d_h1, d_h2), nn.ReLU(),
                                 nn.Linear(d_h2, d_out), nn.ReLU())
        self.pred = nn.Sequential(nn.Linear(d_out, d_h2), nn.ReLU(),
                                  nn.Linear(d_h2, d_out))
        self.pi_head = nn.Linear(d_out, 1)
    def forward(self, x):
        s = self.enc(x)
        return s, self.pred(s), torch.sigmoid(self.pi_head(s))

def entrenar_batch(enc, target_enc, opt, Xb, Xn, fisher, w_star, lam=5.0, tau=0.99, lam_var=1.0):
    s, s_pred, pi = enc(Xb)
    with torch.no_grad():
        s_target = target_enc.enc(Xn)
    loss_pred = (s_pred - s_target).pow(2).mean()
    s_center = s - s.mean(0, keepdim=True)
    loss_var = torch.clamp(1.0 - (s_center**2).mean(), min=0.0)
    ewc = sum((fisher[n_]* (p_-w_star[n_])**2).sum() for n_,p_ in enc.named_parameters())
    loss = loss_pred + lam/2*ewc + lam_var*loss_var
    opt.zero_grad(); loss.backward(); opt.step()
    for n_,p_ in enc.named_parameters():
        if p_.grad is not None: fisher[n_] = 0.9*fisher[n_]+0.1*p_.grad.detach()**2
    for p, pt in zip(enc.parameters(), target_enc.parameters()):
        pt.data.mul_(tau).add_(p.data, alpha=1-tau)
    return float(loss_pred)

def main():
    print(f"VoE-v2 EMERGENTE v3 - 2 frames, velocidad inferible (MPS)")
    print("="*60)
    mundo = MundoObjetos(size=20, retina=8)
    enc = EncoderRico(d_in=128).to(DEVICE)
    target_enc = EncoderRico(d_in=128).to(DEVICE)
    target_enc.load_state_dict(enc.state_dict())
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3)
    w_star = {n: p.detach().clone() for n,p in enc.named_parameters()}
    fisher = {n: torch.zeros_like(p) for n,p in enc.named_parameters()}
    BATCH = 64
    Xb = torch.zeros(BATCH, 128, dtype=torch.float32, device=DEVICE)
    Xn = torch.zeros(BATCH, 128, dtype=torch.float32, device=DEVICE)
    buffer = []
    # frames
    f0 = mundo.obs(); f1 = mundo.obs()
    def par(a, b): return np.concatenate([a, b])
    def frame_sig():
        mundo.avanzar_fisica(); return mundo.obs()
    # F1: warmup 6000 con física normal (velocidad continua)
    for t in range(6000):
        f2 = frame_sig()
        buffer.append((par(f0, f1), par(f1, f2)))  # entrada par_t, target par_{t+1}
        f0, f1 = f1, f2
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            l = entrenar_batch(enc, target_enc, opt, Xb, Xn, fisher, w_star)
            buffer = []
        if t % 100 == 0: torch.mps.empty_cache()
    # separabilidad
    with torch.no_grad():
        a1 = par(mundo.obs(), frame_sig())
        a2 = par(mundo.obs(), frame_sig())
        s1 = enc(torch.tensor(a1, dtype=torch.float32, device=DEVICE).unsqueeze(0))[0]
        s2 = enc(torch.tensor(a2, dtype=torch.float32, device=DEVICE).unsqueeze(0))[0]
        sep = float((s1-s2).pow(2).mean().sqrt())
    print(f"F1 warmup 6000 OK | separación latente entre mundos: {sep:.3f} (anti-colapso activo)")
    # F2: medición sin entrenar
    def eps_trial(tipo):
        a = par(mundo.obs(), frame_sig())  # entrada: par actual
        b = par(mundo.obs(), frame_sig())  # target: par siguiente (física normal)
        if tipo == 'imposible':
            mundo.teleportar(random.randrange(4))  # viola continuidad
        b = par(mundo.obs(), frame_sig())
        with torch.no_grad():
            xt = torch.tensor(a, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            xn = torch.tensor(b, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            s_t, s_pred, pi = enc(xt); s_n,_,_ = enc(xn)
            return float((s_pred - s_n).pow(2).mean().sqrt())
    res = {"base": [], "imposible": []}
    for trial in range(100):
        res["base"].append(eps_trial("base"))
        res["imposible"].append(eps_trial("imposible"))
    base = np.array(res["base"]); imp = np.array(res["imposible"])
    z = (imp.mean() - base.mean()) / (base.std()+1e-8)
    print(f"F2 medición (sin flag):")
    print(f"  física normal ε: {base.mean():.5f} ± {base.std():.5f}")
    print(f"  teletransporte ε: {imp.mean():.5f} (z={z:.1f})")
    print(f"  => {'EMERGENTE CONFIRMADO (violación de continuidad detectada por el modelo)' if z > 5 else 'no separa aún'}")
    # F3: habituación (imposibles repetidos CON entrenamiento)
    eps_hab = []
    for k in range(50):
        a = par(mundo.obs(), frame_sig())
        mundo.teleportar(random.randrange(4))
        b = par(mundo.obs(), frame_sig())
        buffer.append((a, b))
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            entrenar_batch(enc, target_enc, opt, Xb, Xn, fisher, w_star)
            buffer = []
        with torch.no_grad():
            xt = torch.tensor(a, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            xn = torch.tensor(b, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            s_t, s_pred, pi = enc(xt); s_n,_,_ = enc(xn)
            eps_hab.append(float((s_pred - s_n).pow(2).mean().sqrt()))
    p10 = np.mean(eps_hab[:10]); u10 = np.mean(eps_hab[-10:])
    print(f"F3 habituación: ε primeras 10={p10:.4f} -> últimas 10={u10:.4f} (decaída {100*(1-u10/p10):.0f}%)")
    print(f"  => {'HABITUACIÓN (el modelo actualizó su física: aprendió a esperar teletransportes)' if u10 < p10*0.7 else 'sin habituación clara'}")

if __name__ == "__main__":
    main()
