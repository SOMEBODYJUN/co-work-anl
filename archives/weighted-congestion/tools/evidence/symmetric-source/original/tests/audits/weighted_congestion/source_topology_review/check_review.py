#!/usr/bin/env python3
"""Independent exact state oracle and reduction-interface checks; finite evidence only."""
from fractions import Fraction as Q
from itertools import product
from math import comb
import json
import random
from pathlib import Path


def value(poly, x):
    return sum((c * x ** k for k, c in poly.items()), Q(0))


def translate(poly, shift):
    result = {}
    for k, c in poly.items():
        for j in range(k + 1):
            result[j] = result.get(j, Q(0)) + c * comb(k, j) * shift ** (k - j)
    return {k: c for k, c in result.items() if c}


def scale(poly, factor):
    return {k: c * factor ** k for k, c in poly.items() if c}


def literal_costs(n, w, F, G, state):
    # heavy: 0 = A; light: 0 = {a0,bi}, 1 = {b0,ai}
    def strategies(player, action):
        if player == 0:
            return [(action, j) for j in range(n + 1)]
        return [(0, 0), (1, player)] if action == 0 else [(1, 0), (0, player)]
    weights = [Q(1)] + [w] * n
    loads = {(side, j): Q(0) for side in (0, 1) for j in range(n + 1)}
    for player, action in enumerate(state):
        for e in strategies(player, action):
            loads[e] += weights[player]
    current, deviated = [], []
    for player, action in enumerate(state):
        current.append(sum((value(F if j == 0 else G, loads[side, j])
                            for side, j in strategies(player, action)), Q(0)))
        changed = loads.copy()
        for e in strategies(player, action):
            changed[e] -= weights[player]
        for e in strategies(player, 1 - action):
            changed[e] += weights[player]
        deviated.append(sum((value(F if j == 0 else G, changed[side, j])
                             for side, j in strategies(player, 1 - action)), Q(0)))
    return current, deviated


def strict_tests(n, w, F, G, alpha):
    return (value(F, Q(1)) + n * value(G, 1 + w)
            > alpha * (value(F, 1 + n * w) + n * value(G, Q(1)))
            and value(F, 1 + w) + value(G, w)
            > alpha * (value(F, n * w) + value(G, 1 + w)))


def to_source(n, w, F, G, alpha, d):
    assert strict_tests(n, w, F, G, alpha)
    if w > 1:
        assert n == 1
        F, G, w = scale(G, w), scale(F, w), 1 / w
        assert strict_tests(n, w, F, G, alpha)
    assert 0 < w <= 1
    v, u = value(G, 1 + w), value(G, Q(1))
    assert v > 0 and d >= 1
    E = (1 + w) ** d
    lam = (u / v - 1 / E) / (1 - 1 / E)
    assert 0 <= lam < 1
    chord_G = {0: v * lam, d: v * (1 - lam) / E}
    assert value(chord_G, Q(1)) == u
    assert value(chord_G, 1 + w) == v
    assert value(chord_G, w) >= value(G, w)
    assert strict_tests(n, w, F, chord_G, alpha)
    reduced_G = {d: chord_G[d]}
    assert strict_tests(n, w, F, reduced_G, alpha)
    assert E > alpha
    for k in F:
        if k == 0:
            continue
        lower = (alpha * (1 + n * w) ** k - 1) / (n * (E - alpha))
        upper = ((1 + w) ** k - alpha * (n * w) ** k) / (alpha * E - w ** d)
        if lower < upper:
            beta = (lower + upper) / 2
            assert 0 < beta < 1
            assert strict_tests(n, w, {k: Q(1)}, {d: beta}, alpha)
            return
    raise AssertionError("No monomial survived the positive linear functional")


def check_game(n, w, F, G, alpha, counts):
    u, v, z = value(G, Q(1)), value(G, 1 + w), value(G, w)
    def h(m):
        return value(F, 1 + m * w) + m * u + (n - m) * v
    stable = []
    formula_pne = []
    for m in range(n + 1):
        x_ok = m == 0 or value(F, 1 + m * w) + z <= alpha * (value(F, (n - m + 1) * w) + v)
        y_ok = m == n or value(F, (n - m) * w) + v <= alpha * (value(F, 1 + (m + 1) * w) + z)
        if x_ok and y_ok:
            stable.append(m)
            if h(m) <= alpha * h(n - m):
                formula_pne.append(m)
    literal_pne = []
    for state in product((0, 1), repeat=n + 1):
        curr, dev = literal_costs(n, w, F, G, state)
        m = sum(s == state[0] for s in state[1:])
        # For heavy B, "same-column main" light action is 1.
        assert curr[0] == h(m) and dev[0] == h(n - m)
        for player in range(1, n + 1):
            if state[player] == state[0]:
                assert curr[player] == value(F, 1 + m * w) + z
                assert dev[player] == value(F, (n - m + 1) * w) + v
            else:
                assert curr[player] == value(F, (n - m) * w) + v
                assert dev[player] == value(F, 1 + (m + 1) * w) + z
        if all(c <= alpha * t for c, t in zip(curr, dev)):
            literal_pne.append(state)
        counts["literal_states"] += 1
    assert bool(literal_pne) == bool(formula_pne)
    assert stable == list(range(stable[0], stable[-1] + 1))
    if formula_pne:
        return
    counts["no_pne"] += 1
    a, b = stable[0], stable[-1]
    assert set(stable).isdisjoint(n - m for m in stable)
    if 2 * b < n:
        counts["left_no_pne"] += 1
        N, FF = n - 2 * b, translate(F, b * w)
        assert strict_tests(N, w, FF, G, alpha)
        to_source(N, w, FF, G, alpha, max(F.keys() | G.keys(), default=0))
    else:
        assert 2 * a > n
        counts["right_no_pne"] += 1
        N, FF = 2 * a - n, translate(F, (n - a) * w)
        A, B, C = value(FF, Q(1)), value(FF, 1 + N * w), value(FF, w)
        assert B + N * u > alpha * (A + N * v)
        assert C + v > alpha * (B + z)
        assert N * alpha * (alpha - 1) < 1
        # All tested alpha satisfy alpha >= rho, equivalently alpha(alpha-1)>=1/2.
        assert alpha * (alpha - 1) >= Q(1, 2)
        assert N == 1
        reflected_F, reflected_G = scale(FF, w), scale(G, w)
        assert strict_tests(1, 1 / w, reflected_F, reflected_G, alpha)
        to_source(1, 1 / w, reflected_F, reflected_G, alpha, max(F.keys() | G.keys(), default=0))


def main():
    rng = random.Random(314159)
    counts = {"games": 0, "literal_states": 0, "no_pne": 0,
              "left_no_pne": 0, "right_no_pne": 0}
    cases = []
    weights = [Q(1, 100), Q(1, 2), Q(1), Q(3, 2), Q(10)]
    for _ in range(240):
        d, n = rng.randrange(7), rng.randrange(1, 5)
        F = {k: Q(rng.randrange(4), rng.randrange(1, 4)) for k in range(d + 1)}
        G = {k: Q(rng.randrange(4), rng.randrange(1, 4)) for k in range(d + 1)}
        F, G = ({k: c for k, c in p.items() if c} for p in (F, G))
        cases.append((n, rng.choice(weights), F, G))
    for w in weights:
        for F, G in (({}, {}), ({}, {3: Q(1)}), ({3: Q(1)}, {}),
                     ({0: Q(1)}, {3: Q(1)}), ({3: Q(1)}, {0: Q(1)})):
            cases.append((3, w, F, G))
    # An intentionally strong left certificate (n=5); no random discovery claim.
    d, w = 400, Q(1, 100)
    cases.append((5, w, {1: Q(1)}, {d: Q(3, 10) / (1 + w) ** d}))
    # Nontrivial chord/constant deletion and F coefficient elimination.
    cases.append((5, w, {0: Q(1, 100), 1: Q(1), 2: Q(1, 100)},
                  {0: Q(1, 1000), 3: Q(1, 1000),
                   d: Q(3, 10) / (1 + w) ** d}))
    # At alpha=3/2 the stable interval ends at b=1, exercising nonzero translation.
    cases.append((4, w, {1: Q(1)}, {d: Q(127, 200) / (1 + w) ** d}))
    # The reflected n=1 certificate exercises the right branch below phi.
    beta = Q(3, 5) / (1 + w) ** d
    cases.append((1, 1 / w, {1: w}, {d: beta * w ** d}))
    for n, w, F, G in cases:
        for alpha in (Q(7, 5), Q(3, 2), Q(5, 3), Q(2), Q(3)):
            check_game(n, w, F, G, alpha, counts)
            counts["games"] += 1
    result = {"status": "pass", "arithmetic": "fractions.Fraction",
              "seed": 314159, "alpha_values": ["7/5", "3/2", "5/3", "2", "3"],
              "scope": "finite independent literal-state and polynomial-reduction checks",
              **counts}
    target = Path(__file__).with_name("review_results.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
