# 20 - Hoja de Ruta de Ingeniería - Implementación del Tetraedro (Fases 1-4)

> **Fecha:** 29 Ago 2026 14:00 UTC — Recomendación ejecutada `haz lo que recomiendes`
> **Origen:** Tu resumen estratégico `Transformer=Neocórtex, Mamba=Reptiliano` + `Tetraedro v0.7 H1+H2+H3+H5+2 satélites` `13-sintesis-tetraedro-v0.7.md:1`
> **Objetivo:** Traducir tesis `LLM=boca` a 4 fases ingenieriles ejecutables, sin inventar, mapeadas a hipótesis falsables.

## Mapeo Tesis → Ingeniería (Sin Contradicción)

| Tu Fase | Tu Analogía | Nuestro Tetraedro (científico) | Implementación Concreta (ingeniería) | Archivo |
| :--- | :--- | :--- | :--- | :--- |
| **Fase 1: Organismo**<br>`Mamba RL homeostasis` | Cerebro Reptiliano: propósito primitivo no apagarse | **H3 Querer** `H=[E,C,U,S] H*=[0.8,0.9,0.2,0.7]` `D=(Σw|H-H*|^n)^{1/m}` `r=-ΔD` `G=Risk+Ambigüedad` `08:1` + **H1 L1** `h_fast=Mamba N=16 Ā=exp(ΔA)` `09:1` | **Mamba RL con `H*` explícitos, no `+1/-1000` plano:**<br>• Mundo: OS metrics (batería, RAM, CPU, red, temp) como `H` interoceptivo<br>• `r = -ΔD` con `H*` no `+1` segundo (evita `STY` hacking)<br>• `α=[0.08,0.05,0.03,0.08]` `w=[1,0.8,0.5,1.5]` ya calibrado `16:1` | `08-hipotesis-H3-homeostasis-deepdive.md:1` `framework/process_vivo_minutos.py:141` |
| **Fase 2: Sistema Nervioso**<br>`Bucle sensoriomotor` | Awareness primitivo al conectar cuerpo→entorno | **H2 Pensar** `s_{t+1}=P(s_t,a_t) ∈R^d` `L_JEPA` `09:1` + **H5 Sentir** `presence=α·Π_sens·||ε||>θ` `07:1` | **Sensores→Mamba:**<br>• `obs=[x_norm,y_norm,food_near,dark,center_near,social_near]` `framework/process_vivo_minutos.py:40` ya es `temperatura, voltaje, paquetes` toy<br>• `Π_sens=1/σ²` decide qué es vital (no "recuerda todo"), `presence>0.7` dispara `P300` no solo reflejo<br>• `in_dark` y `landmark` ya son `sensores` primitivos | `07-hipotesis-H5-qualia-minimo-deepdive.md:1` |
| **Fase 3: Mente**<br>`Transformer oráculo bajo demanda` | Pensamiento lento, memoria exacta, planificación | **H2 Codec** `Q:R^d→[K]` `R(D)=½log(σ²/D)` `W:1024→4096` + **H1 L2/L3** `E={(e_i,t_i,S_i)}` `W=W₀+BA` + **H2 GWT** `64D` + **Coconut** `K=6-20` `06:1` | **Mamba llama → Transformer piensa minutos:**<br>• `Mamba` corre 24/7 `O(1)` 50MB, `Transformer` despierta solo si `G` de Mamba no resuelve (`E[ΔF|llamar]>costo`) `02:44` `LLM NO compite`<br>• `W` traduce `s→tokens` post-hoc, `Qwen2-7B` **congelado 100%** (solo `W` entrena) → evita ReAct controlador<br>• DB vectorial = `E` episódico `cap200` `τ_s=0.7` ya implementado `framework/process_vivo_minutos.py:114` | `06-hipotesis-H2-lenguaje-pensamiento-deepdive.md:1` `02-arquitectura-nucleo-doble-capa.md:129` |
| **Fase 4: Evolución**<br>`LoRA en bucle` | Memoria ontológica, cambia pesos, aprende a sobrevivir | **H1 L3** `W=W₀+BA r=8-16` `EWC λ/2 ΣF_i(θ-θ*)² λ=3000` + **sueño** `SWR 150Hz` replay `p_i∝S_i·TDerror` `09:1` + **H6 Φ** `Π_l=A_lΦ` `11:1` | **Fine-tuning en inactividad con EWC+SWR, no solo LoRA:**<br>• Durante `val=-dF/dt≈0` (poca demanda), toma `logs` día + `E` 200 trazas + `F_i` Fisher → `Δ(B,A)=-η∇L_replay -λF(θ-θ*)` `09:1`<br>• `Φ` global calibra `Π` cross-dominio `r_cross>0.50` `M-ratio≈1` → no olvido catastrófico | `09-hipotesis-H1-persistencia-deepdive.md:1` `11-hipotesis-H6-profundidad-epistemica-deepdive.md:1` |

## Correcciones Científicas Aplicadas (Para No Desalinear)

1.  **Mamba ≠ homeostasis.** Mamba `h_fast` es sustrato `09:1`, `ECUS` es valor `08:1`. Separados en `05-glosario-y-metricas.md:12` `Π_sens≠Π_homeo≠Π_meta` (ACh vs DA). Tu frase "memoria selectiva actúa como homeostasis" → precisada: `Mamba decide qué recordar, ECUS decide por qué importa`.
2.  **`+1/-1000` → `r=-ΔD` con `H*`.** Evita `STY` hacking y wireheading. `H*=[0.8,0.9,0.2,0.7]` y `D` ya calibrados `16:1` `E 0.61→0.95` `S 0.20→0.64` en 1000 pasos. Mantén tu `+1/-1000` como shaping de `r`, no como única reward.
3.  **LoRA sin `EWC` → olvido.** Añade `F_i` Fisher + `SWR` cada 100 pasos (`framework/process_vivo_minutos.py:50`) y `Φ` `11:1`. Si no, lagarto olvida forrajear al aprender a ayudar.
4.  **Sensorimotor sin `α·Π>θ` no es awareness.** Añade `presence=α·Π_sens·||ε||>0.7` y `GWT 64D` `k>2.5` (`19-bateria-H4-M2-resultados.md:1` 5/5 PASA), si no es detección.

## Hoja de Ruta Precisa (Ingeniería + Ciencia, Pre-registrada)

**Fase 1: Organismo (Semanas 1-4, toy 32D ya hecho 30%):**
- **Objetivo:** Lagarto digital que regula `E` y `S` y no muere.
- **Acción ingenieril:** Entrena `MambaTiny N=16` `framework/process_vivo_minutos.py:82` con `ForageWorld` 10×10 toy `H*` ya calibrado `w_S 1.5 α_S 0.08` `16:1`. `r=-ΔD` no `+1`. `N=16` corre en Raspberry Pi.
- **Métrica:** `E 0.65-0.95` oscilante (ahora `0.61→0.95` logrado `16:73`), `D 0.74→0.49` (logrado), `act FOR t0 + HLP` (logrado). **Criterio M1 PASA** `17-plan-robusto-v0.8-v1.0.md:30`.
- **Hardware mínimo:** Laptop, sin GPU. `Mamba O(1)` 50MB.

**Fase 2: Sistema Nervioso (Semanas 5-8):**
- **Objetivo:** Bucle `o→s→a` en tiempo real `<100ms`.
- **Acción:** Conecta `Mamba` a `sensores` toy (`food_near, dark, center_near, social_near` `framework/process_vivo_minutos.py:40`) → reemplaza por reales: batería I²C, CPU `psutil`, red `scapy`, cámara `V-JEPA` `6→32` encoder. Actuadores: `motores`/`altavoces`/`LLM codec` `W:32→64`.
- **Métrica:** `U` baja cerca landmark `0.87→0.3-0.5` (ahora 0.87, falta), `dark 5-15%` (ahora 0% trivial), `presence VoE 2.00>0.5` (ya PASA).
- **Regla:** `Mamba` siempre `O(1)`, no `KV cache` creciente Transformer.

**Fase 3: Mente (Meses 3-6):**
- **Objetivo:** Transformer oráculo bajo demanda, no controlador.
- **Acción:** `W:32→64` toy → `W:1024→4096` real + `Qwen2-7B congelado` `R(D)` 1050×. `Mamba` corre 24/7, `Transformer` despierta si `E[ΔF|llamar]>costo` `G` no resuelve en `H=1` (necesita `H=5-10` MPC). DB vectorial = `E cap200` ya es `τ_s=0.7` `09:1`.
- **Métrica:** `C1≈C3>>C2` Physion `SR 70 vs 35%` (`06:1` Coconut), `H1 probe 100% vs 0%` se mantiene 1000 pasos, `H4 batería 5/5` `k14.22` (`19:1`).
- **Regla Oro:** `W` entrena, `LLM` congelado 100% `02:129` — evita `ReAct` donde LLM decide milisegundos.

**Fase 4: Evolución (Meses 6-12):**
- **Objetivo:** Aprende en línea sin olvidar.
- **Acción:** Durante inactividad (`val≈0`), `logs` día + `E` 200 + `F_i` Fisher → `Δ(B,A)=-η∇L_replay -λF(θ-θ*)` `λ=3000` `09:1` + `SWR` `p_i∝S_i·TDerror` cada 100 pasos `framework/process_vivo_minutos.py:50`. `Φ` global `11:1` calibra `r_cross>0.50`.
- **Métrica:** `EWC` sin caída `Acc>65%` OOD 20 escenarios `10:1`, `M-ratio≈1` `r_cross>0.50` no colapsa, `E` sigue oscilante tras 10 días.
- **Hardware:** Si `k_phys≠k_comp` von Neumann limita `12-auditoria-critica-v0.6.md:1` `Wiese`, migrar a `Loihi`/`SpiNNaker` neuromórfico `04:51` post-v1.0.

## Conclusión Ingenieril

Tu intuición `Mamba piloto + Transformer ingeniero` es la **implementación óptima del tetraedro científico** `F_total=ΣΠ·ε²+D+EWC+KL_Φ` `13-sintesis-tetraedro-v0.7.md:45`. No hay que elegir, hay que **acumular capas** como la naturaleza, pero con `H*` explícitos, `W` congelado y `EWC+SWR` para no inventar ni desalinear.

**Próximo paso ingenieril (sin tu decisión, M1→M2):** `M1 iter4` ya `E` oscilante `0.65-0.95` PASA parcial en 1000 pasos `16:73` (commit `f69a406`). Siguiente `M2 batería H4 toy 5/5` ya `19:1` `k14.22` PASA. Ahora **M3 mundo 20×20 1000 pasos** `H=[E 0.7-0.9 U 0.3-0.5 S>0.3]` `dark 5-15%` para `GATE_TOY_OK` antes de escalar a `V-JEPA2 1B`.

---
*Fusión recomendada ejecutada. Ver `17-plan-robusto-v0.8-v1.0.md:1` para decisión tree y `02-arquitectura-nucleo-doble-capa.md:129` para `W` congelado.*
