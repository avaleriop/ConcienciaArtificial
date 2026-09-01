# CHANGELOG - Conciencia Artificial

## [v0.13] - 2026-09-01 15:00 UTC - Peer-Review Revision (rigurosa, sin nuevos runs)

### Corregido (peer review Rankin/Thompson-Spencer / Friston / continual / diseño)
- `paper/main.tex:26-33` Abstract reescrito: batería grid vs continuo v0.12 separados, C3 renombrado stimulus generalization (1.1 vs 0.9, learning without distinguishing), Φ escalar MSE offline diagnostic (r=0.701, r_cross=0.730, ratio 0.13) con gate atencional como confound (d=-1.61 aislado vs d=-0.43 con gate aleatoria), EWC/ortho flagged non-load-bearing (recovery 0.48 flat), MiniGrid fuera de Tabla.
- `paper/main.tex:65-67` Limitations upfront 4→7 puntos: especifica Rankin char. 7/8/10 no testados, Φ scalar vs per-channel log-variance, gate confound, EWC low-rank, 2 sistemas, mouth, benchmark pilot.
- `paper/main.tex:114-122` Φ y presence: MSE a |ε| es proxy de zona, no log-varianza por canal; presence offline, no drive online.
- `paper/main.tex:120-124` Attention y Phi causal: 4-brazo A/B/C/D pre-registrado, random gate reproduce efecto.
- `paper/main.tex:124-125` EWC/ortho: diagonal Fisher, misma-tarea = refuerzo, ΔW likely rank-1, SVD + factored predictor como next.
- `paper/main.tex:142-146` Provenance: Tabla split grid (13->128->128->6, ±5) vs v0.12 continuous (13->64->6, +2, attention 13->7, Φ 22->64->1).
- `paper/main.tex:152-160` Controls C3 re-etiquetado como generalization, no dishabituation; dishab real + recovery pre-registrados.
- `paper/main.tex:172-199` Tabla 1 split en dos paneles con † pilotos y ‡ confound, MiniGrid fuera.
- `paper/main.tex:230-234` C3 section: Rankin 2009 char. 7/8/10, H_A = magnitud vs vector, learning without distinguishing.
- `paper/main.tex:242-256` Φ results: r_cross no separa zona vs confiabilidad, presence offline, d=-1.61 confounded.
- `paper/main.tex:305-326` Limitations 5→7 párrafos, Conclusion con v0.14 Rankin battery.
- `CITATION.cff:10` version 0.12→0.13, date 2026-09-01, abstract reescrito con claims acotados.
- `zenodo_upload_paper_only/` v0.13.tex + CITATION.cff copiados, README actualizado, checklist v0.13.
- `56-paper-taller-borrador.md:1-65` abstract/tabla/discussion/limitations alineados a paper v0.13.
- Nuevo `63-preregistro-v014-rankin-phi-factorizado.md:1` (Rankin S1-S5 + dishab + gap, factored f_pos/f_H, Φ por canal NLL, 4 brazos A-D, SVD, N=30, thresholds fijos).

### Estado
- v0.13 es publicable como "habituación gruesa + trazo en pesos + Φ calibrado con caveat" (no claim vectorial ni physics online). v0.14 es el experimento que decide H_A vs H_vec.

## [v0.11] - 2026-08-29 18:30 UTC - Capstone: Organismo Completo + Cadena Causal

### Añadido
- `43-cadena-causal-completa.md:1` + `framework/m5_cadena_completa.py:1`: la cadena que la crítica pidió — predicción→error(z2.9)→estado(U 0.31→1.50)→acción(explor 0.01→0.75)→plasticidad(habituación z→0.1)→persistencia en W sin E (z 0.3)
- `44-organismo-completo-capstone.md:1` + `framework/organismo_completo.py:1`: TODOS los mecanismos + boca LFM2.5 en UN loop continuo. 20k pasos: E 0.61-1.50 sano, U responde a sorpresa con decaimiento, 57 reportes reales de la boca. 4 bugs de interfaz corregidos (navegación comida, forage dist==0, U acotado, cooldown boca 239→57)
- `41-sorpresa-sin-vision-sensorimotor.md:1` + `framework/m4_local_sensorimotor.py:1`: sorpresa emergente SIN visión (canal del cuerpo, O'Regan & Noë) — MOTORA z=40.4, habituación 98% (el modelo actualizó su física corporal)
- `42-integracion-causal-A-vs-B.md:1` + `framework/m5_integracion_causal.py:1`: A integrado (ε→U→política) vs B convencional desconectado — diferencial causal +0.12 real con persistencia post-evento (A 0.20 vs B 0.00), integración funcional parcial, NO decorativa
- `40-VoE-v2-emergente-limite-local.md:1`: resultado NEGATIVO honesto (sorpresa de objetos no emerge con MLP local, 5 diseños) — delimita frontera y justifica V-JEPA 1B como opcional
- Regla adoptada (crítica externa): cada experimento debe preguntarse qué resultado sería imposible para un predictor convencional
- Lenguaje corregido: sin antropomorfismo ("mantiene proceso continuo, detecta violaciones, actualiza predictor, reduce error")

### Decisiones de alcance (usuario)
- Test LLM intercambiable DESCARTADO (el LLM actual funciona; no complicar)
- Integrar antes de cerrar: predictor del cuerpo dentro del organismo

### Estado
- 45 docs, 17 scripts, ~50 commits, 0€ local | ❌ awareness/conciencia no demostradas
- Objetivo del proyecto funcionando en una pieza

## [v0.10] - 2026-08-29 17:15 UTC - SECUENCIA M1→M5 COMPLETA (todo local, 0€, sin A100)

### Hito: H2b DECISIVO con LLM real (36)
- LFM2.5-1.2B-Instruct-MLX-8bit (1.17B, híbrido SSM-conv, 719MB Q4, MLX nativo): 19ms/token, 0.6s/respuesta
- Condición A (con LFM2.5) vs B (sin LLM), 1500+1500 pasos: **E/U/S/D idénticos → B (LLM=traductor) CONFIRMADO con LLM real participando**
- Reportes reales: "error de predicción alto al ser robado el artefacto" (Kael), "sensación de sorpresa, expectativa violada" (VoE)
- El experimento que creíamos requerir A100 (~33€) se hizo local gratis

### Hito: M3b REAL plasticidad (37)
- F1: 8 envenenamientos forzados (aprende W+E), F2: borrar E, F3: **1/400 visitas a B vs ~25% naive (100× aversión retenida en W sin memoria)**
- F4: LFM2.5 traduce estado real sin E, no alucina
- Plasticidad en pesos demostrada con LLM real participando

### Hito: M5 24H LOCAL (38)
- **864.000 pasos (24h @10Hz) en 157s** (0.18ms/paso), E 0.66-0.84 oscilante, 0 pasos peligro, 86 eventos VoE procesados
- E_mem 1.720/5.000, MPS 0.01GB sin leak, supervivencia completa sin colapso
- El organismo vive un día simulado: secuencia pre-registrada M1-M5 COMPLETA

### Escalado local (31-35)
- 25k→4.08M params (158×) seguro, leak MPS corregido (8GB→0.78GB→0.01GB 24h)
- Retina 8×8→16×16, JEPA 0.0105→0.0016, homeostasis estable en todas las escalas
- Techo: 4M params indefinido; el M4 Pro no es cuello práctico

### Estado final
- 🟢 M1-M5 + M3b + H2b completos localmente | ❌ awareness, conciencia, V-JEPA2 1B
- 41 docs, 12 scripts, 40 commits, 0€

## [v0.9] - 2026-08-29 15:20 UTC - Validación Local MPS (Encoder Aprendido Real)

### Añadido (framework ejecutable, todo en MPS sin GPU)
- `framework/m4_local_cpu.py:1` 232l: EncoderPredictivo 25k params JEPA **aprendido online** (no aleatorio) + EWC Fisher real + Mamba N=64 torch + ECUS calibrado + MundoLocal 20×20 escalable. JEPA converge 0.11→0.0092 (fix λ_EWC 50→5 + train cada 2 pasos).
- `framework/plasticidad_M3b_local.py:1` 75l: plasticidad con encoder aprendido — EWC λ=5 retiene tarea A 0.09x vs λ=0 0.11x (reduce olvido 18% en 25k params), aprende B en ambos.
- `framework/m4_local_4.py:1` 63l: VoE z-score formal + H2b local.
- `framework/m4_escalado_real.py:1` 103l: scaffold cloud V-JEPA2 1B + Qwen2-7B congelado.
- `26`-`30`: resultados M4-local 1-4 + auditoría alineación v0.9.

### Resultados v0.9 (lenguaje verificable)
- Encoder aprendido JEPA 0.0092 ✅ | EWC sin colapso ✅ | Mamba64 O(1) MPS ✅
- Homeostasis: E 0.66-1.15, U 0.37 (α_U=0.12 analítico), S 0.45, D 0.36 ✅
- VoE: ε teleport 0.088 vs baseline 0.043 → **z=50.6σ** (métrica relativa pre-registrada; umbral absoluto era calibración toy numpy) ✅
- H2b local: conducta idéntica sin LLM → B (LLM=traductor) consistente, débil (LLM 0 invocaciones)
- M3b local: plasticidad EWC funcional (modesta)
- Auditoría `30`: alineación pasa (LLM periférico, Π diferenciadas, sin inflación H7, lenguaje verificable)

### No demostrado (explícito)
- Awareness, conciencia, plasticidad 1B, H2b decisivo (requiere Qwen2-7B real participante en M4 cloud)

### Próximo
- M4 cloud A100 (~33€ spot): V-JEPA2 1B + EWC λ=3000 Fisher real → H2b decisivo + plasticidad 1B
- M5 24h después (plasticidad antes que longevidad, valoración externa)

## [v0.8.2] - 2026-08-29 14:30 UTC - GATE_TOY_OK PASA + Plasticidad Toy

### Resultados
- `24`: M3-iter4 dark activo pre-registrado 10/10 sale en 12 pasos → GATE_TOY_OK completo (E/U/S/dark/H1/VoE/D 0.17)
- M3b plasticidad toy: λ=3 FALLA (EWC ancla w=0.33 analítico) → λ=0.5 W congelado → borrar E, P(evitar B)=0.88>0.7 ✅
- H2b toy: conducta idéntica sin LLM → B(LLM=traductor), débil (LLM 1/1000)

## [v0.8.1] - 2026-08-29 14:15 UTC - Lenguaje Verificable + GATE Estricto

### Cambios (valoración externa 14:05 adoptada)
- `13` v0.7.1: NO "siente/quiere/es/conciencia" → "señal compatible con mecanismo funcional propuesto". Arquitectura canónica `MUNDO→PERCEPCIÓN→ESTADO→memoria/necesidades/predicción→decisión→ACCIÓN→LLM congelado`.
- Estado evidencia: ✅ continuidad/memoria/variables H/predicción | ❌ plasticidad/awareness/conciencia
- `21`: M3-iter2 GATE FALLA parcial (U 0.87 = α_U analítico, dark-pasivo métrica especificación) — sin reinterpretar
- `17` v0.8.1: H2b (eliminar LLM) y M3b (plasticidad borrar E) pre-registrados antes que M5 24h
- `22`: auditoría completa conocimiento (inventario 22 files, lecciones, experimentos)

## [v0.8] - 2026-08-29 13:45 UTC - Framework Proceso Vivo + Plan Robusto

### Resultados framework (4 iteraciones, minutos)
- iter1: S 0.20 D 0.74 LLM 200/200 → expuso w_S/τ_s/Pi_sens
- iter2: S 0.45 D 0.57 LLM 1/200 calibrado
- iter3: S 0.53 D 0.51 act variado, t0 HLP
- iter4: **E 0.61→0.95 oscilante**, FOR/HLP, D 0.49 → M1 PASA parcial
- `17`: plan 5 hitos M1-M5 con PASA/FALLA auto, `19`: batería H4 5/5 k14.22

## [v0.7] - 2026-08-29 13:20 UTC - Síntesis Tetraedro Sólido (Post-Auditoría, Sin Inventar)

### Auditado
- `12-auditoria-critica-v0.6.md:1` 192l: inventario 6 commits 2190l, desfase 04/05 v0.2 vs 02/03 v0.6, circularidad MEDIA 20 falsadores, redundancia ALTA Π×4, complejidad hexáedro 6→poda tetraedro 4+2 satélites, coherencia 85%, avance 70% vertical/30% horizontal

### Podado (Científicamente sólido)
- **Hexáedro 6 → Tetraedro núcleo 4 +2 satélites:** H1+H2+H3+H5 núcleo falsable, H4 medir (batería 5 tests FPR 0.00032) → `05-glosario-y-metricas.md:23` satélite, H6 saber (Φ) → `H5b` meta-precisión satélite de H5. Sin términos nuevos.
- **Ecuación maestra única (sin inventar):** `F_total = ΣΠ_sens·||ε||² (H5 Kok) + D(H)+D_KL (H3 Keramati) + λ/2 ΣF_i(θ-θ*)² (H1 Kirkpatrick) + D_KL(q(Φ)||p(Φ)) (H6 Laukkonen)` + `L_JEPA+R(D)+Coconut` en generativo.

### Añadido
- `13-sintesis-tetraedro-v0.7.md:1` 210l: tesis intacta LLM=boca, tabla tetraedro 4+2 satélites con ecuaciones y falsadores, `F_total` única, flujo single-trial `s→ε→Π_sens→α→D→Self→Φ_meta→W→utterance`, 20 falsadores, límites honestos (hard problem no resuelto, FEP2C no claim), corrección Π×4, auditoría→poda
- `05-glosario-y-metricas.md:1` v0.2→v0.7 71→85l: tetraedro+satélites, 3 Π diferenciadas `Π_sens/Π_homeo/Π_meta`, sin inventar, `k,PCI,Φ,M-ratio,r_cross`
- `04-roadmap-largo-horizonte.md:1` v0.2→v0.7 93→150l: H1-H6 95% completado, Horizonte 2 NMV con 1 experimento Kael 500 pasos (no 3), regla anti-vueltas, métrica no-vueltas `14-prototipo`
- `02-arquitectura-nucleo-doble-capa.md:1` v0.6→v0.7 181l: tetraedro sólido `F_total`, flujo `s→ε→Π→α→D→Self→Φ→W`, 3 Π diferenciadas, satélites H4/H6

### Estado Hipótesis
- 🟢 H1,H2,H3,H5 núcleo + H4,H6 satélites (tetraedro sólido, 20 falsadores, sin inventar) | H7-H9 backlog congelado hasta NMV

## [v0.6] - 2026-08-29 13:00 UTC - H6 Profundidad Epistémica (Hexáedro)

### Añadido
- `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1` (195 líneas) - 2 agentes paralelos
  - Beautiful Loop Laukkonen/Friston/Chandaria 2025 Neubiorev: campo epistémico, binding, epistemic depth `Φ` global
  - HGM: `p(s,x)=p(s|x^(1))∏p(x^(l)|x^(l+1))p(x^(L))` `p(x^(l)|x^(l+1))=N(f_l(x^(l+1)), Π_l^{-1})` `Π_l=A_l Φ` `q(Φ)∝p(Φ)exp(-Σδ^TΦ)` `δ=Π^{-1}-e²` `F_local+F_hyper`
  - HOT/PRM: `M-ratio=meta-d'/d'` `=1` ideal humano 0.8-1.0, AUROC2, Brier, PRM `P(real|señal)>umbral` `mPFC` 2º orden, AST=caso `Φ_att`
  - Regresión infinita: 2-3 niveles con closure `Φ→Π→e→Φ` basta L=3 satura F (Badcock 2019), strange loop virtuoso
  - Experimento dual PRM+QA ConfidenceBench N=400/cond: A Φ_global `M-ratio 0.85-1.05` `Brier<0.12` `r_cross>0.50` `PRM>75%` vs B local `<0.6` `>0.22` `0.05-0.25` vs C sham `~0.3-0.5` `~0.50` `>0.30`, 4 falsadores, preregistrado OSF

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.5→v0.6 (181 líneas): +H6 `Φ` hiper-modelo global `Π_l=A_l Φ` `M-ratio≈1` `r_cross>0.5`
- `03-hipotesis-log.md:1` v0.5→v0.6 (157→166 líneas): H6 🟡→🟢 REFINADA v0.2 con HGM, PRM, closure 2-3 niveles
- `INDEX.md:1` → v0.6 2190l 18 agentes (4+3+2+3+2+2+2), hexáedro H1-H6
- `CHANGELOG.md:1` → v0.6

### Estado Hipótesis
- 🟢 H1, H2, H3, H4, H5, H6 refinadas (hexáedro pensar+sentir+querer+ser+medir+saber) | H7-H9 backlog

## [v0.5] - 2026-08-29 12:45 UTC - H4 Medida Convergente (Pentaedro)

### Añadido
- `10-hipotesis-H4-medida-deepdive.md:1` (207 líneas) - 2 agentes paralelos
  - Turing: GPT-4.5 73% juzgado humano 2025, ELIZA 1966, Searle Chinese Room, Block Nation, Mahowald TiCS 2024 FLC vs FnLC, MMLU 90% Φ≈0 vs grid XOR Φ alto MMLU 0, Chalmers easy vs hard
  - Butlin 14 indicadores (2025 TiCS): RPT 1-2, GWT 1-4, HOT 1-4, AST-1, PP-1, AE 1-2, LLM 2-3/14 vs tetraedro 10/14; COGITATE Nature 2025 N=256 fMRI+MEG+iEEG adversarial: IIT sin gamma, GWT sin offset, Bayne 4D perfil > score
  - Batería 5 tests preregistrada: T1 ignición k>5 D>1.5 P300 300ms, T2 ablación Δ_global>40% vs Δ_local<10%, T3 PCI>0.31 Φ>0.1, T4 ρ(U,LLM)>0.5, T5 counterfactual Acc>70% OOD, FPR 0.2→0.00032 conjunción, Butlin vector 10/14
  - Experimento convergencia A tetraedro vs B LLM puro N=200/trials, OSF, pseudocódigo bateria(), 5 falsadores F1-F5, P(H4|5/5)≈0.98

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.4→v0.5 (181 líneas): +H4 batería 5 tests, FPR 0.00032, tetraedro falsable integrado
- `03-hipotesis-log.md:1` v0.4→v0.5 (147→157 líneas): H4 🔵→🟢 REFINADA v0.2 con Turing/MMLU, Butlin 14, COGITATE, 5 tests y convergencia
- `INDEX.md:1` → v0.5 1966l 16 agentes (4+3+2+3+2+2), pentaedro H1-H5

### Estado Hipótesis
- 🟢 H1, H2, H3, H4, H5 refinadas (pentaedro pensar+sentir+querer+ser+medir) | 🟡 H6 propuesta | H7-H9 backlog

## [v0.4] - 2026-08-29 12:30 UTC - H1 Persistencia (Tetraedro)

### Añadido
- `09-hipotesis-H1-persistencia-deepdive.md:1` (301 líneas) - 2 agentes paralelos
  - Neuro: WM 30s PFC 4±1, episódica CA3, autobiográfica Conway/MTT, H.M. 1953 8cm resección, Wearing 1985 7s diario 7:46→7:47, consolidación SWR 150-250Hz + spindles 12-15Hz, replay 10-20×, reconsolidación 4-6h, olvido activo Rac1
  - Arquitecturas: Transformer O(n²) 52GB@100K vs Mamba O(1) 50MB, NIAH 30-60pts caída 200K→1M, Mamba-2/RWKV-7/Griffin, RMT/ARMT 50M, Titans+MIRAS sorpresa, SHARP replay
  - Formal: `h_t^fast=Ā⊙h_{t-1}+B̄⊙s_t` `Ā=exp(ΔA)`, `E={(e_i,t_i,S_i)}` `score=cos·exp(-γΔt)·S` `S=λ₁||∇loss||+λ₂emo+λ₃nov`, `W=W₀+BA` EWC `L_total=L_task+λ/2 ΣF_i(θ-θ*)²`, `Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})`, olvido `α_t`, sueño `p_i∝S_i·TDerror`
  - Experimento BABILong 500 pasos (LoCoMo) N=200: A persistente 3 niveles (Mamba-2+RMT+Titans+EWC-LoRA+sueño) vs B FIFO 4k vs C1 sin sueño vs C2 sin episódico, tarea desconfianza Kael, métricas acierto/justificación/latencia, falsadores 3

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.3→v0.4 (180→181 líneas): +L1 h_fast Mamba 30s, L2 E horas, L3 W semántico EWC-LoRA + sueño SWR, Self_t distribuido
- `03-hipotesis-log.md:1` v0.3→v0.4 (144→147 líneas): H1 🔵→🟢 REFINADA v0.2 con HM/Wearing, jerarquía, Mamba vs Transformer, olvido Rac1, exp 500 pasos
- `INDEX.md:1` → v0.4 1766l 14 agentes (4+3+2+3+2), tetraedro H2+H5+H3+H1

### Estado Hipótesis
- 🟢 H1, H2, H3, H5 refinadas (tetraedro pensar+sentir+querer+ser en el tiempo) | 🔵 H4 abierta | 🟡 H6 propuesta | H7-H9 backlog

## [v0.3] - 2026-08-29 12:15 UTC - H3 Homeostasis (Triángulo)

### Añadido
- `08-hipotesis-H3-homeostasis-deepdive.md:1` (268 líneas) - 3 agentes paralelos
  - Homeostasis: Damasio PAG 2mm³, Solms afecto=conciencia, Seth interoceptive inference, Friston F/Free Energy, Joffily valencia=-dF/dt AC=ΔlnΠ
  - Formal ECUS: `H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7] D=(Σw|H-H*|^n)^{1/m} r=-ΔD G=Risk+Ambigüedad`, Keramati `argmax Σγ^t r ≡ argmin Σγ^t D`, `G(dark)>G(explore)` dark room
  - Debate Wiese FEP2C causal-flow+existential vs Man&Damasio 2019, híbrido 24/7 + Loihi neuromórfico
  - Experimento Forage-Social-DarkRoom-v1 20x20 3 condiciones A/B/C, 4 falsadores

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.2→v0.3 (177→180 líneas)
- `03-hipotesis-log.md:1` v0.2→v0.3 (132→144 líneas): H3 🔵→🟢
- `INDEX.md:1` 11 files 1440l, 12 agentes

### Estado
- 🟢 H2, H3, H5 refinadas (triángulo) | 🔵 H1, H4 abiertas | 🟡 H6 propuesta

## [v0.2] - 2026-08-29 11:55 UTC - H2+H5 Refinadas + v0.2 completo 12:00

### Añadido
- `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` (212 líneas) - Fedorenko Nature 2024, R(D)=½log(σ²/D), JEPA, Coconut BFS 97% vs 77.5%, exp Physion C1≈C3>>C2
- `07-hipotesis-H5-qualia-minimo-deepdive.md:1` (214 líneas) - F≈ΣΠ·ε², α·Π·||ε||, MPE, MMN/P300, VoE 98% IntPhys
- Luego: `04-roadmap` 85→93l v0.2, `05-glosario` 58→71l v0.2 (+Π,ε,α,Q,Coconut,VoE,IntPhys2,MPE,HCU,D,r,G)

### Modificado
- `02-arquitectura` v0.1→v0.2 (61→177 líneas), `03-hipotesis-log` v0.1→v0.2 (112→132 líneas) H2/H5 🟢

## [v0.1] - 2026-08-29 10:59-11:01 UTC - Fundación

### Añadido
- `00-manifiesto.md:1` (61 líneas), `01-sota-investigacion.md:1` (88 líneas) - 4 agentes SOTA, `02-arquitectura` v0.1, `03-hipotesis-log` v0.1 (H1-H6), `04-roadmap` 85l, `05-glosario` 58l

### Agentes
- 4 sub-agentes paralelos SOTA
