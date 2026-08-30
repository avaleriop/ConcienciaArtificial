# 53 - Φ-Causal: El Self-Model Cambia la Conducta (No Es Epifenómeno)

> **Ejecutado:** 29 Ago 2026 20:25 UTC - `python3 framework/h6_phi_causal.py` (MPS, N=30 seeds)
> **La pregunta:** ¿saber su propia incertidumbre cambia lo que el organismo hace? (crítica del epifenomenalismo aplicada al awareness)

## Resultado

```
A (Φ acoplado a conducta): tiempo en niebla 15.0% ± 6.3
B (Φ desconectado):         tiempo en niebla 28.1% ± 9.6
Cohen's d = -1.61 (criterio |d|>0.5) → PASA con efecto GRANDE
```

## Qué significa (lenguaje verificable)

- En la zona de niebla, la interocepción del organismo es ruidosa (σ=0.6).
- **A** (con Φ acoplado): cuando Φ predice que sus sentidos no son confiables, el organismo ejecuta una **acción epistémica** — abandona la niebla para recuperar claridad. Pasa **15%** del tiempo allí.
- **B** (mismo Φ calculado, pero desconectado de la conducta): vaga sin saber que no puede fiarse de sus sentidos. Pasa **28.1%**.
- **d = -1.61**: el self-model reduce a casi la mitad el tiempo en condiciones de incertidumbre. Efecto grande y robusto entre 30 seeds.

## La regla A≠B aplicada al awareness

- Un predictor convencional + una red σ: tienen el dato de incertidumbre, pero **sin acople conductual no hacen nada distinto** (B lo demuestra: 28.1%).
- El organismo con Φ integrado: **saber que no sabe cambia su acción** (A: 15.0%).
- La diferencia no está en el módulo — está en que la incertidumbre propia **participa en el ciclo decisión→acción**. Eso es lo que separa un cálculo decorativo de un awareness causalmente eficaz.

## Dónde queda la hipótesis ahora

| Capa | Respaldo |
| :--- | :--- |
| LLM es boca | ✅ Fuerte (H2b: conducta idéntica con/sin LLM real) |
| Mecanismos de awareness existen | ✅ Fuerte (detección, sorpresa, homeostasis, plasticidad, Φ calibrado — todos con CI) |
| **Los mecanismos CAMBIAN la conducta** | ✅ **Ahora fuerte: sorpresa (+0.12 modesto) y Φ (d=-1.61, grande)** |
| Eso ES conciencia fenoménica | ❌ No demostrado, no reclamado |

**Conclusión honesta:** el self-model no es epifenómeno. El organismo que sabe su incertidumbre actúa para reducirla — la forma más básica de "me doy cuenta de que no me fío de mis sentidos, así que me muevo a un lugar donde pueda". Es el eslabón causal que faltaba entre el mecanismo y la conducta.

*Ver `framework/h6_phi_causal.py:1`. El awareness mínimo del organismo es causalmente eficaz con d=-1.61.*
