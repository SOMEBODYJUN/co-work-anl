#!/usr/bin/env python3
"""Exact finite audits; these support, and do not replace, the general proofs."""
from fractions import Fraction as Q
from itertools import product, combinations
from math import comb, lcm
from pathlib import Path
import json
import random

HERE = Path(__file__).resolve().parent


def compositions(n, p):
    if p == 1:
        yield (n,)
        return
    for k in range(n + 1):
        for tail in compositions(n - k, p - 1):
            yield (k,) + tail


def rank(rows):
    basis = {}
    for raw in rows:
        row = list(map(Q, raw))
        for j in sorted(basis):
            if row[j]:
                x = row[j]
                row = [a - x*b for a, b in zip(row, basis[j])]
        j = next((j for j, x in enumerate(row) if x), None)
        if j is not None:
            x = row[j]
            basis[j] = [a/x for a in row]
    return len(basis)


def cover(p, T):
    return tuple(Q(bool(B & T)) for B in range(1, 1 << p))


def payoff(p, q, a):
    assert q[a] > 0
    return tuple(Q(1, sum(q[b] for b in range(p) if B >> b & 1))
                 if B >> a & 1 else Q(0) for B in range(1, 1 << p))


def harmonic(n):
    return sum((Q(1, i) for i in range(1, n + 1)), Q(0))


def potential(p, q):
    return tuple(harmonic(sum(q[b] for b in range(p) if B >> b & 1))
                 for B in range(1, 1 << p))


def minus(x, y):
    return tuple(a-b for a, b in zip(x, y))


def coverage_masks(m, p):
    return [T for T in range(1, 1 << p) if T.bit_count() <= m]


def positive_potential_expansion(p, q):
    support = sum(1 << a for a in range(p) if q[a])
    coeff = {}
    for R in range(1, 1 << p):
        if R & ~support:
            continue
        shift = sum(q[a] for a in range(p) if (support & ~R) >> a & 1)
        poly = {shift: 1}
        for a in range(p):
            if R >> a & 1:
                updated = dict(poly)
                for k, v in poly.items():
                    updated[k + q[a]] = updated.get(k + q[a], 0) - v
                poly = updated
        assert sum(poly.values()) == 0
        coeff[R] = -sum((v*harmonic(k) for k, v in poly.items()), Q(0))
        assert coeff[R] > 0
    phi = potential(p, q)
    for B in range(1, 1 << p):
        assert phi[B-1] == sum((v for R, v in coeff.items() if R & B), Q(0))
    assert sum(coeff.values(), Q(0)) == harmonic(sum(q))
    return len(coeff)


def audit_spaces(m, p):
    masks = coverage_masks(m, p)
    cs = [cover(p, T) for T in masks]
    fs, phis, diffs = [], [], []
    positive_terms = 0
    for q in compositions(m, p):
        phis.append(potential(p, q))
        positive_terms += positive_potential_expansion(p, q)
        fs.extend(payoff(p, q, a) for a in range(p) if q[a])
    for r in compositions(m-1, p):
        branches = []
        for a in range(p):
            q = tuple(x + (i == a) for i, x in enumerate(r))
            branches.append(payoff(p, q, a))
            assert minus(potential(p, q), potential(p, r)) == branches[-1]
        diffs.extend(minus(branches[a], branches[0]) for a in range(1, p))
    d = sum(comb(p, k) for k in range(1, min(m, p)+1))
    ranks = [rank(x) for x in (cs, fs, phis, diffs)]
    assert ranks == [d, d, d, d-1]
    assert rank(diffs + [cs[0]]) == d
    assert all(row[-1] == 0 for row in diffs)
    return dict(m=m, p=p, dimension=d, ranks_coverage_payoff_potential_terminal_differences=ranks,
                positive_potential_coefficients_checked=positive_terms)


def history_strategy(m, p, seed):
    rng = random.Random(seed)
    return {h: rng.randrange(p) for k in range(m) for h in product(range(p), repeat=k)}


def terminal(h, sigma, m):
    while len(h) < m:
        h += (sigma[h],)
    return h


def count(path, p):
    return tuple(path.count(a) for a in range(p))


def strategy_rows(m, p, sigma):
    rows, last = [], []
    for h, a in sigma.items():
        actual = payoff(p, count(terminal(h, sigma, m), p), a)
        for b in range(p):
            alternative = payoff(p, count(terminal(h+(b,), sigma, m), p), b)
            row = minus(actual, alternative)
            rows.append(row)
            if len(h) == m-1:
                last.append(row)
    root = terminal((), sigma, m)
    c = cover(p, sum(1 << a for a in set(root)))
    return rows, last, c, root


def audit_strategies():
    records = []
    for m, p in [(1, 1), (1, 4), (4, 1), (2, 3), (3, 3), (3, 4), (4, 3)]:
        d = len(coverage_masks(m, p))
        for seed in range(8):
            rows, last, c, root = strategy_rows(m, p, history_strategy(m, p, seed))
            rs = [rank(last), rank(rows), rank(rows+[c])]
            assert rs == [d-1, d-1, d]
            assert all(row[-1] == 0 for row in rows)
        records.append(dict(m=m, p=p, independent_complete_strategies=8,
                            last_all_root_ranks=[d-1, d-1, d]))
    return records


def audit_exposures():
    records = []
    for p in range(1, 8):
        checks = 0
        for B in range(1, 1 << p):
            for C in range(1, 1 << p):
                value = sum(bool(C >> a & 1) for a in range(p) if not B >> a & 1)
                value += sum(2*bool(C & ((1 << a) | (1 << b)))
                             - bool(C >> a & 1) - bool(C >> b & 1)
                             for a, b in combinations(range(p), 2) if B >> a & 1 and B >> b & 1)
                r = (B & C).bit_count()
                assert value == (C & ~B).bit_count() + r*(B.bit_count()-r)
                assert value >= 0 and ((value == 0) == (B == C))
                checks += 1
        records.append(dict(p=p, ordered_nonempty_type_pairs=checks,
                            unique_zero_each_exposure=True, nonzero_proper_exposure=p >= 2))
    return records


def audit_disjoint_spe(m, p):
    assert p >= m+1
    sigma = {h: next(a for a in range(p) if a not in h)
             for k in range(m) for h in product(range(p), repeat=k)}
    rows, last, c, root = strategy_rows(m, p, sigma)
    w = tuple(Q(B.bit_count() == 1) for B in range(1, 1 << p))
    slacks = [sum((a*b for a, b in zip(row, w)), Q(0)) for row in rows]
    assert all(x >= 0 for x in slacks)
    assert root == tuple(range(m))
    assert sum(a*b for a, b in zip(c, w)) == m
    if m >= 2:
        for a, b in combinations(range(p), 2):
            assert sum(x*y for x, y in zip(cover(p, (1 << a) | (1 << b)), w)) == 2
    collapsed = [Q(0)] * ((1 << p)-1)
    collapsed[-1] = Q(m)
    assert all(sum(x*y for x, y in zip(row, collapsed)) == 0 for row in rows)
    assert sum(x*y for x, y in zip(c, collapsed)) == m
    return dict(m=m, p=p, decision_histories=len(sigma), action_comparisons=len(rows),
                minimum_slack=str(min(slacks)), strict_comparisons=sum(x > 0 for x in slacks),
                root=list(root), welfare=m, optimum=m, exact_moment_external_obstruction=m >= 2,
                inequalities_only_universal_collapse_preserves_welfare_optimum=True,
                collapse_creates_duplicate_coverage_labels=True)


def kernel_relation(rows):
    """One exact rational relation among columns of a wide matrix."""
    a = [list(map(Q, r)) for r in rows]
    n = len(a[0]); pivots = []; row = 0
    for col in range(n):
        i = next((i for i in range(row, len(a)) if a[i][col]), None)
        if i is None:
            continue
        a[row], a[i] = a[i], a[row]
        z = a[row][col]
        a[row] = [x/z for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                z = a[i][col]
                a[i] = [x-z*y for x, y in zip(a[i], a[row])]
        pivots.append(col); row += 1
        if row == len(a):
            break
    free = next(c for c in range(n) if c not in pivots)
    z = [Q(0)]*n; z[free] = Q(1)
    for i, c in enumerate(pivots):
        z[c] = -a[i][free]
    assert all(sum(x*y for x, y in zip(r, z)) == 0 for r in rows)
    return z


def audit_sparse_reduction(m=2, p=5):
    masks = coverage_masks(m, p)
    types = list(range(1, 1 << p))
    w = {B: Q(1+B % 5) for B in types}
    original = tuple(sum(w[B] for B in types if B & T) for T in masks)
    rounds = 0
    while len(w) > len(masks):
        support = sorted(w)
        matrix = [[Q(bool(B & T)) for B in support] for T in masks]
        z = kernel_relation(matrix)
        assert any(x > 0 for x in z) and any(x < 0 for x in z)
        t = min(w[B]/x for B, x in zip(support, z) if x > 0)
        w = {B: w[B]-t*x for B, x in zip(support, z) if w[B]-t*x > 0}
        rounds += 1
    assert original == tuple(sum(w[B] for B in w if B & T) for T in masks)
    scale = lcm(*(x.denominator for x in w.values()))
    assert all((x*scale).denominator == 1 for x in w.values())
    return dict(m=m, p=p, original_positive_types=len(types), final_positive_types=len(w),
                dimension=len(masks), elimination_rounds=rounds, integer_scale=scale,
                all_union_moments_preserved=True,
                sparse_rational_types={str(B): str(x) for B, x in sorted(w.items())})


def main():
    grid = [(m, p) for m in range(1, 5) for p in range(1, 6)] + [(3, 6), (8, 1)]
    report = dict(
        identity="finite exact audit of CR-1 through CR-5; general half remains OPEN",
        arithmetic="Python standard-library fractions.Fraction; direct all nonempty interest types",
        spaces=[audit_spaces(m, p) for m, p in grid],
        full_ordered_history_strategies=audit_strategies(),
        exposed_rays=audit_exposures(),
        disjoint_complete_SPE=[audit_disjoint_spe(m, m+1) for m in range(1, 5)],
        adaptive_sparse_reduction=audit_sparse_reduction(),
        boundaries="m=1: only singleton extreme rays; p=1: one ray, no nonzero proper exposure; empty type invisible",
    )
    target = HERE / 'coverage_geometry_audit.json'
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(output=str(target), all_checks_passed=True,
                          space_cases=len(report['spaces']), full_strategy_cases=56,
                          exposure_type_pairs=sum(r['ordered_nonempty_type_pairs'] for r in report['exposed_rays']),
                          sparse_support=report['adaptive_sparse_reduction']['final_positive_types'])))


if __name__ == '__main__':
    main()
