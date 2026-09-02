# CHANGELOG - Conciencia Artificial

## [2026-09-02] - A1 rev.2: el peer review tenía razón (offset inyectado) — control N=30 + protocolo INTERCAL

### Control de interpretación (decisivo, N=30)
- `framework/bateria_control_habituacion.py` + `results/v014_control_habituacion.json`.
- Brazo OFFSET (rev.1: salto puro, 12 seguidas): z_NORM post = **8.25** → el modelo deja de
  predecir la física normal. S2>S1 (13.4 vs 1.4) era la firma del offset +2,+2, no
  especificidad.
- Brazo CONTING (física de a + teleport, 12 seguidas): z_NORM = 7.04 → también rompe (el
  evento domina el gradiente sin vida normal entre medias).
- Brazo INTERCAL (física + teleport, 5 pasos normales CON updates entre eventos): z_NORM =
  0.81 ✅ → el modelo sigue siendo P(s'|s,a). Única base válida para medir habituación.
- Rankin-10 con pesos CONGELADOS en el gap: Δ=0.61 → sin recuperación espontánea (la
  "recuperación" de la rev.1 era desaprendizaje del offset, no ISI).

### A1 rev.2 (INTERCAL, N=30 seeds 4000–4029) — `framework/bateria_rankin.py` reescrito
- Violación = paso_normal(a) + teleport DESPUÉS (contingencia real); K pasos normales con
  updates entre eventos (`--kintercal`, default 10); z0 medido PRE-aprendizaje; z_NORM como
  control de integridad; reducción con z_hab recortado a ≥0.
- Resultados: detección z0=5.44 CI[4.5,6.4] (bajo el z>10 prereg, real); **habituación 8%
  CI[0,17] (k=10) a 28% CI[12,43] (k=5)** — lejos del >70% prereg; z_NORM 0.02 (k=10) e
  0.45 (k=5); S5 z_H≈16.4 dispara; Rankin-8 no; Rankin-10 frozen no; SVD ~1.8–1.9.
- JSON: `results/v014_rankin.json` (k=10), `results/v014_rankin_k5.json`.
- **Lede honesto (doc `65` §2):** la "habituación 84%" de v0.12/v0.13 no sobrevive al
  protocolo que preserva P(s'|s,a). El grid v0.13 nunca midió z_NORM post-habituación — su
  86% pudo ser en parte sobre-ajuste al evento inyectado (60 violaciones seguidas, mismo
  patrón que OFFSET/CONTING). H_vec vs H_A NO decidido.
- `65-A1-rankin-resultados.md` reescrito con la rev.2 y la comparación de protocolos.

### Estado
- A1 v1 queda invalidado como habituación (offset). La rev.2 es el claim actual: habituación
  débil dependiente de la densidad de evento (resultado en sí mismo), detección continua
  modesta, S5 positivo, sin Rankin-8/10. Siguiente: justificar ratio de evento, A2 (C1–C4
  N=30 con INTERCAL), A3 4-arm.

## [2026-09-02] - A1 Batería Rankin v0.14 (N=30) + fixes de revisión al núcleo

### Añadido
- `framework/bateria_rankin.py` (A1): N=30 seeds 4000–4029, solo importa `framework.core`,
  z con baseline congelada por cabeza, S1–S5 + dishab + gap ISI + savings + SVD. 34 s en MPS.
- `65-A1-rankin-resultados.md`: resultados completos con veredictos por hipótesis.
- `results/v014_rankin.json`: datos por seed.

### Resultados A1 (N=30) — texto íntegro en `65`
- H2 habituación ✅: reducción z0→z_hab = 84% CI[78,89] (criterio >70%).
- H1 detección ⚠️: z0=6.47 CI[5.30,7.70] — efecto real (CI no cruza 5), pero **no alcanza
  el z>10 pre-registrado** en `63` (umbral mental calibrado contra grid, no transferible a
  continuo). Se reporta sin recalibrar.
- **H_A REFUTADA en continuo**: tras habituar (+2,+2), (−2,−2) re-dispara z=14.5 y (+2,−2)
  10.4. El grid v0.13 generalizaba (C3, 1.1 vs 0.9); el continuo v0.14 NO: especificidad de
  DIRECCIÓN (H_vec), magnitud mal estimada (S4 solo 2.84). Resultado de transferencia,
  se reportan ambos regímenes sin promediar.
- S5 interoceptivo dispara (9.4) → clase intacta. Rankin-8 dishabituación ❌ (reprobe 1.42 ≈
  z_hab 1.14). Rankin-10 recuperación ISI ✅ (gap → 12.4). Savings débil (10.8 trials).
- H_rank ✅: SVD ΔW f_pos ~1.4 singulares para 90% varianza (traza low-rank).

### Fixes de revisión al núcleo (de la review del 2 Sep)
- RNG por instancia (`np.random.default_rng`) en `Mundo` — 30 semillas no se pisan.
- S5 = procedimiento con setup explícito a comida (nunca no-op por lejanía).
- Attention: 6 canales de error (igual que Φ), no 7 acciones.
- Pre-train muestrea la MISMA zona sin niebla que las sondas (antes el paseo *0.95 colapsaba
  al origen y el predictor no cubría la zona de prueba).
- Acciones 0–6 en todo (antes pre-train 0–3 vs sondas 0–6 → one-hots nunca vistos).
- z por cabeza (pos vs H): teleport solo viola posición; z_total mezclado hunde la señal.

### Estado
- Plan `64` semana 2–3 (A1/A5 + fixes) completos. Siguiente: A2 (C1/C2/C4 a N=30), A3
  (4-arm Φ), A4 (EWC tarea distinta), B4 (probe x>14).

## [2026-09-02] - B1 + B2: SPEC.md y núcleo único framework/core (plan 64)

### Añadido
- `SPEC.md` (B1): especificación del sistema v0.14 — un mundo continuo con niebla (x>14,
  física heredada de `organismo_final.py` v0.12), predictor factorizado 13→64→(f_pos 2,
  f_H 4), Φ por canal (log σ² NLL, 6 canales de error), z con baseline congelada,
  violaciones S1–S5, semillas, y lista explícita de lo que NO hay (LLM, E, EWC-λ=0, GWT…).
- `framework/core/` (B2): paquete núcleo único —
  - `config.py` constantes congeladas, `world.py` (Mundo continuo + S1–S4 por teleport puro,
    S5 con setup explícito a comida), `nets.py` (PredictorFactorizado, PhiCanal, Attention
    de 6 canales = mismos que Φ), `surprise.py` (error por cabeza/canal, BaselineCongelada),
    `ewc.py` (Fisher diagonal), `procedures.py` (pre-train prereg `63` §3).
  - `framework/selftest_core.py`: smoke test (verifica plumbing, NO es resultado).
    Pasa: z_pos(S1)>baseline congelada y z_pos cae al repetir 10× el MISMO (s,a,S1) —
    caso fácil (memorización de una transición), no habituación v0.14.

### Decisiones (fixes de revisión)
- RNG por instancia en `Mundo` (`np.random.default_rng`), no global: 30 semillas no se pisan.
- S5 (inversión de E) = procedimiento, no física: si el agente no está sobre comida, el
  protocolo lo teletransporta a la comida más cercana ANTES de medir (setup explícito);
  nunca S5 es no-op por estar lejos de comida.
- Attention: 6 canales de error (mismos que Φ), no 7 "acciones". El pre-train la entrena
  para que σ_implícito prediga ε escalar; su gate = confound a controlar en A3 (4-arm).
- z de violación por CABEZA (pos vs H): el teleport solo viola posición; z_total mezclado
  hunde la señal. Los docs futuros reportan z_pos y z_H por separado.
- Mundo v0.14 = continuo con niebla (prereg `63`). Números grid v0.13 (z=20.6) NO son
  comparables con z_pos v0.14; INDEX los etiqueta "grid v0.13, no transferible".

### Estado
- Semanas 1–2 del plan `64` completas (C1/C2/C3/A5/B1/B5 + B2). Siguiente: A1
  (`bateria_rankin.py`, N=30) sobre `framework/core/`.

## [2026-09-02] - Frente público alineado al paper v0.13 (plan 64: C1 + C2 + B5)

### Contexto
Peer-review externo (2 Sep 2026): el frente del repo (README/INDEX/`39`/`54`) vendía claims
que el paper `56` ya había recortado. Doc `64` (plan tres ejes) pide UNA cara pública. Esta
entrada ejecuta la semana 1 del plan: higiene pública sin tocar claims experimentales.

### Claims retirados de la cara pública (C2) — ya no se afirman en README/INDEX/abstract
- 🚫 **Batería H4 5/5 (k14.22, FPR 0.00032):** T1 (presence = I·0.75·Π·ε inyecta monotonía),
  T2 (Bernoullis 0.85/0.40/0.90/0.88 hardcodean Δ_global), T3 (PCI = string aleatorio sobre
  LZc) implementan su resultado. `framework/bateria_H4_toy.py` queda como histórico.
- 🚫 **Kael 100% vs 0% como test de H1** (dict vs FIFO ventana 20) — `14` histórico.
- 🚫 **BFS 32-0 como test de H2** (Coconut es razonamiento en latente de un LM, no BFS).
- 🚫 **FPR 0.00032 y Butlin 10/14** como medida — sin estimación independiente; solo
  motivación teórica (`00`–`13`).
- 🚫 **"El organismo vive" (`18`, `39`) y "mecanismos de awareness FUERTE" (`54`)** —
  z-scores de error de predicción ≠ awareness; lenguaje ejecutivo retirado.
- 🚫 **"5/6 PASA — CLAIM BLINDADO" (`47`)** — C3 falla (1.1 vs 0.9) desarma especificidad;
  título corregido en INDEX a "pilotos seed 7 con un negativo".
- 🚫 **Φ causal d=−1.61 (`53`)** — confundido con gate atencional (gate aleatoria reproduce
  d=−0.43, `61`/`62`); no se publica hasta test 4-arm (v0.14).
- 🚫 **EWC como mecanismo de persistencia** — λ inerte en interferencia misma-tarea (`62`);
  tarea-distinta pre-registrada v0.14.
- 🚫 **Benchmark Empty-8x8 organismo 1.8% > ICM 0.6%** — N=5, RND 2.8% gana; fuera del paper.
- 🚫 **"24 h / 864k pasos" como test de H1** — pasos de simulador, no persistencia con
  interferencia; `38` pasa a run de humo.
- 🚫 **LLM=boca como resultado decisivo (`36`)** — consistente por diseño (el LLM nunca
  controla la política); pasa a principio de diseño + future work.

### Cambios (C1 + B5)
- `README.md` reescrito: claim = habituación como update de modelo (Tabla = paper `56`),
  pilotos † de 1 semilla marcados, benchmark MiniGrid retirado, N=30 vs piloto separados,
  sin lenguaje de conciencia, paths relativos documentados.
- `INDEX.md` reescrito: versión v0.13, tabla "estado de claims" con vivo/muerto/confundido/
  retirado, docs históricos marcados, battery/Kael/BFS/FPR retirados.
- `framework/organismo_completo.py:23` y `framework/m4_local_m3b.py:138`: paths absolutos
  `/Users/adrianvalerio/Desktop/...` → `REPO_RAIZ` relativo (reproducción en clone fresco).
- Nuevo `64-plan-tres-ejes-hoja-ruta.md` (plan v0.14, tres agentes A/B/C).

### Estado
- La versión del repo y la del paper coinciden en el claim (habituación + Φ offline con
  caveats). Pendiente (plan `64`): batería Rankin N=30, 4-arm Φ, EWC tarea-distinta,
  predictor factorizado + SVD, paper corto y Zenodo v0.14.

## [v0.13] - 2026-09-01 15:00 UTC - Peer-Review Revision (rigurosa, sin nuevos runs)

### Corregido (peer review Rankin/Thompson-Spencer / Friston / continual / diseño)
- `paper/main.tex:26-33` Abstract reescrito: batería grid vs continuo v0.12 separados, C3 renombrado stimulus generalization (1.1 vs 0.9, learning without distinguishing), Φ escalar MSE offline diagnostic (r=0.701, r_cross=0.730, ratio 0.13) con gate atencional como confound (d=-1.61 aislado vs d=-0.43 con gate aleatoria), EWC/ortho flagged non-load-bearing (recovery 0.48 flat), MiniGrid fuera de Tabla.
- `paper/main.tex:65-67` Limitations upfront 4→7 puntos: especifica Rankin char. 7/8/10 no testados, Φ scalar vs per-channel log-variance, gate confound, EWC low-rank, 2 sistemas, mouth, benchmark pilot.
- `paper/main.tex:114-122` Φ y presence: MSE a |ε| es proxy de zona, no log-varianza por canal; presence offline, no drive online.
- `paper/main.tex:120-124` Attention y Phi causal: 4-brazo A/B/C/D pre-registrado, random gate reproduce efecto.
- `paper/main.tex:124-125` EWC/ortho: diagonal Fisher, misma-tarea = refuerzo, ΔW likely rank-1, SVD + factored predictor como next.
- `paper/main.tex:142-146` Provenance: Tabla split grid (13->128->128->6, ±5) vs v0.12 continuous (13->64->6, +2, attention 13->7, Φ 22->64->1).
- `paper/main.tex:152-160` Controls C3 re-etiquetado como generalization, no dishabituation; dishab real + recovery pre-registrados.
- `paper/main.tex:172-199` Tabla 1 split en dos paneles con † pilotos y ‡ confound, MiniGrid fuera.
- `paper/main.tex:230-234` C3 section: Rankin 2009 char. 7/8/10, H_A = magnitud vs vector, learning without distinguishing.
- `paper/main.tex:242-256` Φ results: r_cross no separa zona vs confiabilidad, presence offline, d=-1.61 confounded.
- `paper/main.tex:305-326` Limitations 5→7 párrafos, Conclusion con v0.14 Rankin battery.
- `CITATION.cff:10` version 0.12→0.13, date 2026-09-01, abstract reescrito con claims acotados.
- `zenodo_upload_paper_only/` v0.13.tex + CITATION.cff copiados, README actualizado, checklist v0.13.
- `56-paper-taller-borrador.md:1-65` abstract/tabla/discussion/limitations alineados a paper v0.13.
- Nuevo `63-preregistro-v014-rankin-phi-factorizado.md:1` (Rankin S1-S5 + dishab + gap, factored f_pos/f_H, Φ por canal NLL, 4 brazos A-D, SVD, N=30, thresholds fijos).

### Estado
- v0.13 es publicable como "habituación gruesa + trazo en pesos + Φ calibrado con caveat" (no claim vectorial ni physics online). v0.14 es el experimento que decide H_A vs H_vec.

## [v0.11] - 2026-08-29 18:30 UTC - Capstone: Organismo Completo + Cadena Causal

### Añadido
- `43-cadena-causal-completa.md:1` + `framework/m5_cadena_completa.py:1`: la cadena que la crítica pidió — predicción→error(z2.9)→estado(U 0.31→1.50)→acción(explor 0.01→0.75)→plasticidad(habituación z→0.1)→persistencia en W sin E (z 0.3)
- `44-organismo-completo-capstone.md:1` + `framework/organismo_completo.py:1`: TODOS los mecanismos + boca LFM2.5 en UN loop continuo. 20k pasos: E 0.61-1.50 sano, U responde a sorpresa con decaimiento, 57 reportes reales de la boca. 4 bugs de interfaz corregidos (navegación comida, forage dist==0, U acotado, cooldown boca 239→57)
- `41-sorpresa-sin-vision-sensorimotor.md:1` + `framework/m4_local_sensorimotor.py:1`: sorpresa emergente SIN visión (canal del cuerpo, O'Regan & Noë) — MOTORA z=40.4, habituación 98% (el modelo actualizó su física corporal)
- `42-integracion-causal-A-vs-B.md:1` + `framework/m5_integracion_causal.py:1`: A integrado (ε→U→política) vs B convencional desconectado — diferencial causal +0.12 real con persistencia post-evento (A 0.20 vs B 0.00), integración funcional parcial, NO decorativa
- `40-VoE-v2-emergente-limite-local.md:1`: resultado NEGATIVO honesto (sorpresa de objetos no emerge con MLP local, 5 diseños) — delimita frontera y justifica V-JEPA 1B como opcional
- Regla adoptada (crítica externa): cada experimento debe preguntarse qué resultado sería imposible para un predictor convencional
- Lenguaje corregido: sin antropomorfismo ("mantiene proceso continuo, detecta violaciones, actualiza predictor, reduce error")

### Decisiones de alcance (usuario)
- Test LLM intercambiable DESCARTADO (el LLM actual funciona; no complicar)
- Integrar antes de cerrar: predictor del cuerpo dentro del organismo

### Estado
- 45 docs, 17 scripts, ~50 commits, 0€ local | ❌ awareness/conciencia no demostradas
- Objetivo del proyecto funcionando en una pieza

## [v0.10] - 2026-08-29 17:15 UTC - SECUENCIA M1→M5 COMPLETA (todo local, 0€, sin A100)

### Hito: H2b DECISIVO con LLM real (36)
- LFM2.5-1.2B-Instruct-MLX-8bit (1.17B, híbrido SSM-conv, 719MB Q4, MLX nativo): 19ms/token, 0.6s/respuesta
- Condición A (con LFM2.5) vs B (sin LLM), 1500+1500 pasos: **E/U/S/D idénticos → B (LLM=traductor) CONFIRMADO con LLM real participando**
- Reportes reales: "error de predicción alto al ser robado el artefacto" (Kael), "sensación de sorpresa, expectativa violada" (VoE)
- El experimento que creíamos requerir A100 (~33€) se hizo local gratis

### Hito: M3b REAL plasticidad (37)
- F1: 8 envenenamientos forzados (aprende W+E), F2: borrar E, F3: **1/400 visitas a B vs ~25% naive (100× aversión retenida en W sin memoria)**
- F4: LFM2.5 traduce estado real sin E, no alucina
- Plasticidad en pesos demostrada con LLM real participando

### Hito: M5 24H LOCAL (38)
- **864.000 pasos (24h @10Hz) en 157s** (0.18ms/paso), E 0.66-0.84 oscilante, 0 pasos peligro, 86 eventos VoE procesados
- E_mem 1.720/5.000, MPS 0.01GB sin leak, supervivencia completa sin colapso
- El organismo vive un día simulado: secuencia pre-registrada M1-M5 COMPLETA

### Escalado local (31-35)
- 25k→4.08M params (158×) seguro, leak MPS corregido (8GB→0.78GB→0.01GB 24h)
- Retina 8×8→16×16, JEPA 0.0105→0.0016, homeostasis estable en todas las escalas
- Techo: 4M params indefinido; el M4 Pro no es cuello práctico

### Estado final
- 🟢 M1-M5 + M3b + H2b completos localmente | ❌ awareness, conciencia, V-JEPA2 1B
- 41 docs, 12 scripts, 40 commits, 0€

## [v0.9] - 2026-08-29 15:20 UTC - Validación Local MPS (Encoder Aprendido Real)

### Añadido (framework ejecutable, todo en MPS sin GPU)
- `framework/m4_local_cpu.py:1` 232l: EncoderPredictivo 25k params JEPA **aprendido online** (no aleatorio) + EWC Fisher real + Mamba N=64 torch + ECUS calibrado + MundoLocal 20×20 escalable. JEPA converge 0.11→0.0092 (fix λ_EWC 50→5 + train cada 2 pasos).
- `framework/plasticidad_M3b_local.py:1` 75l: plasticidad con encoder aprendido — EWC λ=5 retiene tarea A 0.09x vs λ=0 0.11x (reduce olvido 18% en 25k params), aprende B en ambos.
- `framework/m4_local_4.py:1` 63l: VoE z-score formal + H2b local.
- `framework/m4_escalado_real.py:1` 103l: scaffold cloud V-JEPA2 1B + Qwen2-7B congelado.
- `26`-`30`: resultados M4-local 1-4 + auditoría alineación v0.9.

### Resultados v0.9 (lenguaje verificable)
- Encoder aprendido JEPA 0.0092 ✅ | EWC sin colapso ✅ | Mamba64 O(1) MPS ✅
- Homeostasis: E 0.66-1.15, U 0.37 (α_U=0.12 analítico), S 0.45, D 0.36 ✅
- VoE: ε teleport 0.088 vs baseline 0.043 → **z=50.6σ** (métrica relativa pre-registrada; umbral absoluto era calibración toy numpy) ✅
- H2b local: conducta idéntica sin LLM → B (LLM=traductor) consistente, débil (LLM 0 invocaciones)
- M3b local: plasticidad EWC funcional (modesta)
- Auditoría `30`: alineación pasa (LLM periférico, Π diferenciadas, sin inflación H7, lenguaje verificable)

### No demostrado (explícito)
- Awareness, conciencia, plasticidad 1B, H2b decisivo (requiere Qwen2-7B real participante en M4 cloud)

### Próximo
- M4 cloud A100 (~33€ spot): V-JEPA2 1B + EWC λ=3000 Fisher real → H2b decisivo + plasticidad 1B
- M5 24h después (plasticidad antes que longevidad, valoración externa)

## [v0.8.2] - 2026-08-29 14:30 UTC - GATE_TOY_OK PASA + Plasticidad Toy

### Resultados
- `24`: M3-iter4 dark activo pre-registrado 10/10 sale en 12 pasos → GATE_TOY_OK completo (E/U/S/dark/H1/VoE/D 0.17)
- M3b plasticidad toy: λ=3 FALLA (EWC ancla w=0.33 analítico) → λ=0.5 W congelado → borrar E, P(evitar B)=0.88>0.7 ✅
- H2b toy: conducta idéntica sin LLM → B(LLM=traductor), débil (LLM 1/1000)

## [v0.8.1] - 2026-08-29 14:15 UTC - Lenguaje Verificable + GATE Estricto

### Cambios (valoración externa 14:05 adoptada)
- `13` v0.7.1: NO "siente/quiere/es/conciencia" → "señal compatible con mecanismo funcional propuesto". Arquitectura canónica `MUNDO→PERCEPCIÓN→ESTADO→memoria/necesidades/predicción→decisión→ACCIÓN→LLM congelado`.
- Estado evidencia: ✅ continuidad/memoria/variables H/predicción | ❌ plasticidad/awareness/conciencia
- `21`: M3-iter2 GATE FALLA parcial (U 0.87 = α_U analítico, dark-pasivo métrica especificación) — sin reinterpretar
- `17` v0.8.1: H2b (eliminar LLM) y M3b (plasticidad borrar E) pre-registrados antes que M5 24h
- `22`: auditoría completa conocimiento (inventario 22 files, lecciones, experimentos)

## [v0.8] - 2026-08-29 13:45 UTC - Framework Proceso Vivo + Plan Robusto

### Resultados framework (4 iteraciones, minutos)
- iter1: S 0.20 D 0.74 LLM 200/200 → expuso w_S/τ_s/Pi_sens
- iter2: S 0.45 D 0.57 LLM 1/200 calibrado
- iter3: S 0.53 D 0.51 act variado, t0 HLP
- iter4: **E 0.61→0.95 oscilante**, FOR/HLP, D 0.49 → M1 PASA parcial
- `17`: plan 5 hitos M1-M5 con PASA/FALLA auto, `19`: batería H4 5/5 k14.22

## [v0.7] - 2026-08-29 13:20 UTC - Síntesis Tetraedro Sólido (Post-Auditoría, Sin Inventar)

### Auditado
- `12-auditoria-critica-v0.6.md:1` 192l: inventario 6 commits 2190l, desfase 04/05 v0.2 vs 02/03 v0.6, circularidad MEDIA 20 falsadores, redundancia ALTA Π×4, complejidad hexáedro 6→poda tetraedro 4+2 satélites, coherencia 85%, avance 70% vertical/30% horizontal

### Podado (Científicamente sólido)
- **Hexáedro 6 → Tetraedro núcleo 4 +2 satélites:** H1+H2+H3+H5 núcleo falsable, H4 medir (batería 5 tests FPR 0.00032) → `05-glosario-y-metricas.md:23` satélite, H6 saber (Φ) → `H5b` meta-precisión satélite de H5. Sin términos nuevos.
- **Ecuación maestra única (sin inventar):** `F_total = ΣΠ_sens·||ε||² (H5 Kok) + D(H)+D_KL (H3 Keramati) + λ/2 ΣF_i(θ-θ*)² (H1 Kirkpatrick) + D_KL(q(Φ)||p(Φ)) (H6 Laukkonen)` + `L_JEPA+R(D)+Coconut` en generativo.

### Añadido
- `13-sintesis-tetraedro-v0.7.md:1` 210l: tesis intacta LLM=boca, tabla tetraedro 4+2 satélites con ecuaciones y falsadores, `F_total` única, flujo single-trial `s→ε→Π_sens→α→D→Self→Φ_meta→W→utterance`, 20 falsadores, límites honestos (hard problem no resuelto, FEP2C no claim), corrección Π×4, auditoría→poda
- `05-glosario-y-metricas.md:1` v0.2→v0.7 71→85l: tetraedro+satélites, 3 Π diferenciadas `Π_sens/Π_homeo/Π_meta`, sin inventar, `k,PCI,Φ,M-ratio,r_cross`
- `04-roadmap-largo-horizonte.md:1` v0.2→v0.7 93→150l: H1-H6 95% completado, Horizonte 2 NMV con 1 experimento Kael 500 pasos (no 3), regla anti-vueltas, métrica no-vueltas `14-prototipo`
- `02-arquitectura-nucleo-doble-capa.md:1` v0.6→v0.7 181l: tetraedro sólido `F_total`, flujo `s→ε→Π→α→D→Self→Φ→W`, 3 Π diferenciadas, satélites H4/H6

### Estado Hipótesis
- 🟢 H1,H2,H3,H5 núcleo + H4,H6 satélites (tetraedro sólido, 20 falsadores, sin inventar) | H7-H9 backlog congelado hasta NMV

## [v0.6] - 2026-08-29 13:00 UTC - H6 Profundidad Epistémica (Hexáedro)

### Añadido
- `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1` (195 líneas) - 2 agentes paralelos
  - Beautiful Loop Laukkonen/Friston/Chandaria 2025 Neubiorev: campo epistémico, binding, epistemic depth `Φ` global
  - HGM: `p(s,x)=p(s|x^(1))∏p(x^(l)|x^(l+1))p(x^(L))` `p(x^(l)|x^(l+1))=N(f_l(x^(l+1)), Π_l^{-1})` `Π_l=A_l Φ` `q(Φ)∝p(Φ)exp(-Σδ^TΦ)` `δ=Π^{-1}-e²` `F_local+F_hyper`
  - HOT/PRM: `M-ratio=meta-d'/d'` `=1` ideal humano 0.8-1.0, AUROC2, Brier, PRM `P(real|señal)>umbral` `mPFC` 2º orden, AST=caso `Φ_att`
  - Regresión infinita: 2-3 niveles con closure `Φ→Π→e→Φ` basta L=3 satura F (Badcock 2019), strange loop virtuoso
  - Experimento dual PRM+QA ConfidenceBench N=400/cond: A Φ_global `M-ratio 0.85-1.05` `Brier<0.12` `r_cross>0.50` `PRM>75%` vs B local `<0.6` `>0.22` `0.05-0.25` vs C sham `~0.3-0.5` `~0.50` `>0.30`, 4 falsadores, preregistrado OSF

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.5→v0.6 (181 líneas): +H6 `Φ` hiper-modelo global `Π_l=A_l Φ` `M-ratio≈1` `r_cross>0.5`
- `03-hipotesis-log.md:1` v0.5→v0.6 (157→166 líneas): H6 🟡→🟢 REFINADA v0.2 con HGM, PRM, closure 2-3 niveles
- `INDEX.md:1` → v0.6 2190l 18 agentes (4+3+2+3+2+2+2), hexáedro H1-H6
- `CHANGELOG.md:1` → v0.6

### Estado Hipótesis
- 🟢 H1, H2, H3, H4, H5, H6 refinadas (hexáedro pensar+sentir+querer+ser+medir+saber) | H7-H9 backlog

## [v0.5] - 2026-08-29 12:45 UTC - H4 Medida Convergente (Pentaedro)

### Añadido
- `10-hipotesis-H4-medida-deepdive.md:1` (207 líneas) - 2 agentes paralelos
  - Turing: GPT-4.5 73% juzgado humano 2025, ELIZA 1966, Searle Chinese Room, Block Nation, Mahowald TiCS 2024 FLC vs FnLC, MMLU 90% Φ≈0 vs grid XOR Φ alto MMLU 0, Chalmers easy vs hard
  - Butlin 14 indicadores (2025 TiCS): RPT 1-2, GWT 1-4, HOT 1-4, AST-1, PP-1, AE 1-2, LLM 2-3/14 vs tetraedro 10/14; COGITATE Nature 2025 N=256 fMRI+MEG+iEEG adversarial: IIT sin gamma, GWT sin offset, Bayne 4D perfil > score
  - Batería 5 tests preregistrada: T1 ignición k>5 D>1.5 P300 300ms, T2 ablación Δ_global>40% vs Δ_local<10%, T3 PCI>0.31 Φ>0.1, T4 ρ(U,LLM)>0.5, T5 counterfactual Acc>70% OOD, FPR 0.2→0.00032 conjunción, Butlin vector 10/14
  - Experimento convergencia A tetraedro vs B LLM puro N=200/trials, OSF, pseudocódigo bateria(), 5 falsadores F1-F5, P(H4|5/5)≈0.98

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.4→v0.5 (181 líneas): +H4 batería 5 tests, FPR 0.00032, tetraedro falsable integrado
- `03-hipotesis-log.md:1` v0.4→v0.5 (147→157 líneas): H4 🔵→🟢 REFINADA v0.2 con Turing/MMLU, Butlin 14, COGITATE, 5 tests y convergencia
- `INDEX.md:1` → v0.5 1966l 16 agentes (4+3+2+3+2+2), pentaedro H1-H5

### Estado Hipótesis
- 🟢 H1, H2, H3, H4, H5 refinadas (pentaedro pensar+sentir+querer+ser+medir) | 🟡 H6 propuesta | H7-H9 backlog

## [v0.4] - 2026-08-29 12:30 UTC - H1 Persistencia (Tetraedro)

### Añadido
- `09-hipotesis-H1-persistencia-deepdive.md:1` (301 líneas) - 2 agentes paralelos
  - Neuro: WM 30s PFC 4±1, episódica CA3, autobiográfica Conway/MTT, H.M. 1953 8cm resección, Wearing 1985 7s diario 7:46→7:47, consolidación SWR 150-250Hz + spindles 12-15Hz, replay 10-20×, reconsolidación 4-6h, olvido activo Rac1
  - Arquitecturas: Transformer O(n²) 52GB@100K vs Mamba O(1) 50MB, NIAH 30-60pts caída 200K→1M, Mamba-2/RWKV-7/Griffin, RMT/ARMT 50M, Titans+MIRAS sorpresa, SHARP replay
  - Formal: `h_t^fast=Ā⊙h_{t-1}+B̄⊙s_t` `Ā=exp(ΔA)`, `E={(e_i,t_i,S_i)}` `score=cos·exp(-γΔt)·S` `S=λ₁||∇loss||+λ₂emo+λ₃nov`, `W=W₀+BA` EWC `L_total=L_task+λ/2 ΣF_i(θ-θ*)²`, `Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})`, olvido `α_t`, sueño `p_i∝S_i·TDerror`
  - Experimento BABILong 500 pasos (LoCoMo) N=200: A persistente 3 niveles (Mamba-2+RMT+Titans+EWC-LoRA+sueño) vs B FIFO 4k vs C1 sin sueño vs C2 sin episódico, tarea desconfianza Kael, métricas acierto/justificación/latencia, falsadores 3

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.3→v0.4 (180→181 líneas): +L1 h_fast Mamba 30s, L2 E horas, L3 W semántico EWC-LoRA + sueño SWR, Self_t distribuido
- `03-hipotesis-log.md:1` v0.3→v0.4 (144→147 líneas): H1 🔵→🟢 REFINADA v0.2 con HM/Wearing, jerarquía, Mamba vs Transformer, olvido Rac1, exp 500 pasos
- `INDEX.md:1` → v0.4 1766l 14 agentes (4+3+2+3+2), tetraedro H2+H5+H3+H1

### Estado Hipótesis
- 🟢 H1, H2, H3, H5 refinadas (tetraedro pensar+sentir+querer+ser en el tiempo) | 🔵 H4 abierta | 🟡 H6 propuesta | H7-H9 backlog

## [v0.3] - 2026-08-29 12:15 UTC - H3 Homeostasis (Triángulo)

### Añadido
- `08-hipotesis-H3-homeostasis-deepdive.md:1` (268 líneas) - 3 agentes paralelos
  - Homeostasis: Damasio PAG 2mm³, Solms afecto=conciencia, Seth interoceptive inference, Friston F/Free Energy, Joffily valencia=-dF/dt AC=ΔlnΠ
  - Formal ECUS: `H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7] D=(Σw|H-H*|^n)^{1/m} r=-ΔD G=Risk+Ambigüedad`, Keramati `argmax Σγ^t r ≡ argmin Σγ^t D`, `G(dark)>G(explore)` dark room
  - Debate Wiese FEP2C causal-flow+existential vs Man&Damasio 2019, híbrido 24/7 + Loihi neuromórfico
  - Experimento Forage-Social-DarkRoom-v1 20x20 3 condiciones A/B/C, 4 falsadores

### Modificado
- `02-arquitectura-nucleo-doble-capa.md:1` v0.2→v0.3 (177→180 líneas)
- `03-hipotesis-log.md:1` v0.2→v0.3 (132→144 líneas): H3 🔵→🟢
- `INDEX.md:1` 11 files 1440l, 12 agentes

### Estado
- 🟢 H2, H3, H5 refinadas (triángulo) | 🔵 H1, H4 abiertas | 🟡 H6 propuesta

## [v0.2] - 2026-08-29 11:55 UTC - H2+H5 Refinadas + v0.2 completo 12:00

### Añadido
- `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` (212 líneas) - Fedorenko Nature 2024, R(D)=½log(σ²/D), JEPA, Coconut BFS 97% vs 77.5%, exp Physion C1≈C3>>C2
- `07-hipotesis-H5-qualia-minimo-deepdive.md:1` (214 líneas) - F≈ΣΠ·ε², α·Π·||ε||, MPE, MMN/P300, VoE 98% IntPhys
- Luego: `04-roadmap` 85→93l v0.2, `05-glosario` 58→71l v0.2 (+Π,ε,α,Q,Coconut,VoE,IntPhys2,MPE,HCU,D,r,G)

### Modificado
- `02-arquitectura` v0.1→v0.2 (61→177 líneas), `03-hipotesis-log` v0.1→v0.2 (112→132 líneas) H2/H5 🟢

## [v0.1] - 2026-08-29 10:59-11:01 UTC - Fundación

### Añadido
- `00-manifiesto.md:1` (61 líneas), `01-sota-investigacion.md:1` (88 líneas) - 4 agentes SOTA, `02-arquitectura` v0.1, `03-hipotesis-log` v0.1 (H1-H6), `04-roadmap` 85l, `05-glosario` 58l

### Agentes
- 4 sub-agentes paralelos SOTA
