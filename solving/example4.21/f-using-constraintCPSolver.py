import os, sys, time
os.system("clear")

sys.path.insert(1,".")
from ConstraintCPSolver import *

np, ns = 6, 5   # number of players, number of strategies

V = IntVarArray(np,'v',0,ns-1)
U = IntVarArray(np,'u',1,np)

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

# players 7 / strategies 5 / loops 35156 / [170.17sg] mac laptop
# players 7 / strategies 5 / loops 97656 / [193.65sg] mac laptop

# players 7 / strategies 5 / loops 35156 / [318.83sg] mac desktop
# players 7 / strategies 5 / loops 97656 / [384.05sg] mac desktop
