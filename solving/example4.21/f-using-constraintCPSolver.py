import os, sys, time
os.system("clear")

sys.path.insert(1,".")
from ConstraintCPSolver import *

V  = IntVarArray(7,'v',0,4)
U  = IntVarArray(7,'u',1,7)

G  = []
for i in range(len(V)) :
    G.append(
        Constraint(
            U[i] == count(V,V[i])
        )
    )

start   = time.time()
S = solveModelPNE( V, U, G)
end     = time.time()


for n in S :
    print(n)
print(f"Total PNE: {len(S)} [{(end-start):.2f}sg]")

# players 7 / strategies 5 / loops 35156 / [170.17sg]
# players 7 / strategies 5 / loops 97656 / [193.65sg]
