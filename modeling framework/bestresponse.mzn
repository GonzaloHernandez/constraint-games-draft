set of int : LECT = 1..10;
set of int : ROOM = 1..3;
set of int : HOUR = 1..5;

array [LECT] of var HOUR : hour;
array [LECT] of var ROOM : room;
array [HOUR] of var int  : cter;

%---------------------------------------------------------------------
% For channeling purpose
%---------------------------------------------------------------------

array [HOUR,LECT] of var 0..1 : sche;
constraint
   forall(h in HOUR,l in LECT)(
      sche[h,l] = if (hour[l] = h) then 1 else 0 endif
   );

constraint
	forall(l1,l2 in LECT where l1!=l2)(
		(room[l1]*10+hour[l1]) != (room[l2]*10+hour[l2])
	);

constraint
	forall(h in HOUR)(
		cter[h] = count(l in LECT)(
			hour[l] = h
		)
	);

%---------------------------------------------------------------------
% Global preference: 
% Minimize the range of houres allocated or
% Minimize the amount of rooms used
%---------------------------------------------------------------------

% solve minimize (max(hour)-min(hour));
% solve minimize (max(room)-min(room));


%---------------------------------------------------------------------
% Lecturer_8 preference: 
% Maximize the number of other teachers sharing the same free time at 
% the first hour
%---------------------------------------------------------------------

% solve minimize (hour[8]=1) + cter[1];

%---------------------------------------------------------------------
% Lecturer_2 preference:
% Minimize the hour allocated, to teach as early as possible.
%---------------------------------------------------------------------

solve minimize hour[2];


%=====================================================================

output[""
	++ "hour =\(hour)\n" 
	++ "room =\(room)\n"
	] ++ 
	[""
	++ if l = 1 then "\n   \(h) = " else " " endif ++ "\(sche[h,l]) " 
	| h in HOUR,l in LECT
	]