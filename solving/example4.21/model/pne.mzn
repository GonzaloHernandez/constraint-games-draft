int : n;
int : s;

set of int : P          = 0..n-1;
set of int : S          = 0..s-1;
set of int : AmountS    = 1..n;

array [P] of var S          : V;
array [P] of var AmountS	: U;

%----------------------------------------------

int : l;
set of int : R          = 0..l-1;

array [R,P] of S 		: Ss;
array [R,P] of AmountS	: Us;

var bool                : E;

constraint
    exists(r in R)(
        forall(i in P)(
            Ss[r,i] = V[i] /\ Us[r,i] = U[i]
        )
    );

% include "table.mzn";
% constraint 
%     table(
%         V ++ U,
%         [(r, i): X[i] | 
%             r in R, X = Ss[r,..] ++ Us[r, ..], 
%             i in index_set(V++U)]
%     );

%----------------------------------------------

constraint
    E = true;

constraint
    E <-> not exists(p in P)(
        exists(r in R)(
            Us[r,p] > U[p]
            /\
            forall(i in P where i != p)(
                Ss[r,i] = V[i]
            )
        )
    );

% constraint 
%     E <-> forall(p in P) (
%         forall(r in R)(
%             Us[r,p] <= U[p]
%             \/
%             not forall(i in P where i != p)(
%                 Ss[r,i] = V[i]
%             )
%         )
%     );