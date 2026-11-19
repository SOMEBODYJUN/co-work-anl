"""Exact check of the three-movers minimax obstruction embedded in six movers."""
from fractions import Fraction
from itertools import product

N = 6
LABELS = tuple(range(7))
EMPTY = 6
CLIENTS = tuple((a,b) for a in range(N) for b in range(a+1,N)
                if (a-b) % N not in (1,5))
SETS = tuple(frozenset(e for e in CLIENTS if a in e) for a in LABELS)


def pay(actions, i):
    return sum((Fraction(1, sum(x in SETS[a] for a in actions))
                for x in SETS[actions[i]]), Fraction(0))


def last(a,b):
    if a == EMPTY or b == EMPTY:
        return max(LABELS, key=lambda c: pay((a,b,c),2))
    if a == b:
        return (a+1) % N
    if (b-a) % N in (1,5):
        return (2*a-b) % N
    if (b-a) % N == 3:
        return (b+1) % N
    # The second player's label already intersects a. This choice can use
    # any maximizing reply, charged second-player payoff is already <=5/2.
    return max(LABELS, key=lambda c: pay((a,b,c),2))


def second(a):
    if a != EMPTY:
        return (a+3) % N
    return max(LABELS, key=lambda b: pay((a,b,last(a,b)),1))


def main():
    rows=[]
    for a in LABELS:
        b=second(a)
        c=last(a,b)
        for alt in LABELS:
            assert pay((a,b,c),1) >= pay((a,alt,last(a,alt)),1)
        rows.append((a,b,c,str(pay((a,b,c),0))))
        for t in LABELS:
            for alt in LABELS:
                assert pay((a,t,last(a,t)),2) >= pay((a,t,alt),2)
    assert all(pay((0,second(0),last(0,second(0))),0) >=
               pay((a,second(a),last(a,second(a))),0) for a in LABELS)
    table=[(max(pay((a,b,c),2) for c in LABELS),a,b) for a,b in product(LABELS,repeat=2)]
    minima=min(table)
    assert minima[0] == Fraction(5,2)
    assert pay((0,3,4),0)==2
    assert sum(pay((0,3,4),i) for i in range(3))==len(set().union(SETS[0],SETS[3],SETS[4]))==7
    # Compare the whole three-move ordered support using independent
    # backward recursion. Prior empty labels make payoffs identical.
    def support(h):
        i=len(h)
        if i==3:
            return (h,)
        child=[support(h+(a,)) for a in LABELS]
        return tuple(s for a,br in enumerate(child) for s in br
                     if all(any(pay(t,i)<=pay(s,i) for t in cb)
                            for t_a,cb in enumerate(child) if t_a!=a))
    roots=support(())
    assert (0,3,4) in roots
    print('customers',CLIENTS,'action_sets',SETS)
    print('selected_action_outcomes',rows)
    print('minimax and first minimizer',minima)
    print('ordered_SPE_tail_outcomes',len(roots),'minimum_first_pay',min(pay(s,0) for s in roots))
    print('tail outcome utilities',tuple(str(pay((0,3,4),i)) for i in range(3)))
    print('all last-node, second-node, first-node alternatives checked; all 49 ordered blocker pairs checked')

if __name__=='__main__':
    main()
