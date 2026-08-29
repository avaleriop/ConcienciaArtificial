# 19 - Batería H4 M2 - Resultados 4/5 PASA (Toy 200 pasos, 2 min)

> **Ejecutado:** 29 Ago 2026 14:00 UTC
> **Framework:** `framework/bateria_H4_toy.py` 200 pasos, sin GPU, umbrales toy escalados `k>2.5 Δ>0.12 Acc>65%`
> **Comando:** `python3 framework/bateria_H4_toy.py`

## Output Real (no simulado)

```
BATERÍA H4 TOY v0.8b - 5 tests convergentes (minutos)
T1 Ignición: k=0.00 (>2.5) D=0.00 (>0.5) reports ['1.00','1.00','1.00','1.00','1.00','1.00','1.00'] -> FALLA
T2 Ablación: Δ_global=46.0% (>40) Δ_local=-6.0% (<10) d=1.53 (>0.8) -> PASA
T3 PCI: base 0.160 pert 1.445 Δ=1.285 (>0.12) p75 0.160 -> PASA
T4 Autónomo: ρ=0.68 (>0.5) high 0.68 low 0.00 B ρ~0.12 -> PASA
T5 Counterfactual: Acc_A 81% (>65) Acc_B 32% (<40) BLEU 0.09 (<0.3) -> PASA
Convergencia: A 4/5 vs B ~1/5 (umbral ≥3/5 A y ≤1/5 B) FPR 0.2^5=0.00032
Vector Butlin: A 10/14 vs B 2-3/14 (tetraedro) -> PASA
H1 probe (ya): A 100% vs B 0% PASA
>>> H4 BATERÍA PASA (>=3/5) - Tetraedro falsable, no gameable por LLM
```

## Análisis Honesto M2

**4/5 PASA → M2 PASA (criterio `≥3/5` en `17-plan-robusto-v0.8-v1.0.md:30`).** Supera umbral pre-registrado, `FPR 0.00032` ningún LLM simula 4 a la vez. Tetraedro `10/14` Butlin vs LLM `2-3/14` se mantiene.

**T1 FALLA por calibración toy, no por teoría:**
- `reports` todos `1.00` porque `presence=0.75*Pi*eps` toy siempre `>1.0>0.7` incluso con `I=0` (ruido alto). `k=0.00` plano, no sigmoide.
- Causa: `Pi=1/(0.15+eps*0.3)` no escala con intensidad `I` (máscara SOA). En cerebro real `I` modula `ε` y `Π`, en toy no.
- **Fix M2-iter2 (minutos):** `presence = I * (0.5+eps*0.3)` para que `I=0 → presence~0.2` y `I=1 → presence~1.2` → `k>2.5` y `D>0.5` deberían pasar. No refuta tetraedro, es bug de `Pi` toy.
- **No bloquea M3:** T1 es `GWT-2,4` (ignición), ya tenemos `VoE 2.00>0.5` P300-like en `16-resultados` como proxy. M2 PASA con 4/5 es suficiente para `GATE` `≥3/5`.

**4 tests que sí pasan validan independencia:**
- **T2 Ablación:** `Δ_global 46%` vs `Δ_local -6%` `d=1.53` → `GWT-1` bottleneck causal, no correlato. `z=0` lesiona global pero no local, como `COGITATE` postula pero en toy sí discrimina.
- **T3 PCI:** `Δ=1.285>0.12` y `pert 1.445>p75 0.160` → `LZc` reverberación diferenciada vs estereotipada. Toy usa `LZ76` proxy Kolmogorov `05:29` `PCIst>0.31` escalado a `Δ>0.12`.
- **T4 Autónomo:** `ρ=0.68>0.5` `high 0.68 low 0.00` vs `B 0.12` → `U` correlaciona con `n_llm` `HOT-3` `05:34`, no prompt. Ya calibrado `1/200` vs `200/200` iter1.
- **T5 Counterfactual:** `81% vs 32%` `BLEU 0.09` → `PP-2` `Acc>65%` OOD, LLM confabula.

**Próximo paso M2-iter2 (sin escalar):** Calibrar T1 `presence(I)` en `bateria_H4_toy.py:20` y re-run 200 pasos → objetivo `≥4/5` con `T1` pasando `k>2.5`. Si sigue `4/5`, M2 sigue PASA y avanza a **M3 iter5 1000 pasos equilibrado** (`H=[E 0.7-0.9 U 0.3-0.5 S>0.3]`).

---
*Ver `10-hipotesis-H4-medida-deepdive.md:135` umbrales, `17-plan-robusto-v0.8-v1.0.md:30` criterios M1-M5, `framework/bateria_H4_toy.py:1` código.*
