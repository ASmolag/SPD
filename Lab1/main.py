from Johnson import Alg_Johnsona
from przeglad import przeglad_zupelny
from pomoc import wczytaj_plik, generowaniePrzebiegowLosowych, rozpisanie_zadan, harmonogram, sortowanie
import time

dane = wczytaj_plik('data.txt')
#dane = generowaniePrzebiegowLosowych(7,2)

M1,M2,M3=rozpisanie_zadan(dane)

#Przeglad zupelny
t0pz = time.time()
tablica1, tablica2, tablica3, sums, min, indeks = przeglad_zupelny(M1,M2,M3)
t1pz = time.time()

totalpz = t1pz-t0pz

#Algorytm Johnsona
t0j = time.time()
kolejnosc=Alg_Johnsona(M1,M2,M3)
t1j = time.time()

totalj = t1j-t0j
tmp1,tmp2,tmp3=sortowanie(M1,M2,M3,kolejnosc)


print("Wprowadzone dane to:")
if M3!=0:
    print(M1,M2,M3)
else:
    print(M1,M2)

print('Rezultaty algorytmu Johnsona:')
print("Optymalna kolejność dla tego zestawu danych: {}".format(kolejnosc))
print('Realizowana przez ustawienie:')
if M3!=0:
    print(tmp1,tmp2,tmp3)
else:
    print(tmp1,tmp2)
print('Total makespan = {}'.format(harmonogram(tmp1,tmp2,tmp3)))
print('Czas wykonywania dla algorytmu Johnsona:{} '.format(totalj))
print()
print('Rezultaty dla przeglądu zupełnego:')
#print('Wygenerowano przebiegi:')
#print(tablica1)
#print(tablica2)
#print(tablica3)
print("Cmax dla koljenych permutacji: {}".format(sums))
print("Optymalne Cmax = {}".format(min))
print("Optymlana koljeność wg przeglądu zupełnego to:")
if tablica3!=0:
    print(tablica1[indeks],tablica2[indeks],tablica3[indeks])
else:
    print(tablica1[indeks], tablica2[indeks])
print('Czas wykonania dla przeglądu zupełnego: {}'.format(totalpz))