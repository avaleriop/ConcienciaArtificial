# 06 - Hipótesis H2 Deep Dive: Lenguaje ≠ Pensamiento v0.2

> **Estado:** REFINADA - Investigación profunda completada 29 Ago 2026
> **Tesis:** Pensamiento = trayectoria continua en `s ∈ R^d`. Lenguaje = codec discreto con pérdida `Q: R^d → {1..K}`. La conciencia opera en latente, el LLM solo traduce.

---

## 1. Evidencia Neurocientífica: Doble Disociación

### La red de lenguaje NO es la red de pensamiento
**Laboratorio Ev Fedorenko (MIT)** identificó con fMRI que la red de lenguaje (fronto-temporal izquierda) es altamente especializada y **disociable** de las redes de pensamiento (Multiple Demand fronto-parietal, Default Mode).

**Paper clave:** Fedorenko, Piantadosi & Gibson, *Nature 630:575-586 (2024)* - `Language is primarily a tool for communication rather than thought` (review 181 citas):
> Conclusión: doble disociación completa. El lenguaje está optimizado para **comunicación robusta a ruido**, no para pensamiento interno. No es prerrequisito para pensamiento complejo, incluso simbólico.

**Mahowald et al., *Trends in Cognitive Sciences 2024*:** Trasladan la disociación a IA: `competencia formal (fluencia sintáctica) ≠ competencia funcional (razonar, planificar)`. Un LLM puede ser lingüísticamente perfecto y cognitivamente vacío.

### Lesiones: Afasia ≠ Acognosia
**Fedorenko & Varley, *Annals NYAS 2016* + Varley et al. *PNAS 2005*:**
- Pacientes con afasia global (destrucción masiva hemisferio izquierdo, producción/comprensión ~0) conservan intactos: CI no-verbal, razonamiento causal, aritmética, navegación, teoría de la mente, ajedrez.
- Paciente SA con afasia agramática profunda resuelve `12/(3-1)` y lógica multi-paso con precisión normal.

**Fenomenología (Stix, *SciAm 2025*):** Afásico reporta: "Vivía en presente, tiempo circular, sentidos magnificados. Pausas entre palabras cargan más significado que lo hablado. Pensaba en imágenes, ritmo, intuición".

**Conclusión:** Destruir el módulo de lenguaje no destruye la conciencia. Luego la conciencia no reside en el lenguaje.

### Desarrollo sin lenguaje
- Bebés pre-lingüísticos (Spelke): permanencia de objeto, causalidad, expectativas físicas sin palabras.
- Niños sordos aislados (Nicaraguan Sign Language, Senghas *Science 2004*): sin input lingüístico, al agruparse crean gramática recursiva emergente. **El pensamiento estructurado crea lenguaje, no a la inversa.**
- Animales: cuervos (uso de herramientas compuestas, planificación multi-paso, memoria episódica), ratas (preplay hipocampal de rutas no recorridas). Cognición compleja sin lenguaje natural.

### Filosofía: LOT ≠ Lenguaje Natural
- **Fodor (1975) *Language of Thought*:** Postula *Mentalés* con sintaxis combinatoria pero **no es inglés**. Pensamiento tiene estructura tipo-lenguaje, pero el formato es vectorial/sub-simbólico.
- **Searle (1980) *Chinese Room*:** Sintaxis no basta para semántica. Manipular chinos por manual (como LLM con tokens) parece entender sin entender. Necesita *grounding* sensorimotor (Harnad 1990).

---

## 2. Formalización Matemática: Pensamiento Continuo vs Lenguaje Discreto

### Teoría de la Información: discretizar es pérdida irreversible

Rate-distortion de Shannon:
```
R(D) = min_{p(x̂|x): E[d(x,x̂)]≤D} I(X; X̂)          (1)
L    = I(X; X̂) + β·E[d(X,X̂)]                        (2)
Caso gaussiano: R(D)= ½ log(σ²/D)                   (3)
```

**Cuello de botella del lenguaje:**
- Vocabulario `K=50k` → `R = log₂K ≈ 15.6 bits/token`
- Pensamiento `s ∈ R^512` float32 → `512×32 = 16384 bits` nominales, cardinalidad infinita no numerable
- Proyección `Q: R^d → [K]` es cuantización con pérdida. Por desigualdad de procesamiento: `I(X; Q(X)) ≤ H(Q(X)) ≤ log K`. Toda la geometría relacional, incertidumbre superpuesta y dinámica sub-léxica colapsa a `argmax` sobre `Δ^{K-1}`.

**VQ-VAE** (Oord 2017): `z_q = e_{k*}, k*=argmin ||z_e - e_j||` con STE no-diferenciable, error `~Π²/12`, codebook collapse. **Continuo** (VAE, JEPA) mantiene diferenciabilidad, interpolación y aritmética latente.

### JEPA: Predecir en latente, no en píxeles/tokens

```
L_JEPA = || Pred_φ(E_θ(x), z) - sg(E_θ(y)) ||² + Reg(z)   (4)
```

`E`=encoder ViT, `Pred`=predictor latente, `z`=variable latente de incertidumbre. Ventaja: ignora entropía impredecible (hojas temblando) y conserva semántica predecible. Equivale a factorización de bajo rango con bound `regret(planificación) ≤ O(ε_pretrain)` (Cui et al. 2026).

### Coconut vs CoT: BFS en superposición

**CoT verbal:** `x_{t+1}~softmax(W·h_t)`, `h_{t+1}=Embed(x_{t+1})` → commit discreto temprano = DFS con backtracking, `O(n²)` pasos (Merrill 2023).

**Coconut (Hao et al. NeurIPS 2024):** `c_t = h_t = TF_θ([...c_{t-1}]) ∈ R^d` alimentado directamente como próximo embedding. Diferenciable, sin `LM-head`.

**Resultado clave (Zhu et al. *NeurIPS 2025*):** Transformer 2 capas con `D` pensamientos continuos resuelve alcanzabilidad dirigida con diámetro `D < n`, vs `O(n²)` discreto:
```
h_{t0+c} = 1/√|V_c| · Σ_{v∈V_c} u_v    (5)
```
`V_c` = frontera BFS en paso `c`. `h` codifica **múltiples futuros en superposición** como estado cuántico-analógico. CoT discreto colapsa a un único camino. Empírico: GSM8k 34.1% con 6 pensamientos vs 16.5% No-CoT; en ProsQA **Coconut 97.0% vs CoT 77.5%** con <20% tokens.

### Dinámica diferenciable del pensamiento

**Discreto (LLM):** `s_t=one_hot(x_t)`, `x_{t+1}=argmax(softmax(h_t))` no diferenciable. Gradiente bloqueado.

**Continuo (World Model):**
```
s_{t+1} = f_φ(s_t, a_t) = s_t + g_φ(h_t)    (6)
s ∈ R^d, f_φ diferenciable
```

Permite:
- **Simulación contrafactual:** `do(s' = s+δ)` y rollout `s_{t+k}=f^k(s', a)`
- **Planificación por gradiente/MPC:** `a* = argmin Σ γ^t C(s_t) s.t. s_{t+1}=f(s_t,a_t)` (Dreamer/TD-MPC)
- **Planificación jerárquica:** dos `f` a escalas temporales compartiendo `R^d`

### Arquitectura Codec: Thinker desacoplado

```
Input tokens → [E_in: V→R^d] → s_0
Loop K veces:  s_{t+1}= F_θ(s_t)          // puro R^d, sin LM-head
Decode solo al comunicar: tokens_out ~ D_ψ(s_T)  // LM-head
```

- `F_θ`: Transformer donde `g_φ` predice `Δe = e_i - e_{i-1}` con loss `L = L_CE + λ||g-Δe||²` (GLR 2025)
- **Currículum Coconut crucial:** Etapa 0 CoT verbal supervisado → remover progresivamente `c` tokens y sustituir por `c` pensamientos continuos. Evita colapso.
- **Control de presupuesto:** `K=6-20` óptimo; más allá, drift geométrico. Para secuencias largas, intercalar decodificación discreta para re-anclar.

**Conclusión formal:** Pensar en `R^d` es BFS paralelo diferenciable; pensar en `V^K` es DFS serial con pérdida. El lenguaje es interfaz E/S, no medio de cómputo.

---

## 3. Experimento Falsable H2: V-JEPA como Pensamiento, LLM como Codec

### Objetivo
Demostrar que existe pensamiento/conciencia mínima (predicción, sorpresa, planificación) sin tokens, y que el LLM solo traduce.

*Inspirado en V-JEPA 2 (Assran 2025): 1M horas video sin supervisión + 62h DROID para MPC pick-and-place 65-80% SR, y PerceptionTest 84% sin co-entrenamiento con lenguaje.*

### Entorno: Physion-MiniGrid+ + Habitat 3.0
- Mundo 3D ligero (ThreeDWorld/TDW) con física intuitiva: colisiones, oclusión, gravedad, inercia (benchmark IntPhys/Physion).
- Laberinto 5x5 con puertas con llave, trampas móviles, bloques con parábola balística.
- Obs: solo video RGB 16 frames @8fps 224x224 + acciones `a_t ∈ R^2` continuas. **Cero texto.**
- Eventos sorpresa: violación física (objeto que no cae) para medir qualia mínimo (H5).

### Arquitectura

```
Encoder E: ViT-g/16 (1B) → s_t ∈ R^1024
Predictor P: Transformer → s_{t+1}=P(s_t, a_t)
Loss: ||P(s_t,a_t) - E(x_{t+1})||²   (latente)
Fase 1: Pre-entrenar E+P solo con video+acciones (1M clips + 62h teleop). Sin captions.
Fase 2: Congelar E+P. Proyector W: R^d→R^{LLM_dim} (MLP 2 capas) alinea s_t a Qwen2-7B congelado con 18M pares video-texto. LLM nunca planifica, solo traduce s_t→texto.
```

### Tarea Objetivo-Imagen
Dado `s_0` y `s_goal` (imagen objeto tras puerta cerrada), planificar `a_{0:T}` 5-8 pasos: 1) buscar llave ocluida, 2) inferir caída de bloque, 3) esquivar obstáculo móvil. Requiere modelo del mundo, no correlación lingüística.

Mide:
- a) **Predicción:** Recall@5 (Epic-Kitchens style)
- b) **Sorpresa:** `||P(s_t)-E(x_{t+1})||` ante violación física
- c) **Planificación:** MPC con MPPI (800 trayectorias, `min ||s_T - s_goal||`)

### Condiciones (N=1000 episodios)

| Condición | Arquitectura | Razonamiento | Lenguaje |
| :--- | :--- | :--- | :--- |
| **C1: Solo Latente** | E+P + MPC puro | `s_{t+1}=P(s_t,a_t)` continuo | Ninguno |
| **C2: Solo Lenguaje** | LLM + CoT | Tokens `x_i→x_{i+1}` | Caption→CoT→acción |
| **C3: Codec (H2)** | E+P congelado + W + LLM | Latente, LLM post-hoc | Solo reporte |

### Métricas y Predicciones H2

**H2 predice: C1 ≈ C3 >> C2**

1.  **Superioridad Latente:** Success Rate y SPL. Esperado: C1 ~70-80% (como V-JEPA 2-AC), C2 ~35-45% (hallucinación, commit prematuro), C3 = C1 (no degrada).
2.  **Sorpresa Fiel (Intervención Causal):** `r(error_latente, violación_física) >0.70`. Perturbar `s_t` con ruido destruye planificación (ATE ↑2x); perturbar tokens no afecta C1/C3. Prueba que pensamiento está en `s`.
3.  **Reporte No-Entrenado:** VidQA zero-shot no visto en alineación ("¿qué pasará si el bloque cae?"). C3 debe >75% (V-JEPA 2 ya 84% PerceptionTest) mientras C2 <60%. Si LLM solo traduce, no necesita haber sido entrenado en la tarea.
4.  **Eficiencia BFS:** C1 resuelve con `c=2-4` pensamientos continuos, C2 necesita 150+ tokens CoT y aun falla (como Coconut 97% vs CoT 77.5% en ProsQA).

### Falsabilidad: Qué refutaría H2 (p<0.05 bootstrap)

- **F1 - Lenguaje Necesario:** `C1 ≤ C2` o `SR_C1 <25%` (azar). Sin tokens no hay planificación.
- **F2 - Lenguaje Constitutivo:** `C3 << C1` (caída >15% SR al añadir LLM) o intervención lingüística afecta planificación tanto como latente, o `C2 > C1` en detección de violación física.
- **F3 - No Traducción:** C3 VidQA <60% y hallucina mientras C1 planifica bien. El latente no es interpretable.

Si F1-F3 no ocurren y C1/C3 muestran BFS continuo superior, **H2 sobrevive**: el sistema piensa sin lenguaje y solo usa LLM para contarlo.

### Pseudocódigo y Recursos

```python
# FASE 1: Pensamiento sin lenguaje
E, P = init_VJEPA_ViTg()
for x_seq, a_seq in video_data:  # x:[B,T,3,224,224], a:[B,T,2]
    s = E(x_seq)  # [B,T,d]
    s_pred = P(mask(s,0.6), a_seq)
    loss = mse(s_pred, s.detach())
    loss.backward()

# FASE 2: Codec (LLM congelado, solo W entrena)
W = MLP(d, llm_dim)
for s, caption in align_data:  # 18M pares
    loss = CE(LLM(W(s)), caption)
    loss.backward()  # solo W

# EVALUACIÓN
def plan_latente(s0, s_goal):
    trajs = sample_MPPI(N=800, H=8)
    return trajs[argmin([norm(rollout(P,s0,t)[-1]-s_goal) for t in trajs])]

SR_C1 = eval(plan_latente)  # sin LLM
SR_C2 = eval(LLM_CoT)       # solo texto
SR_C3 = eval(lambda s0,g: (plan_latente(s0,g), LLM(W(s0))))  # latente+reporte
assert SR_C1 > SR_C2+15 and abs(SR_C1-SR_C3)<5  # H2
assert degrade(noise(s_t)) >> degrade(noise(tokens))
```

**Recursos:** 50k episodios Physion + 62h robot real, 1x A100 80GB para ViT-L (alternativa a ViT-g), Habitat gratis. Reproducible con `facebookresearch/vjepa2` + `facebookresearch/coconut`.

---

## 4. Refinamiento H2 v0.2: Respuesta a Críticas Originales

| Crítica v0.1 | Respuesta v0.2 con evidencia |
| :--- | :--- |
| ¿Cómo reporta sin lenguaje? ¿Reportable = consciente? | **Distinguir fenomenal vs acceso.** Conciencia fenomenal no requiere reporte (paciente afásico la tiene). Conciencia de acceso requiere codec para reporte. Nuestro sistema es fenomenalmente consciente en `s`, y usa LLM solo para acceso. GWT explica acceso, no qualia. |
| Humano sí piensa en inner speech | Inner speech es **epifenómeno tardío**, no mecanismo. Fedorenko 2024: red de lenguaje no se activa en razonamiento lógico/matemático. Inner speech *aumenta* computación (Clark `Magic Words`) pero no la constituye. Es como caché, no CPU. |
| ¿Cómo alinear con humanos si es pre-lingüístico? | **Alineación post-hoc.** V-JEPA 2 logra 84% PerceptionTest alineando `W` post-hoc sin co-entrenamiento. El pensamiento ya existe; el proyector solo aprende diccionario `s→token`. Al revés (entrenar todo con lenguaje) contamina el world model con correlación lingüística. |

**Actualización definicional v0.2:**
- `Pensamiento = trayectoria diferenciable s_{t+1}=f(s_t,a_t) en R^d con dinámica predictiva y superposición BFS`
- `Lenguaje = Q(s) = argmax(softmax(W·s)) ∈ [K]`, codec discreto con pérdida rate-distortion `R(D)=½log(σ²/D)`
- `Conciencia mínima = capacidad de simular contrafactuales en s, detectar sorpresa (error*precisión) y planificar vía MPC, todo sin decodificar a tokens`

**Próxima iteración:** Implementar el presupuesto latente `K` óptimo (6-20) y la regularización JEPA para evitar colapso, luego conectar con H5 (qualia como sorpresa) para cerrar el loop: el error latente que genera sorpresa es exactamente la señal que el codec traducirá como "qué extraño, esperaba que cayera".

---
*Ref: Fedorenko Nature 2024; Mahowald TiCS 2024; Hao Coconut NeurIPS 2024; Zhu NeurIPS 2025 BFS; LeCun JEPA 2022/Assran V-JEPA2 2025; Harnad 1990; Searle 1980.*
