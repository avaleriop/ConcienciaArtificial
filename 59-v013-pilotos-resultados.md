# v0.13 Pilotos — Resultados Honestos (Lite)

> **Pre-registro:** `58-preregistro-v013-evolucion-Hstar.md:1` — tag `prereg-v0.13`
> **Ejecutado:** 31 Ago 2026 — MacBook Pro M4 Pro, sin GPU

## H-EVO-1: Evolución de H* (20 → 8 gen lite, pop 20, 1500 pasos)

```
gen 00: dist_canon 0.140 var 0.0125 mean_f 0.803
gen 07: dist_canon 0.253 var 0.0117 mean_f 0.897
```

**Resultado:** No converge. Varianza no cae (0.0125 → 0.0117), distancia al canónico no disminuye (0.14 → 0.25). Fitness ya saturado en gen 0 (0.80–0.94, frac 0.96–0.98) para casi cualquier H*.

**Interpretación honesta:** En este mundo (grid continuo, comida fuera de niebla, 1500 pasos), cualquier H* dentro de los bounds mantiene E en rango. No hay presión selectiva para H*=[0.8,0.9,0.2,0.7]. Esto no refuta la homeostasis; dice que el task es demasiado fácil para evolucionar valores. Para selección real se necesita κόστος mayor (menos comida, perturbaciones, costo metabólico por desviación).

**Guardado:** `results/evolucion_Hstar.json`

## H-EVO-2: Trade-off comida-en-niebla

```
conPhi: niebla 0.0% ±0.0
sinPhi: niebla 0.0% ±0.0
d = 0.00
```

**Resultado:** Nulo. FOODS_FOG aún tiene comida fuera de niebla (10,3/10,16), el agente nunca necesita entrar. La acción epistémica no se pone a prueba.

**Implicación:** El mundo de trade-off debe tener **toda** la comida dentro de la niebla (x>14). Nueva corrida requerida para H-EVO-2.

## H-ECO-1: Ecología 2 agentes (N=8, 5000 pasos)

```
r_phi_mean = -0.033 ±0.214  (correlación σ_Φ entre agentes)
E_joint = 1.033
```

**Resultado:** Sin acoplamiento. r≈0, dentro de ruido. E_joint alto por el fix de comida (<0.5 radio, +0.2 por paso).

**Interpretación:** Con 2 agentes y atención no entrenada para el otro, no emerge acoplamiento de Φ. Se necesita canal de comunicación explícito (posición del otro como input ya está, pero sin entrenamiento para usarlo) o tarea cooperativa que obligue a coordinar.

## Qué sigue (ajuste v0.13)
1. Endurecer H-EVO: menos comida, costo por |H-H*|, o perturbaciones periódicas.
2. Rehacer H-EVO-2 con comida 100% en niebla.
3. Para ecología: tarea cooperativa (ej. llevar comida al otro) o fine-tuning de Φ joint.
4. Estos pilotos son negativos y se reportan — cumplen el pre-registro.

*Ver `framework/evolucion_Hstar.py:1` y `framework/ecologia_2agentes.py:1`. Resultados lite, no corrida completa 30×20 gen (estimada ~22h en esta laptop).*
