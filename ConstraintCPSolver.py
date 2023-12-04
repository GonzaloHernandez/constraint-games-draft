import sys, time

#--------------------------------------------------------------

sys.path.insert(1,".")
from SimpleCOPSolver import *
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
        self.count  = 0

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
    def search(self, i) :
        self.glob.count += 1
        for c in self.cons :
            if c.prune() is False : 
                return []
        
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
        self = copy.copy(self)
        self.vars,self.cons = copy.deepcopy([self.vars,self.cons])
        return self

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
                            C.append( Constraint( self.glob.V[j] == t[j] ) )

                    S_ = solveModel(self.glob.V + self.glob.U, self.glob.G+C, tops=0)

                    for s in S_ :
                        
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
        for j in range(len(self.glob.V)) :
            if j != i :
                C.append( Constraint( self.glob.V[j] == t[j] ) )
    
        if self.glob.F == [] :
            C.append( Constraint( self.glob.U[i] == 1))
            F = [0,None]
        else :
            F = self.glob.F[i]

        S = solveModel( self.glob.V + self.glob.U , self.glob.G + C , F, tops=0 )

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

