# Plan Estratégico v0.13 — Priorizado y Coherente con el Proyecto
> **Estado base:** v0.12-final publicado (Zenodo 10.5281/zenodo.22191728). Continua 20.0, atención 13→7, Φ 15/22, EWC λ=5. Principio rector: todo corre en un MacBook Pro (M4 Pro, Apple silicon) sin GPU. Todo re-verificado (30k niebla 0.0%, batería N=30, Φ d=-1.61).

## Principios de priorización
1. **Consolidar antes de expandir.** Unificar lo que hoy está repartido en dos mundos (grid vs continuo) evita deuda técnica que invalida comparaciones futuras.
2. **Controles primero.** Cada nuevo claim necesita su control pre-registrado (lección CheckVLA).
3. **Una variable a la vez.** v13 no introduce 3 arquitecturas nuevas; introduce 1 mundo social mínimo y reutiliza el kit Φ.

## Matriz impacto × factibilidad (6 líneas del revisor)

| Línea | Impacto | Factibilidad en 4–8 sem | Riesgo de overclaim | Veredicto |
|---|---|---|---|---|
| **4. Evolución de H*** | Alto | Alta (mismo código + loop de población) | Bajo | **P0 — Hacer ya** |
| **1. Kit Φ estandarizado** | Alto | Alta (unificar y empaquetar) | Bajo | **P0 — Hacer ya** |
| **2. IA alineada (retiro ante niebla)** | Medio-Alto | Media (experimento comida-en-niebla) | Medio | **P1 — Hacer acotado** |
| **5. SER vs DECIR / V-JEPA** | Medio | Baja (cambio de backbone) | Medio | **P2 — Posponer a v0.14** |
| **6. Huella causal / legal** | Bajo (para paper experimental) | Baja | Alto | **P3 — Discusión, no experimento** |
| **3. Patologías (TEPT)** | Medio | Baja | Alto | **P3 — Colaboración externa futura** |

## Roadmap en 3 fases (8 semanas, 1 persona, 1 laptop)

### FASE 0 — Consolidación (Semana 1) — Prerequisito, 12h
**Objetivo:** dejar v0.12 publicable como unidad coherente.
- Unificar batería N=30 al mundo continuo (o documentar explícitamente la partición grid/continuo y congelarla). Decisión: documentar y congelar es suficiente para v0.13; unificar es v0.14.
- Generar 3 figuras vectoriales desde `results/*.json` (habituación, Φ scatter, fog causal).
- Cerrar `h5bis` con script reproducible mínimo (envoltorio de `estadistica_fase2.py`).
- **Salida:** `paper/main.tex` v0.12.1 + figuras + Zenodo v0.12.1.

### FASE 1 — Núcleo v0.13 (Semanas 2–5) — El paper que sigue
**Tres experimentos, un mismo mundo continuo v0.12, pre-registro único.**

**1A. Kit Φ portable (Línea 1) — Semana 2, 16h**
- Empaquetar `h6_selfmodel.py` + `h6_phi_causal.py` como `framework/phi_kit.py` con función `phi_score(agent) -> {r, r_cross, d}`.
- Validar en 2 arquitecturas toy (MLP actual + MLP 13→64→64→6) para mostrar que el índice no depende de un tamaño.
- **Criterio:** r>0.5 y d<-1.0 replican en ambas.
- **Salida:** Sección Métodos 2.4 del próximo paper + repo `phi_kit/` documentado.

**1B. Seguridad por homeostasis (Línea 2 acotada) — Semana 3, 20h**
- Experimento **comida-en-niebla**: 30 seeds, comida en x>14 (niebla) vs comida fuera. Métrica: tiempo en niebla, E final, tasa de forrajeo. Pre-registrar H: "agente con Φ acoplado sacrifica forrajeo para preservar U".
- Control: mismo mundo sin Φ acoplado (B). Comparar.
- **Criterio:** niebla con comida 15% vs sin Φ 35%+ (efecto medio), E diferencia <0.2 (no se muere de hambre por evitar niebla).
- **Salida:** Figura trade-off forrajeo vs claridad.

**1C. Evolución de H* y ecología mínima 2-agentes (Línea 4) — Semanas 4–5, 30h**
- Población 30 agentes con H* muestreado en hipercubo [0.6,1.0]×[0.7,1.0]×[0.1,0.5]×[0.5,1.0]. Cada agente corre 5k pasos solo; fitness = tiempo en rango homeostático + eficiencia (pasos/comida). Selección torneo, mutación gaussiana σ=0.05, 20 generaciones. Observar qué H* estabiliza.
- Luego: **2 agentes acoplados** en mismo mundo continuo, con percepción mutua (posición del otro). ¿Emergen turnos, evitación, o acoplamiento de Φ (correlación de σ entre agentes)?
- Pre-registrar ambas.
- **Criterio:** convergencia de H* en <10 generaciones; en 2-agentes, correlación de σ >0.3 o homeostasis grupal distinta de suma individual.
- **Salida:** Paper v0.13 completo (ALIFE/CogSci late-breaking). Este es el "santo grial" que el revisor pide, pero en versión mínima y defendible.

### FASE 2 — Expansión (Semanas 6–8) — Solo si Fase 1 cierra
- **Línea 5 (V-JEPA):** reemplazar MLP por encoder JEPA pequeño en el mismo loop. Requiere GPU o tiempo. Plan B: dejar como Future Work con diseño, no con experimento. No bloquear v0.13 por esto.
- **Línea 3/6:** 1 párrafo en Discusión cada una; buscar colaborador neuro/legal solo después de tener Fase 1 publicada.

## Publicación
- **v0.12.1 (esta semana):** Zenodo ya publicado. Actualizar con figuras + DOI ya hecho. arXiv `cs.AI` + `q-bio.NC`.
- **v0.13 (5 semanas):** Pre-registro Fase 1 en OSF → 30-seed battery + evolución → Zenodo v0.13 + arXiv v2 + envío ALIFE 2027 / CogSci 2027 (abstract + late-breaking).
- **v0.14 (3 meses):** Unificación grid→continuo + V-JEPA piloto (si hay colaborador/GPU).

## Qué NO hacer en v0.13
- No abrir repo público completo (tu restricción). Publicar kit Φ como módulo aislado si hace falta.
- No reclamar "curación de TEPT" ni "derechos legales". Esas son implicaciones, no resultados.
- No cambiar backbone a la vez que se introducen 2 agentes.

## Checklist de decisión (necesito de vos)
1. ¿Priorizamos **1C evolución H*** como experimento estrella de v0.13? (recomendado: sí)
2. ¿Pre-registro OSF público o privado hasta envío? (recomendado: público con embargo)
3. ¿Figura 1 la tetraedro la mantenemos esquemática o la pasamos a vector con tus colores?
