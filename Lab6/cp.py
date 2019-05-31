from ortools.sat.python import cp_model
from pathlib import Path

# milp jest opensource i dlatego jest dla podstawowych najlatwiejszych problemow
# cp lepiej rozpatruje warunki or
class RPQ():
  def __init__(self,r,p,q):
    self.R = r
    self.P = p
    self.Q = q

def Cp(jobs, instanceName):
  model=cp_model.CpModel()
  variableMaxValue=0
  for i in range(len(jobs)):
    variableMaxValue+=(jobs[i].R+jobs[i].P+jobs[i].Q)

  solver=cp_model.CpSolver()

  #variables:
  alfasMatrix={}
  for i in range(len(jobs)):
    for j in range(len(jobs)):
      alfasMatrix[i,j]=model.NewIntVar(0,1,"alfa"+str(i)+"_"+str(j))
  starts=[]
  for i in range(len(jobs)):
    starts.append(model.NewIntVar(0,variableMaxValue,"starts"+str(i)))
  cmax=model.NewIntVar(0,variableMaxValue,"cmax")

  for i in range(len(jobs)):
    model.Add(starts[i]>=jobs[i].R)
    model.Add(cmax>=starts[i]+jobs[i].P+jobs[i].Q)

  for i in range(len(jobs)):
    for j in range(i+1,len(jobs)):
      model.Add(starts[i]+jobs[i].P <= starts[j]+alfasMatrix[i,j]*variableMaxValue)
      model.Add(starts[j] + jobs[j].P <= starts[i] + alfasMatrix[j, i] *variableMaxValue)
      model.Add(alfasMatrix[i,j]+alfasMatrix[j,i]==1)

  model.Minimize(cmax)
  status=solver.Solve(model)
  if(status is not cp_model.OPTIMAL):
    print("Not optimal!")
  print(instanceName, "Cmax:", solver.ObjectiveValue())
  pi=[]
  for i in range(len(starts)):
    pi.append((i,solver.Value(starts[i])))
  pi.sort(key=lambda x: x[1])
  print(pi)

def GetRPQsFromFile(pathToFile):
  fullTextFromFile=Path(pathToFile).read_text()
  words=fullTextFromFile.replace("\n"," ").split(" ")
  words_cleaned= list(filter(None,words))
  numbers=list(map(int,words_cleaned))

  numberOfJobs=numbers[0]
  numbers.pop(0)
  numbers.pop(0)

  jobs=[]
  for i in range(numberOfJobs):
    jobs.append(RPQ(numbers[0],numbers[1],numbers[2]))
    numbers.pop(0)
    numbers.pop(0)
    numbers.pop(0)

  return jobs

if __name__== '__main__':
  file_paths=["in50.txt"]

  for i in range(len(file_paths)):
    jobs=GetRPQsFromFile(file_paths[i])
    Cp(jobs,file_paths[i])

