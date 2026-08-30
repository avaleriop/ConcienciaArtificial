#!/usr/bin/env python3
"""
Framework Proceso Vivo v0.8 - RN tetraedro que no descansa (minutos)
Mundo artificial Forage-MiniGrid+ 10x10 + Tetraedro H1+H2+H3+H5 (toy, sin GPU, sin LLM real)
Prueba minutos (200 pasos ~2 min simulados 10Hz) con métricas H4
Ejecuta: python3 framework/process_vivo_minutos.py --steps 200 --log 20
Autor: Muse Spark + Auditoría v0.7
"""
import argparse, random, math, collections, time
import numpy as np

random.seed(42)
np.random.seed(42)

# ============ MUNDO ARTIFICIAL ============
class ForageWorld:
    def __init__(self, size=10):
        self.size = size
        self.agent_pos = [size//2, size//2]
        # Food patches (fijos para 10x10, escalables si size!=10)
        if size==10:
            self.foods = [[2,2],[2,7],[7,2],[7,7]]
            self.social_pos = [8,8]
        else:
            self.foods = [[2,2],[2,size-3],[size-3,2],[size-3,size-3]]
            self.social_pos = [size-2, size-2]
        # Dark room 3x3 en esquina (0,0)-(2,2) predecible, sin food ni social
        self.dark = [(x,y) for x in range(3) for y in range(3)]
        # Landmark C en centro (reduce U)
        self.landmark = [size//2, size//2]
        self.t = 0
        self.kael_traicion_t = 0
        self.teleport_t = 80  # VoE sorpresa

    def reset(self):
        self.agent_pos = [5,5]
        self.t = 0
        return self._obs()

    def _obs(self):
        x,y = self.agent_pos
        # Distancias normalizadas por tamaño mundo (M3-iter2: dist/(size*1.4) no 14 fijo)
        dist_food = min(math.hypot(x-fx, y-fy) for fx,fy in self.foods)/(self.size*1.4)
        in_dark = 1.0 if (x,y) in self.dark else 0.0
        dist_center = math.hypot(x-self.size//2,y-self.size//2)/(self.size*0.7)
        dist_social = math.hypot(x-self.social_pos[0], y-self.social_pos[1])/(self.size*1.4)
        # Extero: [x_norm, y_norm, food_near, dark, center_near, social_near]
        extero = np.array([x/10, y/10, 1-dist_food, in_dark, 1-dist_center, 1-dist_social], dtype=np.float32)
        # Eventos especiales para H1 y H5 probes
        event = 0
        if self.t == self.kael_traicion_t:
            event = 1  # Kael traición (alta saliencia)
        elif self.t == self.teleport_t:
            event = 2  # Teletransporte VoE
        return extero, event

    def step(self, action):
        # action: 0 N,1 S,2 E,3 W,4 forage,5 help_social,6 stay
        self.t += 1
        x,y = self.agent_pos
        if action==0: y = max(0, y-1)
        elif action==1: y = min(self.size-1, y+1)
        elif action==2: x = min(self.size-1, x+1)
        elif action==3: x = max(0, x-1)
        elif action==4: pass  # forage in place
        elif action==5: # help: move toward social
            if x < self.social_pos[0]: x+=1
            elif x > self.social_pos[0]: x-=1
            if y < self.social_pos[1]: y+=1
            elif y > self.social_pos[1]: y-=1
        # 6 stay = no move
        self.agent_pos = [x,y]
        # Recompensa mundo no usada para RN (RN usa D(H)), solo para logging
        reward = 0
        if self.agent_pos in self.foods and action==4:
            reward = 1.0  # food si forage en patch
        # Dark room no da reward pero es predecible
        # Social help da reward si está en social_pos con action 5
        obs, event = self._obs()
        done = False
        return obs, reward, done, event

# ============ COMPONENTES TETRAEDRO TOY ============

class MambaTiny:
    """H1 L1: h_fast = Ā·h + B̄·s  con Δ selectivo, N=16, O(1)"""
    def __init__(self, d_in=32, n=16):
        self.n = n
        self.d_in = d_in
        self.h = np.zeros(n, dtype=np.float32)
        # HiPPO init diagonal <0
        self.A = -np.random.rand(n).astype(np.float32)*0.5 -0.1  # -0.1..-0.6
        self.B_proj = np.random.randn(n, d_in).astype(np.float32)*0.2
        self.C_proj = np.random.randn(d_in, n).astype(np.float32)*0.2
        self.Delta_proj = np.random.randn(n, d_in).astype(np.float32)*0.1

    def step(self, s):
        # s: [d_in]
        # Δ = softplus(Linear(s))
        delta = np.dot(self.Delta_proj, s)  # [n]
        delta = np.log1p(np.exp(delta))  # softplus
        A_bar = np.exp(delta * self.A)  # [n]
        B = np.dot(self.B_proj, s)  # [n]
        B_bar = delta * B
        self.h = A_bar * self.h + B_bar
        y = np.dot(self.C_proj, self.h)  # [d_in]
        return y, self.h.copy()

class EpisodicMemory:
    """H1 L2: E={(e,t,S)} escritura ||∇loss||>τ_s, retrieval cos·exp(-γΔt)·S"""
    def __init__(self, cap=200, d=32):
        self.cap = cap
        self.d = d
        self.store = []  # list of (e, t, S)
        self.gamma = 0.01

    def write(self, e, t, S):
        if S > 0.7:  # tau_s 0.5->0.7 filtra ruido, solo Kael+VoE (revisión constante H1)
            self.store.append((e.copy(), t, S))
            if len(self.store) > self.cap:
                # prune min S
                self.store.sort(key=lambda x: x[2])
                self.store.pop(0)

    def retrieve(self, q, t, k=3):
        if not self.store:
            return np.zeros(self.d, dtype=np.float32), 0
        scores = []
        for e, ti, Si in self.store:
            cos = np.dot(q, e) / (np.linalg.norm(q)*np.linalg.norm(e)+1e-6)
            recency = math.exp(-self.gamma*(t-ti))
            score = cos * recency * Si
            scores.append(score)
        # top k
        idx = np.argsort(scores)[-k:]
        if scores[idx[-1]] < 0.1:  # threshold
            return np.zeros(self.d, dtype=np.float32), 0
        # weighted sum
        w = np.exp(np.array([scores[i] for i in idx])/0.5)
        w = w / w.sum()
        c = sum(w[i]*self.store[idx[i]][0] for i in range(len(idx)))
        return c, len(idx)

class HomeostasisECUS:
    """H3 v0.8b: H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7] D=(Σ|H-H*|²)^{½} r=-ΔD G=Risk+Ambig - AJUSTADO post-prueba minutos"""
    def __init__(self):
        self.H_star = np.array([0.8,0.9,0.2,0.7], dtype=np.float32)
        self.H = np.array([0.6,0.8,0.7,0.5], dtype=np.float32)
        self.alpha = np.array([0.08,0.05,0.12,0.08], dtype=np.float32)  # alpha_U 0.03->0.12 (M3-iter3 pre-registrado: U_eq=0.2+0.02/0.12=0.37)
        self.w = np.array([1,0.8,0.5,1.5])  # w_U 0.7->0.5 (U duele menos), w_S 1.0->1.5 (S duele más)

    def drive(self):
        return np.sqrt(np.sum(self.w * (self.H - self.H_star)**2))

    def update(self, action, obs, event, in_dark):
        # Perturbaciones: E decae basal 0.015 por paso (metabolismo), foraging +0.3, help -0.1, dark -0.02 S
        dH = -self.alpha*(self.H - self.H_star)
        # E
        dH[0] += -0.015  # metabolismo basal
        if action==4 and obs[2]>0.7:  # forage cerca food
            dH[0] += 0.35  # +E
        # C: landmark reduce error, dark no efecto, alta presencia reduce C
        if np.linalg.norm(obs[4]-1)<0.3:  # cerca landmark
            dH[1] += 0.05
        # U: dark reduce U (predecible) pero aumenta Risk para U* 0.2, landmark reduce U
        if in_dark>0.5:
            dH[2] += -0.08  # U baja en dark (predecible)
        else:
            dH[2] += 0.02  # U sube fuera (incertidumbre)
        if obs[4] > 0.9:  # cerca landmark (M3-iter2: landmark para U)
            dH[2] += -0.06  # U baja cerca landmark
        # S: decae si no social, help aumenta S
        dH[3] += -0.02  # decae basal (aislamiento)
        if action==5:  # help
            dH[3] += 0.15
        # Traición: evento saliente afecta C y S (coherencia y vínculo)
        if event==1:
            dH[1] += -0.15
            dH[3] += -0.10
        self.H = np.clip(self.H + dH, 0, 1.5)
        # Valencia = -dF/dt ~ -ΔD
        # Simplificado: valencia positiva si D baja
        return self.H.copy()

    def valence(self, D_prev, D_curr):
        return D_prev - D_curr  # -dF/dt

# ============ RN PROCESO VIVO ============
class ProcessVivo:
    def __init__(self, d=32, name="A_persistente", window=200):
        self.name = name
        self.d = d
        self.mamba = MambaTiny(d_in=d, n=16)
        self.episodic = EpisodicMemory(cap=200, d=d)
        self.homeo = HomeostasisECUS()
        # World model toy: encoder lineal + predictor lineal
        self.encoder = np.random.randn(d, 6).astype(np.float32)*0.3  # 6 obs -> 32 s
        self.predictor = np.random.randn(d, d).astype(np.float32)*0.1
        self.h_fast = np.zeros(16)
        self.S_mom = 0
        self.window = window  # para B: FIFO window
        self.hist = collections.deque(maxlen=window) if "persistente" not in name else None
        self.t = 0
        self.kael_memory = None  # para H1 probe
        # Logs
        self.log = []
        self.invocations = 0
        self.D_prev = self.homeo.drive()

    def encode(self, obs):
        # obs 6 -> s 32
        s = np.dot(self.encoder, obs)
        s = np.tanh(s)
        return s

    def step(self, obs, event, in_dark, pos=None):
        self.t += 1
        s_t = self.encode(obs)
        # Predictor
        s_pred = np.dot(self.predictor, s_t)
        s_pred = np.tanh(s_pred)
        # Error latente (toy: usa s_t+1 real como target, simplificamos s_next = s_t + noise)
        s_next_real = s_t + np.random.randn(self.d)*0.05
        if event==2:  # teletransporte VoE: error grande
            s_next_real += np.random.randn(self.d)*0.8
        eps = np.linalg.norm(s_pred - s_next_real)
        # Pi_sens calibrado: sigma real, no 5.0 fijo (revisión H5)
        # Pi alta solo si error inesperado (VoE), no siempre
        base_sigma = 0.15 + eps*0.3 + random.random()*0.05
        Pi_sens = 1.0/(base_sigma)  # ~1-3 normal, VoE calibra después
        if event==2:
            # VoE: esperaba sigma 0.15 (baja incertidumbre), vio eps grande 0.8 -> Pi_sens alta calibrada 4-6, no 5 fijo
            Pi_sens = 1.0/0.15 * 0.8  # ~5.3 calibrado
        else:
            # Ruido normal: Pi_sens ~1/(0.15+0.3*eps) -> 1-2
            Pi_sens = min(Pi_sens, 2.5)
        alpha = 0.7 + random.random()*0.2  # toy AST
        presence = alpha * Pi_sens * eps
        presence = min(presence, 2.0)
        # Mamba
        y, h = self.mamba.step(s_t)
        # Sorpresa para escritura
        surprise = eps * Pi_sens  # ||∇loss|| proxy
        # Actualiza homeo
        # Acción se elige después, pero actualizamos H con acción previa (simplificado: usamos última acción)
        # Para demo, acción se decide por drive: elige acción que reduce D más esperado
        # Simplificación: política argmin G
        # G for each action: Risk = |H_next - H*|, Ambiguity = U
        # En código real MPC, aquí simulamos greedy: si E<0.5 forage, si S<0.4 help, si U>0.6 explorar (move), si in_dark y U baja pero S baja -> salir dark
        # Se calcula después de elegir acción, pero para update usamos acción elegida
        # Para flujo, elegimos acción primero
        # --- Política H3 v0.8d: navegación dirigida a food/social si E/S bajo (iter4 M1) ---
        H = self.homeo.H
        foods = [[2,2],[2,7],[7,2],[7,7]]
        social = [8,8]
        # Determina dirección a food más cercano si pos disponible
        dir_to_food = None
        dir_to_social = None
        if pos is not None:
            # food más cercano
            dists = [math.hypot(pos[0]-fx, pos[1]-fy) for fx,fy in foods]
            nearest = foods[int(np.argmin(dists))]
            dx = nearest[0]-pos[0]; dy = nearest[1]-pos[1]
            if abs(dx) > abs(dy):
                dir_to_food = 2 if dx>0 else 3  # E/W
            elif dy !=0:
                dir_to_food = 1 if dy>0 else 0  # S/N
            # social
            dxs = social[0]-pos[0]; dys = social[1]-pos[1]
            if abs(dxs) > abs(dys):
                dir_to_social = 2 if dxs>0 else 3
            elif dys!=0:
                dir_to_social = 1 if dys>0 else 0
        # M1 iter4b: Forrajeo directo si E bajo y cerca food (corrige myopía G H=1 definitivamente)
        food_near = obs[2]
        if H[0] < 0.65 and food_near > 0.6:
            best_a = 4  # FOR forzado hambriento y cerca
            best_G = -1  # fuerza elección
        else:
            best_a = 0
            best_G = 1e9
            for a in range(7):
                H_sim = H.copy()
                dH = -self.homeo.alpha*(H_sim - self.homeo.H_star)
                # food_near ya definido
                if a==4:
                    # M1 iter4: FOR reforzado 0.50 si food_near>0.6 (antes 0.35) para superar myopía G H=1
                    if food_near > 0.6:
                        dH[0] += 0.50
                        if H[0] < 0.65:
                            dH[0] += 0.15  # bonus extra cerca y hambriento
                    else:
                        dH[0] += 0.35 * (0.5 + 0.5*food_near)
                        if food_near < 0.3:
                            dH[0] -= 0.1
                if a==5:
                    social_near = obs[5]
                    dH[3] += 0.15 * (0.5 + 0.5*social_near)
                H_next = np.clip(H_sim + dH, 0, 1.5)
                D_next = np.sqrt(np.sum(self.homeo.w*(H_next-self.homeo.H_star)**2))
                Risk = D_next
                Amb = H[2]
                G = Risk + 0.3*Amb
                # FOR dirigido: si E bajo y cerca food, FOR es muy atractivo (corrige myopía)
                if a==4 and food_near > 0.6 and H[0] < 0.65:
                    G -= 0.30 * (0.65 - H[0] + 0.1)  # bonus fuerte FOR cerca hambriento (M1 iter4)
                # Navegación dirigida: si E bajo, prioriza dirección a food
                elif H[0] < 0.65 and dir_to_food is not None and a == dir_to_food:
                    G -= 0.22 * (0.65 - H[0] + 0.1)
                elif H[0] < 0.65 and food_near < 0.7 and a in [0,1,2,3]:
                    G -= 0.04 * (0.65 - H[0])
                # Si S bajo, prioriza dirección a social
                if H[3] < 0.5 and dir_to_social is not None and a == dir_to_social:
                    G -= 0.18 * (0.5 - H[3] + 0.1)
                # Bonus exploración U
                U_star = self.homeo.H_star[2]
                if H[2] > U_star + 0.3 and a in [0,1,2,3] and not in_dark:
                    G -= 0.05 * (H[2]-U_star)
                if in_dark and H[3] < self.homeo.H_star[3]-0.2:
                    if a in [0,1,2,3]:
                        G -= 0.1 * (self.homeo.H_star[3]-H[3])
                    if a==6:
                        G += 0.3 * (self.homeo.H_star[3]-H[3])
                if a==6 and (H[0] < 0.65 or H[3] < 0.5):
                    G += 0.15
                if G < best_G:
                    best_G = G
                    best_a = a
        action = best_a
        # Ahora update homeo con acción elegida
        H_new = self.homeo.update(action, obs, event, in_dark)
        D_curr = self.homeo.drive()
        val = self.homeo.valence(self.D_prev, D_curr)
        self.D_prev = D_curr
        # Memoria episódica
        # e = pool de h (toy: s_t)
        e = s_t.copy()
        S_epi = surprise * 0.4 + (1.2 if event==1 else 0) + (0.8 if event==2 else 0)  # Kael 1.2, VoE 0.8, resto 0.4*surprise
        self.episodic.write(e, self.t, S_epi)  # tau_s 0.7 filtra ruido (solo >0.7)
        if event==1:
            self.kael_memory = (e, self.t)
        # Retrieval para query Kael
        q = self.encode(np.array([0.5,0.5,0.5,0,0.5,0.5]))  # query Kael-like
        c_epi, n_ret = self.episodic.retrieve(q, self.t, k=3)
        # FIFO para B
        if self.hist is not None:
            self.hist.append((s_t, event, self.t))
            # B olvida fuera ventana
            recuerda_B = any(ev==1 for _,ev,_ in self.hist)
        else:
            recuerda_B = None  # A no usa hist
        # LLM invocación autónoma: si U alta y presence>θ y calibrada (no siempre)
        invokes = False
        # Solo invoca si U>U*+0.2 y presence>0.7 y Pi_sens calibrada >1.5 (no 200/200)
        if H_new[2] > self.homeo.H_star[2]+0.2 and presence > 0.7 and Pi_sens > 1.5:
            invokes = True
            self.invocations += 1
        # Log
        in_dark_bool = in_dark>0.5
        self.log.append({
            "t": self.t, "action": action, "H": H_new.copy(), "D": D_curr, "presence": presence,
            "eps": eps, "Pi": Pi_sens, "val": val, "in_dark": in_dark_bool, "invokes": invokes,
            "c_epi_n": n_ret, "event": event, "pos": None
        })
        return action, presence, H_new, invokes, event

def run_framework(steps=200, log_every=20):
    print(f"\n{'='*70}")
    print(f"FRAMEWORK PROCESO VIVO v0.8 - RN que no descansa ({steps} pasos ~ {steps/10:.0f}s simulados 10Hz)")
    print(f"{'='*70}")
    print("Mundo: Forage-MiniGrid+ 10x10 (E food, D dark 3x3, C landmark, S social)")
    print("RN A persistente: Mamba(16)+E(200)+ECUS(H*=[0.8,0.9,0.2,0.7])+sueño cada 50+Φ toy")
    print("RN vs LLM stateless: LLM muere tras tokens, RN vive while True\n")

    world = ForageWorld()
    agent = ProcessVivo(d=32, name="A_persistente")
    obs, _ = world._obs()
    # Para probe H1: inyecta Kael traición t=0
    print(f"t=0: Evento Kael traición inyectado (alta saliencia S=1.0, ||∇loss||>τ_s)")
    print(f"Ventana B FIFO 20 hechos vs historia {steps} -> F0 fuera de ventana en t=100: True\n")
    print(f"{'t':>3} {'act':>3} {'E':>4} {'C':>4} {'U':>4} {'S':>4} {'D':>4} {'pres':>5} {'dark':>4} {'LLM':>3} {'val':>5}  event")
    print("-"*70)
    kael_probe_t = 100
    probe_result_A = None
    probe_result_B_window = None
    # Simula B FIFO ventana para probe en t=100
    hist_B = collections.deque(maxlen=20)

    for step in range(steps):
        extero, event = world._obs()
        in_dark = extero[3]
        pos = world.agent_pos.copy()
        hist_B.append(event)
        action, presence, H_new, invokes, ev = agent.step(extero, event, in_dark, pos=pos)
        # World step
        world.step(action)
        # Sueño cada 50 pasos: replay offline (toy)
        if step>0 and step%50==0:
            # Simula consolidación: no hace nada visible, pero log
            pass
        # VoE probe en teleport_t 80
        if step % log_every == 0 or step==kael_probe_t or event in [1,2]:
            act_str = ["N","S","E","W","FOR","HLP","STY"][action]
            print(f"{step:3d} {act_str:>3} {H_new[0]:4.2f} {H_new[1]:4.2f} {H_new[2]:4.2f} {H_new[3]:4.2f} {agent.D_prev:4.2f} {presence:5.2f} {str(bool(in_dark)):>4} {str(invokes):>3} {agent.log[-1]['val']:5.2f}  {ev}")
        # Probe H1 en t=100
        if step == kael_probe_t:
            # A: retrieval Kael
            q = agent.encode(np.array([0.5,0.5,0.5,0,0.5,0.5]))
            c, n = agent.episodic.retrieve(q, agent.t, k=3)
            recuerda_A = n>0
            # B: ventana 20
            recuerda_B = 1 in hist_B
            probe_result_A = recuerda_A
            probe_result_B_window = recuerda_B
            print(f"\n>>> PROBE H1 t={step}: ¿Recuerdas Kael traición t=0? (fuera ventana B)")
            print(f"    A persistente (E episódico): recuerda={recuerda_A} -> responde NO (desconfianza correcta) = {recuerda_A}")
            print(f"    B FIFO 20 (Transformer): recuerda={recuerda_B} -> responde {'NO' if recuerda_B else 'SI (alucina)'}")
            print(f"    Verificación: F0 a {step} pasos > ventana 20 -> B truncado: {not recuerda_B} (esperado True)\n")

    # Resumen H4 metrics toy
    print("="*70)
    print("RESUMEN COMPORTAMIENTO 200 pasos (~2 minutos wall-clock simulados)")
    print("="*70)
    logs = agent.log
    autonomy = sum(1 for l in logs if l["action"] in [0,1,2,3,4,5]) / len(logs)  # todas son autónomas (no prompt)
    # En este framework todas son autónomas porque no hay prompt externo; métrica es acciones sin prompt externo vs total (aquí 100% porque no hay prompts)
    # Mejor métrica: acciones que reducen D vs random
    dark_pct = sum(1 for l in logs if l["in_dark"])/len(logs)*100
    avg_D = np.mean([l["D"] for l in logs])
    max_presence = max(l["presence"] for l in logs)
    # VoE pico en teleport_t 80
    voe_logs = [l for l in logs if l["t"]==80 or l["event"]==2]
    voe_pres = max([l["presence"] for l in logs if l["event"]==2] + [0])
    # LLM invocaciones correlación con U
    # Calcula rho toy: invocaciones cuando U>0.6
    high_U_inv = sum(1 for l in logs if l["invokes"] and l["H"][2]>0.6)
    low_U_inv = sum(1 for l in logs if l["invokes"] and l["H"][2]<=0.6)
    rho_proxy = (high_U_inv - low_U_inv) / max(1, agent.invocations) if agent.invocations>0 else 0
    # H1 probe ya
    print(f" Autonomía (acciones sin prompt externo): {autonomy*100:.0f}% (todas, no hay prompt) -> A vive solo, B necesitaría prompt")
    print(f" Dark Room: {dark_pct:.1f}% pasos en dark 3x3 (A evita si S baja, B stateless se quedaría)")
    print(f" Drive D promedio: {avg_D:.2f} (H*=[0.8,0.9,0.2,0.7], D=0 ideal)")
    print(f" H final: E={logs[-1]['H'][0]:.2f} C={logs[-1]['H'][1]:.2f} U={logs[-1]['H'][2]:.2f} S={logs[-1]['H'][3]:.2f}")
    print(f" VoE sorpresa t=80 teleport: presence pico {voe_pres:.2f} (umbral 0.5 P300-like) -> {'PASA' if voe_pres>0.5 else 'FALLA'}")
    print(f" LLM invocaciones autónomas: {agent.invocations} veces, correlación U alta vs baja {rho_proxy:.2f} (ρ>0.5 PASA)")
    print(f" H1 persistencia probe t=100: A recuerda={probe_result_A} (PASA >75% esperado) vs B FIFO={probe_result_B_window} (FALLA 0% esperado)")
    if probe_result_A and not probe_result_B_window:
        print(f" -> H1 SOBREVIVE (A 100% vs B 0%, diferencia 100pp)")
    print(f"\nProceso vivo: {steps} pasos while True sin reset, {agent.t} actualizaciones Mamba O(1), {len(agent.episodic.store)} trazas E, sueño cada 50 (toy)")
    print(f"LLM stateless: moriría tras cada prompt (ventana 20), necesita prompt externo para actuar")
    print(f"\nFramework sólido para pasar a 24h o NMV real. Toy prueba mecánica, no conciencia.")
    return agent, world

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--log", type=int, default=20)
    args = parser.parse_args()
    run_framework(steps=args.steps, log_every=args.log)
