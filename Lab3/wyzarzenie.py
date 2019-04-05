from neh import qNEH, Cmax
from pomoc import wczytaj_plik
import random
import math

def Wyzarzanie (Maszyny):

    #inicjalizacja
    C, Kolejnosc = qNEH(Maszyny)
    T = 1000
    mi = 0.8

    while T > 50:
        #generowanie ruchu
        Kolejnosc_prim = Swap(Kolejnosc)

        #Potencjalny ruch
        Cprim = Cmax(Maszyny, Kolejnosc_prim)

        if Cprim < C:
            p = 1

        else:
            p = math.exp((C - Cprim)/T)

        if p >= random.random(): #Warunek ruchu
            Kolejnosc = Kolejnosc_prim[:]
            C = Cprim

        #Schładzanie
        T = mi*T

    return C, Kolejnosc


def Swap(Kolejnosc):
    tmp = Kolejnosc[:]
    miejsce_zadanie1 = random.randrange(len(Kolejnosc))
    miejsce_zadanie2 = miejsce_zadanie1
    while miejsce_zadanie1 == miejsce_zadanie2:
        miejsce_zadanie2 = random.randrange(len(Kolejnosc) - 1)
    tmp[miejsce_zadanie1] = Kolejnosc[miejsce_zadanie2]
    tmp[miejsce_zadanie2] = Kolejnosc[miejsce_zadanie1]
    return tmp

dane = wczytaj_plik('data.txt') #Wczytaj dane

Cmax, Kolejnosc = Wyzarzanie(dane)

print(Cmax, Kolejnosc)
