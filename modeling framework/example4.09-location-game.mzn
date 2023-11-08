% Two vendors sell an identical product in their shops settled at a street of length m. The distances from the shop of the vendors’ shop from the beginning of the street are l1 and l2 (with l1 < l2), respectively. Each vendor i needs to determine the price pi for their product from his finite set ρi in order to maximize his benefit bi . There is exactly one client’s house at each point from 1 to m at the street. Each client will buy the product of the vendor for whom he has to pay the minimal cost of the product price plus transport. We assume that the transport cost unit of each customer j is uj . It may exist that the amounts a client needs to pay to both vendors are the same. In this case, the client will privilege vendor labeled by a smaller number.

set of int : P = 1..2;
set of int : Pi = {100,200,300,400,500};
array [P] of var Pi : V;
int : m = 10;
set of int : street = 1..m;
array [P,street] of var int : cost = array2d(P, street, [ abs(j-p)+V[p] | p in P, j in street ]);
array [P,street] of var bool : choice;

constraint
  forall(j in street)(
    cost[1,j] >= cost[2,j] -> choice[1,j]=1);

constraint
  forall(j in street)(
    cost[1,j] <  cost[2,j] -> choice[2,j]=1);

array [P] of var int : b = [ V[p]*sum(j in street)(choice[p,j]) | p in P];

solve maximize sum(b);

output [
  "cost =   \(cost)   \n" ++
  "choice = \(choice) \n" ];

