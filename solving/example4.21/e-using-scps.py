import os,sys
os.system("clear")

sys.path.insert(1,".")
from SimpleCPSolver import IntVarArray, Constraint, SearchInstance
from SimpleCPSolver import count,printlist,solveModel

V  = IntVarArray(5,'v',0,4)
U  = IntVarArray(5,'u',1,5)

G  = []
for i in range(len(V)) :
    G.append(
        Constraint(
            U[i] == count(V,V[i])
        )
    )

C  = [
    Constraint( V[0]!=V[1]),
    Constraint((V[2]==2) & (V[3]==3) & (V[4]==4)),
]
                         
S = solveModel(V+U, G+C)

for s in S:
    printlist(s)
