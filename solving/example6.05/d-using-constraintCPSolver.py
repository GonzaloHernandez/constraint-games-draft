import os,sys

os.system("clear")

#--------------------------------------------------------------

sys.path.insert(1,".")
from ConstraintCPSolver import *

x   = IntVar( 'x',1,9)
y   = IntVar( 'y',1,9)
z   = IntVar( 'z',1,3)
w   = IntVar( 'w',1,3)
ux  = IntVar('ux',0,1)
uy  = IntVar('uy',0,1)
uz  = IntVar('uz',0,1)
uw  = IntVar('uw',0,1)

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

gw = Constraint(
    uw == (x < w)
)

V   = [ x, y, z, w]
U   = [ux,uy,uz,uw]
G   = [gx,gy,gz,gw]

S = solveModelPNE( V, U, G)

for n in S :
    print(n)

print(f"Total PNE: {len(S)}")
