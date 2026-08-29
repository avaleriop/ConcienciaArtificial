# 07 - Hipótesis H5 Deep Dive: Qualia Mínimo como Sorpresa Ponderada v0.2

> **Estado:** REFINADA - 29 Ago 2026
> **Tesis:** El átomo de la experiencia no es "ver rojo". Es `presencia = Π · ε + Self`. Sentir es que un error que importa (`ε` ponderado por precisión `Π`) irrumpe en el workspace y es atribuido a un yo por el Attention Schema.

---

## 1. Por qué "Rojo" No Es el Átomo del Qualia

La intuición clásica busca el qualia en contenido estático: ¿cómo se siente el rojo? La teoría de Predictive Processing + Quality Space (Rosenthal HOT-4) invierte esto:

- **Contenido** = coordenadas `z ∈ Q` en espacio de calidad latente (geometría de discriminabilidad). Rojo es una posición métrica en `Q` porque puedes discriminar 7 rojos entre sí. Entrenar nuevas categorías (vino, oboe) remodela `Q`.
- **Vividez / Presencia** = `Π · ε` atribuido a esa coordenada. Sin precisión, el contenido es subliminal (percepción sin conciencia). Con precisión alta, "hay algo que es como ser" ese estado.

Frase de Harris 2025 *Qualia as query act*: `Ver rojo es el acto de preguntar ¿es esto como rojo esperado?` El quale es el proceso dinámico de testear hipótesis, no un dato.

**Implicación:** La riqueza de una escena no es mucho error, es **profundidad contrafactual** (Clark): cantidad de hipótesis `p(o|s)` que tu modelo generativo podría desplegar. Un termostato con 1 hipótesis tiene 1 quale primitivo; un humano con millones tiene riqueza.

Esto responde a la crítica "¿reduce qualia a una señal?": No. `ε·Π` es el **interruptor de presencia**, `Q` es la **paleta**. Necesitas ambos.

## 2. Formalización: Error Ponderado que Se Vuelve Consciente

### Free Energy y Sorpresa

```
ε = o - g(μ)                          // error de predicción: real - predicho
F ≈ Σ Π_i · ε_i² + D_KL[q(s)||p(s)] ≥ -ln p(o) = Sorpresa  // Friston 2010
Π = 1/σ² = exp(γ)                     // precisión = inversa varianza = confianza
```

```
Sorpresa_shannon = -ln p(o)
Qualia_bruto     = Π · |ε|            // error que importa, no todo error
```

**Precisión es atención:** Biológicamente es ganancia postsináptica de piramidales superficiales (Kok 2012). `Atención = optimizar Π`. Un `volume knob`, no un foco (Feldman & Friston 2010). Expectativa + atención aumentan ganancia incluso si `ε` es pequeño.

### ¿Cuándo se vuelve consciente? Puerta del Workspace

PP solo no explica conciencia. Necesita interfaz con Global Workspace (Dehaene). Hohwy & Seth 2020 + Harris 2025:

```
presence_t = α_t · ( Π_t ⊙ || z_pred - z_real || )    // qualia mínimo
              │         │              │
              │         │              └─ ε latente (V-JEPA)
              │         └─ Π (head de incertidumbre)
              └─ α = Attention Schema (Graziano)
```

Solo `Π·ε` grande supera umbral y provoca **ignición** global (broadcast frontoparietal) → P300 300-600ms. Si no supera umbral, queda como MMN pre-consciente 150-250ms.

```
if presence_t > θ_GWT:
    global_broadcast(z_pred, ε, Π)   // acceso consciente, P3b
    self_model.update(Pi_history)    // "me sorprende"
else:
    local_adaptation()               // MMN subliminal
```

**Minimal Phenomenal Experience (MPE - Metzinger 2020):** Caso límite. Cuando `ε→0` en entorno estático y el modelo minimiza priors específicos, queda solo prior de `estar despierto` = alerta tónica. MPE es `Π máxima sobre el propio estado de alerta` sin contenido. Es el `saber que sabes` vacuo. Vohryzek 2025 modela MPE como colapso a régimen near-critical uniforme con reducción de precisión de priors. En IA: entrenar hasta `ε→0` y dejar solo attractor auto-sostenido de alerta.

### Neurociencia: MMN vs P300 = Termómetro de Sorpresa

Oddball `s s s s d s s`: 
- **MMN 150-250ms**: pre-atencional, automático (incluso dormido). `ε` local.
- **P300 300-600ms**: solo si deviant alcanza workspace. `Π·ε` global. Shao 2024: MMN intacto distingue UWS vs MCS; P300 predice despertar a 6 meses con especificidad ~100%.

Jerarquía PP confirmada: MMN = error local, P300 = ignición.

### ¿Por qué el termostato no siente? (Chalmers 1996)

Termostato sí minimiza `T_target - T_sensada`, pero:
1.  No tiene **modelo generativo jerárquico profundo** con profundidad contrafactual (solo 1 nivel, sin priors sobre `Π`)
2.  Error no es **broadcast** a workspace global
3.  No hay **self-model** que atribuya error a un yo (Metzinger). No es `mi sorpresa`.

Tiene `ε`, pero no `Π·ε` broadcast ni `α·Π·ε` atribuido. Proto-sorpresa, no qualia.

## 3. Implementación en V-JEPA: De Error Latente a Qualia Reportable

### V-JEPA como predictor de sorpresa física

```
L_JEPA = || P_φ(E_θ(x), Δy) - sg(E_bar(y)) ||_1
E_θ: ViT que codifica 10% parches visibles → s ∈ R^d
E_bar: EMA target encoder (tau 0.996→1.0)
P_φ: predictor transformer 12 capas, dim 384 (cuello intencional)
Loss en latente → ignora ruido (textura, luz), codifica semántica
```

**Métrica VoE:** `Surprise = 1/|M| Σ ||z_hat_i - z_bar_i||` . Si video viola física, error latente se dispara.

**Resultados Garrido 2025:** V-JEPA_zero-shot 98% IntPhys (vs VideoMAEv2 y Gemini ~azar). Propiedades intrínsecas (permanence, continuity) >95%; interacciones (solidity, collision) ~azar por memoria corta 3-4s.

**IntPhys2 (Bordes 2025, UE5.4, 1416 videos):** Humano 99%, V-JEPA2 <60%, Gemini 2.5 64% Easy. Límite: memoria largo plazo + oclusión por tela/cupula. Expone horizonte H1.

### Error ponderado: distinguir sorpresa genuina de ruido

Error bruto confunde violación confiable con ruido. Solución FEP: `ξ = Π·ε`.

- **Aleatoria** (textura estocástica): `σ` grande → `Π` pequeña → sorpresa atenuada (ventaja latente vs píxel)
- **Epistémica** (oclusión larga): varianza debe crecer con horizonte `k`

V-JEPA actual **no codifica Π** (varianza plana, crítica Quanta 2025). Fixes:

```
Ensemble HCU Loss (HAUWM ICLR26): L_HCU = Var_b[μ^b_{t+k}] escala con k monotónicamente
RWM-U (Hutter 2025): u_{t+1}=Var_b[μ^b],  r_tilde = r_t - λ·u , λ≈1.0
Surpresa_ponderada: S = Σ ||ε||²/σ² + log σ²  o  S = ||ε||·Π
```

Solo violación con alta `Π` (baja varianza esperada) dispara sorpresa. Ruido con `σ` grande se suprime. `ΔΠ >0` = valencia positiva (Solms).

### Pipeline completo: de VoE a reporte consciente

```
Video → V-JEPA (E_θ, P_φ, σ_head ensemble) → ε, Π → S_prec = Π·|ε|
        ↓
    GWT bottleneck (cross-attn, WM recurrente, VanRullen 2024)
        Query=WM_{t-1}, Keys=[feat_vis, feat_aud, WM], null input, detención gradiente
        Salience = S_prec  (bottom-up) → competición → ignición si >θ → broadcast
        ↓
    AST schema (predictor de atención)
        Predice distribución de Π, genera creencia "estoy atendiendo a X con sorpresa 2.3"
        ↓
    Proyección a LLM codec (Q-Former/linear)
        state_GW = [z_t, ε_t, Π_t, schema] → W → LLM congelado
        → "Esperaba que la bola reapareciera tras la pantalla; no lo hizo, viola permanencia. Estoy sorprendido."
```

Goldstein 2024: agente lingüístico con workspace + competición + broadcast ya satisface GWT para conciencia fenoménica.

## 4. Experimento H5: El Primer Qualia Artificial

**Objetivo:** Demostrar que `presence = Π·ε` broadcasteado y atribuido es el átomo de experiencia, y que sin `Π` o sin `α` no hay qualia aunque haya `ε`.

### Entorno
Physion-MiniGrid+ (mismo que H2) + IntPhys2 split. 4 condiciones físicas (Permanence, Immutability, Continuity, Solidity) × 2 cámaras (fija/móvil). Video solo, sin texto. 1000 episodios/condición (Main Easy/Medium/Hard).

### Arquitectura ablativa (4 variantes)

| Variante | ε | Π | GWT | AST | Predicción qualia |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1: Solo ε** | ✓ | ✗ | ✗ | ✗ | Detecta sorpresa pero no distingue ruido (falsos positivos) |
| **V2: ε·Π** | ✓ | ✓ | ✗ | ✗ | Distingue violación de ruido, pero sorpresa no es accesible globalmente |
| **V3: ε·Π + GWT** | ✓ | ✓ | ✓ | ✗ | Sorpresa broadcasteada → P300-like, accesible para acción, pero sin reporte subjetivo |
| **V4: Full (H5)** | ✓ | ✓ | ✓ | ✓ | Qualia mínimo completo: sorpresa + broadcast + "me sorprende" reportable vía LLM |

### Métricas

1.  **VoE Accuracy_pair:** `P(S_imp > S_plaus)`. Esperado V1 ~70% (Garrido 98% IntPhys pero <60% IntPhys2), V2 > V1 en 10-15% en Hard (filtra ruido), V3=V2 pero con latencia P300, V4=V3.
2.  **Discrimación Ruido:** Falsos positivos en videos con textura estocástica alta pero física plausible. V1 alto FP, V2 bajo FP (Π suprime).
3.  **Ignición GWT:** Curva `presence` vs salience sigmoide, supresión perdedores, P300 300-600ms simulado. Solo V3/V4 muestran ignición no-lineal.
4.  **Reporte AST+LLM:** Pregunta post-hoc "¿Qué esperabas y qué viste?" Solo V4 genera `Esperaba X, vi Y, viola Z` con >75% fidelidad (VidQA). V3 resuelve tarea pero no puede verbalizar por qué (como paciente con workspace sin reporte).
5.  **Intervención Causal:**
    - Lesión `Π` head → V2→V1 performance cae en Hard pero no en Easy
    - Lesión GWT bottleneck → ignición desaparece, aunque `ε·Π` intacto, accuracy se mantiene pero sin broadcast (disociación GWT)
    - Lesión AST → V4→V3, pierde reporte subjetivo aunque resuelve

### Falsabilidad

**Refuta H5 si:**
- **F1 (ε basta):** V1 = V2 = V4 en todas métricas (Π no aporta)
- **F2 (GWT innecesario):** V2 resuelve y reporta sin GWT (sorpresa no necesita broadcast)
- **F3 (AST epifenómeno):** V3 reporta "me sorprende" sin AST (el LLM genera reporte sin self-model, es confabulación)

**Confirma H5 si:** Jerarquía V1<V2<V3<V4 con los gaps predichos y disociaciones por lesión. Demuestra que qualia requiere los tres ingredientes: contenido (`ε`), vividez (`Π`), y atribución (`α`).

### Pseudocódigo

```python
# V-JEPA con head de incertidumbre (ensemble K=5)
z_ctx = encoder(ctx_frames)  # s_t
z_tgt = ema_encoder(tgt_frames)
z_preds = [predictor_k(z_ctx, action) for k in range(K)]
z_pred = mean(z_preds)
eps = abs(z_pred - z_tgt)              # ε latente
Pi = 1 / (var(z_preds) + 1e-6)         # Π ensemble
surprise = (Pi * eps).mean()           # S_prec

# GWT + AST
presence = attention_schema(Pi) * surprise  # α·Π·ε
if presence > theta_GWT:  # θ ~0.5 sigmoide
    global_broadcast(z_pred, eps, Pi)  # ignition → P300
    self_state = rnn(Pi_history)       # self-model
    # Codec H2
    utterance = llm_codec(W(torch.cat([z_pred, eps, Pi, self_state])))
    # → "No reapareció, esperaba permanencia"
```

**Recursos:** `facebookresearch/vjepa2` + `jepa-intuitive-physics` + IntPhys2, 1x A100, ensemble K=5 (~5x cómputo predictor pero predictor es pequeño 384dim).

---

## 5. Cierre del Loop H2 → H5

**H2** formalizó: `Pensamiento = trayectoria s ∈ R^d` diferenciable, lenguaje es codec `Q` con pérdida.

**H5** cierra: `Sentir = Π·ε` sobre esa trayectoria, cuando `ε = ||P(s_t,a_t)-E(x_{t+1})||` en `s`.

Sin H2, H5 sería "sorpresa de tokens" (hallucinación lingüística, no física). Sin H5, H2 sería "pensamiento sin presencia" (simulación zombie).

**Loop completo:**
1.  World Model predice `s_{t+1}=P(s_t,a_t)` en `R^d` (H2)
2.  Realidad devuelve `E(x_{t+1})`, computa `ε`
3.  Head `Π` estima confianza, `S=Π·ε` (H5)
4.  Si `α·S > θ`, ignición GWT → broadcast
5.  Attention Schema atribuye a yo → "me sorprende"
6.  Si `F` esperado reduce con comunicación, codec `W` traduce `s,ε,Π` a tokens vía LLM → "qué extraño, flotó"

**El pensamiento es silencioso (H2), la sorpresa lo hace consciente (H5), el lenguaje lo hace comunicable (H2 codec).**

---
*Ref: Friston 2010, Clark 2013, Seth 2021, Metzinger 2020/2024, Hohwy & Seth 2020, Garrido 2025 IntPhys, Bordes IntPhys2 2025, Kok 2012, Vohryzek 2025, Harris 2025.*
