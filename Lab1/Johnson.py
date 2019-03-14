def ZnajdzNajkrotszeZadanie (M) :
    najkrotszy = M[0]
    nr_indeksu = 0
    for i in range(len(M)):
        if M[i] < najkrotszy:
            najkrotszy = M[i]
            nr_indeksu = i
    return nr_indeksu


def Johnson2maszynowy (M1, M2) :
    Maszyna1 = M1[:]
    Maszyna2 = M2[:]
    L1=[]
    L2=[]
    najdluzszy=99999
    for i in range(len(Maszyna1)):
        indeks1 = ZnajdzNajkrotszeZadanie(Maszyna1)
        indeks2 = ZnajdzNajkrotszeZadanie(Maszyna2)
        if Maszyna1[indeks1] < Maszyna2[indeks2]:
            L1.append(indeks1+1)
            Maszyna1[indeks1] = najdluzszy
            Maszyna2[indeks1] = najdluzszy
        else :
            L2.insert(0,indeks2+1)
            Maszyna1[indeks2] = najdluzszy
            Maszyna2[indeks2] = najdluzszy

    Kolejnosc = L1+L2
    return Kolejnosc

def Johnson3maszynowy(Maszyna1, Maszyna2, Maszyna3):
    wirtualnaMaszyna1=[]
    wirtualnaMaszyna2=[]
    for i in range(len(Maszyna1)):
        wirtualnaMaszyna1.append(Maszyna1[i] + Maszyna2[i])
        wirtualnaMaszyna2.append(Maszyna2[i] + Maszyna3[i])

    Kolejnosc = Johnson2maszynowy(wirtualnaMaszyna1, wirtualnaMaszyna2)
    return Kolejnosc

def Alg_Johnsona (M1,M2,M3):
    if M3!=0:
        return Johnson3maszynowy(M1,M2,M3)
    else:
        return Johnson2maszynowy(M1,M2)
