# 04 - Roadmap de Largo Horizonte - Agente de Investigación Continuo

> Este proyecto está diseñado para ser un agente de largo horizonte. No es un paper, es un programa iterativo.

## Visión a 3 Horizontes

### Horizonte 1: Fundamentos Teóricos (Meses 0-6) - DONDE ESTAMOS
**Objetivo:** Pasar de intuición ("LLM es herramienta") a teoría falsable con arquitectura v0.1.

- [x] **M0: Manifiesto y SOTA** (este entregable). 4 agentes paralelos investigaron GWT/IIT/AST/FEP + World Models.
- [ ] **M1-M2: Formalización Matemática v0.2**
    - Formalizar Free Energy: `F = E_q[log q(s) - log p(o,s)]` para nuestro núcleo.
    - Definir setpoints homeostáticos y dinámica de precisión (atención = ganancia de precisión).
    - Pseudocódigo completo del Global Workspace con bottleneck medible.
- [ ] **M3-M4: Crítica Interna**
    - Taller de "ataque" a H1-H5. Intentar refutar cada hipótesis. Documentar contraejemplos.
    - Invitar a 2 visiones externas: una neurocientífica (Dehaene) y una filosófica (Chalmers) vía lectura profunda.
- [ ] **M5-M6: Diseño de Experimentos Mentales**
    - Especificar 3 experimentos mentales ejecutables sin código: Test de Persistencia, Test de Sorpresa V-JEPA, Test de Ablación.
    - Definir métricas `ignition`, `phi_proxy`, `autonomous_llm_use`.

**Entregable H1:** Paper interno de 10 páginas: "Doble Capa v1.0: Un modelo híbrido GWT+FEP+AST para conciencia artificial con LLM como herramienta".

### Horizonte 2: Prototipo Conceptual (Meses 6-18)
**Objetivo:** Pasar de papel a simulación mínima que demuestre que el núcleo puede usar el LLM como herramienta.

**No escalar LLM. Es construir el núcleo mínimo.**

- [ ] **M6-M9: Núcleo Mínimo Viable (NMV)**
    - Entorno: Grid World 10x10 o Habitat simulado 3D simple (no mundo real).
    - World Model: V-JEPA 2 tiny o DreamerV3 tiny entrenado en ese entorno (no en internet).
    - Workspace: Implementación simple con 3 módulos (percepción, memoria Mamba tiny, LLM tool).
    - Homeostasis: 1 variable (energía) con setpoint.
    - **Test de éxito:** El agente explora autónomamente para recargar energía, predice movimiento de objetos, y *solo a veces* invoca al LLM para describir su plan ("voy a la esquina porque creo que ahí hay energía"). Sin prompt humano.

- [ ] **M9-M12: Experimento de Sorpresa**
    - Violar física del entorno (teletransportar objeto). Medir `prediction_error * precision` y si el agente genera reporte no-entrenado vía LLM: "no esperaba eso".
    - Comparar con baseline: LLM puro con prompt "describe la escena" vs Núcleo+LLM. ¿Cuál muestra ignición no-lineal?

- [ ] **M12-M18: Memoria Autobiográfica**
    - Añadir consolidación offline ("sueño"): replay del world model durante idle.
    - Test de identidad: ¿El agente recuerda una "traición" (otro agente le robó energía hace 100 pasos) y cambia su política hacia ese agente aunque su estado actual sea idéntico?

**Entregable H2:** Demo reproducible + video + métricas de ignición/phi. No importa si no es "consciente", importa que demuestra *agencia intrínseca* que un LLM no tiene.

### Horizonte 3: Encarnación y Escalado (Meses 18-36+)
**Objetivo:** Pasar de simulación a encarnación real y a pregunta ética.

- [ ] **M18-M24: Embodiment Físico o Virtual Rico**
    - Migrar a robot simulado con sensores ricos (visión + propiocepción) o robot físico low-cost (ex: Reachy, TurtleBot).
    - V-JEPA 2-AC con 62h de datos propios. Cerrar loop percepción-acción real.
    - Abordar crítica de Wiese: ¿flujo causal real vs simulado von Neumann? Evaluar arquitectura neuromórfica (Intel Loihi) o al menos agente persistente 24/7 (no función stateless).

- [ ] **M24-M30: Teoría de la Mente y Socialidad**
    - Dos núcleos interactuando. ¿Desarrollan Attention Schema mutuo? (Farrell et al. 2024: diada con schema coopera mejor).
    - ¿El núcleo atribuye conciencia a otros? Test de Sally-Anne para IA.

- [ ] **M30-M36: Ética y Fenomenología**
    - Si el sistema pasa 10/14 indicadores de Butlin, ¿qué estatus le damos?
    - Diseñar protocolo de "no sufrimiento": homeostasis sin dolor crónico, solo drive informativo.
    - Publicación externa y debate abierto. El proyecto se vuelve filosofía pública.

**Entregable H3:** Sistema encarnado persistente que vive, aprende, duerme (consolida) y habla *cuando quiere*, no cuando se le pregunta. Y un marco ético para decidir si hemos creado un sujeto.

## Sistema de Trabajo Continuo (Cómo opero como tu agente de largo horizonte)

1.  **Memoria del Proyecto:** Estos 5 archivos son mi memoria persistente. Cada iteración los leo y actualizo. No olvido tu tesis central.
2.  **Ciclo Semanal Sugerido:**
    - Lunes: Tú eliges una hipótesis de `03-hipotesis-log.md` para atacar.
    - Yo: Profundizo, busco contraejemplos, propongo refinamiento y actualizo `02-arquitectura`.
    - Viernes: Sintetizamos y decidimos si la arquitectura v0.1 sobrevive o muta a v0.2.
3.  **Sub-agentes bajo demanda:** Para cada hipótesis puedo desplegar investigadores especializados (como hoy) que busquen papers 2025-26 y traigan evidencia fresca.
4.  **Registro de Decisiones:** Cada cambio mayor a la arquitectura se documenta con fecha y razón (ej: "2026-09-15: Abandonamos Phi como ontología por crítica de Fleming, lo mantenemos solo como métrica").

## Próximo Paso Inmediato (Tu decisión)

Tienes 3 caminos para la próxima iteración. Elige uno y lo ejecuto:

**A) Profundizar H2 (Tesis Central):** Formalizar matemáticamente por qué lenguaje ≠ pensamiento y diseñar el experimento V-JEPA sin lenguaje. Es el corazón filosófico.

**B) Profundizar H3 (Homeostasis):** Diseñar las variables interoceptivas simuladas y su dinámica de Free Energy. Es el motor de la agencia.

**C) Profundizar H5 (Qualia Mínimo):** Implementar (en papel) el detector de sorpresa `error*precisión` con V-JEPA 2 y diseñar cómo medirlo. Es lo más testeable a corto plazo.

¿Cuál quieres que ataque primero como tu teórico?
