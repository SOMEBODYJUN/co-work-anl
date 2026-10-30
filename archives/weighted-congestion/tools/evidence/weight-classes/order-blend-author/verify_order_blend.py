#!/usr/bin/env python3
"""Exact finite audits for the two-weight descending/ascending blend.

Resource audits use a fixed deterministic list; literal game audits use
the printed fixed seed.  Monomials include k=0.  Fractions perform every
cost/potential comparison; Decimal is used only to print the closed-form
irrational optimum, not for an asserted inequality.  This is finite
implementation evidence, not the proof of the all-real theorem.
"""
from fractions import Fraction as Q
from itertools import product
from decimal import Decimal, localcontext
import json
import sys
import random
import argparse
import hashlib
from pathlib import Path


def mono(x, k):
    return x ** k


def paths(a, b, m, n, k):
    down = sum((a * mono(j * a, k) for j in range(1, m + 1)), Q(0))
    down += sum((b * mono(m * a + j * b, k) for j in range(1, n + 1)), Q(0))
    up = sum((b * mono(j * b, k) for j in range(1, n + 1)), Q(0))
    up += sum((a * mono(n * b + j * a, k) for j in range(1, m + 1)), Q(0))
    return down, up


def game_audit():
    rng = random.Random(7102026)
    totals = {"games": 0, "states": 0, "deviations": 0, "local_minima": 0,
              "strict_alpha_improvements": 0}
    for d, root in [(3, 2), (7, 3), (13, 4)]:
        # d=q(q-1)+1 => optimal A_d=q and lambda=1/(q-1), all rational.
        assert root * root - root == d - 1
        lam, alpha = Q(1, root - 1), Q(root)
        for case in range(8):
            a, b = [(Q(7), Q(1)), (Q(5, 3), Q(2, 7))][case % 2]
            weights = [a, b, a, b]
            strategies = []
            for i in range(4):
                # include incomparable alternatives, empty, and retained-resource moves
                base = [frozenset(), frozenset({0, 1}), frozenset({1, 2})]
                extra = frozenset(e for e in range(4) if rng.randrange(2))
                strategies.append(tuple(dict.fromkeys(base + [extra])))
            coeff = []
            for e in range(4):
                if e == 3:
                    coeff.append([Q(0)] * (d + 1))  # identically zero resource
                else:
                    v = [Q(0)] * (d + 1)
                    v[0] = Q(rng.randrange(3))
                    v[1] = Q(rng.randrange(3))
                    v[d] = Q(rng.randrange(1, 4), rng.randrange(1, 4))
                    coeff.append(v)

            def inspect(state):
                counts = []
                loads = []
                for e in range(4):
                    m = sum(weights[i] == a and e in state[i] for i in range(4))
                    n = sum(weights[i] == b and e in state[i] for i in range(4))
                    counts.append((m, n))
                    loads.append(m*a+n*b)
                costs = [sum((sum((ck * loads[e]**k for k, ck in enumerate(coeff[e])), Q(0))
                              for e in state[i]), Q(0)) for i in range(4)]
                phi = Q(0)
                for e, (m, n) in enumerate(counts):
                    for k, ck in enumerate(coeff[e]):
                        down, up = paths(a, b, m, n, k)
                        phi += ck * (down + lam*up)
                return costs, phi

            states = list(product(*strategies))
            cache = {state: inspect(state) for state in states}
            for state in states:
                old_cost, old_phi = cache[state]
                is_local_minimum = True
                is_alpha_pne = True
                for i in range(4):
                    h = lam*a if weights[i] == a else (1+lam)*b
                    for action in strategies[i]:
                        new = state[:i] + (action,) + state[i+1:]
                        new_cost, new_phi = cache[new]
                        assert new_phi-old_phi <= h*(alpha*new_cost[i]-old_cost[i])
                        if new_phi < old_phi:
                            is_local_minimum = False
                        if old_cost[i] > alpha*new_cost[i]:
                            totals["strict_alpha_improvements"] += 1
                            is_alpha_pne = False
                            assert new_phi < old_phi
                        totals["deviations"] += 1
                if is_local_minimum:
                    assert is_alpha_pne
                    totals["local_minima"] += 1
            totals["games"] += 1
            totals["states"] += len(states)
    totals["seed"] = 7102026
    totals["degree_optimum_pairs"] = [[3, 2], [7, 3], [13, 4]]
    return totals


def run():
    pairs = [(Q(1), Q(1)), (Q(3, 2), Q(1)), (Q(2), Q(1)),
             (Q(13, 2), Q(2, 3)), (Q(1000), Q(1)),
             (Q(1), Q(1, 1000))]
    monomial_edges = 0
    blend_edges = 0
    worst_down_heavy = Q(1)
    worst_up_light = Q(1)
    for a, b in pairs:
        for k, m, n in product(range(0, 13), range(0, 7), range(0, 7)):
            down0, up0 = paths(a, b, m, n, k)
            for heavy in [False, True]:
                new_m, new_n = (m + 1, n) if heavy else (m, n + 1)
                down1, up1 = paths(a, b, new_m, new_n, k)
                w = a if heavy else b
                cost = mono(new_m * a + new_n * b, k)
                dd, du = down1 - down0, up1 - up0
                if heavy:
                    assert 0 <= dd <= a * cost
                    assert du == a * cost
                    worst_down_heavy = min(worst_down_heavy, dd / (a * cost))
                else:
                    assert dd == b * cost
                    assert b * cost <= du <= max(1, k) * b * cost
                    worst_up_light = max(worst_up_light, du / (b * cost))
                monomial_edges += 1
                # Rational lambdas establish the interval without rounding roots.
                for lam in [Q(1, 10), Q(1, 3), Q(1), Q(5)]:
                    d = max(1, k)
                    alpha = max((1 + lam) / lam, (1 + d * lam) / (1 + lam))
                    h = lam * a if heavy else (1 + lam) * b
                    delta = dd + lam * du
                    assert h * cost <= delta <= alpha * h * cost
                    blend_edges += 1
    optima = []
    with localcontext() as ctx:
        ctx.prec = 60
        for d in [2, 3, 4, 10, 100, 1000]:
            alpha = (Decimal(1) + Decimal(4*d - 3).sqrt()) / 2
            lam = Decimal(1) / (alpha - 1)
            # Algebraically exact relation to be separately certified with integers.
            # alpha^2-alpha=d-1.  Print a high-precision residual only diagnostically.
            optima.append({"d": d, "alpha": str(alpha), "lambda": str(lam),
                           "residual": str(alpha*alpha-alpha-(d-1))})
    return {"status": "pass", "python": sys.version.split()[0],
            "arithmetic": "Fraction; Decimal only display of algebraic constants",
            "weight_pairs": [[str(a), str(b)] for a, b in pairs],
            "degrees": [0, 12], "old_counts_each_type": [0, 6],
            "monomial_insertion_edges": monomial_edges,
            "blend_insertion_edges": blend_edges,
            "minimum_descending_heavy_normalized_marginal": str(worst_down_heavy),
            "maximum_ascending_light_normalized_marginal": str(worst_up_light),
            "literal_game_audit": game_audit(),
            "optima_display_only": optima,
            "scope": "finite insertion and explicitly listed four-player game enumerations; not general proof"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    report = run()
    if args.output:
        with open(args.output, "x", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
