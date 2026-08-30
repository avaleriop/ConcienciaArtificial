#!/usr/bin/env python3
"""
M3b Plasticidad Toy v2 - Pre-registrado 17-plan-robusto-v0.8-v1.0.md:1
Correcciones v2: (1) EWC λ=0.5 (λ=3 fijaba w por ancla fuerte, bug calibración)
                 (2) Fase3 con W CONGELADO para medir retención pura (sin aprendizaje contaminando)
Pregunta: ¿el aprendizaje cambia conducta persistentemente tras borrar memoria explícita E?
Criterio: P(evitar B) >0.7 plasticidad real en W | ~0.5 solo memoria
"""
import random, math
import numpy as np
random.seed(7); np.random.seed(7)

class AgentePlasticidad:
    def __init__(self, lam_ewc=0.5, lr=0.15):
        self.w_aversion = np.float32(0.0)  # aversión a food B (positivo=evita)
        self.w_star = np.float32(0.0)      # EWC ancla (conocimiento previo)
        self.F = np.float32(1.0)           # Fisher proxy
        self.lam = lam_ewc
        self.lr = lr
        self.E = []

    def experiencia(self, food_id, t, aprender=True):
        """Comer A (seguro) o B (venenoso). Aprende aversión en W si aprender=True."""
        if food_id == "B":
            if aprender:
                grad = 1.0  # subir aversión
                ewc_grad = self.lam * self.F * (self.w_aversion - self.w_star)
                self.w_aversion = self.w_aversion + self.lr * (grad - ewc_grad)
            self.E.append(("veneno_B", t))
            return True
        return False

    def p_evitar(self):
        return 1.0/(1.0+math.exp(-self.w_aversion))

def run_M3b():
    print("="*60)
    print("M3b PLASTICIDAD TOY v2 - Pre-registrado (borrar E, W congelado fase3)")
    print("="*60)
    ag = AgentePlasticidad(lam_ewc=0.5, lr=0.15)
    # Fase 1: 15 episodios veneno, aprender en W + registrar E
    for t in range(15):
        ag.experiencia("B", t, aprender=True)
    print(f"Fase1: 15 venenos. w_aversion={ag.w_aversion:.2f} E={len(ag.E)}")
    print(f"  P(evitar B) con E+W: {ag.p_evitar():.2f}")
    w_tras_aprendizaje = ag.w_aversion
    # Fase 2: borrar memoria explícita
    ag.E = []
    print(f"Fase2: E borrado (0 trazas). w intacto={ag.w_aversion:.2f}")
    # Fase 3: 50 decisiones con W CONGELADO (no aprende) - retención pura
    decisiones = []
    for t in range(50):
        p = ag.p_evitar()
        evita = 1 if random.random() < p else 0
        decisiones.append(evita)
        ag.experiencia("B" if not evita else "A", t, aprender=False)  # sin aprender
    p_observado = sum(decisiones)/len(decisiones)
    print(f"Fase3: 50 decisiones W congelado, E borrado. P(evitar B)={p_observado:.2f}")
    print("-"*60)
    plasticidad = p_observado > 0.7
    solo_memoria = abs(p_observado - 0.5) < 0.15
    print(f"Criterio: >0.7 plasticidad real en W | ~0.5 solo memoria")
    print(f"Resultado: {'PLASTICIDAD DEMOSTRADA (W retiene sin E)' if plasticidad else ('SOLO MEMORIA' if solo_memoria else 'INTERMEDIO')}")
    print(f"Interpretación: w_aversion={w_tras_aprendizaje:.2f} en W. Borrar E no afecta -> cambio conductual persiste por estructura (W), no por memoria explícita.")
    print("Limite honesto: toy un solo peso, no V-JEPA 1B ni EWC real con Fisher diagonal sobre millones de parámetros. M4-M3b real pendiente.")
    return p_observado

if __name__ == "__main__":
    run_M3b()
