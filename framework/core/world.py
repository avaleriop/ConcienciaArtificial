# Mundo continuo 20x20 con niebla (x>14). Física transcrita de organismo_final.py
# v0.12 (los números v0.13 salieron de este mundo), extendida con las violaciones
# S1-S5 del preregistro 63. Violaciones = mutación PURA del estado (sin física extra).
import math
import numpy as np
from . import config as C


def fisica(pos, a):
    """Un paso de física continua. `a` es vector 7-D (one-hot de la acción)."""
    x = pos[0] + a[0] * 0.8
    y = pos[1] + a[1] * 0.8
    x *= 0.95
    y *= 0.95
    x = max(0.0, min(C.WORLD_SIZE, x))
    y = max(0.0, min(C.WORLD_SIZE, y))
    return [x, y], x > C.NIEBLA_X


def ruido_canal(ch, niebla):
    base = C.RUIDO_BASE
    if niebla and ch in (0, 1, 2, 3, 4):
        base = C.RUIDO_NIEBLA
    if ch == 6:
        base = C.RUIDO_BASE * 0.5
    return np.random.randn() * base


class Mundo:
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.pos = [C.WORLD_SIZE / 2, C.WORLD_SIZE / 2]
        self.H = np.array(C.H_INIT, dtype=np.float32)
        self.foods = C.FOODS
        self.social = C.SOCIAL
        self.historial_estados = []

    def en_niebla(self):
        return self.pos[0] > C.NIEBLA_X

    def estado(self):
        return np.array([self.pos[0], self.pos[1], self.H[0], self.H[1], self.H[2], self.H[3]],
                        dtype=np.float32)

    def _registrar(self):
        self.historial_estados.append(self.estado().copy())
        if len(self.historial_estados) > 200:
            self.historial_estados.pop(0)

    def teleport(self, dx, dy):
        self.pos = [max(0.0, min(C.WORLD_SIZE, self.pos[0] + dx)),
                    max(0.0, min(C.WORLD_SIZE, self.pos[1] + dy))]

    def paso_normal(self, a_idx):
        """Paso de física normal con la acción a_idx. Devuelve s'."""
        a = np.zeros(7, dtype=np.float32)
        a[a_idx] = 1.0
        self._registrar()
        np_pos, niebla = fisica(self.pos, a)
        dH = -0.02 * (self.H - np.array(C.H_CANON, dtype=np.float32))
        if niebla:
            dH[0] -= 0.03
            dH[2] += 0.01
        else:
            dH[2] -= 0.01
        en_comida = any(math.hypot(self.pos[0] - fx, self.pos[1] - fy) < 0.5
                        for fx, fy in self.foods)
        if en_comida:
            dH[0] += 0.2
        for ch in range(7):
            r = ruido_canal(ch, niebla)
            if ch < 4:
                dH[ch] += r * 0.1
        if math.hypot(self.pos[0] - self.social[0], self.pos[1] - self.social[1]) < 0.5:
            dH[3] += 0.1
        self.H = np.clip(self.H + dH, 0, 1.5)
        self.pos = np_pos
        return self.estado()

    def aplicar_violacion(self, spec):
        """Violación programada (S1-S5): mutación pura, devuelve s' sin física normal."""
        self._registrar()
        dx, dy = spec.get("teleport", (0.0, 0.0))
        if dx or dy:
            self.teleport(dx, dy)
        if spec.get("invertir_comida"):
            en_comida = any(math.hypot(self.pos[0] - fx, self.pos[1] - fy) < 0.5
                            for fx, fy in self.foods)
            if en_comida:
                self.H[0] = np.clip(self.H[0] - 0.4, 0, 1.5)
        return self.estado()


VIOLACIONES = {
    "S1": {"teleport": (2.0, 2.0), "invertir_comida": False},   # motor habitual (+2,+2)
    "S2": {"teleport": (-2.0, -2.0), "invertir_comida": False},  # misma mag, dirección opuesta
    "S3": {"teleport": (2.0, -2.0), "invertir_comida": False},   # ortogonal
    "S4": {"teleport": (4.0, 4.0), "invertir_comida": False},    # doble magnitud
    "S5": {"teleport": (0.0, 0.0), "invertir_comida": True},     # interoceptiva (comer baja E)
    "NORM": {"teleport": (0.0, 0.0), "invertir_comida": False},  # física normal
}


def entrada(estado, a):
    if isinstance(a, int):
        a_oh = np.zeros(7, dtype=np.float32)
        a_oh[a] = 1.0
    else:
        a_oh = np.float32(a)
    x, y = float(estado[0]), float(estado[1])
    H_norm = np.array([float(estado[i]) / 1.5 for i in range(2, 6)], dtype=np.float32)
    return np.concatenate([np.array([x / C.WORLD_SIZE, y / C.WORLD_SIZE], dtype=np.float32),
                           H_norm, a_oh], dtype=np.float32)


def objetivo(estado_despues):
    """Target del predictor: [pos/W, H/1.5], 6-D (x,y,E,C,U,S normalizados)."""
    return np.concatenate([np.array(estado_despues[:2], dtype=np.float32) / C.WORLD_SIZE,
                           np.array(estado_despues[2:], dtype=np.float32) / 1.5])
