import os, sys
os.system("clear")

sys.path.insert(1,".")
from SimpleCPSolver import IntVar, Constraint, solveModel, printlist

x   = IntVar( 'x',1,9)
y   = IntVar( 'y',1,9)
z   = IntVar( 'z',1,3)
ux  = IntVar('ux',0,1)
uy  = IntVar('uy',0,1)
uz  = IntVar('uz',0,1)

gx = Constraint(
    ux == (x == (y*z))
)

gy = Constraint(
    uy == (y == (x*z))
)

gz = Constraint(
    uz == (
        (((x*y) <= z) & (z <= (x+y)))
        &
        (((x+1)*(y+1)) != (z*3))
    )
)

V   = [ x, y, z]
U   = [ux,uy,uz]
G   = [gx,gy,gz]

t   = [2,2,1]
i   = 2

C = []
for j in range(len(V)) :
    if j != i :
        C.append( Constraint( V[j] == t[j] ) )

# C.append( Constraint( U[i] > u[i] ))

S = solveModel( V+U, G + C )

for s in S:
    printlist(s)
