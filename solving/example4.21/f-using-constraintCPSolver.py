import os, sys, time
os.system("clear")

sys.path.insert(1,".")
from ConstraintCPSolver import *

np, ns = 7, 5   # number of players, number of strategies

V = IntVarArray(np,0,ns-1,'v')
U = IntVarArray(np,1,np,'u')

G = []
F = []
for i in range(len(V)) :
    G.append(
        Constraint(
            U[i] == count(V,V[i])
        )
    )
    F.append( maximize( U[i] ) )


start   = time.time()
S = solveModelPNE( V, U, G, F)
end     = time.time()

for n in S :
    print(n)
print(f"Total PNE: {len(S)} [{(end-start):.2f}sg]")

# mac desktop
# players 7 / strategies 5 / loops 35156 / [224.62sg] [192.87sg]
# players 7 / strategies 5 / loops 97656 / [384.05sg] 
