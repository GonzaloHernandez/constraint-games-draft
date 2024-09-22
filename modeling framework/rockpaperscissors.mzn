set of int: N  = 1..2;
enum        D  = {'rock    ','paper   ','scissors'};
set of int: DU = -1..1;
array [N] of var D : X;
array [N] of var DU: U;
var D : x1 = X[1];
var D : x2 = X[2];
var DU: u1 = U[1];
var DU: u2 = U[2];
constraint (abs(x1-x2) <= 1) -> (u1 =  (x1-x2))   /\ (u2 = (x2-x1));
constraint (abs(x1-x2)  = 2) -> (u1 = -(x1-x2)/2) /\ (u2 = (x1-x2)/2);

% ------------- Presenting on Enumueration Form ------------------
output ["[ " ++ show(x1)       ++ " " ++ show(x2)       ++ " ]" ++
      "  [ " ++ show_int(2,u1) ++ " " ++ show_int(2,u2) ++ " ]" ]
