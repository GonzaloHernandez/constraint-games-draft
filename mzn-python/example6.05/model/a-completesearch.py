import os, minizinc, asyncio

os.system("clear")

solver      = minizinc.Solver.lookup("gecode")
model       = minizinc.Model("./example6.05/model/problem.mzn")

#--------------------------------------------------------------

async def testing_all_results() :
    inst = minizinc.Instance(solver, model)
    
    async for result in inst.solutions(all_solutions=True) :
        if result.solution is None : continue

        v,u = result["V"],result["U"]
        print(str(v)+" "+str(u))

#--------------------------------------------------------------

asyncio.run(testing_all_results())

#==============================================================

