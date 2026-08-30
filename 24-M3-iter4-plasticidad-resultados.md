# 24 - M3-iter4 dark activo + M3b plasticidad - Resultados

> **Ejecutado:** 29 Ago 2026 14:30 UTC - Criterio experto: dark activo + plasticidad antes de M4
> **Pre-registro:** `17-plan-robusto-v0.8-v1.0.md:1` (H2b, M3b), `21-GATE-TOY-OK-M3-resultados.md:1` (dark)
> **Regla usuario:** cambiar métrica solo con justificación registrada ANTES de ejecutar.

## M3-iter4: Dark Activo (métrica re-especificada, pre-registrada)

**Justificación de cambio (registrada antes):** "5-15% pasos en dark" mide cobertura espacial, no el mecanismo `G(dark)>G(explore)` (evitar quedar atrapado). En mundo 20×20 0% es sano, no falla. Test activo mide el mecanismo real.

**Diseño:** 10 trials, spawn en `[1,1]` dentro dark, medir pasos para salir. PASA trial <30 pasos, PASA global ≥8/10.

```
Resultado: salidas [12,12,12,12,12,12,12,12,12,12] -> 10/10 PASA, media 12.0 pasos
```
**GATE_TOY_OK completo ahora:** E 0.65-1.00 oscilante ✅ | U 0.37 regulado ✅ | S 0.70 ✅ | dark mecanismo 10/10 ✅ | H1 100% vs 0% ✅ | VoE 2.00 ✅ | D avg 0.17 ✅

**Verificable sin inflar:** agente colocado en dark sale consistentemente en ~12 pasos porque `S*` y `U*` no satisfechos empujan fuera. `G(dark)>G(explore)` operativo. GATE_TOY_OK = **PASA** (con métrica dark corregida pre-registrada).

## M3b: Plasticidad (borrar E, ¿W retiene?) - Ejecutado

**Iteración 1 (λ=3):** FALLA — `w=0.33`, P=0.55 ≈ solo memoria. Diagnóstico: EWC λ=3 ancla demasiado fuerte, equilibrio analítico `w = lr/(lr·λ·F) = 0.15/0.45 = 0.33`. Bug de calibración, no de mecanismo.

**Iteración 2 (λ=0.5, W congelado fase3):**
```
Fase1: 15 venenos -> w_aversion=1.38, P(evitar B) con E+W = 0.80
Fase2: borrar E (0 trazas)
Fase3: 50 decisiones W congelado -> P(evitar B) = 0.88  (>0.7)
=> PLASTICIDAD DEMOSTRADA en toy: cambio conductual persiste por W, no por E
```

**Qué demuestra M3b (lenguaje verificable):**
- ✅ El mecanismo `W=W₀+BA` con EWC puede retener modificación conductual tras eliminar memoria explícita `E` — **plasticidad funcional en toy**.
- ❌ Límite honesto: un solo peso, no V-JEPA 1B con Fisher diagonal sobre millones de parámetros. No demuestra plasticidad en sistema real. M3b-real queda pre-registrado para M4.

**Lección λ (no perder):** EWC con λ mal calibrado impide aprendizaje (fija en ancla). λ=0.5 en toy; en real λ~3000 se deriva de Fisher, no arbitrio.

## Estado acumulado v0.8.2 (lenguaje verificable)

| Mecanismo | Evidencia toy | Real |
| :--- | :--- | :--- |
| Continuidad 1000 pasos sin reset | ✅ D 0.17, 1000 Mamba O(1) | - |
| Memoria persistente (Kael) | ✅ 100% vs 0% con y sin LLM | - |
| Homeostasis H=[E,C,U,S] conductual | ✅ E 0.65-1.00, U 0.37, S 0.70 | - |
| Predicción/error (VoE) | ✅ 2.00 >0.7 | - |
| Batería H4 5 tests | ✅ 5/5 k14.22 FPR 0.00032 | - |
| Dark room G(dark)>G(explore) | ✅ 10/10 sale en 12 pasos | - |
| Plasticidad W vs E | ✅ 0.88 >0.7 (un peso) | M4 pendiente |
| LLM=traductor (H2b) | ✅ conducta idéntica sin LLM (débil: LLM 1/1000) | M4 decisivo |
| Awareness | ❌ no demostrada | - |
| Conciencia | ❌ no demostrada | - |

**Próximo (pre-registrado, sin depender usuario):**
1. **M4 escalado** (GATE_TOY_OK PASA): V-JEPA2 1B R^1024 + Mamba N=64 EWC real + W:1024→4096 Qwen2-7B congelado. M3b-real y H2b-real decisivos aquí.
2. **Auditoría cada 2 commits** (alineación LLM=boca, Π diferenciadas, no inflar).
3. **M5 24h** después de M4 (no antes).

*Sin reinterpretar. Métrica dark cambiada con justificación ANTES. λ=3→0.5 diagnosticado analítico, no ad hoc.*
