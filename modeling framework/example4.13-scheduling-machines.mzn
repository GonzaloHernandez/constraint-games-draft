set of int : P = 1..3;										% Players
set of int : M = 1..2;										% Machines

array [P] of var int : d = [2,3,1];				% Task cost
array [M] of var int : c = [3,3];					% Machine capacity

%-----------------------------------------------------------------------
% Vi = {mi}, mi is the machine chosen by player i.
% ∀i ∈ P,D(mi) = {1,...,m}
%-----------------------------------------------------------------------
array [P] of var M 	: m;

%-----------------------------------------------------------------------
% (mi = j) ↔ (choicei j = 1)
%-----------------------------------------------------------------------
array [P,M] of var bool : choice;

constraint
	forall(i in P)(
		forall(j in M)(
			(m[i]=j) <-> (choice[i,j]=1) ));

%-----------------------------------------------------------------------
% ∑ j=1,m (choiceij × ∑ k∈P (choicek j ×dk)) ≤ cj
%-----------------------------------------------------------------------
% constraint
% 	forall(j in M)(
% 		sum(i in P)(choice[i,j]*sum(k in P)(choice[k,j]*d[k])) <= c[j] );

constraint
	forall(j in M)(
		sum(k in P)(choice[k,j]*d[k]) <= c[j] );

%-----------------------------------------------------------------------

% constraint
% 	m = [1,2,1];	% Testing a value
	
%=======================================================================
% I think last constraint is wrong: 
% ∑ j=1,m (choicei j × ∑ k∈P (choicek j ×dk)) ≤ cj

