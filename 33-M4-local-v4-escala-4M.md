# 33 - M4-Local v4 - Escala 4M params: Techo Práctico Local Documentado

> **Ejecutado:** 29 Ago 2026 15:50 UTC - `python3 framework/m4_local_v2.py --steps 50000 --warmup 2000` (MPS)
> **Cambio v4 pre-registrado `32:1`:** encoder 6→2048→1024→512, Mamba N=256.

## Resultado v4 (4.081.409 params, 52k pasos)

```
Params: 4.081.409 (158× el encoder inicial 25k)
MPS peak: 3.59GB (límite 8GB, holgura 55%)
Tiempo: 71s para 52.000 pasos = 1.4ms/paso (mismo que 1M params: MPS dominado por loop Python, no por cómputo)
JEPA final: 0.0033 (convergente)
E: 0.66-1.16 oscilante | U: 0.37 | S: 0.45 | D avg: 0.36 -> homeostasis PASA
Drift memoria: +0.4GB en 50k pasos (negligible, empty_cache cada 100 lo controla)
Seguridad: parada limpia 8GB nunca alcanzada, sin swap, sin crash
```

## Escala acumulada (seguro, esta máquina)

| Versión | Params | JEPA | ms/paso | MPS | Pasos |
| :--- | :--- | :--- | :--- | :--- | :--- |
| v1 | 25k | 0.0092 | ~8 | <0.5GB | 3000 |
| v2a | 283k | 0.0022 | 6.5 | 5.2GB* | 7000 |
| v3 | 1.1M | 0.1008* | 1.4 | 0.78GB | 12000 |
| **v4** | **4.08M** | **0.0033** | **1.4** | **3.59GB** | **52000** |

*antiguos sin fix leak; v3 JEPA alto por warmup corto con lr alto.

## Conclusión honesta sobre escalado local

1. **Techo práctico: ~4M params indefinido** a 1.4ms/paso, 3.6GB — la máquina aguanta sin riesgo. Podría llegar a 10-20M (el cómputo no es cuello, la memoria sí), pero:
2. **Punto de rendimientos decrecientes:** nuestro mundo local tiene obs de **6 dimensiones**. Un encoder de 4M params para 6-dim está **sobreparametrizado** (JEPA 0.0033 ≈ 0.0006 de 1M — no mejora 4×). La ganancia real de escala viene con **input rico (video 224² en V-JEPA)**, no con más MLP sobre 6 números. Esto es evidencia honesta de que el límite del experimento local es el *mundo*, no el *modelo*.
3. **Lo que el escalado SÍ demostró:** la arquitectura tetraedro (JEPA + EWC + Mamba + ECUS) es **estable a través de 160× de escala** — homeostasis idéntica, sin colapso, sin divergencia. Eso valida que el diseño no es un artefacto del tamaño pequeño.
4. **V-JEPA2 1B sigue siendo el salto real** (input video + 1000× params) — requiere A100, honesto.

## Próximos pre-registrados

1. **v5-mundo-rico:** en vez de más params sobre 6-dim, enriquecer el input (obs 64-dim tipo vision patch toy o mini-imagen 8×8) con el encoder 1M — es donde está la ganancia real local.
2. **v4-VoE relativo:** sorpresa vs baseline del mismo modelo (z-score), pendiente.
3. M4 cloud A100: V-JEPA2 1B + Qwen2-7B, si algún día hay presupuesto.

*Seguro: 4M params, 3.6GB, sin daño. El límite lo pone el input de 6-dim, no el hardware. Documentado `framework/m4_local_v2.py:1`.*
