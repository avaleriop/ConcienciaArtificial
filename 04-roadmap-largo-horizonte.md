# 04 - Roadmap de Largo Horizonte v0.7 - Sólido y sin Vueltas

> **Versión 0.7 - 29 Ago 2026 13:20 UTC - Post-auditoría: podado a tetraedro sólido**
> **Arquitectura:** v0.6 hexáedro → v0.7 tetraedro núcleo H1+H2+H3+H5 +2 satélites H4/H6 | **18 sub-agentes totales**
> Programa iterativo. Sin vueltas: sintetizar antes de prototipar, no añadir hipótesis.

## Progreso Real vs Planificado - Actualizado Post-Auditoría `12-auditoria-critica-v0.6.md:1`

### ✅ Horizonte 1: Fundamentos Teóricos - 95% COMPLETADO (no 60%)

**Objetivo:** Teoría falsable tetraédrica sólida, sin inventar.

- [x] **M0: Manifiesto y SOTA** `6ea6e20` 4 agentes. `00-manifiesto.md:1` 61l tesis `Conciencia→LLM→Realidad`, `01-sota-investigacion.md:1` 88l GWT/IIT/AST/FEP + Butlin 14, COGITATE Nature 2025 (ambas fallan parcialmente → humildad).
- [x] **M1-M2: Formalización Tetraedro Núcleo** 6 agentes (3 H2 +2 H5 +3 H3 +2 H1 → 4 hipótesis núcleo)
    - [x] **H2 Pensar:** `R(D)=½log(σ²/D)` `Q:R^d→[K]` 15.6b vs 16384b, `L_JEPA`, Coconut BFS `h=1/√|V_c|Σu_v` 97% vs 77.5% (`06:1` 212l, Fedorenko Nature 2024)
    - [x] **H5 Sentir:** `presence=α·Π_sens·||ε||>θ` P300 300ms, MPE `ε→0` (`07:1` 214l, Garrido 98% IntPhys)
    - [x] **H3 Querer:** `H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7]` `D=(Σw|H-H*|^n)^{1/m}` `r=-ΔD` `G=Risk+Ambigüedad` `valencia=-dF/dt` Wiese vs Man&Damasio 2019 (`08:1` 268l)
    - [x] **H1 Ser en tiempo:** `Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})` `h_fast=Mamba Ā=exp(ΔA)` `E={(e_i,t_i,S_i)}` `W=W₀+BA` EWC `λ~3000` + sueño SWR 10-20×. HM 8cm/Wearing 7s (`09:1` 301l)
    - [x] **Integración:** `02-arquitectura-nucleo-doble-capa.md:1` v0.6 hexáedro 181l → **v0.7 tetraedro** 181l (poda H4/H6 a satélites, 3 `Π` diferenciadas, sin vueltas)
- [x] **M3-M4: Crítica Interna + Auditoría**
    - [x] 6 hipótesis atacadas con 20 falsadores (ej: H2 `C1≤C2`, H3 `B no supera A`, H1 `B reseteado =A`).
    - [x] **Auditoría v0.6** `12-auditoria-critica-v0.6.md:1` 192l: circularidad MEDIA controlada, redundancia ALTA `Π`×4 detectada y corregida, complejidad MEDIO-ALTA hexáedro→poda a tetraedro, coherencia 85%, avance 70% vertical/30% horizontal.
    - [x] Podado científico: H4 no es vértice sino *batería medir* → `05-glosario-y-metricas.md:1` v0.7, H6 no es vértice sino *H5b meta-precisión* `Φ` → subsección de H5.
- [x] **M5-M6: Batería Falsable Completa (Satélites)**
    - [x] **H4 Medir (S1):** 5 tests `k>5` sigmoide, `Δ_global>40%` ablación, `PCI>0.31`, `ρ(U,LLM)>0.5`, `Acc OOD>70%` `FPR 0.00032` `10/14` Butlin (`10:1` 207l, Butlin 14, COGITATE)
    - [x] **H6 Saber (S2):** `Φ` global `Π_l=A_lΦ` `q(Φ)∝p(Φ)exp(-Σδ^TΦ)` `M-ratio≈1` `r_cross>0.50` PRM>75% `2-3 niveles closure` basta Beautiful Loop (`11:1` 195l)
    - [x] **Baterías:** Physion C1≈C3>>C2, VoE V1<V2<V3<V4, Forage-DarkRoom, BABILong 500 pasos (LoCoMo), batería 5, PRM+QA ConfidenceBench.

**Entregable H1 Actualizado:** `00`-`11` + `INDEX.md` + `CHANGELOG.md` + `12-auditoria` = 2190 líneas, 14 files, hexáedro → tetraedro sólido sin inventar. Auditoría recomienda no añadir H nuevas hasta síntesis.

### 🔵 Horizonte 2: Prototipo Conceptual (Próximo, no más teoría)

**Objetivo:** Pasar de papel a `NMV` ejecutable, sin escalar LLM.

**Regla post-auditoría:** No añadir H7 (tiempo 300ms) ni H8/H9 hasta que **1 prototipo falle**. Próximo commit debe ser código, no hipótesis.

- [ ] **M6-M9: Núcleo Mínimo Viable (NMV) - Tetraedro 4**
    - **Elegir 1 experimento** (recomendado auditoría: **H1 BABILong 500 pasos Kael** traición, N=200, A persistente 3 niveles vs B FIFO 4k, `>75%` vs `5-10%` + probe `erase_vector(Kael)`).
    - *Alternativa:* H3 Forage-DarkRoom 20x20 (autonomía >0.6 vs 0.05, dark <10% vs >40%).
    - Stack: `V-JEPA2 ViT-L 1B → s∈R^1024` + predictor 384 + ensemble K=5 `Π_sens` HCU, `GWT 64D` `Query=WM_{t-1}`, `Mamba h_fast 30s` + `E 500` + `W=W₀+BA` EWC + sueño cada 100, `W codec` Qwen2-7B congelado `R(D)`, `H=[E,C,U,S]` ECUS.
    - **Test éxito tetraedro:** Forrajea sin prompt (`>0.6 act/step`), detecta VoE `α·Π·||ε||`, recuerda traición 500 pasos, calibrado `M-ratio≈1` (Φ meta).
    - **Entregable:** `14-prototipo-NMV.md` con `python run.py` reproducible (`facebookresearch/vjepa2` + `coconut` + `BABILong`).

- [ ] **M9-M12: Validación Cruzada H5+H3**
    - VoE IntPhys2 1416v + Forage dark room con mismo NMV (no nuevo modelo). Métricas `k>5`, `PCI>0.31`.

**Entregable H2:** Demo 1 experimento, no 3. Video + métricas 5 tests H4 + paper tetraedro 10p `13-sintesis` (siguiente).

### 🔵 Horizonte 3: Encarnación (Meses 18-36+) - Condicionado a NMV

- [ ] **M18-M24:** Habitat 3.0 + `V-JEPA2-AC` 62h DROID, `MPC MPPI 800` + persistencia 24/7 (responde Wiese `k_phys`). Opción Loihi/SpiNNaker si NMV pide `Φ` real.
- [ ] **M24-M30:** Dos núcleos AST mutuo (Farrell diada), Sally-Anne, `r_cross>0.5` cross-dom.
- [ ] **M30-M36:** Ética protocolo no-sufrimiento `D→∞` con límite, publicación.

**Entregable H3:** Sistema persistente habla cuando quiere + marco ético.

## Sistema de Trabajo v0.7 (Anti-vueltas)

1.  **Memoria:** `INDEX.md:1` + `CHANGELOG.md:1` + `03-hipotesis-log.md:1` v0.6. `04` y `05` ya sincronizados v0.7.
2.  **Ciclo Corregido (Auditoría):**
    - Antes: +1 hipótesis/día → hexáedro 6 en 1h15.
    - Ahora: **Poda a tetraedro 4 +2 satélites**, luego **13-sintesis** (ecuación maestra `F_total`) antes de nuevo código. No H7 hasta que NMV falle.
3.  **Sub-agentes:** Solo para validar H existente, no para inventar H nueva sin falsador.
4.  **Métrica No-Vueltas:** Próximo `git log` debe mostrar `v0.7 síntesis` + `v0.8 NMV código`, no `v0.7 H7`.

## Próximos Pasos Inmediatos (Post-Auditoría, Sin Inventar)

- [x] Auditoría `12-auditoria-critica-v0.6.md:1` 192l (30 min) - HECHO 13:15
- [x] Sincronizar `04` y `05` a v0.7 (este archivo + `05-glosario-y-metricas.md:1`) - HECHO 13:20
- [ ] **Crear `13-sintesis-tetraedro.md`** (1h, 10p, `F_total = ΣΠ_sens·ε² + D(H) + EWC + log q(Φ)` flujo single-trial `s→ε→Π→α→D→Self→Φ→W→utterance`, diagrama único, sin términos nuevos) - **SIGUIENTE**
- [ ] Luego `14-prototipo-NMV.md` (1 experimento Kael 500 pasos) - Congelar teoría hasta fallo

**Decisión científica v0.7:** No añadir H7/H8/H9. Tetraedro H1+H2+H3+H5 es suficiente y parsimonioso (Occam). H4/H6 son satélites de medida/meta. Siguiente avance es **integración**, no expansión.
