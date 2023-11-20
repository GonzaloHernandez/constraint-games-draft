import os, sys
os.system("clear")

sys.path.insert(1,".")
from ConstraintCPSolver import *

V  = IntVarArray(5,'v',0,4)
U  = IntVarArray(5,'u',1,5)

G  = []
for i in range(len(V)) :
    G.append(
        Constraint(
            U[i] == count(V,V[i])
        )
    )

S = solveModelPNE( V, U, G)

for n in S :
    print(n)
print(f"Total PNE: {len(S)}")

# NOTE: Waiting for code the optimization option in solver
