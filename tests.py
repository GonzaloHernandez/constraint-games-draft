import os
os.system("clear")

from SimpleCPSolver import IntVar, Constraint, SearchInstance

x = IntVar('x',1,3)
y = IntVar('y',1,3)
z = IntVar('z',1,3)
u = IntVar('u',0,1)

s = SearchInstance(
        [x, y, z, u],
        [
            Constraint(
                u == (y == x*z)
            )
        ]
)

s.propagate()