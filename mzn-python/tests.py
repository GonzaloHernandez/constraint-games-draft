import os
os.system("clear")

import asyncio
import minizinc

async def show_solutions() :
    model       = minizinc.Model("./example4.21/model/problem.mzn")
    model["n"]  = 1
    model["s"]  = 1
    solver      = minizinc.Solver.lookup("gecode")
    instance    = minizinc.Instance(solver, model)

    async for result in instance.solutions(all_solutions=True) :
        if result.solution is None : continue

        print(result["V"])

asyncio.run(show_solutions())


# import asyncio,time

# async def s() :
#     for _ in range(10) :
#         print(".")
#         time.sleep(0.3)
#     return 10

# async def main() :
#     print("1")
#     r = await s()
#     print(r)

# asyncio.run(main())