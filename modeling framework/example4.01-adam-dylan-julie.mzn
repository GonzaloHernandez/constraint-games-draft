% Use this editor as a MiniZinc scratch book

% Adam, Dylan and Julie are invited to a party. Adam wants to accept the invitation. So does Dylan, but he will go if and only if Adam does go too. For Julie, she wants to go with Dylan but without Adam.

enum P = {Adam, Dylan, Julie};
set of bool: D = {false,true};  % not in use
array [P] of var bool : V;      % bool = D

var bool : x1 = V[Adam];
var bool : x2 = V[Dylan];
var bool : x3 = V[Julie];

var bool : G1 = x1;
var bool : G2 = x1 <-> x2;
var bool : G3 = (not x1) /\ x2 /\ x3;

constraint
  G1 \/ G2 \/ G3;

solve maximize G1 + G2 + G3;    % More goals

output [
  "V: \(V)"];