enum P = {A, B};
array [P] of set of int : D = [1..2, 1..4];
array [P] of var int : V;

constraint
  forall(p in P)(
    V[p] in D[p]);

array [1..card(D[A])*card(D[B])] of int : GA = [2,4,3,7,8,1,6,5];
array [1..card(D[A])*card(D[B])] of int : GB = [1,3,5,7,2,4,8,9];

array [1..card(D[A])*card(D[B])] of string : AxB = ["a\(a) b\(b) " | a in D[A], b in D[B]];

output [
  "\(AxB[i]) \(GA[i])  \(GB[i])\n" | i in 1..card(D[A])*card(D[B])];