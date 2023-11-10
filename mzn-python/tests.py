import os,copy
os.system("clear")

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

vs = [  IntVar('s1',1,3),
        IntVar('s2',1,3),
        IntVar('s3',1,3),
        IntVar('u1',0,1),
        IntVar('u2',0,1),
        IntVar('u3',0,1)
    ]

vt = copy.deepcopy(vs)

for i,v in enumerate(vs) :
    if i == 2 :
        v.min = 2

for v in vt :
    print(v)