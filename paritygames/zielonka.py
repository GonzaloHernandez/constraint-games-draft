import os
os.system("clear")

# ============================================================

class Game :
    #-----------------------------------------------------

    def __init__(self) :
                        #0  1  2  3  4  5  6  7
        self.graph =   [[0, 1, 0, 0, 1, 0, 0, 0], # 0
                        [0, 0, 1, 0, 0, 1, 1, 0], # 1
                        [0, 0, 0, 0, 0, 0, 0, 1], # 2
                        [1, 0, 0, 0, 1, 0, 0, 0], # 3
                        [0, 0, 0, 0, 0, 1, 0, 1], # 4
                        [0, 1, 0, 0, 0, 0, 1, 0], # 5
                        [0, 0, 1, 1, 0, 0, 0, 0], # 6
                        [1, 0, 0, 0, 0, 1, 0, 0]] # 7
        
        self.colors=    [4, 2, 7, 9, 3, 6, 1, 8]

        self.owner =    [0, 1, 1, 0, 0, 1, 0, 1]

    #-----------------------------------------------------

    def __init__(self, graph, colors, owner) :
                       
        self.graph  = graph
        self.colors = colors
        self.owner  = owner

    #-----------------------------------------------------

    def print(self) :
        for row in self.graph :
            print(str(row))

    def remove(self, vertices) :
        delta = 0
        for v in vertices :
            self.graph.__delitem__(v - delta)
            for row in self.graph :
                row.__delitem__(v - delta)
            delta += 1

    #-----------------------------------------------------

    def copy(self) :
        newGraph = []
        for row in self.graph :
            newRow = []
            for item in row :
                newRow.append(item)
            newGraph.append(newRow)
        
        newPriorities = []
        for item in self.colors :
            newPriorities.append(item)
        
        newOwner = []
        for item in self.owner :
            newOwner.append(item)

        return Game(newGraph, newPriorities, newOwner)

    #-----------------------------------------------------

    def attractor(self, o, vertices) :
        A = set()
        for v in vertices :
            for r in range(0,self.graph.__len__()) :
                row = self.graph[r]
                if row[v] == 1 : 
                    if self.owner[r]==o :   # any adge :
                        A=A.union({r}) 
                    elif sum(row)==1 :      # all ages :
                        A=A.union({r})
        A=A.union(vertices)
        if A.__len__()==vertices.__len__() :
            return A
        else :
            return self.attractor(o,A)

# ============================================================

def Zielonka(G) :
    G.print()
    print()
  
    W = [[]]
    if G.graph == [] :
        (W[p],W[q]) = (0,0)
    else :
        m = max(G.colors)
        
        p = m % 2
        q = 1 - p

        U = []
        for i in range(0,G.graph.__len__()) :
            if G.colors[i] == m : U.append(i)

        A = G.attractor(p,U)

        W_ = [[]]

        G_ = G.copy()
        G_.remove(A)
        W_ = Zielonka(G_)
        if W_[q] == [] :
            (W[p],W[q]) = (A+W_[p],[])
        else :
            B = G.attractor(q,W_[q])
            G_ = G.copy()
            G_.remove(B)
            W_ = Zielonka(G_)
            (W[p],W[q]) = (W_[p],W_[q]+B)
        return W

# ============================================================

G = Game( 
    [   [0,1,0,1,0,0,0,0],
        [1,0,1,0,0,0,0,0],
        [0,1,0,0,1,0,0,0],
        [0,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,1,0], 
        [0,0,0,1,0,0,0,1],
        [0,0,0,0,1,0,0,0]   ],
    
        [4,1,6,0,8,3,2,5],

        [0,1,0,1,1,0,1,0]
)

W = Zielonka(G)

print(W)
