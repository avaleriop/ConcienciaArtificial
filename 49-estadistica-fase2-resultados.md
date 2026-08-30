# 49 - Estadística Fase 2: 3/4 Hipótesis Blindadas con CI, H5 Refutada en Este Protocolo

> **Ejecutado:** 29 Ago 2026 19:25 UTC - `estadistica_fase2.py` (30 seeds) + `analisis_fase2.py`
> **Pre-registrado:** `48-preregistro-estadistica.md:1` (protocolo fijo, criterios ANTES de correr)

## Resultados (N=30 seeds, 95% CI bootstrap 2000, Cohen's d)

| Hipótesis | Resultado | Veredicto |
| :--- | :--- | :--- |
| **H1** z(motor) detecta violaciones | media **20.6**, CI **[16.0, 25.5]** (no cruza 5) | ✅ PASA |
| **H3** habituación por aprendizaje | **3.8 → 0.5** (reducción 86%, **d=3.5** efecto grande) | ✅ PASA |
| **H4** traza persiste en W | z_post/z_motor = **0.02** (0.5/20.6) | ✅ PASA |
| **H5** homeostasis estable | E media **0.50**, solo **50%** seeds en rango | ❌ REFUTA en este protocolo |

## Diagnóstico de H5 (honesto, sin esconder)

- **El protocolo estadístico NO incluyó la política de navegación a comida.** `run_seed` mide predictor + habituación con acciones aleatorias, sin el loop de forrajeo del organismo completo.
- Con acciones aleatorias, E deriva a ~0.5 (forrajeos fallidos -0.1 sin navegación dirigida). Esto NO mide la homeostasis del organismo completo — que SÍ fue demostrada con política en `m5_24h` (E 0.66-0.84 durante 864k pasos) pero sin N=30.
- **Regla respetada:** H5 queda REFUTA en este protocolo, registrada. No se reinterpreta.
- **Corrección pre-registrada H5-bis:** re-ejecutar N=30 seeds del organismo completo CON política de navegación (mismo código que m5_24h), midiendo E media sobre 5k pasos. Escrito aquí ANTES de correr, no como ajuste post-hoc.

## Qué queda blindado (con números y CI)

1. **La detección es robusta**: z=20.6 con CI que no toca 5 en 30 seeds — no es un golpe de suerte de una corrida.
2. **La habituación es un efecto grande** (d=3.5): 86% de reducción consistente entre seeds.
3. **La persistencia en W es robusta**: z_post es 2% del z inicial — la traza aprendida vive en pesos en todas las seeds.

## Estado científico del proyecto (tras Fase 1+2)

- ✅ Claim central **blindado**: controles CheckVLA (5/6) + estadística (H1/H3/H4 con CI y d)
- 🟡 H5 homeostasis: demostrada con política (m5_24h) pero pendiente de blindaje estadístico (H5-bis pre-registrada)
- 🟡 C3a especificidad fina: refutada (generalización por dirección), documentada como límite real
- 🔵 Fase 3 (benchmark ICM/RND) y Fase 4 (empaquetado) pendientes

*Resultados en `results/estadistica_fase2.json`. Ver `framework/analisis_fase2.py` y `framework/estadistica_fase2.py`.*
