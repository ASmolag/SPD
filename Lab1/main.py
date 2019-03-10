from Johnson import Johnson3maszynowy
from Johnson import Johnson2maszynowy
from Johnson import sortowanie

#Wczytanie pliku
def wczytaj_plik(nazwa_pliku):
    plik=open(nazwa_pliku)
    try:
        tekst=plik.read()
    finally:
        plik.close()
    return tekst
#Obróbka danych do postaci tablicy int-ów
def dane_do_tab(tekst):
    i=0
    data=[]
    while i < len(tekst):
        data.append(tekst[i])
        i+=2
    dane=list(map(int, data))
    return dane

#Rozpisanie zadań na odpowiednie maszyny
def rozpisanie_zadan(dane):
    i=2
    M1=[]
    M2=[]
    M3=[]
    while i<(dane[0]*dane[1]):
        if dane[1]==2:
            M1.append(dane[i])
            M2.append(dane[i+1])
            M3=0
        else:
            M1.append(dane[i])
            M2.append(dane[i+1])
            M3.append(dane[i+2])
        i+=dane[1]
    return M1,M2,M3,dane
#stworzenie harmonogramu
def harmonogram(M1,M2):
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

def harmonogram3(M1,M2,M3):
    s=M1[0]+M1[0]
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

M1,M2,M3,dane=rozpisanie_zadan(dane_do_tab(wczytaj_plik('data.txt')))
#Obliczenie odpowiedniej kolejności
#if dane[1]==2:
 #   print(Johnson2maszynowy(M1,M2))
#else:
  #  print(Johnson3maszynowy(M1, M2, M3))
print(M1,M2,M3)
tmp1,tmp2,tmp3=sortowanie(M1,M2,M3)
print(harmonogram3(tmp1,tmp2,tmp3))



