# -*- coding: utf-8 -*-
import copy
import operator
import time


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
            Cmax = max(Cmax, t + e[2])
            O.append(e)
    N = O
    return Cmax, O

def pmtn(dane):
    N=copy.deepcopy(dane)
    G = []
    O = []
    t = min(N, key=operator.itemgetter(0))[0]  # zmienna pomocnicza czas
    Cmax = 0
    q0 = 999999999 # zgodnie z instrukcja ma być nieskończenie duze
    l = [0, 0, q0] # zadania aktualne
    n = N.index(min(N, key=operator.itemgetter(0)))

    while len(N) != 0 or len(G) != 0: # tak jak w podstawowym
        while len(N) != 0 and N[n][0] <= t:
            e = N.pop(n) # zadanie gotowe do oddania
            G.append(e)
            if len(N) != 0:
                n = N.index(min(N, key=operator.itemgetter(0)))

            if e[2] > l[2]:  # porownanie czasow zadan i przerwanie
                l[1] = t - e[0]
                t = e[0]
                if l[1] > 0:
                    G.append(l)  # kontynuacja przerwanego
        if len(G) == 0: # reszta jak poprzednie
            t = N[n][0]
        else:
            h = G.index(max(G, key=operator.itemgetter(2)))
            e = G.pop(h)
            t = t + e[1]
            Cmax = max(Cmax, t + e[2])
            l = e
            O.append(e)
    N = O
    return Cmax, O

