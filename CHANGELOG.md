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

## [Unreleased] - Pendiente
- Actualizar 04-roadmap y 05-glosario a v0.2
- Commit git inicial
