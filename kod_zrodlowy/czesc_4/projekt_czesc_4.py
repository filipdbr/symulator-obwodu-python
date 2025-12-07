from kod_zrodlowy.narzedzia import *
from kod_zrodlowy.obwody import *
from kod_zrodlowy.metody_numeryczne import metoda_bisekcji, metoda_siecznych, metoda_quasi_newton
from kod_zrodlowy.czesc_4 import funkcja_celu, oblicz_moc_dla_f

# TODO: zrobić jawny import

def wykonaj_czesc_4():

    katalog = stworz_katalog(4)
    wykres = przygotuj_wykres("Część 4: znajdowanie częstotliwości dla mocy 406 W")

    # wybranie delta F dla metody quasi Newtona
    print("\nSzukanie delta f dla quasi-Newtona")

    czestotliwosc_test = 5.0  # Hz
    wartosci_delta = [0.5, 0.1, 0.05, 0.01, 0.005, 0.001]

    print(f"{'delta f':<10} {'Pochodna':<15} {'Pochodna(detla f/2)':<15} {'Różnica %':<10}")
    print("-" * 60)

    F_test = funkcja_celu(czestotliwosc_test)
    wybrane_delta = wartosci_delta[2]  # domyślnie 0.05

    for delta in wartosci_delta:
        F_plus = funkcja_celu(czestotliwosc_test + delta)
        pochodna1 = (F_plus - F_test) / delta

        F_plus_pol = funkcja_celu(czestotliwosc_test + delta / 2)
        pochodna2 = (F_plus_pol - F_test) / (delta / 2)

        if abs(pochodna2) > 1e-10:
            roznica = abs(pochodna1 - pochodna2) / abs(pochodna2) * 100
        else:
            roznica = 100

        print(f"{delta:<10.4f} {pochodna1:<15.6f} {pochodna2:<15.6f} {roznica:<10.2f}")

        if roznica < 1.0:  # warunek z zadania: różnica < 1%
            wybrane_delta = delta

    print(f"\nWybrano delta f = {wybrane_delta:.4f} (różnica < 1%)")

    # szukanie przedziału początkowego
    print("\nSzukanie przedziału początkowego")

    # test dla różnych częstotliwośći
    test_czestotliwosci = [0.01, 0.1, 0.5, 1, 2, 5, 10, 20, 50]
    przedzial_a, przedzial_b = None, None

    print(f"{'f [Hz]':<10} {'P [W]':<15} {'F(f)=P-406':<15}")

    wartosci_F = []
    for f_test in test_czestotliwosci:
        P_test = oblicz_moc_dla_f(f_test, krok_czasowy=0.001)
        F_wartosc = P_test - 406
        wartosci_F.append(F_wartosc)
        print(f"{f_test:<10.2f} {P_test:<15.2f} {F_wartosc:<15.2f}")

    # znajdź przedział gdzie F zmienia znak
    for i in range(len(test_czestotliwosci) - 1):
        if wartosci_F[i] * wartosci_F[i + 1] < 0:
            przedzial_a, przedzial_b = test_czestotliwosci[i], test_czestotliwosci[i + 1]
            print(f"\nZnaleziono przedział: [{przedzial_a:.3f}, {przedzial_b:.3f}] Hz")
            break

    if przedzial_a is None:
        print("\nNie znaleziono przedziału z różnymi znakami F(f).")
        print("Sprawdzamy maksymalną moc...")

        # Szukamy maksimum mocy
        maks_moc = 0
        maks_f = 0
        for f_test in test_czestotliwosci:
            P_test = oblicz_moc_dla_f(f_test, krok_czasowy=0.01)
            if P_test > maks_moc:
                maks_moc = P_test
                maks_f = f_test

        print(f"Maksymalna moc: {maks_moc:.2f} W przy f = {maks_f:.3f} Hz")

        if maks_moc < 406:
            print("Nie istnieje rozwiązanie (maksymalna moc < 406 W).")

        # usal przedział wokół maksimum
        przedzial_a, przedzial_b = maks_f * 0.8, maks_f * 1.2
        print(f"Ustalamy przedział: [{przedzial_a:.3f}, {przedzial_b:.3f}] Hz")

    # stosowanie metod bisekcji, siecznych i quasi-Newtona
    print("\nStosowanie metod numerycznych")

    wyniki = []

    wybrana_doklanosc = 1e-4

    # metoda bisekcji
    print("\nMetoda bisekcji:")
    f_bisekcji, F_bisekcji, iter_b, ewaluacje_b = metoda_bisekcji(funkcja_celu, przedzial_a, przedzial_b, wybrana_doklanosc)
    wyniki.append(["Bisekcji", f_bisekcji, F_bisekcji, iter_b, ewaluacje_b])
    print(f"  f = {f_bisekcji:.6f} Hz")
    print(f"  F(f) = {F_bisekcji:.6f}")
    print(f"  Iteracje: {iter_b}")
    print(f"  Ewaluacje: {ewaluacje_b}")

    # metoda siecznych
    print("\nMetoda siecznych:")
    f_siecznych, F_siecznych, iter_s, ewaluacje_s = metoda_siecznych(funkcja_celu, przedzial_a, przedzial_b, wybrana_doklanosc)
    wyniki.append(["Siecznych", f_siecznych, F_siecznych, iter_s, ewaluacje_s])
    print(f"  f = {f_siecznych:.6f} Hz")
    print(f"  F(f) = {F_siecznych:.6f}")
    print(f"  Iteracje: {iter_s}")
    print(f"  Ewaluacje: {ewaluacje_s}")

    # metoda quasi-Newtona
    print("\nMetoda quasi-Newtona:")
    f_newton, F_newton, iter_n, ewaluacje_n = metoda_quasi_newton(funkcja_celu, (przedzial_a + przedzial_b) / 2,delta=wybrane_delta, dokladnosc=wybrana_doklanosc)
    wyniki.append(["Quasi-Newtona", f_newton, F_newton, iter_n, ewaluacje_n])
    print(f"  f = {f_newton:.6f} Hz")
    print(f"  F(f) = {F_newton:.6f}")
    print(f"  Iteracje: {iter_n}")
    print(f"  Ewaluacje: {ewaluacje_n}")

    # tabela podsumowująca
    print("\nPodsumowanie:")
    print("-" * 100)
    print(f"{'Metoda':<20} {'f [Hz]':<15} {'F(f)':<15} {'Iteracje':<10} {'Ewaluacje':<15}")

    for wiersz in wyniki:
        print(f"{wiersz[0]:<20} {wiersz[1]:<15.6f} {wiersz[2]:<15.6f} {wiersz[3]:<10} {wiersz[4]:<15}")

    # wykres - funkcja celu F
    print("\nGenerowanie wykresu funkcji celu...")

    f_min, f_max = przedzial_a * 0.5, przedzial_b * 1.5
    f_punkty = np.linspace(f_min, f_max, 30)
    F_punkty = []

    for f in f_punkty:
        F_punkty.append(funkcja_celu(f))

    wykres, os_x_1 = plt.subplots(1, 1, figsize=(10, 6))

    os_x_1.plot(f_punkty, F_punkty, 'b-', linewidth=1.5)
    os_x_1.axhline(y=0, color='r', linestyle='--', linewidth=1, label='F(f)=0')

    kolory = ['red', 'green', 'purple']
    for idx, wiersz in enumerate(wyniki):

        os_x_1.plot(wiersz[1], wiersz[2], 'o', color=kolory[idx], markersize=8, label=f'{wiersz[0]}: f={wiersz[1]:.3f} Hz')

    os_x_1.set_xlabel('Częstotliwość f [Hz]')
    os_x_1.set_ylabel('F(f) = P(f) - 406 [W]')
    os_x_1.set_title('Funkcja celu F(f)')
    os_x_1.grid(True, alpha=0.3)
    os_x_1.legend()

    plt.tight_layout()
    zapisz_wykres(wykres, 'czesc4_wyniki.png', katalog, dpi=150)

    print("Część 4 zakończona")


if __name__ == "__main__":
    wykonaj_czesc_4()