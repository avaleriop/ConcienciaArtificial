# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 12:30 UTC
> **Versión arquitectura:** v0.4 tetraedro (H2+H5+H3+H1 - pensar+sentir+querer+ser en el tiempo)
> **Agente:** Muse Spark (long-horizon) + 14 sub-agentes paralelos (4 SOTA + 3 H2 + 2 H5 + 3 H3 + 2 H1)

## Estructura Documental

| # | Archivo | Estado | Líneas | Descripción |
|---|---------|--------|--------|-------------|
| 00 | `00-manifiesto.md:1` | ✅ v0.1 estable | 61 | Tesis central: LLM=boca, Núcleo=ser. Definiciones axiomáticas. |
| 01 | `01-sota-investigacion.md:1` | ✅ v0.1 estable | 88 | SOTA GWT/IIT/AST/FEP + World Models. Síntesis 4 agentes paralelos. Tabla Butlin 14 indicadores. |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | ✅ **v0.4** | 181 | Arquitectura Doble Capa. Diagrama + pseudocódigo. **H2(R^d)+H5(α·Π·ε)+H3(ECUS)+H1(h_fast+E+W+Self_t)** |
| 03 | `03-hipotesis-log.md:1` | ✅ **v0.4** | 147 | Log iterativo H1-H9. **H1/H2/H3/H5 🟢 REFINADA**, H4 🔵 ABIERTA, H6 🟡 PROPUESTA |
| 04 | `04-roadmap-largo-horizonte.md:1` | ✅ v0.2 | 93 | Roadmap 36 meses. H1 60%, H2/H5 ✅, NMV Physion-MiniGrid+ |
| 05 | `05-glosario-y-metricas.md:1` | ✅ v0.2 | 71 | Glosario operacional. **Π,ε,α,Q,Coconut,VoE,IntPhys2,MPE,HCU,D,r,G,h_fast,E,W** + métricas v0.2 |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | ✅ v0.2 | 212 | Deep dive H2: Fedorenko Nature 2024, rate-distortion, JEPA, Coconut BFS |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | ✅ v0.2 | 214 | Deep dive H5: qualia=α·Π·ε, MPE, MMN/P300, VoE |
| 08 | `08-hipotesis-H3-homeostasis-deepdive.md:1` | ✅ v0.2 | 268 | Deep dive H3: ECUS D=(Σw|H-H*|^n)^{1/m}, r=-ΔD, G=Risk+Ambigüedad, valencia=-dF/dt, Wiese FEP2C |
| 09 | `09-hipotesis-H1-persistencia-deepdive.md:1` | ✅ **v0.2 nuevo** | 301 | Deep dive H1: HM/Wearing 7s, Mamba O(1) vs Transformer O(n²), jerarquía 30s/horas/días, EWC-LoRA, exp 500 pasos |

**Total:** 1766 líneas, 12 archivos (00-09+INDEX+CHANGELOG), 3 commits (`6ea6e20`, `39726ea`, `c32f732`) + pendiente v0.4

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
| 9 | "sigue..." (H1 persistencia) | 2 agentes paralelos (neuro memoria, Mamba vs Transformer) + exp 500 pasos | `09-hipotesis-H1-persistencia-deepdive.md:1` 301l, `02:1`→v0.4 181l, `03:8`→H1 🟢 |

## Estado Hipótesis (v0.4 tetraedro 12:30)

- 🟢 **H1 REFINADA v0.2** (`03-hipotesis-log.md:8` → `09-hipotesis-H1-persistencia-deepdive.md:1`): `Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})`, HM/Wearing 7s, Mamba O(1) 50MB vs Transformer O(n²) 52GB, jerarquía 30s/horas/días + sueño SWR, EWC-LoRA. Exp BABILong 500 pasos A>75% vs B 5-10%.
- 🟢 **H2 REFINADA v0.2** (`03-hipotesis-log.md:52` → `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`): Q:R^d→[K] R(D)=½log(σ²/D), Coconut BFS 97% vs 77.5% CoT. C1≈C3>>C2.
- 🟢 **H3 REFINADA v0.2** (`03-hipotesis-log.md:82` → `08-hipotesis-H3-homeostasis-deepdive.md:1`): ECUS `D=(Σw|H-H*|^n)^{1/m}`, `r=-ΔD`, `G=Risk+Ambigüedad`, `valencia=-dF/dt`. **H2+H5+H3 triángulo.**
- 🟢 **H5 REFINADA v0.2** (`03-hipotesis-log.md:129` → `07-hipotesis-H5-qualia-minimo-deepdive.md:1`): `α·Π·ε`, P300, MPE, VoE 98% IntPhys. V1<V2<V3<V4.
- 🔵 H4 ABIERTA: métricas no-conductuales (convergencia 10/14) - SIGUIENTE
- 🟡 H6 PROPUESTA: epistemic depth `q(precisión de q(s))` | Backlog H7-H9

## Vacíos Detectados → Resueltos (29 Ago 12:30)

1.  ✅ **Commits:** `6ea6e20` 1121l, `39726ea` 1157l, `c32f732` 1440l - HECHO
2.  ✅ **`04-roadmap` v0.2** 93l - HECHO | **`02` v0.4** 181l tetraedro - HECHO
3.  ✅ **`05-glosario` v0.2** 71l con Π,ε,α,Q,Coconut,VoE,MPE,HCU,D,r,G,h_fast,E,W - HECHO
4.  ✅ **CHANGELOG v0.1→v0.3** - HECHO
5.  ⏳ **Pendiente commit v0.4** (02 v0.4, 03 H1 🟢, 09 nuevo, INDEX) - SIGUIENTE

## Próximos Pasos Documentales

- [x] Commit v0.2 - `6ea6e20` (H2+H5)
- [x] Commit v0.2 completo - `39726ea` (roadmap+glosario)
- [x] Commit v0.3 - `c32f732` (H3 triángulo)
- [ ] Commit v0.4 H1 tetraedro (02+03+09+INDEX+CHANGELOG) - PENDIENTE
