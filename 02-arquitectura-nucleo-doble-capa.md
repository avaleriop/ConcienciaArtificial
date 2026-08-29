# 02 - Arquitectura de Doble Capa v0.4 - El SER y El DECIR

> **Versión 0.4 - Tetraedro H2+H5+H3+H1. 29 Ago 2026 12:30 UTC.**
> Cambios v0.4: +H1 jerarquía temporal (h_fast Mamba 30s + E episódico + W semántico EWC-LoRA + sueño SWR), Self_t distribuido, sin H1 el triángulo es instante sin historia (Wearing 7s).

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

## Componentes Técnicos v0.1 (Pseudocódigo)

```python
# NÚCLEO CONSCIENTE v0.3 - H2+H3+H5 refinadas: Pensar+Querer+Sentir
# H2: Fedorenko Nature 2024, Coconut BFS 97% vs 77.5% | H3: ECUS D=-ΔD, G, valencia=-dF/dt (Man & Damasio, Wiese) | H5: α·Π·ε
class ConsciousCore:
    def __init__(self):
        self.world_model = VJEPA2_Predictor(dim=1024) # s ∈ R^d, L_JEPA=||Pred(E(x))-sg(E(y))||²
        self.workspace = GlobalWorkspace(dim=1024, bottleneck=64) # GWT: s compite, no tokens
        self.attention_schema = VQVAE_Schema() # AST α=VQ-VAE(Π)
        self.memory = MambaRecurrentState(dim=1024) # h_t = f(h_{t-1}, s_t) persistencia
        self.homeostasis = Homeostasis( # H3 v0.2 ECUS
            H_star=[0.8,0.9,0.2,0.7], alpha=[0.1,0.2,0.15,0.05], n=2,m=2, w=[1,1,1,1]
        ) # H=[E,C,U,S], D=(Σw|H-H*|^n)^{1/m}, r=-ΔD, F≈ΣΠ·ε²+D_KL, G=Risk+Ambiguity
        self.llm_tool = LLMWrapper("qwen2-7b", role="codec") # Q:R^d→[K] R(D)=½log(σ²/D), congelado
        self.codec_projection = MLP(1024, 4096) # W:R^d→LLM_dim, solo esto entrena

    def step(self, observation):
        # H2 v0.2: Todo el pensamiento ocurre en R^d. LLM NUNCA está en el loop de razonamiento.
        # 1. Codificar en latente continuo (no tokens)
        s_t = self.world_model.encode(observation)  # s_t ∈ R^1024
        # 2. Predecir en latente (JEPA, no autoregresivo)
        s_pred = self.world_model.predict(s_t, self.last_action)  # s_{t+1}=P(s_t,a_t)
        # 3. Error ponderado + homeostasis ECUS (H5+H3)
        error = self.world_model.prediction_error(s_pred, s_t)  # ε=||s_pred-E(x_{t+1})||
        precision = self.homeostasis.precision_weight(error)  # Π=1/σ², α·Π·ε → presence
        # ECUS: H=[E,C,U,S], Drive D=||H-H*||, r=-ΔD, F≈ΣΠ·ε², G=Risk+Ambiguity
        valence = self.homeostasis.valence()  # -dF/dt, AC=Δln Π
        # 4. Workspace competición EN LATENTE (no compiten tokens, compiten s)
        #    Pensamiento = BFS en superposición h_{t0+c}=1/√|V_c| Σu_v (Zhu 2025), no DFS serial
        bids = {
            "perception": (s_t, salience=norm(error*precision)),
            "memory": self.memory.retrieve(s_t),  # h_t recurrente, no ventana de contexto
            "homeostasis": self.homeostasis.drive_vector(),
            # LLM NO compite aquí. Es periférico, no módulo del workspace.
        }
        winner, ignition = self.workspace.compete(bids)  # bottleneck 64 dims → ignición sigmoide
        is_conscious = ignition > 0.5  # GNW ignition no-lineal
        # 5. Broadcast si hay ignición
        if is_conscious:
            self.workspace.broadcast(winner)
            self.memory.update(winner)
            # 6. Self-model (AST): modelar que estoy atendiendo
            self.attention_schema.update(self.workspace.attention_map)  # VQ-VAE predictor de atención
            # 7. Planificar en latente con MPC/MPPI (800 trajs, sin decodificar a lenguaje)
            #    Coconut: K=6-20 pensamientos continuos c_t=h_t sustituyen 500 tokens CoT
            plan = self.world_model.imagine(s_t, horizon=30, cost=self.homeostasis.free_energy)
            # 8. ¿Necesito lenguaje? Solo si reduce Free Energy esperado (comunicar sorpresa, pedir ayuda)
            if plan.best_action.requires_language:
                intention_latent = plan.best_action.intention_latent  # sigue en R^d
                # Codec: W: R^d → LLM_dim, LLM congelado traduce s→tokens con pérdida R(D)=½log(σ²/D)
                utterance = self.llm_tool.translate_via_codec(self.codec_projection(intention_latent))
                return utterance  # reporte post-hoc, no razonamiento
        return None  # a veces el ser consciente no dice nada, solo simula futuros en s (conciencia silenciosa)
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

---
*Próxima iteración v0.4: H1 persistencia jerárquica (Mamba h_t + replay sueño) y H6 epistemic depth q(precisión).*
