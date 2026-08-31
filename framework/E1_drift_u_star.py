#!/usr/bin/env python3
"""
E1 — Drift control + U* load-bearing (corrección de artefactos del panel).
U* es ahora el UMBRAL REAL de la gate Φ: el agente solo busca comida si σ_Φ < U*.
Dos brazos: selección (torneo) vs deriva (padres aleatorios), linajes independientes.
Φ pre-entrenado una vez y congelado (compartido, sin costo por agente).
H-EVO-2 re-hecho: atención ENTRENADA (300 pasos, entropía) antes del tradeoff.
"""
import math, random, json, argparse
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
WORLD_SIZE=20.0; NIEBLA_X=14.0
FOODS=[(3.0,3.0),(10.0,3.0)]
FOODS_FOG=[(16.0,3.0),(16.0,16.0),(17.0,10.0),(18.0,8.0)]
SOCIAL=(18.0,18.0)
RUIDO_BASE=0.15; RUIDO_NIEBLA=0.60
HSTAR_BOUNDS=[(0.6,1.0),(0.7,1.0),(0.1,0.5),(0.5,1.0)]
H_CANON=np.array([0.8,0.9,0.2,0.7])

class Predictor(nn.Module):
    def __init__(self): super().__init__(); self.net=nn.Sequential(nn.Linear(13,64),nn.ReLU(),nn.Linear(64,6))
    def forward(self,x): return self.net(x)
class Phi(nn.Module):
    def __init__(self): super().__init__(); self.net=nn.Sequential(nn.Linear(15,64),nn.ReLU(),nn.Linear(64,1))
    def forward(self,x): return torch.abs(self.net(x))
class Attention(nn.Module):
    def __init__(self): super().__init__(); self.net=nn.Sequential(nn.Linear(13,32),nn.ReLU(),nn.Linear(32,7))
    def forward(self,x): return torch.softmax(self.net(x),dim=-1)

def entrada(estado,a):
    if isinstance(a,int):
        a_oh=np.zeros(7,dtype=np.float32); a_oh[a]=1.0
    else: a_oh=np.float32(a)
    x,y=float(estado[0]),float(estado[1])
    H_norm=np.array([float(estado[i])/1.5 for i in range(2,6)],dtype=np.float32)
    return np.concatenate([np.array([x/WORLD_SIZE,y/WORLD_SIZE],dtype=np.float32),H_norm,a_oh],dtype=np.float32)
def entrada_phi(estado,a,em,es):
    return np.concatenate([entrada(estado,a),np.array([em,es],dtype=np.float32)])

def fisica(pos,a):
    x,y=pos[0]+a[0]*0.8,pos[1]+a[1]*0.8
    x*=0.95; y*=0.95; x=max(0.0,min(WORLD_SIZE,x)); y=max(0.0,min(WORLD_SIZE,y))
    return [x,y], x>NIEBLA_X
def ruido(ch,niebla):
    b=RUIDO_BASE
    if niebla and ch in (0,1,2,3,4): b=RUIDO_NIEBLA
    if ch==6: b=RUIDO_BASE*0.5
    return np.random.randn()*b

class CuerpoMundo:
    def __init__(self,h_star,foods):
        self.pos=[WORLD_SIZE/2,WORLD_SIZE/2]
        self.H=np.array([0.6,0.8,0.7,0.5],dtype=np.float32)
        self.h_star=np.array(h_star,dtype=np.float32); self.foods=foods; self.social=SOCIAL
    def en_niebla(self): return self.pos[0]>NIEBLA_X
    def estado(self): return np.array([self.pos[0],self.pos[1],self.H[0],self.H[1],self.H[2],self.H[3]],dtype=np.float32)
    def step(self,a_idx):
        a=np.zeros(7,dtype=np.float32); a[a_idx]=1.0; H=self.H
        if H[0]<0.55:
            dists=[math.hypot(self.pos[0]-fx,self.pos[1]-fy) for fx,fy in self.foods]
            idx=int(np.argmin(dists)); fx,fy=self.foods[idx]
            ag=np.zeros(7,dtype=np.float32); dx,dy=fx-self.pos[0],fy-self.pos[1]; n=math.hypot(dx,dy)+1e-6; ag[0]=dx/n; ag[1]=dy/n; a=ag
        elif H[3]>0.8:
            dx,dy=self.social[0]-self.pos[0],self.social[1]-self.pos[1]; n=math.hypot(dx,dy)+1e-6; ag=np.zeros(7,dtype=np.float32); ag[0]=dx/n; ag[1]=dy/n; a=ag
        np_pos,niebla=fisica(self.pos,a)
        dH=-0.02*(self.H-self.h_star)
        if niebla: dH[0]-=0.03; dH[2]+=0.01
        else: dH[2]-=0.01
        if any(math.hypot(self.pos[0]-fx,self.pos[1]-fy)<0.5 for fx,fy in self.foods): dH[0]+=0.12
        for ch in range(7):
            r=ruido(ch,niebla)
            if ch<4: dH[ch]+=r*0.1
        if math.hypot(self.pos[0]-self.social[0],self.pos[1]-self.social[1])<0.5: dH[3]+=0.1
        self.H=np.clip(self.H+dH,0,1.5); self.pos=np_pos
        return self.estado()

def preentrenar(phi, pred, mundo, steps=1500):
    opt=torch.optim.Adam(phi.parameters(),lr=1e-3); hist=[]
    for _ in range(steps):
        a=random.randrange(7); sa=mundo.estado(); sd=mundo.step(a_idx=a)
        x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(sd[:2])/WORLD_SIZE,sd[2:]/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        with torch.no_grad(): eps=float((pred(x)-y).pow(2).mean().sqrt())
        hist.append(eps)
        if len(hist)>50: hist.pop(0)
        h=np.array(hist)
        xp=torch.tensor(entrada_phi(sa,a,float(h.mean()),float(h.std())),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        loss=(phi(xp)-torch.tensor([[eps]],dtype=torch.float32,device=DEVICE)).pow(2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return phi

def entrena_pred(pred, mundo, steps=400):
    opt=torch.optim.Adam(pred.parameters(),lr=1e-3)
    for _ in range(steps):
        a=random.randrange(7); sa=mundo.estado(); sd=mundo.step(a_idx=a)
        x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(sd[:2])/WORLD_SIZE,sd[2:]/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        loss=(pred(x)-y).pow(2).mean(); opt.zero_grad(); loss.backward(); opt.step()
    return pred

def eval_agente(h_star, phi, pred, foods, seed, steps=5000, starve=False):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    mundo=CuerpoMundo(h_star,foods)
    pred=entrena_pred(pred,mundo,400)
    U_star=h_star[2]
    e_hist=[]; fog=0; food=0; eps_hist=[]
    for t in range(steps):
        if starve and t%400==399: mundo.H[0]=0.3
        sa=mundo.estado()
        with torch.no_grad():
            h=np.array(eps_hist) if len(eps_hist)>10 else np.array([0.1,0.05])
            xp=torch.tensor(entrada_phi(sa,4,float(h.mean()),float(h.std())),dtype=torch.float32,device=DEVICE).unsqueeze(0)
            sigma=float(phi(xp))
        if mundo.H[0]<0.55 and sigma<U_star: a=4
        elif mundo.H[3]>0.8: a=5
        else: a=random.randrange(4)
        if any(math.hypot(sa[0]-fx,sa[1]-fy)<0.5 for fx,fy in foods): food+=1
        mundo.step(a_idx=a)
        e_hist.append(float(mundo.H[0]))
        if mundo.en_niebla(): fog+=1
        x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(mundo.pos)/WORLD_SIZE,mundo.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        with torch.no_grad(): eps=float((pred(x)-y).pow(2).mean().sqrt())
        eps_hist.append(eps)
        if len(eps_hist)>100: eps_hist.pop(0)
    tight=np.mean([(0.7<=e<=1.0) for e in e_hist]); ran=np.mean([(0.5<=e<=1.2) for e in e_hist])
    food_rate=food/steps; fog_frac=fog/steps
    fitness=0.5*tight+0.3*food_rate-0.2*fog_frac
    return fitness, fog_frac, food_rate

def mutate(h):
    c=list(h)
    for i,(lo,hi) in enumerate(HSTAR_BOUNDS):
        if random.random()<0.5:
            c[i]+=np.random.randn()*0.05; c[i]=max(lo,min(hi,c[i]))
    return tuple(c)
def crossover(a,b): return tuple(a[i] if random.random()<0.5 else b[i] for i in range(4))

def run_evolucion(arm, phi, pred0, seeds_base, pop=20, gens=10, steps=3000):
    pop_i=[tuple(random.uniform(lo,hi) for lo,hi in HSTAR_BOUNDS) for _ in range(pop)]
    var_traj=[]; u_traj=[]
    for g in range(gens):
        fits=[]
        for idx,h in enumerate(pop_i):
            seed=seeds_base+g*1000+idx
            pred=Predictor().to(DEVICE)
            f,_,_=eval_agente(h,phi,pred,FOODS,seed,steps=steps)
            fits.append((f,h))
        fits.sort(key=lambda x:-x[0])
        hs=np.array([x[1] for x in fits])
        var_dim=np.var(hs,axis=0)
        var_traj.append(float(np.mean(var_dim)))
        u_traj.append(float(np.mean([x[1][2] for x in fits])))
        new_pop=[fits[0][1],fits[1][1]]
        while len(new_pop)<pop:
            if arm=="sel":
                c1=random.sample(fits,3); c1.sort(key=lambda x:-x[0]); p1=c1[0][1]
                c2=random.sample(fits,3); c2.sort(key=lambda x:-x[0]); p2=c2[0][1]
            else:
                p1,p2=random.sample(pop_i,2)
            child=crossover(p1,p2); child=mutate(child); new_pop.append(child)
        pop_i=new_pop
    return {"var_traj":var_traj,"u_traj":u_traj,"final_best":list(fits[0][1]),"final_fit":float(fits[0][0])}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--lineages",type=int,default=6)
    ap.add_argument("--pop",type=int,default=20)
    ap.add_argument("--gens",type=int,default=10)
    ap.add_argument("--steps",type=int,default=3000)
    ap.add_argument("--out",type=str,default="results/E1_drift_u_star.json")
    args=ap.parse_args()
    print(f"E1 drift-control: lineages={args.lineages} pop={args.pop} gens={args.gens} steps={args.steps}")
    # pre-train one shared Phi on canonical world
    mundo0=CuerpoMundo(list(H_CANON),FOODS)
    pred0=Predictor().to(DEVICE); entrena_pred(pred0,mundo0,600)
    phi=Phi().to(DEVICE); preentrenar(phi,pred0,mundo0,1500)
    print("Phi compartido pre-entrenado")
    sel_res=[]; drift_res=[]
    for li in range(args.lineages):
        s=li*100000
        rs=run_evolucion("sel",phi,pred0,s,args.pop,args.gens,args.steps)
        rd=run_evolucion("drift",phi,pred0,s,args.pop,args.gens,args.steps)
        sel_res.append(rs); drift_res.append(rd)
        print(f" lineage {li}: SEL var_g0={rs['var_traj'][0]:.4f}->var_g{args.gens-1}={rs['var_traj'][-1]:.4f} U*={rs['u_traj'][-1]:.3f} | DRIFT var={rd['var_traj'][-1]:.4f} U*={rd['u_traj'][-1]:.3f}",flush=True)
    # aggregate
    sel_var=[r["var_traj"][-1] for r in sel_res]; drift_var=[r["var_traj"][-1] for r in drift_res]
    sel_u=[r["u_traj"][-1] for r in sel_res]; drift_u=[r["u_traj"][-1] for r in drift_res]
    print(f"SEL var final {np.mean(sel_var):.4f}+-{np.std(sel_var):.4f} vs DRIFT {np.mean(drift_var):.4f}+-{np.std(drift_var):.4f}")
    print(f"SEL U* {np.mean(sel_u):.3f}+-{np.std(sel_u):.3f} vs DRIFT {np.mean(drift_u):.3f}+-{np.std(drift_u):.3f}")
    out={"sel":sel_res,"drift":drift_res,"sel_var_mean":float(np.mean(sel_var)),"drift_var_mean":float(np.mean(drift_var)),
         "sel_u_mean":float(np.mean(sel_u)),"drift_u_mean":float(np.mean(drift_u))}
    import pathlib; pathlib.Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(args.out).write_text(json.dumps(out,indent=2))
    print(f"Saved {args.out}")
    print("\n--- H-EVO-2 FIX (atención ENTRENADA) ---")
    # train attention properly
    attn=Attention().to(DEVICE)
    optA=torch.optim.Adam(attn.parameters(),lr=1e-3)
    for _ in range(300):
        a=random.randrange(7); sa=mundo0.estado(); mundo0.step(a_idx=a)
        x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        aw=attn(x)
        loss=torch.mean(aw*torch.log(aw+1e-8))+0.05*((aw-1.0/7)**2).mean()
        optA.zero_grad(); loss.backward(); optA.step()
    print("Atención entrenada (300 pasos, entropía)")
    # tradeoff with trained attention vs control (gate off = random uniform)
    trade=[]
    for with_phi in [True,False]:
        fog_fracs=[]
        for s in range(30):
            seed=9000+s
            random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
            mundo=CuerpoMundo(list(H_CANON),FOODS_FOG)
            pred=Predictor().to(DEVICE); entrena_pred(pred,mundo,400)
            fog_time=0
            for t in range(5000):
                if t%400==399: mundo.H[0]=0.3
                sa=mundo.estado()
                if with_phi:
                    x=torch.tensor(entrada(sa,4),dtype=torch.float32,device=DEVICE).unsqueeze(0)
                    with torch.no_grad(): aw=attn(x).cpu().numpy()[0]
                    if aw[0]<0.35 or np.mean(aw[1:5])>0.65: a=3
                    else:
                        if mundo.H[0]<0.55: a=4
                        elif mundo.H[3]>0.8: a=5
                        else: a=random.randrange(4)
                else:
                    if mundo.H[0]<0.55: a=4
                    elif mundo.H[3]>0.8: a=5
                    else: a=random.randrange(4)
                mundo.step(a_idx=a)
                if mundo.en_niebla(): fog_time+=1
            fog_fracs.append(fog_time/5000)
        mf=np.mean(fog_fracs); sf=np.std(fog_fracs)
        trade.append({"with_phi":bool(with_phi),"mean":float(mf),"std":float(sf)})
        print(f" {'conPhi(train)' if with_phi else 'sinPhi'}: fog {mf*100:.1f}% +- {sf*100:.1f}")
    d=(trade[0]["mean"]-trade[1]["mean"])/(np.sqrt((trade[0]["std"]**2+trade[1]["std"]**2)/2)+1e-8)
    print(f" Cohen d = {d:.2f}")
    out["tradeoff"]=trade; out["cohen_d_fixed"]=float(d)
    pathlib.Path(args.out).write_text(json.dumps(out,indent=2))

if __name__=="__main__": main()
