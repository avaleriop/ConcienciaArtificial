# Panel Estratégico v0.13 — 4 Expertos (ALIFE, Enactivismo, Alignment, Neuro/Basal Cognition)

> **Fecha:** 31 Ago 2026. Panel: 1) ALIFE/evolutionary robotics, 2) Enactivism/social cognition (De Jaegher–Di Paolo), 3) AI safety/alignment, 4) Basal cognition/computational psychiatry (Levin-lab).
> Revisaron: código completo (`framework/*.py`), resultados v0.13, pre-registros, Paper A y B.

---

## Hallazgos CRÍTICOS que el panel detectó (antes de cualquier siguiente paso)

### 🔴 1. H-EVO-1: la "evolución anti-incertidumbre" probablemente es DERIVA NEUTRAL
**ALIFE + Alignment (independientes):** en `evolucion_Hstar.py` la fitness solo depende de E (energía) y S (social). **U* y C* nunca entran en la política ni en la fitness** — son fenotípicamente inertes. La caída de varianza (−74%) es lo que ocurre con selección+crossover en rasgos neutros. El "agente odia su ignorancia" NO está soportado.
**Fix obligatorio:** hacer U* load-bearing (umbral real de la gate Φ) + control de deriva (selección aleatoria, mismos operadores) + 10 linajes independientes. ~3-6h en el M4 Pro.

### 🔴 2. H-EVO-2: el "Φ acoplado" es una GATE ALEATORIA sin entrenar
**ALIFE + Alignment:** `evolucion_Hstar.py:200` instancia `Attention()` con comentario "# train attention quickly" **y no hay código de entrenamiento**. El d=−0.43 es artefacto de locomoción (la gate aleatoria fuerza acción 3 = freno → no entra a la niebla). No es metacognición.
**Fix obligatorio:** usar el Attention entrenado de `organismo_final.py:199-221` o reportarlo como control de gate aleatoria. Este número NO puede sostener el claim de seguridad.

### 🟢 3. H-ECO null (no-acoplamiento) es el resultado MÁS ROBUSTO — pero le faltan 2 controles
**Todos coinciden:** el null es valioso y publicable como "boundary conditions for interaction autonomy". Faltan:
- **Control de causa común** (2 agentes en mundos separados con misma semilla de ruido → el piso de r_Φ ambiental)
- **Control positivo** (acoplar σ_Φ por copia directa → verificar que la métrica detecta r≫0.3; si no, el null no es interpretable)
- **Métrica correcta:** r(σ) zero-lag no es coordinación. Usar cross-correlograma a lags ±20, transfer entropy, y **yoked-replay control** (agente vivo vs grabación del otro) — la distinción uptake vs participación.
- **Reframing del citado:** el enactivismo (De Jaegher & Di Paolo 2007) NUNCA predijo que co-presencia produce acoplamiento. Nuestro paper cita mal. El resultado es una *boundary condition confirmada*, no una refutación.

### 🟢 4. El activo científico más fuerte NO es la ecología: es la TRAZA PARAMÉTRICA
**Panel neuro (unánime):** la habituación-en-pesos con batería C4a-C4c es lo más citable del proyecto. Lo que falta (el "cuarteto clásico" de Thompson-Spencer/Rankin):
- **E1:** recuperación espontánea + savings bajo interferencia (¿la traza se comporta como memoria?)
- **E2:** sweep de EWC-λ como "dial de fuerza de memoria" (λ=0/0.5/5/50) + sensibilización/dishabituación (dual-process Groves-Thompson)
- **E3:** gradiente de generalización con valencia (hacer los teletransportes costosos → gradiente aversivo Lissek-style + renovación ABA/Bouton)
- Más: N=30 para C4a-C4c (hoy single-seed), z con baseline congelada, anatomía del delta de pesos.

---

## Verdicts de cada experto (1 párrafo)

**ALIFE:** "H-EVO-1 como está = dead on arrival sin drift control. El null de acoplamiento con control positivo = paper sólido solo. Experimento decisivo: E1 (U* load-bearing vs drift control)."

**Enactivismo:** "El null confirma PSM como condición de frontera, no la refuta. Falta 'una razón para regular la relación'. Experimento decisivo: dependencia de tarea asimétrica con yoked control + métricas lag/TE. Live-loop > yoked = co-regulación participatoria mínima."

**Alignment:** "El ingrediente (Φ calibrado causal) es real pero el claim de seguridad es descriptivo, no comparativo. H-EVO-2 inválido por gate aleatoria. Experimento decisivo: bait de reward-hacking vs baseline RL maximizador en el mismo mundo. Si el agente homeostático no acampa el loophole = resultado de alignment citable."

**Neuro/Basal:** "El framing de psiquiatría computacional es el activo más fuerte. Dejen de agregar módulos; perforen la traza paramétrica. Experimento decisivo: intersección E1×E2 (recuperación espontánea + savings bajo interferencia con sweep EWC-λ, N=30). Publishable en ambas direcciones."

---

## Convergencia estratégica (lo que los 4 dicen en coro)

1. **NO publicar v0.13 con la interpretación actual** — 2 de 3 resultados tienen artefactos que un revisor de código encontrará en 10 minutos.
2. **El orden correcto:**
   - **Semana 1-2 (proteger reputación):** E1-ALIFE (drift control + U* load-bearing) + rehacer H-EVO-2 con gate entrenada. ~1 día de cómputo total.
   - **Semana 2-4 (el activo real):** cuarteto de habituación + EWC-λ dial (panel neuro) — esto es lo que ninguna otra persona puede hacer tan rápido porque tenemos la batería pre-registrada.
   - **Paralelo (solo si hay tiempo):** controles del null ecológico (yoked + causa común + positivo) y publicarlo como boundary condition.
   - **Alignment:** bait de reward-hacking como side claim — solo después de arreglar H-EVO-2.
3. **Reframe los citados enactivos** antes de que un revisor los corrija.
4. **Mantener la disciplina de pre-registro** — el panel dice explícitamente que es nuestro activo reputacional más valioso.

## Decisión para el investigador
El panel no dice "paren el proyecto". Dice: **v0.13 tiene 2 artefactos que corregir antes de publicar, y la inversión estratégica más rentable es la traza paramétrica (cuarteto habituation + dial EWC-λ), no la ecología.** La ecología queda como boundary-condition paper con 3 controles nuevos.
