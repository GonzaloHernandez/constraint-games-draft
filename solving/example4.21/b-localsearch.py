import os
import warnings
from random import randrange
os.system("clear")

from minizinc import Instance, Model, Solver

solver      = Solver.lookup("gecode")
nPlayers    = 5
nStrategies = 5
mznFile     = "./solving/example4.21/model/problem.mzn"
maxStep     = 20

P = set(range(0,nPlayers))
T = []

#--------------------------------------------------------------------

def CG_IBR() :
    model           = Model(mznFile)

    text = (
    """
    solve :: int_search(V, input_order, indomain_max)
        satisfy;
    """
    )

    model.add_string(text)

    instance        = Instance(solver, model)
    instance["n"]   = nPlayers
    instance["s"]   = nStrategies
    solution        = instance.solve()
    if solution != None :
        s,u = solution["V"],solution["U"]
    
        step = 0
        while step < maxStep :
            s_ = neighborIBR(s,u,P)
            T.append(s_)
            if s_ != None :
                s = s_
            else :
                return s
            step += 1

    return None

#--------------------------------------------------------------------

def neighborIBR(s,u,P) :
    while len(P) > 0 :
        i = list(P)[randrange(len(P))]
        s_= findBRC_G(s,u,i)
        if s_ != None and not T.__contains__(s_):
            T.append(s_)
            return s_
        P.remove(i)
    return None

#--------------------------------------------------------------------

def findBRC_G(s,u,i) :
    model           = Model(mznFile)

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

    solve :: int_search(V, input_order, indomain_min)
        maximize U[p];
    """
    ).format(i,s,u)

    model.add_string(text)

    instance        = Instance(solver, model)
    instance["n"]   = nPlayers
    instance["s"]   = nStrategies
 
    with warnings.catch_warnings() : 
        warnings.simplefilter("ignore")
        solution    = instance.solve()

    if solution.__len__() == 0 :
        return None
    else :
        return solution["V"]

#--------------------------------------------------------------------

s = CG_IBR()

print("PNE Strategy:       " + str(s))
