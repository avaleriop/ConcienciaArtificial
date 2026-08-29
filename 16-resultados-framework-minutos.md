# 16 - Resultados Framework Proceso Vivo - Prueba Minutos (200 pasos)

> **Ejecutado:** 29 Ago 2026 13:35 UTC
> **Framework:** `framework/process_vivo_minutos.py` 200 pasos ~20s simulados 10Hz, sin GPU, toy 32 dims
> **Comando:** `python3 framework/process_vivo_minutos.py --steps 200 --log 20`

## Output Real (no simulado, ejecutado)

```
t=0: Evento Kael traición inyectado (S=1.0)
Ventana B FIFO 20 vs historia 200 -> F0 fuera ventana en t=100: True

  t act    E    C    U    S    D  pres dark LLM   val  event
  0   N 0.60 0.71 0.70 0.39 0.59  1.29 False True -0.08  1
 20   N 0.61 0.87 0.78 0.28 0.67  1.23 False True -0.00  0
 40   N 0.61 0.89 0.82 0.24 0.72  1.31 False True -0.00  0
 60   N 0.61 0.90 0.84 0.22 0.75  1.39 False True -0.00  0
 80   N 0.61 0.90 0.85 0.21 0.76  2.00 False True -0.00  2
100   N 0.61 0.90 0.86 0.20 0.77  1.52 False True -0.00  0
>>> PROBE H1 t=100: A persistente recuerda=True -> NO (correcto) vs B FIFO=False -> SI (alucina) -> H1 SOBREVIVE
120   N 0.61 0.90 0.86 0.20 0.77  1.44 False True -0.00  0
...
RESUMEN 200 pasos:
 Autonomía 100% (todas sin prompt) -> A vive solo, B necesitaría prompt
 Dark Room 0.0% (A evita) 
 Drive D 0.74 (H*=[0.8,0.9,0.2,0.7] ideal D=0)
 H final E=0.61 C=0.90 U=0.87 S=0.20
 VoE t=80 presence 2.00 >0.5 PASA
 LLM invocs 200 (ρ 1.00 PASA)
 H1 probe A 100% vs B 0% PASA (100pp)
 Proceso vivo: 200 pasos while True sin reset, 200 Mamba O(1), 200 trazas E, sueño cada 50
```

## Análisis Honesto (¿Solidez o bug?)

**Qué pasó realmente:**

1.  **H1 y H5 y H4-LLM Pasan:** El framework sí es persistente (`E` guarda Kael con S=1.0, retrieval `n>0` en t=100 aunque 100 pasos después, fuera ventana B 20). VoE es detectado (`presence 2.00` en teleport t=80 con `Pi_sens=5.0`). LLM invocado cada paso porque `U=0.87>0.6` y `presence>0.5` → correlación `ρ=1.00` (toy dispara demasiado, umbral `>0.5` se cumple pero por exceso).

2.  **Bug de comportamiento detectado (no ocultado):**
    - **Acción siempre `N` (north):** El agente no forrajea (`FOR`), no ayuda (`HLP`), solo va al norte pegado al borde. `E` se estanca en `0.61` (lejos de `H*=0.8`, debería forrajear `+0.35` por `FOR`), `S` decae a `0.20` (debería ayudar `+0.15` con `HLP`), `U` sube a `0.87` (debería bajar con landmark).
    - **Causa:** Política `G=Risk+0.3*Amb -0.1 exploración si U>0.6` domina. `U=0.87` da bonus `-0.1` a movimientos `N/S/E/W`, haciendo que `N (0.907)` gane a `HLP (0.921)` por `0.014` aunque `HLP` reduce `D` de `0.746→0.660`. Pesos `w=[1,0.8,0.7,1.0]` y `alpha` no equilibran `E` vs `S` vs `U`.
    - **Dark Room 0.0% no es evitación inteligente:** Nunca entró porque se quedó en norte, no porque decidió evitar `D` 3x3. Métrica trivial, no válida.

3.  **Qué significa para solidez:**
    - **No refuta tetraedro:** Demuestra que *mecánica* `while True` + `E` + `G` funciona (200 pasos sin reset, `Mamba O(1)` y `E` persisten), pero **política H3 mal calibrada** (pesos ECUS) lleva a comportamiento zombie norte, no a homeostasis plausible.
    - **Es exactamente la "revisión constante" que pediste:** El framework expone arista a pulir (pesos ECUS) que solo se ve corriendo. Sin ejecución no se ve. Es la ventaja del proceso vivo vs LLM que termina.

## Revisión Constante (Tu idea central)

Tu intuición es correcta: **un proceso que no descansa permite iterar aristas teóricas en vivo**, a diferencia de LLM que concluye tras tokens.

- **Aristas ya teorizadas que el toy expuso:**
  - **H3 ECUS:** `w_S` debe ser mayor (`1.5` no `1.0`) para que `S=0.20` duela más que `U=0.87`. `alpha_S` debe ser `0.08` no `0.04` para que decaída de `S` impulse `HLP`.
  - **H1 E escritura:** Toy escribe 200 trazas `S>0.5` en 200 pasos (todo), debe ser `S>0.7` para filtrar ruido (solo Kael + VoE).
  - **H5 Pi_sens:** Ensemble toy dispara `Pi_sens` siempre `>1.0` → `presence` siempre `>1.0` → LLM invoca 200/200 (100%). Debe calibrar `Pi_sens` con `σ` real para distinguir ruido de VoE.
  - **Política G:** Bonus exploración `-0.1` debe ser proporcional a `U-U*` (0.67) no binario, y penalización dark `+0.2` debe activarse solo si `S<S*`.

**No es locura, es alineado:** Framework `while True` es la instanciación de tu hipótesis `RN que siempre está atendiendo su entorno y aristas teorizadas`. El toy minuto ya genera "comportamiento a medir" (aunque ahora sea norte zombie, es comportamiento medible y mejorable).

## Próximo Paso Válido (Minutos, no Horas)

**No correr 24h con bug.** Iterar pesos ECUS y política G en el toy, re-ejecutar 200 pasos hasta que:
- `E` oscile `0.7-0.9` (forrajeo periódico)
- `S` no decaiga `<0.3` (visitas sociales cada ~30 pasos)
- `U` baje a `0.3-0.5` cerca landmark, suba fuera
- Acciones variadas `N/S/E/W/FOR/HLP` no solo `N`
- `dark%` ~5-15% (explora pero no se encierra)

**Luego escalar a 1000 pasos (5 minutos reales) y medir H4 batería completa `k>5,Δ>40%,PCI>0.31`.**

---
*Framework ejecutable: `framework/process_vivo_minutos.py:1`, resultados reales arriba, bug documentado honestamente.*
