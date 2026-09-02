# Learning Without Remembering: Habituation in Weights and a Calibrated Self-Model in a Minimal Embodied Agent

**Author:** Adrián Valerio Porras — Independent Researcher, San José, Costa Rica — adrian_valerio@valeriogroup.co — ORCID 0009-0003-8445-2214

**Preprint. Intended submission to arXiv cs.AI and q-bio.NC.** 29 August 2026. Paper CC BY 4.0, code MIT.

## Files in this record

| File | Purpose |
| :--- | :--- |
| `Learning_Without_Remembering_v0.12.pdf` | Compiled paper (16 pages, article class) |
| `Learning_Without_Remembering_v0.12.tex` | LaTeX source (authoritative; compiles with pdflatex, tectonic, or Overleaf) |
| `CITATION.cff` | Citation metadata (CFF 1.2.0) |
| `LICENSE` | MIT (code); the paper text and PDF are CC BY 4.0 |
| `README.md` | This file |

## Summary of claims

1. **Detection (grid battery, N=30):** action-conditioned surprise to motor violations, z=20.6, 95% CI [16.0, 25.5]. Action-shuffled control 7.3x weaker, observation-only 8.5x weaker (single-seed pilots).
2. **Habituation as model update:** 86% surprise reduction (d=3.5) that lives in the weight delta — restoring pre-habituation weights restores surprise (z=67.5), freezing weights prevents habituation (z=137.2), post/pre ratio 0.02 with no episodic buffer in the prediction path.
3. **Negative result, kept (C3):** stimulus generalization — habituation to teleport (+5,+5) transfers to (-5,-5) (z 1.1 vs 0.9). The predictor learned displacement magnitude, not the vector: "learning without distinguishing." Rankin 2009 characteristic 7 (specificity) is not met; true dishabituation (char. 8) and spontaneous recovery (char. 10) are not tested here and are pre-registered as the next battery.
4. **Phi:** scalar MSE regressor to |epsilon| (15->64->1), calibrated r=0.701, generalizes r_cross=0.730, offline presence ratio 0.13 (7.7x separation). Isolated causal battery: 15.0% vs 28.1% fog time, d=-1.61. The equivalent effect in the integrated organism is reproduced by a random attention gate, a confound we flag; a 4-arm test is pre-registered.
5. **Integrated 30k run (continuous organism):** 13->64->6 predictor, +2 teleport, attention 13->7, Phi 22->64->1; 0% fog time with food outside fog; 6 violations; homeostasis maintained.
6. **EWC note:** lambda=5 + ortho lambda=0.01 is non-load-bearing for same-task interference (recovery 0.48 invariant across lambda); the habituation trace is likely low-rank. SVD and a factored predictor are pre-registered diagnostics.

## Reproduce

```bash
git clone https://github.com/adrianvalerio/conciencia-artificial
cd conciencia-artificial
git checkout v0.12-final
pip install -r requirements.txt
python3 framework/organismo_final.py --steps 30000     # integrated 30k run
python3 framework/rigor_controles.py                   # C1-C4c battery
python3 framework/estadistica_fase2.py                 # 30-seed statistics
python3 framework/h6_selfmodel.py                      # Phi calibration
python3 framework/h6_phi_causal.py                     # isolated causal battery
```

All numbers in Table 1 come from `framework/*.py` and JSON logs in `results/*.json`. Runs on a MacBook Pro (M4 Pro, Apple silicon) with MPS, no discrete GPU.

## Compile the paper

```bash
tectonic Learning_Without_Remembering_v0.12.tex        # single command
# or: pdflatex Learning_Without_Remembering_v0.12.tex (twice)
```

No external .bib (22 references inline). Requirements: standard article class + booktabs + lmodern + microtype (Overleaf works out of the box).

## Next battery (pre-registered)

Rankin-minimal battery (S1-S5 + true dishabituation + recovery gap), factored predictor (position/ECUS heads), per-channel log-variance Phi, 4-arm gate-vs-presence test, DeltaW SVD, N=30, one continuous world, food outside fog. Full protocol in the repository (doc. 63).

## License

Paper text and PDF: CC BY 4.0. Code: MIT. LFM2.5-1.2B model weights (not included here): LFM Open License v1.0.
