int	: n = 3;
int	: m = 14;

set of int : P = 1..n;
set of int : L = 1..m;

array [P] of var L	: l;
array [P] of var 2..4	: p;

include "globals.mzn";

% no two vendors are located at the same place: all different(l1,l2,...,ln)
constraint
  all_different(l);
  
% ∀i ∈ P,∀c ∈ [1..m], costic = |c−li|+ pi
array [P,L] of var int : cost;
constraint
  forall(i in P,c in L)(
    cost[i,c] = abs(c-l[i])+ p[i]);

% ∀c ∈ [1..m], minc = min(cost1c,...,costnc)
array [L] of var int : mi;
constraint
  forall(c in L)(
    mi[c] = min(i in P)(cost[i,c]));
    
% ∀c ∈ [1..m],(minc =costic) ← (choiceic = 1)
array [P,L] of var bool : choice;
constraint
  forall(c in L)(
    forall(i in P)(
      mi[c]=cost[i,c] <- choice[i,c]=1));

% ∀c ∈ [1..m],∑i∈Pchoiceic = 1
constraint
  forall(c in L)(
    sum(i in P)(choice[i,c])=1);

% ∀i ∈ P, Gi contains the following constraint: benefiti = pi.∑mc=1choiceic
array [P] of var int : benefit;
constraint
  forall(i in P)(
    benefit[i]=p[i]*sum(c in L)(choice[i,c]));


% ∀i ∈ P, the optimization condition opti = max(benefiti)
var float : av = sum(benefit) / card(P);
array [P] of var float : dispersion;
constraint
  forall(i in P)(
    dispersion[i] = abs(int2float(benefit[i])-av));

% solve minimize sum(benefit);
solve minimize sum(dispersion);

% constraint
%   l = [4,5,1];		% testing values

% ------------------------------------------------------------------------

output [
  "\ncost       " ];
  
output [
  "\(2,cost[i,c])" ++ if c<m then " " else "\n           " endif | i in P, c in L ]; 

output [
  "\nmins       " ];
  
output [
  "\(2,mi[c]) " | c in L];

output [
  "\n\nchoice      " ];
  
output [
  "\(bool2int(choice[i,c])) " ++ if c<m then " " else "\n            " endif 
  | i in P, c in L ];

output [
  "\np           " ];
  
output [
  "\(2,p[i]) " | i in P];
  
output [
  "\nl           " ];
  
output [
  "\(2,l[i]) " | i in P];
  
output [
  "\n\nbenefit     " ];

output [
  "\(2,benefit[i]) " | i in P];

output [
  "\n\naverage     " ];
  
output [
  "\(av)"];

output [
  "\n\ndispersion  " ];

output [
  "\(2,dispersion[i]) " | i in P];

output [
  "\(sum(dispersion))"];

%-------------------------------------------------------------------------

% How do you keep everyone happy?  
% What should be optimization formula?
% Can we play with the price too?




