from collections import Counter
from fractions import Fraction as F
from functools import cache
from itertools import combinations, product
from math import comb
import json


def verify(m):
    labels = tuple(range(m + 1))
    s = F(2, m)
    d = F(m-2, m * (m-1))

    @cache
    def moment(S):
        assert len(S) <= m
        return 1 + d * (len(S) - 1) if 0 in S else s * len(S)

    for n in range(m):
        for xs in combinations(labels, n):
            S = frozenset(xs)
            for a in set(labels) - S:
                assert moment(S | {a}) >= moment(S)
            if n+2 <= m:
                for a, b in combinations(set(labels) - S, 2):
                    assert moment(S | {a}) + moment(S | {b}) >= moment(S) + moment(S | {a, b})

    @cache
    def utility(sorted_terminal, a):
        others = list(sorted_terminal)
        others.remove(a)
        result = F(0)
        for size in range(m):
            for ids in combinations(range(m-1), size):
                before = frozenset(others[i] for i in ids)
                result += (moment(before | {a}) - moment(before)) / (m * comb(m-1, size))
        return result

    def terminal(h):
        return tuple(sorted(h + (0,) * (m - len(h))))

    path = terminal(())
    K = max(moment(frozenset({a})) for a in labels)
    W = moment(frozenset(path))
    optimum = max(moment(frozenset(xs)) for n in range(m+1) for xs in combinations(labels, n))
    root = utility(path, 0)
    assert W == K == 1 and optimum == 2 and root == F(1,m)
    slacks = Counter()
    for depth in range(m):
        for h in product(labels, repeat=depth):
            own = utility(terminal(h), 0)
            for a in labels[1:]:
                slacks[own - utility(terminal(h + (a,)), a)] += 1
    assert min(slacks) >= 0
    return {'players':m,'labels':len(labels),'K':K,'W':W,'OPT':optimum,'u':root,
            'histories':sum(len(labels)**d for d in range(m)), 'comparisons':sum(slacks.values()),
            'ties':slacks[0], 'smallest_positive_slack':min(s for s in slacks if s)}


if __name__ == '__main__':
    print(json.dumps([verify(m) for m in (4,5,6,7)], default=str, indent=2))
