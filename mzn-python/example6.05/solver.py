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
            return f"{self.name}({str(self.min)})"
        else :
            return f"{self.name}({str(self.min)}..{str(self.max)})"
    
    def isAssigned(self) :
        return (self.min==self.max)
    
    def isFailed(self) :
        return (self.min>self.max)
    
# -------------------------------------------------

class Solver :
    def __init__(self, vars) -> None:
        self.vars = vars
    
    def __str__(self) -> str:
        text = "["
        for v in self.vars :
            text += str(v) + " "
        return text+"]"

    def propagate(self) :
        propagate(self.vars)

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

vs  = Solver([
        IntVar('s1',5,7),
        IntVar('s2',5,7),
        IntVar('u1',0,1),
        IntVar('u2',0,1),
        ])

vs.propagate()

# -------------------------------------------------


