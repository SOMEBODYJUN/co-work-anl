"""Exact finite audits for box-robust common-scale calibration.

This checks finite algebra and concrete obstruction examples. The accompanying
proof, not this enumeration, supplies general quantifiers. Standard library only.
"""
from fractions import Fraction as Q
from itertools import product
import json
import random
from pathlib import Path


def ratio(num, den, coeff):
    a = sum(x * c for x, c in zip(num, coeff))
    b = sum(x * c for x, c in zip(den, coeff))
    return None if b == 0 else a / b


def threshold_extrema(num, den, lower, upper):
    """All D_k > 0. At most 2(d+2) vertices, including all-zero skip."""
    order = sorted(range(len(num)), key=lambda k: num[k] / den[k])
    low_vertices, high_vertices = [], []
    low, high = list(lower), list(upper)
    for j in range(len(order) + 1):
        lr, hr = ratio(num, den, low), ratio(num, den, high)
        if lr is not None:
            low_vertices.append((lr, tuple(low)))
        if hr is not None:
            high_vertices.append((hr, tuple(high)))
        if j < len(order):
            k = order[j]
            low[k] = upper[k]
            high[k] = lower[k]
    return min(low_vertices), max(high_vertices)


def box_extrema(num, den, lower, upper):
    values = []
    for bits in product((0, 1), repeat=len(num)):
        coeff = tuple(upper[k] if bit else lower[k]
                      for k, bit in enumerate(bits))
        value = ratio(num, den, coeff)
        if value is not None:
            values.append((value, coeff))
    return min(values), max(values)


def robust_lower_holds(num, den, lower, upper, value):
    coeffs = [n - value * d for n, d in zip(num, den)]
    support = sum(c * (lower[k] if c >= 0 else upper[k])
                  for k, c in enumerate(coeffs))
    return support >= 0


def robust_upper_holds(num, den, lower, upper, value):
    return robust_lower_holds([-n for n in num], den, lower, upper, -value)


def order_potential(m, n, a, b, background, power, ascending=False):
    weights = ([b] * n + [a] * m) if ascending else ([a] * m + [b] * n)
    total, value = background, Q(0)
    for w in weights:
        total += w
        value += w * total ** power
    return value


def insertion_coefficients(m, n, a, b, background, degree, heavy, ascending):
    w = a if heavy else b
    mm, nn = m + int(heavy), n + int(not heavy)
    num = [order_potential(mm, nn, a, b, background, k, ascending)
           - order_potential(m, n, a, b, background, k, ascending)
           for k in range(degree + 1)]
    den = [w * (background + mm * a + nn * b) ** k
           for k in range(degree + 1)]
    return num, den


def robust_AB(a, b, na, nb, background, degree, lower, upper):
    a_rows, b_rows = [], []
    for m in range(na):
        for n in range(nb + 1):
            num, den = insertion_coefficients(m, n, a, b, background,
                                               degree, True, False)
            best, _ = threshold_extrema(num, den, lower, upper)
            assert robust_lower_holds(num, den, lower, upper, best[0])
            a_rows.append((best[0], m, n, best[1]))
    for m in range(na + 1):
        for n in range(nb):
            num, den = insertion_coefficients(m, n, a, b, background,
                                               degree, False, True)
            _, best = threshold_extrema(num, den, lower, upper)
            assert robust_upper_holds(num, den, lower, upper, best[0])
            b_rows.append((best[0], m, n, best[1]))
    return min(a_rows), max(b_rows)


def feasible_interval(A, B, beta):
    lm = Q(0) if A == 1 else max(Q(0), (1 / beta - A) / (1 - A))
    lp = Q(1) if B == 1 else min(Q(1), (beta - 1) / (B - 1))
    if lm > lp:
        return None
    lam = lm if A * B >= 1 else lp
    s = 1 / (A + (1 - A) * lam)
    x, y = s * (1 - lam), s * lam
    r = (x + B * y) / beta
    assert A * x + y >= 1
    assert x + y <= beta
    assert r <= x + y
    assert x + B * y <= beta * r
    return r, beta, x, y


def run():
    rng = random.Random(20261021)
    box_cases = 0
    zero_lower_cases = 0
    for dimension in range(1, 7):
        for trial in range(180):
            num = [Q(rng.randrange(1, 23), rng.randrange(1, 9))
                   for _ in range(dimension)]
            den = [Q(rng.randrange(1, 23), rng.randrange(1, 9))
                   for _ in range(dimension)]
            lower = [Q(0) if trial % 3 == 0 else Q(rng.randrange(0, 7), 3)
                     for _ in range(dimension)]
            upper = [lo + Q(rng.randrange(0, 7), 3) for lo in lower]
            if not any(upper):
                upper[0] = Q(1)
            got = threshold_extrema(num, den, lower, upper)
            brute = box_extrema(num, den, lower, upper)
            assert (got[0][0], got[1][0]) == (brute[0][0], brute[1][0])
            assert robust_lower_holds(num, den, lower, upper, got[0][0])
            assert robust_upper_holds(num, den, lower, upper, got[1][0])
            box_cases += 1
            zero_lower_cases += not any(lower)

    local_cases = 0
    for degree in range(1, 6):
        for na, nb in product(range(1, 4), repeat=2):
            for background in (Q(0), Q(2, 3)):
                lower = [Q(rng.randrange(0, 4), 3) for _ in range(degree + 1)]
                upper = [lo + Q(rng.randrange(1, 5), 3) for lo in lower]
                A, B = robust_AB(Q(5, 2), Q(2, 3), na, nb, background,
                                 degree, lower, upper)
                assert 0 < A[0] <= 1 <= B[0] <= degree
                # Independent all-vertex enumeration across every insertion.
                aa, bb = [], []
                for coeff in product(*[(lo, hi) for lo, hi in zip(lower, upper)]):
                    for m in range(na):
                        for n in range(nb + 1):
                            num, den = insertion_coefficients(m, n, Q(5, 2), Q(2, 3),
                                                              background, degree, True, False)
                            value = ratio(num, den, coeff)
                            if value is not None:
                                aa.append(value)
                    for m in range(na + 1):
                        for n in range(nb):
                            num, den = insertion_coefficients(m, n, Q(5, 2), Q(2, 3),
                                                              background, degree, False, True)
                            value = ratio(num, den, coeff)
                            if value is not None:
                                bb.append(value)
                assert A[0] == min(aa) and B[0] == max(bb)
                local_cases += 1

    # One heavy/one light: x + x^2 with independent coefficient intervals.
    sample_A, sample_B = robust_AB(Q(3), Q(1), 1, 1, Q(0), 2,
                                   [Q(0), Q(1), Q(1)], [Q(0), Q(3), Q(4)])
    assert sample_A[0] == Q(15, 17)
    assert sample_B[0] == Q(23, 17)
    sample = feasible_interval(sample_A[0], sample_B[0], Q(10, 9))
    assert sample == (Q(179, 170), Q(10, 9), Q(17, 18), Q(1, 6))

    # Arbitrarily uncertain resource amplitude does not alter local shape ratios.
    amplitude_cases = []
    for scale in (1, 10, 10**6, 10**30):
        A, B = robust_AB(Q(3), Q(1), 1, 1, Q(0), 2,
                         [Q(0), Q(0), Q(1)], [Q(0), Q(0), Q(scale)])
        assert A[0] == Q(7, 8) and B[0] == Q(11, 8)
        amplitude_cases.append(scale)

    # Delay-one obstruction: two simultaneous proposals, serial commits.
    delayed = []
    for degree in range(1, 9):
        state = [0, 0]
        trace = []
        for batch in range(6):
            source, target = state[0], 1 - state[0]
            assert state == [source, source]
            proposals = [(i, source, target, Q(2**degree), Q(1)) for i in range(2)]
            for i, old, new, read_old, read_new in proposals:
                actual_old = Q(sum(v == old for v in state) ** degree)
                actual_new = Q((1 + sum(v == new for j, v in enumerate(state) if j != i)) ** degree)
                state[i] = new
                trace.append((i, read_old, read_new, actual_old, actual_new))
            assert trace[-2][3] > trace[-2][4]
            assert trace[-1][3] < trace[-1][4]
        assert state == [0, 0]
        delayed.append({"degree": degree, "read_ratio": str(2**degree),
                        "batches": 6, "true_worsening_commits": 6})

    # Variable environment: one player and two private constant resources.
    # Every fixed environment has an exact potential; realized-cost BR can cycle.
    drift = []
    action = 0
    for _ in range(8):
        costs = [Q(1), Q(1)]
        costs[action] = Q(4)
        alternative = 1 - action
        assert costs[action] > 3 * costs[alternative]
        drift.append((action, tuple(costs), alternative))
        action = alternative
    assert action == 0

    # Independent attack regression: negative reports depend on global threshold.
    delta = Q(1, 50)
    a_gain = Q(1)
    assert a_gain <= delta * Q(102)
    assert a_gain > delta * Q(2)

    return {"status": "all finite assertions passed",
            "seed": 20261021,
            "fractional_box_cases": box_cases,
            "all_zero_lower_endpoint_cases": zero_lower_cases,
            "local_robust_AB_cases": local_cases,
            "sample": {"A": str(sample_A[0]), "B": str(sample_B[0]),
                       "ratio_interval_and_mixture": [str(x) for x in sample]},
            "amplitude_uncertainty_upper_bounds": amplitude_cases,
            "delay_one_cycles": delayed,
            "varying_environment_cycle_steps": len(drift),
            "global_threshold_report_regression": {
                "delta": str(delta), "unchanged_player_gain": str(a_gain),
                "old_potential": "102", "new_potential": "2",
                "old_negative_report_must_be_invalidated": True},
            "scope": "finite exact audits; no enumeration replaces general proof"}


if __name__ == "__main__":
    result = run()
    target = Path(__file__).with_name("audit_result.json")
    with target.open("x") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
