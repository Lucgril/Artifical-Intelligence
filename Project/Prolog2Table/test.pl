blue(sky).
red(fire).
father(jack, susan).
father(jack, ray).
father(david, liza).
father(david, john).
father(john, peter).
father(john, mary).
mother(karen, susan).
mother(karen, ray).
mother(amy, liza).
mother(amy, john).
mother(susan, peter).
mother(susan, mary).

likes(john, susie).
likes(X, susie).
likes(john, Y).
prefers(john, susie); likes(john, francy).
not(likes(john, pizza)).
not(prefers(pippo, lasagna)); not(likes(luca, pasta)).
not(prefers(francesco, pizza)); likes(andrea, matriciana).


hates(X,Y) :- not(likes(X,Y)).
enemies(X,Y) :- not(likes(X,Y)),not(likes(Y,X)).
parent(X, Y) :- father(X,Y).
parent(X,Y) :- mother(X,Y).
grandfather(X,Y) :- father(X,Z), parent(Z,Y).
grandmother(X,Y) :- mother(X,Z), parent(Z,Y).
mama(X,Y) :- mother(X,Z), father(Z,Y).
colored(X) :- red(X).
colored(X) :- blue(X).

