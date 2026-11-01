"""Independent exact reconstruction of the 29-customer ancestor-price witness."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json


def main():
    labels, players = 5, 4
    # Each multiplicity is a number of distinct unit customers.
    rows = ((7,6),(8,4),(16,2),(21,6),(22,5),(26,6))
    root = (0,)*labels
    floors, allowed, exact_floors = {}, {}, {}

    def step(b,a):
        return b[:a]+(b[a]+1,)+b[a+1:]

    @lru_cache(None)
    def payoff(q):
        u = [F(0)]*labels
        for mask,w in rows:
            c = sum(q[a] for a in range(labels) if mask>>a&1)
            if c:
                for a in range(labels):
                    if q[a] and mask>>a&1:
                        u[a] += F(w,c)
        return tuple(u)

    def welfare(q):
        return sum(w for mask,w in rows if any(q[a] and mask>>a&1 for a in range(labels)))

    @lru_cache(None)
    def hi(b):
        if sum(b)==players:
            return frozenset((b,))
        kids = [hi(step(b,a)) for a in range(labels)]
        bound = max(min(payoff(q)[a] for q in kids[a]) for a in range(labels))
        elig = tuple(a for a in range(labels) if max(payoff(q)[a] for q in kids[a])>=bound)
        floors[b], allowed[b] = bound, elig
        return frozenset(q for a in elig for q in kids[a])

    @lru_cache(None)
    def exact(b):
        if sum(b)==players:
            return frozenset((b,))
        kids = [exact(step(b,a)) for a in range(labels)]
        bound = max(min(payoff(q)[a] for q in kids[a]) for a in range(labels))
        exact_floors[b] = bound
        return frozenset(q for a in range(labels) for q in kids[a] if payoff(q)[a]>=bound)

    @lru_cache(None)
    def cost(b):
        if sum(b)==players:
            return F(0)
        return floors[b]+min(cost(step(b,a)) for a in allowed[b])

    hi(root)
    price = {((0,0,0,0,0),0):F(12,5),
             ((0,0,0,0,1),0):F(12,5),
             ((1,0,0,0,0),3):F(24,5),
             ((1,0,0,0,1),3):F(24,5)}
    paths = []

    def enumerate_paths(b, actions, edges):
        if sum(b)==players:
            u = payoff(b)
            value = F(welfare(b))+sum((price.get((state,a),F(0))*(floors[state]-u[a])
                                      for state,a in edges),F(0))
            assert value>=29
            paths.append((actions,b,value))
            return
        for a in allowed[b]:
            enumerate_paths(step(b,a),actions+(a,),edges+((b,a),))

    enumerate_paths(root,(),())
    assert len(paths)==57 and len(hi(root))==7
    assert cost(root)==F(80,3) and min(welfare(q) for q in hi(root))==25
    assert exact(root)==frozenset(((0,0,2,1,1),))
    good_path = (4,3,2,2)
    b = root
    primal = []
    for a in good_path:
        assert a in allowed[b]
        primal.append((b,a))
        b = step(b,a)
    assert welfare(b)==29
    assert all(payoff(b)[a]>=floors[state] for state,a in primal)
    assert min(v for _,_,v in paths)==29
    for state,a in price:
        assert floors[state]==F(20,3)
    report = dict(unit_customer_count=sum(w for _,w in rows), player_count=players,
                  topic_count=labels, HI_paths=len(paths), HI_terminals=len(hi(root)),
                  G_I=str(cost(root)), minimum_HI_welfare=25,
                  certified_price_value=29, optimum=29, true_SPE_terminal=list(next(iter(exact(root)))),
                  primal_path=good_path, all_primal_edge_constraints_pass=True,
                  all_57_dual_path_inequalities_pass=True,
                  status="independent Fraction reconstruction passed",
                  scope="Strict finite improvement of a universally valid root price interface; no general half proof.")
    Path(__file__).with_name('interval_price_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
