age(john,32).                
age(agnes,41).                
age(george,72).               
age(ian,2).                  
age(thomas,25). 

maturity(X) :-  age(X,Y), Y>18.


likes(dick,mercedes). 
likes(dick,wine). 
likes(ed,wine). 
likes(wife(ed),wine).

likes(dick,X):-likes(X,wine).


loves(mary,computers).

right_for(X,joe) :- loves(X,computers).
loves(X,Y) :- right_for(X,Y).