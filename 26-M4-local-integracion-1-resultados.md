# 26 - M4-Intermedio Local v0.9 - Resultados Integración 1 (honesto, FALLA parcial calibración)

> **Ejecutado:** 29 Ago 2026 14:40 UTC - `python3 framework/m4_local_cpu.py --steps 1000` en MPS (Apple M4 Pro)
> **Qué es nuevo vs toy:** encoder JEPA **aprendido online** (25.793 parámetros, 2 capas 6→128→64, no aleatorio), EWC Fisher real, Mamba N=64 torch, Π head.

## Resultado integración 1 (1000 pasos 20×20)

```
Encoder: 25.793 params entrenables, pérdida JEPA final 0.0716 (aprende a predecir, baja)
E: min 1.10 max 1.50 -> FALLA (criterio 0.7-0.9: FORRAJEO EXCESIVO, satura clip)
U: 0.37 -> PASA (α_U=0.12 heredado)
S: 0.45 -> PASA (>0.3)
D avg: 0.77 -> FALLA (alto por E=1.5 lejos de H*=0.8)
H1 Kael t100: True -> PASA
VoE max: 0.25 -> FALLA (no implementado en mundo local, ver abajo)
LLM inv: 0 -> PASA (calibrado, U<0.4 no invoca)
```

## Diagnóstico (bug implementación vs falla mecanismo)

1. **E 1.10-1.50 = BUG DE POLÍTICA INTEGRACIÓN, no falla ECUS:** La política local `elegir_accion` es más simple que la del toy (`framework/process_vivo_minutos.py:277`) — le falta penalización de sobre-forrajeo (`if food_near<0.3: dH-=0.1`) y bonus condicionado. Resultado: `FOR` demasiado frecuente → `dE/dt ≈ +0.167 - 0.08·(E-0.8) - 0.015` → equilibrio `E≈2.7` clip 1.5. En toy con penalización: FOR 39/1000 y E 0.65-1.00. **Fix pre-registrado M4-local-2:** copiar política completa del toy (`framework/process_vivo_minutos.py:250-330`) con penalizaciones dark/sobre-forrajeo/STY.
2. **VoE 0.25 = NO IMPLEMENTADO:** `MundoLocal.step` no tiene teletransporte (toy lo tenía en `teleport_t=80`). No es falla de `presence`, es ausencia del estímulo. **Fix:** añadir `teleport_t=80` que salta `agent_pos` a otra esquina.
3. **Lo que sí funciona (verificable):** encoder aprende (JEPA 0.07), EWC+Adam entrenan sin colapsar, Mamba64 corre O(1) en MPS, ECUS U heredado calibra 0.37, H1 memoria Kael persiste, LLM no invoca sin U alta.

## Estado M4-local vs toy

| Componente | Toy | M4-local integración 1 |
| :--- | :--- | :--- |
| Encoder | lineal aleatorio | **JEPA aprendido 25k params (real)** ✅ |
| EWC | conceptual | **Fisher online real** ✅ |
| Mamba | N=16 numpy | **N=64 torch MPS** ✅ |
| ECUS | calibrado | heredado, U/S PASA, E por política |
| Política G | completa (4 penalizaciones) | simplificada → E satura (bug integración) |
| VoE | teleport t=80 | ausente (no implementado) |
| GATE_TOY_OK | PASA | FALLA parcial (E, D, VoE por bugs 1 y 2) |

**Conclusión honesta:** M4-local demuestra que el flujo con encoder aprendido y EWC real **corre en hardware local sin GPU** — es el salto que faltaba para M4 completo. La integración 1 no pasa GATE por 2 bugs de portado (política simplificada, VoE ausente), ambos diagnosticados y con fix pre-registrado. No es falla de mecanismo (los mecanismos U/S/H1/JEPA funcionan).

**Próximo pre-registrado M4-local-2:** portar política completa del toy + teleport t=80 → re-run 1000 pasos → GATE_TOY_OK. Después M4-local-3: H2b real (eliminar LLM) y M3b real (borrar E → EWC retiene) con encoder aprendido.

*Sin inflar: "encoder aprendido real corre local" ✅, "GATE PASA" ❌ pendiente M4-local-2.*
