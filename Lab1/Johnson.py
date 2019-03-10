def ZnajdzNajkrotszeZadanie (M) :
    najkrotszy = M[0]
    nr_indeksu = 0
    for i in range(len(M)):
        if M[i] < najkrotszy:
            najkrotszy = M[i]
            nr_indeksu = i
    return nr_indeksu


def ZnajdzNajdluzszeZadanie (M) :
    najdluzszy = M[0]
    for i in range(len(M)):
        if M[i] > najdluzszy:
            najdluzszy = M[i]
    return najdluzszy

def Johnson2maszynowy (Maszyna1, Maszyna2) :
    L1=[]
    L2=[]
    najdluzszy1 = ZnajdzNajdluzszeZadanie(Maszyna1)
    najdluzszy2 = ZnajdzNajdluzszeZadanie(Maszyna2)

    if najdluzszy1 > najdluzszy2:
        najdluzszy = najdluzszy1+1
    else :
        najdluzszy = najdluzszy2+1

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