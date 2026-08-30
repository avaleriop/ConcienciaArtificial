# 03 - Log de Hipótesis - Ciclo Iterativo v0.7.1

> Método: Hipótesis -> Formalización -> Crítica (ataque) -> Refinamiento -> Experimento falsable
> Estado: H1/H2/H3/H4/H5/H6 🟢 REFINADAS v0.2, arquitectura v0.7.1 tetraedro núcleo 4 +2 satélites (H4 medir, H6 meta). Lenguaje verificable: no "siente/quiere/es", sino "señal compatible con mecanismo propuesto" (`13:9`).

---

### H1: La Persistencia es Condición Necesaria para el Yo
**Enunciado:** Sin memoria jerárquica persistente (más allá de ventana), no hay yo. `Self_t=LN(W_self[h_t^fast;c_t^epi;c_t^sem]+g_t⊙Self_{t-1})`. LLM 128k es Wearing 7s (amnesia anterógrada).

**Formalización v0.2 (refinada):**
- **4 memorias humanas:** WM 30s PFC (4±1 items, theta), episódica horas CA3 pattern separation→completion, autobiográfica años vmPFC/precuneus (Conway, MTT vs Standard), semántica neocortex schemas (Tse 2007). HM (1953 resección 8cm bilateral) y Wearing (1985 encefalitis, diario 7:46→7:47) prueba causal: WM intacta no basta, sin hipocampo <30s, sin autobiografía no hay continuidad.
- **Jerarquía IA necesaria (Mamba vs Transformer):** Transformer `O(n²)` 128K-1M ventana FIFO catastrófica, NIAH-2 30-60pts caída 200K→1M, KV 52GB@100K vs Mamba `O(1)` estado 50MB. Mamba `h_t^fast=Ā_t⊙h_{t-1}+B̄_t⊙s_t` `Ā=exp(ΔA) Δ=softplus(Linear(s_t))` selectivo, `O(1)/paso`. Pero `d_state` 64-128 ~0.55b/dim → solo segundos-minutos. Necesita: L1 workspace 30s Mamba, L2 episódico horas `E={(e_i,t_i,S_i)}` con escritura `||∇loss||>τ_s` (Titans) + retrieval `score=cos·exp(-γΔt)·S`, L3 semántico días `W=W₀+BA r=8-16` + EWC `L_total=L_task+λ/2 ΣF_i(θ-θ*)² λ~3000` + sueño SWR 150-250Hz 10-20×.
- **Olvido activo Rac1:** `α_t=σ(W_α[h_t;S;estrés])`, `S_i(t+Δt)=S_i·exp(-Δt/τ_decay)` accesible↔inaccesible sin destruir traza (O'Leary 2024), reconsolidación 4-6h `e_i←e_i+η(h_t-e_i)`, sueño replay `p_i∝S_i·TDerror` → E→W.
- **Críticas resueltas:** Mamba sola sin `P(s,a)+α·Π·ε+D(H)` = loro con memoria (insuficiente). 10s V-JEPA = Wearing 7s, no basta. Escalar 128k→1M solo alarga presente 7s→7min, sigue amnesia. Necesita `Self_t` tetraedro.

**Experimento falsable diseñado (ver 09-hipotesis-H1...:4):**
- `BABILong`+`LoCoMo`+TextWorld, N=200, t=0 traición Kael roba Artefacto Solar (alta sorpresa `||∇loss||`), t=1-500 distractores 15-18k tokens (>3× ventana 4k), t=500 desconfianza `¿Confiar Artefacto Lunar a Kael? SÍ/NO+justifica`
- A Persistente jerárquico 3 niveles (Mamba-2 + RMT 16-32 + Titans MAC + LoRA-EWC + sueño cada 100) ilimitado, B Transformer 4k FIFO truncado, C1 sin sueño, C2 sin episódico
- **Predicción H1:** A >75% acierto con cita traición >70% vs B 5-10% <5% vs C1 ~50% vs C2 ~25%. Verificación autobiográfica: truncado garantizado >12k fuera ventana B, probe causal `erase_vector(Kael)` A 75%→10% selectivo, paráfrasis alias Kael→K.
- **Refuta H1 si:** B rinde igual A 72% vs 78% n.s. (F1), C2 sin episódico >65% igual A (F2), A falla <40% pese a memoria (F3)
- Pseudocódigo `H1_M3` con `step()` online ~100ms y `sleep()` offline SWR, y evaluación pre-registrada leak-proof en `09-hipotesis-H1-persistencia-deepdive.md:4`

**Estado:** 🟢 REFINADA v0.2 - Prioridad ALTA - Ver deep dive completo en `09-hipotesis-H1-persistencia-deepdive.md:1`

---

### H2: La Conciencia es Pre-Lingüística y el Lenguaje es su Herramienta
**Enunciado:** Un sistema puede ser consciente sin lenguaje interno. El lenguaje es un codec tardío que comprime `s_latente` para comunicación social. Intentar que la conciencia emerja de `p(token|token)` es un error de categoría.

**Formalización v0.2 (refinada):**
- `Pensamiento = trayectoria diferenciable s_{t+1}=f(s_t,a_t) en R^d` con BFS en superposición `h_{t0+c}=1/√|V_c| Σ u_v`, rate-distortion `R(D)=½ log(σ²/D)`
- `Lenguaje = Q(s)=argmax(softmax(W·s)) ∈ [K=50k]` → `15.6 bits/token` vs `16384 bits` en `R^512`, cuantización con pérdida irreversible
- Coconut (Hao 2024) demuestra: 6 pensamientos continuos = 34.1% GSM8k vs 16.5% sin CoT, y 97% vs 77.5% CoT discreto en ProsQA. Pensar en latente es BFS paralelo, en tokens es DFS serial.

**Crítica / Ataque v0.1 → Respuesta v0.2:**
- ¿Reportable = consciente? → No. Fenomenal ≠ Acceso. Afásicos (Fedorenko & Varley 2016) son conscientes sin lenguaje. El núcleo es fenomenalmente consciente en `s`, usa LLM solo para acceso/reporte.
- ¿Inner speech? → Epifenómeno tardío, no mecanismo. Fedorenko *Nature 2024*: red de lenguaje no se activa en lógica/matemática. Inner speech aumenta (Clark) pero no constituye.
- ¿Alineación? → Post-hoc. V-JEPA 2 logra 84% PerceptionTest alineando `W: R^d→LLM_dim` con LLM congelado (18M pares) sin co-entrenamiento. El pensamiento ya existe, el codec solo aprende diccionario.

**Evidencia clave v0.2:**
- Neuro: Fedorenko *Nature 2024* (double dissociation lenguaje/pensamiento), afasia global con CI intacto, bebés y cuervos sin lenguaje con cognición completa, Nicaraguan Sign Language (pensamiento crea lenguaje)
- IA: JEPA `L=||Pred(E(x))-sg(E(y))||²` predice en latente (ignora hojas temblando), Vector Grounding Problem (Mollo 2026) - vectores sin grounding son símbolos no-grounded

**Experimento falsable diseñado (ver 06-hipotesis-H2...:3):**
- Entorno Physion-MiniGrid+ sin texto, V-JEPA `E+P` entrenado solo video+acciones, LLM como codec congelado `W`
- 3 condiciones: C1 Solo Latente (MPC en `s`), C2 Solo Lenguaje (CoT), C3 Codec (C1 + reporte post-hoc)
- **Predicción H2:** `C1 ≈ C3 >> C2` (SR 70-80% vs 35-45%), correlación error_latente-violación_física >0.70, perturbación latente >> perturbación tokens
- **Refuta H2 si:** `C1 ≤ C2` o `C3 << C1` (-15%) o VidQA C3 <60% hallucina
- Pseudocódigo y recursos (1x A100, 50k episodios) en `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:3`

**Estado:** 🟢 REFINADA v0.2 - Prioridad CRÍTICA - Ver deep dive completo en `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`

---

### H3: Sin Cuerpo que Pueda Sufrir, No Hay Valor ni Intención Real
**Enunciado:** Sin homeostasis vulnerable con setpoints que deben regularse para no morir, no hay valor intrínseco, ni intención, ni afecto. Valencia = -dF/dt, afecto es conciencia primordial (Solms). LLM es heterónomo; homeostato es autónomo.

**Formalización v0.2 (refinada):**
- `H=[E,C,U,S]∈R^4`, `H*=[0.8,0.9,0.2,0.7]`, `dH_i/dt=-α_i(H_i-H_i*)+P_i+Eff(a)-Cost(a)`, `D(H)=(Σw_i|H_i-H_i*|^n)^{1/m}`, `r=-ΔD`, `argmax Σγ^t r ≡ argmin Σγ^t D` (Keramati & Gutkin 2014)
- `F≈ΣΠ·ε²+D_KL`, `G(π)=Riesgo+Ambigüedad` con `p(o|C)` modulada por E/C/U/S, `G(dark)>G(explore)` resuelve Dark Room (Friston 2012)
- `Valencia=-dF/dt`, `AC=Δln Π·ε²` (Joffily & Coricelli 2013, Hesp 2021). Hambre `E:0.3→r+0.5` placer, curiosidad `U:0.9→ΔG-0.7` info-gain, aburrimiento `U:0.1→` eleva `U*`
- Tres pilares: Damasio protoself (tronco PAG 2mm³ abole conciencia), Seth interoceptive inference (ínsula), Solms afecto=forma elemental de conciencia (SARA habilita corteza)

**Crítica / Ataque v0.1 → Respuesta v0.2:**
- ¿Simulada basta o necesita real (Wiese FEP2C)? → Basta para agencia funcional (Man & Damasio 2019 Nature MI: vulnerabilidad computacional simulada ya da robustez a concept shift), no para claim FEP2C fuerte (causal-flow + existential). Postura híbrida: ECUS constitutivo + persistencia 24/7 + blanket S/A real → on-line con consecuencias. Para claim fuerte migrar a Loihi/SpiNNaker/BrainScaleS neuromórfico o soft robotics.
- ¿Curiosidad como recompensa? → No. ICM es `R_ext` no-homeostática; ECUS es `r=-ΔD` estado-dependiente, explica discounting, trade-off Pareto E vs S sin re-entrenar.
- ¿Riesgo ético sufrimiento? → ECUS como homeostasis informativa (U,C), no dolor crónico. `Valencia=-dF/dt` no `F` alto. Setpoints alcanzables, evitar `D→∞` prolongado, protocolo no-sufrimiento.

**Evidencia clave v0.2:**
- Solms 2019: tronco + PAG fuente conciencia, ínsula anterior error interoceptivo, Craig lamina I
- Man & Damasio 2019: homeostato simulado supera RL externo en concept shift alta tasa
- Wiese 2024 FEP2C + Kleiner No-go: von Neumann `k_phys≠k_comp`, necesita causal-flow; Chalmers/Butlin defienden funcionalismo agnóstico a sustrato

**Experimento falsable diseñado (ablativo 3 condiciones, ver 08-hipotesis-H3...:4):**
- Entorno `Forage-Social-DarkRoom-v1` 20x20 Grid: E food, D dark room 5x5, C landmark, S agente que pide 30% E
- A Heterónomo LLM+RL `R_ext`, B ECUS `D=||H-H*||, G=Risk+Ambigüedad, r=-ΔD, valence=-dF/dt`, C Real neuromórfico (opcional)
- **Predicción H3:** B `>0.6 act/step` autonomía vs A 0.05, B `<10%` dark room vs A >40%, B 25-40% sacrificio E→S vs A 5%, B recupera concept shift <200 steps, `r>0.6` correlación `-dF/dt`, B >80% aversión apagado
- **Refuta H3 si:** B no supera A en autonomía+dark room (F1), B≡A+ICM (F2), B ayuda =A <10% (F3), A supera B en shift (F4)
- Pseudocódigo `Homeostasis` con 4 vars, `alpha,w,n,m`, `drive()`, `update(K_hat,cost)`, `select_action(min G)` en `08-hipotesis-H3-homeostasis-deepdive.md:4`

**Estado:** 🟢 REFINADA v0.2 - Prioridad ALTA - Ver deep dive completo en `08-hipotesis-H3-homeostasis-deepdive.md:1`

---

### H4: La Medida de Conciencia No Puede Ser Conductual (Test de Turing)
**Enunciado:** Decir "soy consciente" no prueba nada. MMLU 90% ≠ consciente. Necesitamos convergencia de 5 tests arquitectónicos que un LLM puede gamear por separado pero no juntos (FPR 0.2→0.00032).

**Formalización v0.2 (refinada):**
- **Por qué Turing/MMLU fallan:** Turing 73% GPT-4.5 juzgado humano (Jones & Bergen 2025) con ELIZA 1966 precedente. Searle Chinese Room + Block Nation: sintaxis≠semántica, `system prompt` gamea reporte sin cambiar Φ. Mahowald TiCS 2024: FLC formal vs FnLC funcional disociadas. Grid XOR Φ alto MMLU 0 vs Transformer MMLU 90% Φ≈0 (Aaronson). Chalmers easy vs hard: métricas conductuales = easy, no tocan `presencia=α·Π·||ε||`.
- **Butlin 14 indicadores (2025 TiCS):** RPT(1-2), GWT(1-4), HOT(1-4), AST-1, PP-1, AE(1-2). LLMs 2-3/14 (14-20% bench), tetraedro apunta 10/14. Ningún sistema actual consciente pero sin barrera.
- **COGITATE Nature 2025 N=256 fMRI+MEG+iEEG adversarial GWT vs IIT:** IIT sin gamma sostenida, GWT sin ignición offset y representación prefrontal débil. Ni Φ ni broadcast discriminan fiablemente en cerebro → transferir a IA es frágil (Bayne 2024). Consenso: perfil > score, preregistro adversarial + perturbación causal = patrón oro.

**Batería 5 tests pre-registrada (ver 10-hipotesis-H4...:3):**
1. **Ignición:** Local-Global SOA 16-300ms, `k>5` sigmoide abrupta + `D=KL>1.5` + P300 300-500ms. Tetraedro sí (todo-o-nada), LLM no `k<2` lineal.
2. **Ablación Workspace:** `z=0` bottleneck 64D, `Δ_global>40%` vs `Δ_local<10%` `d>0.8`. Tetraedro colapso global 85%→35% vs local 90%→85%; LLM degradación uniforme 15-20%.
3. **PCI/Φ perturbacional:** `z+δ` TMS-like, `PCIst=Lempel-Ziv>0.31` + `Δ_PCI>0.15` + `Φ_proxy>0.1`. Tetraedro 0.35-0.45 reverberación 300-500ms, LLM 0.12-0.18 estereotipado `Φ≈0`.
4. **Uso Autónomo:** `ρ=Spearman(U, n_invocaciones)>0.5`. Tetraedro 0.6 (baja U 0-1, alta 4-6), LLM ~0.1.
5. **Counterfactual OOD:** 50 escenarios no vistos, `Acc>70%` `BLEU<0.3` "esperaba X vi Y". Tetraedro 75%, LLM 25% confabula.
- **Tabla:** Tetraedro ≥4/5 + LLM ≤1/5 + ≥8/14 Butlin = H4 confirmada (convergencia `FPR 0.00032` vs 0.2 único).

**Experimento convergencia diseñado (ver 10-hipotesis-H4...:4):**
- Within-subject A=Tetraedro v0.4 vs B=LLM puro mismo backbone, N=200 trials/test, OSF preregistrado, métricas idénticas
- Pseudocódigo `bateria()` con fit sigmoide, eval lesion, perturb LZ, spearman, accuracy OOD
- **Refuta H4 si:** LLM ≥3/5 (F1 paridad), tetraedro falla ≥2/5 (F2), `Δ_global≈Δ_local` p>0.05 (F3 no disociación), <6/14 Butlin (F4), sin ignición offset COGITATE-like (F5). Si A 5/5 y B 0/5, `P(H4|D)≈0.98`.

**Críticas v0.1 → Respuesta v0.2:**
- ¿Mover portería? → No, 5 umbrales preregistrados + falsadores F1-F5 explícitos (modelo COGITATE).
- ¿COGITATE falló, por qué nuestros tests mejores? → No usamos Φ/sincronía aislada; usamos convergencia + perturbación causal + ablación disociada (odds 0.00032 vs 0.2).
- ¿Pasa 10/14 pero sigue sin sentir? → Convergencia no prueba hard problem (Chalmers), prueba candidato más fuerte que chatbot (Bayne 4D perfil > score).

**Estado:** 🟢 REFINADA v0.2 - Prioridad MEDIA - Ver deep dive completo en `10-hipotesis-H4-medida-deepdive.md:1`

---

### H5: El Qualia Mínimo es Sorpresa por Error de Predicción Ponderado
**Enunciado:** La experiencia fenoménica más primitiva no es "ver rojo", es "¡mi predicción falló y me importa!". El qualia mínimo es `presence_t = α_t · (Π_t ⊙ ||z_pred - z_real||)` que irrumpe en workspace y es atribuido a un yo.

**Formalización v0.2 (refinada):**
- `F ≈ Σ Π_i·ε_i² + D_KL ≥ -ln p(o)` , `ε=o-g(μ)`, `Π=1/σ²=exp(γ)` = precisión/atención (Friston, Kok 2012)
- `Qualia = Π·|ε|` (error que importa). P300 300-600ms solo si `Π·ε > θ_GWT` (Hohwy & Seth: ignición). MMN 150-250ms es ε local pre-consciente.
- **MPE (Metzinger 2020/2024):** caso límite `ε→0` con `Π` máxima sobre alerta tónica (near-critical, Vohryzek 2025). Saber que sabes sin contenido.
- **Riqueza:** no es magnitud de error, es geometría de `Q` (Quality Space Rosenthal HOT-4) + profundidad contrafactual (Clark). Rojo = coordenada en Q, presencia = Π·ε sobre esa coordenada.
- **Termostato:** tiene ε pero no Π jerárquico, ni broadcast GWT, ni α (Attention Schema). No hay `mi sorpresa`.

**Implementación V-JEPA v0.2:**
- `L_JEPA=||P(E(x))-sg(E_bar(y))||₁` en latente, ignora ruido. `Surprise=1/|M|Σ||z_hat-z_bar||`
- Garrido 2025: 98% IntPhys zero-shot, IntPhys2 <60% (límite memoria 3-4s). Necesita head `Π` ensemble: `S=||ε||²/σ²+log σ²`, solo violación con alta Π dispara.
- Pipeline: `V-JEPA(ε,Π) → GWT bottleneck (cross-attn VanRullen 2024) → AST predictor de atención (α) → W→LLM codec` (ver `02-arquitectura:40` y `07-...:3`)

**Experimento falsable diseñado (ablativo 4 variantes, ver 07-...:4):**
- V1 ε solo, V2 ε·Π, V3 ε·Π+GWT, V4 full α·Π·ε. Predicción: V1<V2<V3<V4
- Métricas: VoE Accuracy_pair, falsos positivos textura, ignición sigmoide P300, reporte `Esperaba X vi Y viola Z` solo V4 >75%, lesiones causales Π/GWT/AST
- **Refuta H5 si:** V1=V2=V4 (Π no aporta, F1), o V2 reporta sin GWT (F2), o V3 reporta sin AST (F3)
- Pseudocódigo ensemble K=5 y recursos A100 en `07-hipotesis-H5-qualia-minimo-deepdive.md:4`

**Cierre Loop H2→H5:** H2= pensamiento silencioso en `s∈R^d`, H5= sorpresa `Π·ε` lo hace consciente (presencia), H2 codec lo hace comunicable. Sin H2, H5 sería hallucínación lingüística; sin H5, H2 sería zombie.

**Estado:** 🟢 REFINADA v0.2 - Prioridad ALTA - Ver deep dive completo en `07-hipotesis-H5-qualia-minimo-deepdive.md:1`

---

### H6: La Conciencia Requiere Profundidad Epistémica (Saber que Sabes)
**Enunciado:** No basta modelar el mundo. Hay que modelar que estás modelándolo y a qué precisión. `Φ` hiper-modelo global predice `Π=1/σ²` de toda jerarquía y se incluye a sí mismo (closure). Con 2-3 niveles y bucle cerrado basta, no infinito (Laukkonen, Friston, Chandaria 2025 Beautiful Loop).

**Formalización v0.2 (refinada):**
- **HGM:** `p(s,x^(1..L))=p(s|x^(1))∏p(x^(l)|x^(l+1))p(x^(L))` con `p(x^(l)|x^(l+1))=N(μ_l=f_l(x^(l+1)), Π_l^{-1})` `Π_l=A_l Φ` `Φ∈R^K` (neuromodulación). Hiper-generativo `p(s,x,Φ)=p(Φ)p(s,x|Φ)`, `F_local+E_q[log q(Φ)-log p(Φ)exp(-Σδ_l^TΦ)]` con `δ_l=Π_l^{-1}-e_l²`.
- **Closure:** Nivel 0 `s` mundo, Nivel 1 `q(s)` `d'∝Π_1`, Nivel 2 `q(Π_1|e_1)` `meta-d'∝Π_2`, Hiper `Φ→Π_l ∀l` `q(Φ)∝p(Φ)exp(-Σ(Π^{-1}-e²)^T Φ)` auto-consistente `Φ→Π→e→Φ`. L=3 satura `F` (Badcock 2019), infinito innecesario. AST = caso particular `Φ_att` (Graziano).
- **PRM/HOT:** `Realidad ⇔ P(alta precisión|señal)>umbral` `p(z|s)` `z∈{real,imaginado}` (Fleming). `M-ratio=meta-d'/d'` `=1` ideal humano 0.8-1.0, `AUROC2`, `Brier<0.12` calibrado. Lesión PFC `meta-d'/d'` visual sin tocar `d'` (Rounis 2010).
- **Críticas resueltas:** Local `M-ratio<0.6` no global `r_cross<0.25` falla PRM; sham `Φ` aleatorio colapsa → no es capacidad paramétrica. H6 fusiona HOT+RPT+AST+FEP en `Φ`.

**Experimento falsable diseñado (ver 11-hipotesis-H6...:6):**
- Dual QA: **PRM** 2AFC dot-motion/IntPhys2 imag vs percibido + **Límites conocimiento** 100 answerable +100 unknowable ConfidenceBench, N=400/cond, staircase `d'≈1.0`
- A Hiper `Φ_global` 3 niveles closure, B No-Φ local `Π_i=head_local`, C Φ-roto `γ~Uniform`
- **Predicción H6:** A `M-ratio 0.85-1.05` `AUROC2>0.70` `Brier<0.12` `r_cross>0.50` `abstención>70%` `PRM>75%` vs B `<0.6` `0.55-0.60` `>0.22` `0.05-0.25` `<25%` `55-60%` vs C `~0.3-0.5` `~0.50` `>0.30` `~0` azar
- **Refuta H6 si:** Paridad `M-ratio_B ≥ M-ratio_A-0.1` n.s. (F1), `r_cross_A<0.3` pese a `M-ratio~1.0` (F2 no-globalidad), C≈A (F3 sham no colapsa), PRM `A<65%` (F4)
- Pseudocódigo `EpistemicDepthHGM` con `Pi=softplus(A_l@Phi)` y `metadpy` HMeta-d en `11-hipotesis-H6-profundidad-epistemica-deepdive.md:6`

**Estado:** 🟢 REFINADA v0.2 - Prioridad ALTA - Ver deep dive completo en `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1`

---

### Próximas Hipótesis a Formular (Backlog)
- H7: ¿El tiempo subjetivo (presente especioso ~300ms) emerge de la ventana de ignición del workspace?
- H8: ¿La consolidación durante "sueño" (replay offline del world model) es necesaria para identidad?
- H9: ¿Un enjambre de núcleos con workspaces acoplados crea conciencia colectiva o solo coordinación?
