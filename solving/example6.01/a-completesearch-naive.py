import os, asyncio
os.system("clear")

from minizinc import Instance, Model, Solver

solver      = Solver.lookup("gecode")
mznProblem  = "./solving/example6.01/model/problem.mzn"

P   = set(range(1,3))
PNE = []

#--------------------------------------------------------------------

async def CG_enum() :

    model       = Model(mznProblem)
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
    int             : p  = {};
    array [P] of D  : Vs = {};
    array [P] of B  : Us = {};

    constraint
        forall(i in P where i != p)(
            V[i] = Vs[i]
        );

    constraint
        U[p] = true;
    """
    ).format(i,s,u)

    model.add_string(text)
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
