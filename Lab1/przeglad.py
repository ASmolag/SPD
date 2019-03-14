import itertools
from pomoc import harmonogram

#tablice testowe
#tab1=[5,4,4,1,3]
#tab2=[2,6,3,5,4]


#harmonogram(M1,M2,M3)
def przeglad_zupelny(M1,M2,M3):
    sums = []
    min = 1000000
    indeks = 0
    if M3!=0:
        tablica1=list(itertools.permutations(M1))
        tablica2=list(itertools.permutations(M2))
        tablica3=list(itertools.permutations(M3))
        for i in range(len(tablica1)):
            suma = harmonogram(tablica1[i],tablica2[i], tablica3[i])
            if suma < min:
                min = suma
                indeks = i
            sums.append(suma)
#        print(suma3)
    else:
        tablica1 = list(itertools.permutations(M1))
        tablica2 = list(itertools.permutations(M2))
        tablica3 = 0
        for i in range(len(tablica1)):
            suma = harmonogram(tablica1[i], tablica2[i], tablica3)
            if suma < min:
                min=suma
                indeks = i
            sums.append(suma)
#       print(suma2)
    return tablica1, tablica2, tablica3, sums, min, indeks
