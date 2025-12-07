import numpy as np
from kod_zrodlowy.obwody import ulepszona_metoda_eulera_liniowa
from parametry import R1, R2
from kod_zrodlowy.calkowanie import metoda_parabol

"""
Moduł zawiera funkcje pomocnicze dla części 4 projektu
"""

# ozwiązuje obwód dla wymuszenia e(t) = 100*sin(2πft)
def rozwiaz_obwod_dla_f(czestotliwosc, krok_czasowy=0.001, czas_symulacji=30):
    t0, i1_0, i2_0, uc_0 = 0.0, 0.0, 0.0, 0.0

    # podstawiam wzór na wymuszenie z projektu
    wymuszenie = lambda t: 100.0 * np.sin(2 * np.pi * czestotliwosc * t)

    czas, i1, i2, uc, _ = ulepszona_metoda_eulera_liniowa(
        wymuszenie, t0, czas_symulacji, krok_czasowy, i1_0, i2_0, uc_0
    )

    return czas, i1, i2, uc

# oblicza moc całkowitą dla danej częstotliwości
def oblicz_moc_dla_f(czestotliwosc, krok_czasowy=0.001):
    czas, i1, i2, uc = rozwiaz_obwod_dla_f(czestotliwosc, krok_czasowy)
    return metoda_parabol(i1, i2, R1, R2, krok_czasowy)


# funkcja celu F(f) = P(f) - 406
def funkcja_celu(czestotliwosc):
    return oblicz_moc_dla_f(czestotliwosc) - 406