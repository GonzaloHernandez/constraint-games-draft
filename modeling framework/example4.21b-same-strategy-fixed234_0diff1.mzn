int : n=5;
int : s=5;

set of int : P				= 0..n-1;
set of int : S 			= 0..s-1;
set of int : AmountS	= 1..s;

array [P] of var S 				: V;
array [P] of var AmountS	: p;

constraint
	forall(i in P)(
		p[i]=count(j in P)(V[i]=V[j]));

constraint
	V[0] != V[1] /\
	V[2] = 2 /\
	V[3] = 3 /\
	V[4] = 4;

var int : t = sum(p);

output ["\(2,t)     " ++
	show(p) ++ "                       " ++ 
	show(V) ++ "\n"
	]