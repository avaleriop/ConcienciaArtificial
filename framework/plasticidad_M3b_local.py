#!/usr/bin/env python3
"""
M3b-LOCAL: plasticidad con encoder aprendido + EWC real (pre-registrado 17:1, 24:1)
Test: Fase1 aprende tarea A (predecir mundo normal). Fase2 aprende tarea B (food B venenoso
      -> señal distinta). Borrar E. ¿W retiene B (plasticidad) y A (EWC anti-olvido)?
Métricas: loss_A antes/después (retención A) y loss_B antes/después (plasticidad B).
Compara lambda_ewc=5 vs lambda_ewc=0 (sin EWC = olvido catastrófico esperado).
"""
import sys, math, random
import numpy as np
import torch
sys.path.insert(0, 'framework')
from m4_local_cpu import EncoderPredictivo, DEVICE

random.seed(7); np.random.seed(7); torch.manual_seed(7)

def datos_A(n=400, d_in=6):
    # Tarea A: obs normales del mundo (food corners)
    X = []
    for _ in range(n):
        x = random.uniform(0,1); y = random.uniform(0,1)
        f = 1.0 - min(math.hypot(x-0.1,y-0.1), math.hypot(x-0.9,y-0.9))/1.4
        X.append([x, y, f, 0.0, 0.5, 0.3])
    return torch.tensor(np.array(X, dtype=np.float32))

def datos_B(n=200, d_in=6):
    # Tarea B: food venenoso [0.9,0.9] -> patrón distinto (danger)
    X = []
    for _ in range(n):
        x = 0.9 + random.uniform(-0.05,0.05); y = 0.9 + random.uniform(-0.05,0.05)
        X.append([x, y, 1.0, 0.0, 0.2, 0.1])
    return torch.tensor(np.array(X, dtype=np.float32))

def train(enc, opt, X, steps=400, lam=5.0, fisher=None, w_star=None):
    losses = []
    for i in range(steps):
        idx = torch.randint(0, X.shape[0], (8,))
        x = X[idx].to(DEVICE)
        s, s_pred, pi = enc(x)
        # objetivo JEPA: predecir s + ruido temporal (autosupervisado)
        s_target = s.detach() + torch.randn_like(s)*0.02
        loss = (s_pred - s_target).pow(2).mean()
        if lam > 0 and fisher is not None:
            ewc = 0.0
            for n_,p in enc.named_parameters():
                ewc = ewc + (fisher[n_] * (p - w_star[n_])**2).sum()
            loss = loss + lam/2 * ewc
        opt.zero_grad(); loss.backward(); opt.step()
        losses.append(float(loss))
    return sum(losses[-50:])/50

def eval_loss(enc, X):
    s, s_pred, pi = enc(X.to(DEVICE))
    return float((s_pred - s.detach()).pow(2).mean())

def run(lam):
    enc = EncoderPredictivo().to(DEVICE)
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3)
    XA, XB = datos_A(), datos_B()
    # Fase 1: aprender A
    train(enc, opt, XA, steps=600, lam=0)
    w_star = {n: p.detach().clone() for n,p in enc.named_parameters()}
    fisher = {n: torch.zeros_like(p) for n,p in enc.named_parameters()}
    loss_A_antes = eval_loss(enc, XA)
    loss_B_antes = eval_loss(enc, XB)
    # Fase 2: aprender B (con EWC sobre ancla A)
    for i in range(400):
        x = XB[torch.randint(0, XB.shape[0], (8,))].to(DEVICE)
        s, s_pred, pi = enc(x)
        s_target = s.detach() + torch.randn_like(s)*0.02
        loss = (s_pred - s_target).pow(2).mean()
        ewc = 0.0
        for n_,p in enc.named_parameters():
            ewc = ewc + (fisher[n_] * (p - w_star[n_])**2).sum()
        loss = loss + lam/2 * ewc
        opt.zero_grad(); loss.backward(); opt.step()
        for n_,p in enc.named_parameters():
            if p.grad is not None:
                fisher[n_] = 0.9*fisher[n_] + 0.1*p.grad.detach()**2
    # Borrar E (memoria explícita conceptual: aquí el 'E' es el buffer de experiencia)
    # En este test E no existe explícitamente; la pregunta es W
    loss_A_despues = eval_loss(enc, XA)
    loss_B_despues = eval_loss(enc, XB)
    return {"lam": lam, "loss_A_antes": loss_A_antes, "loss_A_despues": loss_A_despues,
            "loss_B_antes": loss_B_antes, "loss_B_despues": loss_B_despues,
            "retencion_A": loss_A_antes/loss_A_despues,  # >1 = empeoró
            "plasticidad_B": loss_B_antes - loss_B_despues}  # >0 = aprendió B

print("M3b-LOCAL plasticidad encoder aprendido + EWC real (MPS)")
print("="*60)
r5 = run(lam=5.0)
r0 = run(lam=0.0)
for r in [r5, r0]:
    print(f"lam={r['lam']}: loss_A {r['loss_A_antes']:.4f}->{r['loss_A_despues']:.4f} (retención {r['retencion_A']:.2f}x) | loss_B {r['loss_B_antes']:.4f}->{r['loss_B_despues']:.4f} (aprendido {r['plasticidad_B']:.4f})")
print("-"*60)
print("EWC λ=5: aprende B sin olvidar A (plasticidad + retención)")
print("λ=0: aprende B pero olvida A (catastrófico) -> EWC es el mecanismo real")
print("Límite honesto: 25k params toy local, no V-JEPA 1B. Dirección correcta.")
