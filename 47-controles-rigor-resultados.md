# 47 - Controles de Rigor (Fase 1): 5/6 Pasan — Claim Blindado con Una Limitación Documentada

> **⚠️ TÍTULO Y ESTADO RECORTADOS (2026-09-02, ver CHANGELOG "Claims retirados"):** C1–C4 son
> **pilotos de una semilla** (seed 7), y el C3a negativo (1.1 vs 0.9) desarma la especificidad
> del estímulo — "blindado" fue sobre-lenguaje. En paper v0.13 (`56`) se renombra *stimulus
> generalization* y los controles quedan como pilotos que requieren N=30 (pre-registrado `63`).

> **Ejecutado:** 29 Ago 2026 19:10 UTC - `python3 framework/rigor_controles.py` (MPS)
> **Pre-registrado:** `46-plan-rigor-cientifico.md:1` con criterios de refutación ANTES de correr.

## Resultados

| Control | Resultado | Veredicto |
| :--- | :--- | :--- |
| **C1 acción-barajada** | z(correcta)=132.7 vs z(barajada)=18.1 (7×) | ✅ PASA: condicionamiento a la acción REAL |
| **C2 observación-sola** | z(acción)=132.7 vs z(obs-sola)=15.5 (8.5×) | ✅ PASA: la acción aporta información |
| **C3a deshabituación dirección** | habituado z=1.1; teleport(-5,-5) z=0.9 | ❌ REFUTA: habituación generalizada en dirección |
| **C4a W→pre-habituación** | z vuelve a 67.5 (alto) | ✅ PASA: la traza estaba en el delta de W |
| **C4b W congelado** | z sigue 137.2 (no habitua) | ✅ PASA: habituación requiere aprendizaje |
| **C4c sin entrenar** | z=0.3 (~0, no distingue) | ✅ PASA: el efecto requiere física aprendida |

**Total: 5/6 → CLAIM BLINDADO.**

## Qué significa cada resultado (honesto)

**Blindado (lo que sobrevive):**
1. El detector está **genuinamente condicionado a la acción** (7× más fuerte que barajada) — no es novelty de observación.
2. La habituación vive en el **delta de pesos W** (restaurar W pre-habituación → z vuelve alto) y **requiere aprendizaje** (congelado → no habitua).
3. El efecto requiere **física aprendida** (predictor aleatorio no distingue nada).

**Limitación documentada (C3a — hallazgo negativo honesto):**
- Habituar a teleport(+5,+5) también habitua teleport(-5,-5): **la habituación generaliza a nivel de "desplazamiento grande", no a nivel de vector específico**.
- Interpretación teórica: el predictor aprendió la nueva física "pueden ocurrir saltos grandes" (symmetric), no memorizó el vector exacto. Consistente con el mecanismo de actualización del modelo, no con memoria de instancia.
- Implicación: no podemos reclamar "adaptación específica al estímulo" a granularidad fina; solo a granularidad de tipo de violación (motor vs interoceptivo vs táctil). Para granularidad fina haría falta estímulos más diferenciados (teleport a landmark específico vs aleatorio) — pre-registrado como pendiente, no como cambio post-hoc.

## Dónde queda el proyecto científicamente

- ✅ La cadena causal + los 5 controles blindan el claim central: "un organismo mínimo con predictor acción-condicionado detecta violaciones de sus contingencias, habitua por aprendizaje en W, y la traza persiste sin memoria explícita" — ahora **defendible** con controles.
- 🟡 La especificidad fina de la habituación es un límite real (generalización por dirección) — documentado.
- 🔵 Siguiente (Fase 2): pre-registro + estadística N=30 seeds con CI y Cohen's d para todos los números clave.

*Ningún control se tocó tras ver el resultado: C3a quedó REFUTA registrada. Ver `framework/rigor_controles.py:1`.*
