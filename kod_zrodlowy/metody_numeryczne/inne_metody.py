"""
Moduł zawiera metody pomocne przy czwartej części projektu.
Oprócz klasycznej implementacji, wdrażam liczniki zgodnie ze stawianymi wymaganiami.
"""

def metoda_bisekcji(funkcja, a, b, dokladnosc=1e-4, maks_iteracji=50):

    liczba_iteracji = 0
    liczba_ewaluacji = 0

    fa = funkcja(a)
    fb = funkcja(b)
    liczba_ewaluacji += 2   # ponieważ przed chwilą wykonano 2 ewaluacje

    if fa * fb > 0:
        print("Funkcja nie zmienia znaku na końcach przedziału")
        return None, None, liczba_iteracji, liczba_ewaluacji

    for i in range(maks_iteracji):
        liczba_iteracji += 1
        c = (a + b) / 2
        fc = funkcja(c)
        liczba_ewaluacji += 1

        if abs(fc) < dokladnosc:
            return c, fc, liczba_iteracji, liczba_ewaluacji

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    # tylko przy przekroczeniu maksymalnej liczby iteracji
    c = (a + b) / 2
    fc = funkcja(c)
    liczba_ewaluacji += 1
    return c, fc, liczba_iteracji, liczba_ewaluacji


def metoda_siecznych(funkcja, x0, x1, dokladnosc=1e-4, maks_iteracji=50):

    liczba_iteracji = 0
    liczba_ewaluacji = 0

    f0 = funkcja(x0)
    f1 = funkcja(x1)
    liczba_ewaluacji += 2

    for i in range(maks_iteracji):
        liczba_iteracji += 1

        # zabezpieczenie przed dzieleniem przez zero
        if abs(f1 - f0) < 1e-12:
            break

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = funkcja(x2)
        liczba_ewaluacji += 1

        if abs(f2) < dokladnosc:
            return x2, f2, liczba_iteracji, liczba_ewaluacji

        x0, x1 = x1, x2
        f0, f1 = f1, f2

    return x1, f1, liczba_iteracji, liczba_ewaluacji


def metoda_quasi_newton(funkcja, x0, delta=0.01, dokladnosc=1e-4, maks_iteracji=50):

    liczba_iteracji = 0
    liczba_ewaluacji = 0

    x = x0

    fx = funkcja(x)
    liczba_ewaluacji += 1

    for i in range(maks_iteracji):
        liczba_iteracji += 1

        if abs(fx) < dokladnosc:
            return x, fx, liczba_iteracji, liczba_ewaluacji

        fx_delta = funkcja(x + delta)
        liczba_ewaluacji += 1
        pochodna = (fx_delta - fx) / delta

        if abs(pochodna) < 1e-12:
            break

        x = x - fx / pochodna

        fx = funkcja(x)
        liczba_ewaluacji += 1

    return x, fx, liczba_iteracji, liczba_ewaluacji