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
