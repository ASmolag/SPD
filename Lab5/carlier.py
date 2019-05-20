from schrage import *


def carlier(permut_tasks,ub = 999999999):
    tasks = copy.deepcopy(permut_tasks)
    u, pi = schrage(tasks)

    if u < ub:
        ub = u

    a = 0
    b = 0
    c = -1

    #  Wyznaczenie b
    cpop = 0
    czas_zakonczenia_operacji = []
    for i in range(len(pi)):
        cpop = max(cpop, max(pi[i][0],cpop) + pi[i][1])
        czas_zakonczenia_operacji.append(cpop)
        if cpop + pi[i][2] == u:
            b = i

    #  Wyznaczenie a
    sum_tasks = 0
    for i in range(b, -1, -1):
        sum_tasks +=pi[i][1]
        if u == sum_tasks + pi[i][0]+pi[b][2] and czas_zakonczenia_operacji[i-1] != pi[i][1]:
            a = i
            break

    #  Wyznaczenie c
    for i in range(a, b+1):
        if pi[i][2] < pi[b][2]:
            c = i

    if c < 0:
        return ub

    #  Wyznaczenie r', q' i p'
    pprim = 0
    rprim = pi[c+1][0]
    qprim = pi[c+1][2]
    for i in range(c+1, b+1):
        pprim += pi[i][1]
        if rprim > pi[i][0]:
            rprim = pi[i][0]
        if qprim > pi[i][2]:
            qprim = pi[i][2]

    #Potomek po lewej stronie - zmiana czasu przygotowania zadania krytycznego
    old_pi_r_c = pi[c][0]
    pi[c][0]=max(pi[c][0], rprim+pprim)

    #Przygotowanie bloku z uwzględnieniem zadania c
    pbis = 0
    rbis = pi[c][0]
    qbis = pi[c][2]
    for i in range(c, b + 1):
        pbis += pi[i][1]
        if rbis > pi[i][0]:
            rbis = pi[i][0]
        if qbis > pi[i][2]:
            qbis = pi[i][2]

    lb, O = pmtn(pi)
    lb = max(max(rprim + qprim + pprim, rbis+pbis+qbis),lb)
    if lb < ub:
        ub = carlier(pi, ub)
    pi[c][0] = old_pi_r_c

    #Potomek po prawej stronie - zmiana czasu stygnięcia zadania krytycznego
    old_pi_q_c = pi[c][2]
    pi[c][2] = max(pi[c][2], qprim + pprim)

    #Przygotowanie bloku z uwzględnieniem zadania krytycznego
    pbis = 0
    rbis = pi[c][0]
    qbis = pi[c][2]
    for i in range(c, b + 1):
        pbis += pi[i][1]
        if rbis > pi[i][0]:
            rbis = pi[i][0]
        if qbis > pi[i][2]:
            qbis = pi[i][2]

    lb, O = pmtn(pi)
    lb = max(max(rprim + qprim + pprim, rbis+pbis+qbis), lb)
    if lb < ub:
        ub = carlier(pi, ub)
    pi[c][2] = old_pi_q_c

    return ub

def carlier_wideLeft(permut_tasks):
    lista_zadan = []
    lb = 0
    ub = 99999999

    u, pi = schrage(permut_tasks)
    if u < ub:
        ub = u

    lista_zadan.append([pi, lb])


    while len(lista_zadan)!=0:
        lb = lista_zadan[0][1]
        podzial, O = pmtn(lista_zadan[0][0])
        if podzial > ub:
            lista_zadan.pop(0)
            continue

        u, pi = schrage(lista_zadan[0][0])
        if u < ub:
            ub = u

        a = 0
        b = 0
        c = -1
        #  Wyznaczenie b
        cpop = 0
        czas_zakonczenia_operacji = []
        for i in range(len(pi)):
            cpop = max(cpop, max(pi[i][0], cpop) + pi[i][1])
            czas_zakonczenia_operacji.append(cpop)
            if cpop + pi[i][2] == u:
                b = i

        #  Wyznaczenie a
        sum_tasks = 0
        for i in range(b, -1, -1):
            sum_tasks += pi[i][1]
            if u == sum_tasks + pi[i][0] + pi[b][2] and czas_zakonczenia_operacji[i - 1] != pi[i][1]:
                a = i
                break

        #  Wyznaczenie c
        for i in range(a, b + 1):
            if pi[i][2] < pi[b][2]:
                c = i
        if c < 0:
            return ub

        #  Wyznaczenie r', q' i p'
        pprim = 0
        rprim = pi[c + 1][0]
        qprim = pi[c + 1][2]
        for i in range(c + 1, b + 1):
            pprim += pi[i][1]
            if rprim > pi[i][0]:
                rprim = pi[i][0]
            if qprim > pi[i][2]:
                qprim = pi[i][2]

        #Lewy potomek
        old_pi_r_c = pi[c][0]
        pi[c][0] = max(pi[c][0], rprim + pprim)

        pbis = 0
        rbis = pi[c][0]
        qbis = pi[c][2]
        for i in range(c, b + 1):
            pbis += pi[i][1]
            if rbis > pi[i][0]:
                rbis = pi[i][0]
            if qbis > pi[i][2]:
                qbis = pi[i][2]

        lb, O = pmtn(pi)
        lb = max(max(rprim + qprim + pprim, rbis + pbis + qbis), lb)
        if lb < ub:
            kolejnosc_l = copy.deepcopy(pi)
            lista_zadan.append([kolejnosc_l, lb])
        pi[c][0] = old_pi_r_c

        #Prawy potomek
        old_pi_q_c = pi[c][2]
        pi[c][2] = max(pi[c][2], qprim + pprim)

        pbis = 0
        rbis = pi[c][0]
        qbis = pi[c][2]
        for i in range(c, b + 1):
            pbis += pi[i][1]
            if rbis > pi[i][0]:
                rbis = pi[i][0]
            if qbis > pi[i][2]:
                qbis = pi[i][2]
        lb, O = pmtn(pi)
        lb = max(max(rprim + qprim + pprim, rbis + pbis + qbis), lb)
        if lb < ub:
            kolejnosc_p = copy.deepcopy(pi)
            lista_zadan.append([kolejnosc_p, lb])
        pi[c][2] = old_pi_q_c

        lista_zadan.pop(0) #Odrzuc sprawdzony wezel

    return ub

def carlier_greedy(permut_tasks):
    lista_zadan = []
    lb = 0
    ub = 99999999

    u, pi = schrage(permut_tasks)
    if u < ub:
        ub = u

    lista_zadan.append([pi, lb])


    while len(lista_zadan)!=0:
        lb = lista_zadan[0][1]
        podzial, O = pmtn(lista_zadan[0][0])
        if podzial > ub:
            lista_zadan.pop(0)
            continue

        u, pi = schrage(lista_zadan[0][0])
        if u < ub:
            ub = u

        a = 0
        b = 0
        c = -1
        #  Wyznaczenie b
        cpop = 0
        czas_zakonczenia_operacji = []
        for i in range(len(pi)):
            cpop = max(cpop, max(pi[i][0], cpop) + pi[i][1])
            czas_zakonczenia_operacji.append(cpop)
            if cpop + pi[i][2] == u:
                b = i

        #  Wyznaczenie a
        sum_tasks = 0
        for i in range(b, -1, -1):
            sum_tasks += pi[i][1]
            if u == sum_tasks + pi[i][0] + pi[b][2] and czas_zakonczenia_operacji[i - 1] != pi[i][1]:
                a = i
                break

        #  Wyznaczenie c
        for i in range(a, b + 1):
            if pi[i][2] < pi[b][2]:
                c = i
        if c < 0:
            return ub

        #  Wyznaczenie r', q' i p'
        pprim = 0
        rprim = pi[c + 1][0]
        qprim = pi[c + 1][2]
        for i in range(c + 1, b + 1):
            pprim += pi[i][1]
            if rprim > pi[i][0]:
                rprim = pi[i][0]
            if qprim > pi[i][2]:
                qprim = pi[i][2]

        #Lewy potomek
        old_pi_r_c = pi[c][0]
        pi[c][0] = max(pi[c][0], rprim + pprim)

        pbis = 0
        rbis = pi[c][0]
        qbis = pi[c][2]
        for i in range(c, b + 1):
            pbis += pi[i][1]
            if rbis > pi[i][0]:
                rbis = pi[i][0]
            if qbis > pi[i][2]:
                qbis = pi[i][2]

        lb, O = pmtn(pi)
        lb = max(max(rprim + qprim + pprim, rbis + pbis + qbis), lb)
        if lb < ub:
            kolejnosc_l = copy.deepcopy(pi)
            lista_zadan.append([kolejnosc_l, lb])
            #print("Lewy potomek: ub = ", ub, " lb = ", lb)
        pi[c][0] = old_pi_r_c

        #Prawy potomek
        old_pi_q_c = pi[c][2]
        pi[c][2] = max(pi[c][2], qprim + pprim)

        pbis = 0
        rbis = pi[c][0]
        qbis = pi[c][2]
        for i in range(c, b + 1):
            pbis += pi[i][1]
            if rbis > pi[i][0]:
                rbis = pi[i][0]
            if qbis > pi[i][2]:
                qbis = pi[i][2]
        lb, O = pmtn(pi)
        lb = max(max(rprim + qprim + pprim, rbis + pbis + qbis), lb)
        if lb < ub:
            kolejnosc_p = copy.deepcopy(pi)
            lista_zadan.append([kolejnosc_p, lb])
            #print("Prawy potomek: ub = ", ub, " lb = ", lb)
        pi[c][2] = old_pi_q_c

        lista_zadan.pop(0) #Odrzuc sprawdzony wezel
        lista_zadan.sort(key=operator.itemgetter(1))
    return ub

#pliki = ["in50.txt", "in100.txt", "in200.txt", "data1.txt", "data2.txt", "data3.txt", "data4.txt", "data5.txt", "data6.txt"]

pliki = ["data7.txt", "data8.txt"]

for i in range(len(pliki)):
    print(pliki[i])
    plik = wczytaj_plik(pliki[i])

    Cmax, O = schrage(plik)
    print("Cmax Schrage = ", Cmax)
    Cmax, O= pmtn(plik)
    print("Cmax Schrage pmtn = ", Cmax)

    #t0 = time.time()
    #Cmax = carlier(plik)
    #t1 = time.time()
    #print("Cmax Carlier (Deep Left) = ", Cmax, " t = ", t1-t0)

    t0 = time.time()
    Cmax = carlier_wideLeft(plik)
    t1 = time.time()
    print("Cmax Carlier (Wide Left) = ", Cmax, " t = ", t1-t0)

    t0 = time.time()
    Cmax = carlier_greedy(plik)
    t1 = time.time()
    print("Cmax Carlier (Greedy) = ", Cmax, " t = ", t1-t0)




