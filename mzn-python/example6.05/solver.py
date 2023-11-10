import os, copy
os.system("clear")

# -------------------------------------------------

class IntVar :
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
    
    def isAssigned(self) :
        return (self.min==self.max)
    
    def isFailed(self) :
        return (self.min>self.max)
    
    def __eq__(self, exp) :
        return Expression(self,"=",exp)

    def __add__(self, exp) :
        return Expression(self,"+",exp)

    def __sub__(self, exp) :
        return Expression(self,"-",exp)

    def __mul__(self, exp) :
        return Expression(self,"*",exp)

    def __mul__(self, exp) :
        return Expression(self,"*",exp)

    def __and__(self, exp) :
        return Expression(self,"&",exp)

    def __or__(self, exp) :
        return Expression(self,"|",exp)


# -------------------------------------------------

class Solver :
    def __init__(self, vars, cons) -> None:
        self.vars = vars
        self.cons = cons
    
    def __str__(self) -> str:
        text = "["
        for v in self.vars :
            text += str(v) + " "
        return text+"]"

    def propagate(self) :
        propagate(self.vars)

# -------------------------------------------------

class Expression :
    def __init__(self, exp1, oper, exp2) -> None:
        self.exp1 = exp1
        self.oper = oper
        self.exp2 = exp2

    def __str__(self) -> str:
        if self.oper is None :
            return str(self.exp1)
        else :
            return "("+str(self.exp1) + self.oper + str(self.exp2)+")"

    def __eq__(self, exp) :
        return Expression(self,"=",exp)

    def __add__(self, exp) :
        return Expression(self,"+",exp)

    def __sub__(self, exp) :
        return Expression(self,"-",exp)

    def __mul__(self, exp) :
        return Expression(self,"*",exp)

    def __mul__(self, exp) :
        return Expression(self,"*",exp)

    def __and__(self, exp) :
        return Expression(self,"&",exp)

    def __or__(self, exp) :
        return Expression(self,"|",exp)

# -------------------------------------------------

class Constraint :
    def __init__(self, exp) -> None:
        self.exp = exp

    def __str__(self) -> str:
        return str(self.exp)

# -------------------------------------------------

def printlist(ls) :
    print("[ ",end="")
    for l in ls : print(l,end=" ")
    print("]")

# -------------------------------------------------

def propagate(vars) :
    for v in vars :
        if v.isFailed() :
            return None
    
    for v in vars :
        if v.prune() :
            return None

    assigned = True
    for v in vars :
        if not v.isAssigned() :
            assigned = False
    
    if assigned :
        printlist(vars)
        return vars
    else :
        for i,v in enumerate(vars) :
            if not v.isAssigned():
                v1 = IntVar(v.name, v.min, v.min)
                v2 = IntVar(v.name, v.min+1, v.max)
                vars1 = copy.deepcopy(vars)
                vars2 = copy.deepcopy(vars)
                vars1[i],vars2[i] = v1,v2
                
                assigned = propagate(vars1)
                assigned = propagate(vars2)
                break
                    
# -------------------------------------------------

x = IntVar('x',1,3)
y = IntVar('y',1,3)
z = IntVar('z',1,3)
ux = IntVar('ux',0,1)
uy = IntVar('uy',0,1)
uz = IntVar('uz',0,1)


vs  = Solver([x,y,z,ux,uy,uz],
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
                ((x+1)*(y+1) != 3*z) 
            )
        ])

# vs.propagate()

# -------------------------------------------------
c = Constraint( ux == (x == (y*z)) )
print(c)
