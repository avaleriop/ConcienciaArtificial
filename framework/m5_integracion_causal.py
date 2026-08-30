#!/usr/bin/env python3
"""
INTEGRACIÓN CAUSAL - El predictor del cuerpo dentro del organismo (test A vs B)
Pregunta (crítica externa adoptada): ¿la sorpresa es una señal decorativa o cambia
funcionalmente lo que el organismo hace? A integrado vs B predictor convencional desconectado.
Loop A (integrado):
  mundo → estado (pos+H) → predice s_{t+1}|(s_t,a) → ε → z-score (sorpresa)
  → ΔU (incertidumbre sube) → política (explora más) → acción → mundo ↺
  → habituación: entrenar predictor en la violación → ε cae → U vuelve → explora menos
Loop B (convencional): mismo predictor y mismo ε, PERO ε NO conectado a U (decorativo).
Criterio A≠B: si la sorpresa es funcional, A muestra pico de exploración tras violación
y B no (B es indistinguible de no-ver-el-ε). Si A≈B, la integración es decorativa.
Lenguaje: "detecta violaciones, actualiza predictor, reduce error" (no antropomórfico).
Ejecuta: python3 framework/m5_integracion_causal.py
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
    def violacion_interoceptiva(self, a):
        """Violación SIN cambio de posición (aisla el efecto causal de la sorpresa):
        comer en comida BAJA la energía (causalidad invertida). El cuerpo no se mueve."""
        x, y = self.pos
        if a == 0: y = max(0, y-1)
        elif a == 1: y = min(SIZE-1, y+1)
        elif a == 2: x = min(SIZE-1, x+1)
        elif a == 3: x = max(0, x-1)
        self.pos = [x, y]
        dH = -0.05*(self.H - np.array([0.8,0.9,0.2,0.7], dtype=np.float32))
        if a == 4 and tuple(self.pos) in self.foods:
            dH[0] -= 0.5  # VIOLACIÓN: comer baja E (mundo traiciona sin mover el cuerpo)
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

class Organismo:
    """Organismo con predictor integrado (A) o desconectado (B)."""
    def __init__(self, integrado):
        self.mundo = CuerpoMundo()
        self.pred = PredictorCuerpo().to(DEVICE)
        self.opt = torch.optim.Adam(self.pred.parameters(), lr=1e-3)
        self.integrado = integrado
        self.eps_hist = []  # baseline reciente para z-score
        self.eps_viol_hist = []
        self.log = []
        self.moves = 0; self.total = 0
    def entrenar_predictor(self, estados_acciones, n=100):
        X = torch.tensor(np.array([entrada(s, a) for s, a, _ in estados_acciones]), dtype=torch.float32, device=DEVICE)
        Y = torch.tensor(np.array([np.concatenate([sd[:2]/SIZE, sd[2:]/1.5]) for _, _, sd in estados_acciones]), dtype=torch.float32, device=DEVICE)
        for _ in range(n):
            idx = torch.randint(0, X.shape[0], (64,))
            y_hat = self.pred(X[idx])
            loss = (y_hat - Y[idx]).pow(2).mean()
            self.opt.zero_grad(); loss.backward(); self.opt.step()
    def step(self, a, violacion=False, tipo="motora"):
        self.total += 1
        if a in (0,1,2,3): self.moves += 1
        s_antes = self.mundo.estado()
        if violacion and tipo == "motora":
            s_despues = self.mundo.violacion_motora(a)
        elif violacion and tipo == "intero":
            s_despues = self.mundo.violacion_interoceptiva(a)
        else:
            s_despues = self.mundo.fisica_normal(a)
        with torch.no_grad():
            x = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y_real = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((self.pred(x) - y_real).pow(2).mean().sqrt())
        self.eps_hist.append(eps)
        if len(self.eps_hist) > 100: self.eps_hist.pop(0)
        base = np.array(self.eps_hist)
        z = (eps - base.mean()) / (base.std()+1e-8)
        # INTEGRACIÓN CAUSAL: sorpresa -> incertidumbre U sube -> política explora más
        if self.integrado:
            self.mundo.H[2] = np.clip(self.mundo.H[2] + 0.15*max(0.0, z), 0, 1.5)
        # habituación: entrenar predictor en la transición (física aprendida, EWC implícito por amortiguamiento)
        self.entrenar_predictor([(s_antes, a, s_despues)], n=5)
        # log
        self.log.append({"t": self.total, "eps": eps, "z": z, "U": self.mundo.H[2],
                         "move": 1 if a in (0,1,2,3) else 0, "viol": violacion})
        return eps, z

def elegir_accion(H, mundo):
    # política ECUS: explora más si U alta; forrajea si E baja y cerca de comida
    x, y = mundo.pos
    dists = [math.hypot(x-fx, y-fy) for fx, fy in mundo.foods]
    cerca_comida = min(dists) < 2.0
    if H[0] < 0.65 and cerca_comida:
        return 4
    if H[2] > 0.6:
        return random.choice([0,1,2,3])  # explorar (U alta)
    if H[3] < 0.5:
        return 5  # ir a social
    return random.choice([4, 0, 1, 2, 3])

def run(integrado, n_pre=500, n_base=300, n_viol=40, n_post=300, tipo_viol='motora'):
    org = Organismo(integrado)
    # pretrain predictor en física normal
    data = []
    for _ in range(1000):
        a = random.randrange(7)
        s_a = org.mundo.estado(); s_d = org.mundo.fisica_normal(a)
        data.append((s_a, a, s_d))
    org.entrenar_predictor(data, n=300)
    # Fase base
    for t in range(n_base):
        a = elegir_accion(org.mundo.H, org.mundo)
        org.step(a)
    # Fase violación (repetición con habituación)
    z_viol = []
    for t in range(n_viol):
        a = elegir_accion(org.mundo.H, org.mundo)
        eps, z = org.step(a, violacion=True, tipo=tipo_viol)
        z_viol.append(z)
    # Fase post (recuperación)
    for t in range(n_post):
        a = elegir_accion(org.mundo.H, org.mundo)
        org.step(a)
    # métricas
    base_moves = np.mean([l["move"] for l in org.log[:n_base]])
    viol_moves = np.mean([l["move"] for l in org.log[n_base:n_base+n_viol]])
    post_moves = np.mean([l["move"] for l in org.log[n_base+n_viol:]])
    U_base = np.mean([l["U"] for l in org.log[:n_base]])
    U_viol = np.mean([l["U"] for l in org.log[n_base:n_base+n_viol]])
    U_post = np.mean([l["U"] for l in org.log[n_base+n_viol:]])
    z_first = np.mean(z_viol[:5]); z_last = np.mean(z_viol[-5:])
    return {"base_moves": base_moves, "viol_moves": viol_moves, "post_moves": post_moves,
            "U_base": U_base, "U_viol": U_viol, "U_post": U_post,
            "z_first": z_first, "z_last": z_last}

def main():
    print("INTEGRACIÓN CAUSAL - A (predictor integrado al organismo) vs B (predictor convencional desconectado)")
    print("="*78)
    A = run(integrado=True)
    B = run(integrado=False)
    A_intero = run(integrado=True, tipo_viol='intero')
    B_intero = run(integrado=False, tipo_viol='intero')
    print(f"A integrado:    z violación primeras={A['z_first']:.1f} -> últimas={A['z_last']:.1f} (habituación {100*(1-A['z_last']/A['z_first']):.0f}%)")
    print(f"                U base {A['U_base']:.2f} -> viol {A['U_viol']:.2f} -> post {A['U_post']:.2f}")
    print(f"                exploración (fracción moves): base {A['base_moves']:.2f} -> viol {A['viol_moves']:.2f} -> post {A['post_moves']:.2f}")
    print(f"B convencional: z violación primeras={B['z_first']:.1f} -> últimas={B['z_last']:.1f} (habituación {100*(1-B['z_last']/B['z_first']):.0f}%)")
    print(f"                U base {B['U_base']:.2f} -> viol {B['U_viol']:.2f} -> post {B['U_post']:.2f}")
    print(f"                exploración (fracción moves): base {B['base_moves']:.2f} -> viol {B['viol_moves']:.2f} -> post {B['post_moves']:.2f}")
    print("-"*78)
    deltaA = A['viol_moves'] - A['base_moves']
    deltaB = B['viol_moves'] - B['base_moves']
    print(f"Δ exploración tras violación: A = {deltaA:+.2f} | B = {deltaB:+.2f}")
    if deltaA > 0.05 and abs(deltaB) < 0.03:
        print("=> CAUSALIDAD CONFIRMADA: la sorpresa cambia la conducta SOLO en el organismo integrado.")
        print("   (A≠B: el predictor convencional detecta pero no actúa; el integrado detecta Y actúa)")
    elif abs(deltaA) < 0.03 and abs(deltaB) < 0.03:
        print("=> INTEGRACIÓN DECORATIVA: la sorpresa no cambia la conducta (señal sin función).")
    else:
        print(f"=> INTERMEDIO: A {deltaA:+.2f} B {deltaB:+.2f} — integración parcial.")
    # Variante interoceptiva (sin cambio de posición, aisla el efecto causal puro)
    dAi = A_intero['viol_moves'] - A_intero['base_moves']
    dBi = B_intero['viol_moves'] - B_intero['base_moves']
    print("-"*78)
    print(f"VIOLACIÓN INTEROCEPTIVA (sin mover el cuerpo, aísla causalidad pura):")
    print(f"  A integrado: U base {A_intero['U_base']:.2f} -> viol {A_intero['U_viol']:.2f} | exploración base {A_intero['base_moves']:.2f} -> viol {A_intero['viol_moves']:.2f} (Δ {dAi:+.2f})")
    print(f"  B convencional: U base {B_intero['U_base']:.2f} -> viol {B_intero['U_viol']:.2f} | exploración base {B_intero['base_moves']:.2f} -> viol {B_intero['viol_moves']:.2f} (Δ {dBi:+.2f})")
    if dAi > 0.05 and abs(dBi) < 0.03:
        print("=> CAUSALIDAD PURA CONFIRMADA: sin cambio de posición, solo A (integrado) cambia conducta.")
    else:
        print(f"=> causalidad pura: A {dAi:+.2f} vs B {dBi:+.2f} — {'parcial' if dAi > dBi else 'no confirmada'}")

if __name__ == "__main__":
    main()
