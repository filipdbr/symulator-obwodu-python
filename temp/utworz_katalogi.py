# tworzy strukturę katalogów
import os

katalogi_funkcjonalne = [
    "metody_numeryczne",
    "obwody",
    "wymuszenia",
    "interpolacja",
    "calkowanie",
    "temp"          # <- do developmentu
]

katalogi_projektowe = [
    "czesc_1",
    "czesc_2",
    "czesc_3",
    "czesc_4",
    "wykresy"
]

for katalog in katalogi_funkcjonalne + katalogi_projektowe:
    os.makedirs(katalog, exist_ok=True)

for katalog in katalogi_funkcjonalne:
    with open(f"{katalog}/__init__.py", "w") as plik:
        plik.write("")