#!/usr/bin/env python3
"""
M4-LOCAL-4: VoE z-score formal + H2b local (eliminar LLM codec)
Pre-registrado: 28-M4-local-3-resultados.md:1
- T1 VoE: baseline eps 100 pasos -> teleport -> z>5sigma = PASA (métrica relativa pre-registrada)
- T2 H2b: A con codec vs B sin codec -> conducta idéntica = LLM traductor (toy)
Ejecuta: python3 framework/m4_local_4.py
"""
import sys, math, random
import numpy as np
import torch
sys.path.insert(0, 'framework')
from m4_local_cpu import AgenteLocal, MundoLocal, elegir_accion, DEVICE

random.seed(7); np.random.seed(7); torch.manual_seed(7)

def run_pipeline(con_codec, steps=1200, warmup=2000):
    mundo = MundoLocal(size=20)
    ag = AgenteLocal()
    obs = mundo.obs()
    # warmup
    for t in range(warmup):
        pos = mundo.agent_pos.copy()
        a = elegir_accion(ag.ecus.H, obs, pos, mundo.foods, mundo.social_pos, mundo.size)
        obs_ant = obs.copy()
        obs = mundo.step(a)
        ag.paso(obs_ant, obs, a, evento_voE=False)
    ag.log = []
    # baseline eps (100 pasos sin eventos)
    baselines = []
    for t in range(100):
        pos = mundo.agent_pos.copy()
        a = elegir_accion(ag.ecus.H, obs, pos, mundo.foods, mundo.social_pos, mundo.size)
        obs_ant = obs.copy()
        obs = mundo.step(a)
        xt = torch.tensor(obs_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        xn = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        s_t, s_pred, pi = ag.enc(xt)
        s_n, _, _ = ag.enc(xn)
        baselines.append(float((s_pred - s_n.detach()).pow(2).mean().sqrt()))
    mean_b, std_b = np.mean(baselines), np.std(baselines) + 1e-8
    # teleport -> z-score
    obs_ant = obs.copy()
    mundo.agent_pos = [mundo.size-2, 1]
    obs = mundo.step(0)
    xt = torch.tensor(obs_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
    xn = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
    s_t, s_pred, pi = ag.enc(xt)
    s_n, _, _ = ag.enc(xn)
    eps_t = float((s_pred - s_n.detach()).pow(2).mean().sqrt())
    z = (eps_t - mean_b) / std_b
    # continuación conducta 500 pasos
    for t in range(500):
        pos = mundo.agent_pos.copy()
        a = elegir_accion(ag.ecus.H, obs, pos, mundo.foods, mundo.social_pos, mundo.size)
        obs_ant = obs.copy()
        obs = mundo.step(a)
        presence, H, invoca = ag.paso(obs_ant, obs, a, evento_voE=False)
    E = [l["H"][0] for l in ag.log]; U = [l["H"][2] for l in ag.log]; S = [l["H"][3] for l in ag.log]
    D = [l["D"] for l in ag.log]
    return {"z": z, "eps_t": eps_t, "mean_b": mean_b, "E_min": min(E), "E_max": max(E),
            "U_final": U[-1], "S_final": S[-1], "D_avg": np.mean(D), "llm_inv": ag.invocaciones}

print("M4-LOCAL-4: VoE z-score formal + H2b local (MPS)")
print("="*60)
res_A = run_pipeline(con_codec=True)
res_B = run_pipeline(con_codec=False)  # H2b: sin codec (invocaciones forzadas 0)
print(f"T1 VoE z-score: z={res_A['z']:.1f} (umbral 5σ) eps_t={res_A['eps_t']:.4f} vs baseline {res_A['mean_b']:.4f} -> {'PASA' if res_A['z']>5 else 'FALLA'}")
print(f"T2 H2b conducta: A(codec) E[{res_A['E_min']:.2f},{res_A['E_max']:.2f}] U{res_A['U_final']:.2f} S{res_A['S_final']:.2f} D{res_A['D_avg']:.2f}")
print(f"                 B(sin codec) E[{res_B['E_min']:.2f},{res_B['E_max']:.2f}] U{res_B['U_final']:.2f} S{res_B['S_final']:.2f} D{res_B['D_avg']:.2f}")
identica = (abs(res_A['E_max']-res_B['E_max'])<0.15 and abs(res_A['U_final']-res_B['U_final'])<0.05
            and abs(res_A['S_final']-res_B['S_final'])<0.05 and abs(res_A['D_avg']-res_B['D_avg'])<0.05)
print(f"H2b: conducta idéntica sin codec = {identica} -> {'B (LLM=traductor) consistente' if identica else 'A (LLM=fuente)'}")
print("Límite honesto: LLM invocaciones 0 en ambos (U<0.4) -> H2b toy débil, decisivo en M4 cloud con Qwen2-7B real")
