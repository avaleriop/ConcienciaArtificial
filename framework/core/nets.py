# Redes del núcleo v0.14 (SPEC.md §2):
#  - Predictor factorizado: encoder compartido 13->64 + cabezas f_pos (->2) y f_H (->4),
#    pérdidas separadas (preregistro 63 §1: sin L2 global mezclada).
#  - PhiCanal: (13 + one-hot canal) -> log sigma^2_c, NLL por canal.
#  - Attention: 13 -> 32 -> 7 softmax (solo para el 4-arm A/B/C/D).
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import config as C


class EncoderCompartido(nn.Module):
    def __init__(self, d_in=C.D_IN, d_enc=C.D_ENC):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_enc), nn.ReLU())

    def forward(self, x):
        return self.net(x)


class PredictorFactorizado(nn.Module):
    """World model acción-condicionado: f_pos(s,a)->(x,y); f_H(s,a)->(E,C,U,S)."""

    def __init__(self, d_in=C.D_IN, d_enc=C.D_ENC):
        super().__init__()
        self.encoder = EncoderCompartido(d_in, d_enc)
        self.f_pos = nn.Linear(d_enc, 2)
        self.f_H = nn.Linear(d_enc, 4)

    def forward(self, x):
        h = self.encoder(x)
        return self.f_pos(h), self.f_H(h)

    def predecir(self, x):
        with torch.no_grad():
            p, h = self.forward(x)
        return p, h


class PhiCanal(nn.Module):
    """Φ por canal: predice log σ²_c del error del predictor en el canal c.

    Canales de error = salidas del predictor (6): [x, y, E, C, U, S].
    Input: [entrada(s,a) (13), one-hot canal (6)] -> log σ²_c (escalar).
    NLL: 0.5·(log σ² + ε_c²/σ²).
    """

    def __init__(self, d_in=C.D_IN, n_canales=C.N_CANALES, d_h=64):
        super().__init__()
        self.n_canales = n_canales
        self.net = nn.Sequential(nn.Linear(d_in + n_canales, d_h), nn.ReLU(),
                                 nn.Linear(d_h, 1))

    def forward(self, x_base, canal_idx):
        oh = F.one_hot(torch.as_tensor(canal_idx, device=x_base.device),
                       self.n_canales).float()
        if oh.dim() == 1:
            oh = oh.unsqueeze(0)
        if oh.shape[0] != x_base.shape[0]:
            oh = oh.expand(x_base.shape[0], self.n_canales)
        return self.net(torch.cat([x_base, oh], dim=-1))

    def log_var(self, x_base, canal_idx):
        return self.forward(x_base, canal_idx)


class Attention(nn.Module):
    """Gate atencional sobre los 6 canales de error [x,y,E,C,U,S] (mismo espacio que Φ).

    Solo se usa en el 4-arm (A3). Entrena para que σ_implícito = RUIDO_BASE +
    (RUIDO_NIEBLA−RUIDO_BASE)·w prediga |ε| por canal. Su gate (w alto → desconfiar) es el
    confound a controlar contra Φ (docs `61`/`62`): puede ser gate de ACCIÓN epistémica.
    """

    def __init__(self, d_in=C.D_IN, d_h=32, n=C.N_CANALES):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, n))

    def forward(self, x):
        return torch.softmax(self.net(x), dim=-1)
