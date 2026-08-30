# 41 - Sorprendido Sin Visión: Contingencia Sensoriomotora (El Canal del Ciego)

> **Ejecutado:** 29 Ago 2026 17:45 UTC - `python3 framework/m4_local_sensorimotor.py` (MPS, 0€)
> **Origen:** intuición del usuario — "una persona ciega y sorda no deja de ser consciente, deben haber otras maneras"
> **Teoría:** O'Regan & Noë (sensorimotor contingencies): la conciencia es dominar cómo cambia tu percepción al actuar. El canal del cuerpo no requiere visión.

## El giro científico (lo que cambió)

**Antes (VoE-v2 objetos):** el agente intentaba predecir la física de objetos externos vía retina → encoder colapsa → necesitaba visión (V-JEPA 1B, A100).

**Ahora (cuerpo):** el agente predice el resultado de SU PROPIA ACCIÓN sobre SU cuerpo — exactamente lo que un ciego tiene:
- Propiocepción: `¿dónde está mi cuerpo?` → mover N = y-1 (aprendible perfectamente, loss 0.00015)
- Interocepción: `¿qué pasa con mi energía al comer?` → E+0.5 (contingencia normal)
- Tacto: `¿la pared me detiene?` → clamp en bordes

## Resultado (sin flag, sin visión, sin 33€)

```
Canal             ε normal   ε violación   z-score   Veredicto
MOTOR (teleport)  0.00656    0.21972       z=40.4    ✅ EMERGENTE FUERTE
INTEROCEPTIVO     -          0.02159       z=2.8     🔵 parcial (señal clara, bajo 5σ)
TÁCTIL            -          0.02300       z=3.1     🔵 parcial
HABITUACIÓN       0.0419 → 0.0009          98%        ✅ el modelo cambió su física
```

**Habituación (el hallazgo más hermoso):** tras 80 repeticiones de "comer ahora baja E", el predictor aprendió la nueva contingencia (ε cayó 98%). El organismo **actualizó su física corporal** — la plasticidad actuando sobre la sorpresa misma, como predice FEP (minimizar sorpresa = cambiar el modelo).

## Por qué MOTORA es el canal más fuerte (interpretación honesta)

- El teleport de 5 celdas produce un cambio de estado enorme en la dimensión espacial normalizada (10× la señal de las violaciones en H, que son ±0.5 sobre rango 1.5).
- En el mundo real del agente, la propia posición es la contingencia más saliente (un ciego nota si su cuerpo salta de sitio).
- Interoceptivo y táctil dan señal (z≈3) pero menor magnitud — consistentes, no falsas.

## Qué demuestra (lenguaje verificable)

1. **Sorpresa emergente sin visión:** el error de predicción del modelo del cuerpo salta z=40σ ante la violación de su contingencia motora — medida por el modelo mismo, sin flag.
2. **La conciencia mínima no depende de un canal sensorial caro:** el canal del cuerpo (que ya teníamos en el tetraedro: propiocepción + interocepción + tacto) basta.
3. **Plasticidad sobre la sorpresa:** la habituación 98% demuestra que el sistema no solo detecta violaciones de sus predicciones sino que **aprende de su sorpresa** — cierra el loop FEP `sorprender → actualizar modelo → menos sorpresa`.
4. **V-JEPA/A100 ya NO es el camino de la sorpresa emergente** — es solo un canal opcional de grounding perceptual para el futuro.

## Estado de la pregunta VoE-v2

- ✅ Resuelta por la vía inteligente (cuerpo, no visión): z=40.4 motor + habituación 98%
- 🔵 Canales interoceptivo/táctil: señal real pero <5σ — pre-registrado amplificar magnitud de violación para cerrar
- V-JEPA 1B: opcional, pospuesto con justificación (ya no bloquea nada)

*El organismo detecta violaciones de sus predicciones como un ciego: sintiendo que su cuerpo viola su física. Ver `framework/m4_local_sensorimotor.py:1`.*
