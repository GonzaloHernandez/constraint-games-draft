import os, time
os.system("clear")

from minizinc import Instance, Model, Solver

solver      = Solver.lookup("gecode")
nPlayers    = 7
nStrategies = 5
mznGameFile = "./solving/example4.21/model/problem.mzn"
mznPNEFile  = "./solving/example4.21/model/pne.mzn"

print("\n-------------- Step 1 ---------------")

game            = Model(mznGameFile)
insGame         = Instance(solver, game)
insGame["n"]    = nPlayers
insGame["s"]    = nStrategies

start   = time.time()
resGame = insGame.solve(all_solutions=True)
end     = time.time()

for i in range(len(resGame)) :
    print(resGame[i,"V"],end=",")
    print(resGame[i,"U"])
print(f"Total solutions: {len(resGame)} [{(end-start):.2f}sg]")

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

start   = time.time()
resPNE  = insPNE.solve(all_solutions=True)
end     = time.time()

# print(resPNE["V"], end="  ")
# print(resPNE["U"])

for i in range(len(resPNE)) :
    print(resPNE[i,"V"], end="  ")
    print(resPNE[i,"U"])
print(f"Total solutions: {len(resPNE)} [{(end-start):.2f}sg]")

print()

# players 7 / strategies 5 / loops 35156 / [1556.76sg]
