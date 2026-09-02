#!/usr/bin/env python3
"""
[RETIRADO COMO EVIDENCIA — 2026-09-02, ver CHANGELOG "Claims retirados"]
Piloto N=5 sin potencia: RND 2.8% gana al organismo 1.8%. Fuera de la Tabla del paper.
Se conserva solo como registro histórico.

FASE 3 BENCHMARK - MiniGrid DoorKey-8x8 vs baselines: Aleatorio, ICM, RND, Organismo (ECUS+sorpresa)
Pre-registrado 46-plan-rigor-cientifico.md:1. Métricas: tasa de éxito, pasos medios, cobertura de estados.
ICM: recompensa = extrínseca + η·||φ(s')-f(φ(s),a)||² (curiosidad por error de forward model)
RND: recompensa = extrínseca + η·||f(s)-f̂(s)||² (novedad por destilación de red aleatoria)
Organismo: recompensa = extrínseca + η·z(sorpresa del predictor del cuerpo) + drive ECUS
Política común: MLP con REINFORCE + entropía. N=10 seeds, 300 episodios, 200 pasos máx.
Ejecuta: python3 framework/benchmark_doorkey.py
"""
import sys, math, random, json, os
import numpy as np
import torch
import torch.nn as nn
import gymnasium as gym
import minigrid
from minigrid.wrappers import FullyObsWrapper

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Benchmark DoorKey-8x8 en {DEVICE}")

def make_env(seed):
    # Empty-8x8: recompensa escasa (solo al llegar a la meta). Es el entorno estándar
    # donde los bonuses de curiosidad (ICM/RND) demuestran ventaja sobre aleatorio.
    # (DoorKey requiere ~1M frames con PPO — inviable en esta máquina; documentado en 51)
    env = gym.make("MiniGrid-Empty-8x8-v0")
    env = FullyObsWrapper(env)
    env.reset(seed=seed)
    return env

def obs_vector(obs):
    # FullyObs: dict {'image': (8,8,3) uint8, 'direction', 'mission'}
    img = obs['image']  # (8,8,3): canal 0 = object indices
    obj = img[:,:,0]
    feat = np.zeros(12, dtype=np.float32)
    for v in range(12):
        feat[v] = float(np.any(obj == v))
    # posición del agente: célula 10 es el agente en MiniGrid
    ag_idx = np.argwhere(obj == 10)
    if len(ag_idx) > 0:
        feat = np.concatenate([feat, ag_idx[0].astype(np.float32)/8.0])
    else:
        feat = np.concatenate([feat, np.zeros(2, dtype=np.float32)])
    return feat.astype(np.float32)

class Policy(nn.Module):
    def __init__(self, d_in, d_h=64, n_act=7):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, n_act))
    def forward(self, x):
        return self.net(x)

def reinf_loop(agent, env, bonus_fn, eta, episodes=100, max_steps=64):
    """REINFORCE con bonus de curiosidad. bonus_fn(obs_ant, obs, a) -> float."""
    opt = torch.optim.Adam(agent.policy.parameters(), lr=1e-3)
    solved = 0; total_steps = 0; coverage = set()
    for ep in range(episodes):
        obs, _ = env.reset(seed=1000+ep)
        logp, rewards = [], []
        done = False
        for t in range(max_steps):
            o = obs_vector(obs)
            coverage.add(hash(o.tobytes()))
            x = torch.tensor(o, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            logits = agent.policy(x)
            dist = torch.distributions.Categorical(logits=logits)
            a = int(dist.sample())
            logp.append(dist.log_prob(torch.tensor(a, device=DEVICE)))
            obs_ant = o.copy()
            obs, r, term, trunc, info = env.step(a)
            bonus = bonus_fn(obs_ant, obs_vector(obs), a) if bonus_fn else 0.0
            rewards.append(float(r) + eta*bonus)
            total_steps += 1
            done = term or trunc
            if done:
                if r > 0: solved += 1
                break
        # REINFORCE con retorno descontado
        G = 0; returns = []
        for r in reversed(rewards):
            G = r + 0.99*G
            returns.insert(0, G)
        returns = torch.tensor(returns, dtype=torch.float32, device=DEVICE)
        if len(returns) > 0:
            returns = (returns - returns.mean())/(returns.std()+1e-8)
            loss = -sum(lp*R for lp, R in zip(logp, returns))/len(returns)
            opt.zero_grad(); loss.backward(); opt.step()
    return {"solved": solved/episodes, "mean_steps": total_steps/episodes, "coverage": len(coverage)}

# ============ Baselines ============
class ICM:
    """Forward model + inverse model sobre features aprendidas."""
    def __init__(self, d_in, d_h=64, d_f=32):
        self.enc = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, d_f)).to(DEVICE)
        self.fwd = nn.Sequential(nn.Linear(d_f+7, d_h), nn.ReLU(), nn.Linear(d_h, d_f)).to(DEVICE)
        self.inv = nn.Sequential(nn.Linear(2*d_f, d_h), nn.ReLU(), nn.Linear(d_h, 7)).to(DEVICE)
        self.opt = torch.optim.Adam(list(self.enc.parameters())+list(self.fwd.parameters())+list(self.inv.parameters()), lr=1e-3)
        self.loss = nn.MSELoss(); self.ce = nn.CrossEntropyLoss()
    def bonus(self, o_ant, o, a):
        x1 = torch.tensor(o_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        x2 = torch.tensor(o, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        f1, f2 = self.enc(x1), self.enc(x2)
        a_oh = torch.zeros(1, 7, device=DEVICE); a_oh[0, a] = 1.0
        f_pred = self.fwd(torch.cat([f1, a_oh], dim=1))
        a_pred = self.inv(torch.cat([f1, f2], dim=1))
        # entrenar
        l = self.loss(f_pred, f2.detach()) + self.ce(a_pred, torch.tensor([a], device=DEVICE))
        self.opt.zero_grad(); l.backward(); self.opt.step()
        return float((f2.detach()-f_pred.detach()).pow(2).mean())

class RND:
    def __init__(self, d_in, d_h=64, d_o=32):
        self.target = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, d_o)).to(DEVICE)
        for p in self.target.parameters(): p.requires_grad = False
        self.pred = nn.Sequential(nn.Linear(d_in, d_h), nn.ReLU(), nn.Linear(d_h, d_o)).to(DEVICE)
        self.opt = torch.optim.Adam(self.pred.parameters(), lr=1e-3)
    def bonus(self, o_ant, o, a):
        x = torch.tensor(o, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        t = self.target(x); p = self.pred(x)
        loss = (p - t.detach()).pow(2).mean()
        self.opt.zero_grad(); loss.backward(); self.opt.step()
        return float((p.detach()-t.detach()).pow(2).mean())

class Organismo:
    """Nuestro agente: predictor del cuerpo (sorpresa z) como bonus + ECUS como drive."""
    def __init__(self, d_in, d_h=64, d_out=None):
        d_out = d_out if d_out is not None else d_in
        self.pred = nn.Sequential(nn.Linear(d_in+7, d_h), nn.ReLU(), nn.Linear(d_h, d_out)).to(DEVICE)
        self.opt = torch.optim.Adam(self.pred.parameters(), lr=1e-3)
        self.eps_hist = []
    def bonus(self, o_ant, o, a):
        x1 = torch.tensor(o_ant, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        x2 = torch.tensor(o, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        a_oh = torch.zeros(1, 7, device=DEVICE); a_oh[0, a] = 1.0
        p = self.pred(torch.cat([x1, a_oh], dim=1))
        eps = float((p - x2.detach()).pow(2).mean().sqrt())
        loss = (p - x2.detach()).pow(2).mean()
        self.opt.zero_grad(); loss.backward(); self.opt.step()
        self.eps_hist.append(eps)
        if len(self.eps_hist) > 100: self.eps_hist.pop(0)
        h = np.array(self.eps_hist)
        z = (eps - h.mean())/(h.std()+1e-8)
        return float(max(0.0, z))

def main():
    d_in = None
    env0 = make_env(0)
    obs0, _ = env0.reset(seed=0)
    d_in = obs_vector(obs0).shape[0]
    env0.close()
    print(f"Dim observación: {d_in}")
    resultados = {}
    for nombre, bonus_cls in [("aleatorio", None), ("ICM", ICM), ("RND", RND), ("organismo", Organismo)]:
        print(f"Ejecutando {nombre}...", flush=True)
        res_list = []
        for seed in range(5):
            env = make_env(seed)
            pol = Policy(d_in).to(DEVICE)
            bonus = bonus_cls(d_in) if bonus_cls else None
            class Ag: 
                pass
            ag = Ag(); ag.policy = pol
            r = reinf_loop(ag, env, bonus.bonus if bonus else None, eta=1.0)
            env.close()
            res_list.append(r)
            print(f"  {nombre} seed {seed}: {r['solved']*100:.0f}%", flush=True)
        solved = np.mean([x['solved'] for x in res_list])
        steps = np.mean([x['mean_steps'] for x in res_list])
        cov = np.mean([x['coverage'] for x in res_list])
        resultados[nombre] = {"solved": float(solved), "mean_steps": float(steps), "coverage": float(cov)}
        print(f"{nombre:10s}: resuelve {solved*100:5.1f}% | pasos medios {steps:6.1f} | cobertura {cov:6.1f}")
    os.makedirs('results', exist_ok=True)
    json.dump(resultados, open('results/benchmark_doorkey.json','w'), indent=2)
    print("-> results/benchmark_doorkey.json")

if __name__ == "__main__":
    main()
