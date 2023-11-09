import os
os.system("clear")

class Value :
    def __init__(self, value) -> None:
        self.value = value
    
    def __add__(self, other) :
        return self.value + other.value

    def __add__(self, other) :
        return Expression(self.value,'+',other)

class Expression :
    def __init__(self,exp1,oper,exp2) -> None:
        self.exp1 = exp1
        self.oper = oper
        self.exp2 = exp2

    def __init__(self,exp1) -> None:
        self.exp1 = exp1
        self.oper = None
        self.exp2 = None

 
a = Value(3)
b = Value(5)
c = 8 * a + 4
print(c)