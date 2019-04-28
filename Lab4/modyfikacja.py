import copy
import operator
import time

#Na podstawie https://www.researchgate.net/publication/241080533_Approximation_algorithms_for_no_idle_time_scheduling_on_a_single_machine_with_release_times_and_delivery_times
#rozdział 2

#funkcja otwierajaca plik i przygotowująca dane z pliku
def wczytaj_plik(nazwa_pliku):
    plik = open(nazwa_pliku)
    zawartosc = plik.read().splitlines()  # kazda linia to inne zadanie
    data = [i.split() for i in zawartosc]  # każde zadanie to lista z trzema elementami
    dane = [list(map(int, dat)) for dat in data]  # zmiana string na int
    dane.pop(0)  # usuniecie liczby zadan bo nie bedzie juz potrzebne
    #dane.sort(key=operator.itemgetter(0))  # sortowanie względem r - czasu dostępności
    return dane

# dwa poniższe algorytmy dla złozoności obliczeniowej n^2
def schrage(dane):
    N = copy.deepcopy(dane)  # zbior nieuszeregowany
    G = [] # zbior gotowych do uszeregowania
    t = min(N, key=operator.itemgetter(0))[0] #zmienna pomocnicza czas
    #t = 0 #zmienna pomocnicza czas
    Cmax = 0 #funkcja celu
    O = [] # czesciowa kolejnosc
    n = N.index(min(N, key=operator.itemgetter(0)))
    while len(N) != 0 or len(G) != 0:
        while len(N) != 0 and  N[n][0] <= t: # sprawdzamy najmniejszy czas przygotowania
            G.append(N.pop(n))
            if len(N) != 0:
                n = N.index(min(N, key=operator.itemgetter(0)))
        if len(G) == 0:
            t = N[n][0]
        else:
            h = G.index(max(G, key=operator.itemgetter(2))) #wybor max dostarczenia
            e = G.pop(h)
            #e.append(t)  # dodanie chwili rozpoczecia jako [3] elementu w e.
            t = t + e[1]
            if Cmax < t+e[2]:
                Cmax = t+e[2]
                zadanie_krytyczne = e #Znalezienie zadania krytycznego
            #Cmax = max(Cmax, t + e[2])
            O.append(e)

    minimum_q = O[O.index(min(O, key=operator.itemgetter(2)))][2]
    if minimum_q == zadanie_krytyczne[2]:
        interferencyjne_indeks = -1 #Jesli zdanie krytyczne ma najkrotsze q, to brak zadania interferncyjnego
    else:
        zadanie_interferencyjne = O[0]
        for i in range(O.index(zadanie_krytyczne)+1): #Sprawdzenie warunku zadania interferncyjnego
            for j in range(O.index(zadanie_interferencyjne)+1, O.index(zadanie_krytyczne)+1):
                if O[j][2] < zadanie_krytyczne[2]:
                    zadanie_interferencyjne = O[j]
                    i=j
                    break
        interferencyjne_indeks = O.index(zadanie_interferencyjne)

    return Cmax, O, O.index(zadanie_krytyczne), interferencyjne_indeks

def schrage_mod(dane):
    I = dane[:]
    Copt = 99999999999
    for k in range(len(dane)):
        Cmax, I, krytyczne_indeks, interferencyjne_indeks = schrage(I) #Wykonaj Schrage
        if Cmax < Copt: #Zapamiętaj rozwiązanie optymalne
            Copt = Cmax
            O = I[:]
        if interferencyjne_indeks == -1: #przerwij, jeśli optymlane
            break
        else:
            I[interferencyjne_indeks][0] = I[krytyczne_indeks][0] #Przesuń zadanie interferencyjne za krytyczne
    return Copt, O

pliki = ["in50.txt", "in100.txt", "in200.txt"]

for i in range(len(pliki)):
    plik = wczytaj_plik(pliki[i])
    t0 = time.time()
    Cmax, O, crit, inter = schrage(plik)
    t1= time.time()
    print("Czas Schrage: ", t1-t0)
    print(O)
    print(Cmax)

    t0 = time.time()
    Cmax, O = schrage_mod(plik)
    t1 = time.time()
    print("Czas Potts: ", t1-t0)
    print(Cmax)
    print(O)