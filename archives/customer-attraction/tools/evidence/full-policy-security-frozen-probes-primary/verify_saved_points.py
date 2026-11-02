"""Rebuild only the four saved inputs, without running the random searches.

The two integer points and reconstructed dual are exact Fraction checks.
The weak-iid decimal record is reported as stored, not rounded into a certificate.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent


def load(name):
    return json.loads((BASE / 'original' / name).read_text())


def policy(record):
    n, k = record['n'], record['k']
    actions = {tuple(map(int, h.split(','))) if h else (): a
               for h, a in record['actions'].items()}
    assert len(actions) == sum(k ** d for d in range(n))
    for d in range(n):
        for h in product(range(k), repeat=d):
            assert h in actions and 0 <= actions[h] < k

    def leaf(h):
        while len(h) < n:
            h += (actions[h],)
        return h

    def row(a, h):
        return [F(int(mask >> a & 1), max(1, sum(mask >> b & 1 for b in h)))
                for mask in range(1, 1 << k)]

    rows = {}
    for h, a in actions.items():
        prescribed = row(a, leaf(h))
        for b in range(k):
            if b != a:
                rows[h, b] = [x - y for x, y in zip(prescribed, row(b, leaf(h + (b,))))]
    actual = leaf(())
    counts = [actual.count(a) for a in range(k)]
    assert counts == record['on_path']
    c = [F(any(mask >> a & 1 for a in actual)) for mask in range(1, 1 << k)]
    return n, k, actions, actual, rows, c


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def one_deviation_backgrounds(n, k, actions):
    leaves = []

    def walk(h, deviations):
        if len(h) == n:
            leaves.append(h)
            return
        a = actions[h]
        walk(h + (a,), deviations)
        if deviations < 1:
            for b in range(k):
                if b != a:
                    walk(h + (b,), deviations + 1)

    walk((), 0)
    backgrounds = set()
    for h in leaves:
        for i in range(n):
            b = h[:i] + h[i+1:]
            backgrounds.add(tuple(b.count(a) for a in range(k)))
    return sorted(backgrounds), len(leaves)


def point(name):
    record = load(name)
    n, k, actions, actual, rows, c = policy(record)
    w = [F(str(x)) for x in record['weights']]
    p = [F(str(x)) for x in record['p']]
    assert sum(p) == 1 and min(p) >= 0 and min(w) >= 0
    ic = [dot(row, w) for row in rows.values()]
    W = dot(c, w)
    bgs = list(combinations_with_replacement(range(k), n-1))
    def payoff(background):
        return sum(w[mask-1] * sum(p[a] for a in range(k) if mask >> a & 1)
                   / (1 + sum(mask >> a & 1 for a in background))
                   for mask in range(1, 1 << k))
    guaranteed = min(map(payoff, bgs))
    # Every positive mass is a single unit client type. Repeating an interested
    # label n-1 times caps every query by 1/n, and the saved p attains it.
    positive = [(i+1, x) for i, x in enumerate(w) if x]
    assert len(positive) == 1 and positive[0][1] == 1
    mask = positive[0][0]
    assert guaranteed == F(1, n)
    assert all(dot(row, w) >= 0 for row in rows.values())
    result = dict(n=n, k=k, histories=len(actions), nonself_comparisons=len(rows),
                  actual_labels=actual, actual_counts=record['on_path'],
                  unique_nonzero_interest_mask=mask, welfare=str(W), min_ic=str(min(ic)),
                  exact_security=str(guaranteed), full_background_count=len(bgs),
                  exact_n_v_over_W=str(n * guaranteed / W))
    if 'backgrounds' in record:
        restricted, leaves = one_deviation_backgrounds(n, k, actions)
        assert [list(b) for b in restricted] == record['backgrounds']
        result.update(saved_backgrounds_rebuilt=True, restricted_background_count=len(restricted),
                      one_deviation_leaves=leaves)
    return result


def dual():
    record = load('one_leaf_dual.json')
    n, k, actions, actual, rows, c = policy(record)
    p = [F(str(x)) for x in record['p']]
    assert p == [F(1, 4)] * 4
    b = record['Q'][0]['background']
    assert record['Q'][0]['probability'] == 1
    backgrounds, leaves = one_deviation_backgrounds(n, k, actions)
    assert tuple(b) in backgrounds
    lambdas = [F(8, 15), F(2, 15)]
    weighted = [F(0)] * len(c)
    for entry, lam in zip(record['lambda_rows'], lambdas):
        assert abs(float(lam) - entry['l']) < 1e-15
        g = rows[tuple(entry['h']), entry['b']]
        weighted = [x + lam*y for x, y in zip(weighted, g)]
    beta = [sum(p[a] for a in range(k) if mask >> a & 1)
            / (1 + sum(b[a] for a in range(k) if mask >> a & 1))
            for mask in range(1, 1 << k)]
    rem = [x - y - n*z for x, y, z in zip(c, weighted, beta)]
    assert min(rem) >= 0
    assert max(abs(float(x)-y) for x, y in zip(rem, record['remainder'])) < 1e-14
    return dict(histories=len(actions), nonself_comparisons=len(rows),
                actual_labels=actual, actual_counts=record['on_path'],
                reconstructed_lambda=list(map(str, lambdas)), background=b,
                restricted_background_count=len(backgrounds), one_deviation_leaves=leaves,
                exact_remainder=list(map(str, rem)), min_remainder=str(min(rem)),
                scope='One specified full policy and uniform p only; not all p or true v.')


def weak_decimal():
    record = load('weak_iid_best.json')
    n, k, actions, actual, rows, c = policy(record)
    w = [F(str(x)) for x in record['weights']]
    q = [F(str(x)) for x in record['q']]
    W = dot(c, w)
    ic = [dot(row, w) for row in rows.values()]
    t = [sum(q[a] for a in range(k) if mask >> a & 1) for mask in range(1, 1 << k)]
    Z = sum(x * (1-(1-y)**n) for x, y in zip(w, t))
    g = [sum((1-y)**j for j in range(n))/n for y in t]
    pure = [sum(w[mask-1]*g[mask-1] for mask in range(1, 1<<k) if mask >> a & 1)
            for a in range(k)]
    errors = [v - Z/n for v in pure]
    return dict(histories=len(actions), nonself_comparisons=len(rows),
                actual_labels=actual, actual_counts=record['on_path'],
                q_sum_exact=str(sum(q)), welfare_exact=str(W),
                min_ic_exact=str(min(ic)), min_ic_float=float(min(ic)),
                negative_ic_count=sum(x < 0 for x in ic),
                max_static_kkt_violation_float=float(max(errors)),
                stored_Z_over_W=record['Z_over_W'], recomputed_Z_over_W=float(Z/W),
                recomputed_weak_ratio=float(F(2*n-1, 2*n)*Z/W),
                caveat='Decimal rationalization is a diagnostic; no exact Nash/SPE certificate asserted.')


if __name__ == '__main__':
    output = dict(best=point('best.json'), leaf=point('leaf_support_best.json'),
                  reconstructed_dual=dual(), weak_decimal=weak_decimal(),
                  random_search_runs=0)
    print(json.dumps(output, ensure_ascii=False, indent=2))
