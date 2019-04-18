from neh import qNEH, Cmax
from pomoc import wczytaj_plik
import random
import math

def Wyzarzanie (Maszyny):
    #inicjalizacja
    T0=200 #Temp. poczatkowa
    Tf=1 #Temp. koncowa
    npmax=165 #liczba perturbacji w ramach 1 iteracji

    alfa = 0.99 #wspolczynnik chlodzenia
    # mi = 0.95
    # mi = 0.9
    # mi = 0.8
    # mi = 0.4
    # mi = 0.01
    # mi= 0.01

    #Losowe ustalenie kolejnosci poczatkowej
    Kolejnosc = [1]
    for i in range(1, Maszyny[0]):
        Kolejnosc.insert(random.randrange(len(Kolejnosc)), i+1)
    C = Cmax(Maszyny, Kolejnosc)

    epsilon, Kolejnosc_NEH = qNEH(Maszyny)

    T=T0

    while T > Tf: #Temperature cycle
        for np in range(1,npmax): #Metropolis Cycle
            #generowanie ruchu
            Kolejnosc_prim = Swap(Kolejnosc) #Innym krokiem może byc Insert

            #Potencjalny ruch
            Cprim = Cmax(Maszyny, Kolejnosc_prim)

            #if Cprim < epsilon:
            #    C = Cprim
            #    Kolejnosc = Kolejnosc_prim[:]
            #    epsilon = Cprim
            #    break

            deltaf = Cprim-C #roznica

            if deltaf < 0:
                C = Cprim
                Kolejnosc = Kolejnosc_prim[:]

            else:
                BoltzmannP = 1/(1+2*math.exp(deltaf/T))

                if BoltzmannP > (random.random()/3): #Warunek ruchu
                    Kolejnosc = Kolejnosc_prim[:]
                    C = Cprim

        #Schładzanie
        T = alfa*T

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

for i in range(5):
    print("i = ", i)
    dane = wczytaj_plik('data4.txt') #Wczytaj dane
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data16.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data25.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data31.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data43.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data54.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data63.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data72.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data81.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data93.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)
    dane = wczytaj_plik('data105.txt')
    Cmax_var, Kolejnosc = Wyzarzanie(dane)
    print(Cmax_var)
    Cmax_NEH, Kolejnosc_NEH = qNEH(dane)
    print('NEH', Cmax_NEH)