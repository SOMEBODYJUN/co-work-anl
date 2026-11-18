"""Exact six-slot verifier of harmonic-strict-r1.md. Ordered decision nodes stay distinct."""
from functools import lru_cache
from fractions import Fraction
from itertools import combinations
import json


LABELS = tuple(range(8))
SLOTS = tuple(range(6))
CUSTOMERS = tuple(combinations(LABELS,2))
COMMON = (None, 3, 4, 4, 5, 5)


def policy(history):
    depth = len(history)
    deviation = next((i for i,a in enumerate(history) if a != i), None)
    if deviation is None:
        return depth
    source = history[deviation]
    if source in SLOTS and source >= deviation:
        omitted = source
    elif deviation > 0:
        omitted = COMMON[deviation]
    else:
        omitted = 5 if source == 6 else 4
    tail = tuple(c for c in SLOTS[deviation:] if c != omitted)
    observed = history[deviation + 1:]
    if observed == tail[:len(observed)]:
        return tail[len(observed)]
    return next(a for a in LABELS if a not in history)


@lru_cache(None)
def payoff(counts, action):
    return sum(60 // (counts[a]+counts[b]) for a,b in CUSTOMERS if action in (a,b))


stats = {"ordered_nodes":0,"comparisons_including_self":0}
root_menus = {}


def check_node(history):
    depth = len(history)
    if depth == 6:
        return tuple(history.count(a) for a in LABELS)
    prescribed = policy(history)
    assert prescribed not in history
    children = [check_node(history+(a,)) for a in LABELS]
    values = [payoff(counts,a) for a,counts in enumerate(children)]
    assert values[prescribed] == max(values)
    if history == SLOTS[:depth]:
        root_menus[depth] = children
    stats["ordered_nodes"] += 1
    stats["comparisons_including_self"] += len(children)
    return children[prescribed]


def main():
    terminal = check_node(())
    assert terminal == (1,1,1,1,1,1,0,0)
    failed = []
    tested = 0
    for x in CUSTOMERS:
        def loads(a):
            return [sum(root_menus[i][a][c] for c in x) for i in SLOTS]
        for a in x:
            own = loads(a)
            h = sum(Fraction(1,c) for c in own)/6
            for b in set(LABELS)-set(x):
                limit = 1+Fraction(sum(loads(b)),6)
                assert h*limit >= 1
                tested += 1
                if Fraction(sum(own),6) > limit:
                    failed.append((x,a,b,str(h),str(limit)))
    assert set(x for x,_,_,_,_ in failed) == {(4,6),(5,7)} and len(failed) == 2
    print(json.dumps({**stats, "terminal_counts":terminal, "customers":len(CUSTOMERS),
                      "W":sum(any(terminal[c] for c in x) for x in CUSTOMERS),
                      "harmonic_pairs":tested,"arithmetic_failures_zero_based":failed,
                      "scale_for_payoffs":60}))


if __name__ == "__main__":
    main()
