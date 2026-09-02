# 65 - A1 Batería Rankin v0.14 — Resultados (N=30, seeds 4000–4029)

> **Ejecutado:** 2 Sep 2026, `python3 framework/bateria_rankin.py --seeds 30` (34 s, MPS).
> **Pre-registrado:** `63` (Rankin S1–S5 + dishab + ISI + savings + SVD), `SPEC.md`.
> **Sistema:** mundo continuo con niebla (x>14), predictor factorizado 13→64→(f_pos 2, f_H 4),
> z por cabeza con baseline CONGELADA (100 pasos sin eventos, nunca re-estimada), contexto de
> sondas en zona sin niebla x∈[5,13], y∈[5,15] (la niebla es dominio del 4-arm, A3).
> **Regla:** ningún umbral se movió tras ver datos; seed con σ base <1e-4 se excluye (0/30).

## Resumen (N=30 incluidas)

| Hipótesis (63 §2) | Métrica | Resultado | Criterio prereg | Veredicto |
|---|---|---|---|---|
| H1 detección | z0(S1, 1ª violación) | **6.47** CI[5.30, 7.70] | z>10 y CI no cruza 5 | ⚠️ **no alcanza z>10**; CI no cruza 5 |
| H2 habituación | z0→z_hab (últ 4 de 12) | **84%** CI[78%, 89%] | reducción >70% | ✅ PASA |
| z(S1) habituado | z_hab | 1.14 CI[0.76, 1.52] | — | bajo (habituado) |
| H_A learning-without-distinguishing | z(S2) = (−2,−2) | **14.54** CI[12.4, 16.8] | H_A: S2/S3 bajos (<2) | ❌ **H_A REFUTADA en continuo** |
| H_vec (especificidad de dirección) | z(S3) = (+2,−2) | **10.35** CI[8.5, 12.2] | H_vec: S2/S3 altos | ✅ consistente |
| Magnitud ×2 | z(S4) = (+4,+4) | 2.84 CI[2.3, 3.4] | — | parcial (aprende dirección, magnitud mal estimada) |
| Clase interoceptiva intacta | z(S5) (comer baja E) | **9.38** CI[8.2, 10.6] | S5 debe disparar (no se entrenó) | ✅ |
| Rankin 8 dishabituación | z_reprobe tras S5 | 1.42 CI[0.88, 2.04], d=0.16 vs z_hab | z_re > 1.5·z_hab | ❌ **NO hay dishabituación** |
| Rankin 10 recuperación ISI | z_gap tras 2000 pasos | **12.42** CI[11.1, 13.9] | z_gap > z_hab | ✅ SÍ recupera |
| Savings | trials a <50% de z0 | 10.8 CI[9.7, 12.0] (n_hab=12) | — | savings débil/nulo |
| H_rank SVD ΔW f_pos | sing. para 90% var | **1.4** | 1–2 singulares | ✅ low-rank |

## Qué dice esto (con frialdad)

1. **Detección real pero más débil que en grid.** z0=6.47 con CI [5.30,7.70]: el efecto existe
   (CI no cruza 0, ni 5 por poco) pero **no alcanza el z>10 pre-registrado en `63`**. La
   batería grid v0.13 (teleport ±5 de 20 = 25% del mundo) daba z=20.6; el teleport continuo
   +2 de 20 = 10% da ~1/3 de señal. H1 según su umbral **no pasa**; según el criterio de
   muerte del plan `64`-A1 (CI inferior <5) **sobrevive por margen mínimo**. Se reporta tal
   cual, sin recalibrar. Desviación anotada: el umbral z>10 del prereg se calibró mentalmente
   contra el grid y no se transfiere al continuo.

2. **El hallazgo grande: en continuo, la habituación NO es "learning without distinguishing".**
   Tras habituar a (+2,+2), sondear (−2,−2) re-dispara z=14.5 (¡> z0 inicial!) y (+2,−2) da
   10.4. Esto **contradice C3 grid v0.13** (1.1 vs 0.9), donde la habituación generalizaba a
   la dirección opuesta. H_A muere en continuo; H_vec sobrevive. El mecanismo aparente: el
   predictor aprende el *sesgo direccional* "+x,+y" y la física normal lo deshace en el gap
   (z_gap=12.4 = recuperación). La magnitud se estima mal (S4 solo 2.84): dirección sí,
   distancia no.

3. **No hay deshabituación Rankin-8**: exponer a la clase interoceptiva S5 (que dispara 9.4)
   NO revive S1 (z_reprobe 1.42 ≈ z_hab). Es un negativo honesto: la traza no es reactivable
   por novedad de otra clase.

4. **Rankin-10 sí**: tras 2000 pasos de física normal con updates, S1 vuelve a disparar
   (12.4). La traza de pesos es frágil frente al re-aprendizaje de física normal — consistente
   con SVD low-rank (1.4 singulares, "ignore large L2").

5. **Comparación grid vs continuo = resultado de transferencia, no bug.** Grid v0.13:
   generalización de magnitud (C3 negativo). Continuo v0.14: especificidad de dirección, sin
   dishabituación, con recuperación. Dos regímenes distintos; el paper v0.14 debe reportar
   ambos y NO promediarlos (regla del peer review).

## Comparación con v0.13 grid (no mezclar)

| Medida | grid v0.13 (z=20.6, ±5) | continuo v0.14 (teleport +2) |
|---|---|---|
| z0 detección | 20.6 CI[16,25.5] | 6.47 CI[5.3,7.7] |
| Habituación | 86% (60 viol.) | 84% (12 viol.) |
| Generalización dirección opuesta | SÍ (1.1 vs 0.9, C3) | **NO** (zS2=14.5) |
| Especificidad interoceptiva | no testeada limpia | S5 dispara 9.4 |
| Recuperación ISI | no testeada | 12.4 (sí) |
| Dishabituación Rankin 8 | no testeada | no (1.42≈1.14) |

## Archivos

- Datos: `results/v014_rankin.json` (por seed: z0, z_hab, reducción, z_S2/S3/S4/S5,
  z_reprobe, z_gap, savings, hab_zpos, SVD por capa).
- Código: `framework/bateria_rankin.py` (solo importa `framework.core`).
- Preregistro: `63`. Especificación: `SPEC.md`.

## Pendiente (no tocar umbrales)

A2: C1/C2/C4 a N=30 en el mismo mundo. A3: 4-arm Φ (presence acoplada/desacoplada/shuffle/
gate). B3: SVD por cabeza ya volcado en el JSON; falta probe de zona x>14 (B4) y EWC
tarea-distinta (A4). Nada de esto cambia los números de arriba.
