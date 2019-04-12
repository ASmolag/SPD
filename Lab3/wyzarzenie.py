from neh import qNEH, Cmax
from pomoc import wczytaj_plik
import random
import math

def Wyzarzanie (Maszyny):

    #inicjalizacja
    C, Kolejnosc = qNEH(Maszyny)
    #T = 1000
    #T=1200
    k=0 #zmienna iteracyjna
    kmax=842
    #mi = 0.99
    #wplywa na ilosc iteracji, czym mniejszy tym wiecej iteracji
    #mi = 0.95
    #mi = 0.9
    #mi = 0.8
    #mi = 0.4
    # mi = 0.01
    # mi= 0.01
    Tk=3
    #while T > Tk:
    while k!=kmax:
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

        k += 1
        #Schładzanie
        #T = mi*T
        T=T*k/kmax; # alternatywna fukcja schladzania
        #print("to jest k",k)
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

def Insert(Kolejnosc):
    tmp = Kolejnosc[:]
    zdejmij_zadanie = random.randrange(len(Kolejnosc))
    nr_zadania = tmp.pop(zdejmij_zadanie)
    wsadz_zadanie = random.randrange(len(Kolejnosc))
    while zdejmij_zadanie == wsadz_zadanie:
        wsadz_zadanie=random.randrange(len(Kolejnosc))
    tmp.insert(wsadz_zadanie, nr_zadania)
    return tmp

dane = wczytaj_plik('data4.txt') #Wczytaj dane

Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data16.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data25.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data31.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data43.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data54.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data63.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data72.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data81.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data93.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
dane = wczytaj_plik('data105.txt')
Cmax_var, Kolejnosc = Wyzarzanie(dane)
print(Cmax_var)
