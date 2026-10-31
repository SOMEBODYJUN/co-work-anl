"""Exact candidate/dual recovery for a common-submodular path relaxation.

The two occupied labels are distinguished; unused labels are exchangeable in
the input. For every actual prefix and queried label, all remaining providers
copying that label is a universal lower bound on its Shapley payoff, by the
decreasing-marginal dilution lemma. These cuts are necessary, not SPE complete.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent


def dot(row, values):
    return sum((a * b for a, b in zip(row, values)), F(0))


def subsets(mask):
    x = mask
    while True:
        yield x
        if not x:
            break
        x = (x - 1) & mask


def compositions(p, n):
    if p == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for tail in compositions(p - 1, n - a):
                yield (a,) + tail


class Moments:
    def __init__(self, p, d, m):
        self.p, self.d, self.m = p, d, m
        self.keys = tuple(sorted({self.key(mask) for mask in range(1, 1 << p)
                                  if mask.bit_count() <= m}))
        self.index = {key: j for j, key in enumerate(self.keys)}
        self.rows = self.axioms()

    def key(self, mask):
        return mask & ((1 << self.d) - 1), (mask >> self.d).bit_count()

    def C(self, mask):
        row = [F(0)] * len(self.keys)
        if mask:
            row[self.index[self.key(mask)]] = 1
        return tuple(row)

    def combine(self, *terms):
        return tuple(sum((factor * row[j] for factor, row in terms), F(0))
                     for j in range(len(self.keys)))

    @lru_cache(None)
    def payoff(self, q, a):
        assert q[a] > 0 and sum(q) <= self.m
        others = sum(1 << b for b in range(self.p) if b != a and q[b])
        out = [F(0)] * len(self.keys)
        for R in subsets(others):
            base = q[a] + sum(q[b] for b in range(self.p)
                              if (others & ~R) & (1 << b))
            beta = sum((F((-1) ** S.bit_count(), base + sum(q[b] for b in range(self.p)
                       if S & (1 << b))) for S in subsets(R)), F(0))
            assert beta > 0
            delta = self.combine((1, self.C(R | (1 << a))), (-1, self.C(R)))
            out = [x + beta * y for x, y in zip(out, delta)]
        return tuple(out)

    def axioms(self):
        rows = set()
        for S in range(1 << self.p):
            if S.bit_count() >= self.m:
                continue
            missing = [a for a in range(self.p) if not S & (1 << a)]
            for a in missing:
                rows.add(self.combine((1, self.C(S | (1 << a))), (-1, self.C(S))))
            if S.bit_count() <= self.m - 2:
                for a, b in combinations(missing, 2):
                    rows.add(self.combine((1, self.C(S | (1 << a))),
                        (1, self.C(S | (1 << b))), (-1, self.C(S)),
                        (-1, self.C(S | (1 << a) | (1 << b)))))
        rows.discard((F(0),) * len(self.keys))
        return tuple(sorted(rows))

    def path_rows(self, path):
        q = tuple(path.count(a) for a in range(self.p))
        k = [0] * self.p
        rows = []
        for a in path:
            own = self.payoff(q, a)
            remaining = self.m - sum(k)
            for T in range(self.p):
                r = tuple(n + (remaining if b == T else 0) for b, n in enumerate(k))
                secure = self.payoff(r, T)
                row = self.combine((1, own), (-1, secure))
                if any(row):
                    rows.append(row)
            k[a] += 1
        return tuple(sorted(set(rows)))


def recover_vertex(rows, w, floating):
    support = [j for j, v in enumerate(floating) if v > 1e-8]
    active = [(w, F(1))] + [(row, F(0)) for row in rows
        if abs(sum(float(a) * b for a, b in zip(row, floating))) < 1e-7]
    basis = {}
    for row, rhs in active:
        eq = [row[j] for j in support] + [rhs]
        for pivot in sorted(basis):
            factor = eq[pivot]
            if factor:
                eq = [a - factor * b for a, b in zip(eq, basis[pivot])]
        pivot = next((j for j, v in enumerate(eq[:-1]) if v), None)
        if pivot is None:
            if eq[-1]:
                return None
            continue
        factor = eq[pivot]
        basis[pivot] = [v / factor for v in eq]
        if len(basis) == len(support):
            break
    if len(basis) != len(support):
        return None
    solution = [F(0)] * len(support)
    for pivot in sorted(basis, reverse=True):
        solution[pivot] = basis[pivot][-1] - sum(basis[pivot][j] * solution[j]
            for j in range(pivot + 1, len(support)))
    values = [F(0)] * len(floating)
    for j, v in zip(support, solution):
        values[j] = v
    return tuple(values)


def solve(rows, w, objective):
    res = linprog(-np.array(objective, dtype=float), A_ub=-np.array(rows, dtype=float),
        b_ub=np.zeros(len(rows)), A_eq=[np.array(w, dtype=float)], b_eq=[1],
        bounds=(0, None), method='highs')
    assert res.success, res.message

    def feasible(v):
        return v is not None and all(a >= 0 for a in v) and dot(w, v) == 1 \
            and all(dot(row, v) >= 0 for row in rows)

    values = tuple(F(float(a)).limit_denominator(10**7) for a in res.x)
    if not feasible(values):
        values = recover_vertex(rows, w, res.x)
    if not feasible(values):
        return {'certified': False, 'reason': 'exact_primal_recovery_failed'}
    beta = F(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
    mu = tuple(F(float(-a)).limit_denominator(10**7) for a in res.ineqlin.marginals)
    dual_ok = all(a >= 0 for a in mu) and all(beta * w[j] - sum(
        a * row[j] for a, row in zip(mu, rows)) >= objective[j]
        for j in range(len(w)))
    value = dot(objective, values)
    return {'certified': True, 'values': values, 'value': value,
            'dual_bound': beta if dual_ok else None,
            'dual_optimal': dual_ok and beta == value,
            'dual_support': [(i, a) for i, a in enumerate(mu) if a] if dual_ok else []}


def spe_completion(moments, values, target, path=None):
    p, m = moments.p, moments.m
    payoff_cache = {}
    thresholds = {}

    def utility(q, a):
        if (q, a) not in payoff_cache:
            payoff_cache[q, a] = dot(moments.payoff(q, a), values)
        return payoff_cache[q, a]

    @lru_cache(None)
    def outcomes(k):
        if sum(k) == m:
            return frozenset({k})
        children = [outcomes(tuple(n + int(b == a) for b, n in enumerate(k)))
                    for a in range(p)]
        floor = max(min(utility(c, a) for c in child) for a, child in enumerate(children))
        thresholds[k] = floor
        return frozenset(c for a, child in enumerate(children) for c in child
                         if utility(c, a) >= floor)

    root = (0,) * p
    result = outcomes(root)
    obstruction = []
    if path:
        k = root
        for a in path:
            child = tuple(n + int(b == a) for b, n in enumerate(k))
            if target not in outcomes(child) or utility(target, a) < thresholds[k]:
                obstruction.append({'prefix_counts': k, 'next_action': a,
                    'target_payoff': utility(target, a), 'credible_floor': thresholds[k],
                    'target_in_selected_child': target in outcomes(child)})
            k = child
    return {'root_target_reachable': target in result, 'root_outcomes': len(result),
            'count_states': outcomes.cache_info().currsize,
            'root_threshold': thresholds[root], 'onpath_obstructions': obstruction}


def serializable(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: serializable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serializable(v) for v in x]
    return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    p, m = args.topics, args.players
    moments = Moments(p, 2, m)
    portfolios = ((tuple(range(2, m + 2))), (0,) + tuple(range(2, m + 1)),
                  (0, 1) + tuple(range(2, m)))
    records = []
    for path in product(range(2), repeat=m):
        if path.count(0) != (m + 1) // 2:
            continue
        q = tuple(path.count(a) for a in range(p))
        w = moments.C(sum(1 << a for a, n in enumerate(q) if n))
        rows = tuple(sorted(set(moments.rows + moments.path_rows(path))))
        for J in portfolios:
            result = solve(rows, w, moments.C(sum(1 << a for a in J)))
            records.append({'path': path, 'portfolio': J, 'rows': len(rows), **result})
    certified = [r for r in records if r.get('certified')]
    best = max(certified, key=lambda r: r['value'])
    completion = spe_completion(moments, best['values'],
        tuple(best['path'].count(a) for a in range(p)), best['path'])
    out = {'scope': 'common monotone-submodular truncated moments, exchangeable unused labels; path necessary cuts only',
           'general_half_status': 'OPEN', 'moment_orbits': moments.keys,
           'records': records, 'best_path': best['path'], 'best_portfolio': best['portfolio'],
           'best_value': best['value'], 'best_exact_point_credible_completion': completion}
    args.output.write_text(json.dumps(serializable(out), indent=2) + '\n')
    print(json.dumps(serializable({k: v for k, v in out.items()
                                  if k not in ('records', 'moment_orbits')}), indent=2))


if __name__ == '__main__':
    main()
