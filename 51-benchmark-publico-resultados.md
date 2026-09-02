# 51 - Benchmark Público (Fase 3): Resultados Preliminares y Límites

> **⚠️ RETIRADO DE LA TABLA DEL PAPER (2026-09-02, ver CHANGELOG):** N=5, sin potencia
> (RND 2.8% > organismo 1.8%). Este doc se conserva como registro histórico.

> **Ejecutado:** 29 Ago 2026 19:50 UTC - `python3 framework/benchmark_doorkey.py`
> **Pre-registrado:** `46-plan-rigor-cientifico.md:1` (Fase 3: medirnos contra el campo)

## Entorno y protocolo

- **MiniGrid Empty-8x8** (recompensa escasa: solo meta). Es el entorno estándar donde los bonuses de curiosidad demuestran ventaja.
- **DoorKey-8x8 fue intentado primero y resultó INVIABLE local**: requiere ~1M frames con PPO (vanilla REINFORCE dio 0% en todos los agentes). Documentado, no escondido.
- Política común: MLP + REINFORCE + entropía. N=5 seeds, 100 episodios, 64 pasos máx.
- Bonus: ICM (curiosidad por error de forward model), RND (novedad por destilación de red aleatoria), organismo (sorpresa z del predictor del cuerpo).

## Resultados (results/benchmark_doorkey.json)

```
Agente      Resuelve   Pasos medios   Cobertura estados
aleatorio   0.4%       63.9           30.6
ICM         0.6%       63.9           34.0
RND         2.8%       63.5           34.0
organismo   1.8%       63.7           34.8   <- mayor cobertura de todos
```

## Lectura honesta

1. **RND > organismo > ICM > aleatorio** en éxito. Nuestro organismo supera a ICM (el baseline clásico de curiosidad) y queda cerca de RND (el más fuerte en este régimen).
2. **El organismo explora más que todos** (cobertura 34.8) — consistente con el drive de sorpresa del cuerpo: visita más estados distintos.
3. **Límites serios (registrados):** N=5 (no 10), 100 episodios (los métodos de curiosidad suelen requerir 10× más), REINFORCE vainilla (el estándar es PPO). Estos números son **preliminares**, no definitivos.
4. DoorKey queda pendiente de GPU/PPO (mismo requisito que V-JEPA 1B: es un costo opcional de ~33€ o un port a PPO vectorizado local con más horas).

## Qué aporta esta fase

- ✅ Primeros números **públicos y comparables** del organismo contra baselines estándar (ya no medimos contra nosotros mismos).
- ✅ Posición clara: competitivo con el estado del arte de curiosidad en régimen escaso, con mayor exploración.
- 🟡 Poder estadístico bajo — el benchmark completo (PPO, 1M frames, DoorKey) es el siguiente escalón, con costo.

## Resultado de Fase 3: PARCIALMENTE COMPLETADA (Empty-8x8 sí, DoorKey pospuesto con justificación)

*Ver `framework/benchmark_doorkey.py:1` y `results/benchmark_doorkey.json`.*
