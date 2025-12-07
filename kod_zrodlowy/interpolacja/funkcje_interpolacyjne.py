import numpy as np

"""
Moduł zawierające funkcje interpolacyjne oraz ekstrapolacyjne:
a) interpolacja wielomianem Legrange'a,
b) interpolacja funkcjami sklejanymi trzeciego stopnia,
c) aproksymacja wielomianowa dowolnego stopnia
"""

def lagrange(x, x_wezly, y_wezly):
    n = len(x_wezly)
    suma = 0.0
    for i in range(n):
        iloczyn = y_wezly[i]
        for j in range(n):
            if j != i:
                iloczyn *= (x - x_wezly[j]) / (x_wezly[i] - x_wezly[j])
        suma += iloczyn
    return suma

def interpolacja_funkcje_sklejane(x_wezly, y_wezly):

    n = len(x_wezly) - 1
    h = np.diff(x_wezly)
    A = np.zeros((n+1, n+1))
    b = np.zeros(n+1)
    A[0, 0] = 1
    A[-1, -1] = 1
    for i in range(1, n):
        A[i, i-1] = h[i-1]
        A[i, i] = 2*(h[i-1]+h[i])
        A[i, i+1] = h[i]
        b[i] = 3 * ((y_wezly[i+1]-y_wezly[i])/h[i] - (y_wezly[i]-y_wezly[i-1])/h[i-1])
    M2 = np.linalg.solve(A, b)      # <-- rozwiązuje równanie różniczkowe

    wspolczynniki = []
    for i in range(n):
        a = y_wezly[i]
        b_ = (y_wezly[i+1]-y_wezly[i])/h[i] - h[i]*(2*M2[i]+M2[i+1])/6
        c = M2[i]/2
        d = (M2[i+1]-M2[i])/(6*h[i])
        wspolczynniki.append({'x0': x_wezly[i],'x1': x_wezly[i+1],'a': a,'b': b_,'c': c,'d': d})

    def splajn(x):
        if x <= x_wezly[0]:
            przedzial = wspolczynniki[0]
        elif x >= x_wezly[-1]:
            przedzial = wspolczynniki[-1]
        else:
            for i in range(len(wspolczynniki)):
                if wspolczynniki[i]['x0'] <= x <= wspolczynniki[i]['x1']:
                    przedzial = wspolczynniki[i]
                    break
            else:
                przedzial = wspolczynniki[-1]
        dx = x - przedzial['x0']
        return przedzial['a'] + przedzial['b'] * dx + przedzial['c'] * dx ** 2 + przedzial['d'] * dx ** 3

    return splajn


def aproksymacja_wielomianowa(x_wezly, y_wezly, stopien):

    n = len(x_wezly)
    liczba_wspolczynnikow = stopien + 1

    X = np.zeros((n, liczba_wspolczynnikow))

    for i in range(liczba_wspolczynnikow):
        X[:, i] = x_wezly ** i

    A = X.T @ X
    b = X.T @ y_wezly

    wsp = np.linalg.solve(A, b)

    # zwróć współczynniki w odwrotnej kolejności (od najwyższej potęgi)
    return wsp[::-1]