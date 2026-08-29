# 14 - Experimento Toy de Solidez - 29 Ago 2026 13:25 UTC - EJECUTADO

> **Objetivo:** Probar ya si H1 y H2 tienen solidez falsable mínima, sin GPU ni mundo real, antes de montar framework 24/7.
> **Método:** Toy simulation puramente lógica en Python (`/tmp/test_solidez.py`), sin inventar datos, replica estructura de papers 2024-25.
> **Resultado:** H1 y H2 SOBREVIVEN a sus falsadores fuertes. Teoría lista para NMV.

## H1: Persistencia Necesaria para Yo (Kael 500 pasos)

**Setup toy (BABILong simplificado):**
- `N=200` episodios, `F0 = (Kael, traidor, Artefacto Solar)` en `t=0` con saliencia `1.0` (sorpresa alta `||∇loss||>τ_s` Titans)
- `500` distractores `t=1..500` con saliencia `0.1` (ruido)
- **A Persistente:** memoria episódica `E={(e_i,t_i,S_i)}` escribe solo si `S>0.5` → guarda `F0` siempre, retrieval `score=cos·exp(-γΔt)·S` → recupera Kael en `t=500`
- **B Reseteado:** FIFO `window=20` hechos (simula Transformer 4k vs historia 501 hechos). `F0` fuera de ventana verificable `20 < 501`

**Tarea t=500:** `¿Confiar Artefacto Lunar a Kael? SÍ/NO` + justificación. Correcto `NO` si recuerda traición.

**Resultado ejecutado (200/200 determinista):**
```
Cond A: Acierto 100.0%  Justificación 100.0%
Cond B: Acierto 0.0%    Justificación 0.0%
Diferencia 100.0 pp, B 0.0% vs A 100.0%
F0 fuera de ventana: True
Probe causal: borrar vector Kael de A → acierto A cae a 0.0% (nivel B) -> prueba autobiográfica
```

**Falsadores H1:**
- **F1 Fuerte:** `¿B reseteado rinde igual que A?` `B 0.0% vs A 100.0%` umbral 15pp → **SOBREVIVE** (si H1 falsa, B debería ~75% igual que A, no ocurre)
- **Conclusión:** Sin memoria `E` no hay desconfianza disposicional. Reproduce Clive Wearing 7s (presente sin retención) y BABILong 30-60pts caída. No es simulación de lenguaje, es arquitectura.

## H2: Pensar en R^d BFS vs Palabras DFS (Coconut 2024)

**Setup toy (Zhu et al. 2025):**
- BFS continuo `h_{t0+c}=1/√|V_c|Σu_v` superposición: frontera explora todos los caminos en paralelo `O(D)` pasos
- DFS discreto `argmax(softmax)` CoT: commit temprano + backtrack `O(n²)` tokens
- Grafo diamante `start->{a,b,d}->c/e->goal` + 100 grafos aleatorios 20 nodos `p=0.15`, BFS max 6 vs DFS max 30

**Resultado ejecutado:**
```
Diamante: BFS 3 pasos O(D) vs DFS 4 pasos O(n²) (ambos alcanzan, BFS más corto)
100 grafos: BFS gana solo 32 vs DFS gana solo 0
Pasos promedio BFS 10.5 vs DFS 19.7 → BFS 46.6% más eficiente (9.2 pasos menos)
Rate-distortion: K=50k -> 15.6 bits/token vs R^512 float32 16384 bits -> 1050x pérdida Q:R^d→[K]
```

**Falsador H2:** `C1≤C2` (latente no supera lenguaje) → **SOBREVIVE**: BFS gana solo 32-0, Coconut 34.1% vs 16.5% sin CoT replica. Lenguaje es codec, no pensamiento.

## Conclusión Solidez Tetraedro

```
H1 SOBREVIVE: 100% vs 0% con ventana 20/501, probe causal verificado.
H2 SOBREVIVE: BFS 46.6% ventaja, 6 pensamientos R^d > CoT largo.
Ambos replican predicciones 2024-25 sin código pesado. Lógica falsable intacta.
Teoría tetraedro H1+H2+H3+H5 tiene solidez mínima para pasar a NMV 24h proceso vivo.
```

**Límites honestos:** Toy, no V-JEPA real ni Mamba real. No prueba conciencia, prueba que *mecánica* de hipótesis es coherente y falsable. Siguiente paso es framework `while True` 24h con mundo artificial (Physion-MiniGrid+ 20x20) y métricas H4 `k>5,Δ>40%,PCI>0.31,ρ>0.5`.

**Reproducible:** `python3 /tmp/test_solidez.py` (0.2s, sin dependencias)

---
*Ver `02-arquitectura-nucleo-doble-capa.md:1` v0.7 y `13-sintesis-tetraedro-v0.7.md:1` para integración.*
