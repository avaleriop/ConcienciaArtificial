# v0.13 Pilotos Endurecidos — Resultados (31 Ago 2026)

> Pre-registro: `58-preregistro-v013-evolucion-Hstar.md:1` (tag `prereg-v0.13`)
> Endurecimiento: comida escasa (2/2 fuera de niebla), recompensa comida 0.12, fitness con rango estrecho [0.7,1.0] (60%), hambruna forzada cada 400 pasos (tradeoff), recompensa social + compartir comida (ecología).

## H-EVO-1: Evolución de H* — CONVERGE ✅ (lite 20×8 gen, 1500 pasos)

| Métrica | Gen 0 | Gen 7 | Cambio |
|---|---|---|---|
| Varianza H* | 0.0125 | 0.0025 | **−80%** |
| Distancia canónico | 0.287 | 0.199 | −31% |
| Fitness medio | 0.669 | 0.784 | +17% |
| Best H* | (0.78, 0.79, 0.42, 0.85) | (0.81, 0.76, **0.10**, 0.80) | — |

**Hallazgo clave:** la selección converge — y converge a **U*=0.10** (el mínimo del rango [0.1,0.5]). En este mundo, el valor intrínseco que evoluciona más fuerte es *odiar la incertidumbre*. E* se estabiliza ~0.81. El canónico exacto [0.8,0.9,0.2,0.7] no es único óptimo — hay un valle de fitness alrededor de él, y U* mínimo domina. Es un resultado interpretable: entre agentes que compiten por homeostasis, sobrevive el que menos tolera su propia ignorancia.

## H-EVO-2: Trade-off comida-en-niebla — DIRECCIÓN CORRECTA, magnitud bajo umbral ⚠️

Hambruna forzada cada 400 pasos (E→0.3), comida 100% en niebla, N=30 seeds × 5000 pasos:

| Condición | Tiempo en niebla | Std |
|---|---|---|
| con Φ acoplado | **24.7%** | ±27.4 |
| sin Φ | 36.8% | ±28.5 |

**d = −0.43** (pre-registrado: |d|>1.0). Dirección correcta (Φ reduce exposición 12 puntos), magnitud bajo umbral. El agente DEBE entrar a la niebla para comer (toda la comida está ahí), y con Φ hace viajes más cortos. Con más pasos o más hambruna el efecto debería ampliarse. Reportado como **parcial** — no movemos el umbral.

## H-ECO-1: Ecología 2 agentes con cooperación — SEÑAL DÉBIL ⚠️

N=8 seeds × 5000 pasos (pre-registrado r>0.3):

| Métrica | Antes (sin coop) | Ahora (con coop) |
|---|---|---|
| r_Φ (correlación σ) | −0.033 ±0.214 | **+0.163 ±0.424** |
| E_joint | 1.033 | 0.811 |

Dirección positiva y homeostasis más ajustada (0.811 vs 1.033), pero varianza entre seeds es enorme (r de −0.36 a +0.80). Con N=8 no alcanza significancia. Requiere N=30 y más pasos (la tarea cooperativa necesita tiempo para emerger).

## Estado y siguiente paso

- **1 de 3 pasó completo (H-EVO-1)** — primer resultado positivo de v0.13: los valores homeostáticos evolucionan y seleccionan anti-incertidumbre.
- **2 de 3 parciales** con dirección correcta — requieren más corrida (N=30, más pasos).
- Próximo: corrida completa 30×20 generaciones (~2.5h) + N=30 ecología (30k pasos) para decidir pass/fail según pre-registro.

*Scripts: `framework/evolucion_Hstar.py:1` (endurecido, hambruna línea tradeoff), `framework/ecologia_2agentes.py:1` (cooperación dist<2 S+, compartir comida dist<3 E+).*
