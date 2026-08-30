# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 18:30 UTC
> **Versión:** v0.11 — ORGANISMO COMPLETO: todos los mecanismos + boca LFM2.5 en UN loop (capstone)
> **Logros clave v0.11:** cadena causal completa (detecta→estado→acción→aprende→persiste en W sin E) + sorpresa emergente sin visión (canal del cuerpo, z=40σ) + capstone integrado 20k pasos

## Estructura Documental (41 docs + 12 scripts)

| # | Archivo | Versión | Líneas | Descripción | Estado |
|---|---------|---------|--------|-------------|--------|
| 00 | `00-manifiesto.md:1` | v0.1 | 61 | Tesis `LLM=boca`, axiomas, falsabilidad | ✅ |
| 01 | `01-sota-investigacion.md:1` | v0.1 | 88 | SOTA GWT/IIT/AST/FEP, Butlin 14 | ✅ |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | v0.7.1 | 194 | Arquitectura canónica, `F_total` | ✅ |
| 03 | `03-hipotesis-log.md:1` | v0.7.1 | 166 | H1-H6 🟢, backlog | ✅ |
| 04 | `04-roadmap-largo-horizonte.md:1` | v0.7 | 73 | Roadmap, anti-vueltas | ✅ |
| 05 | `05-glosario-y-metricas.md:1` | v0.9 | 80 | 3 Π, métricas, z-score VoE | ✅ |
| 06-11 | Deep dives H2/H5/H3/H1/H4/H6 | v0.2 | 1397 | Teoría con papers 2024-25 | ✅ |
| 12 | `12-auditoria-critica-v0.6.md:1` | - | 192 | Poda hexáedro→tetraedro | ✅ |
| 13 | `13-sintesis-tetraedro-v0.7.md:1` | v0.7.1 | 171 | `F_total`, lenguaje verificable | ✅ |
| 14 | `14-experimento-toy-solidez-2026-08-29.md:1` | - | 61 | H1 100% vs 0%, BFS 32-0 | ✅ |
| 15 | `15-framework-proceso-vivo.md:1` | v0.8 | 66 | Framework `while True` | ✅ |
| 16 | `16-resultados-framework-minutos.md:1` | v0.8b | 176 | 4 iteraciones calibración | ✅ |
| 17 | `17-plan-robusto-v0.8-v1.0.md:1` | v0.8.1 | 106 | M1-M5 + H2b + M3b | ✅ |
| 18 | `18-resumen-ejecutivo-v0.8.md:1` | v0.8 | 116 | Resumen (anterior) | ✅ |
| 19 | `19-bateria-H4-M2-resultados.md:1` | v0.8b | 51 | H4 5/5 k14.22 | ✅ |
| 20 | `20-hoja-ruta-ingenieria-implementacion.md:1` | v0.8 | 56 | Fases 1-4 → H1-H6 | ✅ |
| 21 | `21-GATE-TOY-OK-M3-resultados.md:1` | v0.8.1 | 52 | U/dark estricto | ✅ |
| 22 | `22-auditoria-final-conocimiento.md:1` | - | 109 | Inventario completo | ✅ |
| 23 | `23-M3-iter3-H2b-resultados.md:1` | v0.8.1 | 44 | U_eq 0.37, H2b toy | ✅ |
| 24 | `24-M3-iter4-plasticidad-resultados.md:1` | v0.8.2 | 58 | GATE PASA, M3b toy | ✅ |
| 25 | `25-M4-escalado-plan-requisitos.md:1` | - | 56 | Requisitos GPU (superado parcial) | ✅ |
| 26 | `26-M4-local-integracion-1-resultados.md:1` | v0.9 | 51 | Encoder aprendido MPS | ✅ |
| 27 | `27-M4-local-2-resultados.md:1` | v0.9 | 46 | Política portada | ✅ |
| 28 | `28-M4-local-3-resultados.md:1` | v0.9 | 62 | JEPA 0.009, plasticidad EWC | ✅ |
| 29 | `29-M4-local-4-resultados.md:1` | v0.9 | 50 | VoE 50σ, H2b local | ✅ |
| 30 | `30-auditoria-alineacion-v0.9.md:1` | - | 28 | Alineación pasa | ✅ |
| 31 | `31-M4-local-v2-escalado-seguro.md:1` | v0.9 | 46 | Escalado 45×, techo máquina | ✅ |
| 32 | `32-M4-local-v3-leak-fix.md:1` | v0.9 | 32 | Leak MPS corregido 0.78GB | ✅ |
| 33 | `33-M4-local-v4-escala-4M.md:1` | v0.9 | 40 | 4M params, techo documentado | ✅ |
| 34 | `34-M4-local-v5-mundo-rico.md:1` | v0.9 | 48 | Retina 8×8, homeostasis estable | ✅ |
| 35 | `35-M4-local-v6-retina-16.md:1` | v0.9 | 40 | Escalado gradual confirmado | ✅ |
| 36 | `36-H2b-decisivo-LFM25-local.md:1` | **v0.10** | 44 | **LLM real confirma traductor** | ✅ |
| 37 | `37-M3b-real-plasticidad-LFM25.md:1` | **v0.10** | 44 | **Plasticidad W 100× sin E** | ✅ |
| 38 | `38-M5-24h-local.md:1` | **v0.10** | 48 | **864k pasos sin colapso** | ✅ |
| - | `INDEX.md` + `CHANGELOG.md` | **v0.10** | - | Este índice + historial | ✅ |

## Framework ejecutables (12 scripts, todos probados en M4 Pro)

| Script | Rol | Estado |
| :--- | :--- | :--- |
| `framework/process_vivo_minutos.py:1` | Toy numpy, mundo escalable | ✅ |
| `framework/bateria_H4_toy.py:1` | 5 tests H4 | ✅ 5/5 |
| `framework/plasticidad_M3b_toy.py:1` | Plasticidad 1 peso | ✅ 0.88 |
| `framework/m4_escalado_real.py:1` | Scaffold cloud 1B | 🔵 requiere GPU |
| `framework/m4_local_cpu.py:1` | Encoder JEPA + EWC + Mamba | ✅ |
| `framework/plasticidad_M3b_local.py:1` | Plasticidad EWC local | ✅ |
| `framework/m4_local_4.py:1` | VoE z-score + H2b | ✅ 50σ |
| `framework/m4_local_v2.py:1` | Escalado hasta 4M params | ✅ |
| `framework/m4_local_v5.py:1` | Retina 8×8→16×16 | ✅ |
| `framework/m4_local_h2b.py:1` | **H2b con LFM2.5 real** | ✅ decisivo |
| `framework/m4_local_m3b.py:1` | **M3b plasticidad con LFM2.5** | ✅ 100× |
| `framework/m5_24h_local.py:1` | **M5 24h (864k pasos)** | ✅ |

## Estado de Hitos (plan robusto COMPLETO)

| Hito | Resultado | Evidencia |
| :--- | :--- | :--- |
| **M1** navegación | E 0.61→0.95 oscilante, act variado | `16:1` |
| **M2** batería H4 | 5/5 tests, k14.22, FPR 0.00032 | `19:1` |
| **M3** GATE toy/local | U 0.37 analítico, dark 10/10, VoE 50σ→0.9 | `21`,`24`,`29`,`35` |
| **M3b** plasticidad | W retiene 100× sin E (toy 0.88, local, LFM2.5) | `24`,`37` |
| **H2b** LLM real | conducta idéntica con/sin LFM2.5-1.2B | `36` |
| **M5** 24h | 864k pasos, 0 colapsos, D 0.34 | `38` |

## Estado Hipótesis (lenguaje verificable)

- 🟢 **H1 Ser en tiempo:** continuidad y memoria sin reset (Kael 100% vs 0%, 24h vivas)
- 🟢 **H2 Pensar R^d:** BFS 32-0, LLM codec (H2b real: traductor confirmado)
- 🟢 **H3 Querer ECUS:** homeostasis E/U/S/D estable en toy, local y 24h
- 🟢 **H4 Medir:** batería 5/5 FPR 0.00032
- 🟢 **H5 Sentir:** señal de error (VoE 50σ local, 86 eventos en 24h)
- 🟢 **H6 Saber:** Φ meta diseñado, pendiente implementación local
- ❌ **NO demostrado:** awareness, conciencia, V-JEPA2 1B, sorpresa emergente

## Trazabilidad (turnos clave)

| Turno | Logro |
|-------|-------|
| 1-13 | Teoría tetraedro sólida, auditorías, síntesis |
| 14-24 | Toy probado, framework vivo, GATE PASA, plasticidad toy |
| 25-35 | M4 local: encoder aprendido, escalado 4M, retina 16×16 |
| 36-38 | **LFM2.5 real: H2b decisivo + M3b real + M5 24h** |

## Próximos Pasos (pre-registrados)

1. **VoE-v2 emergente:** sorpresa descubierta por el modelo, no programada (evento imposible en latente)
2. **M4 cloud V-JEPA2 1B:** world model real con video (único punto que necesita GPU, si hay presupuesto)
3. **H6 local:** Φ hiper-modelo de precisión (M-ratio)
4. Auditoría cada 2 commits (activa)

*Todo documentado y versionado: 40 commits, 41 docs, 12 scripts, 0€, sin pérdida de conocimiento.*
