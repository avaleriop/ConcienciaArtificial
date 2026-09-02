# EWC (Fisher diagonal) sobre el predictor factorizado.
# En v0.14: solo se usa en A4 (tarea distinta), NO en la batería Rankin (λ=0, SPEC §4).
import torch
from .nets import PredictorFactorizado


class EWC:
    """w_star + Fisher diagonal por parámetro, con pérdida λ/2·Σ F_i(θ−θ*)²."""

    def __init__(self, model, lam=5.0):
        self.lam = lam
        self.model = model
        self.w_star = {n: p.detach().clone() for n, p in model.named_parameters()}
        self.fisher = {n: torch.zeros_like(p) for n, p in model.named_parameters()}

    def actualizar_fisher(self, grad_sq):
        """grad_sq: dict nombre -> grad² acumulado (llamar tras cada backward)."""
        for n, g in grad_sq.items():
            if n in self.fisher:
                self.fisher[n] = 0.9 * self.fisher[n] + 0.1 * g

    def snapshot(self):
        self.w_star = {n: p.detach().clone() for n, p in self.model.named_parameters()}

    def termino(self):
        loss = 0.0
        for n, p in self.model.named_parameters():
            if n in self.fisher and n in self.w_star:
                loss = loss + (self.fisher[n] * (p - self.w_star[n]).pow(2)).sum()
        return (self.lam / 2.0) * loss
