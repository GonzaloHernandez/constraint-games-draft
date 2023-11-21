enum P = {X,Y,Z,W};
set of int : B  = 0..1; % Boolean {false,true}
set of int : Dx = 1..9;
set of int : Dy = 1..9;
set of int : Dz = 1..3;
set of int : Dw = 1..3;
array [P] of var int    : S;
array [P] of var B      : U;

%---------------------------------------------

var int : x = S[X];
var int : y = S[Y];
var int : z = S[Z];
var int : w = S[W];

constraint
    x in Dx /\
    y in Dy /\
    z in Dz /\
    w in Dw;

%---------------------------------------------

constraint
    U[X] =  (
        x = y*z
    );

constraint
    U[Y] =  (
        y = x*z
    );

constraint
    U[Z] =  (   
        (x*y <= z /\ z <= x+y) 
        /\
        ((x+1)*(y+1) != 3*z)    
    );

constraint
    U[W] =  (
        x<w
    );


solve :: int_search(S, input_order, indomain_min)
      satisfy;