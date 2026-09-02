# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 2 Sep 2026
> **Versión:** v0.13 (paper v0.13) — preregistro v0.14 en `63`, plan de tres ejes en `64`
> **Una línea:** habituación como update de modelo en pesos, sin memoria explícita y sin
> especificidad fina, en un agente mínimo encarnado. Marco teórico `00`–`13` = motivación,
> no claim. v0.14 cambia de mundo: **continuo con niebla** (prereg `63`); los números de
> grid (z=20.6) son v0.13, **no transferibles** a v0.14.

## Estado de claims (board del plan `64`)

| Claim | Estado | Evidencia | Nota |
| :--- | :--- | :--- | :--- |
| **Detección** (violación inyectada eleva ε) | ✅ vivo (N=30) | `49`, z=20.6 CI[16.0,25.5] | **grid v0.13**; v0.14 = continuo, sin comparar |
| **C1 condicionamiento a la acción** (acción real > barajada) | ⚠️ piloto 1 semilla | `47`: 7× | C1 ≠ detección: son dos claims |
| Habituación grosera en pesos | ✅ vivo (N=30) | `49`, 86%, d=3.5; C4a/b/c piloto `47` | grid v0.13 |
| Persistencia en W sin memoria E | ✅ vivo (N=30) | `49`, post/pre 0.02 | grid v0.13 |
| Homeostasis con política | ✅ vivo | `50`, E=0.85, 100% seeds | grid v0.13 |
| Φ calibrado / generaliza (offline) | ✅ vivo | `52`, r=0.701, r_cross=0.730 | escalar; por canal en v0.14 |
| Especificidad fina del estímulo | ❌ muerto (C3) | `47`: 1.1 vs 0.9 — generaliza a −5,−5 | renombrado *stimulus generalization* |
| Φ causal (d=−1.61) | ⚠️ confundido | `53`,`61`,`62`: gate atencional; 4-arm v0.14 | **fuera de la tabla del README** |
| EWC como mecanismo de persistencia | ⚠️ herido | `62`: λ inerte misma-tarea; tarea-distinta v0.14 | |
| LLM=boca (demostrado) | 🚫 tautológico por diseño | `36` es consistente, no decisivo; fuera de v0.14 | |
| Batería H4 5/5 (T1–T3) | 🚫 retirado | scripts implementan el resultado; ver CHANGELOG | |
| Kael 100% vs 0% como H1 | 🚫 retirado | dict vs FIFO; doc `14` histórico | |
| BFS 32-0 como H2 | 🚫 retirado | category error; ver CHANGELOG | |
| FPR 0.00032 / Butlin 10/14 | 🚫 retirado | sin medida; solo motivación teórica | |
| Benchmark Empty-8x8 (1.8%) | 🚫 retirado | N=5, RND 2.8% gana; fuera del paper | |
| 24 h / 864k pasos como H1 | 🚫 retirado | run largo = humo, no test de persistencia | |

**Awareness/conciencia fenoménica: NO afirmadas.** (docs `18`,`39`,`54` anteriores lo decían;
ver CHANGELOG v0.14 "Claims retirados").

## Documentos

### Teoría (motivación, no claim experimental) — `00`–`13`

| # | Archivo | Contenido | Estado |
|---|---------|-----------|--------|
| 00 | `00-manifiesto.md` | Manifiesto, tesis LLM=boca, falsabilidad | motivación |
| 01 | `01-sota-investigacion.md` | SOTA GWT/IIT/AST/FEP, Butlin 14 | motivación |
| 02 | `02-arquitectura-nucleo-doble-capa.md` | Arquitectura canónica `F_total` | motivación |
| 03 | `03-hipotesis-log.md` | Log H1–H6 | histórico |
| 04 | `04-roadmap-largo-horizonte.md` | Roadmap largo plazo | histórico |
| 05 | `05-glosario-y-metricas.md` | Glosario, Π, z-score VoE | histórico |
| 06–11 | Deep dives H2/H5/H3/H1/H4/H6 | Teoría con papers 2024-25 | motivación |
| 12 | `12-auditoria-critica-v0.6.md` | Poda hexáedro→tetraedro | histórico |
| 13 | `13-sintesis-tetraedro-v0.7.md` | Tetraedro, lenguaje verificable | histórico |

### Resultados (evidencia que alimenta el paper v0.13)

| # | Archivo | Contenido | Estado |
|---|---------|-----------|--------|
| 14 | `14-experimento-toy-solidez-2026-08-29.md` | Kael 100 vs 0, BFS 32-0 | 🚫 retirado como evidencia |
| 15–16 | Framework proceso vivo | Calibración temprana | histórico |
| 17 | `17-plan-robusto-v0.8-v1.0.md` | Plan M1–M5 | histórico |
| 18 | `18-resumen-ejecutivo-v0.8.md` | Ejecutivo v0.8 ("el organismo vive") | 🚫 lenguaje retirado |
| 19 | `19-bateria-H4-M2-resultados.md` | Batería H4 5/5 k14.22 | 🚫 retirado |
| 20–24 | Plan ingeniería, GATE, plasticidad | Toy/M2–M3 | histórico |
| 25–35 | M4 local, escalado 4M, retina | Encoder aprendido, JEPA local | histórico (no en paper) |
| 36 | `36-H2b-decisivo-LFM25-local.md` | Conducta idéntica con/sin LLM | ⚠️ consistente, no decisivo |
| 37 | `37-M3b-real-plasticidad-LFM25.md` | W retiene aversión sin E | ⚠️ 1 semilla |
| 38 | `38-M5-24h-local.md` | 864k pasos | histórico (no es test H1) |
| 39 | `39-resumen-ejecutivo-final-v0.10.md` | "El Organismo Vive" | 🚫 lenguaje retirado |
| 40 | `40-VoE-v2-emergente-limite-local.md` | Negativo honesto (sin visión) | histórico |
| 41–43 | Sorpresa sin visión, integración causal | Cadena v0.11 | histórico |
| 44 | `44-organismo-completo-capstone.md` | Capstone 20k pasos + boca | histórico |
| 45 | `45-revision-estrategica-sota.md` | Revisión SOTA | histórico |
| 46–47 | Plan rigor + controles C1–C4 | Pilotos seed 7 | ⚠️ v0.13 los degrada a pilotos |
| 48–49 | Pre-registro + batería N=30 | z, habituación, persistencia | ✅ núcleo del paper |
| 50 | `50-h5bis-homeostasis-blindada.md` | Homeostasis 100% seeds | ✅ |
| 51 | `51-benchmark-publico-resultados.md` | Empty-8x8 | 🚫 retirado (N=5) |
| 52 | `52-h6-selfmodel-resultados.md` | Φ calibrado r=0.701 | ✅ offline |
| 53 | `53-h6-phi-causal-resultados.md` | Φ d=−1.61 aislado | ⚠️ confundido con gate |
| 54 | `54-resumen-ejecutivo-cierre-v0.12.md` | "awareness FUERTE" | 🚫 lenguaje retirado |
| 55 | `55-organismo-final-integrado.md` | Run continuo v0.12 30k | ⚠️ segundo sistema |

### Estado actual y plan

| # | Archivo | Contenido |
|---|---------|-----------|
| 56 | `56-paper-taller-borrador.md` | **Paper v0.13** (claim acotado, tablas separadas) |
| 57 | `57-plan-v13-estrategico.md` | Plan v0.13 |
| 58–60 | Preregistros v0.13 (H*, eco) | Históricos |
| 61 | `61-panel-estrategico.md` | Red-team interno (no peer review externo) |
| 62 | `62-correcciones-panel-resultados.md` | Correcciones: EWC inerte, Φ confundido |
| 63 | `63-preregistro-v014-rankin-phi-factorizado.md` | **Pre-registro v0.14** (Rankin, 4-arm, SVD) |
| 64 | `64-plan-tres-ejes-hoja-ruta.md` | **Plan v0.14** (3 ejes A/B/C + hoja de ruta) |

## Framework

Núcleo v0.14 (única fuente de números, SPEC.md en raíz):

| Archivo | Rol | Estado |
| :--- | :--- | :--- |
| `SPEC.md` | Especificación del sistema v0.14 (mundo, redes, qué NO hay) | ✅ B1 |
| `framework/core/` | Paquete núcleo: world, PredictorFactorizado, PhiCanal, z congelado, EWC | ✅ B2 |
| `framework/selftest_core.py` | Smoke test del núcleo | ✅ |
| `framework/bateria_rankin.py` | Batería Rankin N=30 (S1–S5 + dishab + savings + SVD) | ✅ A1 ejecutada (`65`) |
| `framework/factorizado_phi_canal.py` | Φ por canal + 4-arm + SVD | ❌ A3/B4 pendiente |

Scripts que producen números del paper v0.13 (históricos, mundo grid/continuo v0.12):

| Script | Rol | Estado |
| :--- | :--- | :--- |
| `framework/estadistica_fase2.py` + `analisis_fase2.py` | Batería grid N=30 (Tabla 1) | ✅ |
| `framework/rigor_controles.py` | C1–C4 piloto (seed 7) | ⚠️ 1 semilla |
| `framework/h6_selfmodel.py` | Φ calibración | ✅ |
| `framework/organismo_final.py` | Run continuo v0.12 30k | ⚠️ 2º sistema |
| `framework/organismo_completo.py` | Capstone + boca | histórico |
| `framework/m5_24h_local.py` | Run largo | histórico |
| `framework/m4_local_h2b.py` | Con/sin LLM | ⚠️ consistente |
| `framework/m4_local_m3b.py` | Plasticidad | ⚠️ 1 semilla |

Retirados como evidencia (históricos, no citar): `bateria_H4_toy.py` (T1–T3 implementan el
resultado), `m4_local_*.py` tempranos, `benchmark_doorkey.py` (N=5).

## Vivo → muerto (resumen)

- **Hecho (plan 64):** C1/C2/C3+A5 (frente alineado), B1 `SPEC.md`, B2 `framework/core/`,
  **A1 batería Rankin N=30 ejecutada** (`65`, `results/v014_rankin.json`): habituación 84%
  ✅, especificidad de dirección en continuo (H_A grid no se transfiere), S5 intacto,
  Rankin-8 negativo, Rankin-10 ✅, H1 bajo umbral prereg (z0=6.47 < z>10) reportado sin
  recalibrar.
- **Activo v0.14 (plan `64`, prereg `63`):** A2 C1–C4 a N=30, A3 4-arm Φ (A/B/C/D),
  A4 EWC tarea-distinta, B3 predictor factorizado + SVD (parcial: SVD ya en JSON), B4 Φ por
  canal + probe x>14, C4 paper corto + C5 Zenodo v0.14.
- **Prohibido hasta nuevo aviso:** hipótesis nuevas (H7+), V-JEPA/Mamba/GWT en el loop,
  ejecutivos "el organismo vive", simular peer review externo.

*README alineado con paper v0.13. Versión del repo = versión del paper. Los claims retirados
están documentados en CHANGELOG v0.14.*
