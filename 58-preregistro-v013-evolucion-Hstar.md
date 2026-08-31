# Pre-registro v0.13 — Evolución de H* y Ecología Mínima de 2 Agentes
> **Fecha:** 31 Ago 2026 — **Estado:** BORRADOR pre-registro (no ejecutado)
> **Mundo base:** `framework/organismo_final.py` v0.12 (WORLD_SIZE 20.0, niebla x>14 ruido 0.60, MLP 13→64→6, Φ 15→64→1 / 22→64→1, EWC λ=5, 30k pasos)

## 1. Hipótesis

**H-EVO-1 (Convergencia de valores):** En una población de 30 agentes con H* muestreado uniformemente en [E 0.6–1.0, C 0.7–1.0, U 0.1–0.5, S 0.5–1.0], tras 20 generaciones de selección por homeostasis, los H* convergen a una región estable cerca de H*=[0.8,0.9,0.2,0.7] (±0.15). Métrica: varianza de H* cae >40% y media final distancia Euclídea a H* canónico <0.25.

**H-EVO-2 (Trade-off forrajeo-claridad):** Con comida *dentro* de la niebla (x>14), los agentes con Φ acoplado sacrifican forrajeo para evitar niebla: tiempo en niebla con Φ 15%± vs sin Φ 35%+, diferencia E final <0.2 (no mueren por evitar). N=30, d<-1.0 esperado.

**H-ECO-1 (Acoplamiento de 2 agentes):** Dos organismos en el mismo mundo continuo, con percepción mutua de posición, muestran correlación de σ_Φ entre agentes >0.3 o homeostasis grupal distinta de la suma de dos solos. Indica acoplamiento mínimo.

## 2. Diseño

**Mundo:** continuo 20.0, niebla x>14 (0.60), 4 comidas, 1 social. Para H-EVO-2, comidas en (16,3),(16,16) dentro de niebla.

**Población H-EVO:** N=30 agentes, cada agente 5k pasos. Fitness = 0.7*frac_tiempo_en_rango([0.5,1.2] para E) + 0.3*(1 - pasos_por_comida/5000). Selección torneo k=3, elitismo 2, mutación gaussiana σ=0.05 con clip al hipercubo, 20 generaciones. Semilla base 7, variación por agente.

**2-agentes:** mismo mundo, 2 agentes con H* canónico, 30k pasos joint, 30 seeds. Posición del otro concatenada como 2 dims extra a entrada (o como canal visual). Métrica: correlación Pearson de σ_Φ(t) entre agentes en ventana 100, y E medio grupal vs E de 2 corridas solitarias.

**Kit Φ portable:** validar phi_score() en 2 tamaños de predictor (64 y 64→64) — r>0.5 debe replicar.

## 3. Estadística pre-fijada

- N=30 en todos los experimentos de población/causal; 2-agentes N=30 seeds.
- Medias, 95% CI bootstrap 2000, Cohen's d pareado/no pareado.
- Pass/fail fijado arriba antes de ver datos. No se mueve umbral post hoc.
- Controles: sin Φ, sin atención, H* aleatorio.

## 4. Criterio de éxito y de parada

v0.13 se publica si **al menos 2 de 3** hipótesis pasan y la tercera se reporta como nula con interpretación. Si evolución no converge, se reporta como "no convergencia" — sigue siendo publicable como límite.

## 5. Archivos

- `framework/evolucion_Hstar.py` — población + selección
- `framework/ecologia_2agentes.py` — mundo joint
- `results/evolucion_Hstar.json`, `results/ecologia_2agentes.json`
- Este documento es el pre-registro; se sella antes de ejecutar (commit + tag `prereg-v0.13`).
