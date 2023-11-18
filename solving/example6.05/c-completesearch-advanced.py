import os,sys

os.system("clear")

#--------------------------------------------------------------

sys.path.insert(1,".")

from SimpleCPSolver import IntVar, Constraint, solveModel, printlist
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

V   = [ x, y, z]
U   = [ux,uy,uz]
G   = [gx,gy,gz]

#--------------------------------------------------------------

Nash    = []
BR      = [[],[],[]]
cnt     = [0,0,0]
n       = 3

#--------------------------------------------------------------

def findBestResponse(t,u,i) :

    C = []
    for j in range(len(V)) :
        if j != i :
            C.append( Constraint( V[j] == t[j] ) )

    C.append( Constraint( U[i] > u[i] ))
 
    S = solveModel( V + [U[i]] , [G[i]] + C )

    d = []

    for s in S :
        d.append([s[0].min, s[1].min, s[2].min])

    return d

#--------------------------------------------------------------

def checkNash(t,u,i) :
    if i<0 :
        Nash.append(t+u)
    else :
        # d = search_table(t,i)
        # if d is None :
            # d = findBestResponse(t,u,i)
            # pendant to insert other not best responses
            # insert_table(i,d)
            # cnt[i-1] -= 1
        # if t in d :
        d = findBestResponse(t,u,i)
        insert_table(i,d)
        if d == [] :
            checkNash(t,u,i-1)

#--------------------------------------------------------------

def search_table(t,i) :
    if t in  BR[i] :
        return t
    return None

#--------------------------------------------------------------

def insert_table(i,d) :
    for t in d :
        BR[i].append(t)

#--------------------------------------------------------------

def checkEndOfTable(A,i) :
    for t in BR[i] :
        checkNash(t,n-1)

#--------------------------------------------------------------

class SearchInstanceTailored :
    def __init__(self, vars, cons) -> None:
        self.vars = vars
        self.cons = cons
    
    #--------------------------------------------------------------
    def search(self, i) :
        for c in self.cons :
            if c.prune() is False : 
                return []
        
        for v in self.vars :
            if v.isFailed() :
                return []
        
        if i==n :
            t = [self.vars[0].min, self.vars[1].min, self.vars[2].min]
            u = [self.vars[3].min, self.vars[4].min, self.vars[5].min]
            checkNash(t,u, n-1)
            return [self.vars]
        else :
            BR[i]   = []
            cnt[i]  = 1
            for j in range(i+1,len(V)) :
                cnt[i] *= V[j].card()

            s = []

            for j in range(self.vars[i].min, self.vars[i].max+1) :
                branch = copy.deepcopy(self)
 
                branch.vars[i].setle(j)
                branch.vars[i].setge(j)

                s += branch.search(i+1)

                # if cnt[i] <= 0 :
                #     checkEndOfTable(branch.vars, i)
                #     break
            return  s

#====================================================================

def solveModelTailored(vars, cons) :
    model = copy.deepcopy([vars,cons])
    s = SearchInstanceTailored(model[0],model[1])
    return s.search(0)

S = solveModelTailored( V+U, G)
for n in Nash :
    print(n)
print(f"Total solutions: {len(S)}")
print(f"Total PNE: {len(Nash)}")