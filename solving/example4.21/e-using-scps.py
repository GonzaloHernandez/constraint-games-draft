import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver import IntVarArray,solveModel,Equation,printvars,count

V  = IntVarArray(5,0,4,'v')
U  = IntVarArray(5,1,5,'u')

G  = []
for i in range(len(V)) :
    G.append(
        Equation(
            U[i] == count(V,V[i])
        )
    )

C  = [
    Equation( V[0]!=V[1]),
    Equation((V[2]==2) & (V[3]==3) & (V[4]==4)),
]
                         
S = solveModel(V+U, G+C, tops=0)

for s in S:
    printvars(s)
