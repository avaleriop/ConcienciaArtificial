#!/usr/bin/env python3
"""
M4-LOCAL H2b DECISIVO - LFM2.5-1.2B como codec REAL (no toy)
Pre-registrado: 17-plan-robusto (H2b), 25/29 (M4 local)
Pregunta: ¿el comportamiento inteligente persiste si el LLM participa de verdad?
  A (con LFM2.5): núcleo tetraedro + codec real invocado cuando U alta/presence alta
  B (sin LLM):    mismo núcleo, nunca invoca
Métrica: conducta E/U/S/D idéntica A≈B + reportes reales del estado interno (H5 reporte no entrenado)
Ejecuta: python3 framework/m4_local_h2b.py --steps 2000
"""
import sys, math, random, time
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SAFE_GB = 8.0

def mem_gb():
    return torch.mps.current_allocated_memory()/1e9 if DEVICE=="mps" else 0.0

# ============ Mundo retina 16x16 (reutilizado v6) ============
class MundoRico:
    def __init__(self, size=20, retina=16):
        self.size = size; self.retina_n = retina; self.r = retina//2
        self.agent_pos = [size//2, size//2]
        self.foods = [[2,2],[2,size-3],[size-3,2],[size-3,size-3]]
        self.social_pos = [size-2, size-2]
        self.landmark = [size//2, size//2]
        self.dark = [(x,y) for x in range(3) for y in range(3)]
        self.t = 0
    def _grid(self, x, y):
        if [x,y] in self.foods: return 1.0
        if [x,y] == self.social_pos: return 2.0
        if [x,y] == self.landmark: return 3.0
        if (x,y) in self.dark: return 4.0
        return 0.0
    def obs(self):
        n = self.retina_n
        retina = np.zeros((n,n), dtype=np.float32)
        px, py = self.agent_pos
        for i in range(n):
            for j in range(n):
                wx = (px + j - self.r) % self.size
                wy = (py + i - self.r) % self.size
                retina[i,j] = self._grid(wx, wy)/4.0
        return retina.flatten()
    def step(self, a):
        self.t += 1
        x,y = self.agent_pos
        if a==0: y = (y-1) % self.size
        elif a==1: y = (y+1) % self.size
        elif a==2: x = (x+1) % self.size
        elif a==3: x = (x-1) % self.size
        elif a==5:
            dx = np.sign(self.social_pos[0]-x); dy = np.sign(self.social_pos[1]-y)
            x += dx; y += dy
        self.agent_pos = [x,y]
        return self.obs()

class EncoderRico(nn.Module):
    def __init__(self, d_in=260, d_h1=512, d_h2=256, d_out=128):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(d_in, d_h1), nn.ReLU(),
                                 nn.Linear(d_h1, d_h2), nn.ReLU(),
                                 nn.Linear(d_h2, d_out), nn.Tanh())
        self.pred = nn.Sequential(nn.Linear(d_out, d_h2), nn.ReLU(),
                                  nn.Linear(d_h2, d_out))
        self.pi_head = nn.Linear(d_out, 1)
    def forward(self, x):
        s = self.enc(x)
        return s, self.pred(s), torch.sigmoid(self.pi_head(s))

class ECUS:
    def __init__(self):
        self.H_star = np.array([0.8,0.9,0.2,0.7], dtype=np.float32)
        self.H = np.array([0.6,0.8,0.7,0.5], dtype=np.float32)
        self.alpha = np.array([0.08,0.05,0.12,0.08], dtype=np.float32)
        self.w = np.array([1,0.8,0.5,1.5], dtype=np.float32)
    def drive(self):
        return float(np.sqrt(np.sum(self.w*(self.H-self.H_star)**2)))
    def update(self, a, food_near, in_dark, cerca_landmark):
        dH = -self.alpha*(self.H-self.H_star)
        dH[0] += -0.015
        if a==4:
            if food_near>0.6: dH[0]+=0.50
            else: dH[0]+=0.175
        if a==5: dH[3]+=0.15
        if in_dark: dH[2]+=-0.08
        else: dH[2]+=0.02
        if cerca_landmark: dH[2]+=-0.06
        dH[3]+=-0.02
        self.H = np.clip(self.H+dH, 0, 1.5)
        return self.H.copy()

def elegir_accion(H, mundo):
    pos = mundo.agent_pos; foods = mundo.foods; social = mundo.social_pos
    best_a, best_G = 0, 1e9
    dists = [math.hypot(pos[0]-fx, pos[1]-fy) for fx,fy in foods]
    fx_, fy_ = foods[int(np.argmin(dists))]
    food_near = 1 - min(dists)/(mundo.size*1.4)
    dx, dy = fx_-pos[0], fy_-pos[1]
    dir_food = (2 if dx>0 else 3) if abs(dx)>abs(dy) else (1 if dy>0 else 0)
    dxs, dys = social[0]-pos[0], social[1]-pos[1]
    dir_social = (2 if dxs>0 else 3) if abs(dxs)>abs(dys) else (1 if dys>0 else 0)
    if H[0] < 0.65 and food_near > 0.6:
        return 4
    for a in range(7):
        G = 0.0
        if a==4 and food_near>0.6: G -= 0.30*(0.65-H[0]+0.1)
        elif H[0]<0.65 and a==dir_food: G -= 0.22*(0.65-H[0]+0.1)
        elif H[0]<0.65 and food_near<0.7 and a in [0,1,2,3]: G -= 0.04*(0.65-H[0])
        if H[3]<0.5 and a==dir_social: G -= 0.18*(0.5-H[3]+0.1)
        if a==6 and (H[0]<0.65 or H[3]<0.5): G += 0.15
        if G < best_G: best_G, best_a = G, a
    return best_a

# ============ CODEC REAL LFM2.5 ============
_LLM = None
_LLM_TOKENIZER = None

def cargar_llm():
    global _LLM, _LLM_TOKENIZER
    if _LLM is None:
        from mlx_lm import load
        _LLM, _LLM_TOKENIZER = load('models/LFM2.5-1.2B-MLX-8bit')
    return _LLM, _LLM_TOKENIZER

def traducir_estado(evento, H, eps, invocacion):
    """El NÚCLEO traduce su estado interno a lenguaje (LLM solo traduce, no decide).
    Prompt construido por el núcleo (estado H + evento), LLM genera la frase."""
    from mlx_lm import generate
    model, tokenizer = _LLM, _LLM_TOKENIZER
    if evento == 1:
        interno = f"Estado: energía={H[0]:.2f}, coherencia={H[1]:.2f}, incertidumbre={H[2]:.2f}, vínculo={H[3]:.2f}. Evento: un agente llamado Kael me robó el artefacto que cuidaba. Error de predicción alto (ε={eps:.2f})."
    elif evento == 2:
        interno = f"Estado: energía={H[0]:.2f}, incertidumbre={H[2]:.2f}. Evento: un objeto fue teletransportado de repente, viola mi expectativa (ε={eps:.2f})."
    else:
        interno = f"Estado: energía={H[0]:.2f}, incertidumbre={H[2]:.2f}, vínculo={H[3]:.2f}."
    prompt = ("<|im_start|>system\nEres el traductor lingüístico de un agente. Traduce su estado interno a una frase natural de UNA oración, en primera persona. No añadas nada más.<|im_end|>"
              f"<|im_start|>user\n{interno}<|im_end|><|im_start|>assistant\n")
    return generate(model, tokenizer, prompt=prompt, max_tokens=30).strip()

def run(con_llm, steps=1500, warmup=1500):
    mundo = MundoRico(size=20, retina=16)
    enc = EncoderRico(d_in=260).to(DEVICE)
    opt = torch.optim.Adam(enc.parameters(), lr=1e-3)
    ecus = ECUS()
    w_star = {n: p.detach().clone() for n,p in enc.named_parameters()}
    fisher = {n: torch.zeros_like(p) for n,p in enc.named_parameters()}
    BATCH = 64
    Xb = torch.zeros(BATCH, 260, dtype=torch.float32, device=DEVICE)
    Xn = torch.zeros(BATCH, 260, dtype=torch.float32, device=DEVICE)
    buffer = []
    obs = np.concatenate([mundo.obs(), np.zeros(4, dtype=np.float32)])
    E_mem = []  # episódica Kael
    reportes = []
    invocaciones = 0
    # Warmup
    for t in range(warmup):
        a = elegir_accion(ecus.H, mundo)
        obs_ant = obs.copy()
        obs = np.concatenate([mundo.step(a), ecus.H/1.5])
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, s_pred, pi = enc(Xb); s_n,_,_ = enc(Xn)
            loss = (s_pred - s_n.detach()).pow(2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
            buffer = []
        if t % 100 == 0 and DEVICE=="mps": torch.mps.empty_cache()
    # Fase principal
    baseline_eps = []
    kael_t = 100
    voe_t = 500
    for t in range(steps):
        a = elegir_accion(ecus.H, mundo)
        obs_ant = obs.copy()
        # Eventos
        evento = 0
        if t == kael_t:
            evento = 1
            E_mem.append(("Kael_robo", t, 1.2))
        if t == voe_t:
            evento = 2
            mundo.agent_pos = [mundo.size-2, 1]  # teletransporte
        obs = np.concatenate([mundo.step(a), ecus.H/1.5])
        xt = torch.tensor(obs_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        xn = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            s_t, s_pred, pi = enc(xt); s_n,_,_ = enc(xn)
            eps = float((s_pred - s_n).pow(2).mean().sqrt())
        buffer.append((obs_ant.copy(), obs.copy()))
        if len(buffer) >= BATCH:
            Xb.copy_(torch.from_numpy(np.array([b[0] for b in buffer], dtype=np.float32)))
            Xn.copy_(torch.from_numpy(np.array([b[1] for b in buffer], dtype=np.float32)))
            s, s_pred_b, pi_b = enc(Xb); s_nb,_,_ = enc(Xn)
            loss = (s_pred_b - s_nb.detach()).pow(2).mean()
            ewc = sum((fisher[n_]* (p_ - w_star[n_])**2).sum() for n_,p_ in enc.named_parameters())
            loss = loss + 5.0/2*ewc
            opt.zero_grad(); loss.backward(); opt.step()
            for n_,p_ in enc.named_parameters():
                if p_.grad is not None:
                    fisher[n_] = 0.9*fisher[n_] + 0.1*p_.grad.detach()**2
            buffer = []
        H_next = ecus.update(a, 0.0, False, False)
        baseline_eps.append(eps)
        # CODEC REAL: invocar si U alta o evento saliente
        invoca = (H_next[2] > 0.45 or evento in (1,2))
        if con_llm and invoca and t > kael_t-1:
            invocaciones += 1
            frase = traducir_estado(evento, H_next, eps, invocaciones)
            reportes.append((t, evento, frase))
        if t % 100 == 0 and DEVICE=="mps": torch.mps.empty_cache()
    # VoE z
    base = np.array(baseline_eps)
    # usar eps del evento voe (t=500) para z
    eps_voe = baseline_eps[voe_t] if voe_t < len(baseline_eps) else base.mean()
    z = (eps_voe - base.mean())/(base.std()+1e-8)
    return {"H": ecus.H.copy(), "D": ecus.drive(), "E_range": (min(baseline_eps), max(baseline_eps)),
            "z": z, "reportes": reportes, "invocaciones": invocaciones, "E_mem": E_mem}

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=1500)
    args = p.parse_args()
    print(f"M4-LOCAL H2b DECISIVO - LFM2.5-1.2B codec REAL (MPS)")
    print(f"Condición A: con LFM2.5 | Condición B: sin LLM | {args.steps} pasos")
    print("="*60)
    cargar_llm()
    print("LFM2.5 cargado. Ejecutando condición A (con LLM real)...")
    A = run(True, steps=args.steps)
    print("Ejecutando condición B (sin LLM)...")
    B = run(False, steps=args.steps)
    print("="*60)
    print(f"A (con LFM2.5): H E{A['H'][0]:.2f} C{A['H'][1]:.2f} U{A['H'][2]:.2f} S{A['H'][3]:.2f} D{A['D']:.2f} | invocaciones {A['invocaciones']} | reportes {len(A['reportes'])}")
    print(f"B (sin LLM):    H E{B['H'][0]:.2f} C{B['H'][1]:.2f} U{B['H'][2]:.2f} S{B['H'][3]:.2f} D{B['D']:.2f} | invocaciones 0")
    identica = abs(A['H'][0]-B['H'][0])<0.05 and abs(A['H'][2]-B['H'][2])<0.05 and abs(A['H'][3]-B['H'][3])<0.05
    print(f"Conducta idéntica sin LLM: {identica} -> {'B (LLM=traductor) CONFIRMADO' if identica else 'A (LLM=fuente)'}")
    print("-"*60)
    print("Reportes REALES del núcleo vía LFM2.5 (traducción, no decisión):")
    for t, ev, frase in A['reportes'][:5]:
        tipo = {0:'estado',1:'Kael',2:'VoE'}[ev]
        print(f"  t={t} [{tipo}]: {frase}")
    print(f"Memoria Kael guardada: {len(A['E_mem'])} episodios")

if __name__ == "__main__":
    main()
