import os
os.system("clear")

# -------------------------------------------------

class IntVar :
    def __init__(self, name, min, max) -> None:
        self.name   = name
        self.min    = min
        self.max    = max

    def __str__(self) -> str:
        if self.isFailed() :
            return f"{self.name}[]"
        elif self.isAssigned() :
            return f"{self.name}[{str(self.min)}]"
        else :
            return f"{self.name}[{str(self.min)}..{str(self.max)}]"
    
    def isAssigned(self) :
        return (self.min==self.max)
    
    def isFailed(self) :
        return (self.min>self.max)
    
    def __eq__(self, __value: object) -> bool:
        pass
    

# -------------------------------------------------

class Instance :
    def __init__(self, vars) -> None:
        self.vars = vars
    

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


def propagate(vars) :
    for v in vars :
        if v.isFailed() :
            return None
        
    assigned = True
    for v in vars :
        if not v.isAssigned() :
            assigned = False
    
    if assigned :
        print(vars)
        return vars
    else :
        for i,v in enumerate(vars) :
            if not v.isAssigned():
                v1 = IntVar(v.name, v.min, v.max)
                v2 = IntVar(v.name, v.min+1, v.max)
                vars1 = vars
                vars2 = vars
                vars1[i],vars2[i] = v1,v2
                assigned = propagate(vars1)
                if not assigned :
                    assigned = propagate(vars2)
                    

# -------------------------------------------------

vs  = Solver([
        IntVar('s1',1,3),
        IntVar('s2',1,3),
        IntVar('s3',1,3),
        IntVar('u1',0,1),
        IntVar('u2',0,1),
        IntVar('u3',0,1)
        ])

vs.propagate()
# -------------------------------------------------


