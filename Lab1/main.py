from Johnson import Johnson3maszynowy
from Johnson import Johnson2maszynowy

#Wczytanie pliku
plik=open('data.txt')
try:
    tekst=plik.read()
finally:
    plik.close()

#Obróbka danych do postaci tablicy int-ów
i=0
data=[]
while i < len(tekst):
    data.append(tekst[i])
    i+=2
dane=list(map(int, data))

#Rozpisanie zadań na odpowiednie maszyny
i=2
M1=[]
M2=[]
M3=[]
while i<(dane[0]*dane[1]):
    if dane[1]==2:
        M1.append(dane[i])
        M2.append(dane[i+1])
    else:
        M1.append(dane[i])
        M2.append(dane[i+1])
        M3.append(dane[i+2])
    i+=dane[1]

#Obliczenie odpowiedniej kolejności
if dane[1]==2:
    print(Johnson2maszynowy(M1,M2))
else:
    print(Johnson3maszynowy(M1, M2, M3))

print(M1)
print(M2)


