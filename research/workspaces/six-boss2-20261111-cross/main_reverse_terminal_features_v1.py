"""Independent Main formulas for 616 rows and original-terminal requery.

The 17 old queries keep their shared first/two-index moments. Each new reverse
query uses its original ordered history, not a load borrowed from the new macro.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from main_cross_query_features_v1 import all_332, weighted_value, pay


def cross_names():
    names = []
    for branch in (1, 2):
        for a in range(14):
            for b in range(a + 1, 17):
                names.append(f'oldpair{branch}:{a},{b}:product')
        for a in range(14, 17):
            for b in range(a + 1, 17):
                names += [f'oldpair{branch}:{a},{b}:same', f'oldpair{branch}:{a},{b}:off']
            names.append(f'oldpair{branch}:{a},{a}:off')
    assert len(names) == len(set(names)) == 284
    return tuple(names)


CROSS_NAMES = cross_names()


def moment_product(name, qs, moments, remaining=4):
    _, pair, mode = name.split(':')
    a, b = map(int, pair.split(','))
    if mode == 'product':
        assert a < 14 and a < b
        assert qs[a] in (0, 1)
        return qs[a] * qs[b]
    assert 14 <= a <= b < 17
    same = qs[a] if a == b else moments[{(14, 15): 0, (14, 16): 1, (15, 16): 2}[a, b]]
    if mode == 'same':
        assert a < b
        return same
    assert mode == 'off' and remaining > 1
    return (remaining * qs[a] * qs[b] - same) / (remaining - 1)


def all_616(p, ell, t, qs, moments, hidden, k=3, remaining=4):
    values, budgets = all_332(p, ell, t, qs, hidden, k)
    b, c, j, v, s, ss = hidden
    for name in CROSS_NAMES:
        branch, pair, mode = name.split(':')
        a, d = map(int, pair.split(','))
        beta, first, last = (p + t + s, b, c) if branch == 'oldpair1' else (p + c + ss, j, v)
        rho = moment_product(name, qs, moments, remaining)
        assert 0 <= rho <= min(qs[a], qs[d])
        values[name] = (qs[a] + qs[d]) / (beta + 1) - (rho + first) / ((beta + 1) * (beta + 2)) - pay(first + last, beta + first + last)
        budgets[name] = (F(0), F(0), F(0))
    assert len(values) == len(budgets) == 616
    return values, budgets


def reverse_value(name, qs, hidden, family=0):
    node, label = name.split(':')
    b, c, j, v = hidden[:4]
    e = dict(b=b, c=c, j=j, v=v)[label]
    r, z = qs[12], qs[13]
    if node == 'priorR':
        beta = sum(qs[:3]) + qs[6] + qs[10 if family == 0 else 11]
        true = r
    else:
        assert node == 'priorZ'
        beta = sum(qs[:4]) + r
        true = z
    return F(e) / (beta + 1) - pay(true, beta + true)


def projection_624(weights, k=3, family=0, remaining=4):
    old = tuple((n, w) for n, w in weights.items() if not n.startswith('prior'))
    reverse = tuple((n, w) for n, w in weights.items() if n.startswith('prior'))
    assert all(n in ('priorR:b', 'priorR:c', 'priorR:j', 'priorR:v', 'priorZ:b', 'priorZ:c', 'priorZ:j', 'priorZ:v') for n, w in reverse)
    hidden = tuple(bits + (s, ss) for bits in product((0, 1), repeat=4) for s in range(k - 2) for ss in range(k - 2))

    @lru_cache(None)
    def minimum(p, ell, t, qs, moments):
        products = tuple((n, moment_product(n, qs, moments, remaining)) for n, w in old if n.startswith('oldpair'))
        return min(weighted_value(p, ell, t, qs, h, old, products)
                   + sum(w * reverse_value(n, qs, h, family) for n, w in reverse) for h in hidden)
    return minimum
