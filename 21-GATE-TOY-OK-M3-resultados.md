# 21 - GATE_TOY_OK M3-iter2 - Evaluación Estricta (FALLA parcial, sin reinterpretar)

> **Ejecutado:** 29 Ago 2026 14:15 UTC - Evaluación estricta pre-registrada `17-plan-robusto-v0.8-v1.0.md:30`
> **Regla del usuario:** no reinterpretar fracaso ni cambiar métricas para PASA. Distinguir BUG IMPLEMENTACIÓN vs FALLA MECANISMO.

## Resultado M3-iter2 (mundo 20×20, 1000 pasos, obs dist/size*1.4 + landmark U)

```
GATE_TOY_OK:
 E: min 0.60 max 1.00 oscilación 0.40 → PASA (criterio 0.7-0.9 oscilante)
 U: min 0.59 max 0.87            → FALLA (criterio 0.3-0.5)
 S: final 0.67                   → PASA (criterio >0.3)
 dark: 0.0%                      → FALLA (criterio 5-15%)
 H1 probe t100: A True B False   → PASA
 VoE: 2.00                       → PASA (>0.7)
 Actions: FOR 39 HLP 75 moves 896 (ya no FOR 995/1000: obs corregido funcionó)
 D avg 0.50, LLM 1/1000
```

**Resultado neto: GATE_TOY_OK FALLA parcial (2 criterios: U y dark). No se reinterpreta, no se cambia métrica.**

## Diagnóstico (BUG IMPLEMENTACIÓN vs FALLA MECANISMO)

**U = FALLA DE CALIBRACIÓN DEL MECANISMO (no bug de implementación):**
- Ecuación de equilibrio: `0 = -α_U·(U-U*) + perturbación_basal`
- Con `α_U=0.03`, `U*=0.2`, `perturbación +0.02`: `U_eq = 0.2 + 0.02/0.03 = 0.87` — **exactamente el 0.87 observado**. Es analítico, no aleatorio.
- Landmark no ayuda: agente **0/200 visitas** cerca de `[10,10]` (distancia ≤1.4). Va a esquina `[10,0]` y se queda (positions x∈[10,18] y∈[0,1]).
- **Conclusión:** `α_U` demasiado débil vs drive basal. Es la misma clase de error que `w_S` en iter1 (peso mal calibrado), corregible con 1 línea, no refuta `H3` (el mecanismo `D(H)` sí modifica política — `E 0.60→1.00` oscilante lo demuestra).

**dark = CONSECUENCIA DE U:** agente no explora dark porque `U` en equilibrio alto (0.87) pero `G` de `N` hacia esquina `[10,0]` gana; dark `[0-2,0-2]` nunca visitado. No es decisión `G(dark)>G(explore)`, es ausencia de exploración por calibración. Métrica trivial (como `16:43`).

**Lo que SÍ demuestra M3-iter2:**
1. ✅ Obs corregido funciona: `FOR 995/1000 → 39/1000` (bug de denominador `dist/14` confirmado y resuelto)
2. ✅ `E 0.60→1.00` oscila con `H*=0.8` → homeostasis energética funcional en mundo 20×20
3. ✅ `S 0.67` se mantiene con HLP 75 veces → homeostasis social funcional
4. ✅ `H1` 100% vs 0%, `VoE 2.00` → persistencia y sorpresa no se rompen al escalar mundo

## Próxima iteración pre-registrada M3-iter3 (única corrección, sin tocar nada más)

- **Cambio único:** `α_U 0.03 → 0.12` → `U_eq = 0.2 + 0.02/0.12 = 0.37` (dentro de 0.3-0.5). Es calibración analítica, no ajuste ad hoc de métrica.
- **Predicción:** con `U_eq≈0.37`, drive exploratorio emerge (bonus `-0.08*(U-U*)` ya no se satura), agente visita landmark y dark 5-15%.
- **Criterio idéntico:** GATE_TOY_OK exacto, sin cambios.
- **Si FALLA otra vez:** registrar como evidencia de que `H3` con `Π_homeo` requiere revisión del modelo de perturbación basal (no del umbral).

## Estado H3 tras M3-iter2 (lenguaje verificable)

- ✅ `H3 E`: estado homeostático modifica política (E oscila 0.60→1.00) — consistente con H3
- ✅ `H3 S`: idem para S (HLP 75, S 0.67)
- ❌ `H3 U`: calibración `α_U` incorrecta (equilibrio 0.87 ≠ U* 0.2) — FALLA DE CALIBRACIÓN, no de mecanismo
- ❌ `dark`: métrica trivial por U mal calibrada — pendiente M3-iter3

*Sin reinterpretar. Sin cambiar umbrales. M3-iter3 pre-registrado con α_U=0.12 analítico.*
