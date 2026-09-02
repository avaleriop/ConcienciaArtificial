# Conciencia Artificial — Habituation as Model Update in a Minimal Embodied Agent

Proyecto teórico-experimental sobre la **ruta sensorio-motora** (O'Regan & Noë 2001): un agente
mínimo y encarnado — predictor del cuerpo acción-condicionado, drive homeostático (E,C,U,S),
memoria episódica y un módulo auto-modelo (Φ) que predice su propio error de predicción — corre
sin visión ni audición, solo canales corporales. Un LLM local (LFM2.5-1.2B) actúa como **boca**
(traductor congelado de estados internos), nunca como cerebro: no controla la política.

> **Alcance v0.13:** el claim público es *habituación como update de modelo en pesos, sin
> memoria explícita y sin especificidad fina* (paper `56`). **No se afirma conciencia,
> awareness, ni los mecanismos GWT/PCI del marco teórico `00`–`13`** — ese marco es motivación
> e inspiración de diseño, no lo que el código mide. Los claims retirados están listados en el
> [CHANGELOG](CHANGELOG.md) (entrada 2026-09-02, "Claims retirados de la cara pública").

## Resultados (v0.13 — batería grid, N=30; NO transferibles al mundo continuo v0.14)

| Claim | Resultado | Estadístico |
| :--- | :--- | :--- |
| Detección de violaciones inyectadas (teleport ±5) | z=20.6 | CI [16.0, 25.5], N=30 |
| Condicionamiento a la acción (C1)† | 132.7 vs 18.1 | 7× |
| La acción aporta información (C2)† | 132.7 vs 15.5 | 8.5× |
| Habituación (decremento de z con exposición) | 3.8→0.5 | 86%, d=3.5 |
| Persistencia en pesos sin memoria E | post/pre 0.02 | N=30 |
| La traza vive en ΔW (C4a)† | z vuelve a 67.5 | restaurar W pre |
| Habituar requiere aprender (C4b)† | z sigue 137.2 | W congelado |
| Efecto requiere física aprendida (C4c)† | z=0.3 | predictor sin entrenar |
| **Generalización de estímulo (C3)†** | **1.1 vs 0.9** | **negativo: sin especificidad** |
| Homeostasis con política | E=0.85 | 100% seeds, CI [0.84, 0.85] |
| Φ calibrado (MSE escalar a \|ε\|) | r=0.701 | Spearman |
| Φ generaliza OOD (r_cross) | 0.730 | fuera de distribución |
| Φ funcional (offline) | ratio 0.13 | separación 7.7× |

† piloto de **una semilla** (seed 7) — no entra a inferencias sin N=30 (pre-registrado v0.14).

**Fuera de la tabla (retirado/confundido):** Φ causal d=−1.61 — aislado, sin modelar la gate
atencional; gate aleatoria reproduce d=−0.43 (`61`–`62`). Se testea con el 4-arm v0.14.

**Resultado negativo conservado (C3):** habituar a (+5,+5) también habitua (−5,−5). La
habituación es de *magnitud de desplazamiento*, no de vector — "learning without distinguishing"
(Rankin 2009 car. 7 no cumplida). Batería Rankin completa pre-registrada en `63`.

## Límites honestos

- Escala toy (MLP, grid 20×20 + continuo v0.12); dos sistemas que **no se mezclan** en la tabla
  del paper. Sin transferencia a biología.
- Sin deshabituación verdadera ni recuperación ISI testeadas (Rankin car. 8/10, v0.14).
- Φ es proxy escalar, no log-varianza por canal; presence es offline, no drive online.
- EWC λ=5 + ortho 0.01 **no modula** la interferencia misma-tarea (recovery 0.48 plana);
  la traza es probablemente de rango bajo.
- La boca traduce prompts construidos por el investigador; no es recuerdo libre.
- Benchmark MiniGrid N=5 **retirado** de la tabla (RND 2.8% > organismo 1.8%): no es resultado.
- El núcleo corre con `numpy` + `torch` (`requirements.txt`). `mlx`/`mlx-lm` (boca) y
  `gymnasium`/`minigrid` (benchmark piloto) están en `requirements-optional.txt`.

## Instalación y reproducción

```bash
pip install -r requirements.txt        # núcleo: numpy, torch
pip install -r requirements-optional.txt  # boca LLM (mlx) + benchmark (minigrid), opcionales
# boca LLM (opcional, 719MB Q4; el organismo corre idéntico sin ella, ver H2b doc 36):
python3 -c "from huggingface_hub import snapshot_download; snapshot_download('LiquidAI/LFM2.5-1.2B-Instruct-MLX-8bit', local_dir='models/LFM2.5-1.2B-MLX-8bit')"
```

Los paths del LLM se resuelven relativos al repo (`models/`, ignorado por git). Cada resultado
de la tabla se regenera con su script y semilla; los JSON están en `results/`:

| Script | Qué produce | Doc |
| :--- | :--- | :--- |
| `framework/estadistica_fase2.py` + `analisis_fase2.py` | Batería grid N=30 (z, habituación, persistencia, homeostasis, Φ) | `48`–`49` |
| `framework/rigor_controles.py` | C1–C4 (pilotos, seed 7) | `47` |
| `framework/organismo_final.py` | Run continuo v0.12 (30k pasos) | `55` |
| `framework/organismo_completo.py` | Capstone 20k pasos + boca | `44` |
| `framework/m5_24h_local.py` | Run largo 864k pasos | `38` |
| `framework/m4_local_h2b.py` | Conducta idéntica con/sin LLM | `36` |
| `framework/m4_local_m3b.py` | Plasticidad: W retiene aversión sin memoria E | `37` |

Scripts **retirados como evidencia** (históricos, no se citan en tablas ni abstracts):
`bateria_H4_toy.py` (T1–T3 implementan su resultado), `14`-Kael dict-vs-FIFO y BFS-32-0 como
test de H2. Ver CHANGELOG (entrada 2026-09-02).

## Estructura

- `00`–`64` docs numerados: `00`–`13` teoría (motivación), `14`–`55` experimentos y resultados
  (varios con claims ya retirados — leer con el CHANGELOG), `56` paper v0.13, `57` plan,
  `61`–`62` panel, `63` pre-registro v0.14, `64` plan de tres ejes
- `SPEC.md` especificación del sistema v0.14 (única fuente de números)
- `framework/core/` núcleo v0.14 (mundo, predictor factorizado, Φ por canal, z, EWC)
- `framework/` scripts ejecutables
- `results/` JSON con los números
- `paper/` LaTeX (main.tex v0.13, main_v13.pdf)
- `models/` LLM local (excluido de git)

## Estado

- Versión del repo: **v0.13** (paper v0.13) — preregistro y batería **v0.14** en curso según
  plan `64`.
- Tesis de diseño (no resultado): *LLM = boca, no cerebro* (Fedorenko 2024; conducta idéntica
  con/sin LLM es consistente, no decisiva: el LLM nunca controla la política por diseño).
- Lenguaje verificable: el agente "detecta violaciones de predicción, actualiza su predictor
  en pesos, reduce el error y retiene el cambio sin memoria explícita" — sin antropomorfismo.

## Paper y cita

- Borrador de taller (IWAI/ALIFE/CogSci LB): `56-paper-taller-borrador.md` y `paper/main.tex`.
- Citar como `CITATION.cff` (Zenodo DOI 10.5281/zenodo.22191728).
