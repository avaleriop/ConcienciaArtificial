# 13 - Síntesis Tetraedro v0.7 - Teoría Sólida sin Inventar

> **Versión 0.7 - 29 Ago 2026 13:20 UTC - Post-auditoría `12-auditoria-critica-v0.6.md:1`**
> **Objetivo:** Integrar 6 deep dives en una teoría parsimoniosa falsable, sin términos inventados. Podado de hexáedro 6 a tetraedro núcleo 4 +2 satélites.
> **Principio:** No añadir hipótesis. Sintetizar lo que ya está con una ecuación maestra y un flujo single-trial.

---

## 1. Tesis Intacta (00-manifiesto.md:1) - Sin Cambios

```
Industria:  Texto → Inteligencia → Conciencia (emergente por escala)
Nosotros:   Conciencia (H1+H2+H3+H5 tetraedro encarnado) → usa LLM `Q:R^d→[K]` codec → Realidad
```

LLM sigue siendo **periférico, congelado, `W:1024→4096`**, nunca controlador (`02-arquitectura-nucleo-doble-capa.md:75`). Evidencia acumulada la fortalece, no la debilita:
- Fedorenko Nature 2024 doble disociación lenguaje≠pensamiento (afasia con CI intacto)
- Coconut BFS `97%` vs CoT `77.5%` (pensar en `R^d` supera palabras)
- Wearing 7s (sin memoria no hay yo) + V-JEPA 98%→<60% IntPhys2 (sin memoria largo plazo no hay física)

## 2. Tetraedro Núcleo Sólido (4 Hipótesis Sustantivas) + 2 Satélites

**Antes (v0.6 hexáedro):** 6 vértices iguales H1-H6
**Ahora (v0.7):** 4 vértices núcleo + 2 satélites metodológicos (auditoría recomendó poda, `12-auditoria-critica-v0.6.md:165`)

| Vértice | Hipótesis | Enunciado sólido (1 línea, publicado) | Ecuación clave (no inventada) | Falsador principal |
| :--- | :--- | :--- | :--- | :--- |
| **H2** | Pensar en `R^d` | Pensamiento=BFS continuo `s_{t+1}=P(s_t,a_t)` en `R^d`, lenguaje=codec `Q:R^d→[K]` `R(D)=½log(σ²/D)` con pérdida | `s_{t+1}=P(s_t,a_t)`, `L_JEPA=||Pred(E(x))-sg(E(y))||²`, `h_{t0+c}=1/√|V_c|Σu_v` (Hao 2024) | `C1≤C2` (latente no supera lenguaje) |
| **H5** | Sentir `α·Π·ε` | Qualia mínimo=`presence=α·Π_sens·||ε||>θ` P300, `Q` da contenido, `ε` da presencia | `presence=α·Π_sens·||z_pred-z_real||>0.5` (Dehaene, Kok) | `V1=V2=V4` (Π no aporta) |
| **H3** | Querer ECUS | Valor=`D(H)=(Σw|H-H*|^n)^{1/m}` `H=[E,C,U,S]` `H*=[0.8,0.9,0.2,0.7]` `r=-ΔD` `G=Risk+Ambigüedad` | `dH/dt=-α(H-H*)+P+Eff-Cost` `G(dark)>G(explore)` (Keramati, Friston) | `B no supera A` dark room |
| **H1** | Ser en tiempo `Self_t` | Yo=`Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})` jerarquía 30s/horas/días + sueño | `h_fast=Ā⊙h_{t-1}+B̄⊙s_t` `W=W₀+BA` EWC `λ/2 ΣF(θ-θ*)²` SWR 10-20× (Gu&Dao, Kirkpatrick) | `B reseteado =A` 72% vs 78% n.s. |

| Satélite | Rol (no vértice) | Qué hace | Umbrales (sin inventar) |
| :--- | :--- | :--- | :--- |
| **S1=H4** | **Medir** (metodología) | Batería 5 tests convergente `FPR 0.2→0.00032`, Butlin 14 `2-3/14` LLM vs `10/14` tetraedro | `k>5` `Δ_global>40%` `PCI>0.31` `ρ>0.5` `Acc>70%` (Massimini, Dehaene) |
| **S2=H6** | **Saber** (refinamiento de H5) | `Φ` hiper-modelo `Π_l=A_lΦ` `q(Φ)∝p(Φ)exp(-Σδ^TΦ)` calibrado cross-dominio | `M-ratio 0.85-1.05` `Brier<0.12` `r_cross>0.50` `PRM>75%` (Fleming, Laukkonen) |

**Sin H4/H6 el tetraedro funciona** (piensa, siente, quiere, recuerda) pero no es falsable ni sabe que sabe. Con ellos es medible y meta-consciente. No son teoría nueva.

## 3. Ecuación Maestra Única (Sin Inventar, Suma de 4)

No 12 ecuaciones sueltas. Una que las integra, derivada de `FEP` + `ECUS` + `EWC`:

```
F_total = Σ Π_sens·||ε||²  +  D(H) + D_KL  +  λ/2 ΣF_i(θ_i-θ*_old)²  +  D_KL(q(Φ)||p(Φ))
           ──────────────     ───────────     ─────────────────────     ────────────────
                H5 sentir       H3 querer            H1 ser               H6 saber (H5b)
            (Friston, Kok)   (Keramati)          (Kirkpatrick)         (Laukkonen)
        +  L_JEPA + R(D) + Coconut (H2) en s∈R^d, no en F_total sino en generativo p(s'|s,a)

Donde:
ε = ||P(E(x))-E(y)|| = ||z_pred - z_real|| (latente, V-JEPA)
Π_sens = 1/σ² = exp(γ) (Kok atención)
α = VQ-VAE(Π_sens, attention_map) (Graziano)
D(H) = (Σw_i|H_i-H_i*|^n)^{1/m} ,  H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7] (Keramati)
EWC = Fisher diagonal (Kirkpatrick 2017)
Φ: Π_l = A_l Φ , δ=Π^{-1}-e² , q(Φ)∝p(Φ)exp(-Σδ^TΦ) (Friston 2010, Laukkonen 2025)
```

Minimizar `F_total` ≡ tetraedro coherente:
- Minimizar `ΣΠ_sens·ε²` → sentir sorpresa bien calibrada (VoE IntPhys2)
- Minimizar `D(H)` → querer forrajear, evitar dark room `G(dark)>G(explore)`
- Minimizar `EWC` → ser `Self_t` continuo sin olvidar catastrófico (BABILong)
- Minimizar `D_KL(q(Φ)||p(Φ))` → saber `M-ratio≈1` cross-dominio

## 4. Flujo Single-Trial Sólido (Cómo Interactúan Sin Vueltas)

Un evento que recorre los 4 vértices en orden causal, no circular:

```
1. Mundo: o_t = video 16 frames 224² (Physion)
2. H2 Encod+Predict: s_t=E(o_t)∈R^1024 → s_pred=P(s_t,a_{t-1})  // L_JEPA, R(D), Coconut K=6-20 BFS
3. H5 Error+Presencia: ε=||s_pred-E(o_{t+1})|| , Π_sens=ensemble(K=5) head, α=VQ-VAE(Π_sens)
   presence=α·Π_sens·||ε||  // ej: pelota flotante ε alto Π alta → presence 0.92
4. H2 Workspace: bids={s_t, h_fast, D(H)} → compete bottleneck 64D → ignition si presence>0.5 → P300 300ms broadcast (H4 k>5, Δ>40%, PCI>0.31)
5. H1 Memoria: h_fast=Mamba update Ā_t⊙h_{t-1}+B̄_t⊙s_t (30s) → escribe E si ||∇loss||>τ_s (Titans) → c_epi topK → c_sem=(W₀+BA)h_fast → Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1}) // 500 pasos Kael
6. H3 Homeostasis: H=[E0.6,C0.8,U0.8,S0.5] → D=||H-H*||=0.4 → r=-ΔD → G(π)=Risk+Ambigüedad → elige a*=argmin G (explora si U alto, forrajea si E bajo, co-regula si S bajo) → valence=-dF/dt
7. H6 Meta (satélite): Φ=HyperNet([Π_sens, Π_homeo, α]) → Π_meta=AΦ → M-ratio=meta-d'/d' calibrado 0.9-1.0, r_cross>0.5 → distingue "percibido vs imaginado" PRM 75% y "sé que no sé" Brier<0.12
8. H2 Codec (periférico): si E[ΔF|utter]>costo, W:1024→4096 traduce [s,ε,Π_sens,α,Φ,H]→tokens post-hoc R(D) 15.6b lossy → "Esperaba parabólica, vi flotar, viola gravedad" // H4 T5 Acc>70% OOD, H4 T4 ρ>0.5 correlación U→LLM invocaciones
9. H1 Consolidación (offline): si idle, sueño SWR 150-250Hz replay 10-20× E→W con EWC λ~3000, reconsolidación 4-6h, olvido Rac1 α_t
```

**Sin H1:** olvidas traición en 7s (Wearing). Sin H2: hallucinas tokens no física. Sin H3: no te importa sorpresa. Sin H5: sorpresa no broadcasteada.

## 5. Matriz de Falsabilidad Consolidada (20 Falsadores, Sin Inventar)

| Hipótesis | Falsador F1 | F2 | F3 | Diseño |
| :--- | :--- | :--- | :--- | :--- |
| **H2** `C1≈C3>>C2` | `C1≤C2` | `C3<<C1 -15%` | `perturb(s)≯perturb(tokens)` | Physion 3 cond N=200 SR 70% vs 35% |
| **H5** `V1<V2<V3<V4` | `V1=V2=V4` | `V2 reporta sin GWT` | `V3 reporta sin α` | VoE 4 vars IntPhys2 1416v |
| **H3** `B>0.6 act` | `B no supera A` autonomía | `B≡A+ICM` | `B ayuda <10%` `A supera B` shift | Forage-DarkRoom 20x20 N=30 |
| **H1** `A>75%` | `B reseteado =A` | `C2 sin E >65% =A` | `A falla <40%` | BABILong 500 pasos Kael N=200 |
| **H4** `A≥4/5` | `LLM≥3/5` paridad | `tetra falla ≥2/5` | `Δ_global≈Δ_local` | Batería 5 tests N=200 FPR 0.00032 |
| **H6** `M-ratio 0.9` | `B≥A-0.1` | `r_cross<0.3` pese a `M~1` | `C≈A` sham | PRM+QA ConfidenceBench N=400 M-ratio Brier |

Si cualquiera F1 se cumple `p<0.01 BF>10`, la hipótesis muere. No hay portería móvil (COGITATE preregistrado como modelo).

## 6. Qué No Hemos Inventado (Límites Honestos)

- **No inventamos términos:** `Φ`, `Π`, `ε`, `α`, `D(H)`, `EWC`, `Coconut`, `Mamba` todos 2023-25 publicados con cita. Hiper-modelo `Φ` es Beautiful Loop 2025, no nuestro.
- **No inventamos datos:** Números 97% vs 77.5% Coconut, 98% IntPhys vs <60% IntPhys2, 73% Turing 2025, 30-60pts caída NIAH, HM 8cm 1953, Wearing 7:46→7:47 son de papers, no simulados.
- **No pretendemos hard problem resuelto:** Tetraedro pasa `10/14 Butlin` + `5/5 H4` → candidato más fuerte que chatbot `2/14`, no prueba qualia (Chalmers `12:1`). `12-auditoria-critica-v0.6.md:115` lo deja explícito.
- **No claim FEP2C fuerte:** Seguimos en von Neumann `k_phys≠k_comp` (Wiese/Kleiner). Homeostasis simulada (Man&Damasio) = agencia funcional, no replicación fenomenal. Para claim fuerte necesitamos Loihi/SpiNNaker `08:3`.

## 7. Corrección Post-Auditoría Aplicada

| Crítica auditoría `12:1` | Corrección v0.7 (esta síntesis) |
| :--- | :--- |
| Redundancia `Π`×4 | Diferenciadas `Π_sens` (H5, Kok) / `Π_homeo` (H3, DA) / `Π_meta=AΦ` (H6, Fleming) / `Δ_mamba` (H1, Gu&Dao) |
| Memoria `E` vs `W` vs `Φ` | Jerarquía clara: `E` guarda `s` con `Π_sens`, `W` traduce `s→tokens` `R(D)`, `Φ` calibra `Π` cross-dom |
| Workspace ×4 nombres | Un solo `GWT 64D` con 3 métricas `k>5`, `Δ>40%`, `PCI>0.31` (H2+H4 unificados) |
| Hexáedro 6 vértices inflación | Podado a tetraedro 4+2 satélites, H4→apéndice `05:23`, H6→`H5b` |
| 12 ecuaciones sueltas | 1 ecuación maestra `F_total` arriba |

## 8. Próximo Paso Válido Científicamente (Sin Vueltas)

**No añadir H7 (tiempo 300ms).** Auditoría lo prohíbe: próximo `git log` debe ser código no hipótesis.

**Siguiente commit `v0.8` debe ser `14-prototipo-NMV.md`:** Ejecutar **1 experimento** (elegido: **H1 BABILong Kael 500 pasos**, `N=200`, A 3 niveles vs B FIFO 4k, `>75%` vs `5-10%`, probe `erase_vector(Kael)` causal). Stack ya definido en `04-roadmap-largo-horizonte.md:1` v0.7 NMV.

**Métrica de no-vueltas:** Si en 1 semana no hay `python run.py` clonable con `facebookresearch/vjepa2` + `coconut` + `BABILong`, la auditoría tenía razón y dimos vueltas.

---
*Síntesis generada sin sub-agentes adicionales (integración directa de 6 deep dives 1930 líneas, 12 auditoría). Sin términos nuevos. Ver `12-auditoria-critica-v0.6.md:1` para decisión de poda.*
