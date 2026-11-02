"""Exact implementation checks for the stationary scalar envelope; no SPE claim."""
from fractions import Fraction as F
from itertools import product


def check_pointwise(r, b):
    q = (r - 1) ** 2 // 4
    factor = F(r) + F(q, b + 1)
    for indicator in (0, 1):
        for tail in range(r):
            denominator = b + indicator + tail
            root = F(indicator, denominator) if denominator else F(0)
            total = F(indicator + tail, denominator) if denominator else F(0)
            assert total <= factor * root + F(tail - (r - 1) * indicator, b + 1)


def sharp_menu(r, b):
    n_tail = r - 1
    j = (r - 1) // 2
    labels = [('U', 0), ('U', 1), ('V', 0), ('V', 1)]
    n = {a: {c: 0 for c in labels} for a in labels}
    for e in (0, 1):
        root = ('U', e)
        n[('U', 1 - e)][root] += j
        n[('V', e)][root] += n_tail - j
        root = ('V', e)
        n[('U', e)][root] += 1
        n[('V', 1 - e)][root] += n_tail - 1
    p = F(1, r - j)
    pi = {a: (p / 2 if a[0] == 'U' else (1 - p) / 2) for a in labels}
    for a in labels:
        assert n[a][a] == 0
        assert sum(n[c][a] for c in labels) == r - 1
        assert pi[a] > 0
        assert sum(F(n[a][c], r - 1) * pi[c] for c in labels) == pi[a]
    if r >= 3:
        for source in labels:
            reachable = {source}
            while True:
                extended = reachable | {a for c in reachable for a in labels if n[a][c]}
                if extended == reachable:
                    break
                reachable = extended
            assert reachable == set(labels)
    root_sum = F(0)
    total_sum = F(0)
    for a in labels:
        indicator = int(a[0] == 'U')
        tail = sum(n[c][a] for c in labels if c[0] == 'U')
        assert tail == (j if indicator else 1)
        denominator = b + indicator + tail
        root_sum += pi[a] * F(indicator, denominator)
        total_sum += pi[a] * F(indicator + tail, denominator)
    factor = F(r) + F((r - 1) ** 2 // 4, b + 1)
    assert total_sum == factor * root_sum
    return len(labels)


def grid_menu(r):
    a = (r + 1) // 2
    c = r + 1 - a
    topics = list(product(range(c), range(a)))
    row_weight = a * (c - 1)
    col_weight = c * (a - 1)

    def payoff(profile, topic):
        s, t = topic
        return F(row_weight, sum(u == s for u, v in profile)) + F(col_weight, sum(v == t for u, v in profile))

    for root in topics:
        s, t = root
        tail = [z for z in topics if z != root and (z[0] == s or z[1] == t)]
        profile = [root] + tail
        assert len(profile) == r
        assert payoff(profile, root) == r - 1
        assert all(payoff(profile, z) == a * c - 1 for z in tail)
        if r >= 5:
            for last in tail:
                prefix = profile.copy()
                prefix.remove(last)
                if last[0] == s:
                    alternative = (next(u for u in range(c) if u != s), last[1])
                else:
                    alternative = (last[0], next(v for v in range(a) if v != t))
                assert payoff(prefix + [alternative], alternative) > payoff(profile, last)


def full_spe_r3():
    topics = tuple(range(4))
    customers = ((3, 2), (5, 2), (10, 2), (12, 2))
    f = (1, 0, 3, 2)
    g = (2, 3, 0, 1)
    opposite = (3, 2, 1, 0)

    def action(history):
        if not history:
            return 0
        if len(history) == 1:
            return f[history[0]]
        first, second = history
        if first == second:
            return opposite[first]
        if second == f[first]:
            return g[first]
        return min(set(topics) - set(history))

    def end(history):
        while len(history) < 3:
            history += (action(history),)
        return history

    def utility(profile, player):
        return sum((F(weight, sum(bool(mask >> t & 1) for t in profile)) for mask, weight in customers if mask >> profile[player] & 1), F(0))

    comparisons = 0
    for size in range(3):
        for history in product(topics, repeat=size):
            prescribed = end(history)
            for alternative in topics:
                assert utility(prescribed, size) >= utility(end(history + (alternative,)), size)
                comparisons += 1
    for first in topics:
        profile = end((first,))
        assert tuple(utility(profile, i) for i in range(3)) == (F(2), F(3), F(3))
    assert comparisons == 84


if __name__ == '__main__':
    checks = 0
    for r in range(2, 41):
        for b in range(11):
            check_pointwise(r, b)
            sharp_menu(r, b)
            checks += 1
    for r in range(3, 41):
        grid_menu(r)
    full_spe_r3()
    print(f'PASS: {checks} exact parameter pairs; 38 grid menus; complete r3 SPE, 84 comparisons.')
