import os, minizinc, asyncio

os.system("clear")

solver      = minizinc.Solver.lookup("gecode")
model       = minizinc.Model("./example6.05/model/problem.mzn")
D           = []

#--------------------------------------------------------------

async def testing_all_results() :
    inst = minizinc.Instance(solver, model)
    
    async for result in inst.solutions(all_solutions=True) :
        if result.solution is None : continue

        s,u = result["S"],result["U"]
        print(str(s)+" "+str(u))
        D.append(s)

#--------------------------------------------------------------

asyncio.run(testing_all_results())

#==============================================================

br      = []
cnt     = []
nash    = []

#--------------------------------------------------------------

def CG_enum() :
    nash = []
    inst = minizinc.Instance(solver, model)
    A = D
    enum(a,1)
    return nash

#--------------------------------------------------------------

def enum(A,i) :
    