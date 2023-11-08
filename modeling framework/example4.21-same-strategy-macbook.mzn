% Use this editor as a MiniZinc scratch book
int : n=5;
int : s=5;

set of int : P = 0..n-1;
set of int : S = 0..s-1;

array [P] of var S : V;
array [P] of var S : p;

constraint
	forall(i in P)(
		p[i]=sum(j in P)(V[i]=V[j]));

constraint
% 	V[0] = 0 /\
	V[1] = 1 /\
	V[2] = 2 /\
	V[3] = 3 /\
	V[4] = 4;

% constraint
% 	let { var S : aux; } in
% 	forall(i in P)(
% 		V[i]=aux);

constraint
	forall(i in P)(
		p[i] = max(p[i]));

% solve maximize sum(p);