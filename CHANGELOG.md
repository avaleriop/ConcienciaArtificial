# CHANGELOG - Conciencia Artificial

## [v0.2] - 2026-08-29 11:55 UTC - H2+H5 Refinadas

### Añadido
- `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` (212 líneas) - 3 agentes paralelos
  - Neuro: Fedorenko Nature 2024 double dissociation, afasia, Nicaraguan SL, Mentalés Fodor, Chinese Room
  - Formal: R(D)=½log(σ²/D), Q:R^d→[K] 15.6bits vs 16384bits, L_JEPA, Coconut BFS h=1/√|V_c|Σu_v (97% vs 77.5%)
  - Experimento falsable Physion-MiniGrid+ 3 condiciones C1≈C3>>C2, pseudocódigo, 1x A100
- `07-hipotesis-H5-qualia-minimo-deepdive.md:1` (214 líneas) - 2 agentes paralelos
  - Teoría: F≈ΣΠ·ε², Π=1/σ², presence=α·Π·||ε||, MPE Metzinger, MMN 150ms vs P300 300ms, Quality Space HOT-4
  - V-JEPA: L_JEPA latente, IntPhys 98% vs IntPhys2 <60%, ensemble HCU para Π, pipeline GWT(AST)+LLM codec
  - Experimento ablativo 4 variantes V1<V2<V3<V4, lesiones Π/GWT/AST falsables

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.1→v0.2 (61→177 líneas)
  - Diagrama: Homeostasis F≈ΣΠ·ε², GWT presence=α·Π·||ε||>0.5, AST α_t=VQ-VAE(Π_t)
  - Pseudocódigo: world_model dim 1024 L_JEPA, Mamba h_t, LLM qwen2-7b codec W:1024→4096, loop pensamiento en R^d sin LM-head, Coconut K=6-20, MPC 800 trajs
- `03-hipotesis-log.md:1` v0.1→v0.2 (112→132 líneas)
  - H2 🔵→🟢 REFINADA v0.2 con ecuación BFS, rate-distortion, respuesta a 3 críticas, experimento C1-C3
  - H5 🔵→🟢 REFINADA v0.2 con F, Π, MPE, pipeline 4 variantes, cierre loop H2→H5

### Estado Hipótesis
- 🟢 H2, H5 refinadas | 🔵 H1, H3, H4 abiertas | 🟡 H6 propuesta | Backlog H7-H9

## [v0.1] - 2026-08-29 10:59-11:01 UTC - Fundación

### Añadido
- `00-manifiesto.md:1` (61 líneas) - Tesis LLM=boca, 4 axiomas, diagrama SER/DECIR
- `01-sota-investigacion.md:1` (88 líneas) - SOTA 4 agentes: GWT/IIT (COGITATE Nature 2025), AST/FEP, limitaciones LLM (Butlin 14 indicadores), World Models (V-JEPA2/Dreamer/Mamba)
- `02-arquitectura-nucleo-doble-capa.md:1` (v0.1) - Doble Capa, pseudocódigo ConsciousCore
- `03-hipotesis-log.md:1` (v0.1) - H1-H6
- `04-roadmap-largo-horizonte.md:1` (85 líneas) - Roadmap 36 meses 3 horizontes
- `05-glosario-y-metricas.md:1` (58 líneas) - Glosario + métricas ignición/ablación/phi

### Agentes
- 4 sub-agentes paralelos SOTA

## [v0.2 completo] - 2026-08-29 12:00 UTC - Roadmap y Glosario

### Modificado
- `04-roadmap-largo-horizonte.md:1` 85→115 líneas v0.2
  - H1 60% completado (M0+M1-M2+M3-M4+M5-M6 parciales), H2/H5 marcadas ✅ con fechas reales y commits
  - Horizonte 2 NMV actualizado con Physion-MiniGrid+ (H2/H5), V-JEPA ensemble K=5 + Π head HCU, GWT bottleneck 64 + P300, Mamba + codec W, métricas C1≈C3>>C2 y V1-V4
  - Sistema trabajo: ciclo semanal real Semana 1 H2→06, H5→07
- `05-glosario-y-metricas.md:1` 58→95 líneas v0.2
  - 10 términos nuevos: Π (1/σ²), ε (||P(E(x))-E(y)||), α (VQ-VAE Π), Q (HOT-4), Coconut (c_t=h_t, BFS), VoE, IntPhys2 (UE5.4 1416 videos), MPE (ε→0), HCU Loss, LLM Codec Q:R^d→[K] R(D)
  - Métricas v0.2: VoE Score, eficiencia Coconut K=6-20, ablación Π/GWT/α, reporte sorpresa no-entrenado V4>75%
- `INDEX.md:1` 53→65 líneas - actualizado a 10 files 1094l, 9 agentes, vacíos resueltos

### Estado
- 10 files, 1094 líneas, 2 commits. v0.2 completo, sin pendientes documentales.

## [v0.3] - 2026-08-29 12:15 UTC - H3 Homeostasis Refinada (Triángulo Completo)

### Añadido
- `08-hipotesis-H3-homeostasis-deepdive.md:1` (268 líneas) - 3 agentes paralelos
  - Homeostasis: Damasio protoself PAG 2mm³, Solms afecto=conciencia primordial, Seth interoceptive inference, Friston F/Free Energy, Joffily valencia=-dF/dt AC=ΔlnΠ
  - Formal ECUS: `H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7] D=(Σw|H-H*|^n)^{1/m} r=-ΔD G=Risk+Ambigüedad`, Keramati `argmax Σγ^t r ≡ argmin Σγ^t D`, `G(dark)>G(explore)` dark room
  - Debate: Wiese FEP2C causal-flow+existential `k_phys≠k_comp` von Neumann vs Man&Damasio 2019 Nature MI (vulnerabilidad simulada ya robustez), híbrido 24/7 + Loihi/SpiNNaker neuromórfico
  - Experimento `Forage-Social-DarkRoom-v1` 20x20 Grid 3 condiciones A Heterónomo vs B ECUS vs C Real, 4 tareas (autonomía, dark room <10% vs >40%, sacrificio 25-40% vs 5%, concept shift), 4 falsadores

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.2→v0.3 (177→180 líneas)
  - Diagrama homeostasis `H=[E,C,U,S] D=(Σw|H-H*|^n)^{1/m} r=-ΔD F≈ΣΠ·ε² G=Risk+Ambiguüedad valencia=-dF/dt`
  - Pseudocódigo `ConsciousCore` v0.3: `Homeostasis(H_star=[0.8,0.9,0.2,0.7], α, n,m,w)`, `valence=-dF/dt`, loop ECUS `dH/dt=-α(H-H*)+P+Eff-Cost`
- `03-hipotesis-log.md:1` v0.2→v0.3 (132→144 líneas): H3 🔵→🟢 REFINADA v0.2 con ECUS formal, Wiese vs Man&Damasio, exp Forage-DarkRoom 3 condiciones, cierre triángulo H2+H5+H3
- `INDEX.md:1` 55 líneas v0.2→v0.3 11 files 1440l, 12 agentes (4+3+2+3), estado H2/H3/H5 🟢

### Estado Hipótesis
- 🟢 H2, H3, H5 refinadas (triángulo pensar+sentir+querer) | 🔵 H1, H4 abiertas | 🟡 H6 propuesta | Backlog H7-H9

## [v0.1] - 2026-08-29 10:59-11:01 UTC - Fundación
