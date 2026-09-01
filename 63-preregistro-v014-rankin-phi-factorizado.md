# 63 - Preregistro v0.14 — Batería Rankin + Predictor Factorizado + Φ por Canal + 4 Brazos + SVD

> **Fecha:** 2026-09-01 — escrito ANTES de correr v0.14
> **Supersede:** corrige el peer review que tumbó "qué se aprendió" en v0.12/v0.13
> **Mundos:** UNO solo — continuo v0.12 `framework/organismo_final.py:21` WORLD_SIZE 20.0, NIEBLA_X 14.0, RUIDO_BASE 0.15 / RUIDO_NIEBLA 0.60, H*=[0.8,0.9,0.2,0.7], comida FUERA de niebla
> **Estado del peer review:** el decremento z vive en ΔW (C4a/b, persistencia 0.02), pero C3 (1.1 vs 0.9) muestra "learning without distinguishing" (magnitud no vector); Φ escalar MSE es proxy de zona y su d=-1.61 está confundido con gate atencional; EWC no protege misma tarea; todo fue causado por predictor single-head + loss L2 global + λ_ortho + Φ escalar + naming C3.

## 1. Cirugía mínima (no agrandar MLP, no segundo agente)

1. **Predictor factorizado.** Dos cabezas separadas con pérdidas separadas: `f_pos: R13 -> R2` (x,y) y `f_H: R13 -> R4` (E,C,U,S). Encoder compartido 13->64 se mantiene, pero se reporta sorpresa por cabeza. Dos brazos: con `λ_ortho=0.01` y `λ_ortho=0` para ver si el fix global ocultó el colapso.
2. **Φ por canal (precisión real).** Input `(s,a,canal)` y output `log σ²_c` por canal (7 valores). Loss NLL `0.5*(log σ² + (ε_c²)/σ²)`, no MSE a |ε| escalar. Esto separa "Φ aprendió zona x>14" (σ_pos y σ_E suben juntos) de "Φ aprendió confiabilidad por canal" (σ_pos sube en niebla, σ_E no).
3. **Presencia acoplada como brazo.** `presence = ε / σ²_Φ` se acopla al drive U en brazo D; atención se congela ahí. En brazo C se hace lo inverso.

## 2. Hipótesis y criterios de refutación (fijos, no se mueven)

| # | Hipótesis | Métrica | PASA si | REFUTA si | Falsador que usa |
|---|---|---|---|---|---|
| H1 | Detección action-conditioned | z(S1_1) en continuo, N=30, CI95% bootstrap 2000 | z>10 y CI no cruza 5 | CI cruza 5 | C1 vs barajada debe ser >5x |
| H2 | Habituación por aprendizaje en ΔW | z(últimas 4 S1) vs z(S1_1) | reducción >70% con CI | <30% | C4b freeze debe dar ~0 reducción |
| H_A | Trazo es de magnitud, no de vector | z(S2) y z(S3) | H_A predice: z(S2) y z(S3) siguen bajos (<2.0) | Concepto vectorial predice: z(S2),z(S3) > z(S1_hab)+2SD | C3 viejo ya apunta a H_A |
| H_vec | Concepto vectorial alternativo | mismo que H_A | z(S2),z(S3) altos | z bajos | — |
| H_dis | Dishabituación real (Rankin 8) | z(S1_reprobe) tras S5 vs z(S1_hab) | z_reprobe >1.5*z_hab | ≤1.2*z_hab | Si no rebota, no hay dishabituación |
| H_rec | Recuperación espontánea (ISI) | z(gap 2000 pasos, sin updates) | z_gap > z_hab y < z_0 | z_gap ≈ z_hab | Si no recupera, trazo solo en W |
| H_Φcal | Φ calibrado por canal | Spearman r(σ_Φ,pos, ε_pos) | r>0.5 | r<0.3 | r_canal vs r_zona |
| H_Φcross | Φ generaliza | r_cross en violaciones no vistas | >0.3 | <0.1 | — |
| H_Φcaus | Física de precisión vs gate | % niebla en 4 brazos | D < C (presencia gana) si Φ preciso; A≈C << B≈D si gate | A≈C y D≈B → gate explica todo | Corazón del revisor B |
| H_EWC | Dial EWC load-bearing | recovery por λ | Distinto por λ solo si tarea B distinta | Igual en misma tarea (0.48) ya visto | SVD |
| H_rank | ΔW es low-rank | SVD ΔW post-hab | 90% varianza en 1-2 sing. → "ignore large L2" | >4 sing. → trazo rico | Factorizado |

## 3. Protocolo único (within-subject, N=30 mismos seeds, orden fijo por seed)

**Pre-train:** 1200 transiciones, 400 steps predictor, 500 steps Φ por canal, 300 steps attention (si aplica), igual que `organismo_final.py:199-222` pero con pérdida NLL por canal y entropía.

**Por seed (ej. 4000+s):**
1. Habituación S1: teleport (+2,+2) ×12 con aprendizaje (mide z cada vez, baseline congelada 100 pasos pre-violación, reporta ε crudo + z)
2. Sondas sin aprendizaje (mide z):
   - S2 same-mod: (-2,-2) misma magnitud, dirección opuesta
   - S3 ortho: (+2,-2)
   - S4 magnitud: (+4,+4)
   - S5 tipo: inversión de E interoceptiva (comer baja E)
3. Dishabituación: tras S5, re-sonda S1 inmediata → z_reprobe
4. Recuperación: gap 2000 pasos de física normal sin updates (o con updates solo de física normal, sin violaciones) → re-sonda S1 → z_gap
5. Re-habituación (savings): cuenta violaciones S1 hasta volver a <50% de z_0 → savings

**4 brazos Φ vs atención (mismo N=30, mundo comida fuera niebla, métrica % niebla en 3000 pasos):**
- A: Φ + atención + gate actual (`att_vis<0.35` o mean att>0.65 → acción 3)
- B: Φ computado pero no acoplado (igual que `h6_phi_causal.py:107` B)
- C: gate atención solo, Φ freeze (pesos congelados pre-train)
- D: presence = ε/σ²_Φ acoplada al drive U (ΔU += 0.2*presence), atención freeze (pesos congelados)

Predicción H_B: A ≈ C << B ≈ D en % niebla. Predicción Φ real: D < C y D < B.

**Factorizado + SVD:** medir C3 y dishabituación por cabeza (z_pos vs z_H). Guardar W_pre y W_post, hacer SVD de ΔW por capa, reportar nº sing. para 90% y espectro. Si f_pos generaliza y f_H no, el colapso es del encoder 13->64.

## 4. Umbrales y estadística (fijos)

- N=30, semillas 4000-4029 para Rankin, 0-29 para 4 brazos (mismos seeds que H_Φcaus previo)
- CIs 95% bootstrap 2000, Cohen's d pareado para S1_hab vs cada sonda, y para A vs B vs C vs D
- Criterio rank: singular values de ΔW capa hidden->out; reportar acumulado 90%
- Exclusión: seed con base std <1e-4 excluida (no hay baseline para z); se documenta y no se reemplaza post hoc
- Ningún umbral se mueve tras ver datos. MiniGrid sigue fuera.

## 5. Producto

- `framework/bateria_rankin.py` (S1-S5 + dishab + gap + savings)
- `framework/factorizado_phi_canal.py` (pred heads separados + Φ por canal NLL + 4 brazos)
- `results/v014_rankin.json` (por seed: z por sonda y por cabeza, z_reprobe, z_gap, savings, % niebla A-D)
- `results/v014_svd.json` (SVD ΔW por capa y por cabeza, espectro)
- `results/v014_phi_canal.json` (r por canal, r_cross por canal, σ_pos vs σ_E en niebla vs claro)

## 6. Cómo se interpreta el null (el resultado más valioso si H_A gana)

Si S2/S3 siguen bajos, dishab no rebota y SVD da 1-2 componentes, el paper v0.14 se titula honestamente "Learning without distinguishing: coarse habituation in weights" y cierra el claim vectorial. Eso encaja con C3 ya reportado (1.1 vs 0.9) y con EWC flat 0.48 y es publicable comme boundary condition. Si S2/S3 suben y dishab rebota, entonces v0.14 gana habituación estímulo-específica y v0.12 pasa a ser el piloto grueso.

## 7. Checklist de no-regresión

- [ ] Todos los z con baseline congelada pre-violación (no window contaminada post-violación)
- [ ] Reportar ε crudo además de z
- [ ] Guardar w_star y fisher por cabeza
- [ ] No tocar umbrales tras correr
- [ ] Reproducir con `python3 framework/bateria_rankin.py --seeds 30` y `python3 framework/factorizado_phi_canal.py --seeds 30` en M4 Pro MPS, sin GPU, ~1 día total

*Pre-registrado. Ejecutar solo después de este commit. Cualquier desviación se loguea como desviación, no se re-etiqueta C3.*
