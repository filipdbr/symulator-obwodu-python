from ..metody_numeryczne.ulepszona_metoda_eulera import ulepszona_metoda_eulera
from ..metody_numeryczne.metoda_eulera import metoda_eulera
from kod_zrodlowy.interpolacja import interpolacja_funkcje_sklejane
from parametry import *

"""
Moduł zawiera parametry oraz funkcje specyficzne dla obwodu nieliniowego
"""

def stworz_pochodne_nieliniowe(funkcja_M):

    def pochodne(t, i1, i2, uc, e):

        u_L1 = e - R1 * i1 - uc
        u_L1 = max(0, min(u_L1, 320))

        M_n = funkcja_M(u_L1)

        D1 = L1 / M_n - M_n / L2
        D2 = M_n / L1 - L2 / M_n

        di1 = (1 / D1) * (-R1 / M_n * i1 + R2 / L2 * i2 - uc / M_n + e / M_n)
        di2 = (1 / D2) * (-R1 / L1 * i1 + R2 / M_n * i2 - uc / L1 + e / L1)
        duc = i1 / C

        return di1, di2, duc

    return pochodne


def symuluj_z_zapisywaniem_M(wymuszenie, funkcja_M, metoda_numeryczna, dt=0.001, T=30):

    pochodne = stworz_pochodne_nieliniowe(funkcja_M)

    czas, i1, i2, uc, e_vals = metoda_numeryczna(wymuszenie, 0, T, dt, 0, 0, 0, pochodne)

    M_n = np.zeros_like(czas)
    for i in range(len(czas)):
        u_L1 = max(0, min(e_vals[i] - R1 * i1[i] - uc[i], 320))
        M_n[i] = funkcja_M(u_L1)

    return czas, i1, i2, uc, M_n

def metoda_eulera_nieliniowa(e_func, t0, tk, dt, i1_0, i2_0, uc_0, funkcja_M):
    pochodne = stworz_pochodne_nieliniowe(funkcja_M)
    return metoda_eulera(e_func, t0, tk, dt, i1_0, i2_0, uc_0, pochodne)

def ulepszona_metoda_eulera_nieliniowa(e_func, t0, tk, dt, i1_0, i2_0, uc_0, funkcja_M):
    pochodne = stworz_pochodne_nieliniowe(funkcja_M)
    return ulepszona_metoda_eulera(e_func, t0, tk, dt, i1_0, i2_0, uc_0, pochodne)

def rozwiaz_obwod_nieliniowy(e_funkcja, dt, T=30, funkcja_M=None):
    if funkcja_M is None:
        funkcja_M = stworz_funkcje_M_sklejane()
    t0, i1_0, i2_0, uc_0 = 0.0, 0.0, 0.0, 0.0
    czas, i1, i2, uc, e = ulepszona_metoda_eulera_nieliniowa( e_funkcja, t0, T, dt, i1_0, i2_0, uc_0, funkcja_M)
    return czas, i1, i2, uc

def stworz_funkcje_M_sklejane():
    splajn = interpolacja_funkcje_sklejane(u_L1_tablica, M_tablica)
    return splajn