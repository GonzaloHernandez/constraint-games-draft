from datetime import datetime
import os
os.system("clear")

from minizinc import Instance, Model, Solver

class Chronometer :
    def __init__(self) -> None:
        self.t1 = 0
        self.t2 = 0
        self.tt = 0

    def start(self) :
        self.t1 = datetime.utcnow() - datetime(1970, 1, 1)

    def stop(self) :
        self.t2 = datetime.utcnow() - datetime(1970, 1, 1)
        self.tt = self.t2.total_seconds()-self.t1.total_seconds()
        return round(self.tt*100)/100
    
    def get(self) :
        return round(self.tt*100)/100
    
    def __str__(self) -> str:
        return str(round(self.tt*100)/100)

chron       = Chronometer()
solver      = Solver.lookup("gecode")
nPlayers    = 5
nStrategies = 5
mznGameFile = "./example4.21/model/problem.mzn"
mznPNEFile  = "./example4.21/model/pne.mzn"

print("\n-------------- Step 1 ---------------")

game            = Model(mznGameFile)
insGame         = Instance(solver, game)
insGame["n"]    = nPlayers
insGame["s"]    = nStrategies

chron.start()
resGame = insGame.solve(all_solutions=True)
chron.stop()

# for i in range(len(resGame)) :
#     print(resGame[i,"V"],end=",")
#     print(resGame[i,"U"])
print("Total solutions: " + str(len(resGame)) + " [" + str(chron) + "sg]")

#-----------------------------------------------

Vaux = []
Uaux = []
for i in range(len(resGame)) :
    Vaux.append(resGame[i,"V"])
    Uaux.append(resGame[i,"U"])


print("\n-------------- Step 2 ---------------")

pne             = Model(mznPNEFile)
insPNE          = Instance(solver, pne)
insPNE["n"]     = nPlayers
insPNE["s"]     = nStrategies
insPNE["l"]     = len(resGame)
insPNE["Vs"]    = Vaux
insPNE["Us"]    = Uaux

chron.start()
resPNE = insPNE.solve(all_solutions=True)
chron.stop()

# print(resPNE["V"], end="  ")
# print(resPNE["U"])

for i in range(len(resPNE)) :
    print(resPNE[i,"V"], end="  ")
    print(resPNE[i,"U"])
print("Total solutions: " + str(len(resPNE)) + " [" + str(chron) + "sg]")

print()
