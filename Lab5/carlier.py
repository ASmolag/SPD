from schrage import *


def carlier(permut_tasks,ub):
    tasks = permut_tasks[:]
    u, pi = schrage(tasks)
    lb, O = pmtn(tasks)
    if u < ub:
        ub = u
        pi_star = pi[:]

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
    print("b = ", b+1)

    #  Wyznaczenie a

    sum_tasks = 0
    for i in range(b, -1, -1):
        sum_tasks +=pi[i][1]
        if u == sum_tasks + pi[i][0]+pi[b][2] and czas_zakonczenia_operacji[i-1] != pi[i][1]:
            a = i
            break
    print("a = ", a+1)

    #  Wyznaczenie c

    for i in range(a, b+1):
        if pi[i][2] < pi[b][2]:
            c = i
    print("c = ", c+1)

    if c < 0:
        return ub#, pi_star

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
    print("h(block) = ", rprim+pprim+qprim)

    old_pi_r_c = pi[c][0]
    pi[c][0]=max(pi[c][0], rprim+pprim)
    print("r' = ", pi[c][0])
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
    print("Lewy potomek")
    if lb < ub:
        ub = carlier(pi, ub)
    pi[c][0] = old_pi_r_c

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
    lb = max(max(rprim + qprim + pprim, rbis+pbis+qbis), lb)
    print("Prawy potomek")
    if lb < ub:
        ub = carlier(pi, ub)
    pi[c][2] = old_pi_q_c

    return ub#, pi_star

def carlier_wideLeft(permut_tasks):
    lista_zadan = []
    lb = 0
    ub = 99999999

    u, pi = schrage(permut_tasks)
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
    print("b = ", b+1)

    #  Wyznaczenie a
    sum_tasks = 0
    for i in range(b, -1, -1):
        sum_tasks +=pi[i][1]
        if u == sum_tasks + pi[i][0]+pi[b][2] and czas_zakonczenia_operacji[i-1] != pi[i][1]:
            a = i
            break
    print("a = ", a+1)

    #  Wyznaczenie c
    for i in range(a, b+1):
        if pi[i][2] < pi[b][2]:
            c = i
    print("c = ", c+1)

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
    print("h(block) = ", rprim+pprim+qprim)

    old_pi_r_c = pi[c][0]
    pi[c][0]=max(pi[c][0], rprim+pprim)
    print("r' = ", pi[c][0])
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
    print("Lewy potomek")
    if lb < ub:
        print("dodaj Lewego")
        kolejnosc = []
        kolejnosc = copy.deepcopy(pi)
        lista_zadan.append([kolejnosc, lb])
    pi[c][0] = old_pi_r_c

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
    lb = max(max(rprim + qprim + pprim, rbis+pbis+qbis), lb)
    print("Prawy potomek")
    if lb < ub:
        print("Dodaj prawego ", lb)
        kolejnosc_p = []
        kolejnosc_p = copy.deepcopy(pi)
        lista_zadan.append([kolejnosc_p, lb])
    print(pi[c][2], kolejnosc_p[c][2])
    pi[c][2] = old_pi_q_c
    print(pi[c][2], kolejnosc_p[c][2])


    while len(lista_zadan)!=0:
        while len(pi)!=0:
            pi.pop()
        print(ub)
        lb = lista_zadan[0][1]
        podzial, O = pmtn(lista_zadan[0][0])
        if podzial > ub:
            print("Pomijam")
            lista_zadan.pop(0)
            continue

        u, pi = schrage(lista_zadan[0][0])
        print(ub)
        print(podzial)

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
        print("b = ", b + 1)

        #  Wyznaczenie a
        sum_tasks = 0
        for i in range(b, -1, -1):
            sum_tasks += pi[i][1]
            if u == sum_tasks + pi[i][0] + pi[b][2] and czas_zakonczenia_operacji[i - 1] != pi[i][1]:
                a = i
                break
        print("a = ", a + 1)

        #  Wyznaczenie c
        for i in range(a, b + 1):
            if pi[i][2] < pi[b][2]:
                c = i
        print("c = ", c + 1)

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
        print("h(block) = ", rprim + pprim + qprim)

        old_pi_r_c = pi[c][0]
        pi[c][0] = max(pi[c][0], rprim + pprim)
        print("r' = ", pi[c][0])
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
        print("Lewy potomek")
        if lb < ub:
            kolejnosc = []
            kolejnosc = copy.deepcopy(pi)
            print(lb)
            print(ub)
            lista_zadan.append([kolejnosc, lb])
            print("Dodałem lewaka")
        pi[c][0] = old_pi_r_c

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
        print(lb)
        lb = max(max(rprim + qprim + pprim, rbis + pbis + qbis), lb)
        print("Prawy potomek")
        if lb < ub:
            print(lb)
            print(ub)
            kolejnosc_p = []
            kolejnosc_p = copy.deepcopy(pi)
            lista_zadan.append([kolejnosc_p, lb])
            print("Dodałem prawego")
        pi[c][2] = old_pi_q_c

        lista_zadan.pop(0)
        print("Długość listy = ", len(lista_zadan))
    return ub

#pliki = ["data1.txt", "data2.txt", "data3.txt", "data4.txt", "data5.txt", "data6.txt", "data7.txt", "data8.txt", "in50.txt", "in100.txt", "in200.txt"]

pliki = ["data1.txt"]

for i in range(len(pliki)):
    print(pliki[i])
    plik = wczytaj_plik(pliki[i])
    Cmax, O = schrage(plik)
    print("Cmax Schrage: ", Cmax)
    print(O)
    Cmax = carlier_wideLeft(plik)#, Cmax+1)
    print("cmax calier", Cmax)
    Cmax, O= pmtn(plik)
    print("Cmax pmtn: ", Cmax)




