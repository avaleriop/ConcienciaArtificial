# 56 - Paper de Taller (Borrador) - IWAI / ALIFE / CogSci Late-Breaking

> **Estado:** borrador listo para envío cuando el usuario decida
> **Título propuesto:** Habituation as Model Update in a Minimal Embodied Agent: Controls, Dishabituation Limits, and Weight Persistence Without Explicit Memory

## Abstract

We present a minimal embodied agent — a continuous loop of an action-conditioned body predictor, a homeostatic drive (E,C,U,S), episodic memory, and a meta-cognitive module (Φ) that predicts its own prediction error — running without vision or audition, on body channels only. In 30-seed pre-registered experiments: (1) the agent detects violations of its sensorimotor contingencies (z=20.6, 95% CI [16.0, 25.5]); (2) it habituates to repeated violations by learning (86% reduction, Cohen's d=3.5), and this habituation lives in the weight delta — restoring pre-habituation weights restores surprise (z=67.5), freezing weights prevents habituation, and the learned trace persists after erasing explicit episodic memory (post/pre ratio 0.02); (3) an action-shuffled control (7× weaker) and observation-only control (8.5× weaker) establish that detection is genuinely action-conditioned; (4) the meta-cognitive module Φ is calibrated (Spearman r=0.701 between predicted and actual error), generalizes out-of-distribution (r_cross=0.730), and is causally efficacious: an agent that knows its senses are unreliable leaves the unreliable zone (15.0% vs 28.1% time, d=-1.61). We discuss one negative result — habituation generalizes across teleport direction, so fine-grained stimulus specificity is not demonstrated — and frame the system within habituation-as-model-update (Levin lab) rather than as a claim about phenomenal consciousness.

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
C1 action-shuffled, C2 observation-only, C3 dishabituation, C4a weight-restore, C4b weight-freeze, C4c untrained. N=30 seeds, 95% CI (bootstrap 2000), Cohen's d.

## 3. Results

| Claim | Result | Statistic |
| :--- | :--- | :--- |
| Detection | z=20.6 | CI [16.0, 25.5], N=30 |
| Action-conditioning (C1) | 132.7 vs 18.1 | 7× |
| Action adds info (C2) | 132.7 vs 15.5 | 8.5× |
| Habituation (H3) | 3.8→0.5 | 86%, d=3.5 |
| Weight persistence (H4) | post/pre 0.02 | N=30 |
| Habituation in W (C4a) | z returns to 67.5 | restore pre-W |
| Requires learning (C4b) | z stays 137.2 | frozen |
| Requires physics (C4c) | z=0.3 | untrained |
| Homeostasis with policy (H5-bis) | E=0.85 | 100% seeds in range |
| Φ calibration | r=0.701 | Spearman |
| Φ generalization (r_cross) | 0.730 | out-of-distribution |
| Φ functional (noise vs surprise) | ratio 0.13 | 7.7× separation |
| Φ causal efficacy | 15.0% vs 28.1% fog time | d=-1.61 |
| Integrated 30k-step run | fog time 1.9%; mouth reports Φ state | qualitative |

**Negative result (reported):** C3 dishabituation — habituating to teleport(+5,+5) also habituates teleport(−5,−5) (z 1.1 vs 0.9). Habituation generalizes at the level of "large displacement", not the specific vector. Fine-grained stimulus specificity is NOT demonstrated.

## 4. Discussion

The agent's habituation is model update (Levin "Training Ecosystems" 2026): the trace lives in weight deltas, requires learning, and persists without explicit memory — but only at the granularity of violation type, not instance. The Φ module turns raw prediction error into "expected unreliability" — a calibrated, generalizing, behaviorally efficacious self-model (d=−1.61). Per the discriminating rule (what could a conventional predictor not do?): a conventional forward model has ε; it does not predict its own ε, and its uncertainty does not change action. Our agent does both.

We do NOT claim phenomenal consciousness. We claim the architectural machinery — sensorimotor-contingency detection, habituation-as-model-update, meta-cognitive calibration, and causal efficacy of the self-model — is demonstrated in a minimal embodied system at zero cost (single laptop, no GPU).

## 5. Limitations

- Toy scale (MLP, grid world); no claim transfers to biological scale.
- Fine-grained stimulus specificity not shown (C3).
- LLM mouth is a translator of constructed prompts; the "reportability" is a translation of internal state, not free recall.
- Benchmark vs ICM/RND on MiniGrid Empty-8x8 is preliminary (N=5, vanilla REINFORCE): organism 1.8% > ICM 0.6% > random 0.4%, highest coverage — under-powered.

## 6. References (key)

O'Regan & Noë (2001) BBS. Levin "Training Ecosystems" (arXiv 2605.30109). CheckVLA (arXiv 2607.26789). Asleep at the Wheel (arXiv 2608.01336). Gubernaut GCC (arXiv 2607.24339). Christov-Moore et al. (arXiv 2510.07117). Laukkonen, Friston & Chandaria (2025). LFM2 Technical Report (arXiv 2511.23404).

---
*Todos los números provienen de los scripts del repo (`framework/`), reproducibles con `README.md`. Datos crudos en `results/*.json`.*
