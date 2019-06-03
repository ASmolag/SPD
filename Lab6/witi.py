from ortools.sat.python import cp_model
from pathlib import Path

class witi():
    def __init__(self,czas_trwania,waga,dopuszczalny_czas):
        self.p = czas_trwania
        self.w = waga
        self.d = dopuszczalny_czas

def Cp(jobs, instnaceName):

    model = cp_model.CpModel()

    variablesMaxValue = 0
    czas_pracy = 0
    for i in range(len(jobs)):
        czas_pracy += jobs[i].p
    for i in range(len(jobs)):
        if(czas_pracy-jobs[i].d>0):
            variablesMaxValue += jobs[i].w*(czas_pracy-jobs[i].d)


    solver = cp_model.CpSolver()

    alfasMatrix = {}
    for i in range(len(jobs)):
        for j in range(len(jobs)):
            alfasMatrix[i,j] = model.NewIntVar(0,1,"alfa"+str(i)+"_"+str(j))

    starts = []
    ends = []
    delays = []
    for i in range(len(jobs)):
        starts.append(model.NewIntVar(0,variablesMaxValue,"starts"+str(i)))
        ends.append(model.NewIntVar(0, variablesMaxValue, "ends" + str(i)))
        delays.append(model.NewIntVar(0,variablesMaxValue,"delays"+str(i)))

    WiTi = model.NewIntVar(0,variablesMaxValue,"witi")


    for i in range(len(jobs)):
        model.Add(ends[i]>=starts[i]+jobs[i].p)
        model.Add(delays[i]==jobs[i].w*(ends[i]-jobs[i].d))

    for i in range(len(jobs)):
        for j in range(i+1,len(jobs)):
            model.Add(starts[i]+jobs[i].p <= starts[j] + alfasMatrix[i,j]*variablesMaxValue)
            model.Add(starts[j]+jobs[j].p <= starts[i] + alfasMatrix[j,i]*variablesMaxValue)
            model.Add(alfasMatrix[i,j]+alfasMatrix[j,i]==1)

    for i in range(len(delays)):
        WiTi+=delays[i]

    model.Minimize(WiTi)
    status = solver.Solve(model)
    if (status is not cp_model.OPTIMAL):
        print("Not optimal!")
    print(instnaceName, "WiTi: ", solver.ObjectiveValue())
    pi = []
    for i in range(len(starts)):
        pi.append((i,solver.Value(starts[i]),solver.Value(ends[i])))
    pi.sort(key=lambda x: x[1])
    print(pi)

def GetWiTisFromFile(pathToFile):
    fullTextFromFile = Path(pathToFile).read_text()
    words = fullTextFromFile.replace("\n"," ").split(" ")
    words_cleaned = list(filter(None,words))
    numbers = list(map(int, words_cleaned))

    numbersOfJobs = numbers[0]
    numbers.pop(0)
    numbers.pop(0)

    jobs = []
    for i in range(numbersOfJobs):
        jobs.append(witi(numbers[0],numbers[1],numbers[2]))
        numbers.pop(0)
        numbers.pop(0)
        numbers.pop(0)

    return jobs

if __name__ == '__main__':
    file_paths = ["witi.txt"]

    for i in range(len(file_paths)):
        jobs = GetWiTisFromFile(file_paths[i])
        Cp(jobs,file_paths[i])