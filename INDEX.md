# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 11:55 UTC
> **Versión arquitectura:** v0.2 (H2+H5 refinadas)
> **Agente:** Muse Spark (long-horizon) + sub-agentes paralelos

## Estructura Documental

| # | Archivo | Estado | Líneas | Descripción |
|---|---------|--------|--------|-------------|
| 00 | `00-manifiesto.md:1` | ✅ v0.1 estable | 61 | Tesis central: LLM=boca, Núcleo=ser. Definiciones axiomáticas. |
| 01 | `01-sota-investigacion.md:1` | ✅ v0.1 estable | 88 | SOTA GWT/IIT/AST/FEP + World Models. Síntesis 4 agentes paralelos. Tabla Butlin 14 indicadores. |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | 🔄 **v0.2** | 177 | Arquitectura Doble Capa. Diagrama + pseudocódigo. **Actualizada H2 (R^d) + H5 (α·Π·ε)** |
| 03 | `03-hipotesis-log.md:1` | 🔄 **v0.2** | 132 | Log iterativo H1-H9. H2 y H5 🟢 REFINADA, H1/H3/H4 🔵 ABIERTA, H6 🟡 PROPUESTA |
| 04 | `04-roadmap-largo-horizonte.md:1` | ⚠️ v0.1 desactualizado | 85 | Roadmap 36 meses (3 horizontes). **Pendiente actualizar con H2/H5 y fechas reales** |
| 05 | `05-glosario-y-metricas.md:1` | ⚠️ v0.1 desactualizado | 58 | Glosario operacional. **Pendiente añadir Π, ε, α, Q, Coconut, VoE** |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | ✅ **v0.2 nuevo** | 212 | Deep dive H2: Fedorenko Nature 2024, rate-distortion, JEPA, Coconut BFS, experimento 3 condiciones |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | ✅ **v0.2 nuevo** | 214 | Deep dive H5: qualia=α·Π·ε, MPE, MMN/P300, V-JEPA VoE, experimento ablativo 4 variantes |

**Total:** 1027 líneas, 8 archivos, 0 commits (pendiente)

## Trazabilidad Chat → Documentos

| Turno Chat | Request | Agentes | Output |
|------------|---------|---------|--------|
| 1 | "Haz un plan. LLM herramienta, conciencia detrás" | - | Plan de 4 fases + arquitectura Doble Capa v0.1 |
| 2 | "tú teoriza, usa sub-agentes, largo horizonte" | 4 agentes paralelos (GWT/IIT, AST/FEP, limitaciones LLM, World Models) | `00` a `05` (v0.1) creados |
| 3 | "A" (elegir H2) | 3 agentes paralelos (neuro, latente vs discreto, experimento V-JEPA) | `06` creado, `02:112` y `03:25` actualizados a v0.2 |
| 4 | "A" (repetido) | - | (duplicado, no-acción) |
| 5 | "hazlo" (confirmar H5) | 2 agentes paralelos (qualia PP, sorpresa V-JEPA) | `07` creado, `02:65` y `03:91` actualizados a v0.2 |
| 6 | "Estás documentando? Revisa todo el chat" | - | **Esta auditoría + INDEX + commit** |

## Estado Hipótesis

- 🟢 **H2 REFINADA v0.2** (`03-hipotesis-log.md:25` → `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`): Lenguaje=codec Q:R^d→[K] con pérdida R(D)=½log(σ²/D), pensamiento=BFS latente Coconut 97% vs 77.5% CoT. Experimento Physion C1≈C3>>C2 falsable.
- 🟢 **H5 REFINADA v0.2** (`03-hipotesis-log.md:91` → `07-hipotesis-H5-qualia-minimo-deepdive.md:1`): Qualia=α·Π·ε, ignición GWT P300, MPE Metzinger, pipeline V-JEPA ensemble + GWT + AST + LLM codec. Experimento ablativo V1-V4.
- 🔵 H1 ABIERTA: persistencia jerárquica
- 🔵 H3 ABIERTA: homeostasis (siguiente propuesto)
- 🔵 H4 ABIERTA: métricas no-conductuales
- 🟡 H6 PROPUESTA: epistemic depth

## Vacíos Detectados (29 Ago 11:55)

1.  **Sin commits git:** 8 archivos untracked, `main` sin commits. No hay historial trazable.
2.  **`04-roadmap` desactualizado:** sigue en v0.1, no refleja que H2/H5 ya completadas ni fechas reales de ejecución.
3.  **`05-glosario` desactualizado:** faltan términos v0.2: Π/precisión, ε/error, α/attention schema, Q/quality space, Coconut, VoE, IntPhys2, MPE.
4.  **Sin CHANGELOG:** no hay registro fechado de cambios v0.1→v0.2.

## Próximos Pasos Documentales

- [ ] Commit inicial con todo v0.2
- [ ] Actualizar `04-roadmap` y `05-glosario` a v0.2
- [ ] Crear `CHANGELOG.md`
