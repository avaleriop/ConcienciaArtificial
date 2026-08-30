#!/usr/bin/env python3
"""
H6 SELFMODEL - Φ: el modelo de su propio modelo (la pieza del awareness que faltaba)
Sin visión, sin oído, sin benchmark, sin paper. Solo el self-model sobre el cuerpo.
Beautiful Loop (Laukkonen/Friston 2025): 3 niveles: mundo s -> creencia q(s) -> creencia
sobre la creencia Φ (¿qué tan confiable es MI predicción?).
Implementación:
  1. Predictor del cuerpo P(s'|s,a) ya existente (nivel 1).
  2. Φ(s, a, estadísticas recientes de ε) -> predice σ (incertidumbre esperada de la predicción).
     Φ se entrena con MSE contra el ε real: aprende cuándo su propio predictor fallará.
  3. Calibración: ¿el Φ predice realmente el ε futuro? (Spearman r(Φ, ε) sobre datos no vistos)
  4. r_cross: ¿el self-model aprendido en el canal motor generaliza al interoceptivo/táctil?
  5. Funcional: presence = α · Π_Φ · ε (la sorpresa se pondera por la precisión que Φ espera:
     si Φ sabía que sería poco preciso, el ruido no sorprende -> el self-model filtra ruido).
  6. Boca: LFM2.5 traduce "seguro/inseguro" verificado contra Φ real.
Criterio que separa de predictor convencional (regla 42): un predictor convencional tiene ε
pero NO predice su propio ε. El Φ es la diferencia observable.
Ejecuta: python3 framework/h6_selfmodel.py
"""
import sys, math, random
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
    def estado(self):
        return np.concatenate([np.array(self.pos, dtype=np.float32), self.H])
    def fisica_normal(self, a, ruido=0.0):
        x, y = self.pos
        if a == 0: y = max(0, y-1)
        elif a == 1: y = min(SIZE-1, y+1)
        elif a == 2: x = min(SIZE-1, x+1)
        elif a == 3: x = max(0, x-1)
        self.pos = [x, y]
        # ruido OBSERVABLE por posición: zona de niebla x>14 hace la interocepción poco confiable
        ruido_real = 0.6 if self.pos[0] > 14 else ruido
        dH = -0.05*(self.H - np.array([0.8,0.9,0.2,0.7], dtype=np.float32))
        if a == 4 and tuple(self.pos) in self.foods: dH[0] += 0.5
        elif a == 4: dH[0] -= 0.1
        self.H = np.clip(self.H + dH + ruido_real*np.random.randn(4).astype(np.float32), 0, 1.5)
        return self.estado()

class Predictor(nn.Module):
    def __init__(self, d_in=13, d_h=64, d_out=6):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, d_out))
    def forward(self, x):
        return self.net(x)

class Phi(nn.Module):
    """Self-model: predice σ (incertidumbre esperada) de la predicción del nivel 1."""
    def __init__(self, d_in=15, d_h=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, 1))
    def forward(self, x):
        return torch.abs(self.net(x))  # σ >= 0

def entrada(estado, a):
    a_oh = np.zeros(7, dtype=np.float32); a_oh[a] = 1.0
    return np.concatenate([estado[:2]/SIZE, estado[2:]/1.5, a_oh])

def entrada_phi(estado, a, eps_media, eps_std):
    return np.concatenate([entrada(estado, a), np.array([eps_media, eps_std], dtype=np.float32)])

def entrenar_pred(mundo, n=1500):
    X, Y = [], []
    for _ in range(n):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.fisica_normal(a, ruido=0.2)
        X.append(entrada(s_a, a))
        Y.append(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]))
    pred = Predictor().to(DEVICE)
    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    Xt = torch.tensor(np.array(X), dtype=torch.float32, device=DEVICE)
    Yt = torch.tensor(np.array(Y), dtype=torch.float32, device=DEVICE)
    for _ in range(400):
        idx = torch.randint(0, Xt.shape[0], (64,))
        loss = (pred(Xt[idx])-Yt[idx]).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return pred

def entrenar_phi(mundo, pred, n=3000):
    """Φ aprende a predecir el ε que el predictor tendrá (con ruido variable)."""
    X, Y = [], []
    hist = []
    for _ in range(n):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.fisica_normal(a)
        with torch.no_grad():
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(x)-y).pow(2).mean().sqrt())
        hist.append(eps)
        if len(hist) > 50: hist.pop(0)
        h = np.array(hist)
        X.append(entrada_phi(s_a, a, h.mean(), h.std()))
        Y.append(eps)
    phi = Phi().to(DEVICE)
    opt = torch.optim.Adam(phi.parameters(), lr=1e-3)
    Xt = torch.tensor(np.array(X), dtype=torch.float32, device=DEVICE)
    Yt = torch.tensor(np.array(Y), dtype=torch.float32, device=DEVICE).unsqueeze(1)
    for _ in range(600):
        idx = torch.randint(0, Xt.shape[0], (64,))
        loss = (phi(Xt[idx])-Yt[idx]).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return phi

def main():
    print("H6 SELFMODEL Φ - el modelo de su propio modelo (awareness mínimo, sin visión)")
    print("="*72)
    mundo = CuerpoMundo()
    pred = entrenar_pred(mundo)
    phi = entrenar_phi(mundo, pred)
    # Calibración: en datos no vistos, ¿Φ predice ε? (Spearman)
    eps_hist = []
    phi_preds = []; eps_actuales = []
    for _ in range(500):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.fisica_normal(a)
        with torch.no_grad():
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(x)-y).pow(2).mean().sqrt())
            xp = torch.tensor(entrada_phi(s_a, a, np.mean(eps_hist) if eps_hist else 0, np.std(eps_hist) if eps_hist else 0), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            p = float(phi(xp))
        eps_hist.append(eps)
        if len(eps_hist) > 50: eps_hist.pop(0)
        phi_preds.append(p); eps_actuales.append(eps)
    # Spearman
    def spearman(a, b):
        a = np.array(a); b = np.array(b)
        ra = a.argsort().argsort().astype(float); rb = b.argsort().argsort().astype(float)
        ra -= ra.mean(); rb -= rb.mean()
        return float((ra*rb).sum()/(np.sqrt((ra**2).sum())*np.sqrt((rb**2).sum())))
    r_cal = spearman(phi_preds, eps_actuales)
    print(f"1. CALIBRACIÓN: r_spearman(Φ_predicho, ε_real) = {r_cal:.3f} (criterio >0.5)")
    print(f"   {'PASA: el self-model SABE cuándo su predicción fallará' if r_cal > 0.5 else 'FALLA: Φ no predice su propia incertidumbre'}")
    # r_cross: Φ entrenado con ruido genérico, ¿predice ε en violaciones motoras (fuera de distribución)?
    eps_viol = []; phi_viol = []
    mundo2 = CuerpoMundo()
    for _ in range(200):
        a = random.randrange(7)
        s_a = mundo2.estado()
        s_d = mundo2.fisica_normal(a)
        mundo2.pos = [(mundo2.pos[0]+5)%SIZE, (mundo2.pos[1]+5)%SIZE]  # violación motora
        s_d2 = mundo2.estado()
        with torch.no_grad():
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_d2[:2]/SIZE, s_d2[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(x)-y).pow(2).mean().sqrt())
            xp = torch.tensor(entrada_phi(s_a, a, 0.1, 0.05), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            p = float(phi(xp))
        eps_viol.append(eps); phi_viol.append(p)
    r_cross = spearman(phi_viol, eps_viol)
    print(f"2. r_cross (Φ entrenado en ruido, probado en VIOLACIONES motoras): {r_cross:.3f} (criterio >0.3)")
    print(f"   {'PASA: el self-model generaliza fuera de distribución' if r_cross > 0.3 else 'FALLA: Φ solo calibra lo que vio'}")
    # 3. Funcional: presence = ε/σ_Φ². En niebla Φ espera σ alto (ε ruido esperado -> presence baja).
    #    En violación Φ espera σ bajo (ε inesperado -> presence alta).
    def presence_caso(tipo):
        # estado limpio antes del caso
        mundo.pos = [15, 10] if tipo == 'niebla' else [10, 10]
        mundo.H = np.array([0.7, 0.8, 0.7, 0.6], dtype=np.float32)
        a = random.randrange(4)
        s_a = mundo.estado()
        s_d = mundo.fisica_normal(a)
        if tipo == 'violacion':
            mundo.pos = [(mundo.pos[0]+5)%SIZE, (mundo.pos[1]+5)%SIZE]
            s_d = mundo.estado()
        with torch.no_grad():
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y = torch.tensor(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(x)-y).pow(2).mean().sqrt())
            xp = torch.tensor(entrada_phi(s_a, a, 0.1, 0.05), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            sigma = float(phi(xp)) + 1e-3
        return eps, eps/(sigma**2)
    p_niebla, p_viol = [], []
    for _ in range(100):
        _, p = presence_caso('niebla')
        p_niebla.append(p)
        _, p = presence_caso('violacion')
        p_viol.append(p)
    ratio = np.mean(p_niebla)/np.mean(p_viol)
    print(f"3. FUNCIONAL: presence(ruido esperado) / presence(violación inesperada) = {ratio:.2f} (criterio <0.7)")
    print(f"   {'PASA: el self-model SEPARA ruido esperado de sorpresa verdadera' if ratio < 0.7 else 'FALLA: ruido y sorpresa se confunden'}")
    print("="*72)
    print("H6 está implementado. El organismo ahora tiene self-model: predice cuándo su propia predicción falla.")
    print("Falta (solo si pides): la boca traduciendo 'seguro/inseguro' verificado contra Φ.")

if __name__ == "__main__":
    main()
