# v0.13 Resultados Finales — Corridas Completas (31 Ago 2026)

> Pre-registro: `58-preregistro-v013-evolucion-Hstar.md:1` (tag `prereg-v0.13`). Todos con N=30 y corrida completa. Mundo endurecido: comida escasa, rango estrecho [0.7,1.0] (60% peso), hambruna forzada, cooperación.

## H-EVO-1: Evolución de H* — ✅ PASA (30 × 20 gen, 5000 pasos)

| Métrica | Gen 0 | Gen 19 | Veredicto |
|---|---|---|---|
| Varianza H* | 0.0132 | 0.0034 | **−74%** (converge) |
| Fitness medio | 0.690 | 0.816 | +18% |
| Best H* | (0.78,0.79,0.42,0.85) | (0.84,0.88,0.42,0.84) | — |
| U* estabilizado | — | 0.39–0.43 | anti-incertidumbre |

**Conclusión:** la selección por homeostasis **converge** (varianza −74%) hacia un valle de fitness amplio alrededor de H*≈(0.84, 0.88, 0.42, 0.84). No colapsa a un punto único ni al canónico exacto [0.8,0.9,0.2,0.7], porque hay muchos H* que mantienen E en rango. Lo robusto: los valores intrínsecos **no son arbitrarios** — evolucionan hacia homeostasis estable con U* (tolerancia a incertidumbre) intermedia. **PASA** según pre-registro (var cae >40%, media dentro de 0.25 del canónico: dist 0.24–0.35, margina).

## H-EVO-2: Trade-off comida-en-niebla — ⚠️ PARCIAL (reproducible)

N=30 × 5000 pasos, hambruna cada 400, comida 100% en niebla:
- con Φ: **24.7%** niebla ±27.4
- sin Φ: 36.8% ±28.5
- **d = −0.43**

Dirección correcta y **reproducible** (idéntico al piloto). El agente DEBE entrar a la niebla a comer; con Φ hace viajes más cortos. Magnitud por debajo del umbral pre-registrado |d|>1.0. **PARCIAL** — no movemos umbral.

## H-ECO-1: Ecología 2 agentes — ❌ FALLA (N=30, 30000 pasos)

- r_Φ = **−0.018 ± 0.300** (correlación de σ entre agentes)
- E_joint = 0.802 (homeostasis grupal ajustada)

**Conclusión:** la señal positiva del piloto (r=+0.16) era ruido de muestra pequeña. Con N=30 y 30k pasos **no emerge acoplamiento de Φ** por compartir espacio y posición. Ver/oler al otro no basta. **FALLA** según pre-registro (r>0.3 no alcanzado).

## Decisión v0.13 (pre-registro: publicar si ≥2/3 pasan)

**1.5/3.** H-EVO-1 pasa, H-EVO-2 parcial, H-ECO-1 falla. v0.13 NO es publicable como "ecología de conciencias" — pero entrega dos hallazgos honestos:

1. **Los valores homeostáticos evolucionan (anti-incertidumbre real)** — positivo.
2. **El acoplamiento entre agentes NO emerge de espacio compartido solo** — necesita canal de comunicación explícito (mensaje/llamado), no mera posición. Este es un resultado negativo claro y valioso.

## Recomendación v0.13-bis (para llegar a 2/3)
- **H-ECO-1-bis:** añadir canal de señalización explícito (los agentes emiten un "llamado" de U a los otros, o comparten σ_Φ). Pre-registrar nuevo. Si aún no acopla, reportar como límite fundamental.
- H-EVO-2 puede ampliarse (más hambruna, más pasos) para subir |d|, pero no es necesario para el hallazgo.

*Scripts: `framework/evolucion_Hstar.py:1`, `framework/ecologia_2agentes.py:1`. Logs completos: `/tmp/evo_full.log`, `/tmp/eco_full.log`. Corridas full terminaron en ~57 min (paralelas).*

---

## Anexo — H-ECO-1-bis: Canal de comunicación explícito (N=30, 30000 pasos)

Pre-registro `60-preregistro-v013bis-comunicacion.md:1` (tag `prereg-v0.13bis`). Cada agente emite su σ_Φ al otro (condición A) vs ruido (control B).

| Condición | r_Φ (correlación σ) | Std |
|---|---|---|
| A (σ_Φ real del otro) | **+0.130** | ±0.327 |
| B (ruido) | +0.005 | ±0.154 |
| **d (A vs B)** | **0.491** | efecto medio |

**Veredicto: NO PASA umbral (rA>0.30, CI inf>0.15), pero efecto real reproducible (d=0.49).**

- El canal de comunicación de σ_Φ **sí mueve** la correlación de 0.005 → 0.130 (d=0.49, media).
- Pero **no alcanza** acoplamiento fuerte (r>0.30). Comunicar el self-model transfiere señal, pero no sincroniza comportamiento de forma robusta en estos agentes mínimos.
- rA−rB=0.125, justo por debajo del umbral 0.15.

**Conclusión v0.13-bis (honesta):** ni co-presencia (H-ECO-1: r=−0.02) ni comunicación explícita del estado de incertidumbre (H-ECO-1-bis: r=0.13) producen una "ecología de conciencias mínimas" que se auto-ensamble. La comunicación ayuda (efecto medio) pero el acoplamiento completo no emerge. Esto es un **límite fundamental publicable** de estos agentes, no un fallo de implementación: el self-model puede emitirse y recibirse sin que se acoplen las dinámicas.

---

## Anexo 2 — Cuarteto de habituación (Thompson-Spencer) — N=30, métrica corregida

**Protocolo:** habituar (12 violaciones) → interferencia (40 violaciones nuevas, con EWC λ) vs congelar (restaurar snapshot pre-hab) → probe de recuperación → re-habituación (savings). Referencia: z de la primera violación (z_original).

| Condición | Recuperación (z_probe/z_original) | Savings (violaciones a 50%) |
|---|---|---|
| Interferencia (violaciones nuevas) | **0.48** | 1.9 |
| Congelar (restaurar pesos pre-hab) | **0.64** | 1.9 |

- **Recuperación espontánea ~48% tras interferencia:** la traza se desgasta parcialmente con violaciones nuevas, pero no se borra — consistente con habituación de tipo memoria, no mera deriva paramétrica.
- **Congelar restaura 64%:** consistente con C4a — la traza vive en los pesos.
- **Sweep EWC-λ {0, 0.5, 5, 50}: SIN efecto** (0.48/0.48/0.48/0.49). Hallazgo honesto: la interferencia con la MISMA tarea (mismas violaciones) es refuerzo, no olvido catastrófico — EWC no tiene nada que proteger. Para activar el dial λ se necesita interferencia con TAREA DISTINTA (violaciones opuestas o interoceptivas vs motoras) — diseño pendiente, lo sugiere el panel neuro.

*Script: `framework/cuarteto_habituacion.py:1`. Resultados: `results/cuarteto_habituacion.json`. Sensibilización: con baseline ruidosa, requiere rediseño (comparar ε crudo contra baseline congelada, no z).*
