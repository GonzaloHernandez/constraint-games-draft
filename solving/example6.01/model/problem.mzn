set of int : B = 0..1; % Boolean {false,true}
set of int : P = 1..3;
set of int : D = 1..3;
array [P] of var D : V;
array [P] of var B : U;

var int : x = V[1];
var int : y = V[2];
var int : z = V[3];

% -------- Goals ---------------------

constraint
	U[1] = (
        y <= z /\ x >= z
    );
	
constraint
	U[2] = (
        x <= y /\ y >= z
    );
	
constraint
	U[3] = (
        x + y = z
    );

% -------- Hard Constraints ----------

constraint
	x != (y+z);
