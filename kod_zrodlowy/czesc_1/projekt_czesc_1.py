import matplotlib.pyplot as plt
from kod_zrodlowy.narzedzia import stworz_katalog, zapisz_wykres, przygotuj_wykres
from kod_zrodlowy.wymuszenia import wymuszenia_slownik
from kod_zrodlowy.obwody.liniowy import metoda_eulera_liniowa, ulepszona_metoda_eulera_liniowa

# TODO: tytuły wykresów - dodać nazwę wymuszenia

def wykonaj_czesc_1():
    folder = stworz_katalog(nr_czesci = 1)
    wykres = przygotuj_wykres("Część 1: symulator obwodu ze sprzężeniem indukcyjnym")

    t0, tk, dt = 0.0, 30.0, 0.01
    i1_0, i2_0, uc_0 = 0.0, 0.0, 0.0

    wymuszenia = [
        ("prostokatne", wymuszenia_slownik['prostokatne']),
        ("240_sin", wymuszenia_slownik['240_sin']),
        ("210_sin_5Hz", wymuszenia_slownik['210_sin_5Hz']),
        ("120_sin_50Hz", wymuszenia_slownik['120_sin_50Hz'])
    ]

    wyniki = []

    for nazwa, wym in wymuszenia:
        print(f"\nPrzeprowadzanie symulacji dla: {nazwa}")

        czas_e, i1_e, i2_e, uc_e, e_e = metoda_eulera_liniowa(wym, t0, tk, dt, i1_0, i2_0, uc_0)
        czas_u, i1_u, i2_u, uc_u, e_u = ulepszona_metoda_eulera_liniowa(wym, t0, tk, dt, i1_0, i2_0, uc_0)

        wyniki.append((nazwa, czas_u, i1_u, i2_u, e_u))

        # rysuj wykresy
        wykres = plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.plot(czas_e, i1_e, 'b-', label='Euler')
        plt.plot(czas_u, i1_u, 'r--', label='Ulepszony Euler')
        plt.title('Prąd i1')
        plt.xlabel('Czas [s]')
        plt.ylabel('Prąd [A]')
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(czas_e, i2_e, 'b-', label='Euler')
        plt.plot(czas_u, i2_u, 'r--', label='Ulepszony Euler')
        plt.title('Prąd i2')
        plt.xlabel('Czas [s]')
        plt.ylabel('Prąd [A]')
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(czas_e, uc_e, 'g-', label='Euler')
        plt.plot(czas_u, uc_u, 'm--', label='Ulepszony Euler')
        plt.title('Napięcie na kondensatorze')
        plt.xlabel('Czas [s]')
        plt.ylabel('Napięcie [V]')
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 2, 4)
        plt.plot(czas_e, e_e, 'k-')
        plt.title('Wymuszenie e(t)')
        plt.xlabel('Czas [s]')
        plt.ylabel('Napięcie [V]')
        plt.grid(True)

        plt.tight_layout()
        zapisz_wykres(wykres, f'{nazwa}.png', folder)
        plt.close()

    print("\nWszystkie symulacje zakończone.\n")
    print("Generowanie wykresu zbiorczego...")

    wykres = plt.figure(figsize=(15, 10))
    for idx, (nazwa, czas, i1, i2, _) in enumerate(wyniki, 1):
        plt.subplot(2, 2, idx)
        plt.plot(czas, i1, 'b-', label='i1')
        plt.plot(czas, i2, 'r-', label='i2')
        plt.title(nazwa)
        plt.xlabel('Czas [s]')
        plt.ylabel('Prąd [A]')
        plt.grid(True)
        plt.legend()
        plt.xlim(0, 30)

    plt.tight_layout()
    zapisz_wykres(wykres, "czesc1_zbiorcze_i1_i2.png", folder)

    wykonaj_porownanie(folder)

    return wyniki


def wykonaj_porownanie(folder):
    print("\nGenerowanie wykresu porównawczego (wymuszenie sin(t))...")

    t0, tk, dt = 0.0, 30.0, 0.01
    i1_0, i2_0, uc_0 = 0.0, 0.0, 0.0

    czas_e, i1_e, i2_e, uc_e, _ = metoda_eulera_liniowa(wymuszenia_slownik['sin'], t0, tk, dt, i1_0, i2_0, uc_0)
    czas_u, i1_u, i2_u, uc_u, _ = ulepszona_metoda_eulera_liniowa(wymuszenia_slownik['sin'], t0, tk, dt, i1_0, i2_0, uc_0)

    fig = plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(czas_e, i1_e, 'b-', label='i1 Euler')
    plt.plot(czas_u, i1_u, 'b--', label='i1 Metoda Ulepszona')
    plt.plot(czas_e, i2_e, 'r-', label='i2 Euler')
    plt.plot(czas_u, i2_u, 'r--', label='i2 Metoda Ulepszona')
    plt.title('Wykres służący do weryfikacji prądów i1 i i2')
    plt.ylabel('Prąd [A]')
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(czas_e, uc_e, 'g-', label='uc Euler')
    plt.plot(czas_u, uc_u, 'm--', label='Metoda Ulepszona')
    plt.title('Wykres służący do weryfikacji napięcia na kondensatorze')
    plt.xlabel('Czas [s]')
    plt.ylabel('Napięcie [V]')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    zapisz_wykres(fig, "czesc1_do_porownania.png", folder)

    print("\nCzęść 1 zakończona")


if __name__ == "__main__":
    wykonaj_czesc_1()