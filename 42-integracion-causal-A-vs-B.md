# 42 - Integración Causal - A vs B: La Sorpresa Cambia la Conducta (Modestamente)

> **Ejecutado:** 29 Ago 2026 18:00 UTC - `python3 framework/m5_integracion_causal.py` (MPS)
> **Crítica externa adoptada íntegra:** integrar antes de cerrar + test A≠B + corregir lenguaje antropomórfico.

## Pregunta (la que faltaba)

¿La sorpresa es una señal decorativa (aparece en un gráfico) o **cambia funcionalmente lo que el organismo hace**? A integrado (ε→U→política) vs B convencional (mismo predictor, ε desconectado).

## Resultado motor (violación con teleport)

```
A integrado:    z violación 5.8 -> 1.0 (habituación 82%)
                U: 0.31 -> 1.49 -> 0.32   <- la sorpresa SUBE la incertidumbre (solo A)
                exploración: 0.01 -> 0.78 -> 0.20  <- post-violación conserva 0.20 (traza persistente)
B convencional: z violación 6.0 -> 0.6 (habituación 91%)
                U: 0.20 -> 0.20 -> 0.20   <- sin acoplamiento, U inmutable
                exploración: 0.04 -> 0.68 -> 0.00  <- post-violación vuelve a 0 (sin persistencia)
Δ exploración: A +0.76 vs B +0.64 -> diferencial causal puro +0.12
```

## Lectura honesta (sin inflar)

1. **El acoplamiento funciona:** solo en A la sorpresa modifica el estado interno (U 0.31→1.49). En B, U permanece 0.20 — el predictor detecta pero no actúa.
2. **El diferencial causal es real pero pequeño (+0.12):** la mayor parte del cambio de exploración (+0.64) viene del cambio de posición (el teleport mueve al agente lejos de la comida). El componente único de la sorpresa es +0.12.
3. **Traza persistente (la firma causal más limpia):** tras cesar las violaciones, A conserva exploración 0.20 (U elevada persiste) mientras B vuelve a 0.00. La sorpresa dejó una marca en el estado interno de A que sobrevive al evento.
4. **Habituación en ambos (82%/91%):** el predictor se actualiza — esperable en cualquier sistema predictivo, no distintivo.
5. **No rompe el resto:** homeostasis y navegación siguen funcionando durante y después.

## Variante interoceptiva (intento de aislamiento puro): NO CONFIRMADA

La violación sin cambio de posición quedó **confundida** por estados iniciales distintos entre runs (U_base A=0.88 vs B=0.20). No es evidencia ni a favor ni en contra — es diseño experimental insuficiente, registrado como pendiente.

## Veredicto adoptado (reformulación de la crítica externa)

- 🟢 **Causalidad funcional parcial:** la sorpresa modifica el estado interno (U) y produce diferencial conductual (+0.12) con persistencia post-evento (0.20 vs 0.00). La integración NO es decorativa.
- 🟡 **Magnitud modesta:** el efecto es real pero pequeño frente al confound de posición. La cadena causal completa `predicción→error→estado→motivación→acción→plasticidad` está operativa pero débil.
- 🔴 **No demuestra awareness:** un predictor convencional con acoplamiento U haría algo similar. El test A≠B mostró diferencia, no brecha categórica.

## Corrección de lenguaje (aplicada en este doc y en `39`,`41`)

- ❌ "el organismo vive, se sorprende, aprende de su sorpresa"
- ✅ "el organismo mantiene un proceso continuo, detecta violaciones de sus predicciones, actualiza el predictor y reduce posteriormente el error ante estímulos repetidos"

## Regla más importante del proyecto (adoptada de la crítica)

> **Cada experimento debe preguntarse: ¿qué resultado sería imposible o muy improbable si esto fuera simplemente un predictor/RNN convencional?** Si la respuesta es "ninguno", el experimento no demuestra nada nuevo.

## Próximos pre-registrados

1. **Aislamiento interoceptivo limpio:** igualar estados iniciales entre A y B (misma semilla de estado, mismo mundo) → medir diferencial puro sin confound de posición.
2. **Cadena completa:** sorpresa→U→política→acción→plasticidad persistente→**borrar memoria E→¿la traza conductual permanece?** (M3b sobre la sorpresa misma).
3. **Test LLM intercambiable:** mismo organismo con LFM2.5 vs otro LLM → ¿conducta esencialmente idéntica? (la prueba final de LLM=boca).

*La integración no es decorativa: +0.12 diferencial con persistencia. Modesta, honesta, real. Ver `framework/m5_integracion_causal.py:1`.*
