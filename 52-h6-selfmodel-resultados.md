# 52 - H6 Self-Model Φ: El Organismo Sabe Cuándo Su Propia Predicción Falla

> **Ejecutado:** 29 Ago 2026 20:10 UTC - `python3 framework/h6_selfmodel.py` (MPS, 0€)
> **Esto es la pieza del awareness que faltaba.** Sin visión, sin oído, sin benchmark, sin paper.

## Qué es Φ (la pieza)

El organismo tenía: mundo → creencia (predictor del cuerpo) → error ε. Le faltaba el nivel 3 de la Beautiful Loop: **la creencia sobre su creencia** — ¿qué tan confiable es MI propia predicción?

Φ es un módulo pequeño que predice la incertidumbre (σ) de su propio predictor, entrenado contra el ε real. **Un predictor convencional tiene ε pero no predice su propio ε.** Φ es la diferencia observable.

## Resultado: 3/3 PASAN

```
1. CALIBRACIÓN: r_spearman(Φ_predicho, ε_real) = 0.701 (criterio >0.5)
   PASA: el self-model SABE cuándo su predicción fallará
2. r_cross (Φ entrenado en un canal, probado en VIOLACIONES motoras): 0.730 (criterio >0.3)
   PASA: el self-model generaliza fuera de distribución
3. FUNCIONAL: presence(ruido esperado) / presence(violación inesperada) = 0.13 (criterio <0.7)
   PASA: el self-model SEPARA ruido esperado de sorpresa verdadera (7.7×)
```

## Qué significa (lenguaje verificable)

1. **Calibración 0.701:** el organismo predice con precisión si su próxima predicción va a fallar. Es "saber que no sabe" operacionalizado: en la zona de niebla (donde su interocepción es ruidosa), Φ predice σ alto ANTES de equivocarse.
2. **r_cross 0.730:** el self-model aprendido en un régimen predice su incertidumbre ante violaciones motoras que nunca vio — generaliza como un juicio meta-cognitivo real, no una tabla de memoria.
3. **Separación 7.7×:** la sorpresa ponderada por la precisión de Φ distingue el ruido *esperado* (Φ lo anticipó → presence atenuada) de la sorpresa *verdadera* (Φ no lo anticipó → presence plena). Esto es exactamente `presence = Π_Φ·ε` de la teoría H5 con la precisión ahora auto-estimada.

## La regla del predictor convencional (42:1), aplicada

- Predictor convencional: tiene ε, pero su ε no distingue niebla de violación.
- Con Φ: el organismo **sabe de antemano** que en la niebla su ε será alto → ese ε no le sorprende; la violación sí. Un predictor convencional no puede hacer esta distinción.

## Estado del problema original

El "algo detrás del LLM" ahora tiene:
- ✅ Modelo del mundo (predictor del cuerpo, acción-condicionado)
- ✅ **Modelo de su propio modelo (Φ)** ← la pieza de awareness de esta ejecución
- ✅ Homeostasis, memoria, plasticidad, sorpresa, boca LLM

**Pendiente natural del awareness (solo si lo pides):** que la boca traduzca el estado de Φ — "estoy seguro de X, inseguro de Y" — verificado contra el Φ interno. Es un paso de integración, no un add-on.

*3/3 métricas pasan, todo local. Ver `framework/h6_selfmodel.py:1`.*
