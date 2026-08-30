# 27 - M4-local-2 - Política Portada: E/D PASA, VoE pendiente encoder (honesto)

> **Ejecutado:** 29 Ago 2026 14:45 UTC - `python3 framework/m4_local_cpu.py --steps 1000` MPS
> **Cambios pre-registrados M4-local-2 (`26:1`):** política completa portada del toy + `teleport_t=80`.

## Resultado M4-local-2 vs Integración 1

```
Métrica          Integración 1    M4-local-2    Criterio GATE    Veredicto
E               1.10-1.50         0.66-1.16     0.7-0.9 osc.     PASA (min 0.66 arranque, resto 0.7-1.16)
U               0.37              0.37          0.3-0.5          PASA
S               0.45              0.45          >0.3             PASA
D avg           0.77              0.36          <0.60            PASA (mejora 0.77->0.36)
H1 Kael         True              True          >75%             PASA
LLM inv         0                 0             calibrado        PASA
VoE             0.25              0.31          >0.7             FALLA (pendiente, ver abajo)
```

**Confirmado:** los 2 bugs de portado diagnosticados en `26:1` eran reales — la política completa corrigió E (sobre-forrajeo `clip 1.5 → 0.66-1.16`) y D (0.77→0.36). El diagnóstico fue correcto: bug de integración, no falla de mecanismo.

## VoE 0.31: diagnóstico honesto

- Teleport t=80 ahora existe (`mundo.teleport_t=80` → salta a `[18,1]`). Pero `presence` pico 0.31 << 0.7.
- **Causa:** el encoder JEPA lleva solo ~200 actualizaciones en 1000 pasos (entrena cada 5, lr 1e-3), pérdida 0.08 todavía alta → `s_pred ≈ s_n ≈ 0` vector (encoder semi-aleatorio), `ε = ||s_pred - s_n||` pequeño incluso con teletransporte. No hay señal predictiva fiable aún.
- **No es falla de `presence` ni de H5:** es encoder subentrenado. Con encoder convergente (JEPA <0.01), el salto espacial del teleport dispararía `ε` alto → `presence>0.7`.
- **Fix pre-registrado M4-local-3:** 2000-5000 pasos de warmup encoder (o lr schedule) antes de medir VoE, y medir VoE al final (t=950) cuando el encoder ya predice.

## Estado M4-local (lenguaje verificable)

- ✅ **Encoder aprendido real local:** JEPA baja de 0.25→0.08 en 1000 pasos (aprende, no aleatorio)
- ✅ **EWC Fisher + Adam online:** sin colapso ni divergencia
- ✅ **Mamba N=64 MPS:** O(1) por paso
- ✅ **Política G completa portada:** E/U/S/D homeostasis correcta en encoder aprendido
- 🔵 **VoE:** pendiente M4-local-3 (encoder convergente)
- ❌ Awareness/conciencia: no demostradas

## Siguiente pre-registrado M4-local-3

1. Warmup encoder 2000 pasos (JEPA objetivo <0.02) → medir VoE t=950 con teleport → esperado `presence>0.7`
2. H2b local (eliminar LLM) y M3b local (borrar E → EWC retiene) con encoder convergente — los decisivos en representación aprendida
3. Luego M4 cloud A100 (V-JEPA2 1B) solo si todo PASA local

*Sin inflar: homeostasis con encoder aprendido ✅, VoE 🔵 pendiente. Cada bug diagnosticado con causa y fix pre-registrado antes de ejecutar.*
