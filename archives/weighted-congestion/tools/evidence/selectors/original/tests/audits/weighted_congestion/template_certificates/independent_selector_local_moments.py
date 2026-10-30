#!/usr/bin/env python3
"""Independent exact checks of finite costs, categorical differences, and duals."""
from fractions import Fraction as F
from itertools import product, combinations
from math import factorial
from pathlib import Path
import hashlib
import json


def subsets(items):
    items = tuple(items)
    for r in range(len(items) + 1):
        yield from combinations(items, r)


def states(ms):
    return tuple(product(*(range(m) for m in ms)))


def sigs(ms, core=False):
    return tuple(x for x in product(*(range((1 << m) - int(core)) for m in ms)) if any(x))


def c(sig, k, w, s, i):
    # Direct load definition; no polynomial-space expansion is used here.
    if not ((sig[i] >> s[i]) & 1):
        return F(0)
    return sum(w[j] for j in range(len(w)) if (sig[j] >> s[j]) & 1) ** k


def keys(ms, d):
    result = []
    for i in range(len(ms)):
        for own in range(ms[i]):
            for t in subsets(j for j in range(len(ms)) if j != i):
                if len(t) <= d:
                    for u in product(*(range(1, ms[j]) for j in t)):
                        result.append((i, own, t, u))
    return result


def basis(key, s, player):
    i, own, t, u = key
    return int(player == i and s[i] == own and all(s[j] == a for j, a in zip(t, u)))


def first_relation(columns):
    # Gaussian elimination on coordinate rows; intentionally independent of
    # the author's incremental basis/column-dependence implementation.
    width = len(columns)
    mat = [[F(col[r]) for col in columns] for r in range(len(columns[0]))]
    pivots = []
    prow = 0
    for col in range(width):
        pivot = next((r for r in range(prow, len(mat)) if mat[r][col]), None)
        if pivot is None:
            continue
        mat[prow], mat[pivot] = mat[pivot], mat[prow]
        div = mat[prow][col]
        mat[prow] = [v / div for v in mat[prow]]
        for r in range(len(mat)):
            if r != prow and mat[r][col]:
                factor = mat[r][col]
                mat[r] = [a - factor * b for a, b in zip(mat[r], mat[prow])]
        pivots.append(col)
        prow += 1
        if prow == len(mat):
            break
    free = next((j for j in range(width) if j not in pivots), None)
    if free is None:
        return None
    v = [F(0)] * width
    v[free] = 1
    for r, p in enumerate(pivots):
        v[p] = -mat[r][free]
    assert all(sum(v[j] * columns[j][r] for j in range(width)) == 0
               for r in range(len(columns[0])))
    return v


def reduce_positive(columns, coeffs):
    coeffs = list(coeffs)
    active = [j for j, a in enumerate(coeffs) if a]
    steps = 0
    while active:
        rel = first_relation([columns[j] for j in active])
        if rel is None:
            break
        if not any(x > 0 for x in rel):
            rel = [-x for x in rel]
        step = min(coeffs[j] / x for j, x in zip(active, rel) if x > 0)
        for j, x in zip(active, rel):
            coeffs[j] -= step * x
            assert coeffs[j] >= 0
        active = [j for j in active if coeffs[j]]
        steps += 1
    return coeffs, active, steps


def linear_combination(columns, coeffs):
    if not columns:
        return []
    return [sum(a * col[r] for a, col in zip(coeffs, columns)) for r in range(len(columns[0]))]


def cost_fixture(ms, w, d, core=False, zero=False):
    ss = states(ms)
    typ = tuple((sig, k) for sig in sigs(ms, core) for k in range(d + 1))
    columns = [tuple(c(sig, k, w, s, i) for s in ss for i in range(len(ms))) for sig, k in typ]
    coeffs = [F(0) if zero else F((j % 5) + 1, (j % 3) + 1) for j in range(len(typ))]
    reduced, active, steps = reduce_positive(columns, coeffs)
    assert linear_combination(columns, coeffs) == linear_combination(columns, reduced)
    dim = len(keys(ms, d))
    assert len(active) <= dim
    chosen = [typ[j][0] for j in active]
    for i, m in enumerate(ms):
        for a in range(m):
            one = [0] * len(ms)
            one[i] = 1 << a
            chosen.append(tuple(one))
    for i, m in enumerate(ms):
        actions = [set(j for j, sig in enumerate(chosen) if (sig[i] >> a) & 1) for a in range(m)]
        assert len(set(map(frozenset, actions))) == m
        if core:
            assert all(actions)
            assert set.intersection(*actions) == set()
            assert all(not (a <= b) for x, a in enumerate(actions) for y, b in enumerate(actions) if x != y)
    # Anchored finite differences uniquely recover categorical coefficients.
    # All orders above d must vanish, which tests the claimed common space.
    high_checks = 0
    for sig, k in typ:
        for i in range(len(ms)):
            for own in range(ms[i]):
                for t in subsets(j for j in range(len(ms)) if j != i):
                    if len(t) <= d:
                        continue
                    for u in product(*(range(1, ms[j]) for j in t)):
                        diff = F(0)
                        for r in subsets(t):
                            s = [0] * len(ms)
                            s[i] = own
                            for j, a in zip(t, u):
                                if j in r:
                                    s[j] = a
                            diff += (-1) ** (len(t) - len(r)) * c(sig, k, w, tuple(s), i)
                        assert diff == 0
                        high_checks += 1
    return dict(ms=ms, weights=list(map(str, w)), d=d, core=core, all_zero=zero,
                original_types=len(typ), compressed_types=len(active), D=dim,
                markers=sum(ms), elimination_steps=steps,
                cost_entries=len(ss) * len(ms), vanishing_high_order_differences=high_checks)


def dual_fixture(n, d, alpha, genuine):
    ms = (2,) * n
    w = tuple(F(2 * j + 1, j + 1) for j in range(n))
    ss = states(ms)
    kk = keys(ms, d)
    chosen = []
    for s in ss:
        i = 0 if genuine else sum((j + 1) * a for j, a in enumerate(s)) % n
        t = list(s)
        if genuine:
            t[i] ^= 1
        chosen.append((i, tuple(t)))
    psis = [tuple(F(basis(key, s, i)) - alpha * basis(key, t, i) for key in kk)
            for s, (i, t) in zip(ss, chosen)]
    old = [F(1, len(ss))] * len(ss)
    augmented = [v + (F(1),) for v in psis]
    new, active, steps = reduce_positive(augmented, old)
    assert sum(new) == 1
    assert linear_combination(augmented, new) == linear_combination(augmented, old)
    assert len(active) <= len(kk) + 1
    checked = 0
    for sig in sigs(ms):
        for k in range(d + 1):
            row = [c(sig, k, w, s, i) - alpha * c(sig, k, w, t, i)
                   for s, (i, t) in zip(ss, chosen)]
            before = sum(a * b for a, b in zip(old, row))
            after = sum(a * b for a, b in zip(new, row))
            assert after == before <= 0
            checked += 1
    return dict(n=n, d=d, alpha=str(alpha), genuine_flip=genuine,
                original_support=len(ss), reduced_support=len(active), D=len(kk),
                elimination_steps=steps, all_full_signature_columns=checked)


def one_mover_span(ms, w, i, d, core):
    contexts = tuple(product(*(range(ms[j]) for j in range(len(ms)) if j != i)))
    opponents = [j for j in range(len(ms)) if j != i]
    tests = []
    for sig in sigs(ms, core):
        if sig[i] != 1:
            continue
        for k in range(d + 1):
            tests.append(tuple((w[i] + sum(w[j] for j, a in zip(opponents, x) if (sig[j] >> a) & 1)) ** k
                               for x in contexts))
    # Extract rank using independent row elimination above.
    independent = []
    for test in tests:
        if first_relation(independent + [test]) is None:
            independent.append(test)
    moment_count = sum(len(tuple(product(*(range(1, ms[j]) for j in t))))
                       for t in subsets(opponents) if len(t) <= d)
    assert len(independent) == moment_count
    return dict(ms=ms, i=i, d=d, core=core, primitive_tests=len(tests), context_moment_rank=len(independent))


def main():
    out = dict(
        arithmetic="fractions.Fraction; exact zero tests; independent Gaussian elimination",
        reviewed_sha256='f4541469f8aadbb57037b10e1248ed6b1db24d493e31d0d1974c0f85bb6aecbe',
        cost_fixtures=[
            cost_fixture((1,), (F(3, 2),), 0),
            cost_fixture((3,), (F(3, 2),), 2),
            cost_fixture((2, 3, 1), (F(1, 2), F(7, 3), F(2)), 1),
            cost_fixture((2, 2, 2), (F(1, 2), F(7, 3), F(2)), 0),
            cost_fixture((2, 2, 2), (F(1, 2), F(7, 3), F(2)), 1, core=True),
            cost_fixture((2, 3), (F(1, 2), F(7, 3)), 1, core=True),
            cost_fixture((2, 2), (F(1), F(2)), 0, core=True, zero=True),
        ],
        dual_fixtures=[dual_fixture(5, 0, F(1), True), dual_fixture(5, 0, F(3, 2), False)],
        one_mover_spans=[one_mover_span((2, 3, 2), (F(1, 3), F(3, 2), F(7, 5)), 0, d, core)
                         for d in range(3) for core in (False, True)],
    )
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
