import os
os.system("clear")

# ============================================================

class Game :

    #-----------------------------------------------------

    def __init__(self, graph, colors, owner, ids=None) :
        self.graph  = graph
        self.colors = colors
        self.owner  = owner
        self.ids    = list(range(self.graph.__len__())) if ids==None else ids

    #-----------------------------------------------------

    def print(self) :
        for row in self.graph :
            print(str(row))

    def remove(self, vertices) :
        for v in vertices :
            for c in range(self.graph.__len__()) :
                if self.ids[c]==v : break
            self.graph.__delitem__(c)
            for row in self.graph :
                row.__delitem__(c)
            self.colors.__delitem__(c)
            self.owner.__delitem__(c)
            self.ids.__delitem__(c)

    #-----------------------------------------------------

    def copy(self) :
        newGraph = []
        for row in self.graph :
            newRow = []
            for item in row :
                newRow.append(item)
            newGraph.append(newRow)
        
        newColors = []
        newOwner = []
        newIds = []
        for i in range(0,self.graph.__len__()) :
            newColors.append(self.colors[i])
            newOwner.append(self.owner[i])
            newIds.append(self.ids[i])
        
        return Game(newGraph, newColors, newOwner, newIds)

    #-----------------------------------------------------

    def attractor(self, o, vertices) :
        A = set()
        for v in vertices :
            for c in range(self.graph.__len__()) :
                if self.ids[c]==v : break

            for r in range(self.graph.__len__()) :
                row = self.graph[r]
                if row[c] == 1 :
                    if self.owner[r]==o :   # any adge :
                        A=A.union({self.ids[r]}) 
                    elif sum(row)==1 :      # all ages :
                        A=A.union({self.ids[r]})

        A=A.union(vertices)
        if A.__len__()==vertices.__len__() :
            return A
        else :
            return self.attractor(o,A)

# ============================================================

def Zielonka(G) :
    # G.print()
    # print()
  
    W = [[],[]]
    if G.graph == [] :
        (W[0],W[1]) = (0,0)
    else :
        m = max(G.colors)
        
        p = m % 2
        q = 1 - p

        U = []
        for i in range(0,G.graph.__len__()) :
            if G.colors[i] == m : U.append(G.ids[i])

        A = G.attractor(p,U)

        # W_ = [[],[]]

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
            (W[0],W[1]) = (W_[p],W_[q]+B)
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
