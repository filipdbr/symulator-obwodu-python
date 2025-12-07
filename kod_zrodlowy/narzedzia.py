import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

"""
Moduł zawierający funkcje pomocnicze oraz parametry obwodu z zadania.
"""

def stworz_katalog(nr_czesci):
    folder = f"wykresy_czesc_{nr_czesci}"
    os.makedirs(folder, exist_ok=True)
    return folder

def przygotuj_wykres(tytul, autor="Filip Dąbrowski, nr indeksu: 341057"):
    print(f"\n{tytul}")
    print(f"Autor: {autor}")
    return plt.figure()

def zapisz_wykres(wykres, nazwa_pliku, folder, dpi=300):
    sciezka = os.path.join(folder, nazwa_pliku)
    wykres.savefig(sciezka, dpi=dpi)
    plt.close(wykres)
    print(f"Zapisano wykres: {sciezka}")
    return sciezka