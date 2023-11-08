enum P = {X,Y,Z};
set of int : D = 1..3;
array [P] of var D : V;
array [P] of var bool : U;

var int : x = V[X];
var int : y = V[Y];
var int : z = V[Z];

constraint
	U[X] = (y <= z /\ x >= z);
	
constraint
	U[Y] = (x <= y /\ y >= z);
	
constraint
	U[Z] = (x + y = z);

constraint
	x != (y+z); 

output [
	show(V) ++ "    " ++ 
	show(U)];