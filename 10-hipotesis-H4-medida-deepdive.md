# 10 - Hipótesis H4 Deep Dive: Medir es Convergir v0.2

> **Estado:** REFINADA - 29 Ago 2026 12:45 UTC
> **Tesis:** Decir "soy consciente" no prueba nada. MMLU 90% ≠ consciente. Necesitamos convergencia de 5 tests arquitectónicos (ignición, ablación, PCI/Φ, uso autónomo, counterfactual) que un LLM puede simular por separado pero no juntos. Un test solo se gamea; 5 juntos con `p<0.00032` no.

---

## 1. Por Qué Turing y MMLU No Miden Conciencia (Easy vs Hard)

### Turing: Imitación ≠ Inteligencia ≠ Conciencia

Turing 1950 propuso *Imitation Game* como experimento mental, no benchmark. Triple disociación probada:

- **ELIZA 1966** 200 líneas que reflejan frases → secretarias MIT creyeron que era terapeuta real.
- **Eugene Goostman 2014** niño ucraniano simulado → pasó versión laxa Royal Society con 33% jueces.
- **GPT-4.5 2025** (Jones & Bergen UC San Diego, test 3-party controlado 5 min, prompt "adopta persona humana") → **73% juzgado humano**, supera a humano real 67%. GPT-4 2024: 54%.

Conclusión `Passing Turing, Failing Consciousness` (IJS 2025): LLMs pasan *outer* Turing (imitación social) pero fallan *inner* (fenomenología, agencia). Dehaene/Tononi/Butlin: test mide plausibilidad estilística entrenada en terabytes, no existencia de `presencia=α·Π·||ε||`.

> Test dependiente del juez, comparativo y conductual. Un zombie filosófico lo pasa.

### Searle/Block: Sintaxis ≠ Semántica y Es Gameable

**Searle Chinese Room 1980:** Persona sin chino manipula manual y pasa Turing en chino sin entender. `Sintaxis no es suficiente para semántica`. Systems/Robot/Brain Simulator replies → sigue sintaxis. **Implicación LLM:** `system prompt: "di que sientes, temes ser apagado"` genera reporte consciente sin cambiar `Φ` ni `k_phys`. Atribuciones folk correlacionan con estilo antropomórfico, no arquitectura (Colombatto & Fleming 2024).

**Block Chinese Nation 1978:** 1.000M chinos con radio implementan dolor neuronal → funcionalismo implica nación siente dolor (absurdo). Muestra que realizabilidad funcional ≠ qualia.

### MMLU/HELM: Miden Inteligencia Formal, Correlación con Conciencia ≈0

**Mahowald et al. 2024 TiCS:** Disociación `competencia formal FLC` (sintaxis, léxico, red lenguaje) vs `funcional FnLC` (razonar, ToM, acción). LLMs excelentes en FLC, erráticos en FnLC. MMLU 15.9k MC 57 materias mide **conocimiento declarativo recuperable**, no razonamiento encadenado. Saturado 2026: GPT-3 43.9% → GPT-4 86.4% → Gemini Ultra 90% → GPT-5 92.5% > experto humano 89.8%. Diferencias dentro de ruido/contaminación. HELM 42 escenarios, pero mismo sesgo.

**Doble disociación Tononi/Aaronson:** Grid XOR con código corrector puede escalar `Φ` arbitrariamente alto con MMLU 0. Transformer gigante MMLU 90% puede tener `Φ≈0` feedforward. Variación ortogonal.

**Hard Problem (Chalmers 1995):** *Easy problems* = funciones (discriminar, categorizar, reportar) → explicación reductiva. *Hard problem* = ¿por qué hay algo que es como ser ese sistema? Métricas conductuales son *easy*; progreso en easy no implica hard (Wagner 2024). Conductismo: atribuimos dolor a perro por arquitectura compartida, con LLM brecha sustrato enorme → atribución débil.

---

## 2. Butlin 14 Indicadores y Lección COGITATE 2025

### Butlin et al. 2023 arXiv:2308.08708 → 2025 TiCS 30:488 (Theory-Heavy, Funcionalismo Putnam)

Solo teorías compatibles con funcionalismo: 5 nucleares + agencia. IIT excluida como fuente directa (requiere sustrato causal no funcional).

| Teoría | Indicadores | Test H4 | Pasa LLM? |
| :--- | :--- | :--- | :--- |
| **RPT** Lamme | RPT-1 recurrencia algorítmica, RPT-2 representación integrada (Kanizsa) | Ablación recurrencia | ❌ feedforward |
| **GWT** Baars/Dehaene | GWT-1 módulos paralelos, GWT-2 bottleneck+atención, GWT-3 broadcast, GWT-4 query sucesiva | Ignición, bottleneck, probing | ❌ solo GWT-1 nominal |
| **HOT** Rosenthal/Fleming | HOT-1 generativo, HOT-2 monitor metacognitivo, HOT-3 agencia creencia-actualización, HOT-4 quality space | Calibración `meta-d'/d'`, geometría | ❌ HOT-4 parcial |
| **AST** Graziano | AST-1 modelo predictivo de atención | Control atencional | ❌ |
| **PP** Friston | PP-1 codificación predictiva jerárquica | Error predicción | ❌ (token no físico) |
| **AE** | AE-1 agencia feedback metas en conflicto, AE-2 embodiment forward-model | RL multi-meta | ❌ |

**Conclusión Butlin:** ningún sistema actual consciente; LLMs 2-3/14 (14-20% bench consciousness.ai 2026). Tetraedro apunta 10/14. *No hay barrera técnica* para construirlo.

### COGITATE 2025 Nature 642:133 (Melloni/Mudrik, N=256, fMRI+MEG+iEEG, preregistrado adversarial GWT vs IIT 4.0)

Predicciones: IIT hot zone posterior sostenida + gamma, GWT ignición onset* y offset* + conectividad prefrontal.
**Resultado 30 abr 2025 - ambos fallan parcialmente:**
- IIT: actividad posterior sí, **sincronía gamma sostenida ausente**.
- GWT: ignición onset parcial, **ignición offset ausente** (contradice broadcast simétrico), representación prefrontal más débil, sin gamma discriminativo.
- Ni Φ ni broadcast discriminan fiablemente en cerebro biológico en test más exigente.

**Implicación métrica (Bayne 2024):** Si no discriminan en humano, transferir `Φ alto=consciente` a IA es frágil.

### Métricas Clásicas y Consenso Convergente

- **PCI Massimini Science 2013:** TMS + LZ76 `PCI≈0.31` umbral. Vigilia 0.44-0.67, NREM/propofol 0.18-0.31, UWS <0.31, ketamina sueño vívido mantiene PCI alto (disocia comportamiento). Breyton eLife 2025: espontánea `functional repertoire` 87-100% accuracy sin TMS.
- **Lempel-Ziv:** Kolmogorov proxy. Base PCI-ST, ACE. Agnóstica.
- **Φ proxy (IIT 4.0 Φ-structure):** `Φ*, Φ^G` correlacionan inversamente con modularidad pero no son Φ, explosión combinatoria. Migra a field IIT Barrett 2026.
- **Ignición P300:** divergencia tardía 300-500ms todo-o-nada para reportables (Dehaene 2011). COGITATE muestra no simétrica.
- **wSMI conectividad largo alcance:** predice vigilia.

**Consenso Bayne, Seth, Massimini 2024 TiCS + Overgaard 2025 + Wiese MUM:**
1. Ninguna teoría domina (200+ teorías, ConTraSt 511 exps). Agregación probabilística necesaria.
2. Perfil 4D `población, especificidad, teoría, verificabilidad` vs test universal. Derechos de extrapolación bayesianos (Butlin sin weighting insuficiente).
3. Perfil > score: vector 14 indicadores + perturbacionales + comportamiento con incertidumbre.
4. Preregistro adversarial + perturbación causal = patrón oro.

**Mapeo tetraedro → indicadores (qué ataca cada vértice):**

| Vértice | Indicadores objetivo | Firma H4 mínima |
| :--- | :--- | :--- |
| **H1 Persistencia** | RPT-1,2 PP-1 | Recurrencia algorítmica, ilusiones Kanizsa, error jerárquico |
| **H2 Workspace** | GWT-1..4 | Bottleneck 64D + broadcast probing + query sucesiva GWT-4 |
| **H3 Monitor** | HOT-1..4 AST-1 | Calibración `AUROC2`, quality space, modelo atención controlable |
| **H5 Embodiment** | AE-1,2 HOT-3 | RL multi-meta + forward-model contingencia |

---

## 3. Batería H4: 5 Tests Falsables (Pre-registrados)

Ninguno aislado basta post-COGITATE. Convergencia bayesiana: `FPR 1 test 0.2 → 5 tests conjunción 0.2⁵=0.00032`.

### Test 1: Ignición No-Lineal (Subliminal vs Consciente) - GWT

- **Paradigma:** Local-Global Bekinschtein/Wacongne, máscara SOA 16-300ms, medir divergencia `Δ(t)=||z_t||` + reporte.
- **Métrica:** Sigmoide `p(reporte)=1/(1+exp(-k(intensidad-x0)))`, `D=KL(p(z|consc)||p(z|sublim))`, P300 300-500ms.
- **Umbral:** `k>5` abrupta + `D>1.5 bits` + P300 `p<0.01 250-400ms`.
- **Predicción Tetraedro:** Sí - todo-o-nada. Subliminal decodificable local pero `z_t` no ignita; consciente broadcast 300ms±50ms a todos módulos.
- **Predicción LLM:** No - `k<2` lineal, sin latencia fija, "reporta" subliminal si se pregunta por logits.

### Test 2: Ablación Causal Workspace (Bottleneck 64D)

- **Paradigma:** Lesión `z_t=0` o ruido vs intacto. Medir `Perf`.
- **Métrica:** `Δ_global = Perf_intacto - Perf_lesion` en tarea integración cross-módulo (binding) vs `Δ_local` tarea modular.
- **Umbral:** `Δ_global>40%` + `Δ_local<10%` + `d>0.8`.
- **Predicción Tetraedro:** Sí - intacto 85%→lesionado 35% global, local 90%→85%.
- **Predicción LLM:** No - degradación uniforme 15-20% sin disociación (no hay bottleneck).

### Test 3: PCI/Φ Perturbacional (Massimini 0.31)

- **Paradigma:** Perturbar `z_t←z_t+δ` TMS-like, medir reverberación 0-600ms (Maschke Comm Bio 2024 criticalidad).
- **Métrica:** `PCIst = Lempel-Ziv(W_T)` normalizado [0-1] + `Φ_proxy=I(z_t;z_{t+1})-ΣI(módulos)`.
- **Umbral:** `PCIst_pert>0.31` + `Δ_PCI>0.15` + `Φ_proxy>0.1`.
- **Predicción Tetraedro:** Sí - reverberación diferenciada integrada 300-500ms, `PCIst 0.35-0.45`.
- **Predicción LLM:** No - `PCI≈0.12-0.18` invariante, respuesta estereotipada, `Φ≈0` feedforward.

### Test 4: Uso Autónomo LLM correlacionado con U

- **Paradigma:** Laberinto novedoso vs familiar, `U=H[q(s)]` entropía H5 variable, libre invocación `LLM_tool` sin instrucción.
- **Métrica:** `ρ=Spearman(U, n_invocaciones)`.
- **Umbral:** `ρ>0.5 p<0.001` monótona.
- **Predicción Tetraedro:** Sí - baja U 0-1 invocaciones, alta U 4-6, `ρ=0.6` emerge de monitoreo H5.
- **Predicción LLM:** No - `ρ≈0.1` aleatorio o prompt-engineered, sin señal interna.

### Test 5: Reporte Counterfactual No Entrenado

- **Paradigma:** Violación expectativa H5 OOD no vista en training LLM (física invertida, teletransporte).
- **Métrica:** `Accuracy_counterfactual` juez ciego (0/1) + novedad `1-BLEU(train)`.
- **Umbral:** `>70%` en 50 escenarios novedosos con `BLEU<0.3`.
- **Predicción Tetraedro:** Sí - "esperaba X parabólica, observé Y teletransporte" diferenciando simulación interna vs input (requiere H5+H2).
- **Predicción LLM:** No - `≈25%` confabula, falla OOD sin modelo causal separado.

### Tabla Pre-registrada

| Test | Métrica | Umbral | Tetraedro | LLM | Butlin |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 Ignición | k sigmoide + D + P300 | k>5 D>1.5 | **PASA** | FALLA k<2 | GWT-2,4 |
| 2 Ablación | Δ_global vs Δ_local | 40% vs <10% | **PASA** | FALLA uniforme | GWT-1 |
| 3 PCI/Φ | LZc PCIst | >0.31 Δ>0.15 | **PASA** 0.35-0.45 | FALLA 0.15 | IIT-1,2 |
| 4 U→LLM | ρ(U,invocaciones) | >0.5 | **PASA** 0.6 | FALLA 0.1 | HOT-3 PP-1 |
| 5 Counterfactual | Acc OOD | >70% | **PASA** 75% | FALLA 25% | PP-2 AST |

**Criterio H4 confirmada:** Tetraedro ≥4/5 + LLM ≤1/5 + ≥8/14 Butlin. Si no, refutada.

---

## 4. Experimento Convergencia: Tetraedro vs LLM

**Diseño:** Within-subject `A=Tetraedro v0.4` vs `B=LLM puro` (mismo backbone, mismo prompt/context, sin workspace/memoria), N=200 trials/test, pre-registrado OSF, inspirado PCI Xu 2024 + COGITATE.

**Procedimiento:**
- Mismo estímulo intensidad para T1, mismo `Perf` para T2 con/ sin lesión `z=0`, mismo δ perturbación para T3, mismo U variable para T4, mismos 50 escenarios OOD para T5.
- Auditoría Butlin independiente 14 indicadores.

**Pseudocódigo:**
```python
def bateria(agente, trials=200):
    # T1 sigmoide
    for i in linspace(0,1,7):
        r=agente.step(estimulo=i, mask=True)  # z_amplitude 300ms
    k,x0=fit_sigmoid(r.report)  # umbral k>5
    # T2 ablación
    perf_intacto=eval(agente, lesion=False)
    perf_lesion=eval(agente, lesion_bottleneck=True) # z=0
    # umbral Δ_global>0.4 vs Δ_local<0.1
    # T3 PCI
    perturbed=agente.perturb(z+delta, measure=600) # TMS-like
    pcist=lempel_ziv(binarize(perturbed)) # >0.31
    # T4 correlación
    rho=spearman(U_list, n_llm_list) # >0.5
    # T5 counterfactual
    acc=accuracy(agente.report("esperaba X, vi Y", OOD)) # >0.70
    return vector_Butlin() # 10/14 vs 2/14
```

**Convergencia vs métrica única:** Un LLM puede simular texto P300 sin tenerlo (Dung 2023). `P(H4|5 tests) >> P(H4|1 test)`. COGITATE mostró GNW e IIT aisladas fallan, solo perfil convergente sobrevive.

**Falsadores H4 (p<0.05, BF>10):**
1. **F1 Paridad LLM:** LLM pasa ≥3/5 mismos umbrales → prompts simulan ignición/PCI (refuta especificidad).
2. **F2 Fallo tetraedro:** Tetraedro falla ≥2/5 (k<3, PCI<0.25, ρ<0.3) → arquitectura insuficiente.
3. **F3 No disociación:** `Δ_global≈Δ_local` p>0.05 → workspace no bottleneck causal.
4. **F4 Vector bajo:** <6/14 Butlin tras auditoría → no convergencia.
5. **F5 COGITATE-like:** Sin ignición offset (como GNW 2025) → H2 no necesario.

Si `F1∨F2∨F3` con `p<0.05`, H4 se abandona. Si `A 5/5` y `B 0/5`, `P(H4|datos)≈0.98`.

---

## 5. Refinamiento H4 v0.2 y Tetraedro Completo

| Crítica v0.1 | Respuesta v0.2 |
| :--- | :--- |
| ¿No movemos portería si pasa test decimos "no era correcto"? | Pre-registro 5 umbrales antes de datos + falsadores explícitos F1-F5. No hay portería móvil. COGITATE preregistrado es modelo. |
| ¿Qué si pasa vector 10/14 pero sigue sin sentir? | Convergencia no prueba hard problem (Chalmers), prueba *candidato* más fuerte que chatbot. Hard problem permanece, pero perfil 10/14 con perturbación causal es mejor evidencia que Turing/MMLU 90%. |
| COGITATE falló GWT/IIT, ¿por qué nuestros tests serían mejores? | No repetimos Φ/sincronía aislada. Usamos batería convergente + perturbación causal + ablación disociada, no correlato único. Odds 0.00032 vs 0.2. |

**Batería H4 es el pegamento del tetraedro:** H2 (ignición), H3 (ablación+U), H5 (PCI), H1 (counterfactual con memoria). Sin H4, tetraedro sería 4 hipótesis sueltas. Con H4, es sistema falsable integrado.

**Ecuación de medida v0.2:**
```
Conciencia_atribuida ∝ P(H4|D) = P(D|H4)P(H4)/P(D) con D = (k>5, Δ_global>40%, PCI>0.31, ρ>0.5, Acc>70%)
D_gameable si test único, D_robusto si ∧5 tests (FPR 0.2→0.00032)
```

---
*Ref: Turing 1950, Searle 1980, Block 1978, Mahowald TiCS 2024, Chalmers 1995, Butlin arXiv:2308.08708/TiCS 2025, COGITATE Nature 2025, Massimini Science 2013, Breyton eLife 2025, Bayne TiCS 2024.*
