% Use this editor as a MiniZinc scratch book

enum P = {X, Y, Z};
array [P] of set of int : D = [1..3, 1..3, 1..3];
array [P] of var int : V;

constraint
  forall(p in P)(
    V[p] in D[p]);

var int : x = V[X];
var int : y = V[Y];
var int : z = V[Z];

var bool : GX = x = y + z;
var bool : GY = x >= z /\ z > y;
var bool : GZ = x = y /\ y = z;

% constraint
%   x=1 /\ y=2 /\ z=3;

constraint
  GX \/ GY \/ GZ;

solve maximize GX + GY + GZ;    % More goals

constraint
  x <= y /\ y <= z;

output [
  "V: \(V) : (\(GX),\(GY),\(GZ))"];
