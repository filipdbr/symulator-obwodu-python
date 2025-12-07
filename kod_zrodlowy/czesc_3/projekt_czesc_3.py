from matplotlib import pyplot as plt
from kod_zrodlowy.narzedzia import stworz_katalog, przygotuj_wykres, zapisz_wykres
from kod_zrodlowy.calkowanie import metoda_prostokatow, metoda_parabol
from kod_zrodlowy.wymuszenia import wymuszenia_slownik
from parametry import R1, R2
from kod_zrodlowy.obwody import rozwiaz_obwod_liniowy, rozwiaz_obwod_nieliniowy, stworz_funkcje_M_sklejane

# TODO: zrobić jawny import

def wykonaj_czesc_3():

    katalog = stworz_katalog(3)
    wykres = przygotuj_wykres("Część 3: obliczanie mocy czynnej na rezystorach")

    # test dla e(t) = 1 V ok na potrzeby weryfikacji
    print("\nTest dla e(t) = 1 V")

    dt = 0.001

    # obwód liniowy
    t_lin, i1_lin, i2_lin, uc_lin = rozwiaz_obwod_liniowy(wymuszenia_slownik['1V'], dt)
    P_prost_lin = metoda_prostokatow(i1_lin, i2_lin, R1, R2, dt)
    P_para_lin = metoda_parabol(i1_lin, i2_lin, R1, R2, dt)

    # obwód nieliniowy
    M_nieliniowe = stworz_funkcje_M_sklejane()
    t_nlin, i1_nlin, i2_nlin, uc_nlin = rozwiaz_obwod_nieliniowy(wymuszenia_slownik['1V'], dt, funkcja_M=M_nieliniowe)
    P_prost_nlin = metoda_prostokatow(i1_nlin, i2_nlin, R1, R2, dt)
    P_para_nlin = metoda_parabol(i1_nlin, i2_nlin, R1, R2, dt)

    print(f"Liniowy (M=0.8H):")
    print(f"  Metoda prostokątów: {P_prost_lin:.4f} W")
    print(f"  Metoda parabol:     {P_para_lin:.4f} W")

    print(f"Nieliniowy (M(u)):")
    print(f"  Metoda prostokątów: {P_prost_nlin:.4f} W")
    print(f"  Metoda parabol:     {P_para_nlin:.4f} W")
    print(f"  Różnica względem liniowego: {abs(P_para_nlin - P_para_lin):.4f} W")

    # test dla e(t) = sin(t) ----
    print("\nTest dla e(t) = sin(t)")

    t_lin, i1_lin, i2_lin, uc_lin = rozwiaz_obwod_liniowy(wymuszenia_slownik['sin'], dt)
    P_para_lin_sin = metoda_parabol(i1_lin, i2_lin, R1, R2, dt)

    t_nlin, i1_nlin, i2_nlin, uc_nlin = rozwiaz_obwod_nieliniowy(wymuszenia_slownik['sin'], dt)
    P_para_nlin_sin = metoda_parabol(i1_nlin, i2_nlin, R1, R2, dt)

    print(f"Wartość oczekiwana: 3.69 W")
    print(f"Liniowy - metoda parabol: {P_para_lin_sin:.4f} W (różnica: {abs(P_para_lin_sin - 3.69):.4f} W)")
    print(f"Nieliniowy - metoda parabol: {P_para_nlin_sin:.4f} W (różnica: {abs(P_para_nlin_sin - 3.69):.4f} W)")

    # obliczenia dla wszystkich wymuszeń
    print("\nObliczenia dla wszystkich wymuszeń")

    dt_wartosci = [0.001, 0.1]
    wymuszenia = [
        ("1 V", wymuszenia_slownik['1V']),
        ("120 prostokat", wymuszenia_slownik['prostokatne']),
        ("240*sin(t)", wymuszenia_slownik['240_sin']),
        ("210*sin(10pi t)", wymuszenia_slownik['210_sin_5Hz']),
        ("120*sin(100pi t)", wymuszenia_slownik['120_sin_50Hz'])
    ]

    wyniki_liniowe = []
    wyniki_nieliniowe = []

    for nazwa, e_funkcja in wymuszenia:
        wiersz_lin = [nazwa]
        wiersz_nlin = [nazwa]

        for dt in dt_wartosci:

            # liniowy
            t, i1, i2, uc = rozwiaz_obwod_liniowy(e_funkcja, dt)
            wiersz_lin.append(metoda_prostokatow(i1, i2, R1, R2, dt))
            wiersz_lin.append(metoda_parabol(i1, i2, R1, R2, dt))

            # nieliniowy
            t, i1, i2, uc = rozwiaz_obwod_nieliniowy(e_funkcja, dt)
            wiersz_nlin.append(metoda_prostokatow(i1, i2, R1, R2, dt))
            wiersz_nlin.append(metoda_parabol(i1, i2, R1, R2, dt))

        wyniki_liniowe.append(wiersz_lin)
        wyniki_nieliniowe.append(wiersz_nlin)

    # tabele wynikowe
    print("Moc całkowita P [W] - Przypadek liniowy (M=0.8H)")
    print("-" * 100)
    print(f"{'Wymuszenie':<20} {'Prost(dt=0.001)':>20} {'Para(dt=0.001)':>20} {'Prost(dt=0.1)':>20} {'Para(dt=0.1)':>20}")

    for wiersz in wyniki_liniowe:
        print(f"{wiersz[0]:<20} {wiersz[1]:>20.3f} {wiersz[2]:>20.3f} {wiersz[3]:>20.3f} {wiersz[4]:>20.3f}")

    print("")

    print("Moc całkowita P [W] - Przypadek nieliniowy")
    print("-" * 100)
    print(f"{'Wymuszenie':<20} {'Prost(dt=0.001)':>20} {'Para(dt=0.001)':>20} {'Prost(dt=0.1)':>20} {'Para(dt=0.1)':>20}")

    for wiersz in wyniki_nieliniowe:
        print(f"{wiersz[0]:<20} {wiersz[1]:>20.3f} {wiersz[2]:>20.3f} {wiersz[3]:>20.3f} {wiersz[4]:>20.3f}")

    # wykresy dla 240*sin(t)
    print("\nGenerowanie wykresów porównawczych dla 240*sin(t)")

    wykres, osie = plt.subplots(2, 2, figsize=(12, 8))

    for idx, dt in enumerate(dt_wartosci):

        # liniowy
        t_lin, i1_lin, i2_lin, uc_lin = rozwiaz_obwod_liniowy(wymuszenia_slownik['240_sin'], dt)
        P_lin = R1 * i1_lin ** 2 + R2 * i2_lin ** 2

        # nieliniowy
        t_nlin, i1_nlin, i2_nlin, uc_nlin = rozwiaz_obwod_nieliniowy(wymuszenia_slownik['240_sin'], dt)
        P_nlin = R1 * i1_nlin ** 2 + R2 * i2_nlin ** 2

        # prądy
        osie[0, idx].plot(t_lin, i1_lin, 'r-', label='i1 liniowy', linewidth=0.8)
        osie[0, idx].plot(t_lin, i2_lin, 'b-', label='i2 liniowy', linewidth=0.8)
        osie[0, idx].plot(t_nlin, i1_nlin, 'r--', label='i1 nieliniowy', linewidth=0.8, alpha=0.7)
        osie[0, idx].plot(t_nlin, i2_nlin, 'b--', label='i2 nieliniowy', linewidth=0.8, alpha=0.7)
        osie[0, idx].set_title(f'Prądy (dt={dt}s)')
        osie[0, idx].set_xlabel('Czas [s]')
        osie[0, idx].set_ylabel('Prąd [A]')
        osie[0, idx].legend(fontsize='small')
        osie[0, idx].grid(True, alpha=0.3)

        # moc
        osie[1, idx].plot(t_lin, P_lin, 'g-', label='moc liniowa', linewidth=0.8)
        osie[1, idx].plot(t_nlin, P_nlin, 'g--', label='moc nieliniowa', linewidth=0.8, alpha=0.7)
        osie[1, idx].fill_between(t_lin, 0, P_lin, alpha=0.3, color='green')
        osie[1, idx].set_title(f'Moc chwilowa (dt={dt}s)')
        osie[1, idx].set_xlabel('Czas [s]')
        osie[1, idx].set_ylabel('Moc [W]')
        osie[1, idx].legend(fontsize='small')
        osie[1, idx].grid(True, alpha=0.3)

    plt.suptitle('Porównanie liniowego i nieliniowego: e(t)=240·sin(t)')
    plt.tight_layout()
    zapisz_wykres(wykres, 'porownanie_240sint.png', katalog, dpi=150)

    # wykres dla e(t) = 1 V
    print("\nGenerowanie wykresów porównawczych dla e(t) = 1 V")

    # Oblicz moc chwilową dla przypadku liniowego
    P_chwilowa_lin = R1 * i1_lin ** 2 + R2 * i2_lin ** 2

    wykres, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # moc chwilowa
    ax1.plot(t_lin, P_chwilowa_lin, 'b-', label='Liniowy (M=0.8H)', linewidth=1.5)
    ax1.plot(t_nlin, R1 * i1_nlin ** 2 + R2 * i2_nlin ** 2, 'r--', label='Nieliniowy (M(u))', linewidth=1.5)
    ax1.fill_between(t_lin, 0, P_chwilowa_lin, alpha=0.2, color='blue')
    ax1.fill_between(t_nlin, 0, R1 * i1_nlin ** 2 + R2 * i2_nlin ** 2, alpha=0.2, color='red')
    ax1.set_xlabel('Czas [s]')
    ax1.set_ylabel('Moc [W]')
    ax1.set_title('Moc chwilowa P(t) dla e(t) = 1 V')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # prądy
    ax2.plot(t_lin, i1_lin, 'r-', label='i1 liniowy', linewidth=1.5)
    ax2.plot(t_lin, i2_lin, 'b-', label='i2 liniowy', linewidth=1.5)
    ax2.plot(t_nlin, i1_nlin, 'r--', label='i1 nieliniowy', linewidth=1.5, alpha=0.8)
    ax2.plot(t_nlin, i2_nlin, 'b--', label='i2 nieliniowy', linewidth=1.5, alpha=0.8)
    ax2.set_xlabel('Czas [s]')
    ax2.set_ylabel('Prąd [A]')
    ax2.set_title('Prądy w obwodzie dla e(t) = 1 V')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    zapisz_wykres(wykres, 'porownanie_1V.png', katalog, dpi=150)

    print("\nCzęść 3 zakończona")


if __name__ == "__main__":
    wykonaj_czesc_3()