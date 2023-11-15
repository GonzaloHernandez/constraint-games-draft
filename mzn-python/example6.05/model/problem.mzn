enum P = {X,Y,Z};
set of int : Dx = 1..9;
set of int : Dy = 1..9;
set of int : Dz = 1..3;
array [P] of var int    : S;
array [P] of var bool   : U;

%---------------------------------------------

var int : x = S[X];
var int : y = S[Y];
var int : z = S[Z];

constraint
    x in Dx /\
    y in Dy /\
    z in Dz;

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
