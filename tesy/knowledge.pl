parent(alice, bob).
parent(bob, charlie).
parent(charlie, dave).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).