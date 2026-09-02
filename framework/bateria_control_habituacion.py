#!/usr/bin/env python3
"""
CONTROL DE INTERPRETACIÓN (peer review, 2 Sep 2026) — decide si A1 midió
"especificidad de dirección" o "offset +2,+2 inyectado". Correr ANTES de A2/A3.

Protocolo por seed (N=30, 4000-4029): pre-train común + baseline congelada (100 pasos
normales sin eventos). Luego TRES brazos de habituación (12 violaciones c/u), cada uno
partiendo de un CLON del predictor pre-habituación:

  OFFSET   : violación = teleport puro sin física (protocolo A1 actual).
  CONTING  : violación = paso_normal(a) + teleport DESPUÉS (física real de a ocurre).
  INTERCAL : igual que CONTING pero con 5 pasos normales CON updates entre violaciones
             (el modelo sigue viendo física normal mientras habitúa).

Sondas tras cada brazo (baseline congelada, SIN aprendizaje, 8 repeticiones → media):
  z_NORM : física normal sin teleport.  SI ALTO → el modelo ya no predice P(s'|s,a).
  z_S1   : la misma violación entrenada.
  z_S2   : dirección opuesta (−2,−2).
  z_S1_a0 vs z_S1_a3 : S1 sondeado con acción 0 vs 3 (¿el error depende de a, o el
             modelo aprendió un offset incondicional?).

Rankin-10 ISI limpio (en CONTING): tras habituar, gap de 2000 pasos de física normal
SIN ningún opt.step (pesos congelados) → z_S1. Si no sube: no hay recuperación
espontánea en reposo (la "recuperación" de A1 era desaprendizaje, no ISI).

Reglas: umbrales fijos; nada se recalibra; z por cabeza pos.
Ejecuta: python3 framework/bateria_control_habituacion.py --seeds 30
"""
import argparse
import copy
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


class Protocolo:
    def __init__(self, seed):
        self.dev = device()
        self.rng = np.random.default_rng(seed + 1_000_000)
        self.mundo = Mundo(seed=seed)
        self.pred_base = PredictorFactorizado().to(self.dev)
        preentrenar_predictor(self.pred_base, self.mundo, n_trans=1200, n_steps=400,
                              zona=ZONA_PRUEBA)
        trans = []
        for _ in range(100):
            self.mundo.pos = posicion_inicial(self.rng)
            a = int(self.rng.integers(0, 7))
            s_a = self.mundo.estado()
            s_d = self.mundo.paso_normal(a)
            trans.append((s_a, s_d, a))
        self.bl = BaselineCongelada(self.pred_base, trans)
        self.ok = self.bl.sigma["pos"] >= 1e-4

    def clon(self):
        return copy.deepcopy(self.pred_base)

    def actualizar(self, pred, s_a, s_d, a, opt):
        x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=self.dev).unsqueeze(0)
        y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=self.dev).unsqueeze(0)
        p_pos, p_H = pred(x)
        loss = (p_pos - y[:, :2]).pow(2).mean() + (p_H - y[:, 2:]).pow(2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()

    def z_pos(self, pred, s_a, s_d, a):
        eps = error_por_cabeza(pred, s_a, s_d, a)
        return float(self.bl.z(eps)["pos"])

    def violar(self, brazo, a, dx=2.0, dy=2.0):
        """Aplica la violación según el brazo; devuelve s_d."""
        s_a = self.mundo.estado()
        if brazo == "OFFSET":
            self.mundo.aplicar_violacion({"teleport": (dx, dy)})
        else:
            self.mundo.paso_con_violacion(a, dx, dy)
        return s_a

    def habituar(self, pred, brazo, n_hab=12):
        opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
        for _ in range(n_hab):
            self.mundo.pos = posicion_inicial(self.rng)
            a = int(self.rng.integers(0, 7))
            s_a = self.violar(brazo, a)
            s_d = self.mundo.estado()
            self.actualizar(pred, s_a, s_d, a, opt)
            if brazo == "INTERCAL":
                for _ in range(5):
                    a2 = int(self.rng.integers(0, 7))
                    s_a2 = self.mundo.estado()
                    s_d2 = self.mundo.paso_normal(a2)
                    self.actualizar(pred, s_a2, s_d2, a2, opt)

    def sondea(self, pred, brazo, dx=2.0, dy=2.0, n=8):
        """z medio de n sondas SIN aprendizaje."""
        out = {"S1": [], "S2": [], "NORM": []}
        for _ in range(n):
            a = int(self.rng.integers(0, 7))
            self.mundo.pos = posicion_inicial(self.rng)
            # NORM: física normal
            s_a = self.mundo.estado()
            s_d = self.mundo.paso_normal(a)
            out["NORM"].append(self.z_pos(pred, s_a, s_d, a))
            # S1
            self.mundo.pos = posicion_inicial(self.rng)
            s_a = self.violar(brazo, a, 2.0, 2.0)
            s_d = self.mundo.estado()
            out["S1"].append(self.z_pos(pred, s_a, s_d, a))
            # S2
            self.mundo.pos = posicion_inicial(self.rng)
            s_a = self.violar(brazo, a, -2.0, -2.0)
            s_d = self.mundo.estado()
            out["S2"].append(self.z_pos(pred, s_a, s_d, a))
        # acción fija 0 vs 3 para S1
        for etiqueta, af in (("S1_a0", 0), ("S1_a3", 3)):
            self.mundo.pos = posicion_inicial(self.rng)
            s_a = self.violar(brazo, af, 2.0, 2.0)
            s_d = self.mundo.estado()
            out[etiqueta] = self.z_pos(pred, s_a, s_d, af)
        return {k: float(np.mean(v)) if isinstance(v, list) else float(v)
                for k, v in out.items()}


def run_seed(seed, n_hab=12, gap_steps=2000):
    p = Protocolo(seed)
    if not p.ok:
        return {"seed": seed, "excluida": True, "razon": "std base < 1e-4"}
    brazos = {}
    for brazo in ("OFFSET", "CONTING", "INTERCAL"):
        pred = p.clon()
        p.habituar(pred, brazo, n_hab)
        brazos[brazo] = p.sondea(pred, brazo)

    # Rankin-10 ISI limpio: CONTING + gap SIN updates
    pred = p.clon()
    p.habituar(pred, "CONTING", n_hab)
    pre = p.sondea(pred, "CONTING", n=8)["S1"]
    for _ in range(gap_steps):
        a = int(p.rng.integers(0, 7))
        p.mundo.paso_normal(a)  # sin opt.step: pesos congelados
    post = p.sondea(pred, "CONTING", n=8)["S1"]
    return {"seed": seed, "excluida": False, "brazos": brazos,
            "rankin10": {"pre": pre, "post_frozen": post}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--out", type=str, default="results/v014_control_habituacion.json")
    ap.add_argument("--nhab", type=int, default=12)
    ap.add_argument("--gap", type=int, default=2000)
    args = ap.parse_args()

    results = []
    for seed in range(4000, 4000 + args.seeds):
        r = run_seed(seed, n_hab=args.nhab, gap_steps=args.gap)
        results.append(r)
        if not r.get("excluida"):
            b = r["brazos"]
            print(f"seed {seed} | OFFSET N={b['OFFSET']['NORM']:.1f} S1={b['OFFSET']['S1']:.1f} "
                  f"S2={b['OFFSET']['S2']:.1f} | CONT N={b['CONTING']['NORM']:.1f} "
                  f"S1={b['CONTING']['S1']:.1f} S2={b['CONTING']['S2']:.1f} | "
                  f"INT N={b['INTERCAL']['NORM']:.1f} S1={b['INTERCAL']['S1']:.1f} "
                  f"S2={b['INTERCAL']['S2']:.1f} | ISI {r['rankin10']['pre']:.1f}->"
                  f"{r['rankin10']['post_frozen']:.1f}", flush=True)

    inc = [r for r in results if not r.get("excluida")]
    n = len(inc)

    def med(brazo, clave):
        return np.array([r["brazos"][brazo][clave] for r in inc])

    print(f"\n=== CONTROL INTERPRETACIÓN | N={n} ===")
    for brazo in ("OFFSET", "CONTING", "INTERCAL"):
        print(f"--- {brazo} ---")
        for clave in ("NORM", "S1", "S2", "S1_a0", "S1_a3"):
            arr = med(brazo, clave)
            lo, hi = ci_bootstrap(arr)
            print(f"  z_{clave:<7} media={arr.mean():.2f} CI95=[{lo:.2f},{hi:.2f}]")
    pre = np.array([r["rankin10"]["pre"] for r in inc])
    post = np.array([r["rankin10"]["post_frozen"] for r in inc])
    print("--- Rankin-10 ISI limpio (pesos congelados en el gap, brazo CONTING) ---")
    print(f"  z_S1 pre-gap={pre.mean():.2f} | post-gap (frozen)={post.mean():.2f} "
          f"| Δ={np.mean(post - pre):.2f}  (Δ≈0 → sin recuperación espontánea)")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"n_hab": args.nhab, "gap": args.gap, "results": results}, f, indent=2)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
