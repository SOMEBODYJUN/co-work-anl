#!/usr/bin/env python3
"""Independent R3 review: exact certificate and literal resource deviations.

Python Fraction throughout; no floating-point acceptance decisions. The tiny
instance is fully enumerated. The huge family is checked through its proved
certificate, without pretending its astronomical state space was enumerated.
"""
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import argparse
import json


def normalized(u, v, n, k, degree, alpha):
    m = len(u)
    x = [v[i] / u[i] for i in range(m)]
    t = [v[i] / u[(i + 1) % m] for i in range(m)]
    nn = [(1 + x[i]) ** k[i] - alpha * (n[i] * x[i]) ** k[i]
          for i in range(m)]
    mm = [alpha * (1 + n[i] * x[i]) ** k[i] - 1 for i in range(m)]
    pp = [alpha * (1 + t[i]) ** degree - t[i] ** degree for i in range(m)]
    qq = [(1 + t[i]) ** degree - alpha for i in range(m)]
    gain = prod(F(n[i]) * nn[i] * qq[i] / (mm[i] * pp[i]) for i in range(m))
    return x, t, nn, mm, pp, qq, gain


def rational_coefficients(u, v, n, k, degree, alpha):
    """Construct strict rational coefficients with no algebraic-root step."""
    m = len(u)
    _, _, nn, mm, pp, qq, gain = normalized(u, v, n, k, degree, alpha)
    assert all(z > 0 for seq in (nn, mm, pp, qq) for z in seq)
    assert gain > 1
    lower = [pp[i] / nn[i] for i in range(m)]
    upper = [F(n[i - 1]) * qq[i - 1] / mm[i] for i in range(m)]
    factors = [upper[i] / lower[i] for i in range(m)]
    assert prod(factors) == gain
    big_b = [F(1)]
    partial = F(1)
    for i in range(1, m):
        partial *= factors[i]
        shrink = 1 - F(i, m) * (1 - 1 / gain)
        big_b.append(partial * shrink)
    big_a = [(lower[i] * big_b[i] + upper[i] * big_b[i - 1]) / 2
             for i in range(m)]
    assert all(big_a[i] * nn[i] > big_b[i] * pp[i] for i in range(m))
    assert all(n[i - 1] * big_b[i - 1] * qq[i - 1] > big_a[i] * mm[i]
               for i in range(m))
    a = [big_a[i] / u[i] ** k[i] for i in range(m)]
    b = [big_b[i] / u[(i + 1) % m] ** degree for i in range(m)]
    return a, b, gain


def literal_instance(u, v, n, k, degree, a, b):
    """Materialize exactly the stated resources and two strategies per player."""
    m = len(u)
    resources = {}
    for i in range(m):
        for bit in (0, 1):
            resources[("A", i, bit)] = (a[i], k[i])
        for j in range(n[i]):
            for bit in (0, 1):
                resources[("B", i, j, bit)] = (b[i], degree)
    players = []
    for i in range(m):
        strategies = []
        for bit in (0, 1):
            strategies.append((("A", i, bit),) + tuple(
                ("B", (i - 1) % m, j, bit) for j in range(n[i - 1])))
        players.append(("H", i, None, u[i], tuple(strategies)))
    for i in range(m):
        for j in range(n[i]):
            strategies = tuple((("A", i, bit), ("B", i, j, 1 - bit))
                               for bit in (0, 1))
            players.append(("L", i, j, v[i], strategies))
    return resources, players


def literal_costs(resources, players, state):
    loads = {resource: F(0) for resource in resources}
    for player, bit in zip(players, state):
        for resource in player[4][bit]:
            loads[resource] += player[3]
    return tuple(sum((resources[resource][0] * loads[resource] ** resources[resource][1]
                      for resource in player[4][bit]), F(0))
                 for player, bit in zip(players, state))


def exact_small_enumeration():
    # A small independently chosen instance exercises cohorts of size > 1.
    m, degree, alpha = 3, 10, F(11, 10)
    u, v, n, k = list(map(F, [32, 2, 8])), list(map(F, [1, 4, 16])), [3, 1, 1], [2, 10, 10]
    a, b, gain = rational_coefficients(u, v, n, k, degree, alpha)
    resources, players = literal_instance(u, v, n, k, degree, a, b)
    counts = {"states": 0, "states_with_aligned_light": 0, "all_anti_states": 0,
              "aligned_light_strict_checks": 0, "equal_edge_hub_strict_checks": 0,
              "unequal_edge_hub_nonimprovement_checks": 0,
              "literal_cost_formula_equalities": 0}
    for state in product((0, 1), repeat=len(players)):
        counts["states"] += 1
        old = literal_costs(resources, players, state)
        new = []
        for p in range(len(players)):
            moved = list(state)
            moved[p] ^= 1
            new.append(literal_costs(resources, players, tuple(moved))[p])
        aligned = [p for p, player in enumerate(players)
                   if player[0] == "L" and state[p] == state[player[1]]]
        if aligned:
            counts["states_with_aligned_light"] += 1
            for p in aligned:
                i = players[p][1]
                same_count = sum(state[q] == state[i] for q, player in enumerate(players)
                                 if player[0] == "L" and player[1] == i)
                next_same = state[(i + 1) % m] == state[i]
                formula_old = a[i] * (u[i] + same_count * v[i]) ** k[i] + b[i] * (
                    v[i] + (0 if next_same else u[(i + 1) % m])) ** degree
                formula_new = a[i] * ((n[i] - same_count + 1) * v[i]) ** k[i] + b[i] * (
                    v[i] + (u[(i + 1) % m] if next_same else 0)) ** degree
                assert old[p] == formula_old and new[p] == formula_new
                counts["literal_cost_formula_equalities"] += 2
                assert old[p] > alpha * new[p]
                counts["aligned_light_strict_checks"] += 1
        else:
            counts["all_anti_states"] += 1
            equal_edges = [i for i in range(m) if state[i] == state[(i - 1) % m]]
            assert equal_edges
            for i in range(m):
                equal = i in equal_edges
                formula_old = a[i] * u[i] ** k[i] + n[i - 1] * b[i - 1] * (
                    u[i] + (v[i - 1] if equal else 0)) ** degree
                formula_new = a[i] * (u[i] + n[i] * v[i]) ** k[i] + n[i - 1] * b[i - 1] * (
                    u[i] + (0 if equal else v[i - 1])) ** degree
                assert old[i] == formula_old and new[i] == formula_new
                counts["literal_cost_formula_equalities"] += 2
                if i in equal_edges:
                    assert old[i] > alpha * new[i]
                    counts["equal_edge_hub_strict_checks"] += 1
                else:
                    assert old[i] <= alpha * new[i]
                    counts["unequal_edge_hub_nonimprovement_checks"] += 1
        assert any(old[p] > alpha * new[p] for p in range(len(players)))
    return {"parameters": {"m": m, "degree": degree, "alpha": str(alpha),
                            "u": [str(z) for z in u], "v": [str(z) for z in v],
                            "n": n, "k": k},
            "resource_count": len(resources), "player_count": len(players),
            "certificate_gain": str(gain), "counts": counts,
            "alpha_PNE_count": 0, "status": "all assertions passed"}


def candidate_sample(s):
    r = 2 ** s
    m = s if s % 2 else s + 1
    degree, alpha = 2 * s * r, F(r, 4)
    u = [F(r ** (2 * m - 1))] + [F(r ** (2 * i - 1)) for i in range(1, m)]
    v = [F(1)] + [F(r ** (2 * i)) for i in range(1, m)]
    n = [r ** (2 * m - 1) // s] + [1] * (m - 1)
    k = [s] + [degree] * (m - 1)
    x, t, nn, mm, pp, qq, gain = normalized(u, v, n, k, degree, alpha)
    assert x[0] == F(1, r ** (2 * m - 1))
    assert all(x[i] == r for i in range(1, m))
    assert all(z == F(1, r) for z in t)
    assert prod(x) == prod(t)
    ee = (1 + F(1, r)) ** degree
    assert ee > r ** 2
    assert nn[0] > F(1, 2)
    assert mm[0] < 3 * alpha
    assert n[0] >= F(r ** (2 * m - 1), 2 * s)
    assert all(qq[i] / pp[i] > F(3, r) for i in range(m))
    assert all(nn[i] / mm[i] == qq[i] / pp[i] for i in range(1, m))
    assert gain == n[0] * nn[0] / mm[0] * (qq[0] / pp[0]) ** (2 * m - 1)
    assert gain > F(9 ** (m - 1), s * r) > F(r, 6 * s) > 1
    upper = F(16 ** m, s * (r - 4)) * (1 + x[0]) ** s
    assert gain < upper
    return {"s": s, "r": r, "m": m, "degree": degree, "alpha": str(alpha),
            "exceptional_cohort": n[0], "players": m + sum(n),
            "gain_floor": gain.numerator // gain.denominator,
            "proved_lower_bound": str(F(9 ** (m - 1), s * r)),
            "checks": "dimensionless rational certificate and all displayed bounds",
            "state_enumeration": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"arithmetic": "Python fractions.Fraction; exact comparisons",
              "independent_small_instance": exact_small_enumeration(),
              "candidate_family_samples": [candidate_sample(s) for s in (6, 7)]}
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
