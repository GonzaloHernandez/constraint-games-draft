import sys

#--------------------------------------------------------------

sys.path.insert(1,".")
from PythonCPSolver import *
import copy

#--------------------------------------------------------------

class Globals :
    def __init__(self,V,U,G,F) -> None:
        self.Nash   = []
        self.BR     = []
        self.cnt    = []
        self.n      = len(V)
        self.V      = V
        self.U      = U
        self.G      = G
        self.F      = F
        self.count  = 0     # for debugging purposes, counting loops

        for i in range(self.n) : 
            self.BR.append([])
            self.cnt.append(0)

#--------------------------------------------------------------

class SearchInstancePNE :
    def __init__(self, V, U, G, F) -> None:
        self.vars = V
        self.cons = G
        self.glob = Globals(V,U,G,F)

    #--------------------------------------------------------------
    def propagate(self) :
        t1 = 0
        for v in self.vars : t1 += v.card()

        for c in self.cons :
            if c.prune() is False : 
                return []

        t2 = 0
        for v in self.vars : t2 += v.max - v.min + 1

        if t2 < t1 :
            return self.propagate()
        else :
            return True

    #--------------------------------------------------------------
    def search(self, i) :
        self.glob.count += 1

        if not self.propagate() : return []
        
        for v in self.vars :
            if v.isFailed() :
                return []
        
        if i==self.glob.n :
            t = []
            for v in self.vars : t.append(v.min)

            self.checkNash(t,self.glob.n-1)
            return [self.vars]
        else :
            self.glob.BR[i]   = []
            self.glob.cnt[i]  = 1
            for j in range(i+1,len(self.glob.V)) :
                self.glob.cnt[i] *= self.glob.V[j].card()

            for j in range(self.vars[i].min, self.vars[i].max+1) :
                branch = self.clone()

                branch.vars[i].setle(j)
                branch.vars[i].setge(j)

                branch.search(i+1)

                if self.glob.cnt[i] <= 0 :
                    self.checkEndOfTable(i)
                    break
    
    #--------------------------------------------------------------
    def clone(self) :
        branch = copy.copy(self)
        branch.vars, branch.cons = copy.deepcopy([self.vars, self.cons])
        return branch

    #--------------------------------------------------------------
    def checkNash(self,t,i) :
        if i<0 :
            if t not in self.glob.Nash :
                self.glob.Nash.append(t)
        else :
            d = self.search_table(t,i)
            if d == [] :
                d = self.findBestResponse(t,i)
                
                if d == [] :

                    C = []
                    for j in range(len(self.glob.V)) :
                        if j != i :
                            C.append( Equation( self.glob.V[j] == t[j] ) )
                    S = solveModel(self.glob.V + self.glob.U, self.glob.G+C, tops=0)

                    for s in S :
                        
                        dt = []
                        for j in range(self.glob.n) :
                            dt.append(s[j].min)

                        d.append(dt)

                self.insert_table(i,d)
                self.glob.cnt[i] -= 1
            if t in d :
                self.checkNash(t,i-1)

    #--------------------------------------------------------------
    def findBestResponse(self,t,i) :
        C = []
        S = []
        for j in range(len(self.glob.V)) :
            if j != i :
                C.append( Equation( self.glob.V[j] == t[j] ) )
    
        if self.glob.F == [] :
            C.append( Equation( self.glob.U[i] == 1) )
            S = solveModel( self.glob.V + self.glob.U , self.glob.G + C , tops=0 )
        else :
            F = self.glob.F[i]
            S = solveModel( self.glob.V + self.glob.U , self.glob.G + C , F )
            # Pendig to search all optimima solutions
 
        d = []

        for s in S :
            dt = []
            for j in range(self.glob.n) :
                dt.append(s[j].min)
            d.append(dt)

        return d

    #--------------------------------------------------------------

    def checkEndOfTable(self,i) :
        for t in self.glob.BR[i] :
            self.checkNash(t,self.glob.n-1)

    #--------------------------------------------------------------

    def search_table(self,t,i) :
        if len(self.glob.BR[i]) <= 0 : return []

        br = []

        for b in range(len(self.glob.BR[i])) :
            if self.glob.BR[i][b][1:i]+self.glob.BR[i][b][i+1:self.glob.n] == t[1:i]+t[i+1:self.glob.n] :
                br.append( self.glob.BR[i][b] )
        return br

    #--------------------------------------------------------------

    def insert_table(self,i,d) :
        for t in d :
            if t not in self.glob.BR[i] :
                self.glob.BR[i].append(t)

#====================================================================

def solveModelPNE(V,U,G,F=[]) :
    model = copy.deepcopy([V,U,G,F])
    s = SearchInstancePNE(model[0],model[1],model[2],model[3])
    s.search(0)
    print("total loops: "+str(s.glob.count))
    return s.glob.Nash

#--------------------------------------------------------------

