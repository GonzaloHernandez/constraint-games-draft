import os
os.system("clear")

from minizinc import Instance, Model, Solver

print("---------------- Step 1 ---------------------")
model = Model("./example5.01/example5.01.mzn")
gecode = Solver.lookup("gecode")
instanceP = Instance(gecode, model)
resultP = instanceP.solve(all_solutions=True)
for i in range(len(resultP)) :
    print(resultP[i, "V"] + resultP[i, "U"])

tempV = []
tempU = []
for i in range(len(resultP)) :
    tempV.append(resultP[i, "V"])
    tempU.append(resultP[i, "U"])

print("---------------- Step 2 ---------------------")
pne = Model("./example5.01/pne.mzn")
instanceE = Instance(gecode, pne)
instanceE["l"]  = len(resultP)
instanceE["Vs"] = tempV
instanceE["Us"] = tempU

resultE = instanceE.solve(all_solutions=True)
for i in range(len(resultE)) :
    print(resultE[i,"V"] ,end=" ")
    print(resultE[i,"U"] )
