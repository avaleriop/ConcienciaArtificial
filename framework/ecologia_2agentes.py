#!/usr/bin/env python3
"""
Ecología mínima 2 agentes v0.13 — Mundo joint, percepción mutua, correlación de Φ
"""
import math, random, json, argparse
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
WORLD_SIZE=20.0; NIEBLA_X=14.0
FOODS=[(3.0,3.0),(3.0,16.0),(10.0,3.0),(10.0,16.0)]
SOCIAL=(18.0,18.0)
RUIDO_BASE=0.15; RUIDO_NIEBLA=0.60

class Predictor(nn.Module):
    def __init__(self,d_in=15): super().__init__(); self.net=nn.Sequential(nn.Linear(d_in,64),nn.ReLU(),nn.Linear(64,6))
    def forward(self,x): return self.net(x)
class Phi(nn.Module):
    def __init__(self): super().__init__(); self.net=nn.Sequential(nn.Linear(17,64),nn.ReLU(),nn.Linear(64,1))
    def forward(self,x): return torch.abs(self.net(x))

def entrada(estado, other_pos, a):
    if isinstance(a,int):
        a_oh=np.zeros(7,dtype=np.float32); a_oh[a]=1.0
    else: a_oh=np.float32(a)
    x,y=float(estado[0]),float(estado[1])
    ox,oy=float(other_pos[0]),float(other_pos[1])
    H_norm=np.array([float(estado[i])/1.5 for i in range(2,6)],dtype=np.float32)
    visual=np.array([x/WORLD_SIZE,y/WORLD_SIZE,ox/WORLD_SIZE,oy/WORLD_SIZE],dtype=np.float32)
    return np.concatenate([visual,H_norm,a_oh],dtype=np.float32)

def entrada_phi(estado, other_pos, a, em, es):
    base=entrada(estado,other_pos,a)
    return np.concatenate([base, np.array([em,es],dtype=np.float32)])

def fisica(pos,a):
    x,y=pos[0]+a[0]*0.8,pos[1]+a[1]*0.8
    x*=0.95; y*=0.95; x=max(0.0,min(WORLD_SIZE,x)); y=max(0.0,min(WORLD_SIZE,y))
    return [x,y], x>NIEBLA_X

def ruido(ch,niebla):
    b=RUIDO_BASE
    if niebla and ch in (0,1,2,3,4): b=RUIDO_NIEBLA
    if ch==6: b=RUIDO_BASE*0.5
    return np.random.randn()*b

class Agent:
    def __init__(self, h_star, pos, other_pos):
        self.pos=list(pos); self.H=np.array([0.6,0.8,0.7,0.5],dtype=np.float32)
        self.h_star=np.array(h_star,dtype=np.float32)
        self.other_pos=list(other_pos)
        self.foods=FOODS; self.social=SOCIAL
        self.pred=Predictor(d_in=15).to(DEVICE)
        self.phi=Phi().to(DEVICE)
        self.eps_hist=[]
    def estado(self): return np.array([self.pos[0],self.pos[1],self.H[0],self.H[1],self.H[2],self.H[3]],dtype=np.float32)
    def en_niebla(self): return self.pos[0]>NIEBLA_X
    def step(self, a_idx):
        a=np.zeros(7,dtype=np.float32); a[a_idx]=1.0
        H=self.H
        if H[0]<0.55:
            dists=[math.hypot(self.pos[0]-fx,self.pos[1]-fy) for fx,fy in self.foods]
            idx=int(np.argmin(dists)); fx,fy=self.foods[idx]
            ag=np.zeros(7,dtype=np.float32); dx,dy=fx-self.pos[0],fy-self.pos[1]; n=math.hypot(dx,dy)+1e-6; ag[0]=dx/n; ag[1]=dy/n; a=ag
        elif H[3]>0.8:
            dx,dy=self.social[0]-self.pos[0],self.social[1]-self.pos[1]; n=math.hypot(dx,dy)+1e-6; ag=np.zeros(7,dtype=np.float32); ag[0]=dx/n; ag[1]=dy/n; a=ag
        np_pos, niebla = fisica(self.pos,a)
        dH=-0.02*(self.H-self.h_star)
        if niebla: dH[0]-=0.03; dH[2]+=0.01
        else: dH[2]-=0.01
        if any(math.hypot(self.pos[0]-fx,self.pos[1]-fy)<0.5 for fx,fy in self.foods): dH[0]+=0.2
        for ch in range(7):
            r=ruido(ch,niebla)
            if ch<4: dH[ch]+=r*0.1
        if math.hypot(self.pos[0]-self.social[0],self.pos[1]-self.social[1])<0.5: dH[3]+=0.1
        self.H=np.clip(self.H+dH,0,1.5); self.pos=np_pos
        return self.estado()

def entrenar_agente(ag, steps=400):
    opt=torch.optim.Adam(ag.pred.parameters(), lr=1e-3)
    other=[10.0,10.0]
    for _ in range(steps):
        a=random.randrange(7)
        sa=ag.estado(); sd=ag.step(a_idx=a)
        ag.other_pos=[sd[0],sd[1]] if random.random()<0.5 else other
        x=torch.tensor(entrada(sa,other,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(ag.pos)/WORLD_SIZE, ag.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        loss=(ag.pred(x)-y).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    # phi training
    opt2=torch.optim.Adam(ag.phi.parameters(), lr=1e-3)
    hist=[]
    for _ in range(600):
        a=random.randrange(7); sa=ag.estado(); sd=ag.step(a_idx=a)
        x=torch.tensor(entrada(sa,other,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(ag.pos)/WORLD_SIZE, ag.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        with torch.no_grad(): eps=float((ag.pred(x)-y).pow(2).mean().sqrt())
        hist.append(eps)
        if len(hist)>50: hist.pop(0)
        h=np.array(hist)
        xp=torch.tensor(entrada_phi(sa,other,a,float(h.mean()),float(h.std())),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        loss=(ag.phi(xp)-torch.tensor([[eps]],dtype=torch.float32,device=DEVICE)).pow(2).mean()
        opt2.zero_grad(); loss.backward(); opt2.step()
    ag.eps_hist=hist
    return opt

def run_joint(seed, steps=30000):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    h_star=[0.8,0.9,0.2,0.7]
    a1=Agent(h_star, [8,8], [12,12]); a2=Agent(h_star, [12,12], [8,8])
    entrenar_agente(a1, steps=300); entrenar_agente(a2, steps=300)
    sig1=[]; sig2=[]; e1=[]; e2=[]
    for t in range(steps):
        s1=a1.estado(); s2=a2.estado()
        a1.other_pos=list(a2.pos); a2.other_pos=list(a1.pos)
        # phi sigma
        with torch.no_grad():
            h=np.array(a1.eps_hist) if len(a1.eps_hist)>10 else np.array([0.1,0.05])
            xp1=torch.tensor(entrada_phi(s1,a1.other_pos,4,float(h.mean()),float(h.std())),dtype=torch.float32,device=DEVICE).unsqueeze(0)
            sigma1=float(a1.phi(xp1))
            h2=np.array(a2.eps_hist) if len(a2.eps_hist)>10 else np.array([0.1,0.05])
            xp2=torch.tensor(entrada_phi(s2,a2.other_pos,4,float(h2.mean()),float(h2.std())),dtype=torch.float32,device=DEVICE).unsqueeze(0)
            sigma2=float(a2.phi(xp2))
        sig1.append(sigma1); sig2.append(sigma2); e1.append(float(a1.H[0])); e2.append(float(a2.H[0]))
        # policy random for ECO test
        for ag in [a1,a2]:
            if ag.H[0]<0.55: aa=4
            elif ag.H[3]>0.8: aa=5
            else: aa=random.randrange(4)
            ag.step(a_idx=aa)
        dist12=math.hypot(a1.pos[0]-a2.pos[0], a1.pos[1]-a2.pos[1])
        if dist12<2.0:
            a1.H[3]=min(1.5, a1.H[3]+0.02); a2.H[3]=min(1.5, a2.H[3]+0.02)
        for ag,other in [(a1,a2),(a2,a1)]:
            if any(math.hypot(ag.pos[0]-fx,ag.pos[1]-fy)<0.5 for fx,fy in FOODS):
                if math.hypot(ag.pos[0]-other.pos[0],ag.pos[1]-other.pos[1])<3.0:
                    other.H[0]=min(1.5, other.H[0]+0.03)
        # update eps hist
        for ag in [a1,a2]:
            with torch.no_grad():
                x=torch.tensor(entrada(ag.estado(),ag.other_pos,aa),dtype=torch.float32,device=DEVICE).unsqueeze(0)
                y=torch.tensor(np.concatenate([np.array(ag.pos)/WORLD_SIZE, ag.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
                eps=float((ag.pred(x)-y).pow(2).mean().sqrt())
            ag.eps_hist.append(eps)
            if len(ag.eps_hist)>100: ag.eps_hist.pop(0)
    # correlation of sigma
    if np.std(sig1)>1e-6 and np.std(sig2)>1e-6:
        r=float(np.corrcoef(sig1,sig2)[0,1])
    else: r=0.0
    # homeostasis group vs solo baseline (approx: solo E ~0.85)
    mean_e_joint=float(np.mean(e1+e2))
    return r, mean_e_joint, float(np.mean(sig1)), float(np.mean(sig2))

def run_solo_baseline(seed, steps=5000):
    return run_joint(seed, steps=steps)[1]

def main():
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--steps", type=int, default=30000)
    ap.add_argument("--out", type=str, default="results/ecologia_2agentes.json")
    args=ap.parse_args()
    rs=[]; es=[]
    for s in range(args.seeds):
        r,ej,_,_=run_joint(seed=5000+s, steps=args.steps)
        rs.append(r); es.append(ej)
        print(f" seed {s}: r_phi={r:.3f} E_joint={ej:.3f}")
    import pathlib, json
    out={"r_mean":float(np.mean(rs)),"r_std":float(np.std(rs)),"r_all":rs,"e_mean":float(np.mean(es)),"e_std":float(np.std(es)),"e_all":es,"steps":args.steps,"seeds":args.seeds}
    pathlib.Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(args.out).write_text(json.dumps(out,indent=2))
    print(f"N={args.seeds} r_mean={np.mean(rs):.3f}+-{np.std(rs):.3f} E_joint={np.mean(es):.3f}")

if __name__=="__main__": main()
