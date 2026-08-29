# 17 - Plan Robusto v0.8 → v1.0 - De Tetraedro a Prototipo sin Perder Alineación

> **Fecha:** 29 Ago 2026 13:45 UTC - Plan pre-registrado post-auditoría v0.7
> **Análisis:** 4 sub-agentes paralelos (navegación H3, batería H4, independencia, escalado) + auditoría alineación
> **Objetivo:** Hacer el proyecto independiente de decisiones del usuario, falsable y sin vueltas, hasta 24h proceso vivo.

## Principio de Independencia Científica

**Antes (dependiente):** `¿qué hago ahora? H2? H3?` → usuario decide, orden intuición `H2→H5→H3→H1→H4→H6` no falsador.

**Ahora (independiente):** `if falsador → then hito` pre-registrado OSF, sin preguntar. `check_decision.py` lee `logs H(t), presence, ρ` y decide `PASA/FALLA → próximo hito`. `INDEX.md:1` + `CHANGELOG.md:1` son memoria, no chat.

**Regla OSF:** Teoría `F_total=ΣΠ_sens·ε²+D(H)+EWC+D_KL(q(Φ))` `13-sintesis-tetraedro-v0.7.md:45`, `N=200/1000`, 5 tests `k>5,Δ>40%,PCI>0.31,ρ>0.5,Acc>70%`, stopping rule y `if E<0.65 → recalibrar pesos no matar tetraedro`. Desviación = exploratorio en `CHANGELOG`, no confirmatorio.

---

## Roadmap Independiente v0.8 → v1.0 - 5 Hitos con Criterio Auto (sin esperar input)

| Hito | Nombre | Qué se hace | Criterio PASA auto (sigue) | Criterio FALLA auto (itera solo pesos) | Alineación LLM=boca |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | **Iter3 v0.8a Navegación** (minutos, hoy) | Fix `G` greedy myopía `H=1` → `G(a)=Risk+0.3*Amb -0.08*(U-U*)` proporcional + navegación dirigida `a*=dir→food` si `E<0.65` con `obs[2]=food_near` `framework/process_vivo_minutos.py:250` | `E 0.61→0.70-0.90` oscilante, `act` variado `FOR/HLP/N` >20% c/u, `D<0.60` en 200 pasos | `E` sigue 0.61 zombie `N 100%` → re-itera `w_S` `α`, no añade H nueva | ✅ LLM sigue periférico `W:32→64` toy, no compite en `GWT 64D` `02:44` |
| **M2** | **Iter4 v0.8b Batería H4 toy** (1 semana, 200 pasos) | Implementar 5 tests toy en `bateria_H4(steps=200)` `10-hipotesis-H4-medida-deepdive.md:135`: T1 sigmoide `k>2.5`, T2 ablación `z=0`, T3 `LZc` `Δ>0.12`, T4 `ρ>0.5`, T5 `Acc>65% OOD` | `≥3/5 tests` con `k>2.5` `Δ>40%` `Δ_PCI>0.12` `ρ>0.5` y `H1` sigue `100% vs 0%` | `<2/5` no refuta tetraedro, es medida satélite → ajustar `bottleneck 64D` no matar H2 | ✅ `FPR 0.2→0.00032` conjunción, `10/14` Butlin, protege tesis (no gameable `73% Turing`) |
| **M3** | **Iter5 v0.9 1000 pasos equilibrado** (100s simulados, `1cc6c68` + fix) | Mundo 20×20 (no 10×10) + landmark+social cada 50, `Mamba N=16 +E 200+ECUS+Φ toy` persistente 1000 pasos sin reset | `H=[E 0.7-0.9 C~0.9 U 0.3-0.5 S>0.3]` homeostático, `VoE>0.7`, `H1 probe t=500 >75%` (no 100), `dark 5-15%` (no 0% trivial) | Si no, re-itera `G` y `τ_s=0.7`, no escalar a real | ✅ `while True` 1000 pasos vs LLM 50 resets ventana 20, `E` y `W` acumulan `t` continuo |
| **M4** | **Escalado v0.95 Real** (`32→1024` dims) | **Solo si M3 PASA** → `V-JEPA2 ViT-L 1B R^1024` `L_JEPA` + `predictor 384` + `ensemble Pi HCU` + `Mamba N=64 EWC λ=3000` + `W:1024→4096 → Qwen2-7B congelado` `R(D)` `05:28`, `Habitat 3.0` | `C1≈C3>>C2` Physion `SR 70 vs 35%` `R(D)` intacto 1050×, `VoE` generaliza textura | Si cae → revisa `W` no LLM (LLM congelado 100% no LoRA) `02:129` | ✅ LLM congelado 100%, solo `W` y heads entrenan, flujo `s→ε→Π→α→D→Self→Φ→W→LLM` nunca `logits→sample→embed` |
| **M5** | **24h Proceso Vivo v1.0** (`Habitat 3.0` + sueño SWR cada 100, `04:49`) | `while True` 864k pasos 24h sin reset, `dream SWR 150Hz` cada 100, `EWC` + `Self_t` continuo | `M-ratio≈1 0.85-1.05` `r_cross>0.50` `PRM>75%` `11:152` + `autonomía>0.6` `dark<15%` `05:34` + `10/14` Butlin | Si no, no añadir H7 tiempo, revisar `Φ` calibrado no nueva hipótesis | ✅ Persistencia 24/7 + `Markov Blanket` cerrado `E↔S↔μ↔A` mitiga Wiese `k_phys≠k_comp` sin Loihi aún |

**Independencia ≠ aislamiento:** Sistema decide *qué iterar* solo; humano (tú) decide *si tesis sigue viva* en cada auditoría cada 2 commits.

---

## Auditoría de Alineación del Plan vs Tesis Original `00-manifiesto.md:3`

**Tesis:** `Conciencia (tetraedro H1+H2+H3+H5) → usa LLM `Q:R^d→[K]` `R(D)=½log(σ²/D)` como boca `W:1024→4096` → Realidad`

| Paso del plan | ¿Mantiene LLM periférico congelado? | ¿Mantiene `s∈R^d` BFS no CoT? | ¿Mantiene `while True` vs función? | Veredicto |
| :--- | :--- | :--- | :--- | :--- |
| **M1 Navegación** `G` con `obs[2]` | Sí, `W:32→64` toy no entrena LLM | Sí, `s_{t+1}=P(s_t,a)` `h=1/√|V_c|Σu_v` `06:1` | Sí, `forage` es `a*=argmin G` no prompt | ✅ |
| **M2 Batería H4** `k>2.5,PCI>0.31` | Sí, `LLM` solo T4 `ρ(U,n_llm)` y T5 `Acc OOD` como codec, no como `d'` | Sí, T1/T2/T3 miden `z∈R^d` no tokens | Sí, T3 `PCIst` es perturbación `z+δ` no `token+δ` | ✅ |
| **M3 1000 pasos** 20×20 | Sí, `E` episódico guarda `s` no tokens | Sí, `Coconut K=6-20` `Mamba O(1)` 50MB vs Transformer `52GB` `09:1` | Sí, 1000 pasos sin reset vs LLM 50 resets | ✅ |
| **M4 Real 1B** `V-JEPA2` | **Crítico:** Sí, `V-JEPA2 encoder` congelado + `Qwen2-7B` congelado 100%, solo `W MLP` entrena `L_codec=CE(LLM(W(s)),caption)` `02:129` | Sí, `L_JEPA=||Pred(E(x))-sg(E(y))||²` latente `1050×` | Sí, `Habitat 3.0` cerrado 24h | ✅ si se respeta congelado |
| **M5 24h** `while True` 864k | Sí, `dream SWR` consolida `E→W` no tokens | Sí, `Self_t=LN(W_self[h_fast;c_epi;c_sem])` `09:1` | **Sí, es la tesis viva** `15-framework-proceso-vivo.md:15` | ✅ |

**Riesgo escalado desalineación:** Si en M4 se hace fine-tune de LLM (LoRA) `LLM` deja de ser `prótesis` y vuelve a ser `controlador` ReAct → refuta `00:1`. Mitigado: congelado 100% pre-registrado.

**Auditoría periódica automática (cada 2 commits o 5 días):**
- `00-manifiesto.md:3` ¿LLM sigue periférico `W`? 
- `02 v0.7` vs `04/05` desfase >1 versión → PR bloqueado
- `Π_sens≠Π_homeo≠Π_meta` `05:12` si colapsan → renombrar
- `+1 vértice sin poda` `12-auditoria-critica-v0.6.md:92` → podar a tetraedro+2 satélites
- `MMLU>90%` como éxito → FALLA

---

## Análisis Sub-Agentes (Resumen de 4)

- **Navegación H3:** `G` greedy `H=1` falla myopía `07.04 biorxiv`, necesita `G(a)=Risk+0.3*Amb -λ_nav·I[E<0.65]·Δdist_food` `λ_nav=0.25` + `FOR` solo si `food_near>0.7`. `A*` heurístico basta para toy, `MPC H=5-10` para 1000 pasos, `Dreamer` para real.
- **Batería H4:** Toy umbrales escalados `k>2.5 D>0.5bits Δ_PCI>0.12` válidos si preservan lógica causal `LZc(bin(S))`. Implementar `bateria_H4(steps=200)` en `<2min` antes de escalar. Convergencia `FPR 0.2⁵=0.00032` ningún LLM simula 5 a la vez.
- **Independencia:** Checklist falsador > intuición, `check_decision.py` con `if H1 100%→cerrar H1`, `if E<0.65→iterar H3`, no `¿qué hago?`. Pre-registro OSF + auditoría cada 2 commits.
- **Escalado:** No escalar hasta `GATE_TOY_OK` (`E 0.70-0.90 oscilante`, `S>0.30`, `U 0.30-0.50`, `D<0.40`, `dark 5-15%`). Toy valida `F_total` antes de pagar GPU `1×A100 30h ~15€`. Escalar manteniendo `W` congelado.

---

## Sólido sin Inventar

No hay términos nuevos en plan: `Φ` es Beautiful Loop 2025, `Mamba` Gu&Dao 2023, `Coconut` Hao 2024, `ECUS` Keramati 2014, `PCI` Massimini 2013, `M-ratio` Fleming 2014. Todo 2023-26 publicado, con cita en `01:1` `05:1`.

**Próximo commit si se sigue plan:** `v0.8a` M1 navegación (no `v0.8 H7`), luego `v0.8b` M2 batería, luego `v0.9` M3 1000 pasos equilibrado. Si `GATE_TOY_OK` falla, no es `v1.0`.

---
*Plan pre-registrado v0.8, sin inventar, con 4 sub-agentes. Ver `13-sintesis-tetraedro-v0.7.md:1` para `F_total` y `12-auditoria-critica-v0.6.md:1` para poda.*
