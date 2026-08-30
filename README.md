# Conciencia Artificial — Organismo Tetraedro v0.11

Proyecto teórico-experimental: construir un organismo artificial continuo que piensa en
representación aprendida, mantiene homeostasis, detecta violaciones de sus predicciones,
aprende en sus pesos sin memoria explícita, y usa un LLM local (LFM2.5-1.2B) como boca
(traductor), no como cerebro.

**Tesis:** `Conciencia (tetraedro H1+H2+H3+H5) → usa LLM como traductor congelado → Realidad`

## Instalación

```bash
pip install -r requirements.txt
# descargar el LLM local (1.2GB, opcional para experimentos con boca):
python3 -c "from huggingface_hub import snapshot_download; snapshot_download('LiquidAI/LFM2.5-1.2B-Instruct-MLX-8bit', local_dir='models/LFM2.5-1.2B-MLX-8bit')"
```

## Experimentos principales (cada uno con su doc)

| Script | Qué mide | Doc |
| :--- | :--- | :--- |
| `framework/organismo_completo.py` | Organismo completo: predictor+sorpresa+ECUS+memoria+boca en UN loop | `44` |
| `framework/m5_cadena_completa.py` | Cadena causal: detecta→estado→acción→aprende→persiste en W sin E | `43` |
| `framework/rigor_controles.py` | Controles CheckVLA (acción-barajada, obs-sola, ablaciones W) | `47` |
| `framework/estadistica_fase2.py` + `analisis_fase2.py` | N=30 seeds, CI, Cohen's d | `48-49` |
| `framework/benchmark_doorkey.py` | Empty-8x8 vs baselines aleatorio/ICM/RND | `51` |
| `framework/m5_24h_local.py` | 864k pasos (24h simuladas) | `38` |
| `framework/m4_local_h2b.py` | H2b: conducta idéntica con/sin LLM real | `36` |
| `framework/m4_local_m3b.py` | Plasticidad: W retiene aversión sin memoria E | `37` |

## Resultados clave (blindados)

- Detección de violaciones: z=20.6, CI [16.0, 25.5], N=30
- Habituación: 86% reducción, d=3.5
- Persistencia en W sin E: ratio 0.02
- Homeostasis con política: E 0.85, 100% seeds
- Controles: 5/6 (acción-barajada 7×, obs-sola 8.5×, ablaciones W)
- Benchmark: organismo 1.8% vs ICM 0.6% vs aleatorio 0.4% (Empty-8x8, mayor cobertura)

## Estructura

- `00`-`51` docs numerados (teoría, experimentos, auditorías, resúmenes)
- `framework/` scripts ejecutables
- `results/` JSON con todos los números
- `models/` LLM local (excluido de git)

## Límites honestos

No se demuestra awareness ni conciencia. V-JEPA 1B y DoorKey-PPO requieren GPU (opcional).
Lenguaje verificable: "detecta violaciones, actualiza predictor, reduce error" — sin antropomorfismo.
