# 56 - Paper de Taller (Borrador) - IWAI / ALIFE / CogSci Late-Breaking — v0.13 (revisado 2026-09-01, supersede v0.12)

> **Estado:** v0.13 peer-review revision — lista para Zenodo v0.13 y arXiv. Título sin cambios pero claim corregido a "learning without distinguishing".
> **Título propuesto:** Habituation as Model Update in a Minimal Embodied Agent: Controls, Stimulus Generalization Limits, and Weight Persistence Without Explicit Memory

## Abstract (v0.13)

We present a minimal embodied agent — a continuous loop of an action-conditioned body predictor, a homeostatic drive (E,C,U,S), episodic memory, and a meta-cognitive module (Φ) that predicts its own prediction error — running without vision or audition, on body channels only. Grid-world battery (N=30, 13→128→128→6, ±5 teleport): (1) detection z=20.6 CI[16.0,25.5]; (2) habituation 86% d=3.5 lives in weight delta (restore pre-W → z=67.5, freeze → 137.2, post/pre 0.02); (3) action-shuffled 7× and obs-only 8.5× weaker (C1/C2 single-seed pilots). Negative result renamed (C3): stimulus generalization — habituating to (+5,+5) also habituates (−5,−5) (1.1 vs 0.9) → habituation of displacement magnitude, not vector, i.e. learning without distinguishing (Rankin 2009 char. 7 not met; true dishabituation char. 8 and recovery not tested — pre-registered v0.14). (4) Φ scalar MSE to |ε| (15→64→1) is calibrated r=0.701 and generalizes r_cross=0.730; offline presence ratio 0.13 (7.7×). Isolated causal battery: Φ-coupled vs uncoupled 15.0% vs 28.1% fog time d=-1.61 — flagged as confounded with attention gate (att_vis<0.35; random gate reproduces d=-0.43 in continuous v0.12). Continuous v0.12 run (13→64→6, +2, attention 13→7, Φ 22→64→1) closes the loop over 30k steps (0% fog, food outside fog). EWC λ=5 + ortho 0.01 is non-load-bearing for same-task interference (recovery 0.48 invariant); trace likely low-rank. Framed as habituation-as-model-update (Levin lab), not phenomenal consciousness. Pre-registered Rankin battery + factored predictor + per-channel Φ + 4-arm test + ΔW SVD as v0.14.

## 1. Introduction

The claim we test: a minimal agent built from an action-conditioned forward model, homeostatic drives, and a self-model of its own precision can (a) detect violations of its sensorimotor contingencies, (b) habituate to them by updating its model, (c) retain that update in weights without explicit memory, and (d) act on its own meta-cognitive state. This is the sensorimotor-contingency route to awareness (O'Regan & Noë 2001): no vision required, body channels only — as a blind person is conscious through body, not sight.

## 2. Methods

### 2.1 Agent architecture
- **Body predictor** (MLP, 13→64→6): P(s_{t+1} | s_t, a_t) over position (x,y) and interoception (E,C,U,S).
- **Homeostatic drive (ECUS):** H*=[0.8,0.9,0.2,0.7]; D=(Σw|H−H*|²)^{1/2}; action policy from drive.
- **Surprise:** z-score of prediction error ε against a running baseline.
- **Meta-cognitive module Φ** (MLP 15→64→1): predicts σ (expected magnitude of its own prediction error), trained against actual ε. Surprise is precision-weighted: presence = ε/σ².
- **Episodic memory E** (salience-gated, cap 5000) + **EWC** on predictor weights (λ=5).
- **Mouth:** LFM2.5-1.2B (Liquid AI, hybrid SSM-conv, MLX-native) translates internal state to language; never controls action. Behavior is identical with or without it.

### 2.2 World
20×20 grid; foods, a social agent, and a "fog zone" (x>14) where interoception noise σ=0.6 makes sensing unreliable — the observable cue Φ must learn.

### 2.3 Violations
Motor (body teleports 5 cells), interoceptive (eating lowers energy — inverted causality), tactile (wall pass-through).

### 2.4 Controls and statistics (pre-registered before running)
C1 action-shuffled, C2 observation-only, **C3 stimulus generalization (renamed; misnamed dishabituation in v0.12)**, C4a weight-restore, C4b weight-freeze, C4c untrained. Grid battery N=30 for detection/habituation/persistence/H5-bis/Φ; C1-C4c single-seed pilots (seed 7). 95% CI (bootstrap 2000), Cohen's d. Rankin char. 7/8/10 and 4-arm Φ vs attention pre-registered as v0.14.

## 3. Results (v0.13 — grid battery vs continuous v0.12 split)

| Claim | Result | Statistic | System |
| :--- | :--- | :--- | :--- |
| Detection | z=20.6 | CI [16.0, 25.5], N=30 | grid |
| Action-conditioning (C1)† | 132.7 vs 18.1 | 7× | grid pil. |
| Action adds info (C2)† | 132.7 vs 15.5 | 8.5× | grid pil. |
| Habituation (H3) | 3.8→0.5 | 86%, d=3.5 | grid |
| Weight persistence (H4) | post/pre 0.02 | N=30 | grid |
| Habituation in W (C4a)† | z returns to 67.5 | restore pre-W | grid pil. |
| Requires learning (C4b)† | z stays 137.2 | frozen | grid pil. |
| Requires physics (C4c)† | z=0.3 | untrained | grid pil. |
| **C3 Generalization†** | **1.1 vs 0.9** | **fail (no specificity)** | **grid pil.** |
| Homeostasis with policy (H5-bis) | E=0.85 | 100% seeds, CI[0.84,0.85] | grid |
| Φ calibration (scalar MSE) | r=0.701 | Spearman | grid |
| Φ generalization (r_cross) | 0.730 | out-of-distribution | grid |
| Φ functional (offline) | ratio 0.13 | 7.7× separation | grid |
| Φ causal isolated‡ | 15.0% vs 28.1% fog | d=-1.61 | grid iso. |
| Integrated 30k-step run | fog time 0.0%; mouth reports Φ state | 6 viol. | **continuous v0.12** |

† single-seed pilot, ‡ attention not modelled — in continuous organism random gate reproduces d=-0.43, so gate is confound.

**Negative result (kept, renamed):** C3 stimulus generalization — habituating to (+5,+5) also habituates (−5,−5) (1.1 vs 0.9). Habituation is of displacement magnitude, not vector — "learning without distinguishing". Rankin specificity (7), true dishabituation (8) and recovery not tested.

## 4. Discussion

The agent's habituation is model update (Levin "Training Ecosystems" 2026): the trace lives in weight deltas (ΔW), requires learning, and persists without explicit memory — but only as a coarse, likely low-rank "ignore large L2" direction, not a vector concept. Factored predictor + ΔW SVD predicted. The Φ module (scalar MSE to |ε|, 15→64→1) is calibrated and generalizes, and is efficacious in the isolated battery (d=-1.61, offline presence 7.7×), but its effect is confounded with the attention gate att_vis<0.35 in the continuous organism (random gate → same d=-0.43). Per discriminating rule (what could a conventional predictor not do?): a conventional forward model has ε; it does not predict its own ε. Our Φ does (calibrated), but whether its precision (per-channel log-variance) drives action online requires the 4-arm test (v0.14). We keep that distinction explicit.

We do NOT claim phenomenal consciousness. We claim the architectural machinery — sensorimotor-contingency detection, habituation-as-model-update at coarse granularity, meta-cognitive calibration (with offline presence), and a confounded-but-isolated causal efficacy — is demonstrated at zero cost (single laptop, no GPU) and bounded by a precise negative result.

## 5. Limitations (v0.13 — 7 points)

- Toy scale (MLP, grid + continuous 20×20); no transfer to biology; Table splits two systems.
- No stimulus specificity: C3 generalization 1.1 vs 0.9; no dishabituation (Rankin 8) nor ISI recovery; H_A = magnitude not contingency, Rankin battery pre-registered.
- Φ is scalar MSE proxy, not per-channel log-variance; presence offline, not online drive; attention gate confound (requires 4-arm A/B/C/D).
- EWC λ=5 + ortho 0.01 non-load-bearing for same-task; trace likely low-rank (ΔW SVD + factored predictor pending).
- LLM mouth is translator of constructed prompts, not free recall.
- Benchmark MiniGrid N=5 (RND 2.8% beats 1.8%) — pilot removed from Table, under-powered.
- Other gaps: no vision/audition by design, intero/tactile only single-seed, no Rankin S1-S5/isodirectional controls yet.

## 6. References (key)

O'Regan & Noë (2001) BBS. Levin "Training Ecosystems" (arXiv 2605.30109). CheckVLA (arXiv 2607.26789). Asleep at the Wheel (arXiv 2608.01336). Gubernaut GCC (arXiv 2607.24339). Christov-Moore et al. (arXiv 2510.07117). Laukkonen, Friston & Chandaria (2025). LFM2 Technical Report (arXiv 2511.23404).

---
*Todos los números provienen de los scripts del repo (`framework/`), reproducibles con `README.md`. Datos crudos en `results/*.json`.*
