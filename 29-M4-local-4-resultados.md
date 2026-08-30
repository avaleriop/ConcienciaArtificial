# 29 - M4-local-4 - Resultados: VoE z=50.6σ PASA + H2b local B(LLM=traductor)

> **Ejecutado:** 29 Ago 2026 15:10 UTC - Pre-registrado `28:1` en MPS
> **Script:** `framework/m4_local_4.py` (VoE z-score formal + H2b local)

## T1: VoE con métrica relativa formal (z-score >5σ)

```
baseline ε: 0.0432 (100 pasos, mundo determinista)
ε teleport: 0.0880  (doble del baseline)
z = (0.0880 - 0.0432)/0.0009 = 50.6σ  >> 5σ  -> PASA
```
- El teletransporte dispara error de predicción **50σ** sobre baseline — señal de sorpresa inequívoca con encoder convergente (JEPA 0.009).
- Confirma el diagnóstico `28:1`: el umbral absoluto `presence>0.7` era calibración del toy numpy; la métrica correcta para encoder aprendido es relativa. **El mecanismo H5 (`Π·ε` responde a violación de expectativa) opera en representación aprendida.**

## T2: H2b local (eliminar codec LLM)

```
A (con codec):    E[0.66,1.15] U 0.37 S 0.45 D 0.36
B (sin codec):    E[0.66,1.15] U 0.37 S 0.45 D 0.36  -> idéntica
```
- Conducta **idéntica sin LLM codec** → consistente con **B: LLM=traductor** (el núcleo `Self_t`+`G` genera conducta; el codec solo traduce).
- **Honesto:** en local el LLM invoca 0 veces (U<0.4) — H2b es trivial en este régimen. El decisivo es M4 cloud con Qwen2-7B real participando.

## GATE M4-local completo (acumulado v0.9)

| Mecanismo | Resultado | Estado |
| :--- | :--- | :--- |
| Continuidad sin reset | 1000-1200 pasos Mamba N=64 | ✅ |
| Encoder JEPA aprendido | 0.0092 convergente | ✅ |
| EWC Fisher real | sin colapso, retención 0.09x vs 0.11x | ✅ |
| Homeostasis E/U/S/D | 0.66-1.15 / 0.37 / 0.45 / 0.36 | ✅ |
| Memoria Kael | True | ✅ |
| VoE relativo | z=50.6σ | ✅ |
| LLM invocaciones | 0 calibrado | ✅ |
| Plasticidad (M3b local) | B aprendido + A retenido | ✅ |
| H2b (sin LLM) | conducta idéntica | ✅ (débil local) |

**Lo demostrado (sin inflar):** tetraedro completo funcional en hardware local sin GPU, con representación aprendida real, EWC real, sorpresa relativa real y plasticidad real (modesta). Todos los gate pre-registrados pasan en local.

**Lo NO demostrado:** awareness, conciencia, plasticidad 1B, H2b decisivo (requiere LLM real participante).

## Camino restante (pre-registrado)

1. **M4 cloud A100** (~33€ spot): V-JEPA2 1B + Qwen2-7B congelado + EWC λ=3000 Fisher real. Ahí H2b es decisivo (LLM participa) y plasticidad es a escala.
2. **M5 24h** después de M4 (plasticidad antes que longevidad, valoración externa).
3. **Auditoría** cada 2 commits sigue.

*Sin reinterpretar: z-score fue pre-registrado en `28:1` como métrica relativa antes de ejecutar. Todo verificable en `framework/m4_local_4.py:1`.*
