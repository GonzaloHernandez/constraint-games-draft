int 				: n = 2;
set of int	: P = 1..n;
var int			: y;									% minimum value

array [P] of var bool		: choice;	% is the minimal value? true/false
array [P] of var 1..101	:	p;			% payoffs
set of int 							: D = 2..100;
array [P] of var D			: x;

% y = min(x1,..., xn)
constraint
	y = min(x);

% ∀i ∈ P, choicei = 1 ⇔ xi = y
constraint
	forall(i in P)(
		choice[i] = 1 <-> x[i] = y );

% choicei = 1 → pi = xi + n
constraint
	forall(i in P)(
		choice[i] = 1 -> p[i] = x[i]+n );

% choicei = 0 → pi = xi − n
constraint
	forall(i in P)(
		choice[i] = 0 -> p[i] = x[i]-n );

solve maximize sum(p);

% constraint
% 	x[1] = 50 /\ x[2] = 60;		% testing values

%------------------------------- payoff matrix ----------------------------------
% int : size = 5;
% output [
% 	"\(2,if i<=j then i+2 else i-2 endif),\(2,if j<=i then j+2 else j-2 endif) " ++ 
% 	if j=size then "\n\n" else " " endif | i in D where i<=size, j in D where j<=size ];

