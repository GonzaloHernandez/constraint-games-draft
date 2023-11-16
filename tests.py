import os
os.system("clear")

from SimpleCPSolver import IntVar, Constraint, SearchInstance
from SimpleCPSolver import sum,count,alldifferent


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
    [gx,gy,gz]
)

s.search()
