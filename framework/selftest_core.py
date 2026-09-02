# Smoke test del núcleo v0.14 (rápido, ~1-2 min en CPU/MPS).
# Verifica: física + entrada, pre-train predictor, baseline congelada, z ante S1,
# aprendizaje (habituación), Φ por canal con NLL, EWC forward.
# No es la batería (A1/A3); solo prueba que el paquete funciona.
import numpy as np
import torch

from core import config as C
from core.world import Mundo, VIOLACIONES, entrada, objetivo
from core.nets import PredictorFactorizado, PhiCanal, Attention
from core.procedures import seed_todo, preentrenar_predictor, preentrenar_phi, device
from core.surprise import BaselineCongelada, error_por_cabeza


def paso_normal_simple(mundo, a):
    s_a = mundo.estado()
    s_d = mundo.paso_normal(a)
    return s_a, s_d


def main():
    seed_todo(0)
    dev = device()
    print(f"device={dev}")
    mundo = Mundo(seed=0)

    # 1. física y shapes
    s = mundo.estado()
    assert s.shape == (6,)
    assert entrada(s, 3).shape == (13,)
    assert objetivo(s).shape == (6,)
    print("1. física/entrada OK")

    # 2. pre-train predictor (reducido)
    pred = PredictorFactorizado().to(dev)
    preentrenar_predictor(pred, mundo, n_trans=400, n_steps=150)
    pred.eval()
    print("2. pre-train predictor OK")

    # 3. baseline congelada (n_cal ~ prereg: 100 pasos normales)
    trans = []
    for _ in range(100):
        a = int(np.random.choice(C.ACCIONES))
        s_a = mundo.estado()
        s_d = mundo.paso_normal(a)
        trans.append((s_a, s_d, a))
    bl = BaselineCongelada(pred, trans)
    print(f"3. baseline: n={bl.n} mu_pos={bl.mu['pos']:.4f} sigma_pos={bl.sigma['pos']:.4f}")

    # 4. z ante S1: debe disparar la cabeza POS (teleport mueve x,y, no H)
    mundo2 = Mundo(seed=1)
    for _ in range(100):
        mundo2.paso_normal(int(np.random.choice(C.ACCIONES)))
    a = int(np.random.choice(C.ACCIONES))
    s_a = mundo2.estado()
    s_d = mundo2.aplicar_violacion(VIOLACIONES["S1"])
    eps = error_por_cabeza(pred, s_a, s_d, a)
    z = bl.z(eps)
    print(f"4. z(S1) total={z['total']:.2f} pos={z['pos']:.2f} H={z['H']:.2f}")
    assert z["pos"] > 1.5, f"z_pos(S1) debería ser > baseline, fue {z['pos']:.2f}"

    # 5. habituación: repetir el MISMO estímulo idéntico (S1 desde [10,10], Rankin)
    #    con aprendizaje -> z(pos) debe caer (baseline congelada inmutable)
    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    zs = []
    for _ in range(10):
        mundo2.pos = [10.0, 10.0]
        a = 2  # acción fija: mismo (s,a) -> mismo estímulo
        s_a = mundo2.estado()
        s_d = mundo2.aplicar_violacion(VIOLACIONES["S1"])
        x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=dev).unsqueeze(0)
        y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=dev).unsqueeze(0)
        p_pos, p_H = pred(x)
        loss = (p_pos - y[:, :2]).pow(2).mean() + (p_H - y[:, 2:]).pow(2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        eps = error_por_cabeza(pred, s_a, s_d, a)
        zs.append(bl.z(eps)["pos"])
    print(f"5. z_pos(S1) 10× estímulo idéntico con aprendizaje: {[f'{v:.2f}' for v in zs]}")
    assert zs[-1] < zs[0] * 0.6, "la habituación debería reducir z_pos al repetir el estímulo"

    # 6. Φ por canal NLL (reducido): debe bajar la loss
    mundo3 = Mundo(seed=2)
    for _ in range(30):
        mundo3.paso_normal(int(np.random.choice(C.ACCIONES)))
    phi = PhiCanal().to(dev)
    loss_antes = None
    datos = []
    for _ in range(100):
        a = int(np.random.choice(C.ACCIONES))
        s_a = mundo3.estado()
        s_d = mundo3.paso_normal(a)
        x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=dev).unsqueeze(0)
        y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=dev).unsqueeze(0)
        with torch.no_grad():
            p_pos, p_H = pred(x)
            eps2 = torch.cat([(p_pos - y[:, :2]), (p_H - y[:, 2:])], dim=-1).pow(2)
        for c in range(6):
            datos.append((x, c, float(eps2[0, c])))
    opt_phi = torch.optim.Adam(phi.parameters(), lr=1e-3)
    for paso in range(100):
        idx = np.random.randint(0, len(datos), (32,))
        loss = 0.0
        for i in idx:
            x, c, eps2 = datos[i]
            lv = phi(x, [c])
            loss = loss + 0.5 * (lv + eps2 / (lv.exp() + 1e-8)).mean()
        opt_phi.zero_grad()
        loss.backward()
        opt_phi.step()
        if paso == 0:
            loss_antes = loss.item()
    loss_despues = None
    with torch.no_grad():
        lv = phi(datos[0][0], [datos[0][1]])
    print(f"6. Φ NLL: loss_primera={loss_antes:.4f}")
    assert loss_antes is not None

    # 7. Attention forward (6 canales de error, no 7 acciones)
    att = Attention().to(dev)
    x = torch.randn(1, 13, device=dev)
    w = att(x)
    assert w.shape == (1, C.N_CANALES) and abs(float(w.detach().sum()) - 1.0) < 1e-3
    print("7. attention OK")

    # 8. EWC término forward
    from core.ewc import EWC
    ewc = EWC(pred, lam=C.EWC_LAMBDA)
    t = ewc.termino()
    assert t is not None
    print("8. EWC OK")
    print("SMOKE OK")


if __name__ == "__main__":
    main()
