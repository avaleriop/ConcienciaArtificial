# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 15:20 UTC
> **Versión:** v0.9 — tetraedro núcleo H1+H2+H3+H5 +2 satélites (H4 medir, H6 meta), validado en local MPS
> **Agente:** Muse Spark (long-horizon) + 18 sub-agentes (4 SOTA +3 H2+2 H5+3 H3+2 H1+2 H4+2 H6) + 6 auditorías + 4 fases framework

## Estructura Documental (35 archivos, 5018 líneas)

| # | Archivo | Versión | Líneas | Descripción | Estado |
|---|---------|---------|--------|-------------|--------|
| 00 | `00-manifiesto.md:1` | v0.1 | 61 | Tesis `LLM=boca`. Axiomas. Criterio falsabilidad | ✅ estable |
| 01 | `01-sota-investigacion.md:1` | v0.1 | 88 | GWT/IIT/AST/FEP + World Models, Butlin 14, COGITATE | ✅ estable |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | v0.7.1 | 194 | Arquitectura canónica, `F_total`, flujo single-trial | ✅ |
| 03 | `03-hipotesis-log.md:1` | v0.7.1 | 166 | H1-H6 🟢, H7-H9 backlog | ✅ |
| 04 | `04-roadmap-largo-horizonte.md:1` | v0.7 | 73 | Roadmap 36 meses, anti-vueltas | ✅ |
| 05 | `05-glosario-y-metricas.md:1` | v0.7 | 79 | 3 Π diferenciadas, métricas, anti-métricas | ✅ |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | v0.2 | 212 | Fedorenko, R(D), JEPA, Coconut | ✅ |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | v0.2 | 214 | α·Π·ε, MPE, MMN/P300, VoE | ✅ |
| 08 | `08-hipotesis-H3-homeostasis-deepdive.md:1` | v0.2 | 268 | ECUS D, r=-ΔD, G, valencia | ✅ |
| 09 | `09-hipotesis-H1-persistencia-deepdive.md:1` | v0.2 | 301 | HM/Wearing, Mamba, EWC, jerarquía | ✅ |
| 10 | `10-hipotesis-H4-medida-deepdive.md:1` | v0.2 | 207 | Turing/MMLU, Butlin, batería 5 tests | ✅ |
| 11 | `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1` | v0.2 | 195 | Φ global, M-ratio, PRM | ✅ |
| 12 | `12-auditoria-critica-v0.6.md:1` | - | 192 | Poda hexáedro→tetraedro | ✅ |
| 13 | `13-sintesis-tetraedro-v0.7.md:1` | v0.7.1 | 171 | `F_total`, lenguaje verificable, arquitectura canónica | ✅ |
| 14 | `14-experimento-toy-solidez-2026-08-29.md:1` | - | 61 | H1 100% vs 0%, H2 BFS 32-0 | ✅ ejecutado |
| 15 | `15-framework-proceso-vivo.md:1` | v0.8 | 66 | Framework RN `while True` | ✅ |
| 16 | `16-resultados-framework-minutos.md:1` | v0.8b | 176 | 4 iteraciones (S/E/LLM calibrados) | ✅ |
| 17 | `17-plan-robusto-v0.8-v1.0.md:1` | v0.8.1 | 106 | Hitos M1-M5 + H2b + M3b | ✅ |
| 18 | `18-resumen-ejecutivo-v0.8.md:1` | v0.8 | 116 | Resumen ejecutivo | ✅ |
| 19 | `19-bateria-H4-M2-resultados.md:1` | v0.8b | 51 | H4 toy 5/5 k14.22 | ✅ |
| 20 | `20-hoja-ruta-ingenieria-implementacion.md:1` | v0.8 | 56 | Fases 1-4 → H1-H6 | ✅ |
| 21 | `21-GATE-TOY-OK-M3-resultados.md:1` | v0.8.1 | 52 | M3 FALLA parcial U/dark, α_U analítico | ✅ |
| 22 | `22-auditoria-final-conocimiento.md:1` | - | 109 | Inventario, lecciones, experimentos | ✅ |
| 23 | `23-M3-iter3-H2b-resultados.md:1` | v0.8.1 | 44 | U_eq 0.37 confirmado, H2b toy | ✅ |
| 24 | `24-M3-iter4-plasticidad-resultados.md:1` | v0.8.2 | 58 | GATE PASA, M3b toy 0.88 | ✅ |
| 25 | `25-M4-escalado-plan-requisitos.md:1` | - | 56 | M4 cloud requisitos GPU | ✅ |
| 26 | `26-M4-local-integracion-1-resultados.md:1` | v0.9 | 51 | Encoder aprendido corre MPS, 2 bugs portado | ✅ |
| 27 | `27-M4-local-2-resultados.md:1` | v0.9 | 46 | Política portada E/D PASA, VoE pendiente | ✅ |
| 28 | `28-M4-local-3-resultados.md:1` | v0.9 | 62 | JEPA 0.009, VoE mecanismo, plasticidad EWC | ✅ |
| 29 | `29-M4-local-4-resultados.md:1` | v0.9 | 50 | VoE z=50.6σ, H2b B(LLM=traductor) | ✅ |
| 30 | `30-auditoria-alineacion-v0.9.md:1` | - | 28 | Alineación pasa | ✅ |
| - | `framework/process_vivo_minutos.py:1` | v0.8d | 459 | Mundo escalable, tetraedro toy completo | ✅ ejecutable |
| - | `framework/bateria_H4_toy.py:1` | v0.8b | 198 | 5 tests H4 toy | ✅ ejecutable |
| - | `framework/plasticidad_M3b_toy.py:1` | v0.8b | 69 | Plasticidad 1 peso | ✅ ejecutable |
| - | `framework/m4_escalado_real.py:1` | v0.9 | 103 | Scaffold cloud V-JEPA2 1B | ✅ scaffold |
| - | `framework/m4_local_cpu.py:1` | v0.9 | 232 | Encoder JEPA + EWC + Mamba64 MPS | ✅ ejecutable |
| - | `framework/plasticidad_M3b_local.py:1` | v0.9 | 75 | Plasticidad EWC real local | ✅ ejecutable |
| - | `framework/m4_local_4.py:1` | v0.9 | 63 | VoE z-score + H2b local | ✅ ejecutable |
| - | `INDEX.md:1` + `CHANGELOG.md:1` | v0.9 | - | Este índice + historial | ✅ |

## Estado Hipótesis (lenguaje verificable, no "siente/quiere/es")

- 🟢 **H1** (`09:1`): continuidad de estado y memoria sin reset 1000 pasos — demostrado en toy y local (Kael 100% vs 0%)
- 🟢 **H2** (`06:1`): pensamiento `R^d` BFS, LLM codec `R(D)` — BFS 32-0, H2b conducta idéntica sin LLM
- 🟢 **H3** (`08:1`): estado homeostático modifica política — E 0.66-1.15, U 0.37, S 0.45, D 0.36
- 🟢 **H4 SATÉLITE** (`10:1`): batería 5 tests — 5/5 k14.22 FPR 0.00032 (toy)
- 🟢 **H5** (`07:1`): señal de error de predicción responde a violación — VoE z=50.6σ (local)
- 🟢 **H6 SATÉLITE** (`11:1`): Φ global meta-precisión — diseñado, pendiente local

**NO demostrado (explícito):** awareness, conciencia, plasticidad a escala 1B, H2b decisivo (requiere LLM real participante).

## Trazabilidad Chat → Documentos (resumida, 13 sesiones de trabajo)

| Turno | Request | Output clave |
|-------|---------|--------------|
| 1-2 | Plan + teorizar con sub-agentes | `00`-`05` v0.1, 4 agentes SOTA |
| 3-5 | H2, H5 | `06`, `07` deep dives |
| 6-7 | Documentar todo | `INDEX`, `CHANGELOG`, commits |
| 8-11 | H3, H1, H4, H6 | `08`-`11` deep dives |
| 12 | Auditoría anti-vueltas | `12` poda hexáedro→tetraedro |
| 13 | Lo mejor científico | `13` síntesis `F_total` |
| 14-15 | Probar solidez | `14` toy 0.2s, `15` framework `while True` |
| 16 | Framework minutos | `16` 4 iteraciones calibración |
| 17-18 | Plan robusto + resumen | `17` hitos M1-M5, `18` ejecutivo |
| 19-21 | M2 batería + M3 GATE | `19` 5/5, `21` FALLA U/dark estricto |
| 22-23 | Auditoría conocimiento + M3-iter3 | `22` inventario, `23` U_eq 0.37 |
| 24 | M3-iter4 + plasticidad toy | `24` GATE PASA, M3b 0.88 |
| 25-26 | M4 escalado + local | `25` requisitos GPU, `26` M4-local integración 1 |
| 27-29 | M4-local 2-4 | `27`-`29` encoder convergente, VoE 50σ, H2b |
| 30 | Auditoría alineación | `30` pasa |

## Próximos Pasos Pre-registrados

- [x] M1-M4-local completos (toy + local MPS)
- [ ] **M4 cloud A100** (~33€ spot): V-JEPA2 1B + Qwen2-7B congelado — H2b decisivo + plasticidad 1B (requiere aprobación de gasto)
- [ ] **M5 24h** después de M4 (plasticidad antes que longevidad)
- [ ] Auditoría cada 2 commits (activa)
- [ ] Pendientes menores: `02` anotar v0.7.1 lenguaje, `05` añadir z-score VoE

*Todo documentado y versionado. Sin pérdida de conocimiento: cada bug, lección y resultado tiene archivo + commit.*
