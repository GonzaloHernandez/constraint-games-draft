% Use this editor as a MiniZinc scratch book

enum P = {X,Y,Z};
array [P] of set of int: D = [1..3, 1..3, 1..5];
array [P] of var int : V;

constraint
  forall(p in P)(
    V[p] in D[p]);

% ----- creating payoff matrix --------------------------------
% array [P, D[X], D[Y], D[Z]] of int: payoffs 
%   = array4d(P, D[X], D[Y], D[Z], [if     p=X then x * z
%                                   elseif p=Y then x + z - y
%                                   else            x + y - z
%                                   endif 
%                                  |p in P, x in D[X], y in D[Y], z in D[Z]] );

% solve maximize  payoffs[X, V[X], V[Y], V[Z]] + 
%                 payoffs[Y, V[X], V[Y], V[Z]] + 
%                 payoffs[Z, V[X], V[Y], V[Z]];

var int : x = V[X];
var int : y = V[Y];
var int : z = V[Z];

array [P] of var bool : G = [
  x = y + z,          % = G[X]
  x >= z /\ z > y,    % = G[Y]
  x = y /\ y = z ];   % = G[Z]

constraint
  G[X] \/ G[Y] \/ G[Z];

array [P] of var int : E = [
  x * z,        % = a
  x + z - y,    % = b
  x + y - z ];  % = c

solve maximize sum(E) + sum(G);

% ----- printing payoff matrix --------------------------------
% output [
%   "Payoffs: \(payoffs)\n"];

output [
  "V: \(V)    G: \(G)    E: \(E)"];
 