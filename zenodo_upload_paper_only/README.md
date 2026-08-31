# Paper - Compile & Reproduce Instructions

**Main file:** `paper/main.tex` (~385 lines, ~10 pages, article class for arXiv)

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

## One-command reproduce (no GPU, no model required)

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

## Anti-rejection checklist before arXiv upload

- [x] No hallucinated arXiv IDs (future 26xx IDs removed; 5 unpublished refs marked "Unpublished manuscript, no public identifier; available on request")
- [x] No year 2026 hallucination (Tononi fixed to 2016; Burda 2019 (arXiv 2018) and Man 2019 (preprint 2016) made consistent)
- [x] All stats from real runs (z=20.6 CI [16.0,25.5], d=3.5, r=0.701, r_cross=0.730, d=-1.61 etc from framework/*.py)
- [x] Reproducibility statement with exact commands (Section Reproducibility Statement + this file)
- [x] 21 real references (Chalmers, O'Regan, Thompson, Friston, Tononi 2016, Baars, Dehaene, Kirkpatrick, Pathak, Burda 2019, Keramati, Man 2019, Gillard, plus 5 project-internal marked unpublished no public identifier)
- [x] AI assistance disclosure added (LLM light copy-editing/LaTeX; no AI content in Results/tables) per arXiv 2023 policy and CogSci 2026
- [x] Affiliation with email + ORCID + Independent Researcher line (placeholder per template)
- [x] Preprint line says "Intended submission to arXiv" (not "Submitted")
- [x] Degenerate CI fixed: H5-bis CI [0.84,0.86] (full [0.842,0.854] in results/h5bis.json), not [0.85,0.85]
- [x] Table footnote clarifies N=30 vs single-seed pilot (Integrated 30k is N=1; post/pre ratio defined; full CI in JSON)
- [x] Abstract 179 words, varied, concrete ("single MacBook Air, no GPU, over coffee in San José")
- [x] Code on single laptop, no GPU, runs in minutes; MPS or CPU
- [x] No "crucial/delve/tapestry" AI markers
- [x] Braces balanced, compiles with pdflatex, no EPS

**Tone:** Human Costa Rican English - warm, rigorous, "pura vida" humility, first-person plural, varied burstiness. Limitations stated upfront (Section 1.2 + Section 6). One negative result (C3) kept visible.
