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

def SortujPriorytetem (M):
    Kolejnosc = []
    Tmp = M[:]
    for i in range(len(Tmp)):
        nr_indeksu = ZnajdzNajdluzszeZadanie(Tmp)
        Tmp[nr_indeksu]=0
        Kolejnosc.append(nr_indeksu+1)
    return Kolejnosc

def Max (W1, W2):
    if W1 >= W2:
        return W1
    else:
        return W2

def Sciezka_dochodzaca(Maszyny, Kolejnosc):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    nr_zadania = 0
    # Dla pierwszego zadania
    indeks = (Kolejnosc[nr_zadania]-1)*liczba_maszyn+2
    Czas_konca = [Maszyny[indeks]]
    for i in range(1,liczba_maszyn):
        Czas_konca.append(Czas_konca[i-1]+Maszyny[indeks + i])
    #Dla kolejnych zadan
    for i in range(liczba_maszyn,liczba_zadan*liczba_maszyn):
        if i%liczba_maszyn == 0:
            nr_zadania += 1
            indeks = (Kolejnosc[nr_zadania] - 1) * liczba_maszyn + 2
            Czas_konca.append(Czas_konca[i-liczba_maszyn] + Maszyny[indeks])
        else:
            Czas_konca.append(Max(Czas_konca[i-1], Czas_konca[i-liczba_maszyn]) + Maszyny[i%liczba_maszyn+indeks])

    return Czas_konca

def Cmax(Maszyny, Kolejnosc):
    sciezka = Sciezka_dochodzaca(Maszyny, Kolejnosc)
    return sciezka[len(sciezka)-1]

def NEH(Maszyny):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = []
    Kolejnosc_naj = []
    Cmaxmin = 9999999
    ListaZadan = [liczba_zadan, liczba_maszyn]

    Priorytety = ObliczPriorytet(Maszyny)
    KolejnoscPriorytetow = SortujPriorytetem(Priorytety)
    for i in range(liczba_zadan):
        Cmaxmin = 999999
        zadania = WezZadanie(Maszyny, KolejnoscPriorytetow[i])
        ListaZadan.extend(zadania)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
        for j in range (i+1):
            Kolejnosc.insert(j, i+1)
            dlugosc_trwania=Cmax(ListaZadan, Kolejnosc)
            if dlugosc_trwania<Cmaxmin:
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j)
        Kolejnosc = Kolejnosc_naj[:]
    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1]
    return Cmaxmin, Kolejnosc_naj

def WezZadanie (Maszyny, nr_zadania):
    liczba_zadan=Maszyny[0]
    liczba_maszyn = Maszyny[1]
    tmp = []
    indeks = (nr_zadania-1)*liczba_maszyn+2;
    for i in range(liczba_maszyn):
        tmp.append(Maszyny[indeks + i])
    return tmp

dane = wczytaj_plik('data.txt')
Cmax, KolejnoscNajlepsza = NEH(dane)
print('Obliczony czas trwania {}'.format(Cmax))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepsza))