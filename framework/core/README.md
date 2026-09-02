# framework/core — núcleo v0.14

Especificación: `SPEC.md` (raíz). Preregistro: `63`.

Módulos:
- `config.py` — constantes congeladas del mundo (SPEC §1) y seeds.
- `world.py` — mundo continuo 20×20 con niebla (x>14), violaciones S1–S5, entrada/target.
- `nets.py` — PredictorFactorizado (encoder 13→64 + f_pos/f_H), PhiCanal (log σ² NLL), Attention.
- `surprise.py` — error por cabeza/canal y BaselineCongelada (μ,σ sin eventos, nunca se re-estiman).
- `ewc.py` — Fisher diagonal + término λ/2·ΣF(θ−θ*)² (solo A4, tarea distinta).
- `procedures.py` — pre-train (prereg 63 §3): predictor 1200 trans/400 steps, Φ NLL, attention.

Verificación: `python3 framework/selftest_core.py` (smoke, ~1 min) — valida física, pre-train,
baseline congelada, z(S1) alto y caída por habituación con estímulo idéntico, Φ NLL, EWC.

Baterías v0.14 (A1/A3) se construyen sobre este paquete; ningún script viejo debe producir
números de la Tabla v0.14 directamente.
