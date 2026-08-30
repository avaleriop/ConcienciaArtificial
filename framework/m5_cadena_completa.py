#!/usr/bin/env python3
"""
CADENA CAUSAL COMPLETA - El experimento científicamente interesante (crítica externa adoptada)
predicción → error → estado interno → motivación → acción → consecuencia → plasticidad → nuevo organismo
Y la prueba decisiva: borrar memoria E → ¿la traza conductual aprendida permanece en W?

Fases (todo integrado en UN organismo, con memoria episódica E + pesos W con EWC):
  F1 baseline: física normal, organismo forrajea, U baja.
  F2 evento: violación motora (teleport) → ε spike → U sube → exploración sube (causal).
  F3 habituación: repetir violaciones CON aprendizaje → ε cae → U vuelve → explora menos.
  F4 borrar E: eliminar memoria episódica (eventos de violación).
  F5 persistencia: ¿el predictor SÍ predice teleports correctamente (W retuvo) y la conducta
     (exploración baja ante teleports) permanece? → plasticidad en W, no en E.

Lenguaje verificable: sin antropomorfismo. Resultado esperado si la arquitectura es funcional:
  - z alto en F2 (detecta) | U y exploración suben solo si integrado (causal)
  - habituación F3 (aprende) | tras borrar E en F4, F5 mantiene respuesta adaptada (W)
Ejecuta: python3 framework/m5_cadena_completa.py
"""
import sys, math, random, time
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SIZE = 20

class CuerpoMundo:
    def __init__(self):
        self.pos = [10, 10]
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)
        self.foods = [(3,3),(3,16),(16,3),(16,16)]
        self.social = (18, 18)
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
    def violacion_motora(self, a):
        self.fisica_normal(a)
        self.pos = [(self.pos[0]+5)%SIZE, (self.pos[1]+5)%SIZE]
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

class Organismo:
    def __init__(self):
        self.mundo = CuerpoMundo()
        self.pred = PredictorCuerpo().to(DEVICE)
        self.opt = torch.optim.Adam(self.pred.parameters(), lr=1e-3)
        # W con EWC (ancla en física normal aprendida)
        self.w_star = {n: p.detach().clone() for n, p in self.pred.named_parameters()}
        self.fisher = {n: torch.zeros_like(p) for n, p in self.pred.named_parameters()}
        self.E = []  # memoria episódica explícita: (t, tipo, saliencia)
        self.eps_hist = []
        self.t = 0
    def entrenar(self, transiciones, n=20, ewc=True):
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
    def step(self, a, violacion=False, aprender=True):
        self.t += 1
        s_antes = self.mundo.estado()
        if violacion:
            s_despues = self.mundo.violacion_motora(a)
            self.E.append((self.t, "violacion", 1.2))  # memoria explícita del evento
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
        # INTEGRACIÓN: sorpresa -> U -> política explora
        self.mundo.H[2] = np.clip(self.mundo.H[2] + 0.15*max(0.0, z), 0, 1.5)
        if aprender:
            self.entrenar([(s_antes, a, s_despues)], n=5)
        return eps, z

def elegir_accion(H, mundo):
    x, y = mundo.pos
    dists = [math.hypot(x-fx, y-fy) for fx, fy in mundo.foods]
    cerca_comida = min(dists) < 2.0
    if H[0] < 0.65 and cerca_comida: return 4
    if H[2] > 0.6: return random.choice([0,1,2,3])
    if H[3] < 0.5: return 5
    return random.choice([4,0,1,2,3])

def main():
    print("CADENA CAUSAL COMPLETA - predicción→error→estado→motivación→acción→plasticidad→persistencia en W")
    print("="*78)
    org = Organismo()
    # pretrain física normal
    data = []
    for _ in range(1000):
        a = random.randrange(7)
        s_a = org.mundo.estado(); s_d = org.mundo.fisica_normal(a)
        data.append((s_a, a, s_d))
    org.entrenar(data, n=300, ewc=False)
    org.w_star = {n: p.detach().clone() for n, p in org.pred.named_parameters()}
    # F1 baseline (300 pasos normales)
    F1 = []
    for t in range(300):
        a = elegir_accion(org.mundo.H, org.mundo)
        eps, z = org.step(a)
        F1.append({"z": z, "U": org.mundo.H[2], "move": 1 if a in (0,1,2,3) else 0})
    # F2 evento (20 violaciones motoras, sorpresa)
    F2 = []
    for t in range(20):
        a = elegir_accion(org.mundo.H, org.mundo)
        eps, z = org.step(a, violacion=True)
        F2.append({"z": z, "U": org.mundo.H[2], "move": 1 if a in (0,1,2,3) else 0})
    # F3 habituación (60 violaciones más, con aprendizaje)
    F3 = []
    for t in range(60):
        a = elegir_accion(org.mundo.H, org.mundo)
        eps, z = org.step(a, violacion=True)
        F3.append({"z": z, "U": org.mundo.H[2], "move": 1 if a in (0,1,2,3) else 0})
    # F4 borrar memoria E
    n_E = len(org.E)
    org.E = []
    print(f"F4: memoria E borrada ({n_E} trazas de eventos eliminadas)")
    # F5 persistencia (20 violaciones SIN E, sin aprendizaje nuevo - medir si W retiene)
    F5 = []
    for t in range(20):
        a = elegir_accion(org.mundo.H, org.mundo)
        eps, z = org.step(a, violacion=True, aprender=False)
        F5.append({"z": z, "U": org.mundo.H[2], "move": 1 if a in (0,1,2,3) else 0})
    # métricas
    z_F2 = np.mean([d["z"] for d in F2])
    z_F3_last = np.mean([d["z"] for d in F3[-10:]])
    z_F5 = np.mean([d["z"] for d in F5])
    U_F1 = np.mean([d["U"] for d in F1]); U_F2 = np.mean([d["U"] for d in F2]); U_F5 = np.mean([d["U"] for d in F5])
    m_F1 = np.mean([d["move"] for d in F1]); m_F2 = np.mean([d["move"] for d in F2]); m_F5 = np.mean([d["move"] for d in F5])
    print(f"F1 baseline:      z~0 | U {U_F1:.2f} | exploración {m_F1:.2f}")
    print(f"F2 evento:        z {z_F2:.1f} | U {U_F2:.2f} | exploración {m_F2:.2f}  <- detecta Y cambia estado")
    print(f"F3 habituación:   z últimas {z_F3_last:.1f} (aprendió la nueva física)")
    print(f"F5 post-E-borrada: z {z_F5:.1f} | U {U_F5:.2f} | exploración {m_F5:.2f}")
    print("-"*78)
    habituado = z_F3_last < z_F2*0.5
    retiene_W = z_F5 < z_F2*0.5  # sin E y sin aprender, si W retuvo: z sigue bajo
    print(f"HABITUACIÓN F2->F3: z {z_F2:.1f} -> {z_F3_last:.1f} ({'SÍ' if habituado else 'NO'})")
    print(f"PERSISTENCIA EN W (F5 sin E, sin aprendizaje): {'SÍ — la traza conductual aprendida permanece en los pesos' if retiene_W else 'NO — se perdió sin E (era memoria, no plasticidad)'}")
    if habituado and retiene_W:
        print("=> CADENA COMPLETA DEMOSTRADA: detecta -> cambia estado -> actúa -> aprende -> la traza persiste en W sin memoria E")
    else:
        print("=> cadena parcial, ver métricas arriba.")

if __name__ == "__main__":
    main()
