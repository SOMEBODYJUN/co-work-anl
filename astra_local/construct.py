"""Exact rational implementation of the strong-cross-chord construction.

No floating point is used. The golden-ratio comparisons are reduced to
rational polynomial signs. Inputs R, r, weights may be Fraction-compatible.
"""

from fractions import Fraction as F
from collections import Counter
import itertools
import random


def qcmp(t):
    """Return sign(t-q) for rational t, q=(sqrt(5)-1)/2."""
    t = F(t)
    if t < 0:
        return -1
    z = t*t+t-1
    return (z > 0) - (z < 0)


def quotas(r, ws, coords):
    C = sum(ws, F(0))
    gap = 1-r+sum(coords, F(0))
    V = 1+r-C
    LA, LB = (V+gap)/2, (V-gap)/2
    return qcmp(LA/r) >= 0 and qcmp(LB) >= 0


def verify(r, ws, coords):
    gap = 1-r+sum(coords, F(0))
    for w, c in zip(ws, coords):
        assert -w <= c <= w
        if c == w:
            assert gap <= w
        elif c == -w:
            assert gap >= -w
        else:
            assert c == gap
    assert quotas(r, ws, coords)


def vertex_exchange(ws, target):
    """Find a pair-edge-local maximum of sum(c_i^2), sum(c_i)=target.

    abs(target)<=sum(ws). A deterministic first improving
    edge is used. Return coordinates and elementary operation counters.
    """
    m = len(ws)
    assert abs(target) <= sum(ws)
    c = [-w for w in ws]
    fill = target+sum(ws)
    for i, w in enumerate(ws):
        inc = min(2*w, fill)
        c[i] += inc
        fill -= inc
    assert fill == 0
    stats = Counter()
    while True:
        interior = [i for i in range(m) if abs(c[i]) < ws[i]]
        assert len(interior) <= 1 and sum(c) == target
        if not interior:
            return c, stats
        j = interior[0]
        z, d = ws[j], c[j]
        moved = False
        for i in range(m):
            if i == j:
                continue
            stats['edge_checks'] += 1
            v, old = ws[i], c[i]
            b = d+old
            lo, hi = max(-z, b-v), min(z, b+v)
            assert d in (lo, hi)
            nd = hi if d == lo else lo
            ni = b-nd
            gain = nd*nd+ni*ni-d*d-old*old
            if gain <= 0:
                continue
            c[j], c[i] = nd, ni
            stats['moves'] += 1
            if abs(nd) < z:
                assert ni == -old and abs(nd) > abs(d)
                stats['flips'] += 1
                if nd*d < 0:
                    stats['sign_reversals'] += 1
                    assert v > abs(d) and abs(nd) > v
            elif abs(ni) < v:
                stats['pivot_switches'] += 1
                assert v < z
            else:
                stats['endpoint_exits'] += 1
            moved = True
            break
        if not moved:
            # Audit the exact conditions used by the chord proof.
            for i in range(m):
                if i == j:
                    continue
                v = ws[i]
                if c[i] == v:
                    assert d <= v
                else:
                    assert d >= -v
                if d > 0:
                    if c[i] == v:
                        assert v >= z
                    elif v < z:
                        assert v <= d
                if d < 0:
                    if c[i] == -v:
                        assert v >= z
                    elif v < z:
                        assert v <= -d
            assert stats['pivot_switches'] < m
            assert stats['moves'] <= m*m*(m+1)+m
            return c, stats


def repair(r, ws, coords, fixed=()):
    """Largest improving pure customer, with optional forced customers.

    The chosen movable weights are nonincreasing, and each moves at most once.
    Forced customers are treated as part of the fixed base loads.
    """
    c = list(coords)
    fixed = set(fixed)
    moved = set()
    previous_weight = None
    while True:
        gap = 1-r+sum(c, F(0))
        eligible = [i for i, w in enumerate(ws) if i not in fixed and
                    ((c[i] == w and gap > w) or
                     (c[i] == -w and gap < -w))]
        if not eligible:
            return c
        i = max(eligible, key=lambda t: (ws[t], -t))
        assert i not in moved
        assert previous_weight is None or ws[i] <= previous_weight
        previous_weight = ws[i]
        moved.add(i)
        c[i] = -c[i]


def construct(R, r, weights):
    """Return an exact quota NE, or None with an infeasibility certificate.

    Output dict probabilities are original-order independent p_i(A); loads
    are in the original units. Raises ValueError outside the theorem regime.
    """
    R, r = F(R), F(r)
    weights = list(map(F, weights))
    if not (R >= r > 0 and all(w > 0 for w in weights)):
        raise ValueError('Requires R >= r > 0 and positive common weights')
    r, ws = r/R, [w/R for w in weights]
    C, delta, n = sum(ws, F(0)), 1-r, len(ws)
    if not (qcmp(2*r-1) > 0 and qcmp(C/r) < 0):
        raise ValueError('Outside r>phi*R/2 and C<q*r')
    stats = Counter()

    def finish(c, branch):
        verify(r, ws, c)
        gap = delta+sum(c, F(0))
        V = 1+r-C
        return dict(probabilities=[(1+ci/wi)/2 for ci, wi in zip(c, ws)],
                    coords=c, loads=(R*(V+gap)/2, R*(V-gap)/2),
                    branch=branch, stats=dict(stats))

    if n == 0:
        return finish([], 'empty')
    ix = max(range(n), key=lambda i: (ws[i], -i))
    x, S = ws[ix], C-ws[ix]
    if S < delta:
        if qcmp((1-x)/r) < 0:
            return dict(probabilities=None, branch='infeasible',
                        certificate=dict(largest=ix, remaining=S*R,
                                         reach_gap=delta*R,
                                         unique_loads=(R*(1-x), R*(r-S))))
        c = list(ws)
        c[ix] = -x
        return finish(repair(r, ws, c, [ix]), 'dominant_feasible')

    rest = [i for i in range(n) if i != ix]
    v, stats = vertex_exchange([ws[i] for i in rest], -delta)
    c = [F(0)]*n
    for i, cv in zip(rest, v):
        c[i] = cv
    interior = [i for i in rest if abs(c[i]) < ws[i]]
    if not interior:
        return finish(c, 'balanced_vertex')
    iz = interior[0]
    z, d = ws[iz], c[iz]
    c[ix] = d
    if quotas(r, ws, c):
        return finish(c, 'two_mixer')
    others = [i for i in rest if i != iz]

    def mixed(selected, gap, pure_sign):
        selected = set(selected)
        return [gap if i in selected else pure_sign*ws[i] for i in range(n)]

    if d > 0:
        assert all(c[i] == -ws[i] for i in others)
        large = [i for i in others if ws[i] >= z]
        small = [i for i in others if ws[i] < z]
        candidate = [i for i in small if ws[i] >= d/3]
        if candidate:
            i = candidate[0]
            return finish(mixed([ix, iz, i], (d-ws[i])/2, -1),
                          'positive_three')
        assert all(ws[i] < d/3 for i in small)
        if not large:
            prefix, T = [], F(0)
            for i in sorted(small, key=lambda i: (-ws[i], i)):
                if T+ws[i] >= d:
                    break
                T += ws[i]
                prefix.append(i)
            assert prefix
            nd = (d-T)/(len(prefix)+1)
            return finish(mixed([ix, iz]+prefix, nd, -1),
                          'positive_prefix')
        if len(large) == 1:
            iy = large[0]
            T = sum((ws[i] for i in small), F(0))
            if delta+T <= 2*z:
                return finish(mixed([ix, iz, iy], -(delta+T)/2, 1),
                              'positive_large_three')
        assert d <= delta
        pure = [-w for w in ws]
        pure[ix] = x
        return finish(repair(r, ws, pure), 'positive_repair')
    else:
        e = -d
        assert all(c[i] == ws[i] for i in others)
        candidate = [i for i in others if ws[i] >= e/3]
        if candidate:
            i = candidate[0]
            return finish(mixed([ix, iz, i], -(e-ws[i])/2, 1),
                          'negative_three')
        assert all(ws[i] < e/3 for i in others)
        pure = list(ws)
        pure[ix] = -x
        return finish(repair(r, ws, pure), 'negative_repair')


def selftest(seed=20260930, rounds=12000):
    rng = random.Random(seed)
    branches, max_stats = Counter(), Counter()
    examples = {}
    for _ in range(rounds):
        n = rng.randrange(1, 50)
        r = F(rng.randrange(810, 1001), 1000)
        raw = [rng.randrange(1, 10001) for _ in range(n)]
        C = F(rng.randrange(1, 619), 1000)*r
        if qcmp(C/r) >= 0:
            continue
        ws = [C*v/sum(raw) for v in raw]
        out = construct(1, r, ws)
        branches[out['branch']] += 1
        examples.setdefault(out['branch'], dict(r=str(r), weights=list(map(str, ws))))
        for key, val in out.get('stats', {}).items():
            max_stats[key] = max(max_stats[key], val)
    # Targeted small integer instances provide harder uneven weights.
    for ws0 in itertools.combinations_with_replacement(range(1, 9), 4):
        for delta0 in range(0, 8):
            scale = max(40, 2*sum(ws0))
            r = F(scale-delta0, scale)
            ws = [F(w, scale) for w in ws0]
            if not (qcmp(2*r-1) > 0 and qcmp(sum(ws)/r) < 0):
                continue
            out = construct(1, r, ws)
            branches[out['branch']] += 1
            examples.setdefault(out['branch'], dict(r=str(r), weights=list(map(str, ws))))
    targeted = []
    for expected, r, ws in [
        ('positive_prefix', F(85, 100), [F(16, 100), F(11, 100)]+[F(1, 32)]*8),
        ('positive_repair', F(82, 100), [F(15, 100), F(95, 1000), F(13, 100), F(13, 100)]),
        ('negative_repair', F(985, 1000), [F(21, 100)]+[F(37, 1000)]*5+[F(202, 1000)]),
        ('empty', F(9, 10), []),
        ('balanced_vertex', F(9, 10), [F(1, 5), F(1, 10)]),
        ('balanced_vertex', F(1), [F(2, 5)]),
    ]:
        out = construct(1, r, ws)
        assert out['branch'] == expected
        branches[expected] += 1
        example = dict(r=str(r), weights=list(map(str, ws)))
        examples.setdefault(expected, example)
        targeted.append(dict(branch=expected, **example,
                             probabilities=list(map(str, out['probabilities'])),
                             loads=list(map(str, out['loads']))))
    local, _ = vertex_exchange([F(14), F(13), F(19)], F(-10))
    assert local == [F(14), F(-5), F(-19)]
    assert sum(z*z for z in local) == 582 < 654
    return dict(seed=seed, random_rounds=rounds, branches=dict(branches),
                max_stats=dict(max_stats), examples=examples,
                targeted=targeted,
                local_not_global=dict(weights=[14, 13, 19], target=-10,
                                      local=[14, -5, -19], local_objective=582,
                                      better=[-14, -13, 17], better_objective=654))


if __name__ == '__main__':
    import json
    print(json.dumps(selftest(), indent=2))
