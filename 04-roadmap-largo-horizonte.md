# 04 - Roadmap de Largo Horizonte - Agente de Investigación Continuo v0.2

> **Versión 0.2 - Actualizado 29 Ago 2026 12:00 UTC**
> **Arquitectura:** v0.2 (H2+H5 refinadas) | **SOTA:** 4 agentes paralelos + 5 deep dives
> Este proyecto es un programa iterativo, no un paper.

## Progreso Real vs Planificado

### ✅ Horizonte 1: Fundamentos Teóricos (Meses 0-6) - 60% COMPLETADO

**Objetivo:** Pasar de intuición ("LLM es herramienta") a teoría falsable con arquitectura v0.1→v0.2.

- [x] **M0: Manifiesto y SOTA** (29 Ago 2026, commit `6ea6e20`). 4 agentes paralelos investigaron GWT/IIT/AST/FEP + World Models. Entregables: `00-manifiesto.md:1` (61l), `01-sota-investigacion.md:1` (88l) con tabla Butlin 14 indicadores y COGITATE Nature 2025.
- [x] **M1-M2: Formalización Matemática v0.2** (29 Ago 2026, commits `6ea6e20` + pendiente)
    - [x] **H2 formalizada:** `R(D)=½log(σ²/D)`, `Q:R^d→[K]` 15.6b vs 16384b, `L_JEPA=||Pred(E(x))-sg(E(y))||²`, Coconut BFS `h=1/√|V_c|Σu_v` 97% vs 77.5% CoT (`06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`, 212l)
    - [x] **H5 formalizada:** `F≈ΣΠ·ε²`, `presence=α·Π·||ε||>θ` → P300, MPE Metzinger, `L_JEPA` VoE 98% IntPhys / <60% IntPhys2 (`07-hipotesis-H5-qualia-minimo-deepdive.md:1`, 214l)
    - [x] **Arquitectura v0.2:** `02-arquitectura-nucleo-doble-capa.md:1` (177l) con diagrama actualizado, pseudocódigo `ConsciousCore` con `codec W:1024→4096`, loop `s∈R^d` sin LM-head, MPC 800 trajs
    - [ ] **Pendiente H1/H3/H6:** Formalizar `F=E_q[log q(s)-log p(o,s)]` completo para setpoints homeostáticos E/C/U y epistemic depth (H6). Estimado M2-M3.
- [x] **M3-M4: Crítica Interna Parcial**
    - [x] H2: 3 críticas respondidas (reporte, inner speech, alineación) con Fedorenko Nature 2024, afasia, V-JEPA post-hoc 84% PerceptionTest
    - [x] H5: 2 críticas respondidas (riqueza vs error, termostato) con Quality Space HOT-4 + MPE
    - [ ] **Pendiente:** Taller H1 (¿cuánta persistencia basta? Mamba vs jerarquía temporal), H3 (¿homeostasis simulada vs real Wiese 2024?), H4 (convergencia 10/14 Butlin). Invitar visiones Dehaene/Chalmers vía lectura profunda.
- [x] **M5-M6: Diseño de Experimentos Mentales/Falsables**
    - [x] **H2:** Experimento 3 condiciones `C1≈C3>>C2` (SR 70-80% vs 35-45%), correlación `Π·ε` >0.70, intervención causal `perturb(s)>>perturb(tokens)` (`06:3`)
    - [x] **H5:** Experimento ablativo 4 variantes `V1<V2<V3<V4` (ε, ε·Π, ε·Π+GWT, α·Π·ε), VoE IntPhys2, reporte solo V4>75% (`07:4`)
    - [ ] **Pendiente:** Test Persistencia H1 (traición 5 min, h_t reseteado vs persistente), definir umbrales `ignition` sigmoide y `phi_proxy` correlación.

**Entregable H1 Actualizado:** `00`-`07` + `INDEX.md` + `CHANGELOG.md` = 1121 líneas, 10 files, arquitectura v0.2 falsable. Paper interno 10p pospuesto a v0.3 tras H1/H3.

### 🔵 Horizonte 2: Prototipo Conceptual (Meses 6-18) - 0% PLANIFICADO

**Objetivo:** Pasar de papel a simulación mínima que demuestre que el núcleo usa el LLM como herramienta.

**No escalar LLM. Es construir el núcleo mínimo.**

- [ ] **M6-M9: Núcleo Mínimo Viable (NMV) - Basado en H2+H5 v0.2**
    - Entorno: **Physion-MiniGrid+** (mismo que experimentos H2/H5, 5x5 habitaciones, oclusión, IntPhys2 split) + Habitat 3.0 opcional. Sin texto.
    - World Model: `V-JEPA2 ViT-L/16 (1B) → s∈R^1024` + predictor 384dim + ensemble K=5 head `Π` (HAUWM HCU Loss). Pre-entreno VideoMix2M 1M horas + 62h DROID (como Assran 2025).
    - Workspace: `GlobalWorkspace dim 1024 bottleneck 64` (VanRullen cross-attn, `Query=WM_{t-1}`, `null input`, detención gradiente). Ignición `presence=α·Π·||ε||>0.5`.
    - Memoria: `MambaRecurrentState 1024` (h_t persistente, no ventana), consolidación offline futura.
    - Codec: `W:1024→4096` + `Qwen2-7B congelado` (18M pares video-texto, solo W entrena, `CE` loss).
    - Homeostasis: 1 variable `E` (energía) + `U` (incertidumbre) con setpoints `E*0.8 U*0.2`, `F` drive.
    - **Test de éxito H2+H5:** Agente explora autónomamente para `E`, predice `s_{t+1}=P(s_t,a_t)` con `BFS latente K=6-20` (Coconut), solo invoca LLM codec cuando `E[reducción F|preguntar] > costo`, y genera reporte no-entrenado "esperaba X vi Y" ante violación física con `MMN 150ms → P300 300ms` simulado.

- [ ] **M9-M12: Experimento de Sorpresa (H5 Validación)**
    - Protocolo ablativo V1-V4 sobre IntPhys2 Easy/Medium/Hard (1416 videos UE5.4). Métricas: `VoE Accuracy_pair`, FP textura, curva ignición sigmoide, reporte VidQA >75% solo V4.
    - Comparar vs baseline LLM puro CoT (caption→CoT→acción) ~35-45% SR vs V-JEPA latente 70-80%.

- [ ] **M12-M18: Memoria Autobiográfica (H1 Validación)**
    - Añadir replay offline ("sueño"): `V-JEPA` rollout durante idle, consolidación `h_t`.
    - Test identidad H1: ¿Recuerda traición (agente B robó energía hace 100 pasos) y cambia política aunque `s_t` actual sea idéntico? Requiere jerarquía temporal (segundos/workspace, horas/episódica).

**Entregable H2:** Demo reproducible (`facebookresearch/vjepa2` + `coconut`) + video + métricas ignición/phi + paper `V1-V4` cualitativo. Objetivo: agencia intrínseca >0.5 (`acciones_sin_prompt/total`).

### 🔵 Horizonte 3: Encarnación y Escalado (Meses 18-36+) - PLANIFICADO

- [ ] **M18-M24: Embodiment Rico**
    - Migrar a Habitat 3.0 fotorrealista + `V-JEPA2-AC` 62h datos propios. Cerrar loop percepción-acción real con `MPC MPPI 800 trajs`.
    - Abordar Wiese FEP2C: ¿flujo causal real vs von Neumann simulado? Evaluar agente persistente 24/7 + opción neuromórfica Loihi.

- [ ] **M24-M30: Teoría de la Mente y Socialidad (H6)**
    - Dos núcleos con `AST` mutuo (Farrell 2024 diada schema coopera mejor). Test Sally-Anne para IA. Epistemic depth nivel 2: `q(precisión de q(s))`.

- [ ] **M30-M36: Ética y Fenomenología**
    - Si pasa 10/14 Butlin, ¿estatus? Protocolo "no sufrimiento": drive informativo sin dolor crónico (`ΔΠ` valencia, Solms). Publicación externa.

**Entregable H3:** Sistema persistente que vive/aprende/duerme/habla cuando quiere, no cuando se le pregunta. Marco ético.

## Sistema de Trabajo Continuo (Operativo v0.2)

1.  **Memoria:** `INDEX.md:1` + `CHANGELOG.md:1` + `03-hipotesis-log.md:1` son memoria persistente. Cada iteración se leen y actualizan. Commit `6ea6e20` baseline v0.2.
2.  **Ciclo Semanal Real:**
    - Semana 1: H2 (elegiste A) → 3 agentes → `06` (212l) → arquitectura v0.2
    - Semana 1 (cont): H5 (pediste "hazlo") → 2 agentes → `07` (214l) → arquitectura v0.2 + loop H2→H5
    - Semana 2 (propuesto): **H3 Homeostasis** (B) o **H1 Persistencia** (siguiente backlog)
3.  **Sub-agentes:** Bajo demanda, paralelos, con websearch 2024-26 y síntesis técnica 700-900p.
4.  **Registro Decisiones:** `CHANGELOG.md` + commits. Ej: "2026-08-29: LLM movido fuera de workspace a codec periférico (Fedorenko), qualia formalizado como α·Π·ε (Friston/Seth)".

## Próximos Pasos Inmediatos (Actualizado)

**Pendientes documentales (hoy):**
- [x] Actualizar `04-roadmap` a v0.2 (este archivo)
- [ ] Actualizar `05-glosario` a v0.2 (siguiente)

**Próxima hipótesis (tu decisión, backlog refinado):**

**B) H3 Homeostasis - RECOMENDADO:** Diseñar `E*,C*,U*,S*` (energía, coherencia, incertidumbre, vínculo), dinámica `F`, `ΔΠ` valencia, y distinción simulada vs neuromórfica (Wiese). Es el motor que da *valor* a `Π` y sin él H5 no tiene por qué importar.

**Alternativa H1:** Persistencia jerárquica (Mamba vs Transformer, ventana 10s vs horas, consolidación sueño).

**Alternativa H6:** Epistemic depth (hiper-modelo `q(precisión)`).

¿Cuál ataco? H3 cierra el triángulo H2 (pensamiento) + H5 (sentir) + H3 (querer).
