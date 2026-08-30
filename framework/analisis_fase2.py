#!/usr/bin/env python3
"""
ANÁLISIS FASE 2 - Lee results/estadistica_fase2.json y genera tabla CI/Cohen-d
Ejecuta: python3 framework/analisis_fase2.py
"""
import json, numpy as np

def ci95(x):
    x = np.array(x)
    # bootstrap 2000
    rng = np.random.default_rng(42)
    means = [np.mean(rng.choice(x, size=len(x), replace=True)) for _ in range(2000)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))

def cohend(a, b):
    a = np.array(a); b = np.array(b)
    pooled = np.sqrt(((len(a)-1)*a.var() + (len(b)-1)*b.var())/(len(a)+len(b)-2))
    return float((a.mean()-b.mean())/pooled) if pooled > 0 else float('inf')

def main():
    with open('results/estadistica_fase2.json') as f:
        R = json.load(f)
    z_motor = [r['z_motor'] for r in R]
    z_hab_prim = [r['z_hab_primera'] for r in R]
    z_hab_ult = [r['z_hab_ultima'] for r in R]
    z_post = [r['z_post'] for r in R]
    E = [r['E_final'] for r in R]
    print("="*72)
    print(f"ANÁLISIS FASE 2 - N={len(R)} seeds")
    print(f"H1 z(motor):        media {np.mean(z_motor):.1f}  95%CI [{ci95(z_motor)[0]:.1f}, {ci95(z_motor)[1]:.1f}]")
    print(f"   PASA si CI no cruza 5: {'PASA' if ci95(z_motor)[0] > 5 else 'REFUTA'}")
    d_hab = cohend(z_hab_prim, z_hab_ult)
    red = (np.mean(z_hab_prim)-np.mean(z_hab_ult))/np.mean(z_hab_prim)*100
    print(f"H3 habituación:     {np.mean(z_hab_prim):.1f} -> {np.mean(z_hab_ult):.1f} (reducción {red:.0f}%, d={d_hab:.1f})")
    print(f"   PASA si reducción >70%: {'PASA' if red > 70 else 'REFUTA'}")
    ratio = np.mean(z_post)/np.mean(z_motor)
    print(f"H4 persistencia:    z_post/z_motor = {ratio:.2f} ({np.mean(z_post):.1f}/{np.mean(z_motor):.1f})")
    print(f"   PASA si <0.5: {'PASA' if ratio < 0.5 else 'REFUTA'}")
    en_rango = sum(1 for e in E if 0.5 <= e <= 1.2)/len(E)*100
    print(f"H5 homeostasis:     E media {np.mean(E):.2f}, {en_rango:.0f}% seeds en [0.5,1.2]")
    print(f"   PASA si >=90%: {'PASA' if en_rango >= 90 else 'REFUTA'}")
    print("="*72)

if __name__ == "__main__":
    main()
