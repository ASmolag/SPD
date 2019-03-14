import random

#Wczytanie danych
def wczytaj_plik(nazwa_pliku):
    plik=open(nazwa_pliku)
    try:
        tekst=plik.read()
    finally:
        plik.close()
    return list(map(int, tekst.split()))

def generowaniePrzebiegowLosowych (LiczbaZadan, LiczbaMaszyn):
    dane = [LiczbaZadan, LiczbaMaszyn]
    for i in range(LiczbaMaszyn*LiczbaZadan):
        dane.append(random.randint(1,100))
    return dane

#Rozpisanie zadań na odpowiednie maszyny
def rozpisanie_zadan(dane):
    i=2
    M1=[]
    M2=[]
    M3=[]
    while i<(dane[0]*dane[1]+2):
        if dane[1]==2:
            M1.append(dane[i])
            M2.append(dane[i+1])
            M3=0
        else:
            M1.append(dane[i])
            M2.append(dane[i+1])
            M3.append(dane[i+2])
        i+=dane[1]
    return M1,M2,M3

#stworzenie harmonogramu
def harmonogram(M1,M2,M3):
    if M3==0:
        s=M1[0]+M1[1]
        s2=M1[0]+M2[0]
        for i in range(1,len(M1)):
            if s2<=s:
                s2=s+M2[i]
            else:
                s2+=M2[i]
            if i!=len(M1)-1:
                s+=M1[i+1]
        return s2
    else:
        s=M1[0]+M1[1]
        s2=M1[0]+M2[0]
        s3=M1[0]+M2[0]+M3[0]
        for i in range(1,len(M1)):
            if s2<=s:
                s2=s+M2[i]
            else:
                s2+=M2[i]
            if s3<=s2:
                s3=s2+M3[i]
            else:
                s3+=M3[i]
            if i!=len(M1)-1:
                s+=M1[i+1]
        return s3

#Sortowanie wg optymalnej kolejnosci
def sortowanie(M1,M2,M3,tab):
    if M3!=0:
        tmp1=[]
        tmp2=[]
        tmp3=[]
        for i in range(len(tab)):
            tmp1.append(M1[tab[i]-1])
            tmp2.append(M2[tab[i]-1])
            tmp3.append(M3[tab[i]-1])
    else:
        tmp1 = []
        tmp2 = []
        tmp3 = 0
        for i in range(len(tab)):
            tmp1.append(M1[tab[i] - 1])
            tmp2.append(M2[tab[i] - 1])
    return tmp1,tmp2,tmp3