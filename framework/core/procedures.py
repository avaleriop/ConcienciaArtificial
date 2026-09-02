# Procedimientos v0.14 (preregistro 63 §3): pre-train y muestreo de transiciones.
# API compartida para bateria_rankin.py (A1) y factorizado_phi_canal.py (A3).
import numpy as np
import torch
from . import config as C
from .world import Mundo, entrada, objetivo
from .nets import PredictorFactorizado, PhiCanal, Attention


def device():
    return "mps" if torch.backends.mps.is_available() else "cpu"


def transiciones_normal(mundo, n=1200, acciones=(0, 1, 2, 3)):
    """Genera (s_antes, s_despues, a) de física normal. Pura: avanza el mundo."""
    out = []
    for _ in range(n):
        a = int(np.random.choice(acciones))
        s_a = mundo.estado()
        s_d = mundo.paso_normal(a)
        out.append((s_a, s_d, a))
    return out


def preentrenar_predictor(pred, mundo, n_trans=1200, n_steps=400, batch=64):
    dev = device()
    X, Y = [], []
    for _ in range(n_trans):
        a = int(np.random.choice((0, 1, 2, 3)))
        s_a = mundo.estado()
        s_d = mundo.paso_normal(a)
        X.append(entrada(s_a, a))
        Y.append(objetivo(s_d))
    Xt = torch.tensor(np.array(X), dtype=torch.float32, device=dev)
    Yt = torch.tensor(np.array(Y), dtype=torch.float32, device=dev)
    opt = torch.optim.Adam(pred.parameters(), lr=1e-3)
    for _ in range(n_steps):
        idx = torch.randint(0, Xt.shape[0], (batch,))
        p_pos, p_H = pred(Xt[idx])
        loss = (p_pos - Yt[idx][:, :2]).pow(2).mean() + (p_H - Yt[idx][:, 2:]).pow(2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return pred


def preentrenar_phi(phi, pred, mundo, n=500, batch=64, n_muestra=800):
    """Entrena Φ por canal con NLL: 0.5·(log σ² + ε_c²/σ²) sobre canales [x,y,E,C,U,S]."""
    dev = device()
    datos = []
    hist = []
    for _ in range(n_muestra):
        a = int(np.random.choice((0, 1, 2, 3)))
        s_a = mundo.estado()
        s_d = mundo.paso_normal(a)
        x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=dev).unsqueeze(0)
        y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=dev).unsqueeze(0)
        with torch.no_grad():
            p_pos, p_H = pred(x)
            eps2 = torch.cat([(p_pos - y[:, :2]), (p_H - y[:, 2:])], dim=-1).pow(2)  # (1,6)
        for c in range(6):
            datos.append((x, c, float(eps2[0, c])))
    opt = torch.optim.Adam(phi.parameters(), lr=1e-3)
    for _ in range(n):
        batch_idx = np.random.randint(0, len(datos), (batch,))
        loss = 0.0
        for i in batch_idx:
            x, c, eps2 = datos[i]
            log_var = phi(x, [c])
            loss = loss + 0.5 * (log_var + eps2 / (log_var.exp() + 1e-8)).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return phi


def preentrenar_attention(att, pred, mundo, n=300, batch=64):
    """Atención aprende sigma implicado por canal ≈ ε real (mismo esquema que v0.12)."""
    dev = device()
    Xp, Yp = [], []
    for _ in range(800):
        a = int(np.random.choice((0, 1, 2, 3)))
        s_a = mundo.estado()
        s_d = mundo.paso_normal(a)
        x = torch.tensor(entrada(s_a, a), dtype=torch.float32, device=dev).unsqueeze(0)
        y = torch.tensor(objetivo(s_d), dtype=torch.float32, device=dev).unsqueeze(0)
        with torch.no_grad():
            p_pos, p_H = pred(x)
            eps = ((p_pos - y[:, :2]).pow(2).mean() + (p_H - y[:, 2:]).pow(2).mean()).sqrt()
        Xp.append(entrada(s_a, a))
        Yp.append(float(eps))
    Xpt = torch.tensor(np.array(Xp), dtype=torch.float32, device=dev)
    Ypt = torch.tensor(np.array(Yp), dtype=torch.float32, device=dev).unsqueeze(1)
    opt = torch.optim.Adam(att.parameters(), lr=1e-3)
    for _ in range(n):
        idx = torch.randint(0, Xpt.shape[0], (batch,))
        aw = att(Xpt[idx])
        sigma_canal = C.RUIDO_BASE + (C.RUIDO_NIEBLA - C.RUIDO_BASE) * aw
        sigma_canal[:, 6] = C.RUIDO_BASE * 0.5
        sigma_mean = sigma_canal.mean(dim=1, keepdim=True)
        loss = (sigma_mean - Ypt[idx]).pow(2).mean()
        entropy = -(aw * torch.log(aw + 1e-8)).sum(dim=1).mean()
        opt.zero_grad()
        (loss - 0.01 * entropy).backward()
        opt.step()
    return att


def seed_todo(seed):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
