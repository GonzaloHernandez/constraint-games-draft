import os, minizinc, asyncio

os.system("clear")

solver      = minizinc.Solver.lookup("gecode")
model       = minizinc.Model("./example6.05/model/problem.mzn")

#-------------------------------------------------------------- Step 1

async def searching_all_results() :
    inst = minizinc.Instance(solver, model)
    Ss = []
    Us = []
    
    async for result in inst.solutions(all_solutions=True) :
        if result.solution is None : continue

        s,u = result["S"],result["U"]
        Ss.append(result["S"])
        Us.append(result["U"])
        # print(str(s)+" "+str(u))
    return Ss,Us

Ss,Us = asyncio.run(searching_all_results())
print(f"Total solutions: {len(Ss)}")

#----------------------------------------------------------n---- Step 2

async def searching_pne(Ss,Us) :
    text = (
    """
    int                 : l;
    set of int          : R =  0..l-1;
    array [R,P] of int  : Ss;
    array [R,P] of B    : Us;

    var bool            : E;

    constraint
        exists(r in R)(
            forall(i in P)(
                Ss[r,i] = S[i] /\ Us[r,i] = U[i]
            )
        );

    constraint
        E = true;

    constraint
        E <-> not exists(p in P)(
            exists(r in R)(
                Us[r,p] > U[p]
                /\\
                forall(i in P where i != p)(
                    Ss[r,i] = S[i]
                )
            )
        );
    """
    )

    model.add_string(text)

    inst = minizinc.Instance(solver, model)
    
    inst["l"]  = len(Ss)
    inst["Ss"] = Ss
    inst["Us"] = Us
    nash = []
    async for result in inst.solutions(all_solutions=True) :
        if result.solution is None : continue

        s,u = result["S"],result["U"]
        print(str(s)+" "+str(u))
        nash.append([s,u])
    return nash

nash = asyncio.run(searching_pne(Ss,Us))
print(f"Total PNE solutions: {len(nash)}")
