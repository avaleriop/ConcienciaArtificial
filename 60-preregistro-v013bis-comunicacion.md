# Pre-registro v0.13-bis — H-ECO-1-bis: Acoplamiento con Canal de Comunicación Explícito
> **Fecha:** 31 Ago 2026 — **Estado:** BORRADOR pre-registro (no ejecutado)
> **Base:** `framework/ecologia_2agentes.py` v0.13 (H-ECO-1 falló: r=-0.018, no acopla por co-presencia)

## Contexto
H-ECO-1 falló: 2 agentes compartiendo espacio y posición NO producen acoplamiento de Φ (r=-0.018, N=30). Hipótesis: falta un canal donde los agentes emitan su estado interno explícitamente, no solo su posición.

## H-ECO-1-bis: Acoplamiento por señalización de σ_Φ
Cada agente emite periódicamente su **σ_Φ** (incertidumbre autoconsciente) como un "llamado" que el otro recibe como canal adicional (1 dim extra en entrada). Si la señalización permite sincronizar cuándo cada agente "no sabe", debe emerger correlación.

**Métrica:** r = Pearson(σ_Φ(t) de agente 1, σ_Φ(t) de agente 2) sobre ventana completa. Pre-registrado: **r > 0.30** pasa.

**Hipótesis nula explícita:** si r ≤ 0.30, el acoplamiento mínimo NO emerge ni con comunicación directa del estado de incertidumbre — reportar como límite fundamental de estos agentes (comunicar el self-model no implica acoplarse).

## Diseño
- Mundo: continuo 20.0, niebla x>14 (0.60), 4 comidas, 2 agentes H* canónico.
- Entrada predictor/Φ ahora incluye: posición propia + posición otro + **σ_Φ del otro (1 dim, retardado 1 paso)** + estado ECUS + acción.
- Cada 100 pasos, cada agente emite su σ_Φ actual; el otro la recibe como "mensaje".
- Entrenamiento: predictor y Φ se entrenan de nuevo incluyendo el canal de mensaje.
- 30 seeds, 30000 pasos joint, 2 condiciones:
  - **A (señal activa):** los agentes reciben σ_Φ del otro.
  - **B (control):** reciben ruido en lugar de σ_Φ del otro (mismo canal, sin información).
- Métricas: r_Φ(A) vs r_Φ(B), y E_joint en ambos.

## Estadística pre-fijada
- N=30. Medias, 95% CI bootstrap 2000, Cohen's d pareado (A vs B en el mismo seed).
- Pasa si r_Φ(A) > 0.30 con CI inferior > 0.15, y r_Φ(A) - r_Φ(B) > 0.15.
- No se mueven umbrales post hoc.

## Criterio de parada
v0.13-bis se publica como hallazgo de comunicación si pasa; como límite fundamental honesto si falla (comunicar el self-model no acopla el comportamiento de estos agentes). Ambos son publicables.
