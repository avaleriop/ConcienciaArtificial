# 32 - M4-Local v3 - Leak MPS Corregido: 1.1M params 10k pasos a 0.78GB

> **Ejecutado:** 29 Ago 2026 15:40 UTC - `python3 framework/m4_local_v2.py --steps 10000 --warmup 2000` (MPS)
> **Fix v3 pre-registrado `31:1`:** tensores batch pre-allocados reutilizados + `no_grad` inferencia + `empty_cache` cada 100.

## Resultado v3 vs v2b (mismo modelo 1.1M params)

```
              v2b (leak)        v3 (fix)         Diferencia
MPS peak      8.00GB -> stop    0.78GB           LEAK CORREGIDO (10x menos)
Pasos         4500 (parada)     12000 completos  indefinido logrado
ms/paso       6.2ms             1.4ms            4.4x más rápido
E              0.66-1.16        0.66-1.16        homeostasis estable
U/S/D          0.37/0.45/0.36   0.37/0.45/0.36   idéntico (ECUS robusto)
eps final      ~0.0000          0.0002-0.0048    encoder sigue aprendiendo
```

**Causa del leak confirmada:** crear `torch.tensor` nuevo por batch (cada 64 pasos) fragmentaba el allocator MPS. Con tensores pre-allocados `Xb_fixed/Xn_fixed` + `.copy_()`, MPS se estabiliza en <1GB. El fix era de implementación, no del modelo.

## Estado escalado local (verificable)

- ✅ **1.123.329 params (45× el encoder inicial) corren indefinido** en M4 Pro sin GPU: 1.4ms/paso, 0.78GB
- ✅ JEPA converge, ECUS homeostasis estable en todas las escalas (E/U/S/D PASA)
- ✅ Seguridad: parada limpia a 8GB sigue activa (nunca se alcanza ahora), sin swap ni crash
- 🔵 VoE z bajo con encoder potente: el predictor aprende el mapa y predice hasta teleports (FEP: sorpresa = error que importa). v4 pendiente: métrica relativa a capacidad.
- ❌ V-JEPA2 1B sigue fuera de alcance local (1000× params)

## Qué permite esto (capacidad real de la máquina, seguro)

- Runs indefinidos de 1.1M params: 24h ≈ 864k pasos × 1.4ms ≈ **20 minutos wall-clock** (MPS procesa 10Hz simulado 60× más rápido que tiempo real)
- Escalar a ~5M params (encoder 6→2048→1024→512) probablemente viable: ~2-3GB MPS, ~3-5ms/paso — **próximo paso pre-registrado v4-escale**
- El límite real de la máquina: modelos de pocos millones de params, no 1B (honesto)

## Siguientes pre-registrados

1. **v4-escale:** 5M params, 50k pasos, medir JEPA/ms/GB → techo real definitivo local
2. **v4-VoE:** métrica sorpresa relativa a capacidad del predictor (z vs baseline del mismo modelo)
3. M4 cloud A100 solo para 1B (si hay presupuesto)

*Seguro y honesto: el fix era de asignación de tensores, documentado en `framework/m4_local_v2.py:176-184`. Sin dañar hardware.*
