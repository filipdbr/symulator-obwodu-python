# funkcje wymuszeń z projektu
import numpy as np

def wymuszenie_prostokatne(t):
    T = 3.0
    polowa = T / 2

    if (t % T) < polowa:
        return 120.0
    else:
        return 0.0

def wymuszenie_sinus_240(t):
    return 240.0 * np.sin(t)

def wymuszenie_sinus_210_5Hz(t):
    return 210.0 * np.sin(2 * np.pi * 5 * t)

def wymuszenie_sinus_120_50Hz(t):
    return 120.0 * np.sin(2 * np.pi * 50 * t)

def wymuszenie_stala_1V(t):
    return 1.0

def wymuszenie_sinus(t):
    return np.sin(t)

# słownik wymuszeń dla łatwego odwoływania się na zasadzie klucz / wartość. Tutaj: nazwa / funkcja
wymuszenia_slownik = {
    'prostokatne': wymuszenie_prostokatne,
    '240_sin': wymuszenie_sinus_240,
    '210_sin_5Hz': wymuszenie_sinus_210_5Hz,
    '120_sin_50Hz': wymuszenie_sinus_120_50Hz,
    '1V': wymuszenie_stala_1V,
    'sin': wymuszenie_sinus
}