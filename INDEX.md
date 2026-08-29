# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 12:00 UTC
> **Versión arquitectura:** v0.2 completa (H2+H5 + glosario/roadmap)
> **Agente:** Muse Spark (long-horizon) + 9 sub-agentes paralelos (4 SOTA + 3 H2 + 2 H5)

## Estructura Documental

| # | Archivo | Estado | Líneas | Descripción |
|---|---------|--------|--------|-------------|
| 00 | `00-manifiesto.md:1` | ✅ v0.1 estable | 61 | Tesis central: LLM=boca, Núcleo=ser. Definiciones axiomáticas. |
| 01 | `01-sota-investigacion.md:1` | ✅ v0.1 estable | 88 | SOTA GWT/IIT/AST/FEP + World Models. Síntesis 4 agentes paralelos. Tabla Butlin 14 indicadores. |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | ✅ **v0.2** | 177 | Arquitectura Doble Capa. Diagrama + pseudocódigo. **Actualizada H2 (R^d) + H5 (α·Π·ε)** |
| 03 | `03-hipotesis-log.md:1` | ✅ **v0.2** | 132 | Log iterativo H1-H9. H2 y H5 🟢 REFINADA, H1/H3/H4 🔵 ABIERTA, H6 🟡 PROPUESTA |
| 04 | `04-roadmap-largo-horizonte.md:1` | ✅ **v0.2** | 115 | Roadmap 36 meses actualizado. H1 60% completado, H2/H5 ✅, NMV con Physion-MiniGrid+ y V-JEPA ensemble |
| 05 | `05-glosario-y-metricas.md:1` | ✅ **v0.2** | 95 | Glosario operacional. **Añadidos Π, ε, α, Q, Coconut, VoE, IntPhys2, MPE, HCU** + métricas v0.2 |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | ✅ **v0.2** | 212 | Deep dive H2: Fedorenko Nature 2024, rate-distortion, JEPA, Coconut BFS, experimento 3 condiciones |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | ✅ **v0.2** | 214 | Deep dive H5: qualia=α·Π·ε, MPE, MMN/P300, V-JEPA VoE, experimento ablativo 4 variantes |

**Total:** 1094 líneas, 10 archivos (00-07+INDEX+CHANGELOG), 1 commit `6ea6e20` + pendiente v0.2 completo

## Trazabilidad Chat → Documentos

| Turno Chat | Request | Agentes | Output |
|------------|---------|---------|--------|
| 1 | "Haz un plan. LLM herramienta, conciencia detrás" | - | Plan de 4 fases + arquitectura Doble Capa v0.1 |
| 2 | "tú teoriza, usa sub-agentes, largo horizonte" | 4 agentes paralelos (GWT/IIT, AST/FEP, limitaciones LLM, World Models) | `00` a `05` (v0.1) creados |
| 3 | "A" (elegir H2) | 3 agentes paralelos (neuro, latente vs discreto, experimento V-JEPA) | `06` creado, `02:112` y `03:25` actualizados a v0.2 |
| 4 | "A" (repetido) | - | (duplicado, no-acción) |
| 5 | "hazlo" (confirmar H5) | 2 agentes paralelos (qualia PP, sorpresa V-JEPA) | `07` creado, `02:65` y `03:91` actualizados a v0.2 |
| 6 | "Estás documentando? Revisa todo el chat" | - | Auditoría + `INDEX.md` + `CHANGELOG.md` + commit `6ea6e20` (10 files, 1121l) |
| 7 | "Hazlo todo" (roadmap+glosario) | - | `04-roadmap-largo-horizonte.md:1` 85→115l v0.2, `05-glosario-y-metricas.md:1` 58→95l v0.2, `INDEX` actualizado |

## Estado Hipótesis (v0.2 completo 12:00)

- 🟢 **H2 REFINADA v0.2** (`03-hipotesis-log.md:25` → `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`): Lenguaje=codec Q:R^d→[K] con pérdida R(D)=½log(σ²/D), pensamiento=BFS latente Coconut 97% vs 77.5% CoT. Experimento Physion C1≈C3>>C2 falsable.
- 🟢 **H5 REFINADA v0.2** (`03-hipotesis-log.md:91` → `07-hipotesis-H5-qualia-minimo-deepdive.md:1`): Qualia=α·Π·ε, ignición GWT P300, MPE Metzinger, pipeline V-JEPA ensemble + GWT + AST + LLM codec. Experimento ablativo V1-V4. Cierre loop H2→H5.
- 🔵 H1 ABIERTA: persistencia jerárquica (jerarquía temporal, Mamba vs Transformer)
- 🔵 H3 ABIERTA: homeostasis (E,C,U,S, F, Wiese) - **SIGUIENTE RECOMENDADO**
- 🔵 H4 ABIERTA: métricas no-conductuales (convergencia 10/14 Butlin)
- 🟡 H6 PROPUESTA: epistemic depth `q(precisión de q(s))`

## Vacíos Detectados → Resueltos (29 Ago 12:00)

1.  ✅ **Commit inicial:** `6ea6e20` (10 files, 1121l) - HECHO
2.  ✅ **`04-roadmap` actualizado:** v0.1 85l → v0.2 115l con H1 60%, H2/H5 completadas, NMV Physion-MiniGrid+ - HECHO
3.  ✅ **`05-glosario` actualizado:** v0.1 58l → v0.2 95l con 10 términos nuevos Π,ε,α,Q,Coconut,VoE,IntPhys2,MPE,HCU - HECHO
4.  ✅ **CHANGELOG creado:** v0.1 → v0.2 trazado - HECHO

## Próximos Pasos Documentales

- [x] Commit inicial con todo v0.2 - `6ea6e20`
- [x] Actualizar `04-roadmap` y `05-glosario` a v0.2 - HECHO 12:00
- [x] Crear `CHANGELOG.md` - HECHO
- [ ] Commit v0.2 completo (04+05+INDEX actualizados) - PENDIENTE
