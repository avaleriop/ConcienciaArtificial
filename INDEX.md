# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 12:15 UTC
> **Versión arquitectura:** v0.3 (H2+H5+H3 + triángulo pensar+sentir+querer)
> **Agente:** Muse Spark (long-horizon) + 12 sub-agentes paralelos (4 SOTA + 3 H2 + 2 H5 + 3 H3)

## Estructura Documental

| # | Archivo | Estado | Líneas | Descripción |
|---|---------|--------|--------|-------------|
| 00 | `00-manifiesto.md:1` | ✅ v0.1 estable | 61 | Tesis central: LLM=boca, Núcleo=ser. Definiciones axiomáticas. |
| 01 | `01-sota-investigacion.md:1` | ✅ v0.1 estable | 88 | SOTA GWT/IIT/AST/FEP + World Models. Síntesis 4 agentes paralelos. Tabla Butlin 14 indicadores. |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | ✅ **v0.3** | 180 | Arquitectura Doble Capa. Diagrama + pseudocódigo. **H2(R^d)+H5(α·Π·ε)+H3(ECUS D,r=-ΔD,G,valencia)** |
| 03 | `03-hipotesis-log.md:1` | ✅ **v0.3** | 144 | Log iterativo H1-H9. H2/H3/H5 🟢 REFINADA, H1/H4 🔵 ABIERTA, H6 🟡 PROPUESTA |
| 04 | `04-roadmap-largo-horizonte.md:1` | ✅ v0.2 | 93 | Roadmap 36 meses. H1 60%, H2/H5 ✅, NMV Physion-MiniGrid+ |
| 05 | `05-glosario-y-metricas.md:1` | ✅ v0.2 | 71 | Glosario operacional. **Π,ε,α,Q,Coconut,VoE,IntPhys2,MPE,HCU,D,r,G** + métricas v0.2 |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | ✅ v0.2 | 212 | Deep dive H2: Fedorenko Nature 2024, rate-distortion, JEPA, Coconut BFS |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | ✅ v0.2 | 214 | Deep dive H5: qualia=α·Π·ε, MPE, MMN/P300, VoE |
| 08 | `08-hipotesis-H3-homeostasis-deepdive.md:1` | ✅ **v0.2 nuevo** | 268 | Deep dive H3: ECUS D=(Σw|H-H*|^n)^{1/m}, r=-ΔD, G=Risk+Ambiguity, valencia=-dF/dt, Wiese FEP2C, exp Forage-DarkRoom |

**Total:** 1440 líneas, 11 archivos (00-08+INDEX+CHANGELOG), 2 commits (`6ea6e20`, `39726ea`) + pendiente v0.3

## Trazabilidad Chat → Documentos

| Turno Chat | Request | Agentes | Output |
|------------|---------|---------|--------|
| 1 | "Haz un plan. LLM herramienta, conciencia detrás" | - | Plan de 4 fases + arquitectura Doble Capa v0.1 |
| 2 | "tú teoriza, usa sub-agentes, largo horizonte" | 4 agentes paralelos (GWT/IIT, AST/FEP, limitaciones LLM, World Models) | `00` a `05` (v0.1) creados |
| 3 | "A" (elegir H2) | 3 agentes paralelos (neuro, latente vs discreto, experimento V-JEPA) | `06` creado, `02:112` y `03:25` actualizados a v0.2 |
| 4 | "A" (repetido) | - | (duplicado, no-acción) |
| 5 | "hazlo" (confirmar H5) | 2 agentes paralelos (qualia PP, sorpresa V-JEPA) | `07` creado, `02:65` y `03:91` actualizados a v0.2 |
| 6 | "Estás documentando? Revisa todo el chat" | - | Auditoría + `INDEX.md` + `CHANGELOG.md` + commit `6ea6e20` (10 files, 1121l) |
| 7 | "Hazlo todo" (roadmap+glosario) | - | `04-roadmap-largo-horizonte.md:1` 85→93l v0.2, `05-glosario-y-metricas.md:1` 58→71l v0.2, `INDEX` actualizado |
| 8 | "si" (H3 homeostasis) | 3 agentes paralelos (drive, Wiese FEP2C, formalización ECUS) + exp Forage-DarkRoom | `08-hipotesis-H3-homeostasis-deepdive.md:1` 268l, `02:1`→v0.3 180l, `03:53`→H3 🟢 |

## Estado Hipótesis (v0.3 12:15)

- 🟢 **H2 REFINADA v0.2** (`03-hipotesis-log.md:25` → `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`): Lenguaje=codec Q:R^d→[K] R(D)=½log(σ²/D), pensamiento=BFS latente Coconut 97% vs 77.5% CoT. C1≈C3>>C2.
- 🟢 **H5 REFINADA v0.2** (`03-hipotesis-log.md:91` → `07-hipotesis-H5-qualia-minimo-deepdive.md:1`): Qualia=α·Π·ε, P300, MPE, V-JEPA VoE 98% IntPhys. V1<V2<V3<V4.
- 🟢 **H3 REFINADA v0.2** (`03-hipotesis-log.md:53` → `08-hipotesis-H3-homeostasis-deepdive.md:1`): ECUS `D=(Σw|H-H*|^n)^{1/m}`, `r=-ΔD`, `G=Risk+Ambiguity`, `valencia=-dF/dt`, Wiese causal-flow, Man&Damasio. Exp Forage-DarkRoom 3 condiciones. **Triángulo H2(pensar)+H5(sentir)+H3(querer) cerrado.**
- 🔵 H1 ABIERTA: persistencia jerárquica (Mamba h_t, replay sueño) - SIGUIENTE
- 🔵 H4 ABIERTA: métricas no-conductuales
- 🟡 H6 PROPUESTA: epistemic depth

## Vacíos Detectados → Resueltos (29 Ago 12:15)

1.  ✅ **Commits:** `6ea6e20` 1121l, `39726ea` 1157l - HECHO
2.  ✅ **`04-roadmap` v0.2** 93l con H1 60% - HECHO
3.  ✅ **`05-glosario` v0.2** 71l con Π,ε,α,Q,Coconut,VoE,MPE,HCU,D,r,G - HECHO
4.  ✅ **CHANGELOG v0.1→v0.2** - HECHO
5.  ⏳ **Pendiente commit v0.3** (02 v0.3, 03 H3 🟢, 08 nuevo, INDEX) - SIGUIENTE

## Próximos Pasos Documentales

- [x] Commit inicial v0.2 - `6ea6e20`
- [x] Commit v0.2 completo - `39726ea`
- [ ] Commit v0.3 H3 (02+03+08+INDEX+CHANGELOG) - PENDIENTE
