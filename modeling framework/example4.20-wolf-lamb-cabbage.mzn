int : n = 3;

set of int : P = 1..n;
array [P] of var bool : V;
array [P] of var bool : u;

var bool : W = V[1];
var bool : L = V[2];
var bool : C = V[3];

var bool : uW = u[1];
var bool : uL = u[2];
var bool : uC = u[3];


% constrabool
%   W = true <- L =1;

% constrabool
%   L = true <- (C = 1 /\ W = false);

constraint
	uW <- W /\ L ;

constraint
	uL <- ((not W /\ L /\ C) \/ (W /\ not L));

constraint
	u = [1,1,1];

% solve maximize sum(u);
