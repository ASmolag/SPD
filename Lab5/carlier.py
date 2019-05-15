from schrage import *


def carlier(permut_tasks,ub):
    # import copy
    tasks = copy.deepcopy(permut_tasks)
    u, pi = schrage(tasks)
    if u < ub:
        ub = u
        #pi_star = pi.return_without_c()

    a = 0
    b = 0
    c = -1

    #  Wyznaczenie b

    cpop = 0
    for i in range(len(pi)):
        cpop = max(cpop, tasks[i][0] + tasks[i][1])
        if cpop + tasks[i][2] == u:
            b = i

    #  Wyznaczenie a

    sum_tasks = 0
    for i in range(len(tasks)-1, -1, -1):
        sum_tasks += tasks[i][1]
        if u == sum_tasks + tasks[i][0]+tasks[b][2]:
            a = i

    #  Wyznaczenie c

    for i in range(a, b+1):
        if tasks[i][2] < tasks[b][2]:
            c = i

    if c < 0:
        return ub

    #  Wyznaczenie r', q' i p'

    rprim = 0
    pprim = 0
    qprim = 0

    rprim = tasks[c+1][0]
    qprim = tasks[c+1][2]

    for i in range(c+1, b):
        pprim += tasks[i][1]
        if rprim > tasks[i][0]:
            rprim = tasks[i][0]
        if qprim < tasks[i][2]:
            qprim = tasks[i][2]

    old_pi_r_c = tasks[c][0]
    tasks[c][0]=max(tasks[c][0], rprim+pprim)
    lb = pmtn(pi)
    if lb < ub:
        ub = carlier(tasks, ub)
    tasks[c][0] = old_pi_r_c
    old_pi_q_c = tasks[c][2]
    tasks[c][2] = max(tasks[c][2], qprim + pprim)
    lb = pmtn(pi)
    if lb < ub:
        ub = carlier(pi, ub)
    tasks[c][2] = old_pi_q_c

    return ub

pliki = ["in50.txt", "in100.txt", "in200.txt"]

for i in range(len(pliki)):
    print(pliki[i])
    plik = wczytaj_plik(pliki[i])
    Cmax, O = schrage(plik)
    print("Cmax Schrage: ", Cmax)

    Cmax = carlier(plik, Cmax)
    print("cmax calier", Cmax)
    Cmax, O= pmtn(plik)
    print("Cmax pmtn: ", Cmax)




