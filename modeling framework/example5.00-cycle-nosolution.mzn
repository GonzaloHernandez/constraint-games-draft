enum P = {X,Y};
set of int : D = 1..2;
array [P] of var D : V;
array [P] of var bool : U;

var int : x = V[X];
var int : y = V[Y];

constraint
	U[X] = (x > y);
	
constraint
	U[Y] = (y > x);
	
constraint
	x != y;

output [
	show(V) ++ "    " ++ 
	show(U)];