import os, minizinc, asyncio

os.system("clear")

#--------------------------------------------------------------

from SimpleCPSolver_tailored import IntVar, Constraint, printlist
import copy

x   = IntVar( 'x',1,9)
y   = IntVar( 'y',1,9)
z   = IntVar( 'z',1,3)
ux  = IntVar('ux',0,1)
uy  = IntVar('uy',0,1)
uz  = IntVar('uz',0,1)

gx = Constraint(
    ux == (x == (y*z))
)

gy = Constraint(
    uy == (y == (x*z))
)

gz = Constraint(
    uz == (
        (((x*y) <= z) & (z <= (x+y)))
        &
        (((x+1)*(y+1)) != (z*3))
    )
)

#--------------------------------------------------------------

Nash    = []
BR      = [[],[],[]]
cnt     = [0,0,0]
n       = 3

#--------------------------------------------------------------

def findBestResponse(t,i) :
    solver  = minizinc.Solver.lookup("gecode")
    model   = minizinc.Model("./example6.05/model/problem.mzn")

    text = (
    """
    int              : pi;
    P                : p = P[pi];
    array [P] of int : S_;

    constraint
	    forall(i in P where i != p)(
		    S_[i] = S[i]
    	);

    constraint
	    U[p] = 1;
    """
    )

    model.add_string(text)

    inst    = minizinc.Instance(solver, model)

    inst["pi"] = i
    inst["S_"] = t
    d = []

    inst = inst.solve(all_solutions=True)

    for i in range(len(inst)):
        s = inst[i,"S"]
        d.append(s)
    return d

#--------------------------------------------------------------

def checkNash(t,i) :
    if i==0 :
        Nash.append(t)
    else :
        d = search_table(t,i)
        if d is None :
            d = findBestResponse(t,i)
            # pendant to insert other not best responses
            insert_table(i,d)
            cnt[i-1] -= 1
        if t in d :
            checkNash(t,i-1)

#--------------------------------------------------------------

def search_table(t,i) :
    if t in BR[i-1] :
        return t
    return None

#--------------------------------------------------------------

def insert_table(i,d) :
    for t in d :
        BR[i-1].append(t)

#--------------------------------------------------------------

def checkEndOfTable(A,i) :
    for a in A :
        for t in BR[i] :
            checkNash(t,n)

#--------------------------------------------------------------

class SearchInstance :
    def __init__(self, vars, cons) -> None:
        self.vars = vars
        self.cons = cons
    
    #--------------------------------------------------------------
    def propagate(self,i_) :
        for c in self.cons :
            if c.prune() is False : return None
        
        for v in self.vars :
            if v.isFailed() :
                return None
        
        assigned = True
        for v in self.vars :
            if not v.isAssigned() :
                assigned = False
        
        if assigned :
            printlist(self.vars)
            checkNash([self.vars[0].min, self.vars[1].min, self.vars[2].min], n)
            return self.vars
        else :
            BR[i_] = []
            match i_ :
                case 0 : cnt[i_] = 27
                case 1 : cnt[i_] = 9
                case 2 : cnt[i_] = 1
            
            for i,v in enumerate(self.vars) :
                if not v.isAssigned():
                    left    = copy.deepcopy(self)
                    right   = copy.deepcopy(self)

                    left    .vars[i].setle(right.vars[i].min)
                    right   .vars[i].setge(right.vars[i].min+1)

                    left    .propagate(i_+1)
                    right   .propagate(i_+1)

                    if cnt[i_] <= 0 :
                        checkEndOfTable(vars, i_)

                    break

#====================================================================

s = SearchInstance(
    [x,y,z,ux,uy,uz],
    [gx,gy,gz]
)

s.propagate(0)