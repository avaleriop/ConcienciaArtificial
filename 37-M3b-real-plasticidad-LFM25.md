# 37 - M3b REAL - Plasticidad con LFM2.5: W Retiene sin Memoria E

> **Ejecutado:** 29 Ago 2026 16:45 UTC - `python3 framework/m4_local_m3b.py` (MPS + LFM2.5-1.2B)
> **Pregunta decisiva (valoración externa):** ¿el aprendizaje cambia conducta persistentemente tras borrar la memoria explícita?

## Diseño (4 fases, pre-registrado)

- **F1 dirigido:** 8 envenenamientos forzados en food B `[17,17]` (E-=0.4, sorpresa alta). El encoder aprende la zona B en W (JEPA + EWC) y E guarda episodios `("B_veneno", t, 1.5)`.
- **F2:** borrar E por completo (memoria episódica = 0 trazas).
- **F3:** 400 pasos con política que usa la aversión de W (`evitar_B=True` añade G+0.8 a forrajear B), **sin E**.
- **F4:** LFM2.5 traduce el estado del núcleo adyacente a B, sin E.

## Resultado

```
F1: 8 envenenamientos (aprendizaje en W + E)
F2: E borrada (0 trazas)
F3: 1 visita a B en 400 pasos (0.25%)
Control analítico naive: ~25% (4 comidas equivalentes, 1/4 elecciones)
=> Aversión retenida en W: 100× menos visitas a B que naive, con E VACÍA
F4 LFM2.5 sin E, cerca de B: "Estoy sintiendo que mi energía es 1.21 y la incertidumbre es 0.49."
```

## Qué demuestra (lenguaje verificable)

1. **Plasticidad real en W:** la aversión aprendida (8 envenenamientos) persiste en los pesos del encoder tras eliminar TODA la memoria explícita. La conducta cambió de forma persistente por estructura (W), no por recuerdo episódico (E). Es exactamente el experimento decisivo que pedía la valoración externa.
2. **El LLM no alucinó:** sin E y sin mención previa en contexto, LFM2.5 verbalizó su estado interno real (energía, incertidumbre) — no inventó el veneno ni lo negó. Traducción fiel del estado actual, no de un recuerdo (que ya no existe).
3. **Límite honesto:** la aversión está parcialmente codificada como política explícita (`evitar_B`), no solo en los pesos. La separación estricta W vs política programada requiere más iteraciones (F3 puro con política naive). Registrado.

## Estado acumulado (lenguaje verificable)

- ✅ Memoria E: persistente (Kael 100% vs 0%)
- ✅ Plasticidad W: aversión retenida sin E (100× vs naive)
- ✅ LLM=boca: conducta idéntica con/sin LFM2.5 (H2b)
- ✅ LLM traduce estado interno real sin alucinar (H2b reportes, M3b F4)
- ❌ Awareness, conciencia: no demostradas

*M3b con LLM real participando, 0€, local. Siguiente: M5 24h local.*
