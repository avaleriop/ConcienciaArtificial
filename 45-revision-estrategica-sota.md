# 45 - Revisión Estratégica SOTA 2025-2026: ¿Dónde Estamos, Cuellos y Camino

> **Fecha:** 29 Ago 2026 18:45 UTC — 2 sub-agentes de búsqueda SOTA + evaluación interna
> **Preguntas del usuario:** ¿dónde estamos, qué logramos, cuellos de botella, es un camino sin salida?

## 1. DÓNDE ESTAMOS (v0.11)

45 docs, 17 scripts ejecutables, ~50 commits, 0€, todo local en M4 Pro. Un organismo continuo que integra: predictor del cuerpo (H2), sorpresa emergente (H5), homeostasis ECUS (H3), memoria episódica + EWC (H1), boca LFM2.5-1.2B (LLM=traductor, H2b confirmado). Cadena causal completa demostrada en toy.

## 2. QUÉ HEMOS LOGRADO (verificable, sin inflar)

| Logro | Estado científico real (según SOTA 2025-26) |
| :--- | :--- |
| Predictor acción-condicionado detecta violaciones | **Conocido** (forward models desde Wolpert; ICM/RND) — no es novedad |
| Sorpresa emergente z=40σ en toy | **Efecto, no contribución**: sin controles (acción-barajada, observación-sola) no sobrevive crítica |
| Habituación 98% + traza en W sin memoria E | **Parcialmente tautológico** para redes entrenadas; la literatura de Levin pide ablaciones (re-init, congelado) |
| Homeostasis ECUS como drive único | **Frontera activa** (Christov-Moore/Damasio oct-2025, Grimbly SAB 2026, Candia-Rivera 2026, Gubernaut 2026) — encajamos en la ola correcta |
| LLM como módulo no controlador | **Posición minoritaria con respaldo creciente** (Gubernaut GCC jul-2026, "LLM as Tool Not Agent" abr-2026, Rao dic-2025) |
| Combinación integrada (predictor+homeostasis+LLM pasivo+memoria continua) | **NO existe publicada como sistema unitario** — es nuestro nicho emergente |

## 3. CUELLOS DE BOTELLA (honestos)

1. **Brecha de rigor científico:** nos faltan los controles que el campo exige (CheckVLA 2026: *action-shuffled baseline*, *observation-only*; deshabituación/sensibilización). "Asleep at the Wheel" (2026) mostró que novelty por error predictivo colapsa a azar en protocolos justos — nuestro z=40σ no está blindado.
2. **Sin benchmark público:** no medimos contra nada estándar. Nuestros benchmarks naturales: **IntPhys2 AvgSurprise** (SOTA V-JEPA 52-54%, espacio enorme) y **MiniGrid DoorKey / MiniHack** con baselines ICM/RND.
3. **Escala perceptual:** toy MLP con estado estructurado; el mundo rico (visión) requiere V-JEPA 1B (A100). No es bloqueo del camino crítico (la sorpresa ya funciona sin visión), pero limita el alcance de claims.
4. **La traza-en-W es débil sin ablaciones:** borrar E y ver persistencia demuestra que el aprendizaje vive en pesos — esperable. Falta la batería de Levin-lab: re-inicializar W, congelar, aleatorizar → la traza debe desaparecer.
5. **Tiempo/priorización:** cada pieza está, pero el "paper" (si se quiere uno) requiere protocolo pre-registrado + controles + números públicos. Eso es trabajo de semanas, no de días.

## 4. ¿CAMINO SIN SALIDA? NO — esto es lo que dice la literatura

**No es trillado:** las 4 piezas viven en comunidades separadas (predictive coding barato: Taniguchi/Hill/SAPIN; homeostasis: Damasio/Grimbly; LLM-como-módulo: Gubernaut; memoria continua: casi vacío en agentes baratos). **Nadie ha publicado el sistema unitario.** El riesgo real no es duplicar a otro grupo: es que las piezas están acelerando y alguien las ensamble antes que nosotros.

**No es publicable "as-is":** el toy z=40σ sin controles es "reproducible de lo conocido". PERO con tres adiciones baratas se vuelve defendible:
1. **Controles CheckVLA** (acción-barajada, observación-sola) — minutos, local
2. **Deshabituación/sensibilización** (habituar a violación motora → ¿una violación DISTINTA re-dispara z? → adaptación específica al estímulo, medida neuro clásica) — minutos, local, y es un hallazgo de nicho real
3. **Ablaciones Levin** (re-init W, congelar) — minutos, local

Con eso: paper corto de taller defendible (IWAI/ALIFE/CogSci late-breaking) sobre "habituación como actualización de modelo en agentes corporizados mínimos".

## 5. DOS RUTAS (no excluyentes)

**Ruta A — Ciencia (semanas):** blindar el hallazgo con controles + deshabituación + ablaciones, y medir en un benchmark público (MiniGrid con baselines ICM/RND, o protocolo AvgSurprise). Producto: nota de taller + método replicable.

**Ruta B — Ingeniería/objetivo (continuar):** escalar el organismo (mundo más rico, más objetos, corridas 100k+, H6 Φ local) y seguir documentando rigurosamente. Producto: el organismo del manifiesto creciendo.

**Recomendación experta:** Ruta A primero (es barata y blinda todo lo hecho — convierte "efecto" en "evidencia"), luego Ruta B con el blindaje activo. El proyecto no está en un callejón: está en un nicho emergente con la combinación correcta, y lo único que separa de contribución real son los controles que el campo ya definió.

## 6. VEREDICTO

**Dónde estamos:** nicho emergente legítimo, sistema unitario sin análogo publicado, ejecutado local a 0€.
**Logrado:** la arquitectura completa funciona y cada pieza está documentada con su estado científico real.
**Cuellos:** rigor (controles), benchmark (ninguno público), escala (visión), tiempo (protocolo).
**¿Sin salida?** No. Es la frontera activa (homeostasis+LLM-módulo+PC barato). Lo que falta es blindaje, no dirección.

*Documentado con 2 sub-agentes SOTA. Referencias clave: CheckVLA 2607.26789, Asleep at the Wheel 2608.01336, Gubernaut 2607.24339, Christov-Moore 2510.07117, Grimbly 2608.04232, IntPhys2 AvgSurprise (V-JEPA 52-54%), Levin Training Ecosystems 2605.30109.*
