import os
from random import randrange
os.system("clear")

from minizinc import Instance, Model, Solver

solver      = Solver.lookup("gecode")
nPlayers    = 5
nStrategies = 5
mznProblem  = "./example4.21/model/problem.mzn"
maxStep     = 20

P = set(range(0,nPlayers))

#--------------------------------------------------------------------

def CG_enum() :
    PNE = []

    model   = Model(mznProblem)

    text = (
    """
    solve :: int_search(V, input_order, indomain_random)
        satisfy;
    """
    )

    model.add_string(text)
    instance        = Instance(solver, model)
    instance["n"]   = nPlayers
    instance["s"]   = nStrategies
    solution        = instance.solve()
    try     : s,u   = solution["V"],solution["U"]
    except  : s     = None

    while s != None :
        if isPNE(s,u) :
            PNE.append(s)

        solution        = instance.solve()
        try     : s,u   = solution["V"],solution["U"]
        except  : s     = None
    return PNE

#--------------------------------------------------------------------

def isPNE(s,u) :
    for i in P :
        if devC_G(s,u,i) :
            return False
    return True

#--------------------------------------------------------------------

def devC_G(s,u,i) :
    model   = Model(mznProblem)

    text = (
    """
    int                     : p  = {};
    array [P] of S          : Vs = array1d(0..n-1, {});
    array [P] of AmountS    : Us = array1d(0..n-1, {});

    constraint
        U[p] > Us[p];

    constraint
        forall(i in P where i != p)(
            V[i] = Vs[i]
        );

    solve :: int_search(V, input_order, indomain_random)
        maximize U[p];
    """
    ).format(i,s,u)

    model.add_string(text)
    instance        = Instance(solver, model)
    instance["n"]   = nPlayers
    instance["s"]   = nStrategies
    solution        = instance.solve()
    try     : s_    = solution["V"]; 
    except  : s_    = None

    if s_ != None :
        if s_ == s :
            return False
        else :
            return True
    else :
        return False

#--------------------------------------------------------------------

ss = CG_enum()

for s in ss :
    print(s)
