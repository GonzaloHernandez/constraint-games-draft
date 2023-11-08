enum P = {X,Y,Z};
set of int : D = 1..3;
array [P] of var D      : S;
array [P] of var bool   : U;

%---------------------------------------------

var int : x = S[X];
var int : y = S[Y];
var int : z = S[Z];

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
