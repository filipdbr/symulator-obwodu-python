import numpy as np
"""
Moduł zawiera parametry z zadania.
Zmieniając parametry w tym miejscu, program przeprowadzi symulacje dla tychże danych.

Komentarz: w dalszym rozwoju programu można by również dodać krok czasowy, amplitudę itd.
"""
## Obwód liniowy

# parametry obwodu z projektu (część 1, 3, 4)
R1, R2, C = 0.1, 10.0, 0.5
L1, L2, M = 3.0, 5.0, 0.8

# stałe do równań
D1 = L1 / M - M / L2
D2 = M / L1 - L2 / M

## Obwód nieliniowy

# dane z tabeli z zadania
u_L1_tablica = np.array([20, 50, 100, 150, 200, 250, 280, 300])
M_tablica = np.array([0.46, 0.64, 0.78, 0.68, 0.44, 0.23, 0.18, 0.18])