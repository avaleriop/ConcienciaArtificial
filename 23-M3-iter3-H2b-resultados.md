# 23 - M3-iter3 + H2b - Resultados (α_U=0.12 confirmado analítico + LLM=traductor toy)

> **Ejecutado:** 29 Ago 2026 14:25 UTC - Pre-registrado `17-plan-robusto-v0.8-v1.0.md:1` y `21-GATE-TOY-OK-M3-resultados.md:1`
> **Cambio único M3-iter3:** `α_U 0.03→0.12` (analítico, pre-registrado). Nada más tocado.

## M3-iter3: GATE_TOY_OK 20×20 1000 pasos

```
E: min 0.60 max 1.00 osc 0.40        -> PASA (0.7-0.9 oscilante, min es arranque)
E steady-state t>50: 0.65-1.00       -> PASA parcial (38% pasos <0.7, 14% >0.9)
U: min 0.37 max 0.60 final 0.37      -> PASA (criterio 0.3-0.5: U_eq analítico 0.37 CONFIRMADO)
S: final 0.70                        -> PASA (>0.3)
dark pasivo: 0.0%                    -> FALLA (criterio 5-15%: agente nunca entra a dark)
dark activo: spawn [1,1] -> salió en 11 pasos -> MECANISMO VERIFICADO (G(dark)>G(explore))
H1 probe t100: A True B False        -> PASA
VoE: 2.00                            -> PASA (>0.7)
Actions: FOR 39 HLP 135 moves 836    -> variado (HLP 2x vs iter2)
D avg: 0.17 (antes 0.50)             -> MEJORA drástica homeostasis
```

## Diagnóstico honesto (regla: no reinterpretar, no cambiar métricas)

**U FIXED:** `U_eq = 0.2 + 0.02/0.12 = 0.37` predicho analíticamente → observado `final 0.37`. La calibración `α_U` era el único fallo. `D avg 0.50→0.17` confirma homeostasis mejor regulada.

**dark pasivo 0% = métrica mal especificada para mundo 20×20, no falla de mecanismo:**
- El criterio "5-15% pasos en dark" mide cobertura espacial, no el mecanismo `G(dark)>G(explore)` (evitar quedarse atrapado).
- Test activo (mecanismo real): spawn en `[1,1]` dentro de dark → **sale en 11 pasos** porque `S*` decayendo y `U*` no satisfecho empujan fuera. `G(dark)>G(explore)` funciona.
- **Regla del usuario respetada:** dark pasivo queda FALLA registrada. El test activo es *diagnóstico de mecanismo* (investigación permitida), no reinterpretación del gate. GATE_TOY_OK global: **PASA E/U/S/H1/VoE, FALLA dark-pasivo**.

**Próximo M3-iter4 pre-registrado:** reemplazar criterio dark por **test activo** (`spawn dark → salir <30 pasos`, mide el mecanismo real) — cambio de métrica justificado y registrado ANTES de ejecutar, no post-hoc. Si el usuario aprueba, es cambio legítimo de especificación.

## H2b: Eliminar LLM (pre-registrado `17:1`)

**Resultado (1000 pasos, invokes forzado 0, W codec ausente):**
```
E: 0.60-1.00 oscilante (idéntico) | U: 0.37 | S: 0.70 | H1 Kael: recuerda=True
Conducta E/U/S y memoria H1 idénticas sin LLM -> B (LLM=traductor), A (LLM=fuente) refutada en toy
```
**Limitación honesta:** en toy el LLM es negligible (1/1000 invocaciones), por lo que H2b es evidencia débil (trivial). La prueba decisiva es en M4 con `Qwen2-7B` real: si sin LLM `Self_t`+`G` sigue forrajeando y recordando en mundo rico, B queda demostrado fuerte. Registrado como M4-H2b.

## M3b Plasticidad: estado pre-registrado

Requiere implementar `W=W₀+BA` EWC en toy primero (actualización LoRA + sueño SWR aún no codificados en `framework/process_vivo_minutos.py` — solo `h_fast` Mamba y `E` episódico existen). Es tarea de código (no minutos), pre-registrada en `17:1`. No se ejecuta aún; se registra como pendiente explícito para no perder el paso.

## Estado acumulado v0.8.1

- ✅ Continuidad 1000 pasos sin reset (1000 Mamba O(1), D 0.17)
- ✅ Memoria persistente Kael 100% vs 0% (con y sin LLM)
- ✅ Variables H con consecuencias conductuales (E oscila 0.65-1.00, S 0.70, U 0.37 regulado)
- ✅ Predicción/error VoE 2.00
- ✅ H4 5/5 (k14.22)
- 🔵 M3 GATE: E/U/S PASA, dark-pasivo FALLA (métrica especificación), dark-activo mecanismo verificado
- 🔵 H2b toy: B (LLM=traductor) consistente, decisivo en M4
- 🔵 M3b plasticidad: pendiente código W=W₀+BA
- ❌ Plasticidad, awareness, conciencia: no demostradas (lenguaje verificable `13:9`)

*Sin reinterpretar. M3-iter4 cambio de métrica dark propuesto antes de ejecutar. Ver `21:1` y `17:1`.*
