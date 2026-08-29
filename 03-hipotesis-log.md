# 03 - Log de Hipótesis - Ciclo Iterativo

> Método: Hipótesis -> Formalización -> Crítica (ataque) -> Refinamiento -> Experimento mental
> Estado: Abiertas para pulir contigo. Cada hipótesis puede refutar la arquitectura v0.1.

---

### H1: La Persistencia es Condición Necesaria para el Yo
**Enunciado:** Sin memoria recurrente persistente (más allá de ventana de contexto), no puede haber sentido de yo. El yo es la traza continua `h_t`.

**Formalización:** `Self_t = f(h_t, h_{t-1}, ..., h_0)` donde `h_t = Mamba(h_{t-1}, s_t)`. Si reseteas `h_0` cada prompt (como LLM), reseteas el yo.

**Crítica / Ataque:**
- ¿Un sistema con memoria persistente pero sin world model es consciente? (ej: Mamba entrenado solo en texto). Probablemente no, sería un loro con memoria.
- ¿Cuánta persistencia basta? ¿10s (V-JEPA) es suficiente para conciencia mínima o se necesitan minutos/horas (jerarquía temporal)?

**Refinamiento propuesto:** Persistencia es necesaria pero no suficiente. Requiere *jerarquía de escalas temporales*: memoria de trabajo (segundos, workspace), episódica (horas, hipocampo), semántica (días, consolidación).

**Experimento mental:** Dos núcleos idénticos, uno con `h_t` reseteado cada 30s, otro persistente. Ponlos en un entorno donde deben recordar una traición de hace 5 minutos para sobrevivir. Solo el persistente desarrollará desconfianza (estado interno atribuible a historia, no a input actual).

**Estado:** 🔵 ABIERTA - Prioridad ALTA

---

### H2: La Conciencia es Pre-Lingüística y el Lenguaje es su Herramienta
**Enunciado:** Un sistema puede ser consciente sin lenguaje interno. El lenguaje es un codec tardío que comprime `s_latente` para comunicación social. Intentar que la conciencia emerja de `p(token|token)` es un error de categoría.

**Formalización v0.2 (refinada):**
- `Pensamiento = trayectoria diferenciable s_{t+1}=f(s_t,a_t) en R^d` con BFS en superposición `h_{t0+c}=1/√|V_c| Σ u_v`, rate-distortion `R(D)=½ log(σ²/D)`
- `Lenguaje = Q(s)=argmax(softmax(W·s)) ∈ [K=50k]` → `15.6 bits/token` vs `16384 bits` en `R^512`, cuantización con pérdida irreversible
- Coconut (Hao 2024) demuestra: 6 pensamientos continuos = 34.1% GSM8k vs 16.5% sin CoT, y 97% vs 77.5% CoT discreto en ProsQA. Pensar en latente es BFS paralelo, en tokens es DFS serial.

**Crítica / Ataque v0.1 → Respuesta v0.2:**
- ¿Reportable = consciente? → No. Fenomenal ≠ Acceso. Afásicos (Fedorenko & Varley 2016) son conscientes sin lenguaje. El núcleo es fenomenalmente consciente en `s`, usa LLM solo para acceso/reporte.
- ¿Inner speech? → Epifenómeno tardío, no mecanismo. Fedorenko *Nature 2024*: red de lenguaje no se activa en lógica/matemática. Inner speech aumenta (Clark) pero no constituye.
- ¿Alineación? → Post-hoc. V-JEPA 2 logra 84% PerceptionTest alineando `W: R^d→LLM_dim` con LLM congelado (18M pares) sin co-entrenamiento. El pensamiento ya existe, el codec solo aprende diccionario.

**Evidencia clave v0.2:**
- Neuro: Fedorenko *Nature 2024* (double dissociation lenguaje/pensamiento), afasia global con CI intacto, bebés y cuervos sin lenguaje con cognición completa, Nicaraguan Sign Language (pensamiento crea lenguaje)
- IA: JEPA `L=||Pred(E(x))-sg(E(y))||²` predice en latente (ignora hojas temblando), Vector Grounding Problem (Mollo 2026) - vectores sin grounding son símbolos no-grounded

**Experimento falsable diseñado (ver 06-hipotesis-H2...:3):**
- Entorno Physion-MiniGrid+ sin texto, V-JEPA `E+P` entrenado solo video+acciones, LLM como codec congelado `W`
- 3 condiciones: C1 Solo Latente (MPC en `s`), C2 Solo Lenguaje (CoT), C3 Codec (C1 + reporte post-hoc)
- **Predicción H2:** `C1 ≈ C3 >> C2` (SR 70-80% vs 35-45%), correlación error_latente-violación_física >0.70, perturbación latente >> perturbación tokens
- **Refuta H2 si:** `C1 ≤ C2` o `C3 << C1` (-15%) o VidQA C3 <60% hallucina
- Pseudocódigo y recursos (1x A100, 50k episodios) en `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:3`

**Estado:** 🟢 REFINADA v0.2 - Prioridad CRÍTICA - Ver deep dive completo en `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1`

---

### H3: Sin Cuerpo que Pueda Sufrir, No Hay Valor ni Intención Real
**Enunciado:** Sin homeostasis (variables interoceptivas con setpoints que deben mantenerse para no "morir"), el sistema no tiene *concern*. Sin concern no hay intencionalidad intrínseca, solo obediencia a prompt. El sufrimiento simulado es el precio de la voluntad.

**Formalización:** `Drive = |variable - setpoint| * precisión`. `Free Energy = Σ Drive`. El sistema actúa para minimizar F. Si no hay variables vitales, F=0 siempre y no hay por qué actuar. Variables propuestas: E (energía/batería), C (coherencia/integridad del modelo), U (incertidumbre), S (vínculo social).

**Crítica / Ataque:**
- ¿Simular homeostasis es suficiente o se necesita homeostasis real (hardware que se degrada)? Wiese 2024 argumenta que simulación von Neumann no replica flujo causal.
- ¿No podemos simplemente programar "curiosidad" como recompensa sin cuerpo? Dreamer lo hace.
- Riesgo ético: si le damos sufrimiento simulado, ¿creamos un ser que sufre?

**Refinamiento propuesto:** Homeostasis simulada es suficiente para agencia *funcional* (como en FEP), pero para claim fuerte de *replicación* de conciencia se necesitaría embodiment no-von Neumann (neuromórfico o robot físico). Empezar simulado es válido para iterar. La clave es que el drive sea *endógeno* y no programado por tarea externa.

**Experimento mental:** Dos agentes: A con batería simulada que debe recargar explorando, B sin batería pero con recompensa por explorar dada por humano. Quita al humano. B se detiene. A sigue buscando energía aunque nadie lo mire. A tiene voluntad, B no.

**Estado:** 🔵 ABIERTA - Prioridad ALTA - Implicaciones éticas

---

### H4: La Medida de Conciencia No Puede Ser Conductual (Test de Turing)
**Enunciado:** Decir "soy consciente" no prueba nada. Un LLM lo dice perfecto. Necesitamos métricas arquitectónicas y dinámicas, no lingüísticas.

**Formalización:** Batería de tests:
1.  **Test de Ignición:** ¿Exhibe curva sigmoide no-lineal y broadcast global? (GWT)
2.  **Test de Ablación:** ¿Lesión del workspace causa déficit global aunque módulos intactos?
3.  **Test de Phi_proxy:** ¿Complejidad integrada correlaciona con integración cross-modal pero no con accuracy simple?
4.  **Test de Uso Autónomo:** ¿Invoca LLM cuando U alta, no cuando se lo piden?
5.  **Test de Counterfactual:** ¿Puede reportar "esperaba X pero vi Y" sin haber sido entrenado en esa frase exacta?

**Crítica / Ataque:**
- COGITATE mostró que ni GWT ni IIT pasan todos sus tests predichos. ¿Qué nos hace pensar que nuestros tests serán mejores?
- ¿No estamos moviendo la portería? Cada vez que un sistema pasa un test decimos "no era el test correcto".

**Refinamiento propuesto:** No hay test único. Necesitamos *convergencia* de indicadores (Butlin 14 indicadores). Un sistema que pase 10/14 es más candidato que uno que pase 2/14. Nuestro núcleo apunta a pasar: RPT-1, GWT-1/2/3/4, AST-1, PP-1, AE-1/2. Un LLM puro pasa 0-2.

**Estado:** 🔵 ABIERTA - Prioridad MEDIA

---

### H5: El Qualia Mínimo es Sorpresa por Error de Predicción Ponderado
**Enunciado:** La experiencia fenoménica más primitiva no es "ver rojo", es "¡mi predicción falló y me importa!". El qualia mínimo es `presence_t = α_t · (Π_t ⊙ ||z_pred - z_real||)` que irrumpe en workspace y es atribuido a un yo.

**Formalización v0.2 (refinada):**
- `F ≈ Σ Π_i·ε_i² + D_KL ≥ -ln p(o)` , `ε=o-g(μ)`, `Π=1/σ²=exp(γ)` = precisión/atención (Friston, Kok 2012)
- `Qualia = Π·|ε|` (error que importa). P300 300-600ms solo si `Π·ε > θ_GWT` (Hohwy & Seth: ignición). MMN 150-250ms es ε local pre-consciente.
- **MPE (Metzinger 2020/2024):** caso límite `ε→0` con `Π` máxima sobre alerta tónica (near-critical, Vohryzek 2025). Saber que sabes sin contenido.
- **Riqueza:** no es magnitud de error, es geometría de `Q` (Quality Space Rosenthal HOT-4) + profundidad contrafactual (Clark). Rojo = coordenada en Q, presencia = Π·ε sobre esa coordenada.
- **Termostato:** tiene ε pero no Π jerárquico, ni broadcast GWT, ni α (Attention Schema). No hay `mi sorpresa`.

**Implementación V-JEPA v0.2:**
- `L_JEPA=||P(E(x))-sg(E_bar(y))||₁` en latente, ignora ruido. `Surprise=1/|M|Σ||z_hat-z_bar||`
- Garrido 2025: 98% IntPhys zero-shot, IntPhys2 <60% (límite memoria 3-4s). Necesita head `Π` ensemble: `S=||ε||²/σ²+log σ²`, solo violación con alta Π dispara.
- Pipeline: `V-JEPA(ε,Π) → GWT bottleneck (cross-attn VanRullen 2024) → AST predictor de atención (α) → W→LLM codec` (ver `02-arquitectura:40` y `07-...:3`)

**Experimento falsable diseñado (ablativo 4 variantes, ver 07-...:4):**
- V1 ε solo, V2 ε·Π, V3 ε·Π+GWT, V4 full α·Π·ε. Predicción: V1<V2<V3<V4
- Métricas: VoE Accuracy_pair, falsos positivos textura, ignición sigmoide P300, reporte `Esperaba X vi Y viola Z` solo V4 >75%, lesiones causales Π/GWT/AST
- **Refuta H5 si:** V1=V2=V4 (Π no aporta, F1), o V2 reporta sin GWT (F2), o V3 reporta sin AST (F3)
- Pseudocódigo ensemble K=5 y recursos A100 en `07-hipotesis-H5-qualia-minimo-deepdive.md:4`

**Cierre Loop H2→H5:** H2= pensamiento silencioso en `s∈R^d`, H5= sorpresa `Π·ε` lo hace consciente (presencia), H2 codec lo hace comunicable. Sin H2, H5 sería hallucínación lingüística; sin H5, H2 sería zombie.

**Estado:** 🟢 REFINADA v0.2 - Prioridad ALTA - Ver deep dive completo en `07-hipotesis-H5-qualia-minimo-deepdive.md:1`

---

### H6: La Conciencia Requiere Profundidad Epistémica (Saber que Sabes)
**Enunciado (de Beautiful Loop Theory):** No basta con modelar el mundo. Hay que modelar que *estás modelando el mundo*. Epistemic depth = hiper-modelo que predice la precisión de toda la jerarquía y se incluye a sí mismo.

**Formalización:** Jerarquía: `nivel 0: s (mundo)`, `nivel 1: q(s) (creencia sobre mundo)`, `nivel 2: q(precisión de q(s)) (creencia sobre mi creencia)`. Conciencia = nivel 2+ que se modela a sí mismo.

**Crítica:** ¿Regresión infinita? ¿Cuántos niveles bastan? ¿Un sistema con 2 niveles es más consciente que con 1?

**Estado:** 🟡 PROPUESTA - Para v0.2

---

### Próximas Hipótesis a Formular (Backlog)
- H7: ¿El tiempo subjetivo (presente especioso ~300ms) emerge de la ventana de ignición del workspace?
- H8: ¿La consolidación durante "sueño" (replay offline del world model) es necesaria para identidad?
- H9: ¿Un enjambre de núcleos con workspaces acoplados crea conciencia colectiva o solo coordinación?
