enum P = {X, Y, Z};
array [P] of set of int : D = [0..2, 0..1, 0..2];
array [P] of var int : V;

constraint
  forall(p in P)(
    V[p] in D[p]);

include "globals.mzn";

constraint
  all_different(V);    % Hard Constraint

