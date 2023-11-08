import os
import asyncio
from random import randrange
os.system("clear")

from minizinc import Instance, Model, Solver

solver      = Solver.lookup("gecode")
nPlayers    = 5
nStrategies = 5
mznProblem  = "./example4.21/model/problem.mzn"

P = set(range(0,nPlayers))

#--------------------------------------------------------------------

PNE = []

async def CG_enum() :

    model   = Model(mznProblem)

    text = (
    """
    solve :: int_search(V, input_order, indomain_min)
        satisfy;
    """
    )

    model.add_string(text)
    model["n"]  = nPlayers
    model["s"]  = nStrategies
    instance    = Instance(solver, model)

    async for result in instance.solutions(all_solutions=True) :
        if result.solution is None : continue

        s,u   = result["V"],result["U"]
        print(".",end="")
        if await isPNE(s,u) :
            print("\n"+str(s)+" "+str(u))
            PNE.append(s)

    return PNE

#--------------------------------------------------------------------

async def isPNE(s,u) :
    for i in P :
        if await devC_G(s,u,i) :
            return False
    return True

#--------------------------------------------------------------------

async def devC_G(s,u,i) :
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
    model["n"]  = nPlayers
    model["s"]  = nStrategies
    instance    = Instance(solver, model)

    async for result in instance.solutions(all_solutions=False) :
        if result.solution is None : return False
        else :
            s_  = result["V"]
            if s_ == s :
                return False
            else :
                return True

#--------------------------------------------------------------------

asyncio.run(CG_enum())
