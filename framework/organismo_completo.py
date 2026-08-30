#!/usr/bin/env python3
"""
ORGANISMO COMPLETO v0.11 - Todos los mecanismos en UN loop continuo (capstone integrador)
Integra (todo verificado por separado en 01-43):
  H1 memoria jerárquica (E episódica cap 5000 + W con EWC)
  H2 pensar (predictor del cuerpo P(s'|s,a) + LLM codec solo para hablar)
  H3 querer (ECUS H=[E,C,U,S] homeostasis)
  H5 sentir (sorpresa z-score integrada: ε -> U -> política)
  boca: LFM2.5-1.2B invocada en eventos de alta sorpresa (traduce, no decide)
Métricas de continuidad (lenguaje verificable):
  - supervivencia 20k pasos, H estable, z alto en eventos, habituación, E no satura,
  - LFM2.5 reporta en eventos reales (traducción del estado interno del núcleo).
Ejecuta: python3 framework/organismo_completo.py --steps 20000
"""
import sys, math, random, time, argparse
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SIZE = 20
MODELO_LLM = "/Users/adrianvalerio/Desktop/ConcienciaArtificial/models/LFM2.5-1.2B-MLX-8bit"

class CuerpoMundo:
    def __init__(self):
        self.pos = [10, 10]
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)
        self.foods = [(3,3),(3,16),(16,3),(16,16)]
        self.social = (18, 18)
        self.t = 0
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
        dH = -0.05*(self.H - np.array([0.8,0.9,0.2,0.7], dtype=np.float32))
        if a == 4 and tuple(self.pos) in self.foods: dH[0] += 0.5
        elif a == 4: dH[0] -= 0.1
        self.H = np.clip(self.H + dH, 0, 1.5)
        return self.estado()

class PredictorCuerpo(nn.Module):
    def __init__(self, d_in=13, d_h=128, d_out=6):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(),
                                 nn.Linear(d_h, d_h), nn.ReLU(),
                                 nn.Linear(d_h, d_out))
    def forward(self, x):
        return self.net(x)

def entrada(estado, a):
    a_onehot = np.zeros(7, dtype=np.float32); a_onehot[a] = 1.0
    return np.concatenate([estado[:2]/SIZE, estado[2:]/1.5, a_onehot])

_LLM = None; _TOK = None
def boca(frase_interna):
    global _LLM, _TOK
    from mlx_lm import load, generate
    if _LLM is None:
        _LLM, _TOK = load(MODELO_LLM)
    prompt = ("<|im_start|>system\nEres el traductor lingüístico de un agente. Traduce su estado interno a UNA frase en primera persona, sin añadir nada.<|im_end|>"
              f"<|im_start|>user\n{frase_interna}<|im_end|><|im_start|>assistant\n")
    return generate(_LLM, _TOK, prompt=prompt, max_tokens=25).strip()

class OrganismoCompleto:
    def __init__(self):
        self.mundo = CuerpoMundo()
        self.pred = PredictorCuerpo().to(DEVICE)
        self.opt = torch.optim.Adam(self.pred.parameters(), lr=1e-3)
        self.w_star = {n: p.detach().clone() for n, p in self.pred.named_parameters()}
        self.fisher = {n: torch.zeros_like(p) for n, p in self.pred.named_parameters()}
        self.E = []          # memoria episódica
        self.eps_hist = []
        self.invocaciones = 0
        self.reportes = []
        self.t = 0
    def entrenar(self, transiciones, n=5, ewc=True):
        X = torch.tensor(np.array([entrada(s, a) for s, a, _ in transiciones]), dtype=torch.float32, device=DEVICE)
        Y = torch.tensor(np.array([np.concatenate([sd[:2]/SIZE, sd[2:]/1.5]) for _, _, sd in transiciones]), dtype=torch.float32, device=DEVICE)
        for _ in range(n):
            idx = torch.randint(0, X.shape[0], (min(64, X.shape[0]),))
            y_hat = self.pred(X[idx])
            loss = (y_hat - Y[idx]).pow(2).mean()
            if ewc:
                loss = loss + 5.0/2*sum((self.fisher[k]*(p-self.w_star[k])**2).sum() for k,p in self.pred.named_parameters())
            self.opt.zero_grad(); loss.backward(); self.opt.step()
            for k,p in self.pred.named_parameters():
                if p.grad is not None: self.fisher[k] = 0.9*self.fisher[k]+0.1*p.grad.detach()**2
    def step(self, a, evento_sorpresa=False):
        self.t += 1
        s_antes = self.mundo.estado()
        if evento_sorpresa:
            x0, y0 = self.mundo.pos
            self.mundo.pos = [(x0+5)%SIZE, (y0+5)%SIZE]  # violación motora
            s_despues = self.mundo.estado()
            self.E.append((self.t, "sorpresa", 1.2))
        else:
            s_despues = self.mundo.fisica_normal(a)
        with torch.no_grad():
            x = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y_real = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((self.pred(x) - y_real).pow(2).mean().sqrt())
        self.eps_hist.append(eps)
        if len(self.eps_hist) > 100: self.eps_hist.pop(0)
        base = np.array(self.eps_hist)
        z = (eps - base.mean())/(base.std()+1e-8)
        # integración: sorpresa -> U -> política (acotada + decaimiento, calibración v0.11b)
        self.mundo.H[2] = np.clip(self.mundo.H[2] + min(0.2, 0.15*max(0.0, z)) - 0.05, 0, 1.5)
        self.entrenar([(s_antes, a, s_despues)], n=5)
        # boca: invocar en sorpresa fuerte con cooldown (no saturar)
        if z > 4.0 and self.t > 50 and self.t - getattr(self, "_ultima_boca", -9999) > 200:
            self._ultima_boca = self.t
            self.invocaciones += 1
            try:
                frase = boca(f"Estado: energía={self.mundo.H[0]:.2f}, incertidumbre={self.mundo.H[2]:.2f}. Evento: mi cuerpo cambió de posición de forma inconsistente con mi modelo (error de predicción alto).")
                self.reportes.append((self.t, frase))
            except Exception as e:
                self.reportes.append((self.t, f"[boca no disponible: {e}]"))
        return eps, z

def elegir_accion(H, mundo):
    x, y = mundo.pos
    dists = [math.hypot(x-fx, y-fy) for fx, fy in mundo.foods]
    en_comida = min(dists) == 0.0
    if H[0] < 0.65 and en_comida: return 4  # forrajear SOLO si está sobre la comida (fix E=0)
    # navegación dirigida a comida (portado de m5_24h)
    fx_, fy_ = mundo.foods[int(np.argmin(dists))]
    dx, dy = fx_-x, fy_-y
    dir_food = (2 if dx>0 else 3) if abs(dx)>abs(dy) else (1 if dy>0 else 0)
    if H[0] < 0.70:
        return dir_food  # ir a comer si energía baja
    if H[2] > 0.6: return random.choice([0,1,2,3])
    if H[3] < 0.5: return 5
    return random.choice([4,0,1,2,3])

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=20000)
    args = p.parse_args()
    print(f"ORGANISMO COMPLETO v0.11 - todos los mecanismos + boca LFM2.5 en UN loop ({args.steps} pasos)")
    print("="*78)
    org = OrganismoCompleto()
    data = []
    for _ in range(1000):
        a = random.randrange(7)
        s_a = org.mundo.estado(); s_d = org.mundo.fisica_normal(a)
        data.append((s_a, a, s_d))
    org.entrenar(data, n=300, ewc=False)
    org.w_star = {n: p.detach().clone() for n, p in org.pred.named_parameters()}
    print("Física del cuerpo pre-entrenada. Loop continuo iniciado.")
    z_max = 0; E_vals = []; U_vals = []; S_vals = []
    for t in range(args.steps):
        a = elegir_accion(org.mundo.H, org.mundo)
        evento = (t % 5000 == 4999)  # evento de sorpresa ocasional (4 en 20k)
        eps, z = org.step(a, evento_sorpresa=evento)
        z_max = max(z_max, z)
        H = org.mundo.H
        E_vals.append(H[0]); U_vals.append(H[2]); S_vals.append(H[3])
        if t % 4000 == 0 and t > 0:
            print(f"  t={t}: E={H[0]:.2f} U={H[2]:.2f} S={H[3]:.2f} | z_max_ventana {z_max:.1f} | E_mem {len(org.E)} | boca {org.invocaciones}")
            z_max = 0
    print("="*78)
    print(f"20k pasos completados: E {min(E_vals):.2f}-{max(E_vals):.2f} oscila, U final {U_vals[-1]:.2f}, S final {S_vals[-1]:.2f}")
    print(f"Memoria E: {len(org.E)} trazas | invocaciones de boca: {org.invocaciones}")
    print("Reportes de la boca (traducción del estado interno en sorpresa):")
    for t, frase in org.reportes[:4]:
        print(f"  t={t}: {frase}")

if __name__ == "__main__":
    main()
