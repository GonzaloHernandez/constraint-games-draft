import os, sys
os.system("clear")

sys.path.insert(1, '.')
from SimpleCPSolver import IntVar, Constraint, SearchInstance

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

s = SearchInstance(
    [x,y,z,ux,uy,uz],
    [gx,gy,gz,
        # Constraint(
        #     (x==1) & 
        #     (y==1) &
        #     (uz==1)
        # )
    ]
)

s.propagate()