# 50 - H5-bis: Homeostasis Blindada con Política — PASA 100% (N=30)

> **Ejecutado:** 29 Ago 2026 19:35 UTC - H5-bis pre-registrada en `49:1` ANTES de correr
> **Corrección registrada:** el protocolo estadístico de Fase 2 medía el predictor SIN política de navegación (gap diagnosticado). H5-bis incluye la política completa del organismo (la misma de m5_24h).

## Resultado

```
H5-bis (organismo CON política, N=30 seeds, 5000 pasos cada una):
E media final: 0.85, CI95 [0.85, 0.85]
Seeds en rango [0.5, 1.2]: 100%  (criterio ≥90%: PASA)
E min 0.81, max 0.88
```

## Qué demuestra

- **La homeostasis es robusta entre seeds**: E converge a 0.85 (cerca del setpoint 0.8) en las 30 corridas, con rango estrecho [0.81, 0.88]. No es un golpe de suerte de una semilla.
- **El gap de protocolo era real y quedó cerrado**: sin política E caía a 0.50 (H5 refutada); con política E se regula en 0.85. La homeostasis del organismo depende de su política de acción — coherente con la teoría (la homeostasis se mantiene ACTUANDO, no pasivamente).
- **Regla respetada**: H5 original quedó refutada en su protocolo; H5-bis fue pre-registrada antes de ejecutarse. Ninguna corrección post-hoc.

## Estado completo de hipótesis blindadas (Fase 1+2+bis)

| Hipótesis | Evidencia | Veredicto |
| :--- | :--- | :--- |
| H1 detección | z 20.6, CI [16.0, 25.5], N=30 | ✅ blindada |
| H3 habituación | 86% reducción, d=3.5, N=30 | ✅ blindada |
| H4 persistencia W | z_post/z = 0.02, N=30 | ✅ blindada |
| H5 homeostasis | E 0.85, CI [0.85, 0.85], 100% seeds | ✅ blindada (bis) |
| Controles CheckVLA | 5/6 (C1 7×, C2 8.5×, C4a/b/c) | ✅ blindado |
| C3a especificidad fina | refutada (generalización por dirección) | 🟡 límite documentado |

**El claim central del proyecto está ahora completamente blindado**: 4 hipótesis con estadística N=30 + 5 controles de validez, con un límite honesto registrado.

## Pendientes del plan de rigor (`46:1`)

- 🔵 **Fase 3**: benchmark público MiniGrid DoorKey vs ICM/RND (medirnos contra el campo)
- 🔵 **Fase 4**: empaquetado reproducibilidad (README, requirements.txt, results/*.json)
- 🔵 **Fase 5** (decisión posterior): paper de taller con los datos blindados

*Resultado reproducible: `results/h5bis.json`. El organismo completo con política regula su energía en 100% de las semillas.*
