import numpy as np

def metoda_eulera(e_func, t0, tk, dt, i1_0, i2_0, uc_0, pochodne):

    kroki = int((tk - t0) / dt) + 1
    czas = np.zeros(kroki)
    i1 = np.zeros(kroki)
    i2 = np.zeros(kroki)
    uc = np.zeros(kroki)
    e = np.zeros(kroki)

    czas[0], i1[0], i2[0], uc[0], e[0] = t0, i1_0, i2_0, uc_0, e_func(t0)

    for k in range(kroki - 1):
        di1, di2, duc = pochodne(czas[k], i1[k], i2[k], uc[k], e[k])
        i1[k + 1] = i1[k] + dt * di1
        i2[k + 1] = i2[k] + dt * di2
        uc[k + 1] = uc[k] + dt * duc
        czas[k + 1] = czas[k] + dt
        e[k + 1] = e_func(czas[k + 1])

    return czas, i1, i2, uc, e