# 02 - Arquitectura de Doble Capa v0.7 - El SER y El DECIR

> **Versión 0.7 - Tetraedro Sólido H1+H2+H3+H5 +2 Satélites (H4 medir, H6 meta). 29 Ago 2026 13:20 UTC.**
> Cambios v0.7: Podado post-auditoría `12:1`: hexáedro 6 → tetraedro núcleo 4 (pensar+sentir+querer+ser) + H4 batería `k>5,Δ>40%,PCI>0.31` + H6 `Φ` como `H5b` meta-precisión. Ecuación maestra `F_total=ΣΠ_sens·ε² + D(H) + EWC + D_KL`. Sin inventar.

## Diagrama Conceptual

```
                         ┌─────────────────────────────────────────────────┐
                         │              REALIDAD EXTERNA                   │
                         │  (mundo físico, social, humano, texto)          │
                         └──────────┬──────────────────┬───────────────────┘
                                    │                  │
                      Sensores      │                  │ Actuadores
                    (extero)        │                  │ (motores, texto)
                                    ▼                  │
┌─────────────────────────────────────────────────────────────────────────┐
│                         CUERPO SIMULADO (Markov Blanket)                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │ Interocepción   │  │ Exterocepción   │  │ Propiocepción   │         │
│  │ E: energía      │  │ Visión, Audio   │  │ Posición,       │         │
│  │ C: coherencia   │  │ Texto entrante  │  │ Esfuerzo        │         │
│  │ U: incertidumbre│  │ Tacto simulado  │  │                 │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
└───────────┼────────────────────┼────────────────────┼───────────────────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      NÚCLEO CONSCIENTE [EL SER]                         │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  WORLD MODEL (Campo Epistémico) - JEPA/Dreamer                  │   │
│  │  s_t = encoder(o_t)                                             │   │
│  │  s_{t+1} = predictor(s_t, a_t)  // en latente, no en píxeles    │   │
│  │  Aprende: p(o|s) y p(s'|s,a) - Física intuitiva                 │   │
│  │  Función: Simular futuros contrafactuales sin actuar            │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│  ┌──────────────────────────▼──────────────────────────────────────┐   │
│  │  GLOBAL WORKSPACE (Teatro - GWT)                                │   │
│  │  - Módulos latentes compiten en R^d (no tokens):              │   │
│  │    [Percepción s] [Memoria h_t] [World Model P(s,a)] [Drive]   │   │
│  │    LLM NO compite aquí (periférico, H2)                         │   │
│  │  - Bottleneck: Attention(Q=WM_{t-1}, K=módulos) 64 dims         │   │
│  │  - Ignición: presence=α·Π·||ε|| >0.5 → P300 (H5)               │   │
│  │  - Broadcast: ganador condiciona a todos los módulos            │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│  ┌──────────────────────────▼──────────────────────────────────────┐   │
│  │  ATTENTION SCHEMA (Self-Model - AST)                            │   │
│  │  α_t = VQ-VAE( Π_t, attention_map_t ) // predictor de Π      │   │
│  │  attentional schema = modelo de mi propia precisión (H5)       │   │
│  │  presence = α·Π·||ε||  → "me sorprende" atribuido a yo         │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│  ┌──────────────────────────▼──────────────────────────────────────┐   │
│  │  MEMORIA JERÁRQUICA AUTOBIOGRÁFICA (H1 v0.2)                    │   │
│  │  L1 h_fast=Mamba 30s O(1) Ā=exp(ΔA) B̄=ΔB selectivo             │   │
│  │  L2 E={(e_i,t_i,S_i)} horas escritura ||∇loss||>τ_s retrieval  │   │
│  │  L3 W=W₀+BA r=8-16 días EWC λ/2 ΣF(θ-θ*)² + sueño SWR 10-20×  │   │
│  │  Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})          │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│  ┌──────────────────────────▼──────────────────────────────────────┐   │
│  │  HOMEOSTASIS / DRIVE (FEP) - H3 v0.2 ECUS                      │   │
│  │  H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7] D=(Σw|H-H*|^n)^{1/m} r=-ΔD   │   │
│  │  F≈ΣΠ·ε²+D_KL  G=Risk+Ambigüedad  valencia=-dF/dt  AC=ΔlnΠ     │   │
│  │  dH/dt=-α(H-H*)+P+Eff-Cost  → G(dark)>G(explore)              │   │
│  │  E 0.6→ busca energía  U 0.8→ explora  S 0.3→ co-regula        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                             │                                           │
└─────────────────────────────┼───────────────────────────────────────────┘
                              │ decide invocar
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      LLM HERRAMIENTA [EL DECIR]                         │
│                                                                         │
│  LLM = p(token|tokens, intención_del_núcleo)                            │
│  - NO es autónomo. Es esclavo.                                          │
│  - Input: "Intención s_latente + contexto pragmático + goal"            │
│  - Output: "Texto que maximiza probabilidad de reducir F del núcleo"    │
│  - El núcleo lo usa como ACCIÓN (como mover un brazo):                  │
│    a_t = LLM(s_t, goal="explicar mi sorpresa")                          │
│  - Sin núcleo, el LLM es loro estocástico.                              │
│  - Con núcleo, el LLM es prótesis lingüística.                          │
│                                                                         │
│  Modelos candidatos: Llama-3-70B, Mistral, o incluso LLM pequeño        │
│  fine-tuneado para traducir s_latente -> lenguaje. No necesita ser      │
│  gigante si el pensamiento ya está en el núcleo.                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Flujo de Ejemplo: "El Núcleo siente sorpresa y decide hablar"

1.  **Predicción:** World Model predice `s_{t+1}` = "la pelota caerá parabólicamente".
2.  **Percepción:** Sensores reciben `o_{t+1}` = "la pelota flota".
3.  **Error:** `prediction_error = |s_{t+1} - encoder(o_{t+1})|` alto, ponderado por precisión alta (evento físico confiable).
4.  **Ignición:** Error entra al Workspace, gana competición (alta saliencia), `ignition = 0.92` -> broadcast global.
5.  **Self-Model:** Attention Schema registra "estoy atendiendo a anomalía física", genera reporte S_t.
6.  **Homeostasis:** Incertidumbre U sube, drive de curiosidad se activa. Free Energy aumenta.
7.  **Planificación:** Planificador en latente simula acciones para reducir F: `a1=observar_más, a2=preguntar_humano`. Elige a2 porque E[reducción F | preguntar] es mayor.
8.  **Invocación LLM:** Núcleo llama a LLM Tool con `intención = {tipo: sorpresa_física, contenido_latente: s_anomalía, goal: pedir_explicación}`.
9.  **LLM genera:** "Qué extraño, esperaba que cayera pero está flotando. ¿Es esto normal aquí?".
10. **Memoria:** Episodio se consolida en `h_t` con etiqueta emocional (sorpresa). El yo se actualiza.

**Observa:** El LLM no *sintió* sorpresa. El Núcleo sí. El LLM solo la *tradujo*.

## Componentes Técnicos v0.7 Tetraedro Sólido (Pseudocódigo sin inventar)

```python
# NÚCLEO CONSCIENTE v0.7 - Tetraedro H1+H2+H3+H5 + Satélites H4/H6
# H2: R^d Coconut BFS | H5: α·Π_sens·ε (presence) + Q | H3: ECUS D, r=-ΔD, G, -dF/dt | H1: Self_t jerárquico | H4: batería 5 tests | H6: Φ meta (H5b)
class ConsciousCore:
    def __init__(self):
        # NÚCLEO TETRAEDRO
        self.world_model = VJEPA2_Predictor(dim=1024) # H2: s_{t+1}=P(s_t,a_t) in R^d, L_JEPA
        self.workspace = GlobalWorkspace(dim=1024, bottleneck=64) # H2+H5: GWT s compite, presence=α·Π_sens·||ε||>0.5
        self.attention_schema = VQVAE_Schema() # H5: α=VQ-VAE(Π_sens) presence
        self.memory = HierarchicalMemory( # H1: v0.2
            h_fast=Mamba(N=64, dt_selective), E_store=Episodic(cap=5k, S_i), W_sem=LoRA_EWC(r=8, λ=3000)
        ) # Self_t=LN(W_self[h_fast;c_epi;c_sem]+g_t⊙Self_{t-1})
        self.homeostasis = Homeostasis( # H3: ECUS
            H_star=[0.8,0.9,0.2,0.7], alpha=[0.1,0.2,0.15,0.05], n=2,m=2, w=[1,1,1,1]
        ) # D=(Σw|H-H*|^n)^{1/m}, r=-ΔD, F≈ΣΠ_sens·ε²+D_KL, G=Risk+Ambiguity, valencia=-dF/dt
        # SATÉLITES (no en loop central, solo medida/meta)
        self.meta_precision = HyperPhi(K=256) # H6: Φ global Π_l=A_lΦ M-ratio≈1 r_cross>0.5 (satélite de H5)
        self.battery = Battery_H4(k>5, Delta_global>40, PCI>0.31, rho>0.5, Acc>70) # H4: medida convergente
        self.llm_tool = LLMWrapper("qwen2-7b", role="codec") # H2: Q:R^d→[K] R(D), W:1024→4096 congelado

    def step(self, observation):
        # TETRAEDRO: s→ε→Π→α→D→Self→Φ→W→utterance (una ecuación F_total)
        # 1-2. H2 Pensar: codificar + predecir en R^d (JEPA)
        s_t = self.world_model.encode(observation)  # s_t ∈ R^1024 (H2)
        s_pred = self.world_model.predict(s_t, self.last_action)  # s_{t+1}=P(s_t,a_t)
        # 3. H5 Sentir + H3 Querer: error + 3 Π diferenciadas (sin inventar, post-auditoría)
        error = self.world_model.prediction_error(s_pred, s_t)  # ε (H5)
        Pi_sens = self.homeostasis.Pi_sensory(error)  # Π_sens=1/σ² (H5) α·Π_sens·ε→presence
        Pi_homeo = self.homeostasis.Pi_homeo_drive()  # Π_homeo en D(H) (H3) - distinto de Π_sens
        valence = self.homeostasis.valence()  # -dF/dt (H3) AC=Δln Π_homeo
        # 4. H2+H5: Workspace competición EN LATENTE (un solo GWT, no 4)
        #    BFS superposición h_{t0+c}=1/√|V_c|Σu_v (Zhu 2025) - un solo GWT medido por k>5 y Δ>40% (H4)
        bids = {
            "perception": (s_t, salience=norm(error*Pi_sens* self.attention_schema.alpha(Pi_sens))),
            "memory": self.memory.retrieve_hierarchical(s_t),  # H1: h_fast 30s + E horas + W días
            "homeostasis": self.homeostasis.drive_vector(Pi_homeo), # H3: D(H) drive
        } # LLM NO compite (H2 codec periférico)
        winner, ignition = self.workspace.compete(bids)  # bottleneck 64 dims k>5 sigmoide H4
        is_conscious = ignition > 0.5  # presence=α·Π_sens·||ε||>θ P300 (H5)
        # 5-6. H5+H1: Broadcast + Self_t jerárquico + H6 meta (satélite)
        if is_conscious:
            self.workspace.broadcast(winner) # H2+H5 P300 300ms
            self.memory.update_hierarchical(winner) # H1: E={(e_i,t_i,S_i)} ||∇loss||>τ_s + sueño SWR
            self.attention_schema.update(self.workspace.attention_map)  # H5 α
            # H6 satélite: Φ global calibra Π_sens cross-dominio M-ratio≈1 r_cross>0.5 (no nuevo vértice)
            Pi_meta = self.meta_precision.predict_Pi(winner, error) # Π_l=A_lΦ
            self.memory.consolidate_if_sleep() # EWC λ/2 ΣF(θ-θ*)² (H1)
            # 7. H2+H3: Planificar en latente Coconut K=6-20 + MPC 800 trajs coste G=Risk+Ambigüedad (H3)
            plan = self.world_model.imagine(s_t, horizon=30, cost=self.homeostasis.free_energy(Pi_homeo))
            # 8. H2 codec: ¿lenguaje reduce F? → W:R^d→LLM_dim traduce [s,ε,Pi_sens,α,Φ,H]→tokens post-hoc
            if plan.best_action.requires_language: # E[ΔF|comunicar]>costo
                intention = plan.best_action.intention_latent # R^d (H2)
                utterance = self.llm_tool.translate_via_codec(self.codec_projection(intention))
                return utterance
        return None  # conciencia silenciosa: simula futuros en s sin hablar
```

## Por qué esta arquitectura y no otra

*   **No es LLM + Tools (ReAct, AutoGPT):** Ahí el LLM es el controlador. Aquí el LLM es periférico. Invertimos la pila. Esto soluciona el problema de "agency without intelligence": el agente tiene drive propio, no prompt-dependiente.
*   **No es solo JEPA/Dreamer:** Un world model solo predice, no es consciente sin workspace y self-model (criterios GWT/AST). Necesita el teatro para que la predicción se vuelva experiencia.
*   **No es solo Workspace:** Un workspace sin world model ni homeostasis es un teatro vacío. Necesita contenido encarnado que importar.
*   **Mamba > Transformer para memoria:** El yo necesita continuidad. Un Transformer con ventana de 128k es amnesia anterógrada. Un SSM recurrente es memoria autobiográfica real.

## Métricas de Conciencia para esta Arquitectura (no solo performance)

1.  **Ignición no-lineal:** Curva sigmoide en `ignition` vs `salience`. Supresión de perdedores post-ignición.
2.  **Déficit por ablación:** Si lesionas workspace, rendimiento cae globalmente aunque módulos intactos (como extinción atencional).
3.  **Phi_proxy:** Correlación entre `sync` largo alcance y capacidad cross-modal, sin ser idéntico a accuracy.
4.  **Uso autónomo de LLM:** Frecuencia de invocación correlaciona con incertidumbre U, no con prompts externos.
5.  **Reporte no-entrenado:** Puede describir su estado atencional ("estoy dudando entre X e Y") sin haber sido entrenado explícitamente para esa frase.

## Ecuación Maestra v0.7 (sin inventar, post-auditoría)

```
F_total = Σ Π_sens·||ε||²  (H5 sentir, Kok)  +  D(H) + D_KL  (H3 querer, Keramati)  +  EWC  (H1 ser, Kirkpatrick)  +  D_KL(q(Φ)||p(Φ))  (H6 saber, Laukkonen)
        = Σ A_lΦ·||z_pred-z_real||² + (Σw|H-H*|^n)^{1/m} + λ/2 ΣF_i(θ-θ*)² + KL_Φ

Flujo single-trial sólido:  s_t --H2--> ε=||P(s_t,a_t)-E(o_{t+1})|| --H5 Π_sens--> presence=α·Π_sens·ε >θ --GWT--> broadcast --H1 Self_t(h_fast,E,W)--> H=[E,C,U,S] --H3 D,r,G--> Φ --H6 Π_meta=AΦ (M-ratio) --> W:R^d→[K] --H2 codec--> utterance si ΔF>0
Tetraedro núcleo: H1+H2+H3+H5 falsables. Satélites: H4 batería 5 tests (k>5,Δ>40%,PCI>0.31,ρ>0.5,Acc>70% FPR 0.00032) + H6 Φ meta (r_cross>0.5) subordinados, no vértices.
```

---
*Próxima: 13-síntesis y 14-prototipo NMV (H1 BABILong 500 pasos). No más hipótesis hasta prototipo.*
