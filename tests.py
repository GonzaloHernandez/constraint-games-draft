import os, copy
os.system("clear")

from SimpleCOPSolver import *

x   = IntVar('x0',1,9)
y   = IntVar('y1',1,9)
z   = IntVar('z2',1,3)
ux  = IntVar('u3',0,1)
uy  = IntVar('u4',0,1)
uz  = IntVar('u5',0,1)

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

V = [ x, y, z]
U = [ux,uy,uz]
G = [gx,gy,gz]

S = solveModel( V+U, G, minimize(x+y), tops=10)

for s in S :
    printvars(s)
    
print(f"Total Solutions: {len(S)}")

# _start  = time.time()   # PROFILER
# _end    = time.time()   # PROFILER
# print(f"PROFILER: {(_end-_start):.2f}sg")

