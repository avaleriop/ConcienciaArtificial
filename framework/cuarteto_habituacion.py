#!/usr/bin/env python3
"""
Cuarteto de habituación (Thompson-Spencer / Rankin) + dial EWC-λ.
E1: recuperación espontánea + savings bajo interferencia.
E2: sweep EWC-λ {0, 0.5, 5, 50} + sensibilización/dishabituación.
N=30, z con baseline congelada (pre-violación), ε crudo también reportado.
"""
import math, random, json, argparse
import numpy as np
import torch
import torch.nn as nn

random.seed(7); np.random.seed(7); torch.manual_seed(7)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
WORLD_SIZE=20.0; NIEBLA_X=14.0
FOODS=[(3.0,3.0),(10.0,3.0)]
SOCIAL=(18.0,18.0)
RUIDO_BASE=0.15; RUIDO_NIEBLA=0.60
H_CANON=np.array([0.8,0.9,0.2,0.7])
EWC_LAMBDAS=[0.0,0.5,5.0,50.0]

class Predictor(nn.Module):
    def __init__(self,d1=13,dh=64,d2=6): super().__init__(); self.net=nn.Sequential(nn.Linear(d1,dh),nn.ReLU(),nn.Linear(dh,d2))
    def forward(self,x): return self.net(x)

def entrada(estado,a):
    if isinstance(a,int):
        a_oh=np.zeros(7,dtype=np.float32); a_oh[a]=1.0
    else: a_oh=np.float32(a)
    x,y=float(estado[0]),float(estado[1])
    H_norm=np.array([float(estado[i])/1.5 for i in range(2,6)],dtype=np.float32)
    return np.concatenate([np.array([x/WORLD_SIZE,y/WORLD_SIZE],dtype=np.float32),H_norm,a_oh],dtype=np.float32)

def fisica(pos,a):
    x,y=pos[0]+a[0]*0.8,pos[1]+a[1]*0.8
    x*=0.95; y*=0.95; x=max(0.0,min(WORLD_SIZE,x)); y=max(0.0,min(WORLD_SIZE,y))
    return [x,y], x>NIEBLA_X

def ruido(ch,niebla):
    b=RUIDO_BASE
    if niebla and ch in (0,1,2,3,4): b=RUIDO_NIEBLA
    if ch==6: b=RUIDO_BASE*0.5
    return np.random.randn()*b

class Mundo:
    def __init__(self):
        self.pos=[WORLD_SIZE/2,WORLD_SIZE/2]
        self.H=np.array([0.6,0.8,0.7,0.5],dtype=np.float32)
    def en_niebla(self): return self.pos[0]>NIEBLA_X
    def estado(self): return np.array([self.pos[0],self.pos[1],self.H[0],self.H[1],self.H[2],self.H[3]],dtype=np.float32)
    def step(self,a_idx,teleport=False):
        a=np.zeros(7,dtype=np.float32); a[a_idx]=1.0
        if teleport:
            self.pos=[min(WORLD_SIZE,max(0.0,self.pos[0]+2.0)),min(WORLD_SIZE,max(0.0,self.pos[1]+2.0))]
        np_pos,niebla=fisica(self.pos,a)
        dH=-0.02*(self.H-H_CANON)
        if niebla: dH[0]-=0.03; dH[2]+=0.01
        else: dH[2]-=0.01
        if any(math.hypot(self.pos[0]-fx,self.pos[1]-fy)<0.5 for fx,fy in FOODS): dH[0]+=0.12
        for ch in range(7):
            r=ruido(ch,niebla)
            if ch<4: dH[ch]+=r*0.1
        if math.hypot(self.pos[0]-SOCIAL[0],self.pos[1]-SOCIAL[1])<0.5: dH[3]+=0.1
        self.H=np.clip(self.H+dH,0,1.5); self.pos=np_pos
        return self.estado()

def pred_entrena(pred, mundo, steps=400):
    opt=torch.optim.Adam(pred.parameters(),lr=1e-3)
    for _ in range(steps):
        a=random.randrange(4); sa=mundo.estado(); sd=mundo.step(a_idx=a)
        x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(sd[:2])/WORLD_SIZE,sd[2:]/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        loss=(pred(x)-y).pow(2).mean(); opt.zero_grad(); loss.backward(); opt.step()
    return pred

def violacion_z(pred, mundo, teleport_dist=2.0, n=8):
    """z con baseline congelada: mide ε pre-violación (window) y post-violación."""
    eps_pre=[]
    for _ in range(n):
        a=random.randrange(4); sa=mundo.estado(); mundo.step(a_idx=a)
        x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(mundo.pos)/WORLD_SIZE,mundo.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        with torch.no_grad(): eps_pre.append(float((pred(x)-y).pow(2).mean().sqrt()))
    # violación
    a=random.randrange(4); sa=mundo.estado()
    mundo.step(a_idx=a,teleport=True)
    x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
    y=torch.tensor(np.concatenate([np.array(mundo.pos)/WORLD_SIZE,mundo.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
    with torch.no_grad(): eps_viol=float((pred(x)-y).pow(2).mean().sqrt())
    mu,std=np.mean(eps_pre),np.std(eps_pre)+1e-8
    return (eps_viol-mu)/std, eps_viol, mu, std

def run_protocolo(seed, lam, n_hab=12, rest=2000, use_interference=False, n_probe=1):
    """Protocolo completo: habituar -> descanso (frozen o interferencia) -> probe -> re-habituar (savings)."""
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    mundo=Mundo(); pred=Predictor().to(DEVICE)
    pred_entrena(pred,mundo,400)
    w_star={k:v.detach().clone() for k,v in pred.named_parameters()}
    fisher={k:torch.zeros_like(v) for k,v in pred.named_parameters()}
    opt=torch.optim.Adam(pred.parameters(),lr=1e-3)
    # FASE 1: habituación (n_hab violaciones con aprendizaje)
    z_hab=[]
    for i in range(n_hab):
        z,eps,mu,std=violacion_z(pred,mundo)
        z_hab.append(z)
        if i==0: z_original=z
        # aprendizaicé sobre la violación
        x=torch.tensor(entrada(mundo.estado(),0),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(mundo.pos)/WORLD_SIZE,mundo.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        loss=(pred(x)-y).pow(2).mean()
        ewc=0.0
        for k,p in pred.named_parameters():
            if p.grad is not None and k in w_star:
                ewc=ewc+lam/2*(fisher[k]*(p-w_star[k])**2).sum()
        loss=loss+ewc
        opt.zero_grad(); loss.backward(); opt.step()
        for k,p in pred.named_parameters():
            if p.grad is not None: fisher[k]=0.9*fisher[k]+0.1*p.grad.detach()**2
    z_habituado=np.mean(z_hab[-4:])
    # FASE 2: descanso (EWC activo si interferencia; interferencia = violaciones nuevas)
    if use_interference:
        for _ in range(rest//50):
            a=random.randrange(4); mundo.step(a_idx=a)
            z2,eps2,_,_=violacion_z(pred,mundo)
            x=torch.tensor(entrada(mundo.estado(),0),dtype=torch.float32,device=DEVICE).unsqueeze(0)
            y=torch.tensor(np.concatenate([np.array(mundo.pos)/WORLD_SIZE,mundo.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
            loss=(pred(x)-y).pow(2).mean()
            ewc=0.0
            for k,p in pred.named_parameters():
                if p.grad is not None and k in w_star:
                    ewc=ewc+lam/2*(fisher[k]*(p-w_star[k])**2).sum()
            loss=loss+ewc
            opt.zero_grad(); loss.backward(); opt.step()
    else:
        for k,p in pred.named_parameters():
            if 'weight' in k or 'bias' in k:
                p.data.copy_(w_star[k].data)  # congelar = restaurar snapshot pre-hab
    # FASE 3: probe (recuperación espontánea) — referencia = z_original
    z_probe,eps_probe,_,_=violacion_z(pred,mundo,n_probe)
    recuperacion=float(z_probe/(z_original+1e-8))
    # FASE 4: re-habituación (savings) - contar violaciones hasta 50% del z_original
    savings=0
    for i in range(20):
        z,eps,_,_=violacion_z(pred,mundo)
        if z<z_original*0.5: savings=i+1; break
    return {"z_habituado":float(z_habituado),"z_probe":float(z_probe),"recuperacion":recuperacion,"savings":savings}

def run_sensibilizacion(seed, lam):
    """Dishabituación: habituar a (+2,+2), luego estímulo más fuerte (+10,+10), luego re-probar."""
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    mundo=Mundo(); pred=Predictor().to(DEVICE)
    pred_entrena(pred,mundo,400)
    opt=torch.optim.Adam(pred.parameters(),lr=1e-3)
    fisher={k:torch.zeros_like(v) for k,v in pred.named_parameters()}
    w_star={k:v.detach().clone() for k,v in pred.named_parameters()}
    for _ in range(12):
        z,eps,_,_=violacion_z(pred,mundo)
        x=torch.tensor(entrada(mundo.estado(),0),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        y=torch.tensor(np.concatenate([np.array(mundo.pos)/WORLD_SIZE,mundo.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
        loss=(pred(x)-y).pow(2).mean()
        ewc=0.0
        for k,p in pred.named_parameters():
            if p.grad is not None and k in w_star:
                ewc=ewc+lam/2*(fisher[k]*(p-w_star[k])**2).sum()
        loss=loss+ewc
        opt.zero_grad(); loss.backward(); opt.step()
        for k,p in pred.named_parameters():
            if p.grad is not None: fisher[k]=0.9*fisher[k]+0.1*p.grad.detach()**2
    z_base,_,_,_=violacion_z(pred,mundo)  # z a estímulo habituado
    # estímulo fuerte: teleport 10
    a=random.randrange(4); sa=mundo.estado()
    mundo.pos=[min(WORLD_SIZE,max(0.0,mundo.pos[0]+10.0)),min(WORLD_SIZE,max(0.0,mundo.pos[1]+10.0))]
    x=torch.tensor(entrada(sa,a),dtype=torch.float32,device=DEVICE).unsqueeze(0)
    y=torch.tensor(np.concatenate([np.array(mundo.pos)/WORLD_SIZE,mundo.H/1.5]),dtype=torch.float32,device=DEVICE).unsqueeze(0)
    with torch.no_grad(): eps_f=float((pred(x)-y).pow(2).mean().sqrt())
    # re-probar el estímulo original (dishabituación)
    z_re,_,_,_=violacion_z(pred,mundo)
    return {"z_base":float(z_base),"z_fuerte_eps":float(eps_f),"z_reprobe":float(z_re)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seeds",type=int,default=30)
    ap.add_argument("--lam",type=float,default=None,help="sweep de EWC-lambda; default: todos")
    ap.add_argument("--out",type=str,default="results/cuarteto_habituacion.json")
    args=ap.parse_args()
    lams=[args.lam] if args.lam else EWC_LAMBDAS
    results={}
    for lam in lams:
        res_inter=[]; res_frozen=[]
        for s in range(args.seeds):
            ri=run_protocolo(seed=4000+s,lam=lam,n_hab=12,rest=2000,use_interference=True)
            rf=run_protocolo(seed=4000+s,lam=lam,n_hab=12,rest=2000,use_interference=False)
            res_inter.append(ri); res_frozen.append(rf)
            if s%10==0: print(f" lam={lam} seed {s}: rec_inter={ri['recuperacion']:.2f} rec_frozen={rf['recuperacion']:.2f} savings={ri['savings']}",flush=True)
        rec_i=np.mean([r["recuperacion"] for r in res_inter]); rec_f=np.mean([r["recuperacion"] for r in res_frozen])
        sav_i=np.mean([r["savings"] for r in res_inter])
        print(f"lam={lam}: N={args.seeds} recuperación INTERFERENCIA={rec_i:.2f} FROZEN={rec_f:.2f} savings={sav_i:.1f}")
        results[f"lam_{lam}"]={"inter":res_inter,"frozen":res_frozen,"rec_inter":float(rec_i),"rec_frozen":float(rec_f),"savings_mean":float(sav_i)}
    # sensibilización con λ=5 (representativo)
    sens=[]
    for s in range(10):
        sens.append(run_sensibilizacion(seed=8000+s,lam=5.0))
    results["sensibilizacion_lam5"]={"data":sens,"z_fuerte_mean":float(np.mean([x["z_fuerte_eps"] for x in sens])),"z_base_mean":float(np.mean([x["z_base"] for x in sens]))}
    import pathlib; pathlib.Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(args.out).write_text(json.dumps(results,indent=2))
    print(f"Saved {args.out}")

if __name__=="__main__": main()
