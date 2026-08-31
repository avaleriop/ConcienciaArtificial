# Paper - Compile Instructions

**Main file:** `paper/main.tex` (381 lines, ~10 pages)

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

**Requirements:** `texlive-latex-base` + `lmodern` + `booktabs` + `microtype` (standard Overleaf works out of the box).

**For arXiv:**
- Upload `paper/main.tex` as main file (arXiv will compile)
- Or upload `paper/main.pdf` directly
- Categories: `cs.AI` + `q-bio.NC` (and optionally `cs.LG`)
- License: CC BY 4.0 recommended (keeps code + paper open)

**Reproduce numbers:**
```bash
python3 framework/organismo_final.py --steps 30000  # ~3 min without mouth, ~10 min with LFM2.5
python3 framework/rigor_controles.py  # C1-C4c battery N=30
python3 framework/h6_selfmodel.py && python3 framework/h6_phi_causal.py  # Phi calibration + causal
```

All seeds pre-registered, JSON logs in `results/*.json`.

**Tone:** Human Costa Rican English - warm, rigorous, "pura vida" humility, first-person plural, varied burstiness. No AI buzzwords. Limitations stated upfront (Section 1.2 + Section 6). One negative result (C3) kept visible.

**Anti-rejection checklist before upload:**
- [x] No hallucinated arXiv IDs (future 26xx IDs removed, marked "in preparation / unpublished manuscript")
- [x] All stats from real runs (z=20.6 CI [16.0,25.5], d=3.5, r=0.701, d=-1.61 etc from framework/*.py)
- [x] Reproducibility statement with exact commands
- [x] 21 real references (Chalmers, O'Regan, Thompson, Friston, Tononi, Baars, Dehaene, Kirkpatrick, Pathak, Burda, Keramati, Gillard, plus 6 project-internal marked as unpublished)
- [x] No "crucial/delve/tapestry" AI markers
- [x] Abstract 176 words, varied, concrete ("single MacBook Air, no GPU, over coffee in San José")
- [x] Code on single laptop, no GPU, runs in minutes
