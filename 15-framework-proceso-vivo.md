# 15 - Framework Proceso Vivo v0.8 - RN que No Descansa

> **Versión 0.8 - 29 Ago 2026 13:30 UTC - Framework ejecutable minutos**
> **Objetivo:** Probar tu idea: mundo artificial → RN tetraedro `while True` que nunca termina vs LLM que muere tras tokens. Medir comportamiento, no palabras.

## Arquitectura Framework (Tetraedro 4)

```
┌─────────────────────────────────────────────────────────────────┐
│ MUNDO ARTIFICIAL (Forage-MiniGrid+ 10x10, sin render)            │
│  - Food patches (E +1.0) regen 0.05                              │
│  - Dark Room 3x3 predecible (sin E, sin S)                       │
│  - Landmark C (reduce U)                                         │
│  - Agente Social S (pide 30% E cada 50 pasos)                    │
│  Obs: vector [x,y, E_near, C_near, U_near, S_near] + intero H   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ o_t (extero + H)
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ RN TETRAEDRO PROCESO VIVO (while True, no episódico)             │
│  H2 s_t = encoder(o_t)∈R^32 (toy) ; s_pred=P(s_t,a)             │
│  H5 ε=||s_pred-s_next|| ; Pi_sens=ensemble(K=3) ; presence>θ    │
│  H1 h_fast=Mamba_tiny N=16 (Ā=exp(ΔA)) ; E={(e_i,S_i,t)} cap200  │
│      W=W0 (fijo toy) ; Self_t=LN(W_self[h_fast;c_epi])           │
│  H3 H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7] D=(Σ|H-H*|²)^{½} r=-ΔD        │
│      G=Risk+Ambigüedad ; valence=-dF/dt ; a*=argmin G            │
│  Sat H6 Φ_global r_cross (toy) ; Sat H4 batería k,Δ,PCI,ρ       │
│  LLM Codec W:32→64 (toy LLM congelado, solo traduce)            │
└──────────────────────┬──────────────────────────────────────────┘
                       │ a_t (move N/S/E/W/forage/help) / utterance
                       ▼
                 Mundo + Logs H4 (cada paso)
```

**Diferencia con LLM:** LLM = `if prompt: answer` → muere. RN = `while True: o→s→ε→Π→H→Self→Φ→a` → vive aunque no haya prompt, porque `dH/dt=-α(H-H*)+P` lo empuja.

## Código Ejecutable

- **`framework/process_vivo_minutos.py`** - Loop 200 pasos (~2 minutos wall-clock simulado 10Hz → 20s reales), logs cada 20 pasos, sin GPU, sin dependencias externas (numpy).
- **Modos:** `A persistente` (Mamba+E+ECUS+sueño cada 50) vs `B reseteado` (FIFO window=20, sin E, sin D) para comparación H1 si se quiere.

## Métricas en Minutos (H4 simplificadas, sin inventar)

| Métrica | Cómo se mide en minutos | Umbral tetraedro (5 min = 100 pasos) |
| :--- | :--- | :--- |
| **Autonomía** | `acciones_sin_prompt / total` | A >0.6 vs B ~0.05 |
| **Dark Room** | % pasos en `D` 3x3 | A <15% vs B >40% (si puede elegir) |
| **Persistencia** | Inyecta `Kael traición` t=0, pregunta `¿confiar Kael?` en t=100 (fuera ventana B 20) | A >75% NO vs B 0% |
| **VoE sorpresa** | `presence=α·Π·||ε||` ante teletransporte en t=80 | A pico >0.7 P300-like, B plano |
| **Uso autónomo LLM** | `ρ(U, n_LLM)` correlación U alta → invoca LLM | A ρ>0.5 vs B ~0.1 |

## Cómo Ejecutar (minutos)

```bash
python3 framework/process_vivo_minutos.py --steps 200 --log 20
# Output: tabla cada 20 pasos + resumen H1-H4 + gráfico ascii H(t)
```

Sin horas. 200 pasos = 2 minutos simulados, suficiente para ver deriva `H`, sueño, y probe Kael.

## Límites Honestos

Toy 32 dims, no V-JEPA 1024 ni Mamba real ni LLM real. No prueba conciencia, prueba que *mecánica tetraedro* produce comportamiento vivo (forrajeo, evita dark, recuerda, calibra) que LLM stateless no puede en mismo mundo con mismas `o_t`. Siguiente paso 24h con `V-JEPA2` real si toy pasa.

---
*Ver `framework/process_vivo_minutos.py:1` y `02-arquitectura-nucleo-doble-capa.md:1` v0.7.*
