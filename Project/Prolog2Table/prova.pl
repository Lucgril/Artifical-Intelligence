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
prefers(john, susie).
likes(X, susie).
likes(john, Y).
likes(john, francy).
not(likes(john, pizza)).
not(prefers(pippo, lasagna)).
not(likes(luca, pasta)).
not(prefers(francesco, pizza)).
likes(andrea, matriciana).
colored(X) :- blue(X).
colored(X) :- red(X).
parent(X,Y) :- father(X,Y).
parent(X,Y) :- mother(X,Y).
hates(X,Y) :- not(likes(X,Y)).
