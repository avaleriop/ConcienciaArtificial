# Config v0.14 congelada por preregistro 63 / SPEC.md.
WORLD_SIZE = 20.0
NIEBLA_X = 14.0
FOODS = [(3.0, 3.0), (3.0, 16.0), (10.0, 3.0), (10.0, 16.0)]
SOCIAL = (18.0, 18.0)
H_CANON = [0.8, 0.9, 0.2, 0.7]
H_INIT = [0.6, 0.8, 0.7, 0.5]
RUIDO_BASE = 0.15
RUIDO_NIEBLA = 0.60
ORTHO_LAMBDA = 0.01
EWC_LAMBDA = 5.0
D_IN = 13          # 2 pos/W + 4 H/1.5 + 7 action one-hot
D_ENC = 64
N_ACT = 7
N_CANALES = 6      # canales de error del predictor: x, y, E, C, U, S
ACCIONES = tuple(range(N_ACT))
SEEDS_RANKIN = range(4000, 4030)
SEEDS_PHI = range(30)
