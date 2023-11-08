% Use this editor as a MiniZinc scratch book

enum P = {A,B};
set of int: D = {0,1};
array [P] of var D : V;

% ----- creating payoff matrix --------------------------------
% array [P, D, D] of int: payoffs 
%   = array3d(P, D, D, [if p=A then -x+2*y+1 else 2*x-y+1 endif 
%                             | p in P, x in D, y in D] );

% solve minimize payoffs[A,V[A],V[B]] + payoffs[B,V[A],V[B]];

var int : x = V[A];
var int : y = V[B];

array [P] of var int : E = [
  -x + 2 * y + 1 ,
  2 * x - y + 1 ];

% solve minimize sum(E);

% ----- printing payoff matrix --------------------------------
% output [
%   "Payoffs: \(payoffs)\n"];

output [
  "V: \(V)   Payoff: (\(E))"];
