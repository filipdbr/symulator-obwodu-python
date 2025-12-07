import numpy as np
from kod_zrodlowy.narzedzia import *
from kod_zrodlowy.obwody import symuluj_z_zapisywaniem_M
from parametry import u_L1_tablica, M_tablica
from kod_zrodlowy.interpolacja import lagrange, interpolacja_funkcje_sklejane, aproksymacja_wielomianowa
from kod_zrodlowy.metody_numeryczne import ulepszona_metoda_eulera
from kod_zrodlowy.wymuszenia import wymuszenia_slownik

def wykonaj_czesc_2():

    katalog = stworz_katalog(2)
    wykres = przygotuj_wykres("Część 2: symulator obwodu z nieliniową indukcyjnością")

    # twórz wykres porównawczy metod
    print("\nGenerowanie wykresu porównawczego...")

    # tworzenie funkcji M(u) różnymi metodami
    def M_lagrange(u):
        return lagrange(u, u_L1_tablica, M_tablica)

    splajn = interpolacja_funkcje_sklejane(u_L1_tablica, M_tablica)
    def M_funkcje_sklejane(u):
        return splajn(u)

    wsp_3 = aproksymacja_wielomianowa(u_L1_tablica, M_tablica, 3)
    def M_wielomian_3(u):
        return wsp_3[0] * u ** 3 + wsp_3[1] * u ** 2 + wsp_3[2] * u + wsp_3[3]

    wsp_5 = aproksymacja_wielomianowa(u_L1_tablica, M_tablica, 5)
    def M_wielomian_5(u):
        return (wsp_5[0] * u ** 5 + wsp_5[1] * u ** 4 + wsp_5[2] * u ** 3 + wsp_5[3] * u ** 2 + wsp_5[4] * u + wsp_5[5])

    # rysój wykres
    u_test = np.linspace(0, 320, 1000)
    wykres = plt.figure(figsize=(12, 8))

    plt.plot(u_L1_tablica, M_tablica, 'ko', markersize=8, label='dane z tabeli')
    plt.plot(u_test, [M_lagrange(u) for u in u_test], 'b-', linewidth=1.5, label='lagrange')
    plt.plot(u_test, [M_funkcje_sklejane(u) for u in u_test], 'r--', linewidth=1.5, label='funkcje sklejane')
    plt.plot(u_test, [M_wielomian_3(u) for u in u_test], 'g-.', linewidth=1.5, label='wielomian 3')
    plt.plot(u_test, [M_wielomian_5(u) for u in u_test], 'm:', linewidth=1.5, label='wielomian 5')

    plt.axvline(x=78, color='gray', linestyle=':', alpha=0.6)
    plt.xlabel('napięcie u_L1 [V]')
    plt.ylabel('indukcyjność M [H]')
    plt.title('porównanie metod interpolacji')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 320)
    plt.ylim(0, 1.0)
    plt.tight_layout()

    zapisz_wykres(wykres, "wykres_porownawczy.png", katalog)

    # symulacje dla 2 wymuszeń i 4 metod
    print("\nUruchamiam symulacje...")

    metody = [
        ("Lagrange", M_lagrange),
        ("Funkcje sklejane", M_funkcje_sklejane),
        ("Wielomian st. 3", M_wielomian_3),
        ("Wielomian st. 5", M_wielomian_5)
    ]

    wymuszenia = [
        ("240*sin(t)", wymuszenia_slownik['240_sin']),
        ("120*sin(2pi*50*t)", wymuszenia_slownik['120_sin_50Hz'])
    ]

    wyniki = {}
    for nazwa_wym, wymuszenie in wymuszenia:
        print(f"\nSymulacja dla wymuszenia: {nazwa_wym}")
        wyniki_wym = {}

        for nazwa_metody, funkcja_M in metody:
            print(f"  Metoda: {nazwa_metody}")

            # uniwersalna funkcja zapisująca dla układu nieliniowego
            czas, i1, i2, uc, M = symuluj_z_zapisywaniem_M(wymuszenie, funkcja_M, ulepszona_metoda_eulera)

            wyniki_wym[nazwa_metody] = {'czas': czas, 'i1': i1, 'i2': i2, 'uc': uc, 'M': M}

        wyniki[nazwa_wym] = wyniki_wym

    # rysowanie wykresów z wynikami
    def rysuj_wykresy(wyniki, nazwa_wym, folder):

        wykres, osie = plt.subplots(2, 2, figsize=(14, 10))
        wykres.suptitle(f'wyniki dla {nazwa_wym}')

        kolory = ['blue', 'red', 'green', 'purple']
        styl = ['-', '--', '-.', ':']
        grub = [1.5, 1.2, 1.2, 1.2]

        os_x_1, os_x_2, os_x_3, os_x_4 = osie.flatten()
        dane = wyniki[nazwa_wym]

        for i, (met, _) in enumerate(metody):
            d = dane[met]
            os_x_1.plot(d['czas'], d['i1'], color=kolory[i], linestyle=styl[i], linewidth=grub[i], label=met)
            os_x_2.plot(d['czas'], d['i2'], color=kolory[i], linestyle=styl[i], linewidth=grub[i], label=met)
            os_x_3.plot(d['czas'], d['uc'], color=kolory[i], linestyle=styl[i], linewidth=grub[i], label=met)
            os_x_4.plot(d['czas'], d['M'], color=kolory[i], linestyle=styl[i], linewidth=grub[i], label=met)

        os_x_1.set(title='prąd i1', xlabel='czas [s]', ylabel='i1 [A]')
        os_x_2.set(title='prąd i2', xlabel='czas [s]', ylabel='i2 [A]')
        os_x_3.set(title='napięcie uc', xlabel='czas [s]', ylabel='uc [V]')
        os_x_4.set(title='indukcyjność M', xlabel='czas [s]', ylabel='M [H]', ylim=(0, 1))

        for os in [os_x_1, os_x_2, os_x_3, os_x_4]:
            os.grid(True, alpha=0.3)
            os.legend()
            os.set_xlim(0, 30)

        plt.tight_layout()

        if nazwa_wym == "240*sin(t)":
            nazwa_pliku = "240sin_t.png"
        else:
            nazwa_pliku = "120sin_10_pi_t.png"

        zapisz_wykres(wykres, nazwa_pliku, folder)

    print("\nGeneruję wykresy symulacji...")
    for nazwa_wym, _ in wymuszenia:
        rysuj_wykresy(wyniki, nazwa_wym, katalog)

    # tabela porównawcza
    print("\nWatości M dla punktów z tabeli z projektu:")
    print("u[V] | tabela | lagrange  | sklejane | wiel.3 | wiel.5")

    for i in range(len(u_L1_tablica)):
        u = u_L1_tablica[i]
        print(f"{u:4.0f} | {M_tablica[i]:6.3f} | {M_lagrange(u):8.3f} | "
              f"{M_funkcje_sklejane(u):9.3f} | {M_wielomian_3(u):6.3f} | "
              f"{M_wielomian_5(u):6.3f}")

    print("\nCzęść 2 zakończona")


if __name__ == "__main__":
    wykonaj_czesc_2()