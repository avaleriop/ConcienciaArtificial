# 65 - A1 Batería Rankin v0.14 — Resultados (rev.2 tras peer review)

> **Ejecutado:** 2 Sep 2026 (2 corridas N=30 + 1 control N=30, ~2 min en MPS).
> **Pre-registrado:** `63`, `SPEC.md`. **Corregido por peer review** (2 Sep): el protocolo
> v1 (OFFSET) inyectaba un offset +2,+2 incondicional; los números de la rev.1 (84%,
> S2=14.5) quedan **invalidados como habituación** (ver §0 y `bateria_control_habituacion.py`).
> **Regla:** umbrales fijos; nada se recalibró; z por cabeza pos con baseline CONGELADA.

## §0. Por qué se corrigió el protocolo (control decisivo, N=30)

El peer review señaló: "el target siempre es posición+(2,2) sin la física de a" = inyectar un
sesgo. Se corrió un control con 3 brazos de habituación (12 eventos c/u, mismo pre-train):

| Brazo | z_NORM post (integridad) | z_S1 | z_S2 | Lectura |
|---|---|---|---|---|
| **OFFSET** (v1: teleport puro) | **8.25** ❌ modelo roto | 1.43 | 13.42 | offset incondicional; S2>S1 es la firma del sesgo, NO especificidad |
| **CONTING** (física de a + teleport, sin vida entre eventos) | **7.04** ❌ | 1.15 | 13.31 | 12 eventos seguidos siguen dominando el gradiente |
| **INTERCAL** (física + teleport, 5 pasos normales CON updates entre eventos) | **0.81** ✅ | 3.51 | 6.20 | modelo sigue siendo P(s'\|s,a); única base válida |

**Conclusión del control:** la rev.1 entrenaba solo violaciones → el MLP dejaba de predecir
la física normal (z_NORM≈8). Todo lo que se mida con un modelo roto no decide H_vec vs H_A.
La rev.2 usa INTERCAL (violación SOBRE la contingencia real + vida normal entre eventos).

## §1. Resultados rev.2 (INTERCAL, N=30 seeds 4000–4029)

Dos densidades de evento (sweep explícito; no hay ratio pre-registrado, se reportan ambos):

| Métrica | k=10 (evento c/11 pasos) | k=5 (evento c/6 pasos) | Criterio prereg |
|---|---|---|---|
| z0 detección S1 (pre-aprendizaje) | 5.44 CI[4.5,6.4] | 5.44 CI[4.5,6.4] | z>10 y CI no cruza 5 → **⚠️ no pasa** |
| **Reducción z0→z_hab (habituación)** | **8%** CI[0%,17%] | **28%** CI[12%,43%] | >70% → **❌ no pasa** |
| z_NORM_0 (integridad inicial) | 0.03 | 0.03 | ≈0 ✅ |
| **z_NORM post-habituación** | **0.02** ✅ intacto | **0.45** (sube poco) | si alto → modelo roto |
| z(S2) −2,−2 | 5.59 (≈z0) | 6.34 | — |
| z(S3) +2,−2 | 5.07 (≈z0) | 5.53 | — |
| z(S4) +4,+4 | 11.64 | 10.90 | escala con magnitud |
| z(S5) interoceptivo (setup comida) | 16.39 | 16.34 | dispara ✅ |
| Rankin-8 dishabituación (reprobe tras S5) | 6.39 ≈ z_hab | 5.56 vs 3.99 (d≈0.9) | parcial, no concluyente |
| Rankin-10 ISI (gap 2000 pasos, pesos FROZEN) | 4.90 ≈ z_hab 5.05 | 4.13 ≈ z_hab 3.99 | **❌ sin recuperación espontánea** |
| Savings | ~9 | ~7 | débil |
| SVD ΔW f_pos (90% var) | ~1.9 | ~1.8 | low-rank |

## §2. Qué se puede afirmar AHORA (lede honesto)

1. **La habituación fuerte (84%) de la rev.1 era un artefacto de procedimiento.** Cuando la
   violación es un salto puro entrenado sin física intercalada, el MLP aprende un offset
   +2,+2 incondicional: deja de predecir la física normal (z_NORM=8.25) y S2>S1 es la firma
   del sesgo. El control N=30 lo demuestra (brazos OFFSET/CONTING vs INTERCAL).
2. **Con el protocolo que preserva P(s'|s,a) (INTERCAL), la habituación del MLP 13→64 es
   débil**: 8% (evento cada 11 pasos) a 28% (evento cada 6). Lejos del 70% pre-registrado.
   A densidades plausibles de evento (violaciones raras), el efecto tiende a 0. Esto
   **invalida la extrapolación grid v0.13 → continuo** y pone el claim de habituación
   sobre una base mucho más frágil.
3. **Detección continua débil**: z0=5.44 CI[4.5,6.4], bajo el z>10 pre-registrado (el
   umbral se pensó desde el grid ±5; el teleport continuo +2 da ~1/3 de señal). Efecto
   real (CI no cruza 5 por poco), magnitud modesta.
4. **Rankin-8 no demostrado** y **Rankin-10 no**: en reposo con pesos congelados no hay
   recuperación espontánea (Δgap≈0). La "recuperación" de la rev.1 era desaprendizaje del
   offset por re-entreno de física normal, no ISI.
5. **S5 interoceptivo dispara fuerte (z_H≈16)** — la detección de inversión causal de la
   comida existe y no se contamina. Esto es un resultado positivo independiente.
6. **No hay decisión H_vec vs H_A sobre base sólida.** En k=5, S2 (6.3) > S1_hab (4.0) con
   el modelo casi intacto (z_NORM=0.45): *sugiere* especificidad direccional residual, pero
   la habituación base es tan débil (28%) que no sostiene el claim. En k=10 no hay
   diferencia (S2≈z0). El título honesto NO puede ser "H_A refutada".

## §3. Comparación con v0.13 grid (no mezclar; reportar por separado)

| Medida | grid v0.13 (±5, 60 viol.) | continuo v0.14 rev.1 OFFSET | continuo v0.14 rev.2 INTERCAL |
|---|---|---|---|
| Protocolo | violación tras física, 60 seguidas | salto puro, 12 seguidas | física+salto, 12 con vida entre |
| z0 | 20.6 | 6.47 | 5.44 |
| Habituación | 86% | 84% (artefacto) | **8–28%** |
| Modelo intacto (z_NORM) | no medido | roto (8.25) | ✅ 0.02–0.45 |
| Generalización dir. opuesta | sí (C3: 1.1 vs 0.9) | "no" (era el sesgo) | no concluyente |

El grid v0.13 **no midió z_NORM post-habituación**: su "86% con modelo intacto" nunca se
verificó. La rev.2 sugiere que la habituación reportada en v0.12/v0.13 pudo ser en parte
sobre-ajuste al evento inyectado. Esto es un hallazgo metodológico que hay que escribir con
cuidado (el grid entrenaba 60 violaciones seguidas — mismo patrón que OFFSET/CONTING).

## §4. Archivos

- `framework/bateria_control_habituacion.py` + `results/v014_control_habituacion.json`:
  control de interpretación (OFFSET/CONTING/INTERCAL + ISI frozen), N=30.
- `framework/bateria_rankin.py` (rev.2, INTERCAL, `--kintercal`) +
  `results/v014_rankin.json` (k=10, default) + `results/v014_rankin_k5.json`.
- v1 OFFSET: `results/v014_rankin_v1_offset.json` no se conserva como evidencia (números en
  git history del doc); los JSON actuales son rev.2.

## §5. Siguiente

A2 (C1/C2/C4 a N=30) debe usar INTERCAL, no OFFSET. A3 (4-arm) y A4 (EWC tarea distinta)
seguirán sobre el mundo continuo. Antes de cualquier claim de habituación publicable hay que
decidir el ratio de eventos con justificación (no post-hoc): el sweep k∈{5,10} muestra que
el efecto depende críticamente de la densidad de evento — eso es un resultado en sí mismo.
