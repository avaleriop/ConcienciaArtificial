# 64 — Panel de tres ejes y hoja de ruta realista

> Documento de planificación. No modifica código ni claims. Fecha de redacción: 2 Sep 2026.
> Base: peer-review interno del repo `ConcienciaArtificial` (teoría `00`–`13`, framework, `results/`, paper `56`, panel `61`–`62`).
> Los “agentes” son roles de revisión, no autoridades externas.

---

## Encargo

Tres revisores independientes, cada uno con un eje y un criterio de éxito distinto. Se les pidió:

1. Diagnosticar el estado *actual* (no el estado narrado en README/INDEX).
2. Decir qué está muerto, qué está herido y qué está vivo.
3. Proponer solo acciones que quepan en **1 persona + 1 laptop + 8 semanas**, sin GPU cloud.
4. Incluir criterios de matar el claim (si X, no se publica Y).

---

# AGENTE A — Validez empírica y métodos

**Eje:** ¿qué se puede afirmar ante un reviewer que abra `framework/*.py`?
**Lente:** psicología experimental de habituación, controles tipo CheckVLA, estadística mínima publicable.
**Criterio de éxito:** cada número de una tabla futura es regenerable, con N declarado, y no se puede reconstruir “a mano” leyendo el test.

## Diagnóstico

El activo empírico no es el tetraedro. Es un **kit de habituación-en-pesos** sobre un forward model pequeño, más un cabezal que predice `|ε|`.

Vivo:

- Detección de violación inyectada (z alto, N=30 en la batería grid).
- Caída de z con repetición (habituación grosera, d grande).
- C4a/b/c en dirección correcta: restaurar W recupera z; congelar impide habituar; no-entrenado no distingue.
- C3 negativo: generaliza al vector opuesto. Es el resultado más científico del repo porque no se ocultó.
- Cuarteto (recuperación 0.48 / savings 1.9) como *señal*, no como demostración Rankin completa.

Herido:

- C1/C2/C4 reportados como “blindaje” pero son **piloto 1 semilla**. Un reviewer los degrada a “anecdota replicable”.
- z=132 (piloto) vs z=20.6 (batería) sin protocolo de baseline congelada. La métrica no está anclada.
- EWC-λ inerte en misma tarea: el relato “memoria EWC” no tiene dial causal.
- Φ: calibración r≈0.70 es real; d=−1.61 causal está confundido con la gate (panel 61/62).

Muerto como evidencia de las hipótesis originales:

- Batería H4 toy T1–T3 (sigmoide inyectada; ablación Bernoulli hardcodeada; PCI = string aleatorio).
- Kael 100% vs 0% (dict vs FIFO).
- BFS 32-0 como test de H2.
- FPR 0.00032 y Butlin 10/14.
- “24 h de vida” como test de H1.

## Lo que A exigiría antes de cualquier cifra nueva

1. **Congelar la métrica de z** antes de correr: μ, σ estimados en una fase de calibración *sin eventos*, luego congelados. Prohibido actualizar σ durante el evento.
2. **N=30 también para C1, C2, C4a/b/c.** Sin eso no entran a Tabla 1.
3. **Brazo Φ-shuffled** (misma gate, entrada de Φ permutada) y **gate-random no acoplada a Φ**. Si d se mantiene, el claim metacognitivo muere.
4. **Rankin mínimo de 4 caracteres**, no de 1: (i) decremento, (ii) recuperación espontánea, (iii) savings, (iv) especificidad *o* deshabituación verdadera con estímulo de otra clase. C3 ya dijo que la especificidad vectorial murió; hay que testear clase motora vs interoceptiva con métrica de ε crudo, no z reciclado.
5. Interferencia EWC con **tarea distinta** (p. ej. habituar teleport, interferir con inversión E-al-comer). Si λ sigue plana, EWC sale del abstract.

## Hoja de A (semanas 1–3) — “hacer cierto lo pequeño”

| ID | Acción | Esfuerzo | Mata el claim si… |
|---|---|---|---|
| A1 | Protocolo de z congelado + script único `habituation_battery.py` que corre C1–C4 + Rankin-4, N=30 | 2–3 días | El z de detección cae bajo un umbral pre-registrado (p. ej. CI inferior < 5) |
| A2 | C1/C2/C4 a N=30 | 1 día cómputo | C1 o C2 dejan de mostrar razón ≥3× |
| A3 | 4-arm Φ: acoplado / desacoplado / Φ-shuffle / gate-random | 1 día | Los 4 brazos no se separan; o shuffle ≈ acoplado |
| A4 | EWC-λ en tarea distinta | 1 día | λ no modula savings ni recuperación |
| A5 | Retirar H4 toy, Kael toy y BFS toy de cualquier tabla, README y abstract | 2 h | (no es experimento; es higiene) |

Producto de A: **una tabla y un JSON**. Nada de “organismo consciente”. Título tentativo del claim: *habituation as weight-space model update, without stimulus specificity*.

---

# AGENTE B — Arquitectura y cierre teoría–código

**Eje:** ¿el software instancia las cajas del doc `02`, o solo les pone nombre?
**Lente:** world models, continua learning, agentes homeostáticos. Navaja: una pieza nueva solo si mide algo que A necesita.
**Criterio de éxito:** un extraño lee `organismo_*.py` y puede dibujar el diagrama *real* sin abrir los markdowns.

## Diagnóstico

Hay deuda arquitectónica aguda.

El diagrama canónico promete: V-JEPA, GWT 64D, AST/VQ-VAE, Mamba L1, episodios Titans, LoRA+EWC+SWR, Φ hiper-generativo, codec W:R^d→LLM.

El loop que produce números es: `estado 6-D → MLP → ε → z → reglas ECUS → a ∈ {0..5} → opcional LLM(prompt ya escrito)`.

Eso no es un prototipo del tetraedro. Es otro sistema. Mientras convivan, todo documento “H1 🟢” es falso por categoría.

Decisiones de B (no negociables en v0.14):

1. **Congelar el organismo mínimo como especificación.** Un archivo `SPEC.md` de ≤2 páginas: entradas, redes, pérdidas, qué *no* hay. El código es la especificación; los docs `02`/`13` pasan a “motivación”.
2. **Un solo mundo.** Grid *o* continuo. Mezclarlos en una tabla es incomparable. B recomienda **congelar grid** para la batería de A (teleport bien definido) y dejar el continuo solo para el run largo de humo.
3. **Un solo organismo ejecutable.** Hoy hay `organismo_completo.py`, `organismo_final.py`, `process_vivo_minutos.py`, `m4_local_*`, `m5_*`. Eso impide saber qué sistema produjo cada JSON.
4. **LLM fuera del núcleo hasta que haya codec de verdad.** La boca actual no es W:R^d→tokens. Es plantilla. Mantenerla como *demo opcional*, nunca como evidencia H2b.
5. **No introducir V-JEPA, MiniGrid-PPO, Mamba ni GWT en las próximas 8 semanas.** Cada uno es un proyecto. Abrirlos ahora reproduce el patrón v0.6: hipótesis nueva, experimento no hecho.

Qué sí conviene construir (solo si A lo necesita):

- Predictor **factorizado** (posición vs interocepción vs “salto”) para atacar C3: si el canal de salto se habitúa y el de posición no, el negativo se vuelve mecanismo.
- Cabezal Φ **por canal** (log-varianza, no MSE escalar), porque el Φ actual puede ser “clasificador de x>14”.
- SVD / norma de ΔW para documentar que la traza es de rango bajo (el paper ya lo sospecha).
- Quitar paths absolutos y el acoplamiento MLX del script principal.

## Hoja de B (semanas 1–4, en paralelo a A)

| ID | Acción | Esfuerzo | Mata el claim si… |
|---|---|---|---|
| B1 | `SPEC.md` + diagrama del sistema *real* (MLP, shapes, pérdidas) | 4 h | — |
| B2 | Unificar batería en un paquete `framework/core/` (mundo, predictor, Φ, z, EWC) usado por todos los scripts de A | 2–3 días | Scripts viejos siguen produciendo números divergentes |
| B3 | Predictor factorizado + log de ΔW (norma, rango estimado) | 1–2 días | El factor “salto” no existe (todo el error vive en un canal mezclado) y C3 no se puede reinterpretar |
| B4 | Φ por canal + probe “¿predice x>14 mejor que predice ε?” | 1 día | Accuracy de “estoy en niebla” ≈ r(Φ,ε): entonces Φ es detector de zona, no self-model |
| B5 | Higiene: path relativo, `requirements-min.txt` (numpy, torch), seed CLI | 3 h | Un clone fresco no regenera JSON |

Producto de B: **un núcleo único** del que A extrae números. Sin esto, A solo multiplica scripts huérfanos.

---

# AGENTE C — Posicionamiento, publicación y programa

**Eje:** qué cara pública tiene el proyecto y qué programa de 8 semanas no lo vuelve a inflar.
**Lente:** editor de taller (ALIFE / IWAI / CogSci late-breaking) + gestión de un investigador independiente.
**Criterio de éxito:** un extraño entiende en 90 segundos *qué se midió* y *qué no se afirma*. El README no contradice el paper.

## Diagnóstico

El riesgo principal no es técnico. Es **reputacional**.

El repo se llama Conciencia Artificial. El README abre con la tesis de conciencia y lista “resultados blindados”. El paper `56` y el panel `61` ya recortaron eso. Quien clone GitHub cree la versión inflada. Quien lea el paper cree la versión recortada. Esa divergencia es exactamente lo que un reviewer usa para desconfiar del pre-registro.

C no discute si la tesis filosófica es interesante (lo es). Discute si debe ser el *producto* de los próximos dos meses (no).

Posicionamiento correcto (v0.14):

- **Campo:** habituación y update de modelo en un agente mínimo encarnado; incertidumbre aprendida.
- **No-campo:** conciencia fenoménica, GWT, PCI, Butlin, “organismo vivo”.
- **Título de trabajo:** el de CITATION ya es mejor que el del README. Usarlo en GitHub.
- **Tesis LLM=boca:** pasa a *principio de diseño* y Future Work. No es resultado.

Publicación realista:

| Vía | ¿Cuándo? | ¿Con qué manuscrito? |
|---|---|---|
| Zenodo v0.14 | Al cerrar A1–A4 | Record de datos + código + changelog que *retira* claims de v0.12 |
| arXiv cs.AI o cs.LG | Misma semana | Paper corto (4–6 pp) al estilo `56`, no manifiesto |
| Taller ALIFE / IWAI / CogSci LB | Si A3 no mata Φ *o* si se publica solo habituación | Un claim, no seis |
| Revista | No en 8 semanas | — |

Qué no hacer (lista de C, explícita):

- No abrir el repo a “conciencia colectiva”, TEPT, derechos legales, V-JEPA 1B.
- No escribir otro ejecutivo “el organismo vive”.
- No simular paneles de 4 campos como si fueran peer review externo.
- No depositar v0.13 en Zenodo con la interpretación pre-panel.

Comunicación interna del programa:

- Un board de 6 claims máximo, cada uno con estado {pre-reg, corriendo, sobrevive, muerto}.
- Cada dos semanas: o se mata un claim o se cierra un experimento. Prohibido añadir H7–H9.

## Hoja de C (semana 1 y semana 8)

| ID | Acción | Esfuerzo | Mata el programa si… |
|---|---|---|---|
| C1 | Reescribir README + INDEX a la especificación de B y a la tabla de A. Versión del repo = versión del paper | 4 h | — |
| C2 | Changelog de claims retirados (H4 5/5, Kael, BFS, FPR, awareness FUERTE, anti-incertidumbre, Φ detecta niebla) | 2 h | — |
| C3 | Decisión de nombre público: mantener repo y aclarar en la primera línea, *o* añadir un subtitle “habituation / minimal agent” | 30 min | — |
| C4 | Paper 4–6 pp solo con lo que sobreviva A1–A4 | 3–4 días al final | A2 o C3 de A fallan y no queda un claim positivo + un negativo |
| C5 | Zenodo nuevo (concepto ya existe) con tag v0.14 y “supersedes v0.12 interpretation” | 2 h | — |

Producto de C: **una cara**. Si C1 no se hace en la semana 1, A y B trabajarán otra vez contra un frente inflado.

---

# Síntesis — hoja de ruta única (8 semanas, 1 persona)

Los tres agentes convergen en el mismo orden. No es el plan v0.13 de evolucionar H* ni ecología de 2 agentes. Esas líneas se aplazan hasta que la traza paramétrica y Φ tengan controles que un reviewer no destruya en diez minutos.

```
Semana 1     C1 C2 C3 + B1 B5     higiene pública + SPEC real
Semana 1–2   B2                  núcleo único
Semana 2–3   A1 A2 A5            batería N=30 + funeral de toys
Semana 3     A3 B4               4-arm Φ + probe de zona
Semana 4     A4 B3               EWC tarea distinta + predictor factorizado
Semana 5     buffer / fallos     repetir solo lo que haya muerto por bug, no por hipótesis
Semana 6–7   C4                  paper corto
Semana 8     C5                  Zenodo v0.14 + freeze
```

Carga realista: ~6–10 h/día equivaldrían a sobrecarga; el plan cabe en **~8–12 h/semana** si se resiste la tentación de abrir módulos nuevos. Si solo hay 4 h/semana, cortar B3 y el paper; hacer C1 + A1 + A2.

## Board de claims (máximo 6)

| Claim | Estado hoy | Dueño | Criterio de supervivencia |
|---|---|---|---|
| 1. Detección acción-condicionada | vivo, N insuficiente | A | C1 y C2 N=30, razón ≥3×, z congelado |
| 2. Habituación grosera en W | vivo | A | C4a/b/c N=30 + recuperación/savings |
| 3. Especificidad fina al vector | muerto (C3) | A | no resucitar; reemplazar por especificidad de *clase* o declarar límite |
| 4. EWC es el mecanismo de persistencia | herido | A+B | λ modula interferencia de tarea distinta |
| 5. Φ es self-model causal | herido / confundido | A+B | 4-arm; probe x>14 no explica r |
| 6. LLM es boca demostrada | no testeado (tautológico) | C | fuera de v0.14 |

Todo lo demás (GWT, PCI, Butlin, Kael, Coconut, 24 h, evolución anti-incertidumbre, acoplamiento de 2 agentes) queda en **archivo teórico**, no en el board.

## Qué se entrega el día 56

1. README alineado.
2. `framework/core/` + `habituation_battery.py`.
3. `results/battery_v014.json` con C1–C4 N=30 y 4-arm.
4. Paper 4–6 páginas, un positivo, un negativo, un límite de Φ.
5. Zenodo v0.14 que retira interpretaciones de v0.12.

Si el día 56 no existen (1) y (3), el programa fracasó aunque existan 20 markdowns nuevos.

## Anti-patrón que los tres prohíben

Añadir un doc `65-hipotesis-H7-...` o un script `ecologia_*` antes de C1+A2. El cuello de botella no es falta de ideas. Es falta de un sistema y una tabla que coincidan.

---

*Fin del panel. Siguiente acción concreta si se acepta: C1 (README) el mismo día, no un documento 65.*
