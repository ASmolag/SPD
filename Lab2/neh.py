from pomoc import wczytaj_plik

def ObliczPriorytet(Maszyny):
    i=2
    suma = 0;
    Priorytet = []
    while (i<(Maszyny[0]*Maszyny[1]+2)):
        for j in range(Maszyny[1]):
            suma+=Maszyny[i+j]
        Priorytet.append(suma)
        i+=Maszyny[1]
        suma=0
    return Priorytet

def ZnajdzNajdluzszeZadanie (M) :
    najdluzszy = M[0]
    nr_indeksu = 0
    for i in range(len(M)):
        if M[i] > najdluzszy:
            najdluzszy = M[i]
            nr_indeksu = i
    return nr_indeksu

def SortujNEH (M):
    Kolejnosc = []
    Tmp = M[:]
    for i in range(len(Tmp)):
        nr_indeksu = ZnajdzNajdluzszeZadanie(Tmp)
        Tmp[nr_indeksu]=0
        Kolejnosc.append(nr_indeksu+1)
    return Kolejnosc

def Cmax(Maszyny, Kolejnosc):
    Czas_Rozpoczecia = []
    for i in range(Maszyny[0]):
        Czas_Rozpoczecia[i] +=

dane = wczytaj_plik('data.txt')
pri = ObliczPriorytet(dane)
print(pri)
print(SortujNEH(pri))

