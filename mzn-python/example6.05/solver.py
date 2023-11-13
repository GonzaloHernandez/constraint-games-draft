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
                if lmin==rmin and lmax==rmax :
                    self.min = self.max = 1
                elif lmin > rmax or rmin > lmax :
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
        [lmin,lmax] = [self.exp1.min, self.exp1.max]
        [rmin,rmax] = [self.exp2.min, self.exp2.max]

        match self.oper :
            case "==" :
                self.exp1.project( max(lmin,rmin), min(lmax,rmax) )
                self.exp2.project( max(lmin,rmin), min(lmax,rmax) )
            case "<" :
                if min == 1 :
                    self.exp1.project( lmin  , rmax-1 )
                    self.exp2.project( lmin+1, rmax   )
                if max == 0 :
                    self.exp1.project( rmin, lmax )
                    self.exp2.project( rmin, lmax )                    
            case ">" :
                if min == 1 :
                    self.exp1.project( rmin+1, lmax   )
                    self.exp2.project( rmin  , lmax-1 )
                if max == 0 :
                    self.exp1.project( lmin, rmax )
                    self.exp2.project( lmin, rmax )

            case "<=" :
                self.exp1.project( lmin, rmax )
                self.exp2.project( lmin, rmax )
            case ">=" :
                self.exp1.project( rmin, lmax )
                self.exp2.project( rmin, lmax )

            case "+" :
                self.exp1.project( nmin-rmax , nmax-rmin )
                self.exp2.project( nmin-lmax , nmax-lmin )
            case "-" :
                self.exp1.project( nmin+rmin , nmax+rmax )
                self.exp2.project( lmin-nmax , lmax-nmin )
            case "*" :
                if rmin == 0 : rmin = 1
                if rmax == 0 : rmax = 1
                
                [lmin,lmax] = [
                    min(nmin//rmin, nmin//rmax, nmax//rmin, nmax//rmax),
                    max(math.ceil(nmin/rmin), math.ceil(nmin*rmax), 
                        math.ceil(nmax*rmin), math.ceil(nmax*rmax))
                ]
                self.exp1.project(lmin, lmax)

                if lmin == 0 : lmin = 1
                if lmax == 0 : lmax = 1

                [rmin,rmax] = [
                    min(nmin//lmin, nmin//lmax, nmax//lmin, nmax//lmax),
                    max(math.ceil(nmin/lmin), math.ceil(nmin*lmax), 
                        math.ceil(nmax*lmin), math.ceil(nmax*lmax))
                ]
                self.exp2.project(rmin, rmax)

#====================================================================

class Constraint :
    def __init__(self, exp) -> None:
        self.exp = exp
        self.reif = IntVar("_",0,1)

    def __str__(self) -> str:
        return str(self.exp)
    
    def prune(self) :
        [min, max] = self.exp.evaluate()
        self.exp.project(min,max)
        self.reif.project(min,max)

    def getReif(self,name) :
        self.reif.name = name
        return self.reif

#====================================================================

x   = IntVar('x', 1,3)
y   = IntVar('y', 1,3)
z   = IntVar('z', 1,3)
ux  = IntVar('ux', 0,1)
uy  = IntVar('uy', 0,1)
uz  = IntVar('uz', 0,1)

gx  = Constraint(x == y*z)
gy  = Constraint(y == x*z)
gz  = Constraint(x*y <= z)

rx   = gx.getReif("rx")
ry   = gy.getReif("ry")
rz   = gz.getReif("rz")

i1  = SearchInstance(
        [x,y,z,ux,uy,uz],
        [
            Constraint(ux==rx), Constraint(uy==ry), Constraint(uz==rz),
            # gx,gy,gz
        ]
    )

i2 = copy.deepcopy(i1)

i1.propagate()

#====================================================================

