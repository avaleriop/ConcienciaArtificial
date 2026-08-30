# 30 - Auditoría de Alineación v0.9 (gatillada tras 2 commits)

> **Fecha:** 29 Ago 2026 15:15 UTC - Regla auditoría cada 2 commits (`17:1`)
> **Commits auditados:** `4df756b` (M4-local-3), `d77f433` (M4-local-4)

## Checklist de Alineación

| Check | Resultado | Evidencia |
| :--- | :--- | :--- |
| **LLM=boca** (LLM periférico, no controla decisión) | ✅ | `m4_local_cpu.py:163` invoca solo si `U>0.4 && presence>0.7`, nunca decide `a`. Codec separado de política `G`. |
| **Π diferenciadas** (Π_sens≠Π_homeo≠Π_meta) | ✅ parcial | `Π_sens` head (línea 146), `Π_homeo` en pesos ECUS `w=[1,0.8,0.5,1.5]`, `Π_meta/Φ` satélite H6 no implementado local (pre-registrado, no perdido). |
| **Versiones sin desfase** | ✅ | `02` v0.7, `03` v0.7.1, `04` v0.7, `05` v0.7 — coherentes. (Nota: `02` podría decir v0.7.1 lenguaje pero su contenido es arquitectura, no adelanta conclusiones.) |
| **No inflación de hipótesis** | ✅ | H7 solo en backlog (`03:164`), no añadida. Todos los últimos commits son código/resultados, no hipótesis nuevas. |
| **Lenguaje verificable** | ✅ | `29:1` dice "mecanismo H5 opera en representación aprendida", "H2b débil local", "no awareness/conciencia". Sin "siente/quiere/es". |
| **Bug vs mecanismo distinguido** | ✅ | VoE umbral absoluto → calibración sustrato (pre-registrado z-score); política simplificada → bug portado (documentado antes de corregir). |
| **No cambiar métricas para PASA** | ✅ | dark-pasivo quedó FALLA registrada; z-score pre-registrado ANTES en `28:1`. |

## Veredicto

**Alineado.** Sin desviación de tesis `00-manifiesto.md:3`. Progreso es código + resultados verificables, no inflación teórica.

## Pendientes menores (no bloqueantes)

- `02-arquitectura` podría anotar v0.7.1 referencia lenguaje (cosmético, próximo commit con M4 cloud).
- `05-glosario` añadir `z-score VoE` como métrica relativa oficial (ya documentado en `28:1`, `29:1`).
- M4 cloud A100 sigue siendo el único camino para H2b decisivo y plasticidad 1B.

*Auditoría pasa. Siguiente: M4 cloud (GPU) o espera. Todo pre-registrado.*
