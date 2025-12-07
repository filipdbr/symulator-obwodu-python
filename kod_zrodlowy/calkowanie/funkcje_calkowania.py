import numpy as np

"""
Moduł zawiera funkcje całkowania wykorzystywane w części 3 projektu.
"""

def metoda_prostokatow(i1, i2, R1, R2, dt):
    P = R1 * i1 ** 2 + R2 * i2 ** 2
    return np.sum(P) * dt

def metoda_parabol(i1, i2, R1, R2, dt):
    P = R1 * i1 ** 2 + R2 * i2 ** 2
    n = len(P)
    if n % 2 == 0:
        P = P[:-1]
        n -= 1

    suma = P[0] + P[-1]
    for i in range(1, n - 1, 2):
        suma += 4 * P[i]
    for i in range(2, n - 2, 2):
        suma += 2 * P[i]

    return (dt / 3) * suma