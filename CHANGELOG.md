# CHANGELOG - Conciencia Artificial

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
