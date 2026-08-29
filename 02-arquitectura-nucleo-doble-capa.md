# 02 - Arquitectura de Doble Capa v0.2 - El SER y El DECIR

> **Versión 0.2 - H2+H5 refinadas. 29 Ago 2026.**
> Cambios v0.2: Pensamiento en R^d con BFS latente (Coconut), qualia=α·Π·ε con ignición GWT, LLM relegado a codec periférico.

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
│  │  MEMORIA AUTOBIOGRÁFICA (Mamba/RSSM)                            │   │
│  │  h_t = f(h_{t-1}, z_t, a_{t-1}) // estado recurrente persistente│   │
│  │  No es ventana de contexto. Es consolidación lenta, reconsoli- │   │
│  │  dación, olvido. Identidad narrativa.                           │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│  ┌──────────────────────────▼──────────────────────────────────────┐   │
│  │  HOMEOSTASIS / DRIVE (FEP)                                      │   │
│  │  Variables con setpoints: E*, C*, U*                            │   │
│  │  F ≈ Σ Π·ε² + D_KL ,  Π=1/σ²,  presence=α·Π·||ε|| (H5 v0.2)    │   │
│  │  Error interoceptivo ponderado → Drive si α·Π·ε > θ_GWT        │   │
│  │  Si E < E* -> busca energía (curiosidad, recurso)              │   │
│  │  Si U alta -> explora / pregunta (usa LLM codec)               │   │
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
# NÚCLEO CONSCIENTE v0.2 - H2 refinada: Pensamiento en R^d, LLM solo codec
# Evidencia: Fedorenko Nature 2024 (lenguaje≠pensamiento), Coconut (BFS latente 97% vs 77.5% CoT)
class ConsciousCore:
    def __init__(self):
        self.world_model = VJEPA2_Predictor(dim=1024) # s ∈ R^d continuo, L_JEPA=||Pred(E(x))-sg(E(y))||²
        self.workspace = GlobalWorkspace(dim=1024, bottleneck=64) # GWT: s compite, no tokens
        self.attention_schema = VQVAE_Schema() # AST
        self.memory = MambaRecurrentState(dim=1024) # h_t = f(h_{t-1}, s_t) persistencia
        self.homeostasis = Homeostasis(setpoints={"E":0.8, "C":0.9, "U":0.2})
        self.llm_tool = LLMWrapper("qwen2-7b", role="codec") # Q: R^d → [K=50k], 15.6 bits/token, congelado
        self.codec_projection = MLP(1024, 4096) # W: R^d → LLM_dim, solo esto entrena en Fase 2

    def step(self, observation):
        # H2 v0.2: Todo el pensamiento ocurre en R^d. LLM NUNCA está en el loop de razonamiento.
        # 1. Codificar en latente continuo (no tokens)
        s_t = self.world_model.encode(observation)  # s_t ∈ R^1024
        # 2. Predecir en latente (JEPA, no autoregresivo)
        s_pred = self.world_model.predict(s_t, self.last_action)  # s_{t+1}=P(s_t,a_t)
        # 3. Error de predicción * precisión = sorpresa (H5, qualia mínimo)
        error = self.world_model.prediction_error(s_pred, s_t)  # ||s_pred - E(x_{t+1})||²
        precision = self.homeostasis.precision_weight(error)  # atención = ganancia de precisión (FEP)
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
*Próxima iteración v0.2: Definir matemáticamente Free Energy y setpoints homeostáticos.*
