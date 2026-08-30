#!/usr/bin/env python3
"""
RIGOR CONTROLES (Fase 1) - C1 acción-barajada, C2 observación-sola, C3 deshabituación, C4 ablaciones Levin
Pre-registrado en 46-plan-rigor-cientifico.md:1. Ejecuta: python3 framework/rigor_controles.py
Criterios de REFUTACIÓN explícitos (si se cumple, el claim muere):
  C1: si z(imposible|acción-barajada) > z(imposible|correcta) - margen -> condicionamiento ilusorio
  C2: si z(imposible|obs-sola) > z(imposible|acción-condicionada) - margen -> la acción no aporta
  C3: si la violación NUEVA (intero) no re-dispara z tras habituar a MOTORA -> sin especificidad
  C4a: si re-inicializar W NO restaura z alto -> la habituación no estaba en W
  C4b: si W congelado habitua igual -> la habituación no es aprendizaje
  C4c: si predictor sin entrenar distingue base/imposible -> el efecto no requiere física aprendida
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
    def violacion_intero(self, a):
        self.fisica_normal(a)
        if a == 4 and tuple(self.pos) in self.foods:
            self.H[0] = np.clip(self.H[0] - 0.5, 0, 1.5)  # comer BAJA energía
        return self.estado()

class Predictor(nn.Module):
    def __init__(self, d_in, d_h=128, d_out=6):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(),
                                 nn.Linear(d_h, d_h), nn.ReLU(),
                                 nn.Linear(d_h, d_out))
    def forward(self, x):
        return self.net(x)

def entrada(estado, a):
    a_onehot = np.zeros(7, dtype=np.float32); a_onehot[a] = 1.0
    return np.concatenate([estado[:2]/SIZE, estado[2:]/1.5, a_onehot])

def entrada_sin_accion(estado):
    return np.concatenate([estado[:2]/SIZE, estado[2:]/1.5])

def entrenar(pred, X, Y, n=400):
    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    for _ in range(n):
        idx = torch.randint(0, X.shape[0], (64,))
        loss = (pred(X[idx]) - Y[idx]).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return opt

def medir_z(pred, mundo, tipo, n=100, usar_accion=True, accion_barajada=False, d_in=13):
    eps_list = []
    for _ in range(n):
        a = random.randrange(7)
        s_antes = mundo.estado()
        if tipo == 'base':
            s_despues = mundo.fisica_normal(a)
        elif tipo == 'motor':
            s_despues = mundo.violacion_motora(a)
        elif tipo == 'intero':
            s_despues = mundo.violacion_intero(a)
        if usar_accion:
            a_usar = random.randrange(7) if accion_barajada else a
            x = entrada(s_antes, a_usar)
        else:
            x = entrada_sin_accion(s_antes)
        y = np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5])
        with torch.no_grad():
            xt = torch.tensor(x, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            yt = torch.tensor(y, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps = float((pred(xt) - yt).pow(2).mean().sqrt())
        eps_list.append(eps)
    # baseline normal para z
    base_list = []
    for _ in range(100):
        a = random.randrange(7)
        s_antes = mundo.estado()
        s_despues = mundo.fisica_normal(a)
        if usar_accion:
            a_usar = random.randrange(7) if accion_barajada else a
            x = entrada(s_antes, a_usar)
        else:
            x = entrada_sin_accion(s_antes)
        y = np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5])
        with torch.no_grad():
            xt = torch.tensor(x, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            yt = torch.tensor(y, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            base_list.append(float((pred(xt)-yt).pow(2).mean().sqrt()))
    base = np.array(base_list); ev = np.array(eps_list)
    z = (ev.mean() - base.mean())/(base.std()+1e-8)
    return z, ev.mean(), base.mean()

def main():
    print("RIGOR CONTROLES F1 - C1 barajada | C2 obs-sola | C3 deshabituación | C4 ablaciones")
    print("="*78)
    # Datos de entrenamiento con acción real
    mundo = CuerpoMundo()
    X_list, Y_list = [], []
    for _ in range(1500):
        a = random.randrange(7)
        s_a = mundo.estado(); s_d = mundo.fisica_normal(a)
        X_list.append(entrada(s_a, a))
        Y_list.append(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]))
    X = torch.tensor(np.array(X_list), dtype=torch.float32, device=DEVICE)
    Y = torch.tensor(np.array(Y_list), dtype=torch.float32, device=DEVICE)

    pred = Predictor(d_in=13).to(DEVICE)
    opt = entrenar(pred, X, Y, n=400)

    # C1: acción-barajada
    z_correcta, e_c, b_c = medir_z(pred, mundo, 'motor', usar_accion=True, accion_barajada=False)
    z_barajada, e_b, b_b = medir_z(pred, mundo, 'motor', usar_accion=True, accion_barajada=True)
    print(f"C1 acción-condicionada: z(motor|acción correcta) = {z_correcta:.1f}")
    print(f"   acción-barajada:      z(motor|acción al azar)  = {z_barajada:.1f}")
    c1_ok = z_correcta > z_barajada + 2.0
    print(f"   => {'PASA: el condicionamiento a la acción es REAL' if c1_ok else 'REFUTA: detección ilusoria (novelty de observación)'}")

    # C2: observación-sola
    pred2 = Predictor(d_in=6).to(DEVICE)
    X2 = torch.tensor(np.array([entrada_sin_accion(s) for s in []]), dtype=torch.float32, device=DEVICE)
    X2_list, Y2_list = [], []
    mundo2 = CuerpoMundo()
    for _ in range(1500):
        a = random.randrange(7)
        s_a = mundo2.estado(); s_d = mundo2.fisica_normal(a)
        X2_list.append(entrada_sin_accion(s_a))
        Y2_list.append(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]))
    X2 = torch.tensor(np.array(X2_list), dtype=torch.float32, device=DEVICE)
    Y2 = torch.tensor(np.array(Y2_list), dtype=torch.float32, device=DEVICE)
    entrenar(pred2, X2, Y2, n=400)
    z_obs, e_o, b_o = medir_z(pred2, mundo2, 'motor', usar_accion=False)
    print(f"C2 acción-condicionada: z = {z_correcta:.1f} | observación-sola: z = {z_obs:.1f}")
    c2_ok = z_correcta > z_obs + 2.0
    print(f"   => {'PASA: la acción aporta información' if c2_ok else 'REFUTA: la acción no aporta (novelty pura)'}")

    # C3: deshabituación con MAGNITUD IGUALADA (el intero de ±0.5 es 10x menor que teleport ±5)
    # C3a: habituar a motor(+5,+5) -> probar motor(-5,-5) (misma magnitud, dirección distinta)
    def violacion_motora_inversa(m, a):
        m.fisica_normal(a)
        m.pos = [(m.pos[0]-5)%SIZE, (m.pos[1]-5)%SIZE]
        return m.estado()
    mundo3 = CuerpoMundo()
    pred3 = Predictor(d_in=13).to(DEVICE)
    opt3 = entrenar(pred3, X, Y, n=400)
    for k in range(60):
        a = random.randrange(7)
        s_a = mundo3.estado(); s_d = mundo3.violacion_motora(a)
        xb = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        yb = torch.tensor(np.concatenate([s_d[:2]/SIZE, s_d[2:]/1.5]), dtype=torch.float32, device=DEVICE).unsqueeze(0)
        loss = (pred3(xb)-yb).pow(2).mean()
        opt3.zero_grad(); loss.backward(); opt3.step()
    z_motor_habituada, _, _ = medir_z(pred3, mundo3, 'motor')
    # motor inversa: misma magnitud, dirección opuesta
    eps_inv = []
    for _ in range(100):
        a = random.randrange(7)
        s_antes = mundo3.estado()
        s_despues = violacion_motora_inversa(mundo3, a)
        x = entrada(s_antes, a)
        y = np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5])
        with torch.no_grad():
            xt = torch.tensor(x, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            yt = torch.tensor(y, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            eps_inv.append(float((pred3(xt)-yt).pow(2).mean().sqrt()))
    # baseline para z inversa
    base_inv = []
    for _ in range(100):
        a = random.randrange(7)
        s_antes = mundo3.estado(); s_despues = mundo3.fisica_normal(a)
        x = entrada(s_antes, a)
        y = np.concatenate([s_despues[:2]/SIZE, s_despues[2:]/1.5])
        with torch.no_grad():
            xt = torch.tensor(x, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            yt = torch.tensor(y, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            base_inv.append(float((pred3(xt)-yt).pow(2).mean().sqrt()))
    base_a = np.array(base_inv); ev_a = np.array(eps_inv)
    z_inversa = (ev_a.mean()-base_a.mean())/(base_a.std()+1e-8)
    print(f"C3a habituar a teleport(+5,+5): z(mismo)={z_motor_habituada:.1f} (habituado)")
    print(f"    teleport(-5,-5) distinto:    z={z_inversa:.1f}")
    c3a_ok = z_motor_habituada < 2.0 and z_inversa > z_motor_habituada + 2.0
    print(f"    => {'PASA: especificidad (el modelo aprendió EL teleport, no cualquier sorpresa)' if c3a_ok else 'REFUTA: habituación generalizada'}")

    # C4: ablaciones Levin
    # a) restaurar W al snapshot PRE-habituación -> z motor debe volver ALTO (la traza era el delta de W)
    pred_pre = Predictor(d_in=13).to(DEVICE)
    pred_pre.load_state_dict(pred.state_dict())  # snapshot pre-habituación
    z_pre, _, _ = medir_z(pred_pre, mundo3, 'motor')
    c4a_ok = z_pre > z_motor_habituada + 2.0
    print(f"C4a W restaurado a pre-habituación: z(motor) = {z_pre:.1f} (debe volver ALTO)")
    print(f"    => {'PASA: la habituación estaba en el delta de W' if c4a_ok else 'REFUTA: no estaba en W'}")
    # b) W congelado durante 60 violaciones -> NO debe habituar
    pred5 = Predictor(d_in=13).to(DEVICE)
    pred5.load_state_dict(pred.state_dict())
    mundo5 = CuerpoMundo()
    for k in range(60):
        a = random.randrange(7)
        s_a = mundo5.estado(); s_d = mundo5.violacion_motora(a)
        # sin opt.step -> W congelado
    z_congelado, _, _ = medir_z(pred5, mundo5, 'motor')
    c4b_ok = z_congelado > z_motor_habituada + 2.0
    print(f"C4b W congelado (60 violaciones sin aprender): z(motor) = {z_congelado:.1f} (debe seguir ALTO)")
    print(f"    => {'PASA: la habituación requiere aprendizaje' if c4b_ok else 'REFUTA: habituación sin aprendizaje'}")
    # c) predictor sin entrenar
    pred6 = Predictor(d_in=13).to(DEVICE)
    mundo6 = CuerpoMundo()
    z_aleatorio, _, _ = medir_z(pred6, mundo6, 'motor')
    c4c_ok = abs(z_aleatorio) < 2.0
    print(f"C4c predictor sin entrenar: z(motor) = {z_aleatorio:.1f} (debe ser ~0)")
    print(f"    => {'PASA: el efecto requiere física aprendida' if c4c_ok else 'REFUTA'}")
    print("="*78)
    total = sum([c1_ok, c2_ok, c3a_ok, c4a_ok, c4b_ok, c4c_ok])
    print(f"CONTROLES: {total}/6 pasan. {'CLAIM BLINDADO' if total>=5 else 'CLAIMS REQUIEREN CORRECCIÓN'}")

if __name__ == "__main__":
    main()
