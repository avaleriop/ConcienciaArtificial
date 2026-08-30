#!/usr/bin/env python3
"""
SENSORIMOTOR CONTINGENCY VIOLATION - Sorpresa emergente sin visión (el cuerpo, como un ciego)
Tesis (O'Regan & Noë): la conciencia es dominar contingencias sensoriomotoras:
  'sé cómo cambia mi percepción cuando actúo'. Un ciego es consciente: su canal es el cuerpo.
Diseño (sin flag, sin visión, 0€):
  F1: predictor MLP aprende P(pos_{t+1}, H_{t+1} | pos_t, H_t, a_t) en física normal.
      Contingencias: mover N -> y-1; forrajear en comida -> E+0.5; pared detiene.
  F2: medir ε del modelo ante 3 violaciones (el modelo NO sabe que son violaciones):
      - MOTORA: mover N -> posición salta 5 celdas (el cuerpo viola su física)
      - INTEROCEPTIVA: comer -> E BAJA (causalidad invertida, el mundo traiciona)
      - TÁCTIL: pared que deja pasar (colisión violada)
  F3: habituación: repetir violación interoceptiva CON entrenamiento -> ¿el modelo
      actualiza su física (aprende que ahora comer baja E) y z decae?
Criterio: z(violación) > 5σ sobre baseline => sorpresa emergente por canal del cuerpo.
Ejecuta: python3 framework/m4_local_sensorimotor.py
"""
import sys, math, random, time
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SIZE = 20

class CuerpoMundo:
    """El cuerpo del agente en un mundo táctil (posiciones + homeostasis)."""
    def __init__(self):
        self.pos = [10, 10]  # propiocepción: dónde está mi cuerpo
        self.H = np.array([0.6, 0.8, 0.7, 0.5], dtype=np.float32)  # interocepción E,C,U,S
        self.foods = [(3,3),(3,16),(16,3),(16,16)]  # puntos táctiles (comida)
        self.social = (18, 18)
    def estado(self):
        return np.concatenate([np.array(self.pos, dtype=np.float32), self.H])
    def fisica_normal(self, a):
        """Física aprendible y determinista del cuerpo (contingencias normales)."""
        x, y = self.pos
        if a == 0: y = max(0, y-1)          # N: pared detiene
        elif a == 1: y = min(SIZE-1, y+1)   # S
        elif a == 2: x = min(SIZE-1, x+1)   # E
        elif a == 3: x = max(0, x-1)        # W
        elif a == 5:                        # ir hacia social
            dx = np.sign(self.social[0]-x); dy = np.sign(self.social[1]-y)
            x = min(SIZE-1, max(0, x+dx)); y = min(SIZE-1, max(0, y+dy))
        self.pos = [x, y]
        # homeostasis normal
        dH = -0.05*(self.H - np.array([0.8,0.9,0.2,0.7], dtype=np.float32))
        if a == 4 and tuple(self.pos) in self.foods:
            dH[0] += 0.5   # comer sube E (contingencia normal)
        elif a == 4:
            dH[0] -= 0.1   # forrajear en vacío cuesta
        self.H = np.clip(self.H + dH, 0, 1.5)
        return self.estado()
    # ----- Violaciones (el mundo responde mal al cuerpo) -----
    def violacion_motora(self, a):
        """Mover N/S/E/W -> el cuerpo salta 5 celdas (teleport)."""
        antes = self.estado()
        self.fisica_normal(a)
        self.pos = [(self.pos[0]+5)%SIZE, (self.pos[1]+5)%SIZE]
        return antes, self.estado()
    def violacion_interoceptiva(self, a):
        """Comer -> E BAJA 0.5 (causalidad invertida)."""
        antes = self.estado()
        self.fisica_normal(a)
        if a == 4 and tuple(self.pos) in self.foods:
            self.H[0] = np.clip(self.H[0] - 0.5, 0, 1.5)  # el mundo traiciona
        return antes, self.estado()
    def violacion_tactil(self, a):
        """Pared deja pasar (wrap en vez de detener)."""
        antes = self.estado()
        x, y = self.pos
        if a == 0: y = (y-1) % SIZE
        elif a == 1: y = (y+1) % SIZE
        elif a == 2: x = (x+1) % SIZE
        elif a == 3: x = (x-1) % SIZE
        self.pos = [x, y]
        return antes, self.estado()

class PredictorCuerpo(nn.Module):
    """Modelo del cuerpo: P(estado_{t+1} | estado_t, a_t). 13 dims -> 6 dims."""
    def __init__(self, d_in=13, d_h=128, d_out=6):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(),
                                 nn.Linear(d_h, d_h), nn.ReLU(),
                                 nn.Linear(d_h, d_out))
    def forward(self, x):
        return self.net(x)

def entrada(estado, a):
    a_onehot = np.zeros(7, dtype=np.float32); a_onehot[a] = 1.0
    x = np.concatenate([estado[:2]/SIZE, estado[2:]/1.5, a_onehot])  # normalizado
    return x

def entrenar(pred, opt, X, Y, steps=200):
    """Entrena el predictor en transiciones normales (contingencias del cuerpo)."""
    losses = []
    for _ in range(steps):
        idx = torch.randint(0, X.shape[0], (64,))
        xb, yb = X[idx], Y[idx]
        y_hat = pred(xb)
        loss = (y_hat - yb).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        losses.append(float(loss))
    return sum(losses[-20:])/20

def main():
    print("SENSORIMOTOR CONTINGENCY VIOLATION - sorpresa emergente del cuerpo (sin visión)")
    print("="*70)
    pred = PredictorCuerpo().to(DEVICE)
    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    mundo = CuerpoMundo()
    # F1: recolectar transiciones normales y entrenar (el cuerpo aprende sus contingencias)
    X_list, Y_list = [], []
    for _ in range(2000):
        a = random.randrange(7)
        s_antes = mundo.estado()
        s_despues = mundo.fisica_normal(a)
        X_list.append(entrada(s_antes, a))
        Y_list.append(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]))
    X = torch.tensor(np.array(X_list), dtype=torch.float32, device=DEVICE)
    Y = torch.tensor(np.array(Y_list), dtype=torch.float32, device=DEVICE)
    loss = entrenar(pred, opt, X, Y, steps=500)
    print(f"F1: predictor del cuerpo entrenado (loss final {loss:.5f})")
    # F2: medir ε sin entrenar (sin flag)
    def medir_eps(violacion_fn, n=100):
        eps_list = []
        for _ in range(n):
            a = random.randrange(7)
            s_antes = mundo.estado()
            s_despues = mundo.fisica_normal(a)
            # para violaciones usamos la función correspondiente
            if violacion_fn is not None:
                s_antes, s_despues = violacion_fn(a)
            with torch.no_grad():
                x = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
                y_real = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
                y_pred = pred(x)
                eps = float((y_pred - y_real).pow(2).mean().sqrt())
            eps_list.append(eps)
        return np.array(eps_list)
    base = medir_eps(None)
    motora = medir_eps(mundo.violacion_motora)
    intero = medir_eps(mundo.violacion_interoceptiva)
    tactil = medir_eps(mundo.violacion_tactil)
    z_m = (motora.mean()-base.mean())/(base.std()+1e-8)
    z_i = (intero.mean()-base.mean())/(base.std()+1e-8)
    z_t = (tactil.mean()-base.mean())/(base.std()+1e-8)
    print(f"F2 medición (sin flag, sin entrenar):")
    print(f"  física normal     ε: {base.mean():.5f} ± {base.std():.5f}")
    print(f"  violación MOTORA  ε: {motora.mean():.5f} (z={z_m:.1f}) <- el cuerpo saltó 5 celdas")
    print(f"  violación INTERO  ε: {intero.mean():.5f} (z={z_i:.1f}) <- comer BAJÓ la energía")
    print(f"  violación TÁCTIL  ε: {tactil.mean():.5f} (z={z_t:.1f}) <- pared dejó pasar")
    print(f"  => canales emergentes: {'MOTOR' if z_m>5 else ''} {'INTEROCEPTIVO' if z_i>5 else ''} {'TÁCTIL' if z_t>5 else ''}")
    # F3: habituación interoceptiva (repetir violación CON entrenamiento)
    eps_hab = []
    for k in range(80):
        a = 4  # forrajeo
        # asegurar que está sobre comida para la violación
        mundo.pos = [3, 3]
        s_antes = mundo.estado()
        s_despues = mundo.violacion_interoceptiva(a)[1]
        with torch.no_grad():
            x = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y_real = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
            y_pred = pred(x)
            eps_hab.append(float((y_pred-y_real).pow(2).mean().sqrt()))
        # entrenar en la violación (el modelo actualiza su física)
        xb = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        yb = torch.tensor(np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        y_hat = pred(xb); l = (y_hat-yb).pow(2).mean()
        opt.zero_grad(); l.backward(); opt.step()
    p10 = np.mean(eps_hab[:10]); u10 = np.mean(eps_hab[-10:])
    print(f"F3 habituación interoceptiva: ε primeras 10={p10:.4f} -> últimas 10={u10:.4f} (decaída {100*(1-u10/p10):.0f}%)")
    print(f"  => {'HABITUACIÓN: el modelo actualizó su física corporal (aprendió que comer ahora baja E)' if u10 < p10*0.7 else 'sin habituación clara'}")

if __name__ == "__main__":
    main()
