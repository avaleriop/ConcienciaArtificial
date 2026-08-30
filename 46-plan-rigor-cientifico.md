# 46 - Plan de Acción: Rigor Científico (Ruta A) - Fases con Justificación

> **Fecha:** 29 Ago 2026 19:00 UTC — respuesta a "haz lo que tengamos que hacer para que sea sólido científicamente"
> **Base:** revisión SOTA `45:1` (CheckVLA 2607.26789, Asleep at the Wheel 2608.01336, Levin Training Ecosystems 2605.30109)

## Principio rector

Cada fase convierte un claim débil en uno falsable. Regla del proyecto (`42:1`): **¿qué resultado sería imposible si esto fuera un predictor convencional?** Cada fase termina con criterios de REFUTACIÓN explícitos.

---

## FASE 1 — Controles de validez (CheckVLA-style) — 1 día, 0€

**Justificación:** CheckVLA (2026) establece que sin baseline de acción-barajada, la detección "acción-condicionada" es indistinguible de novelty de observación. Asleep at the Wheel (2026) mostró que novelty por error predictivo colapsa a azar en protocolos justos. Sin estos controles, nuestro z=40σ es tamaño de efecto sin significado.

| Control | Qué mide | REFUTA nuestro claim si... |
| :--- | :--- | :--- |
| **C1 acción-barajada** | Predictor con acciones al azar (no la acción real) | ...detecta igual de bien (z alto) → el condicionamiento a la acción es ilusorio |
| **C2 observación-sola** | Predictor P(s'|s) sin acciones | ...detecta igual que P(s'|s,a) → la acción no aporta, es novelty pura |
| **C3 deshabituación** | Habituar a violación MOTORA → probar violación INTEROCEPTIVA distinta → volver a MOTORA | ...la violación nueva NO re-dispara z, o la original NO sigue habituada → no hay adaptación específica al estímulo |
| **C4 ablaciones Levin** | a) W re-inicializado tras habituación b) W congelado c) modelo sin entrenar | a) si la traza NO desaparece → no estaba en W b) si el congelado habitúa → la habituación no es aprendizaje c) si el aleatorio detecta → el efecto no requiere física aprendida |

**Producto:** `framework/rigor_controles.py` + `47-resultados-controles.md` con los 4 controles ejecutados.

---

## FASE 2 — Pre-registro + estadística — 1 día, 0€

**Justificación:** una corrida con semilla fija no es evidencia. El campo exige N≥10 seeds, intervalos de confianza y tamaños de efecto. Sin esto, cualquier reviewer desestima los números.

- N=30 seeds para cada condición clave
- Reporte: media ± 95% CI, Cohen's d entre condiciones (z imposible vs z base; habituación curva)
- **Pre-registro escrito ANTES de correr** (hipótesis + criterios de refutación), en `48-preregistro-estadistica.md`
- Resultados en JSON reproducible (`results/*.json`) + script de análisis

**Producto:** pre-registro + tabla de efectos con CI + JSON.

---

## FASE 3 — Benchmark público — 2-3 días, 0€

**Justificación:** sin comparación contra baselines estándar, seguimos siendo "reproducible de lo conocido" aunque los controles pasen. El campo mide sorpresa/intrinsic motivation en MiniGrid DoorKey y con ICM/RND.

- **MiniGrid DoorKey-8x8**: nuestro organismo (predictor+ECUS+sorpresa) vs **ICM** vs **RND** (los dos baselines canónicos de motivación intrínseca) vs aleatorio
- Métricas estándar: pasos hasta puerta, cobertura de estados, éxito
- Alternativa complementaria: protocolo **AvgSurprise** (IntPhys2) sobre nuestro mundo de objetos: pares plausibles vs imposibles, N grande

**Producto:** tabla comparativa + curvas. Si nuestro organismo ≥ baselines en DoorKey, la combinación sorpresa+homeostasis tiene valor medible en benchmark público.

---

## FASE 4 — Empaquetado de reproducibilidad — 1 día, 0€

**Justificación:** sin reproducción no hay ciencia. Todo lo anterior es inútil si nadie puede correrlo.

- `README.md` con comandos exactos por experimento
- `requirements.txt` (torch, mlx-lm, numpy)
- `results/*.json` con todos los números
- Scripts de análisis (`framework/analisis.py` que lee JSON y genera tablas)

**Producto:** repo clonable → `pip install -r requirements.txt` → `python framework/...` → mismos números.

---

## FASE 5 — (Opcional, decisión posterior) Paper de taller

Con Fases 1-4 completas: borrador para **IWAI / ALIFE / CogSci late-breaking**: "Habituación como actualización de modelo en agentes corporizados mínimos: controles, deshabituación y persistencia en pesos". Decisión solo tras ver resultados de Fase 1-2.

---

## Orden y criterio de avance

```
F1 controles (hoy) → si C1-C4 pasan: los claims sobreviven | si alguno falla: claim corregido y re-ejecutado
F2 estadística (hoy-mañana) → efectos con CI reportados, pre-registrados
F3 benchmark (siguientes días) → comparación pública
F4 empaquetado (paralelo a F3) → repo reproducible
F5 paper (decisión con datos en mano)
```

**Regla anti-desliz:** ninguna fase se salta. Un claim sin controles no avanza. Un número sin CI no entra en el JSON.

*Justificación completa en `45:1`. Ejecuto F1 ahora (minutos, 0€).*
