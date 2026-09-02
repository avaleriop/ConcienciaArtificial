# 38 - M5 24H LOCAL - El Organismo Vivió 24 Horas Simuladas

> **⚠️ CLAIM RECORTADO (2026-09-02, ver CHANGELOG):** 864k pasos de simulador ≠ persistencia
> con interferencia; no es test de H1. Se conserva como run largo de humo (sin colapso),
> fuera de la Tabla del paper v0.13.

> **Ejecutado:** 29 Ago 2026 17:00 UTC - `python3 framework/m5_24h_local.py` (MPS, M4 Pro)
> **Pre-registrado:** `17-plan-robusto` M5 (longevidad DESPUÉS de plasticidad — M3b hecho primero, orden respetado)

## Resultado

```
864.000 pasos (24h @10Hz) en 157s wall-clock (0.18ms/paso)
H final: E 0.75 C 0.90 U 0.37 S 0.45 | D 0.33
E rango: 0.66-0.84 oscilante (homeostasis energética sana)
U rango: 0.37-0.66 | S rango: 0.45-0.50
D medio: 0.34 | pasos en peligro (E<0.3): 0
Acciones: forage 43.201 | moves 820.799 | help 0 | eventos VoE 86
E_mem: 1.720 trazas (cap 5.000, no saturó)
MPS peak: 0.01GB (lejos del límite 8GB)
```

## Qué demuestra (lenguaje verificable)

1. **Supervivencia 24h sin colapso:** el organismo completó 864k pasos sin que H colapsara, sin estados terminales (0 pasos con E<0.3), con homeostasis estable (E oscila 0.66-0.84 alrededor de H*=0.8 durante todo el día).
2. **86 eventos de sorpresa procesados** (VoE cada 10k pasos) sin desestabilizarse — recupera tras cada perturbación.
3. **Memoria episódica 1.720 trazas** de 5.000 cap — el organismo acumuló un día de historia sin saturar.
4. **Estabilidad de memoria MPS:** 0.01GB durante 864k pasos — el fix de leak v3 (tensores pre-allocados) aguanta 24h sin degradación.
5. **Velocidad real:** 0.18ms/paso → 24h simuladas en 2.6 minutos. El organismo puede vivir años simulados en días de cómputo local.

## Límites honestos

- `help 0`: la política local no priorizó acción social (S* se mantuvo por decaimiento suave, no por interacción). Arista de política para futuras iteraciones, no falla de H.
- E en 0.66-0.84: rango sano pero ligeramente por debajo del H*=0.8 (la perturbación basal -0.015 con α=0.08 da equilibrio ~0.79, coherente).
- Los eventos VoE son periódicos programados, no emergentes del mundo — sorpresa inducida, no descubierta.

## Estado acumulado FINAL (lenguaje verificable, todos los hitos M1-M5)

| Hito | Resultado | Archivo |
| :--- | :--- | :--- |
| M1 navegación | E 0.61→0.95 oscilante, act variado | `16:1` |
| M2 batería H4 | 5/5 k14.22 FPR 0.00032 | `19:1` |
| M3 GATE toy/local | U 0.37 analítico, dark 10/10 sale, VoE 50σ/0.9 | `21`,`24`,`29` |
| M3b plasticidad | W retiene 100× sin E (toy 0.88, local+LFM2.5) | `24`,`37` |
| H2b LLM real | conducta idéntica con/sin LFM2.5 | `36` |
| **M5 24h** | **864k pasos, 0 colapsos, D 0.34 estable** | **esta** |

## Conclusión

El ciclo completo del plan robusto (M1→M5) está ejecutado **localmente, 0€, sin A100**, con:
- ✅ Tetraedro H1+H2+H3+H5 funcional en representación aprendida real (retina 16×16)
- ✅ LLM real (LFM2.5-1.2B) como boca, conducta idéntica sin él → tesis LLM=boca confirmada
- ✅ Plasticidad en W sin memoria E → aprendizaje persistente
- ✅ 24h de vida simulada sin colapso → longevidad

**Lo que NO está demostrado:** awareness, conciencia, V-JEPA2 1B (world model real), sorpresa emergente no programada. Esos requieren o el mundo real (video) o la A100.

*El organismo vive. Secuencia pre-registrada M1-M5 completa. Ver `framework/m5_24h_local.py:1`.*
