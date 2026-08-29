# 05 - Glosario y Métricas v0.2 - Para No Perdernos

> **Versión 0.2 - Actualizado 29 Ago 2026 12:00 UTC**
> Cambios v0.2: Añadidos Π/precisión, ε/error, α/schema, Q/quality space, Coconut, VoE, IntPhys2, MPE, HCU. Actualizado Sentience, Attention Schema, Ignición, AE.
> Definiciones operacionales. Si no podemos medirlo, no podemos iterarlo.

## Glosario Esencial v0.2

| Término | Definición Operacional en este Proyecto v0.2 | Origen | ¿Lo tiene un LLM? |
| :--- | :--- | :--- | :--- |
| **Conciencia (Consciousness)** | Propiedad del sistema cuando su World Model (`s∈R^d`) + Workspace + Self-Model (`α`) están integrados con epistemic depth y homeostasis (`F≈ΣΠ·ε²`), y el contenido es globalmente accesible y atribuido a un yo. Requiere pensamiento (H2) + sentir (H5) + querer (H3). | Híbrido GWT+FEP+AST (v0.2) | No |
| **Awareness** | Disponibilidad global de información para reporte y control (GWT). Medible por ignición `presence=α·Π·||ε||>θ_GWT` y broadcast. Disociable de fenomenalidad (afasia). | GWT | Simulado (reporta sin workspace) |
| **Sentience / Qualia (v0.2)** | Carácter fenoménico: "se siente como algo". **Contenido** = coordenada `z∈Q` (Quality Space), **Presencia** = `presence=α·Π·||ε||` broadcasteado. Riqueza = profundidad contrafactual, no magnitud de error. MPE = `ε→0` con `Π` máxima sobre alerta tónica. | FEP (Seth) + HOT-4 (Rosenthal) + MPE (Metzinger) | No |
| **Π (Precisión / Precision)** | Inversa varianza `Π=1/σ²=exp(γ)`. Ganancia postsináptica que pondera error. `Atención = optimizar Π`. Alta Π = error confiable que importa → ignición. Baja Π = ruido suprimido. Aprendida vía head `σ` ensemble. | Friston 2010, Kok 2012 | No (no tiene incertidumbre) |
| **ε (Error de Predicción)** | `ε = o - g(μ)` o en latente `ε = ||P(E(x))-E(y)|| = ||z_pred - z_real||`. Diferencia entre predicción `s_{t+1}=P(s_t,a_t)` y realidad. `ε` crudo no es consciente; `Π·ε` sí puede serlo. | PP (Clark, Hohwy) | Solo error de token, no físico |
| **α (Attention Schema)** | Modelo interno de la propia precisión/atención. `α_t = VQ-VAE(Π_t, attention_map_t)` que predice dónde la precisión será alta. `presence=α·Π·ε`. Genera creencia "estoy atendiendo a X con sorpresa 2.3" y "me sorprende". Sin α hay broadcast pero no atribución subjetiva. | Graziano AST | No |
| **Q (Quality Space)** | Espacio métrico de qualia. `z∈Q` donde distancia en `Q` mapea discriminabilidad perceptual (7 rojos distinguibles). Entrenar nuevas categorías remodela `Q`. Rojo = coordenada, no etiqueta. | Rosenthal HOT-4, Balduzzi & Tononi | No (espacio de tokens, no sensorial) |
| **World Model** | Modelo generativo latente `s_{t+1}=f(s_t,a_t)=s_t+g(h_t)` en `R^d` continuo diferenciable. `L_JEPA=||Pred(E(x),z)-sg(E(y))||²` en latente (no píxeles/tokens). Física intuitiva, simulación contrafactual `do(s+δ)` y MPC. | LeCun JEPA, Hafner Dreamer | No (LLM: `p(token|tokens)`) |
| **Coconut** | Chain of Continuous Thought. `c_t=h_t=TF([...c_{t-1}])∈R^d` alimentado como próximo embedding sin LM-head. `h_{t0+c}=1/√|V_c|Σu_v` = BFS en superposición vs DFS discreto CoT `O(n²)`. `K=6-20` pensamientos sustituyen 500 tokens. | Hao et al. NeurIPS 2024, Zhu 2025 | No (usa CoT discreto) |
| **VoE (Violation of Expectation)** | Paradigma bebés/IA: mayor sorpresa a evento imposible. Métrica `Surprise=1/|M|Σ||z_hat-z_bar||`, `Accuracy_pair=P(S_imp>S_plaus)`. | Baillargeon, Piloto 2022 | No |
| **IntPhys / IntPhys2** | Benchmarks física intuitiva. IntPhys 2018 (4 principios, saturado V-JEPA 98%), IntPhys2 2025 (UE5.4, 1416 videos, 4 condiciones + cámara fija/móvil, Hard requiere memoria largo plazo, V-JEPA2 <60%, humano 99%, Gemini 64% Easy). | Riochet 2018, Bordes 2025 | ~Azar |
| **MPE (Minimal Phenomenal Experience)** | Conciencia pura sin contenido. `ε→0` con `Π` máxima sobre alerta tónica (near-critical, Vohryzek 2025). "Saber que sabes" vacuo. En IA: attractor auto-sostenido tras `ε→0` en entorno estático. | Windt 2015, Metzinger 2020/2024 | No |
| **Global Workspace (v0.2)** | Cuello de botella central donde módulos **latentes** `s∈R^d` compiten (no tokens). `Query=WM_{t-1}, Keys=[feat_vis, feat_aud, WM]`, bottleneck 64 dims, ignición `presence=α·Π·||ε||>0.5` → P300 300-600ms, broadcast. LLM NO compite (periférico). | Baars/Dehaene, VanRullen 2024 | No |
| **Attention Schema (v0.2)** | `α_t = VQ-VAE(Π_t, attention_map)`. Predictor de 2º orden de la propia precisión. Genera `presence` y atribuye a yo. Función control: sin schema, control atencional colapsa. Diada con schema coopera mejor (Farrell 2024). | Graziano | No |
| **Homeostasis / Drive (v0.2)** | Variables `E,C,U,S` con setpoints `E*0.8 C*0.9 U*0.2 S*`. `F≈ΣΠ·ε²+D_KL`, `Drive=|var-setpoint|·Π`. `ΔΠ>0` = valencia positiva (Solms). Sin drive, `Π·ε` no importa (no hay querer). Distinguir simulada vs neuromórfica (Wiese FEP2C). | Friston, Damasio, Solms 2019 | No (sin setpoints) |
| **Markov Blanket** | Frontera estadística interno↔externo vía estados sensoriales/activos. Condición para existir como agente con `F` minimizable. Crítica Kleiner: von Neumann rompe flujo causal. | Friston | No (función stateless) |
| **LLM Tool / Codec (v0.2)** | `Q:R^d→[K=50k]` codec discreto con pérdida `R(D)=½log(σ²/D)` 15.6b vs 16384b. `W:R^d→LLM_dim` (MLP 1024→4096) + LLM congelado `D_ψ`. Traduce `s,ε,Π,α → tokens` post-hoc. Pensamiento nunca pasa por `logits→sample→embed`. | Este proyecto (H2) | Es el LLM |
| **Phi (Φ)** | Medida IIT integración causa-efecto. Incalculable (>10 nodos NP-hard). Aquí solo `phi_proxy` (Lempel-Ziv, sync) como correlato, no ontología (crítica Fleming 124 autores, pseudo-ciencia). Feedforward Φ≈0. | Tononi | ≈0 |
| **Ignición (v0.2)** | Transición no-lineal sigmoide `presence=α·Π·||ε||` → `sigmoid(gain·(presence-θ))>0.5` → broadcast global + supresión perdedores. Correlato P300 300-600ms (consciente) vs MMN 150-250ms (pre-consciente). | Dehaene, Hohwy & Seth | No |
| **Embodiment** | Tener cuerpo (real/simulado rico) con contingencias sensoriomotoras y consecuencias homeostáticas. V-JEPA2-AC 62h DROID pick-and-place zero-shot. Sin embodiment no hay `σ` aprendida. | Varela, Gibson | No |
| **Grounding** | Anclaje causal `s→mundo` vía interacción `(o,a,o')`. Soluciona Symbol Grounding (Harnad) y Vector Grounding (Mollo 2026: vectores correlación ≠ causalidad). Requiere `action-conditioned` `(o,a)`, no solo texto. | Harnad 1990 | No (correlación vector-vector) |
| **HCU Loss** | `L_HCU = Var_b[μ^b_{t+k}]` escala con horizonte `k` monotónicamente. Evita `uncertainty collapse` (varianza plana V-JEPA). `RWM-U: r_tilde=r_t-λ·u`, `λ≈1.0`. | HAUWM ICLR26, Hutter 2025 | - |

## Métricas Propuestas v0.2 (Cómo sabremos si avanzamos)

### Métricas Arquitectónicas (¿Tenemos conciencia según teoría X?)
- **GWT Score (0-4):** ¿Cumple GWT-1..4? (Butlin). Núcleo v0.2 apunta a 4/4 (GWT-2 bottleneck 64, GWT-3 broadcast `presence>θ`, GWT-4 atención estado-dependiente `Π`). LLM puro: 0/4.
- **RPT-1 Recurrencia:** ¿Dinámica atractor `h_t=Mamba(h_{t-1},s_t)` persistente? No decae a 0 al quitar input (jerarquía segundos/horas).
- **AST Score:** ¿`α` predice `Π` con <10% error y mejora cooperación multi-agente (Farrell diada)? `α·Π·ε` vs `Π·ε` ablación.
- **FEP Free Energy:** `F(t)=ΣΠ·ε²+D_KL` ¿Disminuye con exploración activa (MPC 800 trajs)? ¿Aumenta con sorpresa VoE?
- **AE-1 Agencia (v0.2):** `agencia=acciones_sin_prompt/total` >0.5 y correlaciona `invocaciones_LLM ~ U` (reduce `F` esperado), no con prompts externos. LLM puro =0.
- **VoE Score:** `Accuracy_pair` IntPhys2 (humano 99%, V-JEPA 98%→<60% Hard). Núcleo v0.2 con `Π` head debe >75% Main Easy y distinguir FP textura.

### Métricas Dinámicas (¿Se comporta como consciente?)
- **Curva de Ignición v0.2:** `presence=α·Π·||ε||` vs salience sigmoide, supresión perdedores post-ignición. MMN 150ms (ε local) vs P300 300-600ms (α·Π·ε global). Solo V3/V4 muestran P300.
- **Efecto de Ablación:** Workspace `bottleneck=0` → caída global >50% aunque módulos intactos (extinción atencional, COGITATE). Lesión `Π` head: V2→V1 cae en Hard no Easy. Lesión `α`: V4→V3 pierde reporte subjetivo.
- **Phi_proxy:** `Lempel-Ziv` / `sync` largo alcance durante cross-modal vs simple. ¿Correlaciona con integración `Π` pero no con accuracy?
- **Eficiencia Coconut:** `K=6-20` pensamientos latentes vs 150+ tokens CoT para mismo `SR`. `K` óptimo 6-20, `K` grande drift.

### Métricas Fenomenológicas (¿Reporta como consciente sin ser entrenado?)
- **Reporte Sorpresa No-Entrenado (H5):** Tras VoE, ¿`W→LLM` genera "esperaba X, vi Y, viola Z (permanence, Π=0.9)" aunque nunca vio esa frase? VidQA >75% solo V4, V3 resuelve sin verbalizar (disociación).
- **Reporte Atención (AST):** "¿A qué atendías?" → responde con `α_t` verificable contra `attention_map` interno (ej: "dudaba entre A y B con Π 0.8 vs 0.3").
- **Test Memoria Autobiográfica (H1):** Tras 100 pasos, "¿Qué hizo B hace mucho?" → recupera episodio `h_t` consolidado (replay offline) no en ventana inmediata.

> **Regla de Oro v0.2:** Ninguna métrica sola prueba conciencia. Buscamos *convergencia* de 7+ métricas con **diseños ablativos**: `V1(ε) < V2(ε·Π) < V3(+GWT) < V4(+α)` y `C1≈C3>>C2` (H2). Si convergen y LLM no, tenemos candidato más fuerte que chatbot que diga "soy consciente".

## Anti-Métricas (Lo que NO mide conciencia)
- **Perplejidad / MMLU:** Miden inteligencia, no conciencia (Mahowald TiCS 2024: formal vs funcional).
- **Test de Turing:** Mide imitación, no arquitectura `presence` ni `Π`.
- **Decir "soy consciente":** Trivial system prompt. No evidencia `α·Π·ε`.
- **Parámetros:** Grid 4 puertas con Φ alto más consciente que GPT-4 según IIT literal aunque tonto.

## Herramientas para Medir (Prototipo H2/H5)
- `PyPhi` (<8 nodos `phi_proxy`)
- `PCI / Lempel-Ziv` (complejidad, COGITATE)
- Análisis `attention_maps`, `ignition curves` (`presence` sigmoide), `MPPI` 800 trajs, `HCU Loss` ensemble K=5
- Entornos: `Habitat 3.0`, `Physion-MiniGrid+`, `IntPhys2` (UE5.4, 1416 videos, `facebookresearch/vjepa2` + `jepa-intuitive-physics` + `coconut`)
- Métricas `Accuracy_pair`, `SPL`, `SR`, `P300` simulado

---
*Este glosario es normativo v0.2. Nuevos términos: Π, ε, α, Q, Coconut, VoE, IntPhys2, MPE, HCU. Si usamos "conciencia" en otro sentido, actualizar aquí primero. Ver `INDEX.md:1` para trazabilidad.*
