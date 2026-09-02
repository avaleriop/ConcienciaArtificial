#!/usr/bin/env python3
"""
BATERÍA RANKIN v0.14 rev.2 (plan 64-A1, prereg 63, corregida por peer review 2 Sep 2026).
N=30 seeds 4000-4029. Importa SOLO framework.core.

CORRECCIÓN (peer review): el protocolo v1 habituaba con teleport puro (OFFSET) y con
updates solo de violación -> inyectaba un offset +2,+2 incondicional (z_NORM=8.25: el
modelo dejaba de predecir la física normal; S2>S1 era la firma del offset, no
especificidad). Ver framework/bateria_control_habituacion.py (N=30, decisivo).

Protocolo rev.2 (INTERCAL, validado: z_NORM=0.81 -> el modelo sigue siendo P(s'|s,a)):
  La violación ocurre SOBRE la contingencia real: paso_normal(a) y LUEGO teleport.
  Cada evento S1 va seguido de K pasos de física normal CON updates (el agente sigue
  viviendo; el evento es raro, no domina el gradiente).

  FASE 0: pre-train 1200 trans + 400 steps; baseline congelada (100 pasos sin eventos).
  FASE 1: z0 = z(S1) pre-aprendizaje + z_NORM_0 (integridad del modelo intacto).
  FASE 2: habituación INTERCAL: 12 eventos S1 (violación CONTING) × K=10 pasos normales
          con updates entre eventos.
  FASE 3: sondas SIN aprendizaje: S2 (−2,−2), S3 (+2,−2), S4 (+4,+4) [z_pos],
          S5 (comer baja E, setup a comida) [z_H], y z_NORM (¿el modelo sigue vivo?).
  FASE 4: dishabituación: re-sonda S1 tras S5 (Rankin 8).
  FASE 5: ISI con pesos CONGELADOS: 2000 pasos de física normal SIN opt.step
          -> re-sonda S1 (Rankin 10 real: reposo, no desaprendizaje).
  FASE 6: savings: re-habituar contando eventos hasta z_pos < 0.5·z0 (max 20).
  SVD: dW = W_post − W_pre por capa (H_rank).

Reglas (63 §4): umbrales fijos; seed con σ base <1e-4 excluida y documentada; se reporta
ε crudo; reducción con z_hab recortado a ≥0 (z<0 = error bajo baseline, no "más habituado").
Ejecuta: python3 framework/bateria_rankin.py --seeds 30
"""
import argparse
import json
import os
import numpy as np
import torch

from core import config as C
from core.world import Mundo, VIOLACIONES, entrada, objetivo
from core.nets import PredictorFactorizado
from core.surprise import BaselineCongelada, error_por_cabeza
from core.procedures import seed_todo, preentrenar_predictor, device

ZONA_PRUEBA = (5.0, 13.0, 5.0, 15.0)
TP_S1 = VIOLACIONES["S1"]["teleport"]


def posicion_inicial(rng):
    return [float(rng.uniform(5.0, 13.0)), float(rng.uniform(5.0, 15.0))]


def ci_bootstrap(arr, n=2000, q=0.95):
    arr = np.asarray(arr, dtype=float)
    if arr.size == 0 or np.isnan(arr).all():
        return float("nan"), float("nan")
    rng = np.random.default_rng(0)
    lo, hi = (1 - q) / 2, 1 - (1 - q) / 2
    means = np.array([rng.choice(arr, size=arr.size, replace=True).mean() for _ in range(n)])
    return float(np.quantile(means, lo)), float(np.quantile(means, hi))


def run_seed(seed, n_hab=12, k_intercal=10, gap_steps=2000):
    seed_todo(seed)
    dev = device()
    rng = np.random.default_rng(seed + 1_000_000)
    mundo = Mundo(seed=seed)

    pred = PredictorFactorizado().to(dev)
    preentrenar_predictor(pred, mundo, n_trans=1200, n_steps=400, zona=ZONA_PRUEBA)

    trans = []
    for _ in range(100):
        mundo.pos = posicion_inicial(rng)
        a = int(rng.integers(0, 7))
        s_a = mundo.estado()
        s_d = mundo.paso_normal(a)
        trans.append((s_a, s_d, a))
    bl = BaselineCongelada(pred, trans)
    if bl.sigma["pos"] < 1e-4 or bl.sigma["H"] < 1e-4:
        return {"seed": seed, "excluida": True,
                "razon": "std base < 1e-4 (sin baseline para z; regla 63 §4)"}

    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    w_pre = {n: p.detach().clone() for n, p in pred.named_parameters()}

    def z_de(s_a, s_d, a):
        eps = error_por_cabeza(pred, s_a, s_d, a)
        z = bl.z(eps)
        return {"z_pos": float(z["pos"]), "z_H": float(z["H"]), "z_total": float(z["total"]),
                "eps_pos": float(eps["pos"]), "eps_H": float(eps["H"])}

    def actualizar(s_a, s_d, a):
        x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=dev).unsqueeze(0)
        y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=dev).unsqueeze(0)
        p_pos, p_H = pred(x)
        loss = (p_pos - y[:, :2]).pow(2).mean() + (p_H - y[:, 2:]).pow(2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()

    def violacion_sobre_contingencia(a, dx=TP_S1[0], dy=TP_S1[1]):
        """paso_normal(a) y LUEGO teleport: la física de a ocurre (P(s'|s,a) viva)."""
        mundo.pos = posicion_inicial(rng)
        s_a = mundo.estado()
        s_d = mundo.paso_con_violacion(a, dx, dy)
        return s_a, s_d

    def sondea_s1(n=8, dx=TP_S1[0], dy=TP_S1[1]):
        vals = []
        for _ in range(n):
            a = int(rng.integers(0, 7))
            s_a, s_d = violacion_sobre_contingencia(a, dx, dy)
            vals.append(z_de(s_a, s_d, a)["z_pos"])
        return float(np.mean(vals))

    def sondea_norm(n=8):
        vals = []
        for _ in range(n):
            mundo.pos = posicion_inicial(rng)
            a = int(rng.integers(0, 7))
            s_a = mundo.estado()
            s_d = mundo.paso_normal(a)
            vals.append(z_de(s_a, s_d, a)["z_pos"])
        return float(np.mean(vals))

    # FASE 1: z0 pre-aprendizaje + integridad del modelo intacto
    z0 = sondea_s1()
    z_norm_0 = sondea_norm()

    # FASE 2: habituación INTERCAL (evento sobre contingencia + vida normal entre eventos)
    hab = []
    for _ in range(n_hab):
        a = int(rng.integers(0, 7))
        s_a, s_d = violacion_sobre_contingencia(a)
        hab.append(z_de(s_a, s_d, a)["z_pos"])
        actualizar(s_a, s_d, a)
        for _ in range(k_intercal):
            a2 = int(rng.integers(0, 7))
            mundo.pos = posicion_inicial(rng)
            s_a2 = mundo.estado()
            s_d2 = mundo.paso_normal(a2)
            actualizar(s_a2, s_d2, a2)
    z_hab = float(np.mean(hab[-4:]))
    reduccion = float((z0 - max(z_hab, 0.0)) / (z0 + 1e-8))
    w_post = {n: p.detach().clone() for n, p in pred.named_parameters()}

    # FASE 3: sondas SIN aprendizaje
    def sonda_tipo(dx, dy):
        vals = []
        for _ in range(8):
            a = int(rng.integers(0, 7))
            s_a, s_d = violacion_sobre_contingencia(a, dx, dy)
            vals.append(z_de(s_a, s_d, a)["z_pos"])
        return float(np.mean(vals))

    z_S2 = sonda_tipo(*VIOLACIONES["S2"]["teleport"])
    z_S3 = sonda_tipo(*VIOLACIONES["S3"]["teleport"])
    z_S4 = sonda_tipo(*VIOLACIONES["S4"]["teleport"])
    z_norm = sondea_norm()

    def sonda_s5():
        vals = []
        for _ in range(8):
            mundo.pos = posicion_inicial(rng)
            a = int(rng.integers(0, 7))
            s_a_setup, s_d = mundo.paso_con_comida_invertida(a)
            eps = error_por_cabeza(pred, s_a_setup, s_d, a)
            vals.append(float(bl.z(eps)["H"]))
        return float(np.mean(vals))

    z_S5_H = sonda_s5()

    # FASE 4: dishabituación (re-sonda S1 tras S5, sin aprendizaje)
    z_reprobe = sondea_s1()

    # FASE 5: ISI REAL — pesos CONGELADOS durante el gap (sin opt.step)
    for _ in range(gap_steps):
        a = int(rng.integers(0, 7))
        mundo.paso_normal(a)
    z_gap = sondea_s1()

    # FASE 6: savings (re-habituar INTERCAL, contar eventos hasta <50% de z0)
    savings = 20
    for i in range(20):
        a = int(rng.integers(0, 7))
        s_a, s_d = violacion_sobre_contingencia(a)
        actualizar(s_a, s_d, a)
        for _ in range(k_intercal):
            a2 = int(rng.integers(0, 7))
            mundo.pos = posicion_inicial(rng)
            s_a2 = mundo.estado()
            s_d2 = mundo.paso_normal(a2)
            actualizar(s_a2, s_d2, a2)
        if sondea_s1(n=1) < 0.5 * z0:
            savings = i + 1
            break

    # SVD ΔW (H_rank): capa encoder y cabezas
    svd = {}
    for n, p in pred.named_parameters():
        if "weight" in n:
            dW = (p.detach() - w_pre[n].to(dev)).cpu().numpy()
            try:
                s = np.linalg.svd(dW, compute_uv=False)
                acum = np.cumsum(s ** 2) / (np.sum(s ** 2) + 1e-12)
                k90 = int(np.searchsorted(acum, 0.90) + 1)
                svd[n] = {"k90": k90, "sing": [float(v) for v in s[:8]]}
            except np.linalg.LinAlgError:
                svd[n] = {"k90": None, "sing": []}

    return {"seed": seed, "excluida": False,
            "z0": float(z0), "z_norm_0": z_norm_0,
            "z_hab": z_hab, "reduccion": reduccion,
            "hab_zpos": [float(v) for v in hab],
            "z_S2_pos": z_S2, "z_S3_pos": z_S3, "z_S4_pos": z_S4,
            "z_S5_H": z_S5_H, "z_norm": z_norm,
            "z_reprobe_pos": z_reprobe, "z_gap_pos": z_gap,
            "savings": savings, "svd": svd}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--out", type=str, default="results/v014_rankin.json")
    ap.add_argument("--nhab", type=int, default=12)
    ap.add_argument("--kintercal", type=int, default=10)
    ap.add_argument("--gap", type=int, default=2000)
    args = ap.parse_args()

    results = []
    for seed in range(C.SEEDS_RANKIN[0], C.SEEDS_RANKIN[0] + args.seeds):
        r = run_seed(seed, n_hab=args.nhab, k_intercal=args.kintercal, gap_steps=args.gap)
        results.append(r)
        tag = "EXCL" if r.get("excluida") else "ok"
        print(f"seed {seed} [{tag}] z0={r.get('z0', float('nan')):.1f} "
              f"z_hab={r.get('z_hab', float('nan')):.1f} red={r.get('reduccion', float('nan')):.2f} "
              f"norm0={r.get('z_norm_0', float('nan')):.1f}->{r.get('z_norm', float('nan')):.1f} "
              f"S2={r.get('z_S2_pos', float('nan')):.1f} S3={r.get('z_S3_pos', float('nan')):.1f} "
              f"S4={r.get('z_S4_pos', float('nan')):.1f} S5H={r.get('z_S5_H', float('nan')):.1f} "
              f"re={r.get('z_reprobe_pos', float('nan')):.1f} gap={r.get('z_gap_pos', float('nan')):.1f} "
              f"sav={r.get('savings')}", flush=True)

    excl = [r for r in results if r.get("excluida")]
    inc = [r for r in results if not r.get("excluida")]
    n = len(inc)

    def res(key):
        return np.array([r[key] for r in inc])

    def line(nombre, arr, ref=None):
        lo, hi = ci_bootstrap(arr)
        d = ""
        if ref is not None:
            dif = arr - ref
            dl, dh = ci_bootstrap(dif)
            d = f" d_pareado={float(dif.mean() / (dif.std() + 1e-12)):.2f} CI_d=[{dl:.2f},{dh:.2f}]"
        print(f"  {nombre:<30} media={float(arr.mean()):.2f} CI95=[{lo:.2f},{hi:.2f}]{d}")

    z0 = res("z0"); zhab = res("z_hab"); red = res("reduccion")
    print(f"\n=== A1 RANKIN v0.14 rev.2 (INTERCAL) | N={n} incluidas, {len(excl)} excluidas ===")
    line("z0 deteccion S1 (pre-aprendizaje)", z0)
    line("z_NORM_0 (modelo intacto)", res("z_norm_0"))
    line("H2 z_hab (ult 4 eventos)", zhab)
    print(f"  {'reduccion (z0->z_hab, z_hab>=0)':<30} media={float(red.mean()):.2f} "
          f"CI95={ci_bootstrap(red)}")
    line("z_NORM post-habituacion (integ.)", res("z_norm"))
    line("z(S2) -2,-2", res("z_S2_pos"), zhab)
    line("z(S3) +2,-2", res("z_S3_pos"), zhab)
    line("z(S4) +4,+4", res("z_S4_pos"), zhab)
    line("z(S5) interoceptivo H", res("z_S5_H"))
    line("Rankin8 z(S1) reprobe", res("z_reprobe_pos"), zhab)
    line("Rankin10 z(S1) gap FROZEN", res("z_gap_pos"), zhab)
    print(f"  {'savings (eventos a <50% z0)':<30} media={float(res('savings').mean()):.1f} "
          f"CI95={ci_bootstrap(res('savings'))}")

    k90 = []
    for r in inc:
        for name, v in r["svd"].items():
            if "f_pos.weight" in name and v["k90"]:
                k90.append(v["k90"])
    if k90:
        print(f"  SVD dW f_pos: sing. 90%% varianza media={float(np.mean(k90)):.1f}")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"version": "rev2_intercal", "n_hab": args.nhab,
                   "k_intercal": args.kintercal, "gap_steps": args.gap,
                   "results": results}, f, indent=2)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
