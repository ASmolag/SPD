from pomoc import wczytaj_plik
import time

def ObliczPriorytet(Maszyny):
    i=2 #Pomijamy informację o liczbie zadań i maszyn
    suma = 0;
    Priorytet = []
    while (i<(Maszyny[0]*Maszyny[1]+2)):
        for j in range(Maszyny[1]):
            suma+=Maszyny[i+j] #sumuje czasy na każdej maszynie dla danego zadania
        Priorytet.append(suma) #Numer indeksu wagi odpowiada numerowi zadania (o 1 mniejszy)
        i+=Maszyny[1]
        suma=0
    return Priorytet

def ZnajdzNajdluzszeZadanie (M): #Zwraca numer zadania (pomniejszony o 1), które ma największy priorytet
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
        Tmp[nr_indeksu]=0 #Aby wyeliminować najdłuższe zadanie i nie zmieniać koljeności pozostałych
        Kolejnosc.append(nr_indeksu+1)
    return Kolejnosc #Zwraca numery zadań w kolejności wg priorytetów (nierosnąco)

def Max (W1, W2): #Wybiera większą z 2 liczb
    if W1 >= W2:
        return W1
    else:
        return W2

def Sciezka_dochodzaca(Maszyny, Kolejnosc): #Zwraca czasy zakończenia zadań na kolejnych maszynach (idąc od początku do końca) dla zadań w podanej kolejności
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
        if i%liczba_maszyn == 0: #Na pierwszej maszynie zaczynamy od razu, gdy poprzednie się zakończy
            nr_zadania += 1
            indeks = (Kolejnosc[nr_zadania] - 1) * liczba_maszyn + 2
            Czas_konca.append(Czas_konca[i-liczba_maszyn] + Maszyny[indeks])
        else: #Na pozostałych maszynach czekamy aż maszyna wolna i zadanie wyjdzie z poprzedniej maszyny
            Czas_konca.append(Max(Czas_konca[i-1], Czas_konca[i-liczba_maszyn]) + Maszyny[i%liczba_maszyn+indeks])

    return Czas_konca

def Sciezka_wychodzaca(Maszyny, Kolejnosc): #Zwraca czasy zakończenia zadań na koljenych maszynach (idąc od końca do początku) dla zadań w podanej kolejności. Wszystkie zadania dosunięte do prawej
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    nr_zadania = len(Kolejnosc)-1
    # Dla pierwszego zadania
    indeks = Kolejnosc[nr_zadania]*liczba_maszyn+1 #Zadanie z 3 maszyny
    Czas_konca = [Maszyny[indeks]]
    for i in range(1,liczba_maszyn):
        Czas_konca.append(Czas_konca[i-1]+Maszyny[indeks-i])
    #Dla kolejnych zadan
    for i in range(liczba_maszyn,liczba_zadan*liczba_maszyn):
        if i%liczba_maszyn == 0: #Na ostatniej maszynie zaczynamy od razu, gdy poprzednie zadanie się zakończy
            nr_zadania -= 1
            indeks = Kolejnosc[nr_zadania] * liczba_maszyn + 1
            Czas_konca.append(Czas_konca[i-liczba_maszyn] + Maszyny[indeks])
        else: #Na pozostałych czekamy aż maszyna wolna i zadanie zakończy się na poprzedniej maszynie
            Czas_konca.append(Max(Czas_konca[i-1], Czas_konca[i-liczba_maszyn]) + Maszyny[indeks-i%liczba_maszyn])

    Czas_konca.reverse() #Odwracamy tablicę. Dzięki temu wartości ze ścieżki dochodzącej i wychodzącej o tych samych indeksacj odpowiadają temu samemu zadaniu
    return Czas_konca


def Cmax(Maszyny, Kolejnosc): #Zwraca długość trwania najdłuższej ścieżki od początku do końca (ścieżki krytycznej)
    sciezka = Sciezka_dochodzaca(Maszyny, Kolejnosc)
    return sciezka[len(sciezka)-1]

def NEH(Maszyny):
    print(Maszyny)
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = []
    Kolejnosc_naj = []
    Cmaxmin = 9999999
    ListaZadan = [liczba_zadan, liczba_maszyn]
    Priorytety = ObliczPriorytet(Maszyny)
    KolejnoscPriorytetow = SortujPriorytetem(Priorytety)
    for i in range(liczba_zadan): #Dla każdego zadania
        Cmaxmin = 999999 #Cmaxmin badany dla każdej iteracji na nowo
        zadania = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobieramy zadanie wg kolejności priorytetów
        ListaZadan.extend(zadania) #Dorzucamy je do listy wykonywanych zadań
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
        for j in range (i+1):
            Kolejnosc.insert(j, i+1) #Dodane zadanie wstawiamy na każdą możliwość
            dlugosc_trwania=Cmax(ListaZadan, Kolejnosc) #Badamy Cmax dla danego ustawienia
            if dlugosc_trwania<Cmaxmin: #Jeżeli znaleziono wartość najmniejszą, to zapamiętuejmy ją oraz kolejność,która jej odpowiada
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j) #Aby badać zupełnie nową permutację
        Kolejnosc = Kolejnosc_naj[:] #Uzyskana koljeność jest podstawą do dalszych badań
    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1] #Zwracana kolejność w postaci pierwotnych numerów zadań. Lista "Kolejnosc" zawiera informację, w której iteracji pojawiło się zadanie w tym miejscu.

    return Cmaxmin, Kolejnosc_naj

def qNEH(Maszyny):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = [1]
    Kolejnosc_naj = []
    Cmaxmin = 9999999
    ListaZadan = [1, liczba_maszyn]
    Priorytety = ObliczPriorytet(Maszyny)
    KolejnoscPriorytetow = SortujPriorytetem(Priorytety)
    #print(KolejnoscPriorytetow)
    #Zadanie 1. trywialne
    zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[0])
    ListaZadan.extend(zadanie)
    print("pierwsze zadania",zadanie)

    for i in range(1,liczba_zadan):
        Cmaxmin = 999999 #Za każdym razem Cmaxmin rozpatrywane na nowo
        #Najpierw należy uzupełnić wartości ścieżek dla pamiętanej kolejności
        sciezka_wy = Sciezka_wychodzaca(ListaZadan, Kolejnosc)
        sciezka_do = Sciezka_dochodzaca(ListaZadan, Kolejnosc)
        print('do {}'.format(sciezka_do))
        print(sciezka_wy)
        zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobierz kolejne zadanie wg priorytetów
        ListaZadan.extend(zadanie)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
        print("w petli lista zdana to:", ListaZadan)
        for j in range (i+1):
            dlugosc_trwania=0 #Dla każdego ustawienia badane na nowo
            Kolejnosc.insert(j, i+1) #Badamy każdą permutację
            for k in range(liczba_maszyn): #Wybieramy ścieżkę krytyczną z powstałych wstawień
                #Sposób oblicznia ścieżki krytycznej zależy od miejsca włożenia nowego zadania
                if j == 0: #Na początku
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_wy[liczba_maszyn-1-k]) + zadanie[liczba_maszyn-1-k]
                elif j == i: #Na końcu
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_do[(j-1)*liczba_maszyn+k]) + zadanie[k]
                else: #W środku
                    if k==0:
                        droga = sciezka_do[(j-1)*liczba_maszyn+k]
                    else:
                        droga = Max(sciezka_do[(j-1)*liczba_maszyn+k], Pamiec_drogowa) #Porównaj nowe drogi dochodzące
                    Pamiec_drogowa = droga+zadanie[k] #Pamiętaj drogę dojścia
                    dlugosc_trwania = Max(dlugosc_trwania, droga+sciezka_wy[j*liczba_maszyn+k]+zadanie[k])
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka krytyczna jest lepsza niż dla innych permutacji
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j)
        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla której ścieżka krytyczna najkrótsza

    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1]
        print("osttatnie",Kolejnosc_naj)
    if liczba_zadan==1:
        Cmaxmin = Cmax(Maszyny, Kolejnosc)

    return Cmaxmin, Kolejnosc_naj

def ModNEH(Maszyny):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = [1]
    Kolejnosc_naj = []
    Cmaxmin = 9999999
    ListaZadan = [1, liczba_maszyn]
    Priorytety = ObliczPriorytet(Maszyny)
    KolejnoscPriorytetow = SortujPriorytetem(Priorytety)
    #print(KolejnoscPriorytetow)
    #Zadanie 1. trywialne
    zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[0])
    ListaZadan.extend(zadanie)


    for i in range(1,liczba_zadan):
        Cmaxmin = 999999 #Za każdym razem Cmaxmin rozpatrywane na nowo
        #Najpierw należy uzupełnić wartości ścieżek dla pamiętanej kolejności
        sciezka_wy = Sciezka_wychodzaca(ListaZadan, Kolejnosc)
        sciezka_do = Sciezka_dochodzaca(ListaZadan, Kolejnosc)
        #print('do {}'.format(sciezka_do))
        #print(sciezka_wy)
        zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobierz kolejne zadanie wg priorytetów
        ListaZadan.extend(zadanie)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
        #print("w petli lista zdana to:", ListaZadan)
        for j in range (i+1):
            dlugosc_trwania=0 #Dla każdego ustawienia badane na nowo
            Kolejnosc.insert(j, i+1) #Badamy każdą permutację
            for k in range(liczba_maszyn): #Wybieramy ścieżkę krytyczną z powstałych wstawień
                #Sposób oblicznia ścieżki krytycznej zależy od miejsca włożenia nowego zadania
                if j == 0: #Na początku
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_wy[liczba_maszyn-1-k]) + zadanie[liczba_maszyn-1-k]
                elif j == i: #Na końcu
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_do[(j-1)*liczba_maszyn+k]) + zadanie[k]
                else: #W środku
                    if k==0:
                        droga = sciezka_do[(j-1)*liczba_maszyn+k]
                    else:
                        droga = Max(sciezka_do[(j-1)*liczba_maszyn+k], Pamiec_drogowa) #Porównaj nowe drogi dochodzące
                    Pamiec_drogowa = droga+zadanie[k] #Pamiętaj drogę dojścia
                    dlugosc_trwania = Max(dlugosc_trwania, droga+sciezka_wy[j*liczba_maszyn+k]+zadanie[k])
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka krytyczna jest lepsza niż dla innych permutacji
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j)
        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla której ścieżka krytyczna najkrótsza

    ListaTmp=ListaZadan.copy()
    ListaPomoc=[]
    MinimalnaPoUsunieciu=99999999


    for i in range (1,liczba_zadan):
        print("lista tmp", ListaTmp)
        zadanie=[]
        start=2
        stop=start+ListaTmp[1]
        for j in range(start, stop):
            zadanie.append(ListaTmp[j])
        for k in range(start,stop):
            del ListaTmp[start]

        print("lista pomoc", zadanie)
        print("lista tmp", ListaTmp)

    #for j in range (i+1):


    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1]
    if liczba_zadan==1:
        Cmaxmin = Cmax(Maszyny, Kolejnosc)


    return Cmaxmin, Kolejnosc_naj

def WezZadanie (Maszyny, nr_zadania): #Pobiera z ogólnej tablicy wartości dla konkretnego zadania
    liczba_zadan=Maszyny[0]
    liczba_maszyn = Maszyny[1]
    tmp = []
    indeks = (nr_zadania-1)*liczba_maszyn+2;
    for i in range(liczba_maszyn):
        tmp.append(Maszyny[indeks + i])
    return tmp




dane = wczytaj_plik('data.txt') #Wczytaj dane

#NEH
#t0 = time.time()
#cmax, KolejnoscNajlepsza = NEH(dane)
#t1 = time.time()

#NEH z akceleracją
t0q = time.time()
cmaxq, KolejnoscNajlepszaq = ModNEH(dane)
t1q = time.time()

#print('NEH - czas trwania: {}'.format(t1-t0))
#print('Obliczony czas trwania {}'.format(cmax))
#print('Wyznaczona kolejność {}'.format(KolejnoscNajlepsza))

print('qNEH - czas trwania: {}'.format(t1q-t0q))
print('Obliczony czas trwania {}'.format(cmaxq))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepszaq))
