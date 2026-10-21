#!/usr/bin/env python3
"""Explicit finite audits; the companion text proves the all-m statement."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import json
import random


def setup(m):
    x = (1 << (m - 1)) - 1
    y = x << (m - 1)
    u, v = 1 << (2 * m - 2), 1 << (2 * m - 1)
    return 2 * m, (x | u, x | v, y | u, y | v), (1, 1, 1, -1)


def character(b, e):
    return 1 if (b & e).bit_count() % 2 == 0 else -1


def all_submasks(mask):
    a = mask
    while a:
        yield a
        a = (a - 1) & mask


def explicit_audit(m):
    p, edges, signs = setup(m)
    ntypes = 1 << p
    weights, fvalues = [], []
    for b in range(ntypes):
        terms = [s * character(b, e) for s, e in zip(signs, edges)]
        prod = 1
        for t in terms:
            prod *= t
        assert prod == -1
        total = sum(terms)
        assert total in (-2, 2)
        w, f = 1 + total, 1 - F(total, 2)
        assert w in (-1, 3) and f in (0, 2)
        weights.append(w)
        fvalues.append(f)
    assert fvalues[0] == 0
    assert sum(weights) == ntypes
    assert sum(w * f for w, f in zip(weights, fvalues)) == -ntypes
    assert weights.count(-1) == weights.count(3) == ntypes // 2

    marginal_checks = 0
    covers = {}
    for k in range(m + 1):
        for dlabels in combinations(range(p), k):
            d = sum(1 << a for a in dlabels)
            marginal = defaultdict(int)
            for b, w in enumerate(weights):
                marginal[b & d] += w
            contained = [i for i, e in enumerate(edges) if e & d == e]
            assert len(contained) <= 1
            scale = 1 << (p - k)
            for a, value in marginal.items():
                predicted = scale * (1 + sum(signs[i] * character(a, edges[i])
                                               for i in contained))
                assert value == predicted and value >= 0
                if k < m:
                    assert value == scale
                marginal_checks += 1
            assert sum(marginal.values()) == ntypes
            covers[d] = sum(value for a, value in marginal.items() if a)
    q = F(0)
    for e, sign in zip(edges, signs):
        for t in all_submasks(e):
            k = t.bit_count()
            q += sign * (-1) ** (m + k) * 2 ** (k - 1) * covers[t]
    assert q == -ntypes

    # Verify the row equality on every full Boolean type, independently of w.
    for b, f in enumerate(fvalues):
        row = 0
        for e, sign in zip(edges, signs):
            for t in all_submasks(e):
                k = t.bit_count()
                row += sign * (-1) ** (m + k) * 2 ** (k - 1) * bool(t & b)
        assert row == f

    rng = random.Random(3300 + m)
    for _ in range(24):
        qcounts = [0] * p
        for _ in range(m):
            qcounts[rng.randrange(p)] += 1
        occupied = [a for a, q in enumerate(qcounts) if q]
        support = sum(1 << a for a in occupied)
        for a in occupied:
            explicit = sum((F(w, sum(qcounts[c] for c in occupied if b >> c & 1))
                            for b, w in enumerate(weights) if b >> a & 1), F(0))
            uniform = sum((F(1, sum(qcounts[c] for c in occupied if b >> c & 1))
                           for b in range(ntypes) if b >> a & 1), F(0))
            predicted = uniform
            if support in edges:
                assert len(occupied) == m and all(qcounts[c] == 1 for c in occupied)
                predicted -= F(signs[edges.index(support)] * (1 << (p - m)), m)
            assert explicit == predicted
    return {"m": m, "types": ntypes, "marginal_entries_checked": marginal_checks,
            "nonnegative_separating_row_value": str(q),
            "local_marginals": "nonnegative", "all_lower_degree_moments": "uniform"}


def bi_audit(m):
    p, edges, signs = setup(m)
    mass = 1 << p
    actions = {}

    @lru_cache(None)
    def payoffs(q, signed):
        occupied = [a for a in range(p) if q[a]]
        k = len(occupied)
        ans = [F(0)] * p
        for b in range(1 << k):
            load = sum(q[a] for j, a in enumerate(occupied) if b >> j & 1)
            if load:
                for j, a in enumerate(occupied):
                    if b >> j & 1:
                        ans[a] += F(1 << (p - k), load)
        support = sum(1 << a for a in occupied)
        if signed and k == m and support in edges:
            corr = F(signs[edges.index(support)] * (1 << (p - m)), m)
            for a in occupied:
                ans[a] -= corr
        return tuple(ans)

    def inc(q, a):
        return q[:a] + (q[a] + 1,) + q[a + 1:]

    @lru_cache(None)
    def solve(q):
        if sum(q) == m:
            return q
        children = [solve(inc(q, a)) for a in range(p)]
        vals = [payoffs(children[a], True)[a] for a in range(p)]
        a = max(range(p), key=lambda a: (vals[a], -a))
        assert q[a] == 0  # Strong all-new conclusion, at every count-state.
        actions[q] = a
        return children[a]

    root = solve((0,) * p)
    rowchecks = 0
    for q, chosen in actions.items():
        terminal = solve(inc(q, chosen))
        signed_actual = payoffs(terminal, True)[chosen]
        uniform_actual = payoffs(terminal, False)[chosen]
        for a in range(p):
            alternate = solve(inc(q, a))
            assert signed_actual >= payoffs(alternate, True)[a]
            assert uniform_actual >= payoffs(alternate, False)[a]
            rowchecks += 1
    support = sum(1 << a for a in range(p) if root[a])
    assert support == edges[3]
    assert sum(payoffs(root, True)[a] * root[a] for a in range(p)) == mass
    assert sum(payoffs(root, False)[a] * root[a] for a in range(p)) == mass - (1 << (p - m))
    am = F(m - 2, m * (m - 1)) + F(1, (1 << (m - 1)) * m * (m - 1))
    bm = F(1, m) - F(1, m * (1 << (m - 1)))
    gap = F(1, m * (m - 1)) - F(1, (m - 1) * (1 << (m - 1)))
    assert bm - am == gap and gap > 0
    return {"m": m, "decision_count_states": len(actions),
            "signed_and_true_uniform_comparisons_each": rowchecks,
            "all_actions_new": True, "new_vs_old_minimum_gap_normalized": str(gap),
            "signed_root_coverage": mass,
            "true_uniform_same_graph_root_coverage": mass - (1 << (p - m))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"status": "passed",
              "explicit_type_audits": [explicit_audit(m) for m in range(3, 7)],
              "formal_bi_and_true_source_audits": [bi_audit(m) for m in range(3, 6)],
              "scope": "Signed global gluing obstruction, not a legal customer instance or a half counterexample."}
    if args.output:
        if args.output.exists():
            raise FileExistsError(args.output)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
