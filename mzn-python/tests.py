import os
os.system("clear")

from SimpleCPSolver import IntVar, Constraint, SearchInstance

x = IntVar('x',1,5)
y = IntVar('y',1,5)
z = IntVar('z',1,5)

s = SearchInstance([x, y, z],[
    Constraint( x == y + 1 ),
    Constraint( z >= x * 2 )
])

s.propagate()