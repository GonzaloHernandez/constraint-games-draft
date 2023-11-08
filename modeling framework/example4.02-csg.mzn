% Use this editor as a MiniZinc scratch book

enum P = {X, Y, Z};
set of int: D = 0..2;
array [P] of var D : V;

var int : x = V[X];
var int : y = V[Y];
var int : z = V[Z];

var bool : GX = x != y /\ x > z;
var bool : GY = x <= y /\ y > z;
var bool : GZ = x + 1 = y + z;

constraint
  GX \/ GY \/ GZ;

solve maximize GX + GY + GZ;    % More goals

output [
  "V: \(V) : (\(GX),\(GY),\(GZ))"];
  