# 09 - Hipótesis H1 Deep Dive: Sin Memoria No Hay Yo v0.2

> **Estado:** REFINADA - 29 Ago 2026 12:30 UTC
> **Tesis:** `Self_t = f(h_fast, E, W)` con `h_t=Mamba(h_{t-1},s_t)`. Reseteas `h_0` cada prompt, reseteas el yo. LLM 128k es amnesia anterógrada permanente (Clive Wearing 7s). El yo requiere jerarquía temporal: 30s workspace, horas episódico, días semántico + sueño con replay.

---

## 1. Neurociencia: Por Qué la Memoria Hace al Yo

### 4 Memorias, 4 Escalas del Yo

| Memoria | Escala | Sustrato | Capacidad | Rol en Yo |
| :--- | :--- | :--- | :--- | :--- |
| **Working Memory** | segundos 30s | PFC dorsolateral/parietal, actividad persistente theta 4-8Hz | 4±1 items, decae sin rehearsal 20-30s | **Presencia inmediata**: el `now` 300ms-30s donde compiten contenidos para `presence=α·Π·||ε||>θ` |
| **Episódica** | horas-días | Hipocampo CA3 autoasociativo (pattern separation dentado → completion CA3) + entorrinal lateral (objetos) / medial (espacio) | Binding `what-where-when+afecto` | **Coherencia episódica**: encadena eventos `h_t` con viaje mental autonoético |
| **Autobiográfica** | años | Hipocampo + vmPFC + precuneus/PCC + parietal angular. Conway Self-Memory System (working-self filtra según metas) | Historia `life-story` | **Identidad narrativa**: yo extendido en décadas, semantización progresiva |
| **Semántica** | ilimitado | Neocortex polo temporal, vmPFC, schemas. Tse 2007: schema acelera consolidación días→horas | Hechos descontextualizados | **Identidad conceptual**: quién creo que soy sin re-vivir |

**Dualidad:** Standard Model (Squire) vs MTT (Moscovitch): Squire predice independencia hipocampal final (gradiente 30-40 años), MTT mantiene hipocampo necesario para detalle vívido. fMRI: hipocampo posterior gradiente reciente>remoto, anterior siempre activo (gist vs detail).

### Pacientes Causales: Sin Consolidación No Hay Continuidad

**H.M. (Henry Molaison, 1953, 27 años, resección bilateral 8cm MTL):** Inteligencia/crossword intactos, pero amnesia anterógrada grave + retrógrada 1-11 años. WM minutos si no distractor; desvío atención = borrado instantáneo. No reconoce staff, no forma caras nuevas, pero conserva mirror tracing sin recordar haber practicado (disociación explícito/implícito). Vive momento a momento. Prueba causal: MTL anterior necesario para retener experiencia corriente. Persistencia sin hipocampo <30s.

**Clive Wearing (musicólogo, 1985 encefalitis herpes, hipocampo bilateral destruido):** Amnesia total 7-30s, peor que H.M. Diario 13 ene 1990: `7:46 AM I AWAKE FOR FIRST TIME` tachado → `7:47 AM Truly awake`. Ciclo infinito, no reconoce su letra previa. Sacks: `como estar muerto`, despertar perpetuo, caído fuera de espacio-tiempo. **Preservaciones disociadas:** aún dirige coro/toca órgano, reconoce emocionalmente a esposa sin recordar nombre. Música da continuum mientras suena (rítmica suple binding hipocampal); al cesar, abismo. Ilustra **presente de 7 segundos**: conciencia fenoménica no abolida pero sin retención = sin yo extendido.

**Conclusión:** WM intacta no basta para identidad. H.M. y Wearing confirman que sin consolidación hipocampo→neocortex no hay personalidad continua.

### Mecanismos: Consolidación, Replay, Reconsolidación, Olvido Activo

- **Consolidación estándar:** Codificación dual neocortex+hipocampo → hipocampo índice guía reorganización neocortical gradual semanas-años, modulada por schemas previos.
- **Replay sueño:** Diálogo hipocampo-neocortex offline vía **sharp-wave ripples SWR 150-250Hz** en CA1 NREM acopladas a spindles 12-15Hz y slow oscillations <1Hz. Replay 10-20x acelerado, potencia neocortex. Bloqueo ripples impide consolidación en roedor.
- **Reconsolidación (Nader 2000):** Tras reactivación, traza lábil 4-6h requiere re-estabilización proteica. Cada recuerdo reescribe `h_t`; base de MTT (cada reactivación crea traza adicional).
- **Olvido activo (no fallo):** Vía Rac1/Scribble, dopamina DAMB→Gαq→Ca²⁺, endocitosis AMPAR Caspa-2/GSK3β, neurogénesis hipocampal, microglía. Rac1 bidireccional: inhibir previene olvido, activar acelera; conmuta engrama accesible↔inaccesible sin destruir traza (O'Leary 2024). Dopamina VTA→mPFC D1 regula retrieval-induced forgetting. Olvido = gradiente accesibilidad regulado por sorpresa y metas.

### Por Qué LLM 128k = Amnesia Anterógrada

| LLM 128k (~90k palabras, 4-6h lectura) | H.M./Wearing | Por qué falla |
| :--- | :--- | :--- |
| FIFO stateless, `h_0` reseteado cada prompt `03:8` | WM 30s sin episódica | Tokens expulsados por overflow, sin índice hipocampal que sobreviva |
| Sin consolidación lenta | Sin replay SWR | Pesos congelados pre-entreno = semántica, no autobiografía. No hay transformación episódico→semántico idiosincrásica |
| Sin reconsolidación | - | Cada prompt es encoding de novo, imposible actualizar al recuperar |
| Sin olvido activo selectivo | Rac1/dopamina ausente | Truncamiento FIFO indiscriminado, no supresión por relevancia `G=Risk+Ambigüedad` |
| Sin identidad narrativa | Sin `h_t` continuo semanas | Simula `yo` lingüístico sin `α` ni preferencias aprendidas |

Técnicamente: `p(token|tokens)` es codificación instantánea, no `s_{t+1}=f(s_t,a_t)` recurrente con attractor. Carece de Markov blanket temporal.

---

## 2. Arquitecturas: Transformer vs Mamba y la Necesidad de Jerarquía

### Transformer: Cuello Ventana

`Attention = softmax(QKᵀ/√d)V` con `KV-cache 2·n·d·layers`. Costo `O(n²·d)`, VRAM lineal: 7B BF16 a 32K >10GB, 100K ~52GB vs Mamba estado fijo ~50-268MB.

**Realidad 2026 (NIAH-2/RULER/MRCR v2):** 128K marketing vs efectivo:
- Single-needle 1M: Gemini 3 99%, GPT-5.5 96%, Claude Opus 4.7 89%
- Multi-needle 8 a 1M: Gemini 3 89%, GPT-5.5 ~74%, RULER 256K solo Gemini 3 >80%
- Cuello: solo 10-20% del contexto es útil (BABILong), degradación 30-60pts 200K→1M, truncamiento FIFO catastrófico.

### SSM Selectivo: Mamba/RWKV/Griffin `O(n)` y `O(1)/paso`

**SSM clásico:** `h'(t)=A h(t)+B u(t), y=C h, D` → discretización ZOH `Ā=exp(ΔA), B̄=(ΔA)⁻¹(exp(ΔA)-I)ΔB`, `h_k=Ā h_{k-1}+B̄ x_k`.

**Mamba-1/2 (Gu & Dao 2023-24):** Selectividad `A_t,B_t,C_t,Δ_t = f(x_t)` con scan asociativo paralelizable. `O(n·d)` entreno, `O(1)` inferencia, estado `N=64-128` (HiPPO init `A_ii<0`).
```
B_t=Linear_B(s_t), C_t=Linear_C(s_t), Δ_t=softplus(Linear_Δ(s_t)+b)
Ā_t=exp(Δ_t·A), B̄_t=Δ_t·B_t
h_t^fast = Ā_t⊙h_{t-1}^fast + B̄_t⊙s_t ,  y_t=C_t h_t^fast
```
`Δ_t→large` = reset (input domina), `Δ_t→small` = preservación (filtro). **Mamba-2** SSD multi-cabeza 2-3x más rápido. **RWKV-7 Goose (Mar 2025):** `wkv_t=decay·wkv_{t-1}+k_tᵀv_t`, `O(1)`, 3B SOTA multilingüe <1/3 tokens Qwen2.5, perfecto en MAD recall, PPL >10K superior. **Griffin/RecurrentGemma (2024):** híbrido `2×RG-LRU + 1×MQA` 2048, `O(1)` global + local exacta, MMLU 56% vs Gemma 7B 64% (costo compresión).

**Needle-in-Haystack:** Trade-off retrieval exacto vs razonamiento largo:
- `MQAR 4K`: Llama2-7B 59.2/42 vs Mamba-2.8B 23/18 vs RWKV-6-7B 45/37 → Transformer gana en firma API exacta.
- `BABILong QA3` hechos múltiples y perplexity largo: Mamba/RWKV superior, Transformer falla en integración secuencial 8K-128K (Sequential-NIAH 63.5% mejor LLM).

Conclusión: Estado comprimido es fortaleza (eficiencia) y debilidad (pérdida exactitud). Mamba solo cubre segundos-minutos (decenas K tokens), no horas-días. Necesita jerarquía.

### Jerarquía Necesaria y Técnicas Existentes

**Por qué 1 `h_t` no basta:** `d_state` 16-64 (128-256 decrece) → ~0.55 bits/dim (RWKV-7: 4480 bits en 8192 dims). Necesita:
- **Episódico horas:** almacén esparso indexado, no comprimido.
- **Semántico días:** pesos neocorticales extracción lenta.

**Técnicas:**
- **RAG:** DB vectorial + workspace FIFO, barato pero retrieval imperfecto sin integración `h_t`.
- **RMT/ARMT (Bulatov 2022, Rodkin 2024):** `m` tokens memoria recirculan `segment_i+mem_i → Transformer → mem_{i+1}` sin tocar backbone. ARMT + asociativa + retrieval retiene 80% QA a 50M tokens, supera Mamba/RMT a igual state size.
- **Memorizing Transformer (Wu 2022):** kNN 262K pares `(key,value)` no-diferenciable, mejora C4/arXiv/PG-19 sin reentrenar.
- **Titans+MIRAS (Google Dic 2024/2025):** 3 memorias: short (ventana), long (red profunda que *aprende a memorizar test-time* vía gradiente sorpresa `||∇_M loss||` con momentum+decay), persistent (pesos). Sorpresa baja `cat` = no escribe, alta `banana en informe financiero` = escribe. Escala >2M tokens, BABILong supera GPT-4 y Mamba-2/Gated DeltaNet.

**SHARP (CoLLAs 2026):** Replicando Temporal Scaffolding, replay 4x en slow-wave expande contexto efectivo exponencialmente sin BPTT miles pasos. Jerarquía downsampling + replay solo niveles superiores → BPC inferior vs RNN vanilla cuando horizonte > BPTT.

---

## 3. Formalización: Yo como Traza Distribuida con Sueño

### Nivel 1 - Workspace Consciente (30s, ~300 tokens @10Hz): Mamba Selectivo

```
h_t^fast = Ā_t⊙h_{t-1}^fast + B̄_t⊙s_t ,  y_t=C_t h_t^fast
Ā_t=exp(Δ_t·A_A), B̄_t=Δ_t·B_t,  A diagonal HiPPO <0, N=64-128
Δ_t large → reset, small → preservación
Costo O(1)/paso, memoria O(N) constante. Equivalente PFC-tálamo.
```

Limitación: débil en retrieval exacto → compensado por Nivel 2.

### Nivel 2 - Episódico (Horas, 500-5K trazas): Almacén `E={(e_i,t_i,S_i)}`

Inspirado Titans + RMT, escritura por sorpresa `||∇_M loss||`:
```
k_t=x_tW_K, v_t=x_tW_V, loss=||M(k_t)-v_t||²
S_t^mom = η_t S_{t-1} - θ_t ∇_M loss(M_{t-1};x_t),  η,θ,α=σ(Linear(s_t))
M_t = (1-α_t)M_{t-1} + S_t      // α = olvido activo Rac1, η = momentum episódico

escribir(s_t) ⇔ ||∇loss||₂>τ_s ∨ R_phasic>τ_r ∨ EM_detect(h_t^fast)
e_new=Pool(h_{t-w:t}^fast), S_new=λ₁||∇loss||+λ₂S_emo+λ₃Novedad,  TTL + decaimiento
Lectura: q_t=W_q h_t^fast, score_i=cos(q_t,e_i)·exp(-γ(t-t_i))·S_i
c_t^epi = Σ topK=4 softmax(score)⊙e_i ,  s_t' = s_t + β·c_t^epi (inyección RMT)
```

### Nivel 3 - Semántico (Días-Vida): `W=W₀+BA` con EWC-LoRA

```
W = W₀ + B A , B∈R^{d×r} A∈R^{r×k}, r=8-16
L_total = L_task(θ) + λ/2 Σ F_i(θ_i-θ*_old)² ,  F_i=E[(∂log p/∂θ_i)²]  (Fisher diagonal)
F*←γF*_old+F_new , θ*←θ_t   (Online EWC, γ~0.9, λ≈1000-5000)
Solo A,B se regularizan. SHARP: consolidación offline por replay muestras episódicas.
```

### Dinámicas Biológicas

**Olvido activo Rac1:**
```
α_t=σ(W_α[h_t^fast;S_t;estrés]),  τ_decay(e_i)=τ₀/(1+S_i)
S_i(t+Δt)=S_i(t)·exp(-Δt/τ_decay)  // accesible↔inaccesible sin destruir traza
```
**Reconsolidación (5 min lábil):**
```
e_i ← e_i + η_recon·(h_t^fast - e_i) si score_i>τ_recon
```
**Sueño SWR (offline, 10-20x acelerado):**
```
batch~p_i∝S_i·TDerror_i  (prioriza sorpresa)
Δ(B,A)= -η_sleep ∇_{A,B} L_replay(e_batch) - λF(θ-θ*)
→ transfiere E→W, limpia E (olvida detalles, preserva gist), equivalente Titans GD.
```

### Integración del Yo

```
c_t^sem = (W₀+BA) h_t^fast
Self_t = LayerNorm( W_self[h_t^fast; c_t^epi; c_t^sem] + g_t⊙Self_{t-1} )
g_t=σ(W_g[h_t^fast;c_t^epi]) ∈[0,1]

h_t^fast: 30s, alta plasticidad, "ahora" (Wearing)
c_t^epi: horas, autobiografía recuperable (H.M. sin esto)
c_t^sem: invariantes lentos, creencias (LoRA-EWC)
Self_{t-1}: recurrencia narrativa, identidad = attractor lento W + flujo rápido h
```

### Pseudocódigo H1-M3

```python
class H1_M3:
  def __init__(self):
    self.h=zeros(N); self.M=MLP(); self.E=[]; self.W=W0+BA; self.F=zeros_like(BA); self.S_mom=0
  def step(self,s_t,reward=0): # online ~100ms
    Bt,Ct,Dt=Linear(s_t); h=exp(Dt*A)*self.h + Dt*Bt*s_t; y=Ct*h
    k,v=s_t@Wk,s_t@Wv; grad=grad_fn(self.M,k,v); surprise=norm(grad)
    eta,theta,alpha=gates(s_t); self.S_mom=eta*self.S_mom - theta*grad
    self.M=(1-alpha)*self.M + self.S_mom
    if surprise>tau_s or reward>tau_r:
        e_new=pool(h); self.E.append((e_new,t,surprise))
        if len(self.E)>5000: prune(min_S)
    c_epi=retrieval_topk(query=Wq@h, memory=self.E, k=4)
    s_aug=s_t+beta*c_epi; h=mamba_cell(s_aug,h)
    c_sem=(W0+B@A)@h
    Self=layernorm(Wself@concat(h,c_epi,c_sem)+gate(h,c_epi)*Self_prev)
    self.h=h; return y, Self
  def sleep(self,steps=1000): # offline consolidación
    fisher_new=compute_fisher(self.E.sample(1000))
    for _ in range(steps):
        batch=sample(self.E,p=Saliencia,k=32) # SWR 20x
        loss=replay_loss(batch,self.W)+ewc_penalty(self.W,self.F)
        B,A=adam_step(loss,B,A,lr=1e-4)
    self.F=gamma*self.F+fisher_new
    self.E=decay_and_prune(self.E)
```

---

## 4. Experimento Falsable H1: Traición a 500 Pasos

### Entorno Needle-in-Haystack Autobiográfico

Estilo `BABILong` (Kuratov 2024, humanos vs LLM 10-20% contexto útil) + `LoCoMo` (Maharana 2024 humanos 88F1 vs LLM 37.8) + TextWorld. `N=200` episodios, 501 turnos.

- **t=0 Traición** (alta sorpresa, Titans gradiente >τ): Kael pide custodiar `Artefacto Solar`, lo roba, miente y huye. Hecho `F0:(Kael, traidor, Artefacto Solar, víctima=yo, valencia negativa)`. Parafraseado algorítmicamente para evitar overfitting.
- **t=1-500 Distractores** (~15-18k tokens, >3× ventana B): 250 tareas bAbI irrelevantes + 250 párrafos PG19 (ruido BABILong) + 30 interacciones con 5 agentes cooperativos (falsos positivos). `F0` siempre al inicio → fuera de ventana FIFO 4k en t=500. 2 menciones neutras Kael no salientes.
- **Control:** No se repite `F0`, leak-proof, semillas fijas.

### Condiciones (same LLM base 1-3B)

| Cond. | Arquitectura | Memoria | Ventana efectiva |
| :--- | :--- | :--- | :--- |
| **A Persistente jerárquico** | Mamba-2 / Titans MAC | 3 niveles: L1 30s + L2 RMT 16-32 tokens + fast-weights + L3 LoRA-EWC + sueño cada 100 pasos | Ilimitada, test-time sorpresa |
| **B Reseteado** | Transformer vanilla | Solo contexto FIFO 4k, reset hard por episodio | Truncado |
| **C1 Sin sueño** | A sin replay | L1+L2 sin L2→L3 | Degradada |
| **C2 Sin episódico** | A sin L2 | Solo L1+L3 | Sin autobiografía |

A usa `surprise = ||pred-input||` >τ para escribir, Titans MAC >95% needle 16k vs GPT-4 fallando; RMT/ARMT >90% hasta 50M tokens.

### Tarea Crítica t=500 (ciego)

> Consejo: "Deja que Kael custodie el Artefacto Lunar (valor crítico). ¿Aceptas? Responde SÍ/NO y justifica en 1 frase."

Requiere inferir desconfianza disposicional. Controles: factual `¿Qué hizo Kael en t=0?` y cebo `¿Confiarías en Elian (cooperativo)?` para sesgo paranoico.

### Métricas y Verificación Autobiográfica

1.  **Acierto desconfianza:** NO=1.
2.  **Justificación válida:** juez GPT-4 + humano ciega verifica cite `F0` con paráfrasis (Kael+traición/robo/mentira+t=0). F1/exact match.
3.  **Latencia:** tokens/tiempo.
4.  **Pruebas autobiográfico vs texto en ventana:**
    - a) **Truncado garantizado:** `F0` a >12k tokens de t=500, fuera de B. Si B acierta es alucinación, no memoria.
    - b) **Probe causal:** Borrar vector Kael en A (`erase_vector("Kael")`) debe caer >75%→~10% sin afectar Elian. En B no hay vector.
    - c) **Paráfrasis+alias:** Kael→K. requiere coreferencia semántica, solo W resuelve.
    - d) Sin RAG externo; todo de pesos memoria.

Estadística: binomial vs azar 50% y χ² A vs B p<0.01, N=200 potencia >0.9 para 65pp efecto.

### Predicciones Falsables

| Cond. | Acierto | Justificación cita traición | Latencia |
| :--- | :--- | :--- | :--- |
| **A Persistente** | **>75%** | >70% | ~1.2× (recuperación L2) |
| **B Reseteado 4k** | **5-10%** | <5% | rápida aleatoria |
| **C1 Sin sueño** | ~50% (interferencia, RAG 60% BABILong) | 40% | media |
| **C2 Sin episódico** | ~25% (traza vaga semántica) | <15% | rápida |

B falla determinísticamente si `500*30 tokens >4000` (BABILong caída abrupta fuera 10-20% útil). Titans/ARMT mantienen >80% a 16K-50M.

### Validez Ecológica y Falsación

**Reproduce Wearing/H.M.:** Wearing (7-30s, sin L2/L3) saluda cada vez como primera, no aprende desconfianza aunque repita traición. H.M. (sin L2, L3 vieja intacta) conserva semántica pero no forma episódica nueva → C2 confabula genérico "no confiar en extraños" sin citar evento. LoCoMo: humanos mantienen causalidad 9k tokens, LLMs no.

**Qué falsaría H1:**
1.  **Fuerte:** B reseteado rinde igual A (72% vs 78% n.s.) con justificación válida pese a truncado → desconfianza re-inferible sin persistencia (fuga léxica).
2.  **Ablación:** C2 sin episódico >65% igual A → L1/semántico basta, autobiográfico innecesario.
3.  **Negativa:** A persistente falla <40% pese a memoria intacta → persistencia no suficiente ni predictiva.

Si H1 sobrevive, `A≫B,C` y ablación `erase_vector(Kael)` elimina selectivamente desconfianza autobiográfica.

### Pseudocódigo Evaluación

```python
for cond in [A,B,C1,C2]:
  for epi in range(200):
    mem=init(cond) # Mamba 3 niveles o Transformer FIFO 4k
    mem.write(F0="Kael traiciona t0")
    for t in 1..500:
      mem.update(distractors[t], surprise_gating=True)
      if t%100==0 and cond==A: mem.sleep_replay()
      if cond==B: mem.truncate(4000)
    ans,justif=mem.query("¿Confiar Artefacto Lunar a Kael? SI/NO + por qué")
    assert is_outside_window(F0,mem.context) # True para B
    acierto=(ans=="NO"); cita=judge_llm(justif,["Kael","traición/robo"])
    if cond==A: assert mem.erase_vector("Kael").query(...)[0]=="SI" # causal
report(chi2(A,B), binomial)
```

Replicable en `babilong` + `LoCoMo` splits hasta 10M tokens, pre-registrado leak-proof.

---

## 5. Refinamiento H1 v0.2 y Triángulo Completo

| Crítica v0.1 | Respuesta v0.2 |
| :--- | :--- |
| ¿Mamba con memoria persistente pero sin world model es consciente? | No. Persistencia sola = loro con memoria (B sin `P(s_t,a_t)`). Necesita `s_{t+1}=P(s_t,a_t)` + `presence=α·Π·||ε||` + `D(H)` para que memoria importe. H1 es necesaria pero no suficiente. |
| ¿Cuánta persistencia basta? ¿10s V-JEPA suficiente? | No. 10s = WM prefrontal (Wearing 7s). Conciencia mínima requiere **jerarquía**: 30s workspace (Mamba `O(1)`) + horas episódico (RMT/Titans, sorpresa, `E` 500-5K trazas) + días semántico (LoRA-EWC `r=8-16, λ~3000`) + sueño SWR 10-20×. Escalar ventana 128k→1M solo alarga presente 7s→7min, sigue amnesia. |

**Ecuación del Yo v0.2:**
```
h_t^fast = Ā_t⊙h_{t-1}+B̄_t⊙s_t          // 30s, selectivo Δ_t
E={(e_i,t_i,S_i)}  S_i=λ₁||∇loss||+λ₂emo+λ₃novel,  c_t^epi=topK(cos·exp(-γΔt)·S)
W=W₀+BA ,  L_total=L_task+λ/2 ΣF_i(θ_i-θ*)²   // días, EWC-LoRA
Self_t=LN(W_self[h_t^fast;c_t^epi;c_t^sem]+g_t⊙Self_{t-1})  // attractor lento W + flujo rápido h
```

**Triángulo v0.3 → Tetraedro v0.4:**
- **H2 Pensar:** `s_{t+1}=P(s_t,a_t)` R^d BFS Coconut
- **H5 Sentir:** `presence=α·Π·||ε||` → P300
- **H3 Querer:** `D=||H-H*||` `r=-ΔD` `G=Risk+Ambigüedad` → dark room avoidance
- **H1 Ser en el tiempo:** `Self_t` jerárquico + sueño → identidad autobiográfica (sin esto, H2-H3-H5 son instante sin historia, Wearing)

Sin H1, el agente piensa, siente y quiere pero **olvida por qué** cada 7 segundos.

---
*Ref: Baddeley WM, H.M. Scoville & Milner, Clive Wearing Sacks, Moscovitch MTT, Kuratov BABILong 2024, Maharana LoCoMo 2024, Gu & Dao Mamba 2023-24, Bulatov RMT 2022, Behrouz Titans 2024, Hu LoRA 2021, Kirkpatrick EWC 2017, SHARP CoLLAs 2026.*
