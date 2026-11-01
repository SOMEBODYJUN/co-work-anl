"""Exploratory full-tree payoff transport; not a universal proof.

Every comparison edge uses the continuation of its actual ordered history.
Optional same-action dilution arcs are valid coordinatewise on every type.
The LP is a sufficient certificate in the free space of payoff vertices;
failure is not a counterexample to half coverage.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json
import random

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix


def compositions(n, p):
    if p == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for q in compositions(n - a, p - 1):
                yield (a,) + q


def counts(z, p):
    c = Counter(z)
    return tuple(c[i] for i in range(p))


def payoff(a, z, weights):
    return sum((F(w, sum(bool(mask & (1 << b)) for b in z))
                for mask, w in weights.items() if mask & (1 << a)), F(0))


def full_tree(m, p, weights, rng):
    sigma, leaves = {}, {}
    for depth in range(m - 1, -1, -1):
        for h in product(range(p), repeat=depth):
            alternatives = {a: h + (a,) if depth == m - 1 else leaves[h + (a,)]
                            for a in range(p)}
            values = {a: payoff(a, z, weights) for a, z in alternatives.items()}
            best = max(values.values())
            sigma[h] = rng.choice([a for a in range(p) if values[a] == best])
            leaves[h] = alternatives[sigma[h]]
    return sigma, leaves


def sharp_cost(a, q, r):
    """Smallest k with F(a,q) <= k F(a,r) on every nonempty type."""
    p = len(q)
    return max(F(sum(r[b] for b in range(p) if mask & (1 << b)),
                 sum(q[b] for b in range(p) if mask & (1 << b)))
               for mask in range(1, 1 << p) if mask & (1 << a))


def transport_lp(m, p, sigma, leaves, optimum, include_dilution=True):
    vertices = [(a, q) for q in compositions(m, p) for a in range(p) if q[a]]
    index = {v: i for i, v in enumerate(vertices)}
    columns, labels = [], []
    # Keep genuinely distinct ordered-history comparisons, even if graph edges repeat.
    for h, s in sigma.items():
        q = counts(leaves[h], p)
        for a in range(p):
            z = h + (a,) if len(h) == m - 1 else leaves[h + (a,)]
            source, target = index[a, counts(z, p)], index[s, q]
            if source != target:
                columns.append({source: F(-1), target: F(1)})
                labels.append(("real", h, a))
    if include_dilution:
        for i, (a, q) in enumerate(vertices):
            for j, (b, r) in enumerate(vertices):
                if a == b and i != j:
                    columns.append({i: F(-1), j: sharp_cost(a, q, r)})
                    labels.append(("dilution", (a, q), (b, r)))
    # Free coefficient target = beta * root welfare - portfolio coverage.
    root = counts(leaves[()], p)
    opt = counts(optimum, p)
    goal = np.zeros(len(vertices))
    for a in range(p):
        if opt[a]:
            goal[index[a, opt]] -= opt[a]
    beta_col = {}
    for a in range(p):
        if root[a]:
            beta_col[index[a, root]] = F(-root[a])
    columns.append(beta_col)
    labels.append(("beta",))
    row, col, data = [], [], []
    for j, column in enumerate(columns):
        for i, value in column.items():
            row.append(i); col.append(j); data.append(float(value))
    mat = csc_matrix((data, (row, col)), shape=(len(vertices), len(columns)))
    objective = np.zeros(len(columns)); objective[-1] = 1
    result = linprog(objective, A_ub=mat, b_ub=goal,
                     bounds=(0, None), method="highs")
    return result, vertices, columns, labels


def run(seed=1701, cases=50, m=3, p=3):
    rng = random.Random(seed)
    maximum = None
    failures = []
    for case in range(cases):
        weights = {mask: rng.randint(0, 8) for mask in range(1, 1 << p)}
        sigma, leaves = full_tree(m, p, weights, rng)
        portfolios = list(combinations_with_replacement(range(p), m))
        # Test every portfolio: valid theorem cannot assume which portfolio is optimal on the cone.
        for opt in portfolios:
            result, vertices, columns, labels = transport_lp(m, p, sigma, leaves, opt)
            value = result.fun if result.success else None
            item = {"case": case, "portfolio": opt, "beta": value,
                    "root": leaves[()], "weights": weights}
            if value is None or value > 2 + 1e-7:
                item["sigma"] = [[list(h), a] for h, a in sigma.items()]
                failures.append(item)
                return {"seed": seed, "cases_completed": case + 1, "m": m, "p": p,
                        "maximum": maximum, "failures": failures}
            if maximum is None or value > maximum["beta"]:
                maximum = item
    return {"seed": seed, "cases_completed": cases, "m": m, "p": p,
            "maximum": maximum, "failures": failures}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1701)
    parser.add_argument("--cases", type=int, default=50)
    parser.add_argument("--players", type=int, default=3)
    parser.add_argument("--topics", type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(run(args.seed, args.cases, args.players, args.topics), indent=2))
