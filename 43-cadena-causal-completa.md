# 43 - Cadena Causal Completa: Detecta → Cambia Estado → Actúa → Aprende → Persiste en W

> **Ejecutado:** 29 Ago 2026 18:15 UTC - `python3 framework/m5_cadena_completa.py` (MPS)
> **Este es el experimento que la crítica externa señaló como "mucho más interesante científicamente":** la cadena causal completa, no el predictor aislado.

## Resultado

```
F1 baseline:       z~0    | U 0.31 | exploración 0.01   (forrajea normal)
F2 evento:         z 2.9  | U 1.50 | exploración 0.75   <- detecta Y cambia estado Y actúa
F3 habituación:    z 0.1  (aprendió la nueva física tras 60 repeticiones)
F4: memoria E borrada (80 trazas de eventos eliminadas)
F5 post-E-borrada: z 0.3  | sin E, sin aprendizaje nuevo

HABITUACIÓN F2->F3: z 2.9 → 0.1 (SÍ)
PERSISTENCIA EN W:  SÍ — la traza conductual aprendida permanece en los pesos
=> CADENA COMPLETA DEMOSTRADA
```

## La cadena (lo que la crítica pedía, ahora observado en ejecución)

```
predicción P(s'|s,a)
   ↓
error ε (z=2.9 en evento)
   ↓
estado interno (U 0.31 → 1.50)
   ↓
motivación/política (exploración 0.01 → 0.75)
   ↓
acción
   ↓
consecuencia (mundo responde)
   ↓
plasticidad (habituación z → 0.1, W actualizado vía EWC)
   ↓
nuevo organismo (z 0.3 sin memoria E: la física aprendida vive en W)
```

## Qué distingue esto de un predictor convencional (la regla A≠B)

Un predictor convencional: detecta (z alto) y habitúa (z bajo). **Punto.** No tiene estado motivacional (U) que cambie su conducta, ni la prueba de que el aprendizaje vive en pesos (W) y no en memoria explícita (E).

Este organismo: detecta → el error **modifica su estado interno** → eso **cambia su política de acción** → aprende → y tras borrar toda memoria de eventos (E=∅), la física aprendida **persiste en los pesos** (z 0.3 < 1.45 umbral, sin aprendizaje adicional).

**Cada eslabón de la cadena es observable por separado y falsable.** Es la hipótesis arquitectónica completa (la más ambiciosa), ahora operativa en ejecución local.

## Límites honestos

- **U 1.20 y exploración 0.95 en F5**: la integración sorpresa→U acumula U sin decaimiento; en F5 el organismo sigue explorando por U residual alta. Es una arista de calibración (falta decaimiento de U), no afecta la conclusión de persistencia en W (medida sobre z, no sobre U).
- Toy-scale: MLP pequeño, grid 20×20. La cadena está demostrada en estructura, no en escala biológica.
- El lenguaje sigue siendo verificable: "detecta violaciones, cambia estado, actualiza predictor, reduce error posterior" — no "se sorprende y aprende".

## Decisión de alcance (usuario)

- **Test de LLM intercambiable: descartado** (el LLM actual funciona; no complicar lo innecesario).
- Siguiente paso natural: **organismo completo integrado** (todos los mecanismos + boca LFM2.5 en un solo loop continuo), rumbo al objetivo del proyecto.

*La cadena es el resultado más científico del proyecto hasta ahora: cada eslabón observable y falsable. Ver `framework/m5_cadena_completa.py:1`.*
