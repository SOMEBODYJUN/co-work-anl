#!/usr/bin/env python3
"""Exact finite regression for WC-R1-MULTICOLUMN-2-v1; not a proof."""
from fractions import Fraction as Q
from itertools import product
from math import ceil
from pathlib import Path
import json


def poly(coeff):
    return lambda x: sum((a * x**k for k, a in enumerate(coeff)), Q(0))


def compositions(n, q):
    if q == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for tail in compositions(n - first, q - 1):
            yield (first,) + tail


def formulas(n, q, w, f, g):
    b, c, B = g(w), g(Q(1)), g(1 + w)
    A = lambda t: f(1 + t * w) + (q - 1) * b
    D = lambda t: f(t * w) + B + (q - 2) * b
    F = lambda t: f(1 + t * w) + (n - t) * B + t * c
    return A, D, F


def direct_costs(profile, n, q, w, f, g):
    strategies = []
    h = profile[0]
    strategies.append({(h, i) for i in range(n + 1)})
    for i, j in enumerate(profile[1:], 1):
        strategies.append({(j, 0)} | {(k, i) for k in range(q) if k != j})
    weights = [Q(1)] + [w] * n
    loads = {}
    for weight, strategy in zip(weights, strategies):
        for resource in strategy:
            loads[resource] = loads.get(resource, Q(0)) + weight
    costs = []
    for strategy in strategies:
        costs.append(sum((f(loads[r]) if r[1] == 0 else g(loads[r])
                          for r in strategy), Q(0)))
    return costs


def check_formulas():
    total = 0
    for q in (3, 4):
        for n in range(1, 4):
            for w in (Q(1, 3), Q(1)):
                f = poly([Q(1, 7), Q(2), Q(0), Q(1, 5)])
                g = poly([Q(1, 11), Q(1, 3), Q(2, 9)])
                A, D, F = formulas(n, q, w, f, g)
                for profile in product(range(q), repeat=n + 1):
                    counts = [profile[1:].count(j) for j in range(q)]
                    h = profile[0]
                    predicted = [F(counts[h])] + [
                        (A if j == h else D)(counts[j]) for j in profile[1:]]
                    assert direct_costs(profile, n, q, w, f, g) == predicted
                    for player in range(n + 1):
                        for target in range(q):
                            moved = list(profile)
                            moved[player] = target
                            cost = direct_costs(moved, n, q, w, f, g)[player]
                            if player == 0:
                                expected = F(counts[target])
                            elif target == profile[player]:
                                expected = predicted[player]
                            else:
                                expected = (A if target == h else D)(counts[target] + 1)
                            assert cost == expected
                    total += 1
    return total


def check_existence():
    families = [
        ([0], [0]),
        ([1], [0]),
        ([0, 1], [0, 0, 1]),
        ([0, 0, 0, 1], [0, 1]),
        ([Q(1, 7), 2, 0, Q(1, 5)], [Q(1, 11), Q(1, 3), Q(2, 9)]),
    ]
    cases = 0
    states = 0
    selected = 0
    for q in range(3, 7):
        for n in range(1, 8):
            for w in (Q(1, 10), Q(1, 2), Q(1)):
                for fc, gc in families:
                    f, g = poly(fc), poly(gc)
                    A, D, F = formulas(n, q, w, f, g)
                    bound = Q(2) if n == 1 else min(Q(2), max(
                        1 + Q(1, n), Q(n, n - ceil(Q(n, q - 1)))))
                    found = False
                    for counts in compositions(n, q):
                        states += 1
                        if max(counts[1:]) - min(counts[1:]) > 1:
                            continue
                        exact = True
                        for j, number in enumerate(counts):
                            if not number:
                                continue
                            current = (A if j == 0 else D)(number)
                            for target in range(q):
                                if target != j and current > (A if target == 0 else D)(counts[target] + 1):
                                    exact = False
                        if exact:
                            found = True
                            selected += 1
                            for u in counts[1:]:
                                assert F(counts[0]) <= 2 * F(u)
                                assert F(counts[0]) <= bound * F(u)
                    assert found
                    cases += 1
    return cases, states, selected


def check_sharpness():
    out = []
    for n in range(4, 13):
        d = n**3
        w = Q(1, n**2)
        beta = Q(1, 2) / (1 + w)**d
        b, B = beta * w**d, Q(1, 2)
        lower = Q(2 * n, n + 3)
        assert beta < Q(1, 2 * n)
        assert w + beta < B
        # All aligned profiles: current >= 1, deviation <= n*w+B+b.
        assert 1 > lower * (n * w + B + b)
        # All unaligned profiles: largest other occupancy u >= n/2.
        heavy_deviation_upper = 1 + Q(n, 4) + n * (w + beta) / 2
        assert 1 + n * B > lower * heavy_deviation_upper
        # Check every occupancy orbit against all deviation ratios as well.
        A, D, F = formulas(n, 3, w, poly([0, 1]), lambda x: beta * x**d)
        checked = 0
        for counts in compositions(n, 3):
            t = counts[0]
            if t:
                assert any(A(t) > lower * D(u + 1) for u in counts[1:])
            else:
                assert any(F(0) > lower * F(u) for u in counts[1:])
            checked += 1
        out.append({"n": n, "degree": d, "certified_no_alpha_pne_at": str(lower),
                    "occupancy_orbits": checked})
    return out


def main():
    formula_profiles = check_formulas()
    cases, states, selected = check_existence()
    result = {
        "claim": "WC-R1-MULTICOLUMN-2-v1",
        "arithmetic": "fractions.Fraction throughout; no tolerance comparisons",
        "direct_resource_formula_profiles": formula_profiles,
        "direct_formula_scope": "q=3,4; n=1,2,3; w=1/3,1; all pure profiles and all deviations",
        "existence_game_cases": cases,
        "occupancy_states_inspected": states,
        "balanced_light_equilibria_checked": selected,
        "existence_scope": "q=3..6; n=1..7; w=1/10,1/2,1; five polynomial pairs including zeros",
        "sharpness_checks": check_sharpness(),
        "status": "all exact assertions passed",
        "limitation": "finite regression only; general statements rely on RESULT.md proofs",
    }
    path = Path(__file__).with_name("evidence.json")
    if path.exists():
        raise SystemExit("Refusing to overwrite frozen evidence.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
