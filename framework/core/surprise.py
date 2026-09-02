# Sorpresa con baseline congelada (SPEC.md §2, regla del plan 64-A1):
#  μ, σ se estiman en una fase de calibración SIN eventos y se CONGELAN;
#  prohibido actualizar σ durante o después del evento.
import numpy as np
import torch
from .world import entrada, objetivo


def error_por_cabeza(pred, s_antes, s_despues, a):
    """Errores del predictor factorizado sobre una transición (s,a)->s'.

    Devuelve: eps_pos (head x,y), eps_H (head E,C,U,S), eps_total (MSE global),
    y eps_canal: vector 6-D [x,y,E,C,U,S] de error por componente (L2 de cada dim).
    """
    dev = next(pred.parameters()).device
    x = torch.tensor(entrada(s_antes, a), dtype=torch.float32, device=dev).unsqueeze(0)
    y = torch.tensor(objetivo(s_despues), dtype=torch.float32, device=dev).unsqueeze(0)
    with torch.no_grad():
        p_pos, p_H = pred(x)
        d_pos = (p_pos - y[:, :2]).pow(2).mean().sqrt().item()
        d_H = (p_H - y[:, 2:]).pow(2).mean().sqrt().item()
        d_tot = np.sqrt((d_pos ** 2 + d_H ** 2) / 2.0)
        canal = torch.cat([(p_pos - y[:, :2]), (p_H - y[:, 2:])], dim=-1).pow(2).mean(dim=0).sqrt().cpu().numpy()
    return {"pos": d_pos, "H": d_H, "total": d_tot, "canal": canal}


class BaselineCongelada:
    """μ, σ por métrica (pos/H/total/canal), estimados sin eventos y congelados."""

    def __init__(self, pred, transiciones_normal):
        """transiciones_normal: iterable de (s_antes, s_despues, a) de física normal."""
        muestras = {"pos": [], "H": [], "total": [], "canal": []}
        for s_a, s_d, a in transiciones_normal:
            e = error_por_cabeza(pred, s_a, s_d, a)
            for k in ("pos", "H", "total"):
                muestras[k].append(e[k])
            muestras["canal"].append(e["canal"])
        self.mu = {}
        self.sigma = {}
        for k in ("pos", "H", "total"):
            arr = np.array(muestras[k])
            self.mu[k] = float(arr.mean())
            self.sigma[k] = float(arr.std()) + 1e-8
        canal_arr = np.array(muestras["canal"])  # (n, 6)
        self.mu["canal"] = canal_arr.mean(axis=0)
        self.sigma["canal"] = canal_arr.std(axis=0) + 1e-8
        self.n = len(muestras["total"])

    def z(self, eps):
        """z congelado: (ε − μ_cal)/σ_cal. eps es dict de error_por_cabeza."""
        out = {}
        for k in ("pos", "H", "total"):
            out[k] = (eps[k] - self.mu[k]) / self.sigma[k]
        out["canal"] = (eps["canal"] - self.mu["canal"]) / self.sigma["canal"]
        return out
