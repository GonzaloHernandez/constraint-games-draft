int : n = 4;
int : a = 15;
int : b = 8;
int : c = 7;
set of int : P = 1..n;
set of int : A = 10..30;	% strategy set (set of efforts?)
array [P] of var A : V;		% player's effort
var int : M;							% minimum effort
array [P] of var int : p;	% payoff

constraint
	M = min(A);

constraint
	forall(i in P)(
		p[i] = a + b * M - c * V[i] );

solve maximize sum(p);

% I don't understand what is the purpose of this game. Always the best option is the first one.