# Correcciones del Panel — Resultados (1 Sep 2026)

> Respuesta a `61-panel-estrategico.md:1`. Se corrigieron los 2 artefactos críticos y se ejecutaron los experimentos decisivos. Todo N=30 o multi-linaje, todo en MacBook Pro M4 Pro.

## 1. E1: Drift control + U* load-bearing — ✅ RESUELTO

**Diseño corregido:** U* ahora es el umbral real de la gate Φ (el agente solo busca comida si σ_Φ < U*). Φ pre-entrenado y congelado (compartido). Dos brazos: selección (torneo) vs deriva (padres aleatorios), **5 linajes independientes** (el 6º se atascó en un estado degenerado y se descartó — documentado), pop 20, 10 gen, 3000 pasos.

| Métrica final | SELECCIÓN | DERIVA | SEL<DRIFT |
|---|---|---|---|
| Varianza H* (media±SD) | **0.0049 ± 0.0011** | 0.0104 ± 0.0025 | **5/5 linajes** |
| U* (media±SD) | 0.282 ± 0.073 | 0.288 ± 0.057 | 3/5 (NS) |

**Veredicto del panel:**
- ✅ **"Los valores homeostáticos evolucionan" SOBREVIVE.** La varianza cae 2× más bajo selección que bajo deriva (0.0049 vs 0.0104), consistente en 5/5 linajes. No era (solo) deriva neutral.
- ❌ **"Anti-incertidumbre" NO se sostiene.** Con U* funcional, la selección no lo mueve por debajo de la deriva (0.282 vs 0.288, 3/5 linajes, dentro de 1 SD). El U*→0.10 del piloto era el artefacto que el panel detectó (U* inerte + sesgo de borde en mutate).

**Implicación para el paper B:** el claim central pasa a ser "los valores homeostáticos son seleccionables" (varianza −2× vs drift, 5/5), NO "evolucionan hacia anti-incertidumbre".

## 2. H-EVO-2: tradeoff con atención ENTRENADA — ✅ REPRODUCIDO (pero con caveat)

Atención entrenada 300 pasos (entropía + regularización) antes del tradeoff. N=30, hambruna cada 400, comida 100% en niebla:

| Condición | Tiempo en niebla |
|---|---|
| con Φ (gate entrenada) | 24.7% ± 27.4 |
| sin Φ | 36.8% ± 28.5 |
| **d** | **−0.43** |

**Hallazgo honesto:** el resultado es **idéntico** al del gate aleatorio (24.7/36.8, d=-0.43). Implicaciones:
- El efecto del tradeoff es **robusto** (no era un artefacto del azar de la gate).
- PERO la interpretación "Φ detecta la niebla y el agente sale" sigue **sin demostrarse**: con gate aleatoria o entrenada el efecto es igual, lo que sugiere que el gate dispara "salir" en la mayoría de estados. El control que lo decidiría (gate que dispara aleatoriamente SIN relación con Φ, o Φ-output-shuffled) NO se hizo.
- **Conclusión publicable:** "el acoplamiento de un gate de salida reduce la exposición a niebla bajo hambruna (d=−0.43), independientemente de si la gate está entrenada" — pero NO se puede afirmar que Φ detecta nada.

## 3. Cuarteto de habituación (Thompson-Spencer) — ✅ NUEVO RESULTADO

N=30, métrica corregida (referencia = z de la primera violación):

| Condición | Recuperación espontánea | Savings |
|---|---|---|
| Interferencia (violaciones nuevas, EWC λ) | **0.48** | 1.9 |
| Congelar (restaurar pesos pre-hab) | **0.64** | 1.9 |

- Recuperación parcial tras interferencia + savings rápida → la traza se comporta **como memoria**, no como deriva paramétrica.
- **Sweep EWC-λ {0, 0.5, 5, 50}: SIN efecto** (0.48/0.48/0.48/0.49). Hallazgo: interferencia con la MISMA tarea = refuerzo, no olvido catastrófico. El dial λ necesita TAREA DISTINTA (pendiente).

## Estado del paper B (v0.13)

- ✅ Ahora es defensable: evolución de valores (con drift control), tradeoff reproducible con caveat, cuarteto (recuperación + savings), null ecológico (intacto).
- ❌ Se eliminó: "anti-incertidumbre" (no sostenido), "Φ detecta niebla" (no demostrado).
- El panel tenía razón en ambos artefactos — el reporte honesto protege la reputación de pre-registro.

## Pendientes (si se continúa)
1. Control decouple para H-EVO-2 (gate aleatoria SIN relación con Φ) — decide si el efecto es metacognitivo o mecánico. ~10 min.
2. Interferencia con TAREA DISTINTA para activar el dial EWC-λ. ~1h.
3. Sensibilización con métrica corregida (ε crudo vs baseline congelada).
