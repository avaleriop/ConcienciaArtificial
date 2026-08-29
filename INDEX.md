# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 12:45 UTC
> **Versión arquitectura:** v0.5 pentaedro (H1+H2+H3+H4+H5 - pensar+sentir+querer+ser+medir)
> **Agente:** Muse Spark (long-horizon) + 16 sub-agentes paralelos (4 SOTA + 3 H2 + 2 H5 + 3 H3 + 2 H1 + 2 H4)

## Estructura Documental

| # | Archivo | Estado | Líneas | Descripción |
|---|---------|--------|--------|-------------|
| 00 | `00-manifiesto.md:1` | ✅ v0.1 estable | 61 | Tesis central: LLM=boca, Núcleo=ser. Definiciones axiomáticas. |
| 01 | `01-sota-investigacion.md:1` | ✅ v0.1 estable | 88 | SOTA GWT/IIT/AST/FEP + World Models. Síntesis 4 agentes paralelos. Tabla Butlin 14 indicadores. |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | ✅ **v0.5** | 181 | Arquitectura Doble Capa. Diagrama + pseudocódigo. **H1+H2+H3+H5+H4 (pentaedro falsable)** |
| 03 | `03-hipotesis-log.md:1` | ✅ **v0.5** | 157 | Log iterativo H1-H9. **H1/H2/H3/H4/H5 🟢 REFINADA v0.2**, H6 🟡 PROPUESTA |
| 04 | `04-roadmap-largo-horizonte.md:1` | ✅ v0.2 | 93 | Roadmap 36 meses. H1 60%, H2/H5 ✅, NMV Physion-MiniGrid+ |
| 05 | `05-glosario-y-metricas.md:1` | ✅ v0.2 | 71 | Glosario operacional. **Π,ε,α,Q,Coconut,VoE,IntPhys2,MPE,HCU,D,r,G,h_fast,E,W,PCI,k** + métricas v0.2 |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | ✅ v0.2 | 212 | Deep dive H2: Fedorenko Nature 2024, rate-distortion, JEPA, Coconut BFS |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | ✅ v0.2 | 214 | Deep dive H5: qualia=α·Π·ε, MPE, MMN/P300, VoE |
| 08 | `08-hipotesis-H3-homeostasis-deepdive.md:1` | ✅ v0.2 | 268 | Deep dive H3: ECUS D=(Σw|H-H*|^n)^{1/m}, r=-ΔD, G=Risk+Ambigüedad, valencia=-dF/dt, Wiese FEP2C |
| 09 | `09-hipotesis-H1-persistencia-deepdive.md:1` | ✅ v0.2 | 301 | Deep dive H1: HM/Wearing 7s, Mamba O(1) vs Transformer O(n²), jerarquía 30s/horas/días, EWC-LoRA |
| 10 | `10-hipotesis-H4-medida-deepdive.md:1` | ✅ **v0.2 nuevo** | 207 | Deep dive H4: Turing 73%, MMLU≠conciencia, Butlin 14, COGITATE, batería 5 tests k>5/Δ>40%/PCI>0.31 |

**Total:** 1966 líneas, 13 archivos (00-10+INDEX+CHANGELOG), 4 commits (`6ea6e20`, `39726ea`, `c32f732`, `ce91ba2`) + pendiente v0.5

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

## Estado Hipótesis (v0.5 pentaedro 12:45)

- 🟢 **H1 REFINADA v0.2** (`03-hipotesis-log.md:8` → `09-hipotesis-H1-persistencia-deepdive.md:1`): `Self_t=LN(...)`, HM/Wearing 7s, Mamba O(1) 50MB vs O(n²) 52GB, jerarquía 30s/horas/días + sueño SWR. A>75% vs B 5-10%.
- 🟢 **H2 REFINADA v0.2** (`03-hipotesis-log.md:52` → `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`): Q:R^d→[K] R(D)=½log(σ²/D), Coconut BFS 97% vs 77.5% CoT.
- 🟢 **H3 REFINADA v0.2** (`03-hipotesis-log.md:82` → `08-hipotesis-H3-homeostasis-deepdive.md:1`): ECUS `D=(Σw|H-H*|^n)^{1/m}`, `r=-ΔD`, `G=Risk+Ambigüedad`, `valencia=-dF/dt`.
- 🟢 **H4 REFINADA v0.2** (`03-hipotesis-log.md:112` → `10-hipotesis-H4-medida-deepdive.md:1`): Turing 73% GPT-4.5, MMLU≠conciencia, Butlin 14 (LLM 2-3/14 vs tetra 10/14), COGITATE falló, batería 5 tests k>5/Δ>40%/PCI>0.31/ρ>0.5/Acc>70% FPR 0.00032.
- 🟢 **H5 REFINADA v0.2** (`03-hipotesis-log.md:139` → `07-hipotesis-H5-qualia-minimo-deepdive.md:1`): `α·Π·ε`, P300, MPE, VoE 98% IntPhys.
- 🟡 H6 PROPUESTA: epistemic depth `q(precisión de q(s))` | Backlog H7-H9 - SIGUIENTE

## Vacíos Detectados → Resueltos (29 Ago 12:45)

1.  ✅ **Commits:** `6ea6e20` 1121l, `39726ea` 1157l, `c32f732` 1440l, `ce91ba2` 1766l - HECHO
2.  ✅ **`02` v0.5** 181l pentaedro - HECHO | **`03` v0.5** 157l H1-H5 🟢 - HECHO
3.  ✅ **`05-glosario` v0.2** 71l - HECHO (próximo v0.3 con k, PCI)
4.  ✅ **CHANGELOG v0.1→v0.4** - HECHO
5.  ⏳ **Pendiente commit v0.5** (02 v0.5, 03 H4 🟢, 10 nuevo, INDEX) - SIGUIENTE

## Próximos Pasos Documentales

- [x] Commit v0.2 - `6ea6e20` (H2+H5)
- [x] Commit v0.2 completo - `39726ea` (roadmap+glosario)
- [x] Commit v0.3 - `c32f732` (H3)
- [x] Commit v0.4 - `ce91ba2` (H1 tetraedro)
- [ ] Commit v0.5 H4 pentaedro (02+03+10+INDEX+CHANGELOG) - PENDIENTE
