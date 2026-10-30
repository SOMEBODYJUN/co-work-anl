#!/usr/bin/env python3
"""Exact, finite audits for zero-preserving support distortion claims.

All arithmetic is rational; stdout is one JSON object. The general statements
require the accompanying mathematical proof. Finite checks do not prove them.
The quartic boundary examples have negative coefficients and lie outside MODEL.
"""

from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import random
import sys


SEED = 20261015


def text(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def poly_eval(coeff, x):
    value = F(0)
    for c in reversed(coeff):
        value = value * x + c
    return value


def values(original_weights, state):
    load = sum(w * bit for w, bit in zip(original_weights, state))
    return tuple(bit * load for bit in state)


def costs(weights, resources, state):
    """A resource is (tuple of users, tuple of ascending coefficients).

    Every resource is selected exactly by its users with label one.
    """
    answer = [F(0)] * len(weights)
    for users, coeff in resources:
        active = [i for i in users if state[i]]
        load = sum(weights[i] for i in active)
        fee = poly_eval(coeff, load)
        for i in active:
            answer[i] += fee
    return tuple(answer)


def pair_bound(m, epsilon, r):
    total = 1 + m * epsilon
    return F(m) * (1 + epsilon) / ((r - 1) * total + m * epsilon)


def full_bound(m, epsilon, r):
    total = 1 + m * epsilon
    return F(m) * total / ((r - 1) * total + m * m * epsilon)


def algebra_checks():
    count = 0
    nontrivial = 0
    for m in range(1, 21):
        for epsilon in (F(1, 1000), F(1, 10), F(1), F(2), F(10)):
            total = 1 + m * epsilon
            for r in range(1, m + 4):
                a = r - 1
                p = pair_bound(m, epsilon, r)
                q = full_bound(m, epsilon, r)
                # Rearrangement and exact numerator identity for P - Q.
                assert p * (a * total + m * epsilon) == m * (1 + epsilon)
                assert q * (a * total + m * m * epsilon) == m * total
                lhs = (1 + epsilon) * (a * total + m * m * epsilon)
                lhs -= total * (a * total + m * epsilon)
                rhs = (m - 1) * epsilon * (m - a * total)
                assert lhs == rhs
                if q > 1:
                    assert p >= q
                    nontrivial += 1
                # Effective support and trivial beta >= 1 are separate facts.
                assert pair_bound(m, epsilon, min(r, m + 1)) >= p
                count += 1
    return {"cases": count, "nontrivial_full_bounds": nontrivial,
            "checks": ["exact rearrangement", "P-Q numerator identity",
                       "P >= Q whenever Q > 1", "effective support cap"]}


def finite_epsilon_and_symmetric_checks():
    rows = []
    scale_cases = 0
    for r in range(1, 9):
        for kind, parameter in [("beta", F(1)), ("beta", F(3, 2)),
                                ("beta", F(2)), ("beta", F(10)),
                                ("A", F(1)), ("A", F(3, 2)),
                                ("A", F(2)), ("A", F(5))]:
            beta = parameter if kind == "beta" else parameter ** 2
            m = int(beta * (r - 1)) + 1
            assert m > beta * (r - 1)
            if beta * r == 1:
                assert r == 1 and beta == 1
                threshold = None
                epsilon = F(1)
            else:
                threshold = (m - beta * (r - 1)) / (m * (beta * r - 1))
                assert threshold > 0
                epsilon = threshold / 2
            bound = pair_bound(m, epsilon, r)
            assert bound > beta
            rows.append({"r": r, "kind": kind, "parameter": text(parameter),
                         "beta": text(beta), "m": m, "epsilon": text(epsilon),
                         "epsilon_upper_limit": None if threshold is None else text(threshold),
                         "pair_bound": text(bound)})
            if kind == "A":
                a = parameter
                for v in (F(0), F(1, 100), F(1), F(7)):
                    for c in (v / a, (v / a + a * v) / 2, a * v):
                        assert v / a <= c <= a * v
                        assert v <= a * c <= (a ** 2) * v
                        scale_cases += 1
    return {"finite_positive_rational_epsilon_cases": len(rows),
            "symmetric_scale_cases": scale_cases, "rows": rows}


def singleton_exact_boundary():
    rows = []
    states_checked = 0
    for m in (1, 2, 3, 5):
        for epsilon in (F(1, 1000), F(1, 10), F(1), F(2)):
            weights = (F(1),) + (epsilon,) * m
            total = sum(weights)
            resources = [((i,), (total,)) for i in range(m + 1)]
            beta = F(1)
            for state in product((0, 1), repeat=m + 1):
                target = values(weights, state)
                actual = costs(weights, resources, state)
                for v, c in zip(target, actual):
                    assert c >= v
                    if v:
                        beta = max(beta, c / v)
                    else:
                        assert c == 0
                states_checked += 1
            assert beta == total / min(weights)
            # A singleton-only game has each active cost independent of others;
            # comparing its smallest and largest target states forces this beta.
            rows.append({"m": m, "epsilon": text(epsilon),
                         "optimal_beta": text(beta),
                         "formula": "(1+m*epsilon)/min(1,epsilon)"})
    return {"states_checked": states_checked, "rows": rows}


def equal_weight_pair_boundary():
    rows = []
    states_checked = 0
    for n in range(2, 9):
        q_min = 1
        while 2 ** q_min < n:
            q_min += 1
        for q in (q_min, q_min + 1, q_min + 3):
            denominator = 2 ** q - 1
            private = 1 - F(n - 1, denominator)
            assert private >= 0
            resources = [((i,), (private,)) for i in range(n)]
            for pair in combinations(range(n), 2):
                coeff = [F(0)] * (q + 1)
                coeff[q] = F(1, denominator)
                resources.append((pair, tuple(coeff)))
            weights = (F(1),) * n
            for state in product((0, 1), repeat=n):
                assert costs(weights, resources, state) == values(weights, state)
                states_checked += 1
            bound = pair_bound(n - 1, F(1), 2)
            assert bound <= 1
            rows.append({"n": n, "degree": q, "private_constant": text(private),
                         "beta": "1", "support": 2, "pair_bound": text(bound)})
    return {"states_checked": states_checked, "rows": rows,
            "scope": "In MODEL: equal-weight exact pair decomposition; no universal support rigidity."}


def zero_marker_audit():
    states_checked = 0
    for m in (1, 2, 4):
        for epsilon in (F(1, 100), F(1), F(2)):
            n = m + 1
            weights = (F(1),) + (epsilon,) * m
            # Resource 0 is shared, resource 1+2*i+bit is private zero fee.
            strategies = [({1 + 2 * i}, {0, 2 + 2 * i}) for i in range(n)]
            for zero, one in strategies:
                assert zero and one and not zero & one
                assert not zero <= one and not one <= zero
            fees = [(F(0), F(1))] + [(F(0),)] * (2 * n)
            for state in product((0, 1), repeat=n):
                selected = [strategies[i][state[i]] for i in range(n)]
                loads = [sum(weights[i] for i in range(n) if e in selected[i])
                         for e in range(1 + 2 * n)]
                actual = tuple(sum(poly_eval(fees[e], loads[e]) for e in selected[i])
                               for i in range(n))
                assert actual == values(weights, state)
                states_checked += 1
    return {"states_checked": states_checked,
            "checks": ["actual loads including zero marker resources",
                       "nonempty distinct disjoint antichain actions",
                       "markers do not alter any state cost"]}


def nonnegative_coefficient_enumeration():
    rng = random.Random(SEED)
    rows = []
    states_checked = 0
    pair_charge_checks = 0
    full_charge_checks = 0
    for m in (1, 2, 3, 4):
        n = m + 1
        for epsilon in (F(1, 100), F(1, 3), F(2)):
            original = (F(1),) + (epsilon,) * m
            weight_lists = (
                ("equal", (F(1),) * n),
                ("increasing", tuple(F(2) ** i for i in range(n))),
                ("heavy_dominant", (F(100),) + tuple(F(i + 1, 100) for i in range(m))),
                ("heavy_lightest", (F(1, 100),) + tuple(F(i + 1) for i in range(m))),
            )
            for r in range(1, n + 1):
                for name, converted in weight_lists:
                    resources = [((i,), (F(rng.randint(1, 5), 7),)) for i in range(n)]
                    for size in range(1, r + 1):
                        for users in combinations(range(n), size):
                            degree = rng.choice((0, 1, 2, 3, 5))
                            coeff = [F(0)] * (degree + 1)
                            coeff[degree] = F(rng.randint(1, 5), rng.randint(1, 7))
                            resources.append((users, tuple(coeff)))
                    states = tuple(product((0, 1), repeat=n))
                    all_values = [(values(original, s), costs(converted, resources, s)) for s in states]
                    scale = max(v / c for target, actual in all_values
                                for v, c in zip(target, actual) if v)
                    beta = max(scale * c / v for target, actual in all_values
                               for v, c in zip(target, actual) if v)
                    assert beta >= 1
                    scaled = [(u, tuple(scale * c for c in cs)) for u, cs in resources]
                    for state in states:
                        target = values(original, state)
                        actual = costs(converted, scaled, state)
                        for v, c in zip(target, actual):
                            assert v <= c <= beta * v
                        states_checked += 1
                    all_one = (1,) * n
                    heavy_zero = (0,) + (1,) * m
                    full = costs(converted, scaled, all_one)
                    without_heavy = costs(converted, scaled, heavy_zero)
                    sum_pair_differences = F(0)
                    for i in range(1, n):
                        pair = tuple(int(j in (0, i)) for j in range(n))
                        singleton = tuple(int(j == i) for j in range(n))
                        sum_pair_differences += costs(converted, scaled, pair)[i]
                        sum_pair_differences -= costs(converted, scaled, singleton)[i]
                    assert sum_pair_differences <= (r - 1) * full[0]
                    assert m * (1 + epsilon - beta * epsilon) <= sum_pair_differences
                    pair_charge_checks += 1
                    sum_full_differences = sum(full[i] - without_heavy[i] for i in range(1, n))
                    assert sum_full_differences <= (r - 1) * full[0]
                    assert m * (1 + m * epsilon - beta * m * epsilon) <= sum_full_differences
                    full_charge_checks += 1
                    assert beta >= pair_bound(m, epsilon, r)
                    assert beta >= full_bound(m, epsilon, r)
                    rows.append({"m": m, "epsilon": text(epsilon), "r": r,
                                 "converted_weights": name,
                                 "beta": text(beta),
                                 "pair_bound": text(pair_bound(m, epsilon, r))})
    return {"seed": SEED, "games_checked": len(rows),
            "states_checked": states_checked, "pair_charge_checks": pair_charge_checks,
            "full_charge_checks": full_charge_checks, "degree_choices": [0, 1, 2, 3, 5],
            "rows": rows}


def arbitrary_nonnegative_quartic_boundary():
    rows = []
    states_checked = 0
    for m in (1, 2, 3, 5):
        for epsilon in (F(1, 1000), F(1, 10), F(1), F(2)):
            original = (F(1),) + (epsilon,) * m
            converted = tuple(F(2) ** i for i in range(m + 1))
            directed = []
            for i in range(m + 1):
                for j in range(m + 1):
                    if i == j:
                        continue
                    a, b = converted[i], converted[j]
                    scalar = original[j] / ((a - b) ** 2 * b ** 2)
                    first = (b * b, -2 * b, F(1))
                    second = ((a + b) ** 2, -2 * (a + b), F(1))
                    coeff = tuple(scalar * x for x in poly_mul(first, second))
                    assert len(coeff) == 5 and coeff[4] > 0
                    assert any(c < 0 for c in coeff)
                    assert poly_eval(coeff, a) == original[j]
                    assert poly_eval(coeff, b) == 0
                    assert poly_eval(coeff, a + b) == 0
                    directed.append((i, j, coeff))
            for state in product((0, 1), repeat=m + 1):
                actual = [original[i] * state[i] for i in range(m + 1)]
                for i, j, coeff in directed:
                    # e_ij is selected by i at label 1 and j at label 0.
                    load = converted[i] * state[i] + converted[j] * (1 - state[j])
                    fee = poly_eval(coeff, load)
                    assert fee >= 0
                    if state[i]:
                        actual[i] += fee
                    if not state[j]:
                        actual[j] += fee
                assert tuple(actual) == values(original, state)
                states_checked += 1
            rows.append({"m": m, "epsilon": text(epsilon),
                         "converted_weights": [text(x) for x in converted],
                         "support": 2, "degree": 4, "beta": "1",
                         "pair_bound_at_r_2": text(pair_bound(m, epsilon, 2))})
    return {"states_checked": states_checked, "rows": rows,
            "scope": "Outside MODEL: globally nonnegative quartics with negative coefficients.",
            "global_nonnegativity_certificate":
            "w_j*(x-b)^2*(x-a-b)^2/((a-b)^2*b^2), where a,b>0 and a!=b"}


def main():
    answer = {"status": "passed", "arithmetic": "fractions.Fraction",
              "reproducibility": {"python_version": sys.version,
                                  "command": [sys.executable] + sys.argv,
                                  "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                  "random_seed": SEED,
                                  "precision": "exact rational; no floating point tolerance"},
              "scope": "Finite exact audits only; the universal inequalities need their written proof.",
              "algebra": algebra_checks(),
              "finite_epsilon_and_symmetric": finite_epsilon_and_symmetric_checks(),
              "r_1_exact_boundary": singleton_exact_boundary(),
              "equal_weight_pair_boundary": equal_weight_pair_boundary(),
              "zero_markers": zero_marker_audit(),
              "nonnegative_coefficient_games": nonnegative_coefficient_enumeration(),
              "arbitrary_nonnegative_quartic_boundary": arbitrary_nonnegative_quartic_boundary()}
    print(json.dumps(answer, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
