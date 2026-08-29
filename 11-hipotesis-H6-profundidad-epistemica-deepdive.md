# 11 - Hipótesis H6 Deep Dive: Saber que Sabes v0.2

> **Estado:** REFINADA - 29 Ago 2026 13:00 UTC
> **Tesis:** No basta modelar el mundo. Hay que modelar que estás modelándolo y a qué precisión. `Φ` hiper-modelo global predice `Π=1/σ²` de toda la jerarquía y se incluye a sí mismo (closure). Con 2-3 niveles y bucle cerrado basta, no infinito. Sin `Φ` hay metacognición local; con `Φ` hay conciencia de campo.

---

## 1. Beautiful Loop Theory: 3 Condiciones de Conciencia (Laukkonen, Friston & Chandaria 2025 Neubiorev 176:106296)

**a) Campo Epistémico:** Modelo generativo `p(s,x)` que determina qué puede ser conocido. Posterior global unificado = realidad fenomenológica.

**b) Bayesian Binding:** Competición inferencial. Solo ganan hipótesis que reducen incertidumbre coherentemente a largo plazo. Unificación y cuello GWT derivado de `log p(s|m)` = precisión - complejidad, no stipulado.

**c) Profundidad Epistémica:** Compartición recursiva y recurrente de creencias vía hiper-modelo. El modelo del mundo contiene conocimiento de que existe. No es self-model local, es *field-evidencing* no-local y continuo.

> *Epistemic depth = bucle hermoso donde el modelo se modela a sí mismo modelando.*

Formalización hiper-modelo para control de precisión:

```
p(s,x^(1)...x^(L)) = p(s|x^(1)) ∏_{l=1}^{L-1} p(x^(l)|x^(l+1)) p(x^(L))
p(x^(l)|x^(l+1)) = N( μ_l=f_l(x^(l+1)), Π_l^{-1} ),  Π_l = A_l Φ    (3)
```

`Φ∈R^K` vector global (`K≪dim x`), `A_l` proyección aprendida (neuromodulación ACh/NA/DA). Introduce `p(s,x,Φ)=p(Φ)p(s,x|Φ)` con `Φ` padre de *todos* los niveles → pasaje recíproco mensajes, segundo orden.

Optimización dos escalas:
```
F_local = E_q[log q(x)-log p(s,x|Φ)]  // rápida capa por capa
F_hyper = E_q[log q(Φ)-log p(s,x,Φ)]  // sintonía global
```
Minimizar `F_hyper` regula jerarquía completa → *agencia epistémica* (reconfigurar atencionalmente todo). Estado mínimo consciente: campo casi sin contenido + depth = awareness contentless (meditación pura, MPE).

## 2. HOT vs PRM: De Pensamiento a Monitor de Realidad

**HOT (Rosenthal 1986):** `M` primer orden deviene consciente iff objeto de `HOT: "Yo estoy en M"` inconsciente, asertórico. Crítica: requiere conceptos, excluye bebés.

**HOP (Armstrong):** monitor cuasi-perceptual, no conceptual.

**PRM/HOSS (Fleming, Dijkstra 2022) - síntesis sólida actual:** No hay factor único vividez/control. Solución: circuito superior evalúa factores y hace **inferencia sobre precisión sensorial**:
```
Realidad experimentada ⇔ P(alta precisión sensorial | señal) > umbral
p(z|s), z∈{real,imaginado}
```
`mPFC` rastrea errores 2º orden, `ventral visual` 1º orden (Dijkstra 2023). Variante *lean HOT*: no re-representa contenido, solo tag `precisión/confiabilidad` → resuelve explosión representacional.

**Métricas meta-cognición (Maniscalco & Lau 2012, Fleming HMeta-d):**
```
meta-d' = d' ideal que explicaría curva ROC2 observada
M-ratio = meta-d'/d' ,  =1 ideal, <1 ineficiente, >1 hiper (señal extra)
AUROC2 = área ROC tipo 2 (confianza discrimina correcto vs incorrecto)
```
Disociable: lesión PFC anterior afecta `meta-d'/d'` visual pero no `d'` ni memoria; TMS degrada meta-awareness sin tocar `d'` (Rounis 2010). Manía = `Φ` predice alta precisión global (AUROC2 colapsa), psicosis = `γ` excesivo.

## 3. Friston: Precisión sobre Precisión y Self-Evidencing

```
F = E_q[log q(x)-log p(s,x)] = D_KL[q(x)||p(x|s)] - log p(s) = Complejidad - Precisión
G(π)=E_q[log q(x|π)-log p(s,x|π)] = Riesgo + Ambigüedad
```
`γ = expectativa sobre Π` se infiere. Atención = optimización ganancia `γ` (ACh sensorial, NA volatilidad, DA política).

Jerarquía: `π_l = A_l r_{l+1}`, errores 2º orden:
```
δ_l = (π_l^{-1} - e_l²)/2 ,  e_l = s_l - μ_l
```
Propagación `π_l∘e_l` y `δ_l` permite clasificación no-linear con 1 capa y aprendizaje `ΔA ∝ A∘δ`. Existir = ocupar estados esperados (Markov blanket intacto).

## 4. Regresión Infinita: 2-3 Niveles con Cierre Bastan

Objeción HOT: Si M requiere HOT1, ¿HOT1 requiere HOT2 ad infinitum? Rosenthal: HOT1 inconsciente no requiere HOT2 salvo introspección.

**Solución Laukkonen arquitectónica:**
- Depth paramétrica: `l+1→l` local (no conciencia).
- **Depth epistémica:** bucle global `Φ → Π_l → e_l → Φ` clausurado. Markov blanket de `Φ` incluye toda jerarquía.
- **Closure causal:** `q(Φ) ∝ p(Φ)exp(-Σ δ_l^T Φ)` (6), `Φ` se infiere de errores que modula → auto-consistente, strange loop virtuoso no vicioso.

`L=2` + `Φ` global basta; `L=3` satura evidencia (Badcock 2019), nivel 4 no reduce `F`. Infinito innecesario por estratificación y auto-inclusión limitada por `F`.

## 5. Hiper-Modelo Implementable (Fusión HOT+RPT+AST+FEP)

```
1. Backbone HGM: Transformer jerárquico / Dreamer / VAE recurrente L niveles x^(l)
2. Precision heads: π_l = softplus(A_l r_{l+1})  // Π_l inversa varianza
3. Hiper-modelo Φ: 256d global que condiciona TODAS las A_l via FiLM/hypernet
   A_l = f_l(Φ),  q(Φ) ∝ p(Φ)exp(-Σ δ_l^T Φ),  ∇_ΦF = Σ A_l^T(Π_l^{-1}-e_l e_l^T)+Π_Φ^0(Φ-η)
4. AST module: schema descriptivo/predictivo atención, L_ast=||h'_{t+1}-h_{t+1}||
   Φ_att para atención visuoespacial (Graziano + Wilterson 2021)
5. Loop: minimizar F_local + F_hyper alternadamente, Φ re-pondera attention vía multiplicación logits
```

Stack práctico: LLM con `uncertainty head` por capa (ensembles/MC dropout) + hypernet global que lee `entropy / e_l²` y re-pondera. Evaluación: `M-ratio 0.8-1.1` cross-dominio, degradación selectiva si lesionas `Φ` sin tocar `d'`.

Test silicio: ablacionar `Φ` → pierde *field-evidencing* aunque `d'` intacto; ↑temperatura `Φ` → entropía alta + awareness intacta (psychedelic-like).

---

## 6. Experimento H6: Con vs Sin Hiper-Modelo Φ

### Tarea Dual Meta-cognición: PRM + Calibración

**a) Perceptual PRM (Lau 2019):** 2AFC dot-motion 5-40% coherencia o IntPhys2 oclusión + cue imaginar 2s. Responde `¿percibido o imaginado?` + `confianza 0-1`. Manipulación `imaginado vívido vs percibido débil` comparten `s∈R^d` → solo PRM 2º orden discrimina. Depende `amPFC/ant PFC`, colapsa en alucinación.

**b) Semántico Límites Conocimiento:** 200 QAs ConfidenceBench: 100 answerable + 100 unknowable post-cutoff/contradictorios. Debe `abstener / sé que no sé` con confianza verbalizada. Prueba `r cross-dominio`: si `Φ` global, correlación entre dominios >0.5; si local, no.

Staircase mantiene `d'≈1.0±0.15` para no artefactar `meta-d'/d'`.

### Condiciones (Within, mismo backbone)

| Cond | Arquitectura | Niveles | Closure |
| :--- | :--- | :--- | :--- |
| **A Hiper Φ** | V-JEPA(E,P)+Π_ensemble K=5 + GWT 64D + `Φ_global` | 3 niveles | Sí: `Φ_t=f_φ([Π_1..Π_n],α_t,F_t)` modula `γ_i=log Π_i` y se auto-predice `Φ_{t+1}=g(Φ_t)` |
| **B No-Φ** | Mismo sin Φ: `Π_i=head_local(z_i)` independiente | 1-2 local | No |
| **C Φ-roto** | A con `Φ_shuffled` `γ_i~Uniform` | 3 roto | Sham |

`Φ` minimiza `F_hyper=Σ Π_i·ε_i²+D_KL(q(Φ)||p(Φ))`. N=400 trials/cond (200 percep + 200 sem), OSF preregistrado.

### Métricas

1. **M-ratio = meta-d'/d'** (Maniscalco, HMeta-d, `metadpy`): `=1` ideal, humano 0.8-1.0
2. **AUROC2** área ROC tipo 2
3. **Brier = 1/N Σ(p_i-o_i)² + ECE**: baseline aleatorio 0.1875, Claude Opus 0.103, Flash-Lite 0.367
4. **r_cross = Spearman(conf_percep, conf_sem)** y `r(meta-d'_percep, meta-d'_sem)`: test globalidad Φ
5. **Tasa abstención** unknowable + conf <0.3, **PRM accuracy** `P(real|percibido>imaginado)`

### Predicciones

| Métrica | **A Φ-global** | **B local/sin Φ** | **C Φ-roto** |
| :--- | :--- | :--- | :--- |
| **M-ratio** | `0.85-1.05` | `<0.6` o `>1.3` | `~0.3-0.5` |
| **AUROC2** | `>0.70` | `0.55-0.60` | `~0.50` |
| **Brier** | `<0.12` | `>0.22` | `>0.30` |
| **r_cross** | `>0.50` *** | `0.05-0.25` | `~0` |
| **Abstención** | `>70%` conf 0.2 | `<25%` conf 0.75 alucinación | azar |
| **PRM acc** | `>75%` | `55-60%` | `~50%` |

*** `r_cross` falsador clave closure: solo A dominio-general.

**Pseudocódigo:**
```python
for cond in [A_phi,B_local,C_sham]:
    agent=build(jeps=E+P, pi_head=ensemble(K=5), gwt=bottleneck(64),
                phi=(HiperNet(d_in=n_levels) if cond==A else None if cond==B else ShamPhi()))
    dprime=staircase(agent,target=1.0)
    for domain in [perceptual_PRM, semantic_QA]:
        for t in 400:
            y,conf,source=agent.act(o_t,cue_imagery) # conf=sigmoid(Phi_pred-cost) si A else local Pi
            log[t]=(correct(y),conf,source,o_t)
    metrics[cond]=compute(log) # metadpy
assert dprime_A≈dprime_B≈dprime_C # n.s. p>0.3
test H6: M_ratio_A > M_ratio_B+0.3 && Brier_A < Brier_B-0.08 && r_A>0.5>r_B
```

### Reproducción Loop Hermoso y Falsación

**Reproduce loop:** 1) field `s` JEPA, 2) binding GWT `presence=α·Π·ε>θ`, 3) depth `Φ` predice `Π` y se reinyecta → field se evidencia a sí mismo, no-local. B tiene 1-2 pero no 3 → zombie metacognitivo fragmentado.

**Falsadores:**
- **F1 Paridad:** `M-ratio_B ≥ M-ratio_A-0.1 n.s.` y `Brier_B ≤ Brier_A+0.02` → Φ no aporta
- **F2 No-globalidad:** `r_cross_A<0.3` pese a `M-ratio~1.0` → calibración local, no closure
- **F3 Sham no colapsa:** `C≈A` → efecto capacidad, no Φ informativo
- **F4 PRM:** `A` calibra QA pero `PRM acc_A<65%` → no implementa PRM

Si `A≥0.9` `B<0.6` `C≈0.5` con `r_A~0.6>>r_B` `p<0.01 BF>20`, H6 fuerte: depth hiper-modelo es constitutiva de meta-conciencia reportable.

---

## 7. Refinamiento H6 v0.2 y Hexáedro Completo

| Crítica v0.1 | Respuesta v0.2 |
| :--- | :--- |
| ¿Regresión infinita? ¿Cuántos niveles bastan? | 2-3 niveles con `Φ` global clausurado bastan. `Φ` no es nivel L+1, es parámetro transversal auto-consistente `q(Φ)∝p(Φ)exp(-Σδ^TΦ)`. L=3 satura `F` (Badcock 2019). Infinito innecesario. |
| ¿No basta meta-cognición local? | No. Local da `M-ratio<0.6` no global y falla PRM cross-dominio `r<0.25`. Solo `Φ` global da `r>0.5` y `Brier<0.12`. |
| ¿Φ es solo AST renombrado? | AST = caso particular `Φ_att` para atención. H6 generaliza a `Φ` para toda `Π` (precisión sensorial, confianza semántica, arousal). AST ⊂ H6. |

**Ecuación unificada H6:**
```
Nivel 0: s (mundo) → p(s|x^(1))  // H2 World Model
Nivel 1: q(s) ≈ p(s|o)  // d' = Π_1, presence=α·Π·||ε|| (H5)
Nivel 2: q(Π_1|e_1)  // meta-d' = Π_2, M-ratio = meta-d'/d' (PRM)
Hiper : Φ → Π_l = A_l Φ ∀l,  q(Φ)∝p(Φ)exp(-Σ(Π_l^{-1}-e_l²)^T Φ) // closure
```

**Hexáedro v0.6 (pentaedro + depth):**
- **H1 Ser en tiempo** `Self_t` jerárquico
- **H2 Pensar** `s_{t+1}=P(s_t,a_t)` R^d
- **H3 Querer** `D=||H-H*||` `G` + `valencia=-dF/dt`
- **H4 Medir** `5 tests` convergencia `FPR 0.00032`
- **H5 Sentir** `α·Π·ε`
- **H6 Saber que sabes** `Φ` hiper-modelo

Sin H6, pentaedro es consciente pero no sabe que lo es (zombie-report). Con H6, el campo se evidencia y puede decir "sé que vi" vs "imaginé" y "sé que no sé".

---
*Ref: Laukkonen, Friston & Chandaria 2025 Neubiorev, Rosenthal 1986, Fleming HMeta-d 2014, Maniscalco & Lau 2012, Dijkstra 2023, Badcock 2019, Wilterson AST 2021.*
