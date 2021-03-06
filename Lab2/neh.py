from pomoc import wczytaj_plik
import time
import math

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

    for i in range(1,liczba_zadan):
        Cmaxmin = 999999 #Za każdym razem Cmaxmin rozpatrywane na nowo
        #Najpierw należy uzupełnić wartości ścieżek dla pamiętanej kolejności
        sciezka_wy = Sciezka_wychodzaca(ListaZadan, Kolejnosc)
        sciezka_do = Sciezka_dochodzaca(ListaZadan, Kolejnosc)
        zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobierz kolejne zadanie wg priorytetów
        ListaZadan.extend(zadanie)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
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
    if liczba_zadan==1:
        Cmaxmin = Cmax(Maszyny, Kolejnosc)

    return Cmaxmin, Kolejnosc_naj

def ModNEH4(Maszyny):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = [1]
    Kolejnosc_naj = []
    KolejPoUsunieciu = []
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
        zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobierz kolejne zadanie wg priorytetów
        ListaZadan.extend(zadanie)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
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
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j)
        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla której ścieżka najkrótsza

        #MODYFIKACJA 4
        MinimalnaPoUsunieciu = 999999

        for n in range(1, i+1): #Dla każdego zadania oprócz ostatniego (dodanego w tej iteracji) na liście zadań
            usuniete = Usun_zadanie(ListaZadan, n)
            Kolej = WeryfikujKolejnosc(Kolejnosc, n)
            C = Cmax(ListaZadan, Kolej)
            if C < MinimalnaPoUsunieciu: #Badanie, dla usunięcia którego zadania otrzymane Cmax będzie najmniejsze
                MinimalnaPoUsunieciu = C #Zapamiętanie tych wartości
                KolejPoUsunieciu = Kolej[:]
                numer_zadanie_usunietego = n
            Dodaj_zadanie(usuniete, ListaZadan, n) #Przywróć zadanie

        usuniete = Usun_zadanie(ListaZadan, numer_zadanie_usunietego) #Usuń znalezione zadanie z listy zadań

        sciezka_wy = Sciezka_wychodzaca(ListaZadan, KolejPoUsunieciu) #Wyznacz ścieżkę dochodzącą i wychodzącą w tej sytuacji
        sciezka_do = Sciezka_dochodzaca(ListaZadan, KolejPoUsunieciu)

        Dodaj_zadanie(usuniete, ListaZadan, numer_zadanie_usunietego) #Przywróć zadanie na listę
        NaprawKolejnosc(KolejPoUsunieciu, numer_zadanie_usunietego)


        for j in range (i+1):
            dlugosc_trwania=0 #Dla każdego ustawienia badane na nowo
            KolejPoUsunieciu.insert(j, numer_zadanie_usunietego) #Badamy każdą permutację, wstawiając zadanie właśnie usunięte
            for k in range(liczba_maszyn): #Wybieramy ścieżkę krytyczną z powstałych wstawień
                #Sposób oblicznia ścieżki krytycznej zależy od miejsca włożenia nowego zadania
                if j == 0: #Na początku
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_wy[liczba_maszyn-1-k]) + usuniete[liczba_maszyn-1-k]
                elif j == i: #Na końcu
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_do[(j-1)*liczba_maszyn+k]) + usuniete[k]
                else: #W środku
                    if k==0:
                        droga = sciezka_do[(j-1)*liczba_maszyn+k]
                    else:
                        droga = Max(sciezka_do[(j-1)*liczba_maszyn+k], Pamiec_drogowa) #Porównaj nowe drogi dochodzące
                    Pamiec_drogowa = droga+usuniete[k] #Pamiętaj drogę dojścia
                    dlugosc_trwania = Max(dlugosc_trwania, droga+sciezka_wy[j*liczba_maszyn+k]+usuniete[k])
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = KolejPoUsunieciu[:]
                Cmaxmin = dlugosc_trwania
            KolejPoUsunieciu.pop(j)

        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla ścieżka najkrótsza


    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1]
    if liczba_zadan==1:
        Cmaxmin = Cmax(Maszyny, Kolejnosc)


    return Cmaxmin, Kolejnosc_naj

def ModNEH1(Maszyny):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = [1]
    Kolejnosc_naj = []
    KolejPoUsunieciu = []
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
        zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobierz kolejne zadanie wg priorytetów
        ListaZadan.extend(zadanie)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
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
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j)
        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla której ścieżka najkrótsza

        #MODYFIKACJA 1
        sciezka_do = Sciezka_dochodzaca(ListaZadan, Kolejnosc)

        sciezka_krytyczna = WyznaczSciezkeKrytyczna(sciezka_do, liczba_maszyn)
        indeks_najdluzszej_operacji = ZnajdzNajdluzszeZadanie(sciezka_krytyczna)
        numer_zadanie_usunietego = math.floor(indeks_najdluzszej_operacji/liczba_maszyn)+1

        usuniete = Usun_zadanie(ListaZadan, numer_zadanie_usunietego) #Usuń znalezione zadanie z listy zadań
        KolejPoUsunieciu = WeryfikujKolejnosc(Kolejnosc, numer_zadanie_usunietego)

        sciezka_wy = Sciezka_wychodzaca(ListaZadan, KolejPoUsunieciu) #Wyznacz ścieżkę dochodzącą i wychodzącą w tej sytuacji
        sciezka_do = Sciezka_dochodzaca(ListaZadan, KolejPoUsunieciu)

        Dodaj_zadanie(usuniete, ListaZadan, numer_zadanie_usunietego) #Przywróć zadanie na listę
        NaprawKolejnosc(KolejPoUsunieciu, numer_zadanie_usunietego)


        for j in range (i+1):
            dlugosc_trwania=0 #Dla każdego ustawienia badane na nowo
            KolejPoUsunieciu.insert(j, numer_zadanie_usunietego) #Badamy każdą permutację, wstawiając zadanie właśnie usunięte
            for k in range(liczba_maszyn): #Wybieramy ścieżkę krytyczną z powstałych wstawień
                #Sposób oblicznia ścieżki krytycznej zależy od miejsca włożenia nowego zadania
                if j == 0: #Na początku
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_wy[liczba_maszyn-1-k]) + usuniete[liczba_maszyn-1-k]
                elif j == i: #Na końcu
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_do[(j-1)*liczba_maszyn+k]) + usuniete[k]
                else: #W środku
                    if k==0:
                        droga = sciezka_do[(j-1)*liczba_maszyn+k]
                    else:
                        droga = Max(sciezka_do[(j-1)*liczba_maszyn+k], Pamiec_drogowa) #Porównaj nowe drogi dochodzące
                    Pamiec_drogowa = droga+usuniete[k] #Pamiętaj drogę dojścia
                    dlugosc_trwania = Max(dlugosc_trwania, droga+sciezka_wy[j*liczba_maszyn+k]+usuniete[k])
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = KolejPoUsunieciu[:]
                Cmaxmin = dlugosc_trwania
            KolejPoUsunieciu.pop(j)

        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla ścieżka najkrótsza


    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1]
    if liczba_zadan==1:
        Cmaxmin = Cmax(Maszyny, Kolejnosc)


    return Cmaxmin, Kolejnosc_naj

def ModNEH2(Maszyny):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = [1]
    Kolejnosc_naj = []
    KolejPoUsunieciu = []
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
        zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobierz kolejne zadanie wg priorytetów
        ListaZadan.extend(zadanie)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
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
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j)
        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla której ścieżka najkrótsza

        #MODYFIKACJA 2
        sciezka_do = Sciezka_dochodzaca(ListaZadan, Kolejnosc)

        sciezka_krytyczna = WyznaczSciezkeKrytyczna(sciezka_do, liczba_maszyn)
        numer_zadanie_usunietego = NajwiekszaSumaOperacji(sciezka_krytyczna, liczba_maszyn, ListaZadan[0])

        usuniete = Usun_zadanie(ListaZadan, numer_zadanie_usunietego) #Usuń znalezione zadanie z listy zadań
        KolejPoUsunieciu = WeryfikujKolejnosc(Kolejnosc, numer_zadanie_usunietego)

        sciezka_wy = Sciezka_wychodzaca(ListaZadan, KolejPoUsunieciu) #Wyznacz ścieżkę dochodzącą i wychodzącą w tej sytuacji
        sciezka_do = Sciezka_dochodzaca(ListaZadan, KolejPoUsunieciu)

        Dodaj_zadanie(usuniete, ListaZadan, numer_zadanie_usunietego) #Przywróć zadanie na listę
        NaprawKolejnosc(KolejPoUsunieciu, numer_zadanie_usunietego)


        for j in range (i+1):
            dlugosc_trwania=0 #Dla każdego ustawienia badane na nowo
            KolejPoUsunieciu.insert(j, numer_zadanie_usunietego) #Badamy każdą permutację, wstawiając zadanie właśnie usunięte
            for k in range(liczba_maszyn): #Wybieramy ścieżkę krytyczną z powstałych wstawień
                #Sposób oblicznia ścieżki krytycznej zależy od miejsca włożenia nowego zadania
                if j == 0: #Na początku
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_wy[liczba_maszyn-1-k]) + usuniete[liczba_maszyn-1-k]
                elif j == i: #Na końcu
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_do[(j-1)*liczba_maszyn+k]) + usuniete[k]
                else: #W środku
                    if k==0:
                        droga = sciezka_do[(j-1)*liczba_maszyn+k]
                    else:
                        droga = Max(sciezka_do[(j-1)*liczba_maszyn+k], Pamiec_drogowa) #Porównaj nowe drogi dochodzące
                    Pamiec_drogowa = droga+usuniete[k] #Pamiętaj drogę dojścia
                    dlugosc_trwania = Max(dlugosc_trwania, droga+sciezka_wy[j*liczba_maszyn+k]+usuniete[k])
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = KolejPoUsunieciu[:]
                Cmaxmin = dlugosc_trwania
            KolejPoUsunieciu.pop(j)

        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla ścieżka najkrótsza


    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1]
    if liczba_zadan==1:
        Cmaxmin = Cmax(Maszyny, Kolejnosc)


    return Cmaxmin, Kolejnosc_naj

def ModNEH3(Maszyny):
    liczba_zadan = Maszyny[0]
    liczba_maszyn = Maszyny[1]
    Kolejnosc = [1]
    Kolejnosc_naj = []
    KolejPoUsunieciu = []
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
        zadanie = WezZadanie(Maszyny, KolejnoscPriorytetow[i]) #Pobierz kolejne zadanie wg priorytetów
        ListaZadan.extend(zadanie)
        ListaZadan[0] = i+1 #Na liście zadań jest dokładnie i+1 zadań
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
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = Kolejnosc[:]
                Cmaxmin = dlugosc_trwania
            Kolejnosc.pop(j)
        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla której ścieżka najkrótsza

        #MODYFIKACJA 3
        sciezka_do = Sciezka_dochodzaca(ListaZadan, Kolejnosc)

        sciezka_krytyczna = WyznaczSciezkeKrytyczna(sciezka_do, liczba_maszyn)
        numer_zadanie_usunietego = NajwiekszaLiczbaOperacji(sciezka_krytyczna, liczba_maszyn, ListaZadan[0])

        usuniete = Usun_zadanie(ListaZadan, numer_zadanie_usunietego) #Usuń znalezione zadanie z listy zadań
        KolejPoUsunieciu = WeryfikujKolejnosc(Kolejnosc, numer_zadanie_usunietego)

        sciezka_wy = Sciezka_wychodzaca(ListaZadan, KolejPoUsunieciu) #Wyznacz ścieżkę dochodzącą i wychodzącą w tej sytuacji
        sciezka_do = Sciezka_dochodzaca(ListaZadan, KolejPoUsunieciu)

        Dodaj_zadanie(usuniete, ListaZadan, numer_zadanie_usunietego) #Przywróć zadanie na listę
        NaprawKolejnosc(KolejPoUsunieciu, numer_zadanie_usunietego)


        for j in range (i+1):
            dlugosc_trwania=0 #Dla każdego ustawienia badane na nowo
            KolejPoUsunieciu.insert(j, numer_zadanie_usunietego) #Badamy każdą permutację, wstawiając zadanie właśnie usunięte
            for k in range(liczba_maszyn): #Wybieramy ścieżkę krytyczną z powstałych wstawień
                #Sposób oblicznia ścieżki krytycznej zależy od miejsca włożenia nowego zadania
                if j == 0: #Na początku
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_wy[liczba_maszyn-1-k]) + usuniete[liczba_maszyn-1-k]
                elif j == i: #Na końcu
                    dlugosc_trwania = Max(dlugosc_trwania, sciezka_do[(j-1)*liczba_maszyn+k]) + usuniete[k]
                else: #W środku
                    if k==0:
                        droga = sciezka_do[(j-1)*liczba_maszyn+k]
                    else:
                        droga = Max(sciezka_do[(j-1)*liczba_maszyn+k], Pamiec_drogowa) #Porównaj nowe drogi dochodzące
                    Pamiec_drogowa = droga+usuniete[k] #Pamiętaj drogę dojścia
                    dlugosc_trwania = Max(dlugosc_trwania, droga+sciezka_wy[j*liczba_maszyn+k]+usuniete[k])
            if dlugosc_trwania<Cmaxmin: #Gdy znaleziona ścieżka jest lepsza niż dla innych permutacji
                Kolejnosc_naj = KolejPoUsunieciu[:]
                Cmaxmin = dlugosc_trwania
            KolejPoUsunieciu.pop(j)

        Kolejnosc = Kolejnosc_naj[:] #Zapamiętaj kolejność, dla ścieżka najkrótsza


    for i in range(len(Kolejnosc_naj)):
        Kolejnosc_naj[i] = KolejnoscPriorytetow[Kolejnosc[i]-1]
    if liczba_zadan==1:
        Cmaxmin = Cmax(Maszyny, Kolejnosc)


    return Cmaxmin, Kolejnosc_naj

def NajwiekszaLiczbaOperacji(sciezka_krytyczna, liczba_maszyn, liczba_zadan):
    MaxZadan = 0
    Zadan = 0
    for i in range(liczba_zadan):
        for j in range(liczba_maszyn):
            if sciezka_krytyczna[i+j]!=0:
                Zadan+=1
        if Zadan>MaxZadan:
            MaxZadan = Zadan
            nr_zadania = i+1
    return nr_zadania

def Usun_zadanie(ListaZadan, nr_zadania):
    zadanie_usuniete = []
    liczba_maszyn = ListaZadan[1]
    ListaZadan[0] -= 1
    indeks = (nr_zadania - 1)*liczba_maszyn + 2
    for i in range(liczba_maszyn):
        zadanie_usuniete.append(ListaZadan.pop(indeks))
    return zadanie_usuniete

def Dodaj_zadanie(zadanie, ListaZadan, nr_zadania):
    liczba_maszyn = ListaZadan[1]
    ListaZadan[0] += 1
    indeks_poczatkowy = (nr_zadania-1)*liczba_maszyn + 2
    for i in range(liczba_maszyn):
        ListaZadan.insert(indeks_poczatkowy + i, zadanie[i])

def WeryfikujKolejnosc(Kolejnosc, nr_zadania_usunietego):
    tmp = Kolejnosc[:]
    tmp.remove(nr_zadania_usunietego)
    for i in range(len(tmp)):
        if tmp[i] > nr_zadania_usunietego:
            tmp[i] -= 1
    return tmp

def NaprawKolejnosc(Kolejnosc, nr_zadania):
    for i in range(len(Kolejnosc)):
        if Kolejnosc[i] >= nr_zadania:
            Kolejnosc[i] += 1

def WezZadanie (Maszyny, nr_zadania): #Pobiera z ogólnej tablicy wartości dla konkretnego zadania
    liczba_zadan=Maszyny[0]
    liczba_maszyn = Maszyny[1]
    tmp = []
    indeks = (nr_zadania-1)*liczba_maszyn+2;
    for i in range(liczba_maszyn):
        tmp.append(Maszyny[indeks + i])
    return tmp

def WyznaczSciezkeKrytyczna (sciezka_dochodzaca, liczba_maszyn):
    sciezka = sciezka_dochodzaca[:]
    indeks = len(sciezka_dochodzaca)-1
    sciezka_kryt = []

    while indeks > 0:
        if indeks%liczba_maszyn == 0:
            sciezka_kryt.append(-sciezka_dochodzaca[indeks-liczba_maszyn] + sciezka_dochodzaca[indeks])
            indeks -= liczba_maszyn
            for k in range(1, liczba_maszyn):
                sciezka_kryt.append(0)
        elif indeks<liczba_maszyn:
            sciezka_kryt.append(-sciezka_dochodzaca[indeks - 1] + sciezka_dochodzaca[indeks])
            indeks -= 1
        else:
            if sciezka_dochodzaca[indeks-liczba_maszyn] >= sciezka_dochodzaca[indeks-1]:
                sciezka_kryt.append(-sciezka_dochodzaca[indeks-liczba_maszyn] + sciezka_dochodzaca[indeks])
                indeks -= liczba_maszyn
                for k in range(1, liczba_maszyn):
                    sciezka_kryt.append(0)

            else:
                sciezka_kryt.append(-sciezka_dochodzaca[indeks-1] + sciezka_dochodzaca[indeks])
                indeks -= 1
    sciezka_kryt.append(sciezka_dochodzaca[indeks]) #Początek
    sciezka_kryt.reverse()
    return sciezka_kryt

def NajwiekszaSumaOperacji (sciezka_krytyczna, liczba_maszyn, liczba_zadan):
    SumMax = 0
    Sum = 0
    for i in range(liczba_zadan):
        for j in range(liczba_maszyn):
           Sum += sciezka_krytyczna[i+j]
        if Sum > SumMax:
            SumMax = Sum
            nr_zadania = i+1
        Sum = 0
    return nr_zadania

dane = wczytaj_plik('data.txt') #Wczytaj dane

#NEH
t0 = time.time()
cmax, KolejnoscNajlepsza = NEH(dane)
t1 = time.time()

#NEH z akceleracją
t0q = time.time()
cmaxq, KolejnoscNajlepszaq = qNEH(dane)
t1q = time.time()

#NEH z modyfikacją 1
t0m1 = time.time()
cmaxm1, KolejnoscNajlepszam1 = ModNEH1(dane)
t1m1 = time.time()

#NEH z modyfikacją 2
t0m2 = time.time()
cmaxm2, KolejnoscNajlepszam2 = ModNEH2(dane)
t1m2 = time.time()

#NEH z modyfikacją 3
t0m3 = time.time()
cmaxm3, KolejnoscNajlepszam3 = ModNEH3(dane)
t1m3 = time.time()

#NEH z modyfikacją 4
t0m4 = time.time()
cmaxm4, KolejnoscNajlepszam4 = ModNEH4(dane)
t1m4 = time.time()

print('NEH - czas trwania: {}'.format(t1-t0))
print('Obliczony czas trwania {}'.format(cmax))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepsza))

print('qNEH - czas trwania: {}'.format(t1q-t0q))
print('Obliczony czas trwania {}'.format(cmaxq))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepszaq))

print('ModNEH1 - czas trwania: {}'.format(t1m1-t0m1))
print('Obliczony czas trwania {}'.format(cmaxm1))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepszam1))

print('ModNEH2 - czas trwania: {}'.format(t1m2-t0m2))
print('Obliczony czas trwania {}'.format(cmaxm2))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepszam2))

print('ModNEH3 - czas trwania: {}'.format(t1m3-t0m3))
print('Obliczony czas trwania {}'.format(cmaxm3))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepszam3))

print('ModNEH4 - czas trwania: {}'.format(t1m4-t0m4))
print('Obliczony czas trwania {}'.format(cmaxm4))
print('Wyznaczona kolejność {}'.format(KolejnoscNajlepszam4))