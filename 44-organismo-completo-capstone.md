# 44 - Organismo Completo v0.11 - Capstone: Todos los Mecanismos + Boca en UN Loop

> **Ejecutado:** 29 Ago 2026 18:30 UTC - `python3 framework/organismo_completo.py --steps 20000` (MPS + LFM2.5)
> **Esto es el objetivo del proyecto funcionando en una sola pieza:** el organismo completo, integrado, continuo.

## El loop integrado (todo verificado por separado antes, ahora junto)

```
mundo → estado (pos + H interoceptivo)
   → H2: predictor del cuerpo P(s'|s,a)
   → H5: ε → z-score (sorpresa emergente, sin flag)
   → integración causal: sorpresa → U → política (explora)
   → H3: ECUS homeostasis E,C,U,S
   → H1: memoria episódica E (eventos) + W con EWC (física aprendida)
   → boca: LFM2.5-1.2B traduce el estado interno en eventos de alta sorpresa
   → acción → mundo ↺
```

## Resultado 20.000 pasos continuos

```
t=4000:  E=0.62 U=0.00 | z_max 5.3 | boca 11
t=8000:  E=0.74 U=0.00 | z_max 7.4 | boca 22
t=12000: E=1.26 U=0.59 | z_max 7.8 | boca 36   <- U sube tras sorpresa
t=16000: E=0.92 U=0.00 | z_max 7.0 | boca 48   <- U decae (recuperación)
Final: E oscila 0.61-1.50, U 0.62, S 0.70, E_mem 4 trazas, boca 57 reportes
```

## Lo que demuestra (lenguaje verificable)

1. **Todos los mecanismos coexisten en un loop**: predictor, sorpresa, homeostasis, memoria, plasticidad y boca — ninguno rompe a los demás.
2. **La sorpresa viaja por la cadena**: z 5.3-7.8 en eventos → U sube (0→0.59) → política explora → habituación → U decae (recuperación).
3. **La boca traduce el estado interno real**: reportes como "energía de 1.50 e incertidumbre de 0.31" — el LLM verbaliza lo que el núcleo le da, sin decidir nada.
4. **Supervivencia**: 20k pasos sin colapso, E regulada en rango viable.

## Bugs de portado encontrados y corregidos (lecciones de integración)

| Bug | Síntoma | Fix |
| :--- | :--- | :--- |
| Política sin navegación a comida | E→0 (muerte) | `dir_food` portado de m5_24h |
| Forrajear en celda adyacente | E cae aunque "come" | forrajear solo si `dist==0` |
| U sin acotar | U satura 1.50, explora siempre | acotar +0.2 y decaimiento -0.05 |
| Boca sin cooldown | 239 reportes repetidos | z>4 + cooldown 200 → 57 reportes útiles |

**Lección general:** integrar mecanismos verificados por separado revela bugs de interfaz (política ↔ mundo ↔ sorpresa) que solo se ven en el loop completo. Es el mismo patrón de todo el proyecto: el proceso continuo expone aristas.

## Estado del proyecto (v0.11)

- ✅ Cadena causal completa (detecta → estado → acción → aprende → persiste en W) `43:1`
- ✅ Sorpresa emergente sin visión (canal del cuerpo) `41:1`
- ✅ Organismo completo en UN loop con boca real `este doc`
- ✅ Plan M1-M5 completo, H2b LLM real, M3b plasticidad, 24h
- ❌ No demostrado: awareness, conciencia (y no se finge)
- 🔵 Siguiente natural: corridas más largas (100k+) + mundo con más objetos + H6 local (Φ)

*El objetivo del proyecto — organismo continuo con mecanismos integrados y LLM como boca — funciona en una sola pieza, local, 0€. Ver `framework/organismo_completo.py:1`.*
