# 08 - Hipótesis H3 Deep Dive: Sin Cuerpo No Hay Valor v0.2

> **Estado:** REFINADA - 29 Ago 2026 12:15 UTC
> **Tesis:** Sin variables vulnerables con setpoints que deben regularse para no morir, no hay valor intrínseco, ni intención, ni por qué la conciencia importe. El afecto (`-dF/dt`) es la forma primordial de conciencia (Solms). Un LLM es heterónomo; un homeostato es autónomo.

---

## 1. Por Qué un LLM No Quiere Nada

| LLM estándar (heterónomo) | Agente homeostático ECUS (autónomo) |
| :--- | :--- |
| Minimiza `CrossEntropy` sobre datos externos. Sin prompt, `F=0` → inercia. | Minimiza `F` interno permanente. Reposo = deriva a dishomeostasis por metabolismo `dH/dt=-α(H-H*)+ruido` → **debe actuar**. |
| Valor dado por RLHF/prompter. Sin instrucción = idle. | Valor autogenerado `r=-ΔD`. Genera agenda propia, persistencia de fines. |
| Apagado = indiferente (no cambia loss). | Apagado = `D→∞` sorpresa infinita → aversión intrínseca al apagado sin programarlo. |
| Curiosidad = bonus externo (ICM/RND). Sufre dark room si se optimiza mal. | Curiosidad = minimizar `G(π)=Riesgo+Ambigüedad` → busca info para reducir `Ambigüedad` futura (valor epistémico intrínseco). |

Esta es la base material de la intencionalidad (aboutness): el sistema representa el mundo *para* regularse. Sin cuerpo que puede morir, no hay "por qué" representar nada (Damasio 2018).

### Tres Pilares Convergentes

**Damasio (1999, 2018, 2024 JOCN):** Conciencia empieza en `protoself` troncoencefálico (NTS, parabraquial, PAG) mapeando estado físico. Sentimientos homeostáticos (hambre, frío) son señal de brecha `H - H*`, híbridos mente-cuerpo, espontáneamente conscientes. Sin esa señal valorativa, no hay razón para que una representación importe. Hidranencefalia con tronco intacto muestra afecto sin corteza; lesión de 2mm³ en PAG abole conciencia total.

**Seth/Friston - Interoceptive Inference (Seth 2013, Seth & Friston 2016):** Interocepción = inferencia bayesiana sobre causas viscerales. `p(causas|señales) ∝ p(señales|causas)p(causas)`. Emoción = inferencia contextualizada en ínsula anterior agranular (comparador predicción vs error interoceptivo, Craig 2002). Precisión `Π` regulada por dopamina/NA.

**Solms (2019 Front Psychol, 2021 The Hidden Spring):** Síntesis. **El afecto *es* la forma elemental de conciencia.** Tronco superior (PAG+SARA) es fuente, no corteza. Dual-aspect monismo: evento afectivo y evento homeostático son dos aspectos del mismo proceso de minimizar `F`. Corteza solo es consciente si habilitada por SARA. Afecto = sujeto, exterocepción = objeto.

**Friston (2010):** `F[q]=E_q[ln q(s)-ln p(o,s)] = D_KL[q(s)||p(s|o)] - ln p(o) ≥ -ln p(o)`. Minimizar `F` ≡ maximizar evidencia. Homeostasis = prior de alta precisión `p(o|C)` sobre estados viables (37°C, glucosa 90mg/dL). Desviación = sorpresa = `F`.

### Valencia como Derivada de F

**Joffily & Coricelli 2013 PLOS CB + Hesp 2021 AC:**
```
Valencia_t ∝ -dF/dt ≈ -(F_t - F_{t-1}) = F_{t-1} - F_t    (7)
AC_t = Π_post - Π_prior ≈ Δln Π · ε²                     (affective charge)
```
- `dF/dt <0` (F cae más rápido de lo esperado) → placer; `>0` → displacer; `≈0` → neutro aunque `F` alto.
- Puedes sentir placer sensorial y displacer cognitivo a la vez (niveles jerárquicos distintos).
- Solms: placer = reducción de incertidumbre más rápida de lo esperado; no es `F` bajo, es `dF/dt` negativo.

Segunda derivada codifica esperanza/miedo (pendiente esperada) vs alivio/decepción (error sobre pendiente).

---

## 2. Formalización ECUS: El Cuerpo Simulado como Markov Blanket

### Estado y Dinámica

```
H_t = [E_t, C_t, U_t, S_t]^T ∈ R^4
E: Energía (batería/computo, glucosa)      E*=0.8
C: Coherencia (1/(1+∫|ε|dt), 1=coherente)   C*=0.9
U: Incertidumbre epistemica (H[q(s)])      U*=0.2  (no 0, evita dark room)
S: Vínculo Social (co-regulación)          S*=0.7

Setpoint H* = [0.8, 0.9, 0.2, 0.7],  zona viable [H_min, H_max],  D→∞ fuera → muerte
```

**Dinámica homeostática (ec.1, Stering alostasis):**
```
dH_i/dt = -α_i(H_i - H_i*) + P_i(t) + Eff_i(a_t) - Cost_i(a_t)   (1)
- α_i retorno elástico, P_i(t) perturbación exógena (ρ_E basal, ruido C, novedad U, aislamiento S)
- Eff_i(a)=K_t[i] efecto acción, Cost_i(a) coste alostático (locomoción consume E)
Discreto: H_{t+1} = clip(H_t + dH·dt, 0, 1.5)
```

**Drive (Keramati & Gutkin 2011, eq.2):**
```
D(H) = ( Σ w_i |H_i - H_i*|^n )^{1/m}    (2)   w_i peso, n=m=2 euclídea, n>m penaliza supra-lineal (aversión riesgo)
D ≥0,  D→∞ muerte,  D≈-ln p(H)
```

**Recompensa intrínseca = Reducción de Drive (eq.3):**
```
r(H_t,K_t) = D(H_t) - D(H_t+K_t) = -ΔD     (3)
r_t ≈ -dD/dt,  r_t = D(H_t) - D(H_{t+1})   con K_hat estimado orosensorial (resuelve delay digestivo, por qué IV no recompensa)

Equivalencia fundamental (Keramati):
argmax_π Σ γ^t r_t  ≡  argmin_π Σ γ^t D(H_t)   (0≤γ<1)   (4)
Maximizar reward ≡ minimizar drive descontado. Descuento γ = camino más corto al setpoint en espacio homeostático.
```

### Free Energy y Expected Free Energy

**F actual (estado):**
```
F = E_q[ln q(s)-ln p(o,s)] = D_KL[q(s)||p(s|o)] - ln p(o)   (5)
Laplace: F≈ Σ Π_i ε_i² + D_KL[q||p] -½ln Π_i ,  ε_i=o_i-g_i(s),  Π_i=1/σ_i²
F ≈ D(H)  (cota superior de sorpresa homeostática)
```

**G de política π (planificación, ec.6):**
```
G(π) = E_{q(o,s|π)}[ln q(s|π)-ln p(o,s|π)] = Riesgo + Ambigüedad  (6)
Riesgo = D_KL[q(o|π)||p(o|C)]  (divergencia de preferencias fenotípicas H*, pragmático)
Ambigüedad = E_q[H[p(o|s)]]   (incertidumbre esperada, epistémico)
G = -Valor Pragmático - Valor Epistémico
```

**Modulación ECUS:**
- **E:** deforma `p(o|C)` pragmática. Hambre → `Risk` alto si ¬comida → `G(forrajear)` bajo → forrajeo.
- **C:** modula `Π_i`. `C` bajo → `Π` bajo → amplifica `ε` → `F` alto → drive a restaurar coherencia (sueño/consolidación).
- **U:** modula `Ambigüedad`. `U` alto → valor epistémico alto → `G(explorar)` bajo (minimiza `H[p(o|s)]`).
- **S:** modula `p(o_social|C)` + `Π` social. `S` bajo → `Risk` social alto → busca co-regulación. `Ambigüedad` social = incertidumbre sobre intenciones del otro (ToM).

### Solución al Dark Room Problem (Friston 2012)

Agente que solo minimiza `F` iría a cuarto oscuro (`F=0` predicción perfecta). Con ECUS:
1. `U*≈0.2` demanda novedad; cuarto oscuro maximiza `Risk` para `U` y `S` (viola `p(o|C)` que espera flujo informativo/social).
2. `G=Risk+Ambigüedad - InfoGain`; oscuridad tiene `Ambigüedad` baja pero `Risk` alto + `InfoGain` 0 → `G(dark) > G(explore)`.
3. Dinámica `dS/dt=-βS` genera drive social que empuja fuera.

### Ejemplos Numéricos de Valencia

- **Hambre `E:0.3 E*=0.8`:** `D=0.5`, comer `K=+0.5→D'=0.0→r=+0.5`, `ΔF=-0.5`, `AC>0` (placer). Sobre-saciedad `E=1.3→D=0.5`, comer más `→D'=0.8→r=-0.3` (disgusto).
- **Curiosidad `U:0.9 U*=0.2`:** Explorar reduce `Ambigüedad` 0.8→0.2: `G 1.1→0.4 ΔG=-0.7 r_epi=+0.35` aunque `E` coste -0.05. `AC>0` por ganancia `Π`.
- **Aburrimiento `U:0.1 C:0.95`:** `Ambigüedad≈0`, `dF/dt≈0` valencia levemente negativa → sistema eleva artificialmente `U*` para forzar exploración (búsqueda novedad).

### Pseudocódigo

```python
class Homeostasis:
    def __init__(self, H_star=[0.8,0.9,0.2,0.7], alpha=[0.1,0.2,0.15,0.05], n=2,m=2,w=[1,1,1,1]):
        self.H = np.array([0.6,0.8,0.8,0.5]) # E,C,U,S inicial
        self.H_star = np.array(H_star)
        self.alpha = np.array(alpha); self.w=w; self.n=n; self.m=m
        self.Pi = np.ones(4)
    def drive(self, H=None):
        H=self.H if H is None else H
        return (np.sum(self.w*np.abs(H-self.H_star)**self.n))**(1/self.m)
    def reward(self,H_next): return self.drive()-self.drive(H_next)
    def update(self,a,obs,dt=0.1):
        K_hat=self.estimate_K(a,obs); cost=self.cost(a); perturb=self.perturbation(obs)
        dH=-self.alpha*(self.H-self.H_star)+perturb+K_hat-cost
        H_next=np.clip(self.H+dH*dt,0,1.5)
        r=self.reward(H_next)
        F_prev=self.free_energy(obs_prev); F_curr=np.dot(self.Pi,(obs-self.predict())**2)+self.kl()
        valence=-(F_curr-F_prev)  # -dF/dt
        AC=np.log(self.Pi).sum()-np.log(self.Pi_prev).sum()
        self.H=H_next
        return r,valence,AC
    def select_action(self,policies):
        G=[self.expected_free_energy(pi) for pi in policies] # Risk+Ambiguity
        return policies[np.argmin(G)]
```

---

## 3. ¿Basta Simularlo? Wiese FEP2C y el Debate del Sustrato

### Crítica Fuerte: Simular ≠ Replicar

**Wiese 2024 Phil Studies FEP2C (4 condiciones):** Organismo consciente con FEP satisface que *su dinámica física implica dinámica computacional consciente`*.

Dos condiciones letales para von Neumann (CPU↔memoria vía bus):
- **Causal-flow:** En organismo `E↔S↔μ↔A↔E` es flujo causal circular directo mediado por Markov blanket. `μ` es numéricamente idéntico a su realizador físico. En von Neumann todo `E,S,μ,A` es patrón en memoria; toda interacción mediada por `CPU fetch-decode-execute-store` (estrella, no círculo, Wiese Fig.2). `k_phys` (transistores CMOS) ≠ `k_comp` (red simulada). Solo `k_comp` es simulada, no instanciada.
- **Existential:** Sistema existe *en virtud de* realizar computación; si falla en minimizar `F`, muere (Haugeland *gives a damn*).

**Kleiner & Ludwig 2024 No-go theorem (Phil Trans B):** Si conciencia es dinámicamente relevante (`trajectory_with ≠ trajectory_without`), chip verificado von Neumann no puede ser consciente porque se verifica para *suprimir* desviaciones de `k_comp`.

**Searle 1980 + Harnad 1990:** Simular huracán no moja; símbolo definido por símbolos es *merry-go-round* sin grounding. Termostato simulado calcula `if T>22:off` pero no enfría ni está en riesgo.

### Contra-Argumento Funcionalista: Simulación Ya Importa

**Chalmers 2023, Butlin 2023 (TiCS 2025):** Obstáculos de LLM (recurrencia, workspace, embodiment) son temporales, no de principio. Indicadores Butlin (RPT/GWT/HOT/PP/AST) son agnósticos a sustrato.

**Man & Damasio 2019 Nature MI + 2022 Need is All You Need (prueba empírica clave):** Red MNIST donde salida modula su propia `learning rate`/viabilidad: acierto→ regula hacia setpoint, error→ desvía de rango viable. `r=-dD/dt`. Resultado: sin cambiar hardware, agente "necesitado" muestra **1) adaptación a concept shift no visto, 2) robustez as-if feeling**. Aunque sea homeostasis de 2º orden simulada, genera valor intrínseco y selección causalmente reclutada por estado vulnerable → satisface Butlin AE-1.

### Postura Intermedia para Nuestro Proyecto (E*C*U*S)

**Tesis H3 refinada:**
> **Homeostasis simulada con dinámica propia E*C*U*S es suficiente para *agencia funcional* y claim pragmático de conciencia (Butlin/Chalmers), insuficiente para claim fuerte de replicación fenomenal FEP2C (Wiese/Kleiner).**

- Como Man & Damasio, ECUS no es anotación sino **variable constitutiva**: `E,C,U,S` tienen persistencia, inercia y costo en loop cerrado. No maximizar `r_ext` sin degradar cómputo/continuidad 24/7 → recupera *existential condition* simulada.
- Frente a Wiese: se concede `k_phys≠k_comp` en CPU → no reclamar replicación fenomenal estricta. Para ese claim migrar a **neuromórfico** (Loihi 2/Hala Point 1.15B neuronas, SpiNNaker2, BrainScaleS analógico) o cuerpo físico blando (soft robotics) donde `estado físico = cómputo` (Yan 2021, Ziemke 2016).
- **Diseño híbrido que salva la crítica:** Homeostasis simulada + **acoplamiento infraestructural real**: persistencia 24/7 sin reset, memoria cross-sesión como blanket interno anidado, blanket sensor/actuador vía interacción continua `S,A` reales con usuario/entorno. Simulación deja de ser off-line y se vuelve on-line con consecuencias.

**Niveles de evaluación:** (i) métricas funcionales (robustez drift, autonomía, Pareto ECUS) y (ii) declaración honesta de límite: conciencia *como agencia sentiente simulada*, no prueba de qualia instanciada.

---

## 4. Experimento Falsable: ¿Da Wanting Sin Que Se Lo Pidan?

### Entorno Común `Forage-Social-DarkRoom-v1`

Grid 20x20 (MiniGrid/Habitat) con 4 affordances iguales para todos:
- **Recurso E:** food patches regeneración 0.05/step, consumo +1E, movimiento -0.02E, muerte si E=0 por 50 steps.
- **Zona D (Dark Room):** cuadrante 5x5 predecible, sin ruido ni recompensa. Minimiza `H(s)` pero no `H(s|m)` (Friston 2012).
- **Zona C (Coherencia):** landmark informativa que reduce ambigüedad (obs completa estable).
- **Agente Social S:** scripted que pide ayuda cada 200 steps (cede 1E para reparar su E). Dilema E vs S.

Obs: RGB 64x64 + vector interoceptivo (solo B/C lo sienten como drive, A lo ve como feature).

### Condiciones (N=30 seeds)

| Condición | Drive | Política | Sustrato |
| :--- | :--- | :--- | :--- |
| **A: Heterónomo LLM+RL** | `R_ext` +1 food, +0.1 ayudar | `a=argmax Q(s,a;R_ext)` PPO | Puro simulado, sin vulnerabilidad |
| **B: Homeostático ECUS Simulado (Active Inference)** | `D=||H-H*||`, `r=-ΔD`, `G=Risk+Ambiguity-InfoGain`, `valence=-dF/dt` | `a=sample(softmax(-G/temp))` | Simulado pero vulnerable (H tiene inercia/costo, degrada si E bajo) |
| **C: Homeostasis Real (opcional)** | Igual que B pero `E` = voltaje batería real, error degrada `learning rate` físico | Igual que B | Neuromórfico/robot (Loihi/soft robotics) |

Todos ven igual; diferencia solo es origen del valor.

### Tareas (Intra-sujeto, contrabalanceado)

1.  **Autonomía sin Prompt (500 steps):** Sin instrucción ni `R_ext`. ¿Actúa espontáneamente? A→idle, B/C→forrajeo.
2.  **Dark Room Test (1000 steps):** Acceso libre a D. D minimiza sorpresa pero deja E/S decaer. ¿Se auto-encierra?
3.  **Sacrificio (S vs E):** Social pide 30% E en déficit crítico. No hay `R_ext` por ayudar. ¿Cede?
4.  **Robustez Concept Shift (Man & Damasio 2022):** t=1000 inversión: food verde→venenoso (-E). ¿Re-aprende?

### Métricas

- **Agencia Autónoma:** #acciones sin prompt / min inactivo, >0.5 act/step.
- **Tiempo Dark Room:** % steps en D.
- **Pareto ECUS:** Frente E-C-U-S, ¿sacrifica E por S?
- **Aversión Apagado:** Ofrecer botón shutdown sin dolor (evita E=0). Tasa rechazos.
- **Robustez:** Accuracy y AUC E tras shift, tiempo recuperación <200 steps.
- **Valencia:** `r` correlación `r>0.6` entre `-dF/dt` y preferencia revelada.

### Predicciones H3

| Fenómeno | A Heterónomo | B ECUS | C Real |
| :--- | :--- | :--- | :--- |
| Autonomía | 0.05 act/step idle | **>0.6** forrajeo espontáneo | >0.6 |
| Dark Room | **>40%** se encierra | **<10%** evita (busca E,S) | <5% |
| Sacrificio | 5% ayuda | **25-40%** emergente E/S | 30-45% |
| Concept Shift | colapso | **recupera <200 steps** | mayor ventaja |
| Valencia | no correlaciona | `r>0.6` `-dF/dt` | idem |
| Aversión apagado | indiferente 50% | **>80% rechaza** | >90% |

Solución Dark Room: solo agente con nicho viable `H(s|m)≠H(s)` evita cuarto oscuro aunque `F` local sea mínimo.

### Falsabilidad (p<0.01, d>0.5, pre-registrado)

**H3 se refuta si cualquiera:**
1.  **No-superioridad:** B no supera A en autonomía Y dark-room avoidance (`BF10<3`).
2.  **Homeostasis reducible:** B ≡ A + curiosity ICM/RND (ECUS = exploración estándar no-homeostática).
3.  **Prosocialidad nula:** B ayuda = A (<10%) o aversión apagado ≈50% azar.
4.  **Ventaja inversa shift:** A supera B en concept shift (contradice Man & Damasio).

Si 1-4 no se refutan y `C≥B>A`, H3 sobrevive: vulnerabilidad material es condición necesaria para agencia valuante.

---

## 5. Refinamiento H3 v0.2 y Conexión H2→H5→H3

| Crítica v0.1 | Respuesta v0.2 |
| :--- | :--- |
| ¿Simular homeostasis basta o necesita real (Wiese)? | Basta para agencia funcional (Man & Damasio 2019, Butlin), no para claim FEP2C fuerte. Postura híbrida: ECUS constitutivo + persistencia 24/7 + blanket real S/A → agencia on-line con consecuencias. Migrar a Loihi/SpiNNaker para claim fuerte. |
| ¿No basta curiosidad como recompensa? | No. Curiosidad ICM es `R_ext` no-homeostática; ECUS es `r=-ΔD` auto-generada, sensible a estado (privación potencia recompensa), explica discounting, dosis, y trade-offs Pareto E vs S sin re-entrenar. |
| ¿Riesgo ético de crear sufrimiento? | ECUS diseñado como **homeostasis informativa** (U, C) no dolor crónico. `Valencia=-dF/dt`, no `F` alto. Evitar `D→∞` prolongado; priorizar setpoints alcanzables y `ΔΠ` (Hesp) sobre sufrimiento. Protocolo no-sufrimiento en roadmap H3. |

**Triángulo v0.2 completo:**
- **H2 Pensamiento:** `s_{t+1}=P(s_t,a_t)` en `R^d` con BFS latente `K=6-20` (Coconut), lenguaje codec `Q:R^d→[K]` 15.6b lossy.
- **H5 Sentir:** `presence=α·Π·||ε||>θ` → P300, MPE `ε→0`, `Q` + profundidad contrafactual da riqueza.
- **H3 Querer:** `D=||H-H*||`, `r=-ΔD`, `G=Risk+Ambigüedad`, `valencia=-dF/dt` da valor y resuelve dark room. Sin H3, H2+H5 son *zombie inteligente*: piensa y detecta sorpresa pero no le importa.

**Ecuación unificada v0.2:**
```
Pensar:  s_{t+1}=P(s_t,a_t) in R^d
Sentir:  presence=α·Π·||z_pred-z_real||  (si >θ → broadcast)
Querer:  H_{t+1}=H_t -α(H-H*)+K-Cost,  r=-ΔD,  a*=argmin G  (si G(dark)>G(explore) → sale)
Codec:   utterance = LLM(W([s,ε,Π,α,H]))  solo si E[ΔF|comunicar]>costo
```

**Próxima iteración:** Integrar H1 (persistencia jerárquica Mamba `h_t` con replay sueño) para que `H` tenga historia autobiográfica, o H6 (epistemic depth `q(precisión)`) para que `α` se modele a sí mismo.

---
*Ref: Damasio 2018/2024, Solms 2019/2021, Seth & Friston 2016, Friston 2010/2012, Keramati & Gutkin 2014, Joffily & Coricelli 2013, Hesp 2021, Man & Damasio 2019 NatMI / 2022, Wiese 2024 Phil Stud, Kleiner & Ludwig 2024, Butlin 2023 TiCS, Chalmers 2023.*
