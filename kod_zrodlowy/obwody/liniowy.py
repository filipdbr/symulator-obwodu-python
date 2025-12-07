from ..metody_numeryczne.ulepszona_metoda_eulera import ulepszona_metoda_eulera
from ..metody_numeryczne.metoda_eulera import metoda_eulera
from parametry import *
"""
Moduł zawiera parametry oraz funkcje specyficzne dla obwodu liniowego
"""

def pochodne_liniowe(t, i1, i2, uc, e):
    di1 = (1/D1) * (-R1/M*i1 + R2/L2*i2 - uc/M + e/M)
    di2 = (1/D2) * (-R1/L1*i1 + R2/M*i2 - uc/L1 + e/L1)
    duc = i1 / C
    return di1, di2, duc

# wrappery dla metod Eulera
def metoda_eulera_liniowa(e_func, t0, tk, dt, i1_0, i2_0, uc_0):
    return metoda_eulera(e_func, t0, tk, dt, i1_0, i2_0, uc_0, pochodne_liniowe)

def ulepszona_metoda_eulera_liniowa(e_func, t0, tk, dt, i1_0, i2_0, uc_0):
    return ulepszona_metoda_eulera(e_func, t0, tk, dt, i1_0, i2_0, uc_0, pochodne_liniowe)

# Rozwiązuje obwód liniowy i zwraca tylko czas, prądy i napięcie
def rozwiaz_obwod_liniowy(e_funkcja, dt, T=30, t0=0.0, i1_0=0.0, i2_0=0.0, uc_0=0.0):
    czas, i1, i2, uc, e = ulepszona_metoda_eulera_liniowa(e_funkcja, t0, T, dt, i1_0, i2_0, uc_0)
    return czas, i1, i2, uc