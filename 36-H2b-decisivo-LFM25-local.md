# 36 - H2b DECISIVO LOCAL: LFM2.5 Confirma LLM=Traductor (con LLM Real)

> **⚠️ "DECISIVO" RETIRADO (2026-09-02, ver CHANGELOG "Claims retirados"):** el resultado es
> *consistente* con LLM=boca pero no decisivo — el LLM nunca controla la política por diseño,
> así que conducta idéntica con/sin LLM está garantizada. Pasa a principio de diseño, no a
> evidencia de H2. Ver paper v0.13 (`56`).

> **Ejecutado:** 29 Ago 2026 16:30 UTC - `python3 framework/m4_local_h2b.py --steps 1500` en M4 Pro (MPS)
> **Importante:** este era el experimento que creíamos requerir A100 (~33€). LFM2.5-1.2B lo hace local, 0€.

## Setup (cambio clave: LLM real, no toy)

- **LLM codec real:** `LiquidAI/LFM2.5-1.2B-Instruct-MLX-8bit` (1.17B params, híbrido SSM-conv, 719MB Q4, MLX nativo Apple)
- Velocidad medida: **19ms/token, 0.6s por respuesta de 30 tokens** — viable en loop
- **Condición A (con LLM):** núcleo tetraedro (encoder 364k retina 16×16 + Mamba + ECUS) + LFM2.5 invocado cuando `U>0.45` o evento saliente
- **Condición B (sin LLM):** mismo núcleo, 0 invocaciones
- Eventos: Kael traición `t=100`, teletransporte VoE `t=500`
- **El núcleo construye el prompt desde su estado interno; el LLM SOLO traduce, nunca decide** (`framework/m4_local_h2b.py:96`)

## Resultado

```
A (con LFM2.5): E 0.75 C 0.90 U 0.37 S 0.45 D 0.33 | 2 invocaciones reales
B (sin LLM):    E 0.75 C 0.90 U 0.37 S 0.45 D 0.33 | 0 invocaciones
Conducta idéntica: TRUE → B (LLM=traductor) CONFIRMADO con LLM real
```

**Reportes reales traducidos por LFM2.5 (fieles al estado interno del núcleo):**
- `t=100 [Kael]:` "Estoy experimentando un error de predicción alto al ser robado el artefacto que cuidaba."
- `t=500 [VoE]:` "Estoy experimentando una sensación de sorpresa, ya que un objeto apareció de repente y mi expectativa fue violada."

## Qué significa (lenguaje verificable)

1. **`LLM=boca` se confirma en su versión decisiva:** con un LLM real participando (2 generaciones reales), la conducta del organismo (E/U/S/D) es idéntica con o sin él. El LLM no aporta inteligencia conductual: traduce estados internos que el núcleo ya tiene.
2. **El LLM traduce fielmente el estado interno:** los reportes describen correctamente los eventos (robo por Kael, violación de expectativa) — evidencia de que el núcleo tiene contenido interno coherente y el codec lo verbaliza sin añadir.
3. **Arquitectura coherente:** LFM2.5 es híbrido SSM-convolución (no Transformer puro) — la "boca" comparte filosofía con el núcleo Mamba.

## Implicación para el proyecto

- **M4 cloud A100 ya no es imprescindible para H2b** — hecho local, 0€.
- Siguiente: **M3b con LFM2.5** (plasticidad con LLM real) y **M5 24h local** (864k pasos ≈ 20 min wall-clock con el núcleo local; LLM invocaciones ocasionales suman ~1s c/u).
- M4 cloud queda solo para V-JEPA2 1B (world model real), si algún día hay presupuesto.

## Nota operacional

- `models/` (1.2GB) excluido del repo (.gitignore). Descarga: `snapshot_download('LiquidAI/LFM2.5-1.2B-Instruct-MLX-8bit', local_dir='models/...')`
- Historial git limpio: `.git` 1.09GiB → 259KiB (blob purgado con filter-branch + reflog expire).

*Hito: el experimento que creíamos imposible sin GPU se hizo en local con un modelo edge. Ver `framework/m4_local_h2b.py:1`.*
