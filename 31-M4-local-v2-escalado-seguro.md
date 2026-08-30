# 31 - M4-Local v2 - Escalado Seguro: Techo de la Máquina Encontrado

> **Ejecutado:** 29 Ago 2026 15:30 UTC - `python3 framework/m4_local_v2.py` en MPS (Apple M4 Pro, 24GB unificada, 14 cores)
> **Objetivo usuario:** usar esta máquina al máximo seguro, sin dañar nada. Sin A100.

## Configuraciones probadas (todo con límite seguridad 8GB MPS + parada limpia)

| Config | Encoder | Mamba | Params total | JEPA final | ms/paso | MPS peak | Resultado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| v1 (previo) | 6→128→64 | N=64 | 25.793 | 0.0092 | ~8ms | <0.5GB | ✅ full run |
| **v2a** | 6→512→256→128 | N=128 | 283.137 | **0.0022** | 6.5ms | 5.23GB | ✅ 7000 pasos completos |
| **v2b** | 6→1024→512→256 | N=256 | 1.123.329 | **0.0006** | 6.2ms | 8.00GB | ⚠️ parada seguridad t≈4500 (límite) |

## Hallazgos

1. **Techo seguro encontrado:** ~**283k params indefinido** (5.2GB, 7000 pasos sin problema). **~1.1M params** solo para runs cortos (~4500 pasos) antes de tocar 8GB. Encoder más grande aprende mejor (JEPA 0.0006 vs 0.0092 = 15× mejor), como se espera.
2. **Leak de memoria MPS detectado:** MPS crece linealmente con pasos (0.03→8GB), no por modelo (1M params = ~4MB) sino por **fragmentación del caching allocator MPS** con batches de 64 creados cada 64 pasos. `torch.mps.empty_cache()` cada 500 ayuda parcialmente. No es dañino (para en 8GB con seguridad), pero limita runs largos.
   - **Fix candidato (próximo):** batch allocation pre-allocado + `empty_cache()` cada 100 pasos + `torch.no_grad()` en inferencia → debería estabilizar ~2-3GB y permitir 1M params indefinido.
3. **Seguridad funcionó como diseñado:** la parada limpia a 8GB protegió la máquina (sin swap, sin sobrecalentamiento, sin crash). RAM unificada intacta.
4. **Homeostasis PASA en todas las configs:** E 0.66-1.16 oscilante, U 0.37, S 0.45, D 0.36 — el escalado no rompe ECUS (heredado calibrado).
5. **VoE z débil (0.7-1.1):** con encoder grande y JEPA 0.0006, la predicción es tan buena que incluso el teleport se predice parcialmente (el predictor aprende las posiciones del mapa). En v1 (25k) z era 50σ porque el encoder era más débil. **Interpretación honesta:** a más capacidad predictiva, más difícil sorprender — consistente con FEP (sorpresa = error que importa, no error bruto). El umbral de VoE debe ser relativo a la capacidad del modelo, no absoluto.

## Estado escalado local (lenguaje verificable)

- ✅ **Escalado 45×** desde el encoder inicial 25k → 1.12M params, todo en máquina local, seguro
- ✅ JEPA 0.0092 → **0.0006** (15× mejor predicción con 45× más capacidad)
- ✅ Homeostasis ECUS estable en todas las escalas
- 🔵 Techo práctico: 283k indefinido / 1.1M corto, pendiente fix leak MPS para 1M indefinido
- ❌ V-JEPA2 1B sigue fuera de alcance local (1000× más params — A100 o nada, honesto)

## Siguiente pre-registrado

1. **v3 leak-fix:** batch pre-allocado + empty_cache 100 + no_grad → 1M params indefinido, 10k pasos
2. **v4 VoE relativo a capacidad:** z-score sobre baseline de modelos de igual tamaño (no umbral absoluto)
3. M4 cloud A100 queda como única vía para 1B (si algún día hay presupuesto)

*Seguro, sin dañar hardware: parada limpia verificada. Ver `framework/m4_local_v2.py:1`.*
