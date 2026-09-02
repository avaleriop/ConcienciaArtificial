#!/usr/bin/env python3
"""
BATERÍA RANKIN v0.14 (plan 64-A1, preregistro 63) - N=30 seeds 4000-4029.
Importa SOLO framework.core. z con baseline CONGELADA (100 pasos sin eventos), por cabeza.

Protocolo por seed (within-subject, orden fijo):
  Pre-train: 1200 transiciones + 400 steps predictor (63 §3).
  Calibración: 100 pasos normales -> BaselineCongelada (pos/H/canal/total).
  Habituación S1: teleport (+2,+2) x12 CON aprendizaje (z por trial, contexto variado:
                  pos inicial uniforme [5,15]^2 y accion aleatoria -> no es memorizar
                  una transicion, es habituar la CLASE "desplazamiento +2,+2").
  Sondas SIN aprendizaje: S2 (-2,-2), S3 (+2,-2), S4 (+4,+4) [z_pos], S5 (comer baja E,
                  setup explicito a comida) [z_H].
  Dishabituacion: re-sonda S1 tras S5 (Rankin 8).
  Recuperacion (ISI): gap 2000 pasos de fisica normal CON updates (solo fisica normal,
                  sin violaciones) -> re-sonda S1 (Rankin 10).
  Savings: re-habituar S1 contando trials hasta z_pos < 0.5*z_0 (max 20).
  SVD: dW = W_post_hab - W_pre_hab por capa, singulares acumulados 90% (H_rank).

Reglas (63 §4): umbrales fijos; seed con std base <1e-4 se excluye y se documenta;
se reporta epsilon crudo ademas de z; sin recalibracion post-hoc.
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


def posicion_inicial(rng, magnitud=2.0):
    """Contexto SIN niebla (x<=13) y sin clip para teleports de hasta +4:
    x ~ U[5,13], y ~ U[5,15]. La niebla es dominio del 4-arm (A3), no de Rankin.
    """
    x = float(rng.uniform(5.0, 13.0))
    y = float(rng.uniform(5.0, 15.0))
    return [x, y]


ZONA_PRUEBA = (5.0, 13.0, 5.0, 15.0)  # misma zona para pre-train y sondas


def ci_bootstrap(arr, n=2000, q=0.95):
    arr = np.asarray(arr, dtype=float)
    if arr.size == 0 or np.isnan(arr).all():
        return float("nan"), float("nan")
    rng = np.random.default_rng(0)
    lo, hi = (1 - q) / 2, 1 - (1 - q) / 2
    means = np.array([rng.choice(arr, size=arr.size, replace=True).mean() for _ in range(n)])
    return float(np.quantile(means, lo)), float(np.quantile(means, hi))


def run_seed(seed, n_hab=12, gap_steps=2000):
    seed_todo(seed)
    dev = device()
    rng = np.random.default_rng(seed + 1_000_000)
    mundo = Mundo(seed=seed)

    # Pre-train (misma zona sin niebla que las sondas)
    pred = PredictorFactorizado().to(dev)
    preentrenar_predictor(pred, mundo, n_trans=1200, n_steps=400, zona=ZONA_PRUEBA)

    # Calibracion (baseline congelada, SIN eventos; mismo contexto que las sondas)
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

    # Snapshots para SVD
    w_pre = {n: p.detach().clone() for n, p in pred.named_parameters()}

    def probar(clave_violacion, con_aprendizaje=True, comer=False):
        """Un trial de violacion: contexto variado, mide z con baseline congelada."""
        mundo.pos = posicion_inicial(rng)
        a = int(rng.integers(0, 7))
        s_a = mundo.estado()
        if comer:
            s_a_setup, s_d = mundo.paso_con_comida_invertida(a)
            eps = error_por_cabeza(pred, s_a_setup, s_d, a)
        else:
            mundo.aplicar_violacion(VIOLACIONES[clave_violacion])
            s_d = mundo.estado()
            eps = error_por_cabeza(pred, s_a, s_d, a)
        z = bl.z(eps)
        if con_aprendizaje:
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=dev).unsqueeze(0)
            y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=dev).unsqueeze(0)
            p_pos, p_H = pred(x)
            loss = (p_pos - y[:, :2]).pow(2).mean() + (p_H - y[:, 2:]).pow(2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
        return {"z_pos": float(z["pos"]), "z_H": float(z["H"]), "z_total": float(z["total"]),
                "eps_pos": float(eps["pos"]), "eps_H": float(eps["H"])}

    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)

    # FASE 1: habituacion S1 (+2,+2) con aprendizaje
    hab = []
    for _ in range(n_hab):
        hab.append(probar("S1", con_aprendizaje=True))
    z_0 = hab[0]["z_pos"]
    z_hab = float(np.mean([h["z_pos"] for h in hab[-4:]]))
    w_post = {n: p.detach().clone() for n, p in pred.named_parameters()}

    # FASE 2: sondas SIN aprendizaje
    s2 = probar("S2", con_aprendizaje=False)
    s3 = probar("S3", con_aprendizaje=False)
    s4 = probar("S4", con_aprendizaje=False)
    s5 = probar("S5", con_aprendizaje=False, comer=True)

    # FASE 3: dishabituacion (re-sonda S1 sin aprendizaje)
    reprobe = probar("S1", con_aprendizaje=False)

    # FASE 4: recuperacion ISI (gap de fisica normal, sin violaciones, con updates)
    for i in range(gap_steps):
        a = int(rng.integers(0, 7))
        s_a = mundo.estado()
        s_d = mundo.paso_normal(a)
        if i % 32 == 31:
            x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=dev).unsqueeze(0)
            y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=dev).unsqueeze(0)
            p_pos, p_H = pred(x)
            loss = (p_pos - y[:, :2]).pow(2).mean() + (p_H - y[:, 2:]).pow(2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
    z_gap = probar("S1", con_aprendizaje=False)["z_pos"]

    # FASE 5: savings (re-habituar, contar trials hasta <50% de z_0)
    savings = None
    for i in range(20):
        r = probar("S1", con_aprendizaje=True)
        if r["z_pos"] < 0.5 * z_0:
            savings = i + 1
            break
    if savings is None:
        savings = 20

    # SVD de dW (H_rank): capas encoder y cabezas
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
            "z0": float(z_0), "z_hab": z_hab,
            "reduccion": float((z_0 - z_hab) / (z_0 + 1e-8)),
            "z_S2_pos": float(s2["z_pos"]), "z_S3_pos": float(s3["z_pos"]),
            "z_S4_pos": float(s4["z_pos"]), "z_S5_H": float(s5["z_H"]),
            "eps_S5_H": float(s5["eps_H"]),
            "z_reprobe_pos": float(reprobe["z_pos"]),
            "z_gap_pos": float(z_gap),
            "savings": savings,
            "hab_zpos": [float(h["z_pos"]) for h in hab],
            "svd": svd}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--out", type=str, default="results/v014_rankin.json")
    ap.add_argument("--nhab", type=int, default=12)
    ap.add_argument("--gap", type=int, default=2000)
    args = ap.parse_args()

    assert C.SEEDS_RANKIN[0] == 4000, "seeds fijas 4000-4029 (prereg 63)"
    results = []
    for i, seed in enumerate(range(C.SEEDS_RANKIN[0], C.SEEDS_RANKIN[0] + args.seeds)):
        r = run_seed(seed, n_hab=args.nhab, gap_steps=args.gap)
        results.append(r)
        tag = "EXCL" if r.get("excluida") else "ok"
        print(f"seed {seed} [{tag}] z0={r.get('z0', float('nan')):.1f} "
              f"z_hab={r.get('z_hab', float('nan')):.1f} "
              f"red={r.get('reduccion', float('nan')):.2f} "
              f"zS2={r.get('z_S2_pos', float('nan')):.1f} zS3={r.get('z_S3_pos', float('nan')):.1f} "
              f"zS4={r.get('z_S4_pos', float('nan')):.1f} zS5H={r.get('z_S5_H', float('nan')):.1f} "
              f"z_re={r.get('z_reprobe_pos', float('nan')):.1f} z_gap={r.get('z_gap_pos', float('nan')):.1f} "
              f"sav={r.get('savings')}", flush=True)

    excl = [r for r in results if r.get("excluida")]
    inc = [r for r in results if not r.get("excluida")]
    n = len(inc)

    def res(key):
        return [r[key] for r in inc]

    z0_arr = np.array(res("z0"))
    zhab_arr = np.array(res("z_hab"))
    red_arr = np.array(res("reduccion"))
    z2 = np.array(res("z_S2_pos"))
    z3 = np.array(res("z_S3_pos"))
    z4 = np.array(res("z_S4_pos"))
    z5h = np.array(res("z_S5_H"))
    zre = np.array(res("z_reprobe_pos"))
    zgap = np.array(res("z_gap_pos"))
    sav = np.array(res("savings"))

    def line(nombre, arr, ref=None):
        lo, hi = ci_bootstrap(arr)
        d = ""
        if ref is not None:
            dif = arr - ref
            dl, dh = ci_bootstrap(dif)
            sd = np.sqrt(((len(dif) - 1) * dif.var()) / (len(dif) - 1) + 1e-12)
            d = f" d_pareado={float(dif.mean() / (dif.std() + 1e-12)):.2f} CI_d=[{dl:.2f},{dh:.2f}]"
        print(f"  {nombre:<28} media={float(arr.mean()):.2f} CI95=[{lo:.2f},{hi:.2f}]{d}")

    print(f"\n=== A1 RANKIN v0.14 | N={n} incluidas, {len(excl)} excluidas ===")
    line("H1 z0 deteccion S1", z0_arr)
    line("H2 z_hab (ult 4)", zhab_arr)
    print(f"  {'reduccion (z0->z_hab)':<28} media={float(red_arr.mean()):.2f} "
          f"CI95={ci_bootstrap(red_arr)}")
    line("H_A z(S2) same-mag", z2, zhab_arr)
    line("H_A z(S3) ortho", z3, zhab_arr)
    line("z(S4) magnitud x2", z4, zhab_arr)
    line("z(S5) interoceptivo H", z5h)
    line("H_dis z(S1) reprobe", zre, zhab_arr)
    line("H_rec z(S1) gap", zgap, zhab_arr)
    print(f"  {'savings (trials a <50% z0)':<28} media={float(sav.mean()):.1f} "
          f"CI95={ci_bootstrap(sav)}")

    k90 = []
    for r in inc:
        for n, v in r["svd"].items():
            if "f_pos.weight" in n and v["k90"]:
                k90.append(v["k90"])
    if k90:
        print(f"  SVD dW f_pos: singulares para 90% varianza media={float(np.mean(k90)):.1f}")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"n_hab": args.nhab, "gap_steps": args.gap, "results": results}, f, indent=2)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
