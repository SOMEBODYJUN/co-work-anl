"""Exact implementation checks for the stationary scalar envelope; no SPE claim."""
from fractions import Fraction as F


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


if __name__ == '__main__':
    checks = 0
    for r in range(2, 41):
        for b in range(11):
            check_pointwise(r, b)
            sharp_menu(r, b)
            checks += 1
    print(f'PASS: {checks} exact parameter pairs; pointwise bound and sharp no-self menus.')
