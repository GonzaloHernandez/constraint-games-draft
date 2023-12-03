import os, copy
os.system("clear")

from ConstraintCPSolver import *

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

# S = solveModelPNE( V, U, G)

# for n in S :
#     print(n)
    
# print(f"Total PNE: {len(S)}")

for i,v in enumerate(V) :
    if id(v)== id(z) :
        break


print("index of y : "+str(i))