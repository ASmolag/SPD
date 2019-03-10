import itertools
from main import wczytaj_plik, dane_do_tab, rozpisanie_zadan, harmonogram3, harmonogram
import time
#tablice testowe
#tab1=[5,4,4,1,3]
#tab2=[2,6,3,5,4]


M1,M2,M3=rozpisanie_zadan(dane_do_tab(wczytaj_plik('data.txt')))
#harmonogram(M1,M2,M3)
if M3!=0:
    t0 = time.time()
    tablica1=list(itertools.permutations(M1))
    tablica2=list(itertools.permutations(M2))
    tablica3=list(itertools.permutations(M3))
    sums3=[]
    min3 = 1000000
    a = 0
    for i in range(len(tablica1)):
        suma3 = harmonogram3(tablica1[i],tablica2[i], tablica3[i])
        if suma3 < min3:
            min3 = suma3
            a = i
        sums3.append(suma3)
#        print(suma3)
    t1 = time.time()
    print(tablica1)
    print(tablica2)
    print(tablica3)
    print("Cmax dla koljenych permutacji: {}".format(sums3))
    print("Optymalne Cmax = {}".format(min3))
    print("Optymlana koljeność to:")
    print(tablica1[a],tablica2[a],tablica3[a])
else:
    t0 = time.time()
    tablica1 = list(itertools.permutations(M1))
    tablica2 = list(itertools.permutations(M2))
    sums= []
    min2 = 1000000
    a = 0
    for i in range(len(tablica1)):
        suma2 = harmonogram(tablica1[i], tablica2[i])
        if suma2 < min2:
            min2=suma2
            a = i
        sums.append(suma2)
#       print(suma2)
    t1 = time.time()
    print(tablica1)
    print(tablica2)
    print("Cmax dla koljenych permutacji: {}".format(sums))
    print("Optymalne Cmax = {}".fomrat(min2))
    print("Optymlana koljeność to:")
    print(tablica1[a], tablica2[a])

total = t1-t0
print('Czas wykonywania przegladu zupelnego:{} '.format(total))