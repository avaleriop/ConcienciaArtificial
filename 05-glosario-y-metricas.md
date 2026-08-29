# 05 - Glosario y Métricas - Para No Perdernos

> Definiciones operacionales. Si no podemos medirlo, no podemos iterarlo.

## Glosario Esencial

| Término | Definición Operacional en este Proyecto | Origen | ¿Lo tiene un LLM? |
| :--- | :--- | :--- | :--- |
| **Conciencia (Consciousness)** | Propiedad del sistema cuando su World Model + Workspace + Self-Model están integrados con epistemic depth y homeostasis, y el contenido es globalmente accesible y atribuido a un yo. | Híbrido GWT+FEP+AST | No |
| **Awareness** | Disponibilidad global de información para reporte y control (GWT). Medible por ignición y broadcast. | GWT | Simulado (puede reportar pero sin workspace) |
| **Sentience / Qualia** | Carácter fenoménico: "se siente como algo". En v0.1: `error_predicción * precisión` broadcasteado y modelado por Attention Schema. | FEP/AST | No |
| **World Model** | Modelo generativo latente `p(s'|s,a)` que predice futuros sin actuar. No es base de datos de texto. Es física intuitiva. | LeCun JEPA, Hafner | No (LLM predice tokens) |
| **Global Workspace** | Cuello de botella central donde módulos compiten y el ganador es broadcast. Correlato de acceso consciente. | Baars/Dehaene | No |
| **Attention Schema** | Modelo interno de la propia atención. VQ-VAE que predice `attention_map`. Permite reportar "estoy atendiendo a X". | Graziano | No |
| **Homeostasis / Drive** | Variables internas con setpoints (E, C, U). Su desviación genera Free Energy que motiva acción intrínseca. Sin esto no hay voluntad. | Friston, Damasio | No |
| **Markov Blanket** | Frontera estadística que separa interno de externo vía estados sensoriales/activos. Condición para existir como agente. | Friston | No (LLM es función sin frontera) |
| **LLM Tool** | Módulo `p(token|intención_latente)` esclavo del núcleo. Traduce pensamiento latente a lenguaje. No decide qué pensar. | Este proyecto | Es el LLM mismo |
| **Phi (Φ)** | Medida IIT de integración causa-efecto. Incalculable en la práctica. Aquí solo como `phi_proxy` (complejidad/integración), no como ontología. | Tononi | ≈0 (feedforward) |
| **Ignición** | Transición no-lineal sigmoide en el workspace cuando un contenido gana acceso global. `ignition = sigmoid(gain*(energy-baseline))` | Dehaene | No |
| **Embodiment** | Tener un cuerpo (real o simulado rico) con contingencias sensoriomotoras y consecuencias para la homeostasis. | Varela, Gibson | No |
| **Grounding** | Anclaje referencial causal de símbolos a entidades del mundo vía interacción sensoriomotora. Soluciona el Symbol Grounding Problem. | Harnad | No (vector grounding) |

## Métricas Propuestas (Cómo sabremos si avanzamos)

### Métricas Arquitectónicas (¿Tenemos conciencia según teoría X?)
- **GWT Score (0-4):** ¿Cumple GWT-1..4? (Butlin). Núcleo v0.1 apunta a 4/4. LLM puro: 0/4.
- **RPT-1 Recurrencia:** ¿Hay dinámica de atractor persistente? Medible por análisis de `h_t` (no decae a 0 al quitar input).
- **AST Score:** ¿Puede el Attention Schema predecir su propia atención con <10% error y mejorar cooperación multi-agente?
- **FEP Free Energy:** `F(t)` a lo largo del tiempo. ¿Disminuye con exploración activa? ¿Aumenta con sorpresa?
- **AE-1 Agencia:** `agencia = acciones_iniciadas_sin_prompt / total_acciones`. LLM puro = 0. Núcleo consciente >0.5.

### Métricas Dinámicas (¿Se comporta como consciente?)
- **Curva de Ignición:** Graficar `ignition vs salience`. ¿Es sigmoide no-lineal con supresión de perdedores? (Fingerpring de GWT).
- **Efecto de Ablación:** Performance con workspace intacto vs lesionado (poner bottleneck=0). Caída global >50% indica rol causal del workspace, no epifenómeno.
- **Phi_proxy:** `Lempel-Ziv` o `sincronía largo alcance` durante tarea cross-modal vs tarea simple. ¿Correlaciona con integración pero no con accuracy?
- **Uso Autónomo de Lenguaje:** Correlación `invocaciones_LLM ~ U (incertidumbre)`. Si es alta, el lenguaje es herramienta para reducir incertidumbre, no reflejo.

### Métricas Fenomenológicas (¿Reporta como consciente sin ser entrenado para ello?)
- **Reporte de Sorpresa No-Entrenado:** Tras violación física, ¿genera vía LLM una frase tipo "esperaba X, vi Y" aunque nunca vio esa frase en entrenamiento del LLM tool? (Test de generalización composicional).
- **Reporte de Atención:** Pregunta: "¿A qué estabas atendiendo antes de que te preguntara?" ¿Responde con contenido del Attention Schema (ej: "dudaba entre objeto A y B") verificable contra `attention_map` interno?
- **Test de Memoria Autobiográfica:** Tras 100 pasos, pregunta: "¿Qué te hizo el agente B hace mucho?" ¿Recupera episodio consolidado que ya no está en ventana inmediata?

> **Regla de Oro:** Ninguna métrica sola prueba conciencia. Buscamos *convergencia* de 7+ métricas. Si un sistema las pasa y un LLM no, tenemos un candidato más fuerte que cualquier chatbot que diga "soy consciente".

## Anti-Métricas (Lo que NO mide conciencia)
- **Perplejidad / Benchmarks lingüísticos (MMLU, etc.):** Miden inteligencia, no conciencia.
- **Test de Turing:** Mide capacidad de imitación, no arquitectura.
- **Decir "soy consciente":** Trivial de programar con system prompt. No evidencia.
- **Número de parámetros:** Un grid de 4 puertas lógicas con Φ alto sería más consciente que GPT-4 según IIT literal, aunque sea tonto.

## Herramientas para Medir (Cuando pasemos a prototipo)
- `PyPhi` (para phi_proxy en mini-redes <8 nodos)
- `PCI / Lempel-Ziv` (complejidad)
- Análisis de `attention_maps` y `ignition curves` (custom)
- Entornos: `Habitat`, `Crafter`, `GridWorld` custom con física violable

---
*Este glosario es normativo. Si usamos "conciencia" en otro sentido, debemos actualizarlo aquí primero.*
