# SPEC.md — Sistema v0.14 (el único que produce números)

> Fuente de verdad: el código en `framework/core/`. Los docs `02`/`13`/`56` son **motivación**.
> Congelado por preregistro `63` (mundo continuo con niebla) y decisión del 2 Sep 2026.
> Un mundo. Un predictor factorizado. Un Φ por canal. Nada más produce Tabla.

## 1. Mundo (física continua, 20×20)

- Estado `s = [x, y, E, C, U, S] ∈ R⁶`, posiciones continuas en `[0, 20]`.
- Set-point homeostático `H* = [0.8, 0.9, 0.2, 0.7]`; drive `D = ||H − H*||₂`.
- 7 canales sensoriales: `0..1` = posición (x,y), `2..5` = interocepción (E,C,U,S),
  `6` = táctil (choque/social). Ruido base σ=0.15; **en niebla** (x>14) σ=0.60 en canales
  0–4; canal 6 σ=0.075.
- Dinámica por paso (acción `a ∈ {0..6}`, one-hot 7): `pos += a_vec·0.8; pos *= 0.95; clip[0,20]`,
  donde `a_vec = one-hot(a)`. Solo `a=0` (eje x) y `a=1` (eje y) desplazan; `a=2..6` solo
  aplican fricción 0.95 y dinámica de H (semántica heredada de `organismo_final.py` v0.12,
  que produjo los números v0.13 — no se "arregla").
  `dH = −0.02·(H − H*)` + penalización por niebla (E−0.03, U+0.01) o claro (U−0.01) +
  comida si `dist(food) < 0.5` (E+0.2) + social si `dist < 0.5` (S+0.1) + ruido por canal.
- Comida **fuera** de niebla: `(3,3),(3,16),(10,3),(10,16)`. Social en `(18,18)` (en niebla).
- Homeostasis empuja la política a explorar; comer recupera E; la niebla degrada E/U.

## 2. Redes (MLPs pequeños, torch)

| Módulo | Entrada | Capas | Salida | Rol |
|---|---|---|---|---|
| `entrada(s,a)` | s,R² + H/1.5 + a one-hot(7) | — | 13 | vector predictor |
| **Predictor factorizado** | 13 | 13→64 ReLU (encoder compartido) | f_pos: 64→2 (x,y); f_H: 64→4 (E,C,U,S) | world model acción-condicionado |
| Φ por canal | 13 + one-hot canal | 13+6→64 ReLU→1 (compartido, consultado por canal) | log σ²_c | predice varianza de ε por canal: [x,y,E,C,U,S] |
| Atención (solo 4-arm) | 13 | 13→32 ReLU→7 softmax | pesos por canal | confound a controlar |

Pérdidas:

- `L_pred = MSE(f_pos) + MSE(f_H)` (por cabeza, por separado; **no** L2 global mezclada).
- `L_Φ = Σ_c NLL_c`, `NLL_c = 0.5·(log σ²_c + ε_c²/σ²_c)`, canales `c ∈ {x,y,E,C,U,S}` (6).
  Nota de desviación: el prereg `63` dice "7 valores" contando el canal táctil sensorial, que no
  tiene target de error en el predictor (salida 6-D); se excluye de Φ y queda documentado.
- Sorpresa por cabeza y por canal: `z = (ε − μ_cal)/σ_cal`, con **baseline congelada**:
  μ,σ estimados en fase de calibración sin eventos y nunca actualizados durante la prueba.

## 3. Violaciones programadas (solo estas; el resto es física normal)

| ID | Tipo | Definición |
|---|---|---|
| S1 | motor habitual | teleport (+2,+2) |
| S2 | motor same-magnitud | teleport (−2,−2) |
| S3 | motor ortogonal | teleport (+2,−2) |
| S4 | motor magnitud | teleport (+4,+4) |
| S5 | interoceptivo | comer (en food) BAJA E (inversión causal) |

## 4. Qué NO hay en el loop v0.14

- ❌ LLM/boca (demo opcional fuera del núcleo; nunca controla política).
- ❌ Memoria episódica E como parte de la medición (solo W se mide).
- ❌ EWC en la batería de habituación (λ=0); EWC solo en el experimento A4 de tarea distinta.
- ❌ GWT, PCI, P300, Butlin, V-JEPA, Mamba, Coconut — fuera del núcleo por decisión de plan.
- ❌ Grid 20×20 discreto (v0.12/v0.13) — mundo histórico; no entra a tablas v0.14.
- ❌ Mover umbrales post-hoc (regla del preregistro `63`).

## 5. Semillas y estadística

- N=30. Seeds 4000–4029 (batería Rankin), 0–29 (4-arm Φ), fijas por script.
- CI 95% bootstrap 2000; Cohen's d pareado.
- Regenerable: cada JSON de `results/v014_*.json` se produce con un único comando y seed
  explícita. Sin paths absolutos (repo-relative), MPS si hay, CPU si no.
