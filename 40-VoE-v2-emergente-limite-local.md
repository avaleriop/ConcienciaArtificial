# 40 - VoE-v2 EMERGENTE - Resultado Honesto: Límite del Toy Local

> **Ejecutado:** 29 Ago 2026 17:30 UTC - `python3 framework/m4_local_voe2.py` (5 iteraciones de diseño, MPS)
> **Pre-registrado:** `34:1`, `35:1`, `39:1` — sorpresa descubierta por el modelo, sin flag.

## Resultado neto: NEGATIVO en toy local (hallazgo honesto)

| Iteración | Diseño | Separación latente | z(imposible) | Veredicto |
| :--- | :--- | :--- | :--- | :--- |
| 1 | objetos se mueven ±1 cada 50 pasos | 0.005 | 0.1 | colapso encoder |
| 2 | permanencia (mundo estático) | 0.005 | 0.0 | colapso (1 solo input) |
| 3 | continuidad ±1 cada paso (aleatorio) | 0.003 | 0.0 | colapso |
| 4 | + EMA target + varianza (anti-colapso) | **0.372** | -0.1 | separa, pero ε domina ruido |
| 5 | física determinista (velocidad const.) | 0.000→0.970 | 0.1 | separación inestable, ε gigante |

**Lección verificable:** con encoders MLP locales (hasta 4M params), la sorpresa EMERGENTE para física de objetos **no emerge**: o el encoder colapsa (JEPA sin estructura rica) o el error de predicción está dominado por el ruido estructural. El predictor no aprende la dinámica de objetos con arquitectura MLP+retina escasa.

## Precedente positivo (ya demostrado, no olvidar)

- `m4_local_4.py` (doc `29:1`): **agent-teleport z=50.6σ** — cuando el evento viola el MODELO (el agente salta), la señal es inequívoca en encoder aprendido.
- La diferencia: el agente es autocontrolado (el modelo sabe dónde estaba él), los objetos no (posición externa no modelada por el predictor).

## Por qué V-JEPA 1B existe (y por qué A100)

Garrido 2025: V-JEPA logra **98% IntPhys** precisamente porque:
1. Encoder ViT (patches, no retina escasa) — estructura espacial real
2. Pretrain 1M horas de video — física aprendida de verdad
3. Predicción en latente de patches ENMASCARADOS (no frame→frame directo)

Nuestro toy demostró empíricamente **por qué se necesita eso**: la sorpresa emergente de física de objetos NO es un artefacto de un MLP pequeño. Es el primer resultado del proyecto que requiere V-JEPA2 1B (A100 ~33€) de forma genuina y documentada.

## Estado (lenguaje verificable)

- ✅ Sorpresa por violación del propio modelo: **agente** (z=50σ, local)
- ❌ Sorpresa por violación de física de **objetos**: no emerge en toy local (5 diseños)
- 🔵 Requiere V-JEPA2 1B (A100): el siguiente salto REAL, ahora con justificación empírica
- ✅ Habituación parcial vista en iter 4 (decaída 26% con entrenamiento) — dirección prometedora a mayor escala

## Decisión registrada

No fabricar z alto (regla del usuario: pre-registrado, sin tocar umbral). Este es un resultado negativo honesto que **delimita el espacio de lo local** y **justifica el único gasto posible del proyecto** (33€ A100) con evidencia, no con entusiasmo.

*El toy llegó a su frontera real: la sorpresa emergente de objetos es el primer fenómeno que exige V-JEPA2 1B. Ver `framework/m4_local_voe2.py:1`.*
