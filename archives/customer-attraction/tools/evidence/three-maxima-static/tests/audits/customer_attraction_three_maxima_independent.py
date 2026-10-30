"""Independent Fraction audit of the three-maxima static seat budget.

No repository imports, LP solver, or floating arithmetic. A positive customer
mass may be multiplied by a common denominator to obtain unit-customer clones.
This checks the universal linear certificate and its sharp normalized LP value;
the all-history SPE superset-seat induction is a separate proof obligation.
"""

from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import random


def budget_certificate(n, a):
    """Minimum fractional cover of private and all pair Venn regions."""
    total = sum(a)
    maximum = max(a)
    bound = max(F(total), F(n + maximum), F(3 * n, 2))
    cap = bound - n
    assert all(F(x) <= cap for x in a)
    assert total <= bound <= 3 * cap
    y = list(map(F, a))
    remaining = bound - total
    for j in range(3):
        increase = min(remaining, cap - y[j])
        y[j] += increase
        remaining -= increase
    assert remaining == 0
    assert sum(y) == bound
    assert all(y[j] >= a[j] for j in range(3))
    assert all(y[j] + y[k] >= n for j in range(3) for k in range(j))
    assert sum(y) >= n
    return bound, tuple(y)


def quantities(weights, n, include_nu=True):
    w = tuple(weights[(1 << j) - 1] for j in range(3))
    v = tuple(sum(weights[mask - 1] for mask in range(1, 8)
                  if mask.bit_count() >= 2 and mask & (1 << j))
              for j in range(3))
    c = weights[6]
    nu = None
    if include_nu:
        seats = sorted((w[j] / k + v[j] / n
                        for j in range(3) for k in range(1, n + 1)), reverse=True)
        nu = seats[n - 1]
    return sum(weights), w, v, c, nu


def check_weights(weights, n):
    union, w, v, c, nu = quantities(weights, n)
    shifted = nu - c / n
    assert shifted >= 0
    if nu == 0:
        assert union == 0
        return
    e = tuple(sum(w[j] / k + v[j] / n > nu
                  for k in range(1, n + 1)) for j in range(3))
    assert sum(e) <= n - 1
    a = tuple(x + 1 for x in e)
    assert max(a) <= n
    bound, y = budget_certificate(n, a)
    fs = tuple(w[j] / a[j] + v[j] / n for j in range(3))
    fs_shifted = tuple(f - c / n for f in fs)
    assert all(f <= nu for f in fs)
    assert all(0 <= f <= shifted for f in fs_shifted)
    certificate = sum(y[j] * fs[j] for j in range(3))
    shifted_certificate = sum(y[j] * fs_shifted[j] for j in range(3))
    assert union <= certificate <= bound * nu <= 2 * n * nu
    assert union - c <= shifted_certificate <= bound * shifted <= 2 * n * shifted
    if shifted == 0:
        assert union == c


def normalized_primal_extreme(n, a, bound):
    """Construct an optimal primal for f_j(a_j)<=1, possibly zero regions."""
    weights = [F(0)] * 7
    if bound == sum(a):
        for j in range(3):
            weights[(1 << j) - 1] = F(a[j])
    elif bound == n + max(a):
        j = max(range(3), key=lambda j: a[j])
        weights[(1 << j) - 1] = F(a[j])
        pair = 7 ^ (1 << j)
        weights[pair - 1] = F(n)
    else:
        assert bound == F(3 * n, 2)
        for pair in (3, 5, 6):
            weights[pair - 1] = F(n, 2)
    union, w, v, _, _ = quantities(weights, n, include_nu=False)
    assert all(w[j] / a[j] + v[j] / n <= 1 for j in range(3))
    assert union == bound


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="Optional report path; omitted prints the report without saving it")
    parser.add_argument("--proof", type=Path,
                        help="Optional proof file whose SHA256 is recorded in the report")
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error(f"Refusing to overwrite existing report: {args.output}")
    proof = args.proof
    if proof is None:
        candidate = (Path(__file__).resolve().parents[2] / "research" / "current" /
                     "customer_attraction" / "three_maxima_bound.md")
        if candidate.exists():
            proof = candidate
    if proof is not None and not proof.is_file():
        parser.error(f"Proof file does not exist: {proof}")
    pattern_count = membership_count = primal_count = 0
    for n in range(2, 51):
        for e0 in range(n):
            for e1 in range(n - e0):
                for e2 in range(n - e0 - e1):
                    e = (e0, e1, e2)
                    a = tuple(x + 1 for x in e)
                    bound, y = budget_certificate(n, a)
                    assert sum(a) <= n + 2 <= 2 * n
                    assert bound <= 2 * n
                    assert all(F(x) <= n for x in y)
                    for mask in range(1, 8):
                        if mask.bit_count() == 1:
                            j = (mask.bit_length() - 1)
                            coeff = y[j] / a[j]
                        else:
                            coeff = sum(y[j] for j in range(3) if mask & (1 << j)) / n
                        assert coeff >= 1
                        membership_count += 1
                    normalized_primal_extreme(n, a, bound)
                    primal_count += 1
                    pattern_count += 1
    assert pattern_count == comb(53, 4) - comb(4, 4)

    exhaustive_weights = 0
    for n in range(2, 11):
        for weights_int in product(range(3), repeat=7):
            check_weights(tuple(map(F, weights_int)), n)
            exhaustive_weights += 1

    rng = random.Random(8043)
    rational_weights = 1000
    for _ in range(rational_weights):
        n = rng.randrange(2, 101)
        weights = tuple(F(rng.randrange(30), rng.randrange(1, 20)) for _ in range(7))
        check_weights(weights, n)

    sharpness_count = 0
    for n in range(2, 51):
        for multiplier in (n, n * n, n * n * n, 10**6):
            # B1 has nM private clients; B2 and B3 share nM clients and
            # have one private client each, so all three maxima are distinct.
            weights = (F(n * multiplier), F(1), F(0), F(1), F(0),
                       F(n * multiplier), F(0))
            union, w, v, c, nu = quantities(weights, n)
            assert c == 0
            assert nu == multiplier + 1
            assert union == 2 * n * multiplier + 2
            ratio = union / (n * nu)
            assert ratio < 2
            assert 2 - ratio == F(2 * n - 2, n * (multiplier + 1))
            check_weights(weights, n)
            sharpness_count += 1

    four_maxima_obstructions = 0
    for n in range(2, 51):
        # Four genuine distinct maxima: B1 is disjoint and private; among
        # B2,B3,B4 every pair has its own n distinct shared unit clients.
        regions = {1: F(2 * n), 6: F(n), 10: F(n), 12: F(n)}
        private = tuple(regions.get(1 << j, F(0)) for j in range(4))
        shared = tuple(sum(weight for mask, weight in regions.items()
                           if mask.bit_count() >= 2 and mask & (1 << j))
                       for j in range(4))
        seats = sorted((private[j] / k + shared[j] / n
                        for j in range(4) for k in range(1, n + 1)), reverse=True)
        nu = seats[n - 1]
        union = sum(regions.values())
        assert private == (2 * n, 0, 0, 0)
        assert shared == (0, 2 * n, 2 * n, 2 * n)
        assert nu == 2
        assert union == 5 * n > 4 * n == 2 * n * nu
        assert sum(value > nu for value in seats) == n - 1
        four_maxima_obstructions += 1

    report = {
        "status": "passed",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": hashlib.sha256(proof.read_bytes()).hexdigest() if proof else None,
        "scope": "Exact independent audit of static three-maxima budget; no SPE enumeration",
        "threshold_n_range": [2, 50],
        "threshold_patterns": pattern_count,
        "single_membership_linear_coefficients": membership_count,
        "normalized_primal_extremes": primal_count,
        "exhaustive_weight_n_range": [2, 10],
        "exhaustive_seven_region_integer_weight_cases": exhaustive_weights,
        "seeded_rational_weight_cases": rational_weights,
        "sharpness_integer_cases": sharpness_count,
        "four_maxima_scalar_obstruction_n_range": [2, 50],
        "four_maxima_scalar_obstruction_integer_cases": four_maxima_obstructions,
        "formula": "S=max(sum(a), n+max(a), 3n/2); U-c <= S*(nu-c/n) <= 2n*(nu-c/n)",
        "sharpness_family": "w1=nM, w2=w3=1, t23=nM, all other shared regions zero; nu=M+1 for M>n-1",
        "four_maxima_scalar_obstruction": "B1 private=2n; pair-only blocks B2B3,B2B4,B3B4=n each; nu=2 and U=5n>2n*nu=4n",
    }
    if args.output is not None:
        with args.output.open("x") as output_file:
            output_file.write(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
