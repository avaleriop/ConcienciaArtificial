# 05 - Glosario y Métricas v0.7 - Sólido y sin Inventar

> **Versión 0.7 - 29 Ago 2026 13:20 UTC - Consolidación científica post-auditoría**
> Cambios v0.7: Podado a tetraedro núcleo H1+H2+H3+H5 + 2 satélites (H4 medir, H6 saber/meta). Diferenciados 3 `Π` (sensorial/homeostático/meta), añadidos k, PCI, Φ/M-ratio, r_cross. Sin términos inventados, solo 2024-26 publicados.
> Definiciones operacionales. Si no podemos medirlo, no podemos iterarlo.

## Glosario Esencial v0.7 - Tetraedro Núcleo

| Término | Definición Operacional v0.7 (sin inventar) | Origen publicado | ¿Lo tiene un LLM? |
| :--- | :--- | :--- | :--- |
| **Conciencia (mínima)** | Propiedad del sistema cuando `s∈R^d` (World Model) + `Workspace 64D` + `Self_t` jerárquico están integrados con `D(H)` homeostasis y `presence=α·Π_sens·||ε||>θ` atribuido a yo es globalmente accesible. Requiere H1+H2+H3+H5. Satélites H4/H6 miden/saben. | Híbrido GWT+FEP+AST (Butlin 14) | No |
| **Awareness** | Disponibilidad global para reporte/control (GWT). Medible por ignición `k>5` sigmoide + broadcast. Disociable de fenomenalidad (afasia Fedorenko Nature 2024). | GWT (Dehaene) | Simulado |
| **Sentience / Qualia (núcleo H5)** | Contenido=`z∈Q` Quality Space (Hot-4 Rosenthal), Presencia=`α·Π_sens·||ε||` broadcasteado. Riqueza=profundidad contrafactual, no error magnitud. MPE=`ε→0` con `Π` máxima sobre alerta (Vohryzek 2025). | FEP (Seth) + HOT-4 | No |
| **Π_sens (Precisión sensorial)** | `Π=1/σ²=exp(γ)` ganancia postsináptica sensorial. `Atención = optimizar Π_sens` (Kok 2012). Alta=error confiable→ignición, baja=ruido suprimido. Head ensemble `σ` V-JEPA. | Friston 2010, Kok 2012 | No |
| **Π_homeo (Precisión homeostática)** | Peso `w_i·Π_homeo` en `D(H)=(Σw_i|H_i-H_i*|^n)^{1/m}`. `Valencia=-dF/dt` con `F≈ΣΠ_homeo·ε²`, no es `Π_sens`. Distinto neuromodulador (DA vs ACh). | Keramati 2014, Joffily 2013, Solms | No |
| **Π_meta / Φ (Precisión meta)** | `Π_l=A_lΦ` con `Φ∈R^K` hiper-modelo global `q(Φ)∝p(Φ)exp(-Σδ^TΦ)` `δ=Π^{-1}-e²`. `M-ratio=meta-d'/d'` `=1` ideal. AST es caso `Φ_att`. Satélite H6 de H5, no nueva Π. | Laukkonen/Friston 2025 Beautiful Loop, Fleming HMeta-d | No |
| **ε (Error predicción)** | `ε=o-g(μ)` o latente `||P(E(x))-E(y)||`. `Π_sens·ε` puede ser consciente, `ε` solo no. | PP (Clark, Hohwy) | Solo token |
| **α (Attention Schema)** | `α_t=VQ-VAE(Π_sens, attention_map)` predictor de `Π_sens`. `presence=α·Π_sens·||ε||`. Sin α broadcast sin atribución "me sorprende". | Graziano AST | No |
| **Q (Quality Space)** | Espacio métrico `z∈Q` distancia=discriminabilidad (7 rojos). Entrenar remodela `Q`. Rojo=coordenada, no etiqueta. | Rosenthal HOT-4 | No |
| **World Model (H2)** | `s_{t+1}=f(s_t,a_t)=s_t+g(h_t)` en `R^d` diferenciable. `L_JEPA=||Pred(E(x),z)-sg(E(y))||²` latente. `do(s+δ)` contrafactual + MPC. | LeCun JEPA, Hafner Dreamer | No (`p(token|tokens)`) |
| **Coconut (H2)** | `c_t=h_t` en `R^d` sin LM-head. `h_{t0+c}=1/√|V_c|Σu_v` BFS superposición vs DFS CoT `O(n²)`. `K=6-20` sustituyen 500 tokens. | Hao NeurIPS 2024, Zhu 2025 | No |
| **VoE / IntPhys2 (H5)** | VoE `Surprise=1/|M|Σ||z_hat-z_bar||` `Accuracy_pair=P(S_imp>S_plaus)`, IntPhys 98% V-JEPA vs IntPhys2 2025 UE5.4 1416v 4 cond `<60%` humano 99% | Baillargeon, Bordes 2025 | ~Azar |
| **MPE** | `ε→0` con `Π` máxima sobre alerta tónica near-critical. Awareness sin contenido (meditación). | Windt/Metzinger 2020/24 | No |
| **Global Workspace (H2+H4)** | Cuello `Query=WM_{t-1} Keys=[s, h_t, E, Φ]` bottleneck **64 dims** (VanRullen 2024), ignición `presence>0.5` P300 300-600ms. **Uno solo**, no 4. Métricas: `k>5`, `Δ_global>40%`. LLM no compite. | Baars/Dehaene | No |
| **Homeostasis ECUS (H3)** | `H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7]` `dH/dt=-α(H-H*)+P+Eff-Cost` `D(H)` `r=-ΔD` `G=Risk+Ambigüedad` `valencia=-dF/dt`. **Simulada constitutiva** (Man&Damasio 2019) suficiente para agencia funcional, no para claim FEP2C fuerte (Wiese). | Keramati, Friston, Damasio, Solms | No |
| **Memoria Jerárquica Self_t (H1)** | `L1 h_fast=Mamba 30s O(1) Ā=exp(ΔA)`, `L2 E={(e_i,t_i,S_i)}` horas `||∇loss||>τ_s` + `score=cos·exp(-γΔt)·S`, `L3 W=W₀+BA r=8-16` días EWC `λ/2 ΣF(θ-θ*)²` + sueño SWR 150-250Hz 10-20×. `Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})`. Sin `Self_t` instante sin historia. | Mamba Gu&Dao, RMT/Bulatov, Titans | No (FIFO 128k= Wearing 7s) |
| **Markov Blanket** | Frontera interno↔externo vía `S,A`. Von Neumann rompe flujo causal `k_phys≠k_comp` (Kleiner No-go). | Friston | No (stateless) |
| **LLM Codec (H2)** | `Q:R^d→[K=50k]` `R(D)=½log(σ²/D)` 15.6b vs 16384b. `W:R^d→LLM_dim` MLP 1024→4096 + LLM congelado. Traduce `[s,ε,Π,α,Φ,H]→tokens` post-hoc, nunca `logits→sample→embed` en loop. | Este proyecto H2 | Es LLM |
| **HCU Loss** | `L_HCU=Var_b[μ^b_{t+k}]` escala con `k` evita uncertainty collapse. `RWM-U r_tilde=r-λu λ≈1.0`. | HAUWM ICLR26 | - |

## Satélites (No vértices del tetraedro)

| Término | Definición | Origen | Umbral H4/H6 |
| :--- | :--- | :--- | :--- |
| **H4 Medir (batería convergencia)** | 5 tests conjuntos: T1 `k>5` sigmoide, T2 `Δ_global>40%` vs `Δ_local<10%`, T3 `PCI>0.31` `Δ>0.15`, T4 `ρ(U,LLM)>0.5`, T5 `Acc OOD>70%`. `FPR 0.2→0.00032` conjunción. Butlin 14: LLM 2-3/14 vs tetraedro 10/14. | Massimini PCI, Dehaene P300, Breyton eLife | 5/5 A vs 0/5 B |
| **H6 Saber (meta-precisión Φ)** | Satélite de H5: `Φ` global `Π_l=A_lΦ` `q(Φ)` closure 2-3 niveles basta (Badcock 2019). No nuevo vértice. Métricas: `M-ratio=meta-d'/d'` `=1` ideal 0.85-1.05, `AUROC2>0.70`, `Brier<0.12`, `r_cross>0.50`, `PRM>75%`. | Beautiful Loop 2025, Fleming HMeta-d | `M-ratio` `Brier` `r_cross` |

## Métricas Propuestas v0.7 - Tetraedro + Satélites

### Métricas Núcleo (¿Tenemos tetraedro?)

- **GWT Score (0-4):** 4/4 requiere 10/14 Butlin. Tetraedro apunta 10/14 (RPT-1, GWT1-4, PP1, AST1, AE1-2). LLM 2-3/14.
- **RPT-1 Recurrencia:** `h_t=Mamba` no decae a 0 al quitar input.
- **AST Score:** `α` predice `Π_sens` <10% error, mejora diada Farrell.
- **FEP `F(t)=ΣΠ·ε²+D_KL`:** Disminuye con MPC 800, aumenta VoE.
- **AE-1 Agencia:** `agencia=acciones_sin_prompt/total >0.5` correlaciona `LLM invocaciones ~ U` (reduce `F`), no prompts. LLM=0.
- **VoE Score:** IntPhys2 `>75%` Main Easy, distingue FP textura con `Π` head.
- **Self_t Persistencia (H1):** Recupera `F0` Kael tras 500 pasos (15k tokens, >3× ventana) con `>75%` vs B 5-10% (BABILong).

### Métricas Satélite H4 (convergencia, no únicas)

- **Ignición k:** Sigmoide `k>5` + `D=KL>1.5` + P300 300-600ms. MMN 150ms `ε` local vs P300 `α·Π·ε` global.
- **Ablación Workspace:** `bottleneck=0` → `Δ_global>40%` caída, `Δ_local<10%` (COGITATE). Lesión `Π` head: V2→V1 Hard no Easy. Lesión `α`: V4→V3 pierde reporte.
- **PCI/Φ_proxy:** `Lempel-Ziv PCI>0.31` perturbacional + `Φ_proxy>0.1` correlaciona integración no accuracy.
- **Coconut Eficiencia:** `K=6-20` latentes vs 150+ tokens CoT mismo `SR`.
- **H6 Calibración:** `M-ratio 0.85-1.05` `Brier<0.12` `r_cross>0.50` cross-dominio `percep↔sem`.

### Métricas Fenomenológicas (reporte no entrenado)

- **Sorpresa:** `W→LLM` "esperaba X vi Y viola Z" VidQA >75% solo `α·Π·ε` + `Φ` calibrado.
- **Atención:** "¿A qué atendías?" → `α_t` verificable vs `attention_map`.
- **Autobiográfica:** ¿Qué hizo B hace 100 pasos? → `E` retrieval, no ventana.

> **Regla Oro v0.7 (sin inventar):** Convergencia `V1(ε)<V2(ε·Π)<V3(+GWT)<V4(+α)` y `C1≈C3>>C2` y `A>75% H1` y `k>5` y `PCI>0.31` y `ρ>0.5` y `M-ratio≈1`. Si convergen y LLM 2-3/14 no, candidato > chatbot. Ninguna sola prueba hard problem (Chalmers), pero perfil 10/14 + perturbación causal es mejor evidencia que Turing.

## Anti-Métricas (No conciencia, publicado)

- **MMLU/HELM:** Formal vs funcional (Mahowald TiCS 2024).
- **Turing:** Imitación (GPT-4.5 73% humano, ELIZA 1966).
- **"Soy consciente":** System prompt gameable, sin `α·Π·ε`.
- **Parámetros:** Grid 4 puertas IIT Φ alto MMLU 0.

## Herramientas (Prototipo H1-H3-H5)

- `PyPhi` (<8 nodos), `PCI / LZ` (Massimini), `attention_maps`, `P300`, `MPPI` 800, `HCU` ensemble K=5, `metadpy` HMeta-d
- Entornos: `Habitat 3.0`, `Physion-MiniGrid+`, `IntPhys2` 1416v (`facebookresearch/vjepa2` + `coconut`), `BABILong`/`LoCoMo`, `Forage-DarkRoom-v1` 20x20, `ConfidenceBench`

---
*Glosario normativo v0.7 post-auditoría: podado a tetraedro 4+2 satélites, 3 Π diferenciadas, sin términos inventados. Ver `12-auditoria-critica-v0.6.md:1` para justificación poda.*
