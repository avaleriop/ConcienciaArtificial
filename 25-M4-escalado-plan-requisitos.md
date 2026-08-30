# 25 - M4 Escalado Real - Plan, Requisitos y Estado Honesto

> **Fecha:** 29 Ago 2026 14:35 UTC - M4 pre-registrado `17-plan-robusto-v0.8-v1.0.md:1` (GATE_TOY_OK PASA `24:1`)
> **Estado real:** Scaffold listo (`framework/m4_escalado_real.py`), ejecución bloqueada por hardware (honesto).

## Requisitos M4 (verificados en máquina)

| Recurso | Necesario | Disponible ahora | Diferencia |
| :--- | :--- | :--- | :--- |
| GPU | 1× A100 40GB (o 2× A10 24GB) | ❌ M4 Pro, torch 2.9.1 CUDA=False (solo MPS) | Requiere cloud ~15€/día |
| V-JEPA2 ViT-L 1B | pesos facebookresearch/vjepa2 (1M horas video) | ❌ no descargados | ~4GB disco, A100 para encoder 16f 224² |
| Qwen2-7B codec | HF Qwen/Qwen2-7B, congelado 100% | ❌ no descargado | ~14GB BF16 |
| Datos | Physion/IntPhys2 1416v UE5.4 + Habitat 3.0 | ❌ | procedimental |
| Tiempo | 24h simulado 10Hz = 864k pasos ≈ 30h A100 | ❌ | coste |

**Conclusión honesta:** M4 no puede ejecutarse en esta máquina. Scaffold define el flujo pre-registrado (`framework/m4_escalado_real.py:1`), espera GPU. No fingiremos ejecución en CPU (violaría criterio verificable `13:9`).

## Flujo M4 pre-registrado (lo que se ejecutará con GPU)

```
MUNDO (Habitat 3.0 / Physion) → V-JEPA2 E(x) CONGELADO R^1024
  → predictor 384 + ensemble K=5 Π_sens (HCU Var_b[μ] evita collapse)
  → ε = ||P(s,a) - E(o')||, presence = α·Π·ε
  → GWT 64D (Q=WM_{t-1}, k>5, Δ>40%, PCI>0.31 reales)
  → Self_t: Mamba N=64 Δ-selectivo + E 5k τ_s=0.7 + W=W₀+BA r=16 EWC λ=3000 + sueño SWR cada 100
  → H=[E,C,U,S] ECUS α=[0.08,0.05,0.12,0.08] w=[1,0.8,0.5,1.5] (calibrados toy)
  → G(π)=Risk+Ambig, MPPI 800 trajs H=30 → a*
  → LLM codec: W:1024→4096 (SOLO W entrena), Qwen2-7B congelado, R(D)=½log(σ²/D)
```

**Solo entrena:** predictor 384, heads Π, W codec, Mamba Δ, GWT Q. **Congelado:** V-JEPA2 encoder, Qwen2-7B. (Protege tesis `LLM=boca` `02:129`.)

## Experimentos decisivos M4 (pre-registrados, se ejecutan con GPU)

1. **M4-H2b real (sin LLM):** ¿`Self_t`+`G` sigue forrajeando/recordando Kael sin Qwen2-7B? Toy fue trivial (LLM 1/1000 invocaciones); en mundo rico el LLM participa más. A colapsa=LLM fuente, B sigue=LLM traductor. **Métrica:** ΔE, H1 probe, D avg con vs sin codec.
2. **M4-M3b real (plasticidad):** aprender aversión en mundo rico → borrar E 5k → ¿W=W₀+BA r=16 EWC λ=3000 retiene? Toy dio 0.88>0.7 con un peso; real mide Fisher diagonal sobre millones. **Métrica:** P(evitar|E borrado)>0.7.
3. **H4 real:** k>5 (no 2.5), Δ_global>40%, PCI>0.31 (LZ76), ρ>0.5, Acc>70% con V-JEPA2 VoE IntPhys2 1416v.
4. **24h:** solo después de M3b-real PASA (plasticidad antes que longevidad, valoración externa).

## Opciones para avanzar SIN GPU (criterio experto)

1. **M4-intermedio CPU/MPS:** V-JEPA2 ViT-Small/Tiny (~300M/95M) + Qwen2-0.5B, Habitat-lite 10Hz, 1-4h/día en M4 Pro MPS. No es M4 completo pero valida flujo real (encoder aprendido, no lineal toy) en hardware disponible. Coste 0€.
2. **Cloud spot:** A100 ~1.1€/h spot, 30h ≈ 33€. Ejecutar M4 completo un fin de semana.
3. **Esperar:** mantener toy como referencia, esperar GPU.

**Recomendación experta:** Opción 1 (M4-intermedio CPU/MPS) — valida el flujo con encoder real aprendido y EWC real sin coste, antes de invertir 33€ en A100. Es el siguiente paso que sí se puede ejecutar hoy.

## Estado acumulado v0.8.2

- ✅ Toy completo: GATE_TOY_OK PASA (E/U/S/dark/H1/VoE/D 0.17), H4 5/5, H2b toy B, M3b toy 0.88
- 🔵 M4 bloqueado por GPU (honesto, scaffold listo)
- 🔵 M4-intermedio CPU/MPS viable hoy (propuesta)
- ❌ No demostrado: awareness, conciencia, plasticidad real

*Sin inflar. Scaffold es flujo, no ejecución. Ver `24-M3-iter4-plasticidad-resultados.md:1` y `framework/m4_escalado_real.py:1`.*
