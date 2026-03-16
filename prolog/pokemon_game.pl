:-ensure_loaded("pokemon_list.pl").
:-ensure_loaded("pokemon_info_attacks.pl").
:-ensure_loaded("pokemon_route.pl").

player_starts(0,0).
next_rooms(X,Y,L) :-
    route(M),
    size(M,N),
    X1 is X+1,
    X2 is X-1,
    Y1 is Y+1,
    Y2 is Y-1,
    rooms_dir(M,N,X1,Y,R1),
    rooms_dir(M,N,X2,Y,R2),
    rooms_dir(M,N,X,Y1,R3),
    rooms_dir(M,N,X,Y2,R4),
    join(R1,R2,T1),
    join(R3,R4,T2),
    join(T1,T2,L).

next_rooms(_,_,[]).
rooms_dir(M,N,X,Y,[]) :-
    X < 0.
rooms_dir(M,N,X,Y,[]) :-
    Y < 0.
rooms_dir(M,N,X,Y,[]) :-
    X >= N.
rooms_dir(M,N,X,Y,[]) :-
    Y >= N.

rooms_dir(M,N,X,Y,[[Id,Name,Level,X,Y,Types]]) :-
    nth0(X,M,Row),
    nth0(Y,Row,(Id,Level)),
    Id > 0,
    pokemon(Id,Name,Types).
size([],0).
size([_|T],N) :-
    size(T,N1),
    N is N1+1.

join([],L,L).
join([X|T],L,[X|R]) :-
    join(T,L,R).