import itertools
#tablice testowe
tab1=[5,4,4,1,3]
tab2=[2,6,3,5,4]
def harmonogram(tab1,tab2):
    s=tab1[0]+tab1[1]
    s2=tab1[0]+tab2[0]
    for i in range(1,len(tab1)):
        if s2<=s:
            s2=s+tab2[i]
        else:
            s2+=tab2[i]
        if i!=len(tab1)-1:
            s+=tab1[i+1]
    return s2

tablica1=list(itertools.permutations(tab1))
tablica2=list(itertools.permutations(tab2))

print(tablica1)
print(tablica2)
sums= []
min = 1000
a = 0
for i in range(len(tablica1)):
    suma2 = harmonogram(tablica1[i], tablica2[i])
    if suma2 < min:
        min=suma2
        a = i
    sums.append(suma2)
    print(suma2)

print(sums)
print(min, a)
print(sums.index(21))