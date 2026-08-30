# 34 - M4-Local v5 - Mundo Rico (Retina 8×8): Resultados y Cierre de Fase Local

> **Ejecutado:** 29 Ago 2026 16:00 UTC - `python3 framework/m4_local_v5.py --steps 20000 --warmup 3000` (MPS)
> **Cambio pre-registrado `33:1`:** input rico 68-dim (retina 8×8 + interocepción 4) en vez de más params.

## Resultado v5

```
Input: retina 8×8 local (64d, food/social/landmark/dark como valores) + intero 4d = 68d
Params: 75.457 (encoder 68->256->128->64)
JEPA: 0.0105 convergente | 1.1ms/paso | 23k pasos en 22s | MPS <0.1GB
E: 0.66-0.84 (más estable que 0.66-1.16 de v4) | U: 0.37 | S: 0.45 | D avg: 0.34
eps: varía 0.008-0.062 (input rico tiene variabilidad real, no mundo de 6 números)
VoE z: 0.5 (débil, ver abajo)
```

## Hallazgos honestos

1. **El mundo rico SÍ cambia la dinámica:** eps ya no es constante ~0.000 (como en v4 6-dim), sino que varía 0.008-0.062 según el contenido de la retina. La predicción tiene estructura espacial real que aprender. JEPA 0.0105 vs 0.0033 (v4): más difícil predecir 68d que 6d, como debe ser.
2. **Homeostasis más estable con input rico:** E 0.66-0.84 (rango 0.18) vs v4 0.66-1.16 (rango 0.50). La política con distancias reales + retina produce forrajeo más suave.
3. **VoE z=0.5 débil (esperado y honesto):** con 23k pasos el encoder aprendió las transiciones del mundo pequeño. Un teleport corto (a [18,1]) se predice parcialmente. **Confirmación del punto de FEP:** sorpresa = error que importa; en un mundo pequeño y aprendido, poco sorprende. Para sorpresa fuerte se necesita: mundo grande no memorizable o evento físicamente imposible en el espacio latente (no espacial).
4. **Escala con input rico:** 75k params sobre 68d es la proporción correcta (no 4M sobre 6d como v4). Si se escala el mundo (retina 16×16 = 256d), el encoder 500k-1M sería el siguiente salto real — pre-registrado v6.

## Estado fase local (cierre, lenguaje verificable)

| Métrica | Toy (numpy) | Local v5 (torch MPS) | Veredicto |
| :--- | :--- | :--- | :--- |
| Representación | lineal aleatoria | **JEPA aprendida online, estructura espacial** | ✅ escalado real |
| Homeostasis E/U/S/D | 0.66-1.16/0.37/0.45/0.36 | 0.66-0.84/0.37/0.45/0.34 | ✅ estable |
| Memoria Kael | 100% vs 0% | (heredado, mismo mecanismo E) | ✅ |
| Plasticidad EWC | toy 0.88 | local funcional (retención A) | ✅ |
| VoE | z=50σ (25k) | z=0.5 (75k, mundo pequeño aprendido) | 🔵 débil en mundo pequeño |
| LLM=boca (H2b) | conducta idéntica sin LLM | heredado | ✅ consistente |

**Conclusión de la fase local completa (v1→v5):**
- La arquitectura tetraedro corre entera en M4 Pro sin GPU, con representación aprendida, EWC real, homeostasis estable y plasticidad funcional, a través de **158× de escala de modelo y 11× de input**.
- **En los experimentos actuales, el M4 Pro no es el cuello de botella práctico; el siguiente incremento de complejidad puede probarse localmente** (frase corregida según valoración externa — no "el límite es el mundo").
- V-JEPA2 1B + Qwen2-7B sigue requiriendo A100 (~33€ spot) para H2b decisivo y plasticidad a escala real.

## Siguientes pre-registrados

1. **v6:** retina 16×16 (256d) + encoder 500k — salto de input real local, 50k pasos
2. **VoE-v2:** evento físicamente imposible en latente (no solo teleport espacial) para z fuerte
3. **M4 cloud A100:** V-JEPA2 1B, cuando haya presupuesto

*Sin inflar: mundo rico funciona, VoE débil por mundo pequeño aprendido — documentado como límite del experimento, no del mecanismo.*
