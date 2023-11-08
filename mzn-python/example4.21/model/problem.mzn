int : n;
int : s;

set of int : P			= 0..n-1;
set of int : S 			= 0..s-1;
set of int : AmountS	= 1..n;

array [P] of var S 			: V;
array [P] of var AmountS	: U;

%----------------------------------------------

constraint
	forall(i in P)(
		U[i]=count(j in P)(
            V[i]=V[j]
        )
    );

%----------------------------------------------

constraint
    V[0] != V[1] /\
    V[2] != V[3] /\
    V[4] !=    0 ;