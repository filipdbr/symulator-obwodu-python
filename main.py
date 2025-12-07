import sys
import os
from kod_zrodlowy.czesc_1.projekt_czesc_1 import wykonaj_czesc_1
from kod_zrodlowy.czesc_2.projekt_czesc_2 import wykonaj_czesc_2
from kod_zrodlowy.czesc_3.projekt_czesc_3 import wykonaj_czesc_3
from kod_zrodlowy.czesc_4.projekt_czesc_4 import wykonaj_czesc_4

# dodaję katalogi z częściami do ścieżki dla łatwego importu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'czesc_1'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'czesc_2'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'czesc_3'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'czesc_4'))

def main():

    print("Autor: Filip Dąbrowski\nNr indeksu: 341057\n")

    while True:
        print("Menu główne - projekt - metody numeryczne")
        print("1. Część 1 - Symulator stanu nieustalonego (metody Eulera)")
        print("2. Część 2 - Obwód z nieliniową indukcyjnością")
        print("3. Część 3 - Obliczanie mocy czynnej")
        print("4. Część 4 - Znajdowanie częstotliwości dla mocy 406 W")
        print("5. Wykonaj wszystkie części po kolei")
        print("0. Wyjście")

        wybor = input("Wybierz opcję (0-5): ").strip()

        if wybor == "1":
            wykonaj_czesc_1()
        elif wybor == "2":
            wykonaj_czesc_2()
        elif wybor == "3":
            wykonaj_czesc_3()
        elif wybor == "4":
            wykonaj_czesc_4()
        elif wybor == "5":
            # wykonywanie wszystkich części
            czesci = [wykonaj_czesc_1, wykonaj_czesc_2, wykonaj_czesc_3, wykonaj_czesc_4]
            for i, czesc in enumerate(czesci, start=1):
                print(f"\nUruchamianie części {i}...")
                czesc()
        elif wybor == "0":
            print("Do widzenia!")
            break
        else:
            print("Nieprawidłowy wybór. Wybierz ponownie.")

        input("\nNaciśnij Enter, aby kontynuować...")

if __name__ == "__main__":
    main()