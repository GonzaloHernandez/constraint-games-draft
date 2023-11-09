int : l;

set of int : P = 1..3;
set of int : S = 1..3;      % D
set of int : R = 1..l;

array[R,P]  of S    : Vs;
array[R,P]  of bool : Us;

array[P]  of var S     : V;
array[P]  of var bool  : U;
var bool  : E;

constraint
    exists(r in R)(
        forall(i in P)(
            Vs[r,i] = V[i] /\ Us[r,i] = U[i]
        )
    );

constraint
    E = true;
    
constraint
    E <-> not exists(p in P)(
        exists(r in R)(
            Us[r,p] > U[p]
            /\
            forall(i in P where i != p)(
                Vs[r,i] = V[i]
            )
        )
    );

