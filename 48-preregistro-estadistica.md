# 48 - Pre-registro Estadístico (Fase 2) - N=30 Seeds, CI, Cohen's d

> **Fecha:** 29 Ago 2026 19:15 UTC — escrito ANTES de correr la estadística final
> **Propósito:** convertir "z=40σ en una corrida" en efectos medibles con incertidumbre.

## Hipótesis a medir (cada una con su refutación)

| # | Hipótesis | Métrica | Criterio de PASA | Refutación si... |
| :--- | :--- | :--- | :--- | :--- |
| **H1** | El predictor acción-condicionado detecta violaciones | z(motor) media ± 95% CI | z > 10 con CI que no cruza 5 | CI cruza 5 (efecto no robusto) |
| **H2** | El condicionamiento a la acción es real | d(Cohen) z(correcta) vs z(barajada) | d > 2.0 | d < 1.0 |
| **H3** | La habituación ocurre por aprendizaje en W | z(primera 5) vs z(últimas 5) | reducción > 70% con CI | reducción < 30% |
| **H4** | La traza persiste en W sin memoria E | z(post-borrado) < z(pre-habituación)/2 | SÍ con CI | z post ≥ pre/2 |
| **H5** | El organismo sobrevive con homeostasis estable | E media en rango [0.5, 1.2] sobre 30 seeds | ≥ 90% seeds en rango | < 70% seeds |
| **H6** | La boca traduce (no decide) | correlación de conducta con vs sin LLM | r > 0.9 | r < 0.7 |

## Protocolo (fijo, no se cambia)

1. 30 seeds (0-29), cada una corre el protocolo completo del `framework/m5_cadena_completa.py` reducido a 4 mediciones: z-base, z-motor, habituación (60 repeticiones), post-borrado-E.
2. Resultados en `results/estadistica_fase2.json` (una entrada por seed con todos los números).
3. Análisis: media, 95% CI (bootstrap 2000), Cohen's d entre pares de condiciones.
4. NO se modifica el protocolo tras ver resultados.

## Lo que queda fuera (honesto)

- C3a (especificidad por dirección) ya REFUTADA en Fase 1 — no se re-mide para "arreglar", se reporta.
- Comparación con baselines ICM/RND: es Fase 3 (benchmark), no Fase 2.

## Producto

`framework/estadistica_fase2.py` (ejecuta 30 seeds y escribe JSON) + `framework/analisis_fase2.py` (lee JSON, genera tabla CI/d) + `results/estadistica_fase2.json`.

*Pre-registrado. Correr con: python3 framework/estadistica_fase2.py && python3 framework/analisis_fase2.py*
