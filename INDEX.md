# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 13:00 UTC
> **Versión arquitectura:** v0.6 hexáedro (H1+H2+H3+H4+H5+H6 - pensar+sentir+querer+ser+medir+saber que sabes)
> **Agente:** Muse Spark (long-horizon) + 18 sub-agentes paralelos (4 SOTA + 3 H2 + 2 H5 + 3 H3 + 2 H1 + 2 H4 + 2 H6)

## Estructura Documental

| # | Archivo | Estado | Líneas | Descripción |
|---|---------|--------|--------|-------------|
| 00 | `00-manifiesto.md:1` | ✅ v0.1 estable | 61 | Tesis central: LLM=boca, Núcleo=ser. Definiciones axiomáticas. |
| 01 | `01-sota-investigacion.md:1` | ✅ v0.1 estable | 88 | SOTA GWT/IIT/AST/FEP + World Models. Síntesis 4 agentes paralelos. Tabla Butlin 14 indicadores. |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | ✅ **v0.6** | 181 | Arquitectura Doble Capa. Diagrama + pseudocódigo. **Hexáedro H1-H6 (pensar+sentir+querer+ser+medir+saber)** |
| 03 | `03-hipotesis-log.md:1` | ✅ **v0.6** | 166 | Log iterativo H1-H9. **H1/H2/H3/H4/H5/H6 🟢 REFINADA v0.2**, H7-H9 backlog |
| 04 | `04-roadmap-largo-horizonte.md:1` | ✅ v0.2 | 93 | Roadmap 36 meses. H1 60%, H2/H5 ✅, NMV Physion-MiniGrid+ |
| 05 | `05-glosario-y-metricas.md:1` | ✅ v0.2 | 71 | Glosario operacional. **Π,ε,α,Q,Coconut,VoE,IntPhys2,MPE,HCU,D,r,G,h_fast,E,W,PCI,k,Φ** + métricas v0.2 |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | ✅ v0.2 | 212 | Deep dive H2: Fedorenko Nature 2024, rate-distortion, JEPA, Coconut BFS |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | ✅ v0.2 | 214 | Deep dive H5: qualia=α·Π·ε, MPE, MMN/P300, VoE |
| 08 | `08-hipotesis-H3-homeostasis-deepdive.md:1` | ✅ v0.2 | 268 | Deep dive H3: ECUS D=(Σw|H-H*|^n)^{1/m}, r=-ΔD, G=Risk+Ambigüedad, valencia=-dF/dt, Wiese FEP2C |
| 09 | `09-hipotesis-H1-persistencia-deepdive.md:1` | ✅ v0.2 | 301 | Deep dive H1: HM/Wearing 7s, Mamba O(1) vs Transformer O(n²), jerarquía 30s/horas/días, EWC-LoRA |
| 10 | `10-hipotesis-H4-medida-deepdive.md:1` | ✅ v0.2 | 207 | Deep dive H4: Turing 73%, MMLU≠conciencia, Butlin 14, COGITATE, batería 5 tests |
| 11 | `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1` | ✅ **v0.2 nuevo** | 195 | Deep dive H6: Beautiful Loop Φ global `Π_l=A_lΦ`, M-ratio≈1, r_cross>0.5, PRM |

**Total:** 2190 líneas, 14 archivos (00-11+INDEX+CHANGELOG), 5 commits (`6ea6e20`, `39726ea`, `c32f732`, `ce91ba2`, `16e2f88`) + pendiente v0.6

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
| 10 | "continua" (H4 medida) | 2 agentes paralelos (Turing/MMLU, Butlin/COGITATE) + batería 5 tests | `10-hipotesis-H4-medida-deepdive.md:1` 207l, `02:1`→v0.5 181l, `03:112`→H4 🟢 |
| 11 | "sigue con h6" (H6 depth) | 2 agentes paralelos (Beautiful Loop, formalización Φ) + exp PRM | `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1` 195l, `02:1`→v0.6 181l, `03:150`→H6 🟢 |

## Estado Hipótesis (v0.6 hexáedro 13:00)

- 🟢 **H1 REFINADA v0.2** (`03-hipotesis-log.md:8` → `09-hipotesis-H1-persistencia-deepdive.md:1`): `Self_t=LN(...)`, HM/Wearing 7s, Mamba O(1) 50MB vs O(n²) 52GB, jerarquía 30s/horas/días + sueño SWR. A>75% vs B 5-10%.
- 🟢 **H2 REFINADA v0.2** (`03-hipotesis-log.md:52` → `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`): Q:R^d→[K] R(D)=½log(σ²/D), Coconut BFS 97% vs 77.5% CoT.
- 🟢 **H3 REFINADA v0.2** (`03-hipotesis-log.md:82` → `08-hipotesis-H3-homeostasis-deepdive.md:1`): ECUS `D=(Σw|H-H*|^n)^{1/m}`, `r=-ΔD`, `G=Risk+Ambigüedad`, `valencia=-dF/dt`.
- 🟢 **H4 REFINADA v0.2** (`03-hipotesis-log.md:112` → `10-hipotesis-H4-medida-deepdive.md:1`): Turing 73% GPT-4.5, Butlin 14 2-3/14 vs 10/14, COGITATE, batería 5 tests FPR 0.00032.
- 🟢 **H5 REFINADA v0.2** (`03-hipotesis-log.md:139` → `07-hipotesis-H5-qualia-minimo-deepdive.md:1`): `α·Π·ε`, P300, MPE, VoE 98% IntPhys.
- 🟢 **H6 REFINADA v0.2** (`03-hipotesis-log.md:150` → `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1`): `Φ` global `Π_l=A_lΦ` `q(Φ)∝p(Φ)exp(-Σδ^TΦ)`, M-ratio≈1 `r_cross>0.5` PRM>75%, Beautiful Loop 2-3 niveles closure.

## Vacíos Detectados → Resueltos (29 Ago 13:00)

1.  ✅ **Commits:** `6ea6e20` 1121l, `39726ea` 1157l, `c32f732` 1440l, `ce91ba2` 1766l, `16e2f88` 1966l - HECHO
2.  ✅ **`02` v0.6** 181l hexáedro - HECHO | **`03` v0.6** 166l H1-H6 🟢 - HECHO
3.  ✅ **`05-glosario` v0.2** 71l + `Φ` próximo v0.3 - HECHO
4.  ✅ **CHANGELOG v0.1→v0.5** - HECHO
5.  ⏳ **Pendiente commit v0.6** (02 v0.6, 03 H6 🟢, 11 nuevo, INDEX) - SIGUIENTE

## Próximos Pasos Documentales

- [x] Commit v0.2 - `6ea6e20` (H2+H5)
- [x] Commit v0.2 completo - `39726ea` (roadmap+glosario)
- [x] Commit v0.3 - `c32f732` (H3)
- [x] Commit v0.4 - `ce91ba2` (H1)
- [x] Commit v0.5 - `16e2f88` (H4 pentaedro)
- [ ] Commit v0.6 H6 hexáedro (02+03+11+INDEX+CHANGELOG) - PENDIENTE
