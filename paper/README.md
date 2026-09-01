# Paper v0.13 - Compile & Reproduce Instructions (peer-review revision, 1 Sep 2026)

**Main file:** `paper/main.tex` (~410 lines, article class for arXiv) — v0.13 supersedes v0.12

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

All stats in Table 1 come from `framework/*.py` and JSON logs in `results/*.json` (`estadistica_fase2.json`, `h5bis.json`, `h6_phi.json`, `benchmark_doorkey.json`, `cuarteto_habituacion.json` 0.48 lam-invariant).

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

- [x] Peer-review fixes: C3 renamed, Table 1 split, Phi offline + attention confound flagged, EWC non-load-bearing, MiniGrid removed from Table
- [x] No hallucinated arXiv IDs; 5 unpublished refs marked "Unpublished manuscript"
- [x] No year 2026 hallucination (Tononi 2016; Burda 2019; Man 2019)
- [x] All stats from real runs (z=20.6 CI[16.0,25.5], d=3.5, r=0.701, r_cross=0.730, d=-1.61 flagged, d=-0.43 random gate, recovery 0.48 lam-invariant)
- [x] Reproducibility statement + prereg `63-preregistro-v014-rankin-phi-factorizado.md` (Rankin battery + factored predictor + per-channel Phi + 4-arm + SVD)
- [x] 22 refs verified: previous 20 + Thompson & Spencer 1966 + Rankin et al. 2009 Neurobiol Learn Mem added
- [x] AI assistance disclosure added
- [x] Affiliation + ORCID, preprint line "Intended submission", date 1 Sep 2026 v0.13
- [x] H5-bis CI [0.84,0.85] (full [0.842,0.854] in results/h5bis.json)
- [x] Table footnote: N=30 vs pilots + confound note; MiniGrid only in Limitations (RND wins)
- [x] Abstract rewritten: learning without distinguishing, provenance split
- [x] M4 Pro MPS, no GPU, minutes; no crucial/delve, braces balanced, no EPS

**Tone:** Professional, first-person plural. Limitations up front (Sec 1.2 + Sec 6, 7 points). Negative result kept visible. Pre-registered next step.
