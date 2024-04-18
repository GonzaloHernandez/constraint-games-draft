import os, sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver import IntVar, Equation, solveModel, printvars

x   = IntVar(1,9,'x')
y   = IntVar(1,9,'y')
z   = IntVar(1,3,'z')
ux  = IntVar(0,1,'ux')
uy  = IntVar(0,1,'uy')
uz  = IntVar(0,1,'uz')

gx = Equation(
    ux == (x == (y*z))
)

gy = Equation(
    uy == (y == (x*z))
)

gz = Equation(
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
        C.append( Equation( V[j] == t[j] ) )

# C.append( Constraint( U[i] > u[i] ))

S = solveModel( V+U, G+C, tops=0 )

for s in S:
    printvars(s)
