import os,sys

os.system("clear")

#--------------------------------------------------------------

sys.path.insert(1,".")

from PythonCPSolver import IntVar, Equation, solveModel, printvars
import copy

x   = IntVar(1,9,'x')
y   = IntVar(1,9,'y')
z   = IntVar(1,3,'z')
ux  = IntVar(0,1,'ux')
uy  = IntVar(0,1,'uy')
uz  = IntVar(0,1,'uz')

gx = Equation(
    ux == (x == (y*z))
)

gy = Equation(
    uy == (y == (x*z))
)

gz = Equation(
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

def findBestResponse(t,i) :

    C = []
    for j in range(len(V)) :
        if j != i :
            C.append( Equation( V[j] == t[j] ) )

    C.append( Equation( U[i] == 1 ))
 
    S_ = solveModel( V + U , G + C )

    d = []

    for s in S_ :
        d.append([s[0].min, s[1].min, s[2].min])

    return d

#--------------------------------------------------------------

def checkNash(t,i) :
    if i<0 :
        if t not in Nash :
            Nash.append(t)
    else :
        d = search_table(t,i)
        if d == [] :
            d = findBestResponse(t,i)
            
            if d == [] :
                C = []
                for j in range(len(V)) :
                    if j != i :
                        C.append( Equation( V[j] == t[j] ) )
                        
                S_ = solveModel(V+U, G+C)
                for s in S_ :
                    d.append([s[0].min, s[1].min, s[2].min])

            insert_table(i,d)
            cnt[i] -= 1
        if t in d :
            checkNash(t,i-1)

#--------------------------------------------------------------

def search_table(t,i) :
    if len(BR[i]) <= 0 : return []

    br = []

    for b in range(len(BR[i])) :
        if BR[i][b][1:i]+BR[i][b][i+1:n] == t[1:i]+t[i+1:n]:
            br.append( BR[i][b] )
    return br

#--------------------------------------------------------------

def insert_table(i,d) :
    for t in d :
        if [t[0],t[1],t[2]] not in BR[i] :
            BR[i].append([t[0],t[1],t[2]])

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
            
            if  self.vars[0].min == 2 and self.vars[1].min == 2 and self.vars[2].min == 1 :
                pass
                
            checkNash(t,n-1)
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

                if cnt[i] <= 0 :
                    checkEndOfTable([branch.vars[0].min, branch.vars[1].min, branch.vars[2].min] , i)
                    break
            return  s

#====================================================================

def solveModelTailored(vars, cons) :
    model = copy.deepcopy([vars,cons])
    s = SearchInstanceTailored(model[0],model[1])
    return s.search(0)

#--------------------------------------------------------------

S = solveModelTailored( V, G)
for n in Nash :
    print(n)
print(f"Total solutions: {len(S)}")
print(f"Total PNE: {len(Nash)}")
