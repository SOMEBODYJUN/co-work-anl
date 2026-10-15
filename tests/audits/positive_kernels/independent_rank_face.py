#!/usr/bin/env python3
"""Independent exact finite audit of positive Boolean kernel rank faces.

This program uses direct truth tables and finite differences, not manuscript
implementations.  Its only stdout output is one JSON object.  Finite checks do
not establish the universal or closure claims.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb, factorial
import json
from pathlib import Path
import sys


def submasks(mask):
    current = mask
    while True:
        yield current
        if not current:
            return
        current = (current - 1) & mask


def masks_of_size(mask, size):
    bits = [j for j in range(mask.bit_length()) if mask & (1 << j)]
    for selected in combinations(bits, size):
        yield sum(1 << j for j in selected)


def table(n, weights, support, exponent):
    values = [[Fraction(0) for _ in range(1 << n)] for _ in range(n)]
    for state in range(1 << n):
        load = sum((weights[j] for j in range(n)
                    if support & state & (1 << j)), Fraction(0))
        for i in range(n):
            if support & state & (1 << i):
                values[i][state] = load ** exponent if exponent else Fraction(1)
    return values


def unanimity_table(n, support):
    return [[Fraction(bool(support & (1 << i) and state & support == support))
             for state in range(1 << n)] for i in range(n)]


def difference(values, i, directions, background):
    return sum(((-1) ** (directions.bit_count() - part.bit_count())
                * values[i][background | part | (1 << i)]
                for part in submasks(directions)), Fraction(0))


def rank(values):
    n = len(values)
    full = (1 << n) - 1
    degrees = [directions.bit_count()
               for i in range(n)
               for directions in submasks(full ^ (1 << i))
               if difference(values, i, directions, 0)]
    # The zero vector has degree <= 0 for the statements audited here.
    return max(degrees, default=0)


def functionals(values, q):
    n = len(values)
    full = (1 << n) - 1
    top = Fraction(0)
    all_contexts = Fraction(0)
    bottom = Fraction(0)
    negative_difference = False
    for i in range(n):
        rest = full ^ (1 << i)
        for directions in masks_of_size(rest, q):
            complement = rest ^ directions
            top += difference(values, i, directions, complement)
            bottom += difference(values, i, directions, 0)
            for background in submasks(complement):
                value = difference(values, i, directions, background)
                all_contexts += value
                negative_difference |= value < 0
    return top, all_contexts, bottom, negative_difference


def elementary(weights, support, q):
    return sum((product(weights[j] for j in range(len(weights))
                        if chosen & (1 << j))
                for chosen in masks_of_size(support, q)), Fraction(0))


def product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def gamma_for_support(weights, support, q):
    m = support.bit_count()
    total = sum((weights[j] for j in range(len(weights))
                 if support & (1 << j)), Fraction(0))
    return factorial(q) * (m - q) * elementary(weights, support, q) / (m * total ** q)


def rational(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def main():
    failures = []
    counters = {"kernels": 0, "rank_checks": 0, "functional_checks": 0,
                "gap_checks": 0, "sharp_checks": 0,
                "monotonicity_checks": 0, "unanimity_checks": 0,
                "functional_norm_checks": 0}

    def check(condition, kind, **context):
        if not condition and len(failures) < 20:
            failures.append({"kind": kind, **context})

    for n in range(1, 6):
        full = (1 << n) - 1
        profiles = [[Fraction(1)] * n,
                    [Fraction(j + 1) for j in range(n)],
                    [Fraction(1, j + 1) for j in range(n)]]
        for profile_id, weights in enumerate(profiles):
            gammas = {q: min(gamma_for_support(weights, support, q)
                             for support in range(1, full + 1)
                             if support.bit_count() >= q + 1)
                      for q in range(1, n)}
            for support in range(1, full + 1):
                m = support.bit_count()
                last_ratios = {}
                for exponent in range(9):
                    values = table(n, weights, support, exponent)
                    counters["kernels"] += 1
                    actual_rank = rank(values)
                    expected_rank = min(exponent, m - 1)
                    counters["rank_checks"] += 1
                    context = {"n": n, "profile": profile_id,
                               "support": support, "k": exponent}
                    check(actual_rank == expected_rank, "rank", **context)
                    b = sum(values[i][full] for i in range(n))
                    total_norm = sum(map(sum, values), Fraction(0))
                    check(b > 0, "nonzero_kernel", **context)
                    for q in range(1, n + 1):
                        top, all_contexts, _, negative = functionals(values, q)
                        counters["functional_checks"] += 1
                        forbidden = m >= q + 1 and exponent >= q
                        check(not negative and (top > 0) == forbidden
                              and (all_contexts > 0) == forbidden,
                              "difference_sign_or_support", q=q, **context)
                        if forbidden:
                            ratio = top / b
                            local_gamma = gamma_for_support(weights, support, q)
                            counters["gap_checks"] += 1
                            check(ratio >= local_gamma >= gammas[q],
                                  "top_gap", q=q, **context)
                            check(all_contexts / total_norm >= gammas[q] / 2 ** (n - 1),
                                  "all_context_gap", q=q, **context)
                            if exponent == q:
                                counters["sharp_checks"] += 1
                                check(ratio == local_gamma, "sharp_at_k_q", q=q, **context)
                            if q in last_ratios:
                                counters["monotonicity_checks"] += 1
                                check(ratio >= last_ratios[q], "occupancy_monotonicity", q=q, **context)
                            last_ratios[q] = ratio
                unanimity = unanimity_table(n, support)
                for q in range(1, n + 1):
                    top, all_contexts, bottom, negative = functionals(unanimity, q)
                    expected = comb(m - 1, q) if q <= m - 1 else 0
                    counters["unanimity_checks"] += 1
                    check(not negative and top == m * expected
                          and all_contexts == m * expected * 2 ** (n - m),
                          "unanimity_functionals", n=n, support=support, q=q)
                    if m >= q + 2:
                        check(bottom == 0 and rank(unanimity) > q - 1,
                              "bottom_closure_counterexample", n=n, support=support, q=q)
        for q in range(1, n):
            coefficients = {}
            for i in range(n):
                rest = full ^ (1 << i)
                for directions in masks_of_size(rest, q):
                    background = rest ^ directions
                    for part in submasks(directions):
                        key = (i, background | part)
                        coefficients[key] = coefficients.get(key, 0) + (-1) ** (q - part.bit_count())
            counters["functional_norm_checks"] += 1
            check(sum(abs(value) for value in coefficients.values())
                  == n * comb(n - 1, q) * 2 ** q,
                  "functional_l1_norm", n=n, q=q)

    signed_tables = [table(2, [Fraction(1)] * 2, 3, k) for k in range(3)]
    signed = [[signed_tables[2][i][state] - 3 * signed_tables[1][i][state]
               + 3 * signed_tables[0][i][state] for state in range(4)] for i in range(2)]
    check(signed == signed_tables[0] and rank(signed) == 0,
          "signed_coefficient_counterexample")
    zero_weights = table(3, [Fraction(1), Fraction(0), Fraction(0)], 7, 2)
    check(rank(zero_weights) == 1, "zero_weight_counterexample")
    invalid_old_zero_example = table(3, [Fraction(1), Fraction(1), Fraction(0)], 7, 2)
    check(rank(invalid_old_zero_example) == 2,
          "rejected_old_zero_weight_example_has_rank_two")
    zero_kernel = table(2, [Fraction(0)] * 2, 3, 1)
    check(not any(map(any, zero_kernel)), "zero_kernel_boundary")
    negative_weights = table(2, [Fraction(1), Fraction(-1)], 3, 1)
    negative_top = functionals(negative_weights, 1)[0]
    check(rank(negative_weights) == 1 and negative_top == 0,
          "negative_weight_counterexample")
    near_boundary = []
    for denominator in (10, 100, 1000):
        weights = [Fraction(1), Fraction(1, denominator), Fraction(1, denominator)]
        near_boundary.append({"epsilon": f"1/{denominator}",
                              "q": 2,
                              "gamma": rational(gamma_for_support(weights, 7, 2))})
    reuse_weights = [Fraction(1), Fraction(2), Fraction(3)]
    reuse_linear = table(3, reuse_weights, 7, 1)
    reuse_bad = table(3, reuse_weights, 7, 2)
    reuse_pair = table(3, reuse_weights, 3, 4)
    reuse_low = [[reuse_linear[i][state] + reuse_pair[i][state] / 1000
                  for state in range(8)] for i in range(3)]
    reuse_full = [[reuse_low[i][state] + reuse_bad[i][state] / 100
                   for state in range(8)] for i in range(3)]
    reuse_gamma = gamma_for_support(reuse_weights, 7, 2)
    reuse_l = functionals(reuse_full, 2)[0]
    reuse_bad_mass = sum(reuse_bad[i][7] for i in range(3)) / 100
    check(rank(reuse_low) == 1 and rank(reuse_full) == 2
          and reuse_gamma == Fraction(11, 54)
          and reuse_l == Fraction(11, 50)
          and reuse_bad_mass == reuse_l / reuse_gamma == Fraction(27, 25),
          "actual_reuse_example")
    check(all(0 <= reuse_full[i][state] - reuse_low[i][state] <= reuse_bad_mass
              for i in range(3) for state in range(8)),
          "actual_reuse_coordinate_bound")
    parameters = {"n": [1, 2, 3, 4, 5], "k": list(range(9)),
                  "positive_weight_profiles": {
                      "ones": "w_j=1",
                      "ascending": "w_j=j for j=1,...,n",
                      "reciprocal": "w_j=1/j for j=1,...,n"},
                  "supports": "all nonempty subsets",
                  "q": "all integers 1,...,n; gap checks only q<=n-1",
                  "actual_reuse": "n=3,w=(1,2,3),C=K_all,1+K_all,2/100+K_pair12,4/1000,q=2",
                  "boundary_cases": ["signed n=2,w=(1,1),k=0,1,2",
                                     "zero n=3,w=(1,0,0),S=all,k=2",
                                     "rejected old zero n=3,w=(1,1,0),S=all,k=2 has rank 2",
                                     "zero n=2,w=(0,0),S=all,k=1",
                                     "negative n=2,w=(1,-1),S=all,k=1",
                                     "q=2,n=3,w=(1,1/d,1/d),d=10,100,1000"]}
    encoded_parameters = json.dumps(parameters, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")
    metadata = {"command": "python3 tests/audits/positive_kernels/independent_rank_face.py",
                "python_version": sys.version,
                "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                "input_sha256": sha256(encoded_parameters).hexdigest(),
                "input_hash_encoding": "UTF-8 JSON parameters, sort_keys=True, separators=(',',':')",
                "parameters": parameters, "seed": None,
                "precision": "fractions.Fraction; exact rational arithmetic",
                "rounding_error": "0"}
    output = {"audit": "independent_rank_face", "status": "pass" if not failures else "fail",
              "metadata": metadata,
              "arithmetic": "exact fractions", "scope": {"n": [1, 5], "k": [0, 8],
              "positive_weight_profiles_per_n": 3}, "counts": counters,
              "boundary_counterexamples": {
                  "signed_coefficients": "K_pair,2 - 3 K_pair,1 + 3 K_pair,0 = K_pair,0 for w=(1,1)",
                  "zero_weights": "n=3,w=(1,0,0),S=all,k=2 has rank 1 instead of 2",
                  "negative_weights": "n=2,w=(1,-1),S=all,k=1 has rank 1 and L_top,1=0",
                  "bottom_context": "unanimity on |S|>=q+2 has rank |S|-1 but all order-q bottom differences vanish",
                  "weight_uniformity_q_2": near_boundary},
              "actual_reuse": {"gamma": rational(reuse_gamma),
                               "L_q": rational(reuse_l),
                               "bad_mass": rational(reuse_bad_mass),
                               "low_rank": rank(reuse_low),
                               "full_rank": rank(reuse_full)},
              "failures": failures,
              "limitation": "Finite audit only; closure and universal claims require the separate proof."}
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
