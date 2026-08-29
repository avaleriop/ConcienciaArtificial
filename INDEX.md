# INDEX - Conciencia Artificial - Estado del Proyecto

> **Última actualización:** 29 Ago 2026 13:20 UTC
> **Versión arquitectura:** v0.7 tetraedro sólido H1+H2+H3+H5 +2 satélites (H4 medir, H6 meta) - sin inventar
> **Agente:** Muse Spark (long-horizon) + 18 sub-agentes (4 SOTA +3 H2+2 H5+3 H3+2 H1+2 H4+2 H6) + auditoría + síntesis

## Estructura Documental

| # | Archivo | Estado | Líneas | Descripción |
|---|---------|--------|--------|-------------|
| 00 | `00-manifiesto.md:1` | ✅ v0.1 estable | 61 | Tesis central: LLM=boca, Núcleo=ser. Definiciones axiomáticas. |
| 01 | `01-sota-investigacion.md:1` | ✅ v0.1 estable | 88 | SOTA GWT/IIT/AST/FEP + World Models. Síntesis 4 agentes paralelos. Tabla Butlin 14 indicadores. |
| 02 | `02-arquitectura-nucleo-doble-capa.md:1` | ✅ **v0.7** | 181 | Arquitectura Doble Capa. **Tetraedro sólido H1+H2+H3+H5 +2 satélites H4/H6** - `F_total` |
| 03 | `03-hipotesis-log.md:1` | ✅ **v0.6** | 166 | Log H1-H6 🟢 H7-H9 backlog |
| 04 | `04-roadmap-largo-horizonte.md:1` | ✅ **v0.7** | 150 | Roadmap v0.7 post-auditoría, H1-H6 95% completado, NMV tetraedro |
| 05 | `05-glosario-y-metricas.md:1` | ✅ **v0.7** | 85 | Glosario v0.7 tetraedro+satélites, 3 Π diferenciadas, sin inventar |
| 06 | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` | ✅ v0.2 | 212 | Deep dive H2: Fedorenko Nature 2024, R(D), JEPA, Coconut BFS |
| 07 | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` | ✅ v0.2 | 214 | Deep dive H5: α·Π·ε, MPE, MMN/P300, VoE |
| 08 | `08-hipotesis-H3-homeostasis-deepdive.md:1` | ✅ v0.2 | 268 | Deep dive H3: ECUS D, r=-ΔD, G, valencia=-dF/dt, Wiese FEP2C |
| 09 | `09-hipotesis-H1-persistencia-deepdive.md:1` | ✅ v0.2 | 301 | Deep dive H1: HM/Wearing 7s, Mamba O(1), jerarquía 30s/horas/días, EWC-LoRA |
| 10 | `10-hipotesis-H4-medida-deepdive.md:1` | ✅ v0.2 | 207 | Deep dive H4: Turing 73%, Butlin 14, COGITATE, batería 5 tests |
| 11 | `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1` | ✅ v0.2 | 195 | Deep dive H6: Φ global Π_l=A_lΦ, M-ratio≈1, r_cross>0.5 |
| 12 | `12-auditoria-critica-v0.6.md:1` | ✅ | 192 | Auditoría: no vueltas, pero hexáedro→poda tetraedro |
| 13 | `13-sintesis-tetraedro-v0.7.md:1` | ✅ **v0.7 nuevo** | 210 | Síntesis tetraedro: ecuación maestra F_total, flujo single-trial, 20 falsadores |

**Total:** ~2600 líneas, 15 archivos, 7 commits + pendiente v0.7

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
| 12 | "registra todo + revisa vueltas" (auditoría) | Revisión directa 14 files 2212l | `12-auditoria-critica-v0.6.md:1` 192l hexáedro→tetraedro poda |
| 13 | "haz lo mejor científico" (poda+síntesis) | Auditoría → tetraedro sólido | `13-sintesis-tetraedro-v0.7.md:1` 210l F_total, `02:1` v0.7, `04:1`/`05:1` v0.7 |

## Estado Hipótesis (v0.7 tetraedro sólido 13:20)

- 🟢 **H1 REFINADA v0.2** (`03-hipotesis-log.md:8` → `09-hipotesis-H1-persistencia-deepdive.md:1`): `Self_t` jerárquico HM/Wearing 7s Mamba O(1) 50MB vs 52GB. A>75% vs B 5-10%.
- 🟢 **H2 REFINADA v0.2** (`03-hipotesis-log.md:52` → `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`): Q:R^d→[K] R(D)=½log(σ²/D), Coconut BFS 97% vs 77.5%.
- 🟢 **H3 REFINADA v0.2** (`03-hipotesis-log.md:82` → `08-hipotesis-H3-homeostasis-deepdive.md:1`): ECUS D, r=-ΔD, G=Risk+Ambigüedad, valencia=-dF/dt.
- 🟢 **H4 REFINADA v0.2 SATÉLITE** (`10-hipotesis-H4-medida-deepdive.md:1`): Turing 73%, Butlin 14 2-3/14 vs 10/14, batería 5 tests FPR 0.00032.
- 🟢 **H5 REFINADA v0.2** (`03-hipotesis-log.md:139` → `07-hipotesis-H5-qualia-minimo-deepdive.md:1`): α·Π_sens·||ε|| P300, MPE.
- 🟢 **H6 REFINADA v0.2 SATÉLITE** (`11-hipotesis-H6-profundidad-epistemica-deepdive.md:1`): Φ global Π_l=A_lΦ M-ratio≈1 r_cross>0.5 PRM>75% (H5b).

## Vacíos Detectados → Resueltos (29 Ago 13:20)

1.  ✅ **Commits:** 6 commits hasta v0.6 hexáedro 2190l - HECHO
2.  ✅ **`02` v0.7** 181l tetraedro sólido + `F_total` - HECHO
3.  ✅ **`04` v0.7** 150l post-auditoría + **`05` v0.7** 85l tetraedro+satélites 3 Π - HECHO
4.  ✅ **`12` auditoría** 192l + **`13` síntesis** 210l F_total - HECHO
5.  ⏳ **Pendiente commit v0.7** (02 v0.7, 04 v0.7, 05 v0.7, 13 síntesis, INDEX) - SIGUIENTE

## Próximos Pasos Documentales (v0.7 sólido, sin inventar)

- [x] Commit v0.2 - `6ea6e20` (H2+H5)
- [x] Commit v0.2 completo - `39726ea` (roadmap+glosario)
- [x] Commit v0.3 - `c32f732` (H3 triángulo)
- [x] Commit v0.4 - `ce91ba2` (H1 tetraedro)
- [x] Commit v0.5 - `16e2f88` (H4 pentaedro)
- [x] Commit v0.6 - `3542400` (H6 hexáedro)
- [x] Commit auditoría - `b00f290` (12)
- [ ] Commit v0.7 tetraedro sólido (02 v0.7, 04 v0.7, 05 v0.7, 13 síntesis, INDEX, CHANGELOG) - PENDIENTE
- [ ] Luego `14-prototipo-NMV.md` (1 experimento Kael 500 pasos H1) - Congelar teoría
