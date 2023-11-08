% In this game, all players guess a number in a range from 0 to 100. The winners are the players whose number is the closest to two thirds of the average of the numbers guessed by all players. Let m be the number of winners, then all these players with get a score of 100/m. All others get a score of zero.

int : n = 5;

set of int : P = 1..n;
set of int : D = 0..100;
array [P] of D : V = [30,45,60,70,80];

int : TTA = round((2/3)*(sum(V)/n));
array [P] of int : Y = [ abs(V[p] - TTA) | p in P];
int : Z = min(Y);
array [P] of var bool : C;
array [P] of var int : Q;

constraint
  forall(p in P)(
    C[p] = 1 <-> Y[p]=Z);

constraint
  forall(p in P)(
    C[p] = 1 -> Q[p] = round(100/(sum(C))));
    
constraint
  forall(p in P)(
    C[p] = 0 -> Q[p] = 0);

solve maximize sum(Q);
                        
output [
  "V =   \(V) \n" ++
  "TTA = \(TTA) \n" ++
  "Y =   \(Y) \n" ++
  "Z =   \(Z) \n" ++
  "C =   \(C) \n" ++
  "Q =   \(Q)"  
  ];
  
  
  
  