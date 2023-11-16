#====================================================================
# 
# Simple Constraint Programming Solver V1.0
# Gonzalo Hernandez
# 
# This file is inherited from solver.py
#====================================================================

import copy, math

def printlist(ls) :
    print("[ ",end="")
    for l in ls : print(l,end=" ")
    print("]")

#====================================================================

class Operable :
    def __add__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"+",exp)

    def __sub__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"-",exp)

    def __mul__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"*",exp)

    def __mul__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"*",exp)

    def __eq__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"==",exp)

    def __ne__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"!=",exp)

    def __lt__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"<",exp)

    def __le__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"<=",exp)

    def __gt__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,">",exp)

    def __ge__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,">=",exp)

    def __and__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"&",exp)

    def __or__(self, exp) :
        if isinstance(exp, int) : exp = IntVar("_",exp,exp)
        return Expression(self,"|",exp)

#====================================================================

class IntVar (Operable) :
    def __init__(self, name, min, max) -> None:
        self.name   = name
        self.min    = min
        self.max    = max

    # #--------------------------------------------------------------
    # def __str__(self) -> str:
    #     if self.isFailed() :
    #         return f"{self.name}()"
    #     elif self.isAssigned() :
    #         return f"{self.name}{{{str(self.min)}}}"
    #     else :
    #         return f"{self.name}{{{str(self.min)}..{str(self.max)}}}"

    # #--------------------------------------------------------------
    # def __str__(self) -> str:
    #     if self.name == "_" :
    #         return str(self.min)
    #     else :
    #         return str(self.name)

    #--------------------------------------------------------------
    def __str__(self) -> str:
        if self.isFailed() :
            return "_"
        elif self.isAssigned() :
            return f"{self.min}"
        else :
            return f"{{{str(self.min)}..{str(self.max)}}}"

    #--------------------------------------------------------------
    def setge(self, val) :
        self.min = max(self.min, val)

    def setle(self, val) :
        self.max = min(self.max, val)

    def isAssigned(self) :
        return (self.min==self.max)
    
    def isFailed(self) :
        return (self.min>self.max)
    
    def evaluate(self) :
        return [self.min, self.max]

    def project(self, newmin, newmax) :
        self.setge(newmin)
        self.setle(newmax)

#====================================================================

class Expression (Operable) :
    def __init__(self, exp1, oper, exp2) -> None:
        self.exp1 = exp1
        self.oper = oper
        self.exp2 = exp2

    #--------------------------------------------------------------
    def __str__(self) -> str:
        if self.oper is None :
            return str(self.exp1)
        else :
            return "("+str(self.exp1) + self.oper + str(self.exp2)+")"

    #--------------------------------------------------------------
    def evaluate(self) :
        [lmin,lmax] = self.exp1.evaluate()
        [rmin,rmax] = self.exp2.evaluate()

        match self.oper :

            case "==" :
                if lmin == rmin == lmax == rmax :
                    self.min = self.max = 1
                elif lmin > rmax or rmin > lmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "!=" :
                if lmax<rmin or rmax<lmin :
                    self.min = self.max = 1
                elif lmin == rmin == lmax == rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "<" :
                if lmax < rmin :
                    self.min = self.max = 1
                elif lmin >= rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case ">" :
                if lmin > rmax :
                    self.min = self.max = 1
                elif lmax <= rmin :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "<=" :
                if lmax <= rmin :
                    self.min = self.max = 1
                elif lmin > rmax :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case ">=" :
                if lmin >= rmax :
                    self.min = self.max = 1
                elif lmax < rmin :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "&" :
                if lmin >= 1 and rmin >= 1 :
                    self.min = self.max = 1
                elif lmax <= 0 or rmax <= 0 :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "|" :
                if lmin >= 1 or rmin >= 1 :
                    self.min = self.max = 1
                elif lmax <= 0 and rmax <= 0 :
                    self.min = self.max = 0
                else :
                    [self.min, self.max] = [0,1]

            case "+" :
                [self.min, self.max] = [lmin+rmin , lmax+rmax]
            case "-" :
                [self.min, self.max] = [lmin-rmax , lmax-rmin]
            case "*" :
                [self.min, self.max] = [
                    min(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax),
                    max(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax)
                ]

        return [self.min, self.max]

    #--------------------------------------------------------------
    def project(self, nmin, nmax) :
        if nmin > nmax : return False
        
        [lmin,lmax] = [self.exp1.min, self.exp1.max]
        [rmin,rmax] = [self.exp2.min, self.exp2.max]

        match self.oper :
            case "==" :
                if nmin == nmax == 1 :
                    if self.exp1.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
                    if self.exp2.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
                if nmin == nmax == 0 :
                    if lmin == lmax == rmin == rmax :
                        if self.exp1.project( lmin+1 , lmax ) is False : return False
                        if self.exp2.project( rmin+1 , rmax ) is False : return False
            case "!=" : 
                if nmin == nmax == 1 :
                    if lmin == lmax == rmin == rmax :
                        if self.exp1.project( lmin+1 , lmax ) is False : return False
                        if self.exp2.project( rmin+1 , rmax ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
                    if self.exp2.project( max(lmin,rmin), min(lmax,rmax) ) is False : return False
            case "<" :
                if nmin == nmax == 1 :
                    if self.exp1.project( lmin  , rmax-1 ) is False : return False
                    if self.exp2.project( lmin+1, rmax   ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( rmin, lmax ) is False : return False
                    if self.exp2.project( rmin, lmax ) is False : return False
            case ">" :
                if nmin == nmax == 1 :
                    if self.exp1.project( rmin+1, lmax   ) is False : return False
                    if self.exp2.project( rmin  , lmax-1 ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( lmin, rmax ) is False : return False
                    if self.exp2.project( lmin, rmax ) is False : return False
            case "<=" :
                if nmin == nmax == 1 :
                    if self.exp1.project( lmin, rmax ) is False : return False
                    if self.exp2.project( lmin, rmax ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( rmin+1, lmax   ) is False : return False
                    if self.exp2.project( rmin  , lmax-1 ) is False : return False
            case ">=" :
                if nmin == nmax == 1 :
                    if self.exp1.project( rmin, lmax ) is False : return False
                    if self.exp2.project( rmin, lmax ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( lmin  , rmax-1 ) is False : return False
                    if self.exp2.project( lmin+1, rmax   ) is False : return False

            case "&" :
                if nmin == nmax == 1 :
                    if self.exp1.project( 1, lmax ) is False : return False
                    if self.exp2.project( 1, rmax ) is False : return False
                if nmin == nmax == 0 :
                    if rmin == rmax == 1 :
                        if self.exp1.project( lmin, 0 ) is False : return False
                    if lmin == lmax == 1 :
                        if self.exp2.project( rmin, 0 ) is False : return False
            case "|" :
                if nmin == nmax == 1 :
                    if rmin == rmax == 0 :
                        if self.exp1.project( 1, lmax ) is False : return False
                    if lmin == lmax == 0 :
                        if self.exp2.project( 1, rmax ) is False : return False
                if nmin == nmax == 0 :
                    if self.exp1.project( lmin, 0 ) is False : return False
                    if self.exp2.project( rmin, 0 ) is False : return False

            case "+" :
                if self.exp1.project( nmin-rmax , nmax-rmin ) is False : return False
                if self.exp2.project( nmin-lmax , nmax-lmin ) is False : return False
            case "-" :
                if self.exp1.project( nmin+rmin , nmax+rmax ) is False : return False
                if self.exp2.project( lmin-nmax , lmax-nmin ) is False : return False
            case "*" :
                if rmin == 0 : rmin = 1
                if rmax == 0 : rmax = 1
                
                [lmin,lmax] = [
                    min(nmin//rmin, nmin//rmax, nmax//rmin, nmax//rmax),
                    max(math.ceil(nmin/rmin), math.ceil(nmin*rmax), 
                        math.ceil(nmax*rmin), math.ceil(nmax*rmax))
                ]
                if self.exp1.project(lmin, lmax) is False : return False

                if lmin == 0 : lmin = 1
                if lmax == 0 : lmax = 1

                [rmin,rmax] = [
                    min(nmin//lmin, nmin//lmax, nmax//lmin, nmax//lmax),
                    max(math.ceil(nmin/lmin), math.ceil(nmin*lmax), 
                        math.ceil(nmax*lmin), math.ceil(nmax*lmax))
                ]
                if self.exp2.project(rmin, rmax) is False : return False
        return True

#====================================================================

def sum(vars) :
    exp = vars[0]
    for i in range(1,len(vars)):
        exp = exp + vars[i]
    return exp

def count(vars,cond) :
    exp = vars[0]==cond
    for i in range(1,len(vars)):
        exp = exp + (vars[i]==cond)
    return exp

def alldifferent(vars) :
    exp = IntVar("",1,1)
    for i in range(len(vars)):
        for j in range(len(vars)):
            if (i != j) : 
                exp = exp & (vars[i] != vars[j])
    return exp

#====================================================================

class Constraint :
    def __init__(self, exp) -> None:
        self.exp = exp

    def __str__(self) -> str:
        return str(self.exp)
    
    def prune(self) :
        self.exp.evaluate()
        return self.exp.project(1,1)

#====================================================================

class SearchInstance :
    def __init__(self, vars, cons) -> None:
        self.vars = vars
        self.cons = cons
    
    #--------------------------------------------------------------
    def search(self) :
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
            return self.vars
        else :
            for i,v in enumerate(self.vars) :
                if not v.isAssigned():
                    left    = copy.deepcopy(self)
                    right   = copy.deepcopy(self)

                    left    .vars[i].setle(right.vars[i].min)
                    right   .vars[i].setge(right.vars[i].min+1)

                    left    .search()
                    right   .search()
                    break

#====================================================================
