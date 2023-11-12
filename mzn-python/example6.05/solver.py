import os, copy
os.system("clear")

# -------------------------------------------------

def printlist(ls) :
    print("[ ",end="")
    for l in ls : print(l,end=" ")
    print("]")

# -------------------------------------------------

class Operable :
    def __add__(self, exp) :
        return Expression(self,"+",exp)

    def __sub__(self, exp) :
        return Expression(self,"-",exp)

    def __mul__(self, exp) :
        return Expression(self,"*",exp)

    def __mul__(self, exp) :
        return Expression(self,"*",exp)

    def __eq__(self, exp) :
        return Expression(self,"=",exp)

    def __ne__(self, exp) :
        return Expression(self,"!=",exp)

    def __lt__(self, exp) :
        return Expression(self,"<",exp)

    def __le__(self, exp) :
        return Expression(self,"<=",exp)

    def __gt__(self, exp) :
        return Expression(self,">",exp)

    def __ge__(self, exp) :
        return Expression(self,">=",exp)

    def __and__(self, exp) :
        return Expression(self,"&",exp)

    def __or__(self, exp) :
        return Expression(self,"|",exp)

# -------------------------------------------------

class IntVar (Operable) :
    def __init__(self, name, min, max) -> None:
        self.name   = name
        self.min    = min
        self.max    = max

    def __str__(self) -> str:
        if self.isFailed() :
            return f"{self.name}()"
        elif self.isAssigned() :
            return f"{self.name}{{{str(self.min)}}}"
        else :
            return f"{self.name}{{{str(self.min)}..{str(self.max)}}}"
    
    def setge(self, val) :
        self.min = val

    def setle(self, val) :
        self.max = val

    def isAssigned(self) :
        return (self.min==self.max)
    
    def isFailed(self) :
        return (self.min>self.max)

# -------------------------------------------------

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

    def evaluate(self) :
        if  isinstance(self.exp1, int) :
            self.range = [self.exp1,self.exp1]

        if  isinstance(self.exp1, IntVar) :
            self.range = [self.exp1.min,self.exp1.max]
        
        [lmin,lmax] = self.exp1.evaluate()
        [rmin,rmax] = self.exp2.evaluate()

        match self.oper :
            case "+" :
                self.range = [lmin+rmin , lmax+rmax]
            case "-" :
                self.range = [lmin-rmax , lmax-rmin]
            case "*" :
                self.range = [lmin*rmin , lmax*rmax]
            case "==" :
                self.range = [0 , 1]

        return self.range

    def project(self, range) :
        [newmin,newmax] = range

        if  isinstance(self.exp1, int) :
            pass

        if  isinstance(self.exp1, IntVar) :
            self.exp1.setge(newmin)
            self.exp1.setle(newmax)
            return

        [prewin,premax] = self.range

        match self.oper :
            case "+" :
                pass
            case "-" :
                pass
            case "*" :
                pass
            case "==" :
                pass

        pass
    
# -------------------------------------------------

class SearchInstance :
    def __init__(self, vars, cons) -> None:
        self.vars = vars
        self.cons = cons
    
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

# -------------------------------------------------

class Constraint :
    def __init__(self, exp) -> None:
        self.exp = exp

    def __str__(self) -> str:
        return str(self.exp)
    
    def prune(self) :
        [min,max] = self.exp.evaluate()
        self.exp.project( [min,max] )

# -------------------------------------------------

x = IntVar('x',1,3)
y = IntVar('y',1,3)
z = IntVar('z',1,3)
ux = IntVar('ux',0,1)
uy = IntVar('uy',0,1)
uz = IntVar('uz',0,1)

i1  = SearchInstance(
        [x,y,z,ux,uy,uz],
        [
            Constraint(
                ux == (x == (y*z)) 
            ),
            Constraint( 
                uy == (y == (x*z)) 
            ),
            Constraint(
                (x*y <= z & z <= x+y) 
                &
                ((x+1)*(y+1) != z*3) 
            )
        ])

i2 = copy.deepcopy(i1)

i1.propagate()

# -------------------------------------------------

