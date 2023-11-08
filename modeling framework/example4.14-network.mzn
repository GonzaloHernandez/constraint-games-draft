int : n = 5;
int : m = 3;

set of int : P = 1..n;								% clients
set of int : M = 1..m;								% links to transfer

array [P] of int : d = [5,4,3,8,6];				% data of player
array [M] of int : c = [10,8,9];					% capacity of each channel
array [M] of int : s = [3,4,8];						% time spent of each channel by data unit
array [M] of int : p = [50,40,20];				% price of each channel by data unit
array [P] of int : T = [30,30,30,30,30];	% time other providers

array [P] of var M 				: r;				% link selected by client
array [P,M] of var bool		: choice;		% channeling

array [P] of var int : cost;
array [P] of var int : time;

%-----------------------------------------------------------------------
% (ri = j) ↔ (choicei j = 1)
%-----------------------------------------------------------------------
constraint
	forall(i in P)(
		forall(j in M)(
			(r[i]=j) <-> (choice[i,j]=1) ));

%-----------------------------------------------------------------------
% ∀ j ∈ {1,...,m},∑ni=1 choicei j ×di ≤ cj
%-----------------------------------------------------------------------
constraint
	forall(j in M)(
		sum(i in P)(choice[i,j]*d[i]) <= c[j]);

%-----------------------------------------------------------------------
% costi = ∑mj=1 choicei j ×di ×(pj)
%-----------------------------------------------------------------------
constraint
	forall(i in P)(
		cost[i] = sum(j in M)(choice[i,j]*d[j]*p[j]));

%-----------------------------------------------------------------------
% timei = ∑mj=1 choicei j ×di ×(sj)
%-----------------------------------------------------------------------
constraint
	forall(i in P)(
		time[i] = sum(j in M)(choice[i,j]*d[j]*s[j]));

%-----------------------------------------------------------------------
% timei ≤ ψi
%-----------------------------------------------------------------------
constraint
	forall(i in P)(
		time[i] <= T[i]);

%-----------------------------------------------------------------------
% ∀i ∈ P,opti = min(costi)
%-----------------------------------------------------------------------
solve minimize sum(cost);

%=======================================================================
% I have ignored additional costs and times (αij and βij) becouse these values do not provide important constraints. 
