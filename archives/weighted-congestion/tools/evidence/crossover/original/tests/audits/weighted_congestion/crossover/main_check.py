#!/usr/bin/env python3
"""Second reconstruction: explicit strategies, and direct leaf sign checks.

This does not import either candidate verifier. Run from any directory.
All comparisons are integer/Fraction comparisons; decimals are diagnostic.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, lcm
from pathlib import Path
import json

if not __debug__:
    raise RuntimeError("Do not run with -O")

BASE = Path(__file__).resolve().parent
WEIGHTS = (F(1), F(1, 10), F(1, 20), F(1, 50))
PAIRS = ("0101", "0112", "1022", "1100", "1120", "1122", "1211")
AMPLITUDES = (127, 231, 145, 139, 28, 41, 289)


def literal_game(high_degree=32):
    strategies = [[set(), set()] for _ in WEIGHTS]
    resources = []
    for j, pattern in enumerate(PAIRS):
        support = tuple(i for i, ch in enumerate(pattern) if ch != "0")
        total = sum(WEIGHTS[i] for i in support)
        degree = high_degree if j < 6 else 2
        for side in (0, 1):
            index = len(resources)
            resources.append((F(AMPLITUDES[j]) / total**degree, degree, total))
            for i in support:
                action = (int(pattern[i]) - 1) ^ side
                strategies[i][action].add(index)
    return strategies, resources


def literal_costs(state, strategies, resources, limiting=False):
    loads = [F(0) for _ in resources]
    for i, action in enumerate(state):
        for e in strategies[i][action]:
            loads[e] += WEIGHTS[i]
    fees = [((coefficient * capacity**degree if loads[e] == capacity else F(0))
             if limiting and degree > 2 else coefficient * loads[e]**degree)
            for e, (coefficient, degree, capacity) in enumerate(resources)]
    return tuple(sum((fees[e] for e in strategies[i][action]), F(0))
                 for i, action in enumerate(state))


def check_game():
    strategies, resources = literal_game()
    certificate = json.loads((BASE / "degree32_certificate.json").read_text())
    rows = {row["state"]: row for row in certificate["records"]}
    best = {}
    for state in product((0, 1), repeat=4):
        key = "".join(map(str, state))
        current = literal_costs(state, strategies, resources)
        alternatives = []
        for i in range(4):
            target = list(state)
            target[i] ^= 1
            alternatives.append(literal_costs(target, strategies, resources)[i])
        assert tuple(F(x) for x in rows[key]["current_costs_exact"]) == current
        assert tuple(F(x) for x in rows[key]["deviation_costs_exact"]) == tuple(alternatives)
        ratios = tuple(current[i] / alternatives[i] for i in range(4))
        assert all(c > 0 for c in current + tuple(alternatives))
        best[key] = max(F(1), *ratios)
        assert best[key] > F(9, 5)
    value = min(best.values())
    assert str(value) == certificate["best_equilibrium_factor_exact"]
    assert [s for s in best if best[s] == value] == ["0110", "1001"]
    return {"states": len(best), "deviations": 4 * len(best),
            "factor_exact": str(value), "strict_9_over_5": True}


def check_fixed_failure():
    summaries = []
    for degree, limiting, filename in [
        (40, False, "degree40_failure_certificate.json"),
        (32, True, "fixed_weight_limit_certificate.json"),
    ]:
        strategies, resources = literal_game(degree)
        frozen = json.loads((BASE / filename).read_text())
        rows = {r["state"]: r for r in frozen["records"]}
        factors = []
        for state in product((0, 1), repeat=4):
            key = "".join(map(str, state))
            current = literal_costs(state, strategies, resources, limiting)
            target_costs = []
            for i in range(4):
                target = list(state)
                target[i] ^= 1
                target_costs.append(literal_costs(target, strategies, resources, limiting)[i])
            assert tuple(map(F, rows[key]["current_costs_exact"])) == current
            assert tuple(map(F, rows[key]["deviation_costs_exact"])) == tuple(target_costs)
            factors.append(max(F(1), *(current[i]/target_costs[i] for i in range(4))))
        value = min(factors)
        assert value == F(frozen["best_equilibrium_factor_exact"]) < F(9, 5)
        if limiting:
            assert value == F(5235403, 2930833)
        summaries.append({"degree": "limit" if limiting else degree,
                          "states": 16, "deviations": 64, "below_9_over_5": True})
    return summaries


def convolution(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i+j] += a[i] * b[j]
    return result


def elimination_polynomial(n, k):
    # Construct 2500 times the literal necessary strict margin.
    a = [50*comb(32, j) for j in range(33)]
    a[0] -= 89
    b = [50*comb(k, j) for j in range(k+1)]
    b[k] -= 89*n**k
    c = [89*comb(k, j)*n**j for j in range(k+1)]
    c[0] -= 50
    e = [89*comb(32, j) for j in range(33)]
    e[32] -= 50
    first, second = convolution(a, b), convolution(c, e)
    return [n*x-y for x, y in zip(first, second)]


def check_interval(poly, left, right):
    """Direct power-to-Bernstein transform on each leaf; no subdivision code."""
    degree = len(poly)-1
    denominator = lcm(left.denominator, right.denominator)
    left_integer = left.numerator*(denominator//left.denominator)
    width_integer = (right-left).numerator*(denominator//(right-left).denominator)
    # Affine-transform by accumulating one polynomial monomial at a time.
    transformed = [0]*(degree+1)
    for i, coefficient in enumerate(poly):
        for j in range(i+1):
            transformed[j] += (coefficient * comb(i, j) * left_integer**(i-j)
                               * width_integer**j * denominator**(degree-i))
    common = lcm(*(comb(degree, j) for j in range(degree+1)))
    for i in range(degree+1):
        coefficient = sum(transformed[j]*comb(i,j)*(common//comb(degree,j))
                          for j in range(i+1))
        assert coefficient < 0


def check_source():
    path = BASE.parent / "source32_bound" / "certificate.json"
    frozen = json.loads(path.read_text())
    assert F(56, 55)**32 < F(89, 50)
    expected = {(n, k) for n in range(1, 56) for k in range(1, 33)}
    leaves = 0
    for row in frozen["records"]:
        n, k = row["n"], row["k"]
        expected.remove((n, k))
        whole_left, whole_right = F(1, 55), F(1, max(1, n-1))
        poly = elimination_polynomial(n, k)
        intervals = []
        for leaf in row["leaves"]:
            code = leaf["path"]
            assert set(code) <= {"0", "1"}
            denominator = 2**len(code)
            numerator = int(code, 2) if code else 0
            left = whole_left+(whole_right-whole_left)*F(numerator, denominator)
            right = whole_left+(whole_right-whole_left)*F(numerator+1, denominator)
            check_interval(poly, left, right)
            intervals.append((left, right))
        intervals.sort()
        assert intervals[0][0] == whole_left and intervals[-1][1] == whole_right
        assert all(a[1] == b[0] for a,b in zip(intervals, intervals[1:]))
        leaves += len(intervals)
    assert not expected
    assert F(89, 50) < F(9, 5)
    return {"all_parameter_polynomials": len(frozen["records"]),
            "directly_checked_leaves": leaves, "source_upper": "89/50"}


if __name__ == "__main__":
    print(json.dumps({"game": check_game(), "fixed_failure": check_fixed_failure(),
                      "source": check_source()}, indent=2))
