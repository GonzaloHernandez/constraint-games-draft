import os, copy, math
os.system("clear")

#====================================================================

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

    #--------------------------------------------------------------
    def __str__(self) -> str:
        if self.isFailed() :
            return f"{self.name}()"
        elif self.isAssigned() :
            return f"{self.name}{{{str(self.min)}}}"
        else :
            return f"{self.name}{{{str(self.min)}..{str(self.max)}}}"

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

class SearchInstance :
    def __init__(self, vars, cons) -> None:
        self.vars = vars
        self.cons = cons
    
    #--------------------------------------------------------------
    def propagate(self) :
        for c in self.cons :
            c.prune()
        
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

                    left    .propagate()
                    right   .propagate()
                    break

#====================================================================

class Expression (Operable):
    def __init__(self, exp1, oper, exp2) -> None:
        self.exp1 = exp1
        self.oper = oper
        self.exp2 = exp2

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
            case "+" :
                [self.min, self.max] = [lmin+rmin , lmax+rmax]
            case "-" :
                [self.min, self.max] = [lmin-rmax , lmax-rmin]
            case "*" :
                [self.min, self.max] = [
                    min(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax),
                    max(lmin*rmin, lmin*rmax, lmax*rmin, lmax*rmax)
                ]
            case "==" :
                [self.min, self.max] = [max(lmin,rmin), min(lmax,rmax)]

        return [self.min, self.max]

    #--------------------------------------------------------------
    def project(self, newmin, newmax) :
        [premin, premax] = [self.min, self.max]
        [curmin, curmax] = max(premin,newmin), min(premax, newmax)

        match self.oper :
            case "==" :
                self.exp1.project(curmin, curmax)
                self.exp2.project(curmin, curmax)
            case "+" :
                [rmin,rmax] = [self.exp2.min, self.exp2.max]
                [lmin,lmax] = [curmin-rmax,curmax-rmin]
                self.exp1.project(lmin, lmax)

                [lmin,lmax] = [self.exp1.min, self.exp1.max]
                [rmin,rmax] = [curmin-lmax,curmax-lmin]
                self.exp2.project(rmin, rmax)
            case "-" :
                [rmin,rmax] = [self.exp2.min, self.exp2.max]
                [lmin,lmax] = [curmin+rmin,curmax+rmax]
                self.exp1.project(lmin, lmax)

                [lmin,lmax] = [self.exp1.min, self.exp1.max]
                [rmin,rmax] = [curmin+lmin,curmax+rmax]
                self.exp2.project(rmin, rmax)
            case "*" :
                [lmin,lmax] = [self.exp1.min, self.exp1.max]
                [rmin,rmax] = [self.exp2.min, self.exp2.max]


                if rmin == 0 : rmin = 1
                if rmax == 0 : rmax = 1
                
                [lmin,lmax] = [
                    min(newmin//rmin, newmin//rmax, newmax//rmin, newmax//rmax),
                    max(math.ceil(newmin/rmin), math.ceil(newmin*rmax), 
                        math.ceil(newmax*rmin), math.ceil(newmax*rmax))
                ]
                self.exp1.project(lmin, lmax)

                if lmin == 0 : lmin = 1
                if lmax == 0 : lmax = 1

                [rmin,rmax] = [
                    min(newmin//lmin, newmin//lmax, newmax//lmin, newmax//lmax),
                    max(math.ceil(newmin/lmin), math.ceil(newmin*lmax), 
                        math.ceil(newmax*lmin), math.ceil(newmax*lmax))
                ]
                self.exp2.project(rmin, rmax)

#====================================================================

class Constraint :
    def __init__(self, exp) -> None:
        self.exp = exp

    def __str__(self) -> str:
        return str(self.exp)
    
    def prune(self) :
        [min,max] = self.exp.evaluate()
        self.exp.project( min,max )

#====================================================================

x = IntVar('x', 2,6)
y = IntVar('y',-2,5)
z = IntVar('y', 1,3)

i1  = SearchInstance(
        [x,y,z],
        [
            Constraint(
                x == y * z
            )
        ])

i2 = copy.deepcopy(i1)

i1.propagate()

#====================================================================

