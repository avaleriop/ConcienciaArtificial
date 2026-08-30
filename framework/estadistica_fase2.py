#!/usr/bin/env python3
"""
FASE 2 ESTADÍSTICA - N=30 seeds, protocolo fijo (pre-registrado en 48)
Mide por seed: z_base, z_motor, habituación (z primeras vs últimas), z post-borrado-E.
Escribe results/estadistica_fase2.json. Luego: python3 framework/analisis_fase2.py
Ejecuta: python3 framework/estadistica_fase2.py
"""
import sys, math, random, json, os
import numpy as np
import torch
import torch.nn as nn

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SIZE = 20

class CuerpoMundo:
    def __init__(self):
        self.pos = [10, 10]
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)
        self.foods = [(3,3),(3,16),(16,3),(16,16)]
    def estado(self):
        return np.concatenate([np.array(self.pos, dtype=np.float32), self.H])
    def fisica_normal(self, a):
        x, y = self.pos
        if a == 0: y = max(0, y-1)
        elif a == 1: y = min(SIZE-1, y+1)
        elif a == 2: x = min(SIZE-1, x+1)
        elif a == 3: x = max(0, x-1)
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

class Predictor(nn.Module):
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

def entrenar(pred, X, Y, n=400):
    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    for _ in range(n):
        idx = torch.randint(0, X.shape[0], (64,))
        loss = (pred(X[idx]) - Y[idx]).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return opt

def medir_z(pred, mundo, tipo, n=50):
    """z de violación vs baseline normal (n trials cada uno)."""
    def eps_de(s_antes, s_despues, a):
        with torch.no_grad():
            x = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            return float((pred(x)-y).pow(2).mean().sqrt())
    base = []; ev = []
    for _ in range(n):
        a = random.randrange(7)
        s_a = mundo.estado()
        s_d = mundo.violacion_motora(a) if tipo=='motor' else mundo.fisica_normal(a)
        ev.append(eps_de(s_a, s_d, a))
        a2 = random.randrange(7)
        s_a2 = mundo.estado(); s_d2 = mundo.fisica_normal(a2)
        base.append(eps_de(s_a2, s_d2, a2))
    base = np.array(base); ev = np.array(ev)
    return (ev.mean()-base.mean())/(base.std()+1e-8)

def run_seed(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    mundo = CuerpoMundo()
    X_list, Y_list = [], []
    for _ in range(1200):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.fisica_normal(a)
        X_list.append(entrada(s_a, a))
        Y_list.append(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]))
    X = torch.tensor(np.array(X_list), dtype=torch.float32, device=DEVICE)
    Y = torch.tensor(np.array(Y_list), dtype=torch.float32, device=DEVICE)
    pred = Predictor().to(DEVICE)
    opt = entrenar(pred, X, Y, n=400)
    z_base = medir_z(pred, mundo, 'base')
    z_motor = medir_z(pred, mundo, 'motor')
    # habituación: 60 violaciones con entrenamiento, midiendo z cada 10
    z_hab = []
    for k in range(60):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.violacion_motora(a)
        xb = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        yb = torch.tensor(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        loss = (pred(xb)-yb).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        if k % 10 == 9:
            z_hab.append(medir_z(pred, mundo, 'motor'))
    # E: medir z post (ya habituado)
    z_post = medir_z(pred, mundo, 'motor')
    return {"seed": seed, "z_base": z_base, "z_motor": z_motor,
            "z_hab_primera": z_hab[0], "z_hab_ultima": z_hab[-1], "z_post": z_post,
            "E_final": float(mundo.H[0])}

def main():
    print("FASE 2 ESTADÍSTICA - 30 seeds (protocolo pre-registrado 48)")
    resultados = [run_seed(s) for s in range(30)]
    os.makedirs('results', exist_ok=True)
    with open('results/estadistica_fase2.json', 'w') as f:
        json.dump(resultados, f, indent=2)
    print(f"30 seeds completadas -> results/estadistica_fase2.json")
    print("Ejecuta: python3 framework/analisis_fase2.py")

if __name__ == "__main__":
    main()
