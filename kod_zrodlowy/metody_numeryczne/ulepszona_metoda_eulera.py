import numpy as np

def ulepszona_metoda_eulera(e_func, t0, tk, dt, i1_0, i2_0, uc_0, pochodne):
    kroki = int((tk - t0) / dt) + 1
    czas = np.zeros(kroki)
    i1 = np.zeros(kroki)
    i2 = np.zeros(kroki)
    uc = np.zeros(kroki)
    e = np.zeros(kroki)

    czas[0], i1[0], i2[0], uc[0], e[0] = t0, i1_0, i2_0, uc_0, e_func(t0)

    for k in range(kroki - 1):
        k1_i1, k1_i2, k1_uc = pochodne(czas[k], i1[k], i2[k], uc[k], e[k])
        t_pol = czas[k] + dt / 2
        i1_pol = i1[k] + (dt / 2) * k1_i1
        i2_pol = i2[k] + (dt / 2) * k1_i2
        uc_pol = uc[k] + (dt / 2) * k1_uc
        e_pol = e_func(t_pol)

        k2_i1, k2_i2, k2_uc = pochodne(t_pol, i1_pol, i2_pol, uc_pol, e_pol)

        i1[k + 1] = i1[k] + dt * k2_i1
        i2[k + 1] = i2[k] + dt * k2_i2
        uc[k + 1] = uc[k] + dt * k2_uc
        czas[k + 1] = czas[k] + dt
        e[k + 1] = e_func(czas[k + 1])

    return czas, i1, i2, uc, e