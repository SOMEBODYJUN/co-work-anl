#!/usr/bin/env python3
"""Exact finite audit for PK rank faces; stdout only, immutable input contract.

This computes actual Boolean response tables, then independent transforms of
those tables. It does not replace the arbitrary-weight/degree proofs.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial, prod
from pathlib import Path
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / "examples/positive_kernels/rank_face_inputs.json"


def subsets(mask):
    value = mask
    while True:
        yield value
        if value == 0:
            break
        value = (value - 1) & mask


def table(weights, support, degree):
    n = len(weights)
    support = frozenset(support)
    rows = []
    for state in range(1 << n):
        load = sum((weights[j] for j in support if state >> j & 1), F())
        rows.append(tuple(load**degree if i in support and state >> i & 1 else F()
                          for i in range(n)))
    return rows


def transform(rows):
    n = len(rows[0])
    mobius = []
    for i in range(n):
        opposite = ((1 << n) - 1) ^ (1 << i)
        coefficients = {}
        for mask in subsets(opposite):
            coefficients[mask] = sum(
                ((-1)**(mask.bit_count() - v.bit_count()) * rows[v | 1 << i][i]
                 for v in subsets(mask)), F())
        mobius.append(coefficients)
    return mobius


def difference(rows, i, mask, context):
    return sum(((-1)**(mask.bit_count() - v.bit_count()) *
                rows[context | v | 1 << i][i] for v in subsets(mask)), F())


def top(rows, q, bottom=False):
    n = len(rows[0])
    total = F()
    for i in range(n):
        others = [j for j in range(n) if j != i]
        for group in combinations(others, q):
            mask = sum(1 << j for j in group)
            context = 0 if bottom else ((1 << n) - 1) ^ (mask | 1 << i)
            total += difference(rows, i, mask, context)
    return total


def gamma(weights, q):
    values = []
    for size in range(q + 1, len(weights) + 1):
        for support in combinations(range(len(weights)), size):
            W = sum((weights[j] for j in support), F())
            elementary = sum((prod(weights[j] for j in group)
                              for group in combinations(support, q)), F())
            values.append(F(factorial(q) * (size - q), size) * elementary / W**q)
    return min(values)


def add(tables, coefficients):
    return [tuple(sum((a * t[s][i] for t, a in zip(tables, coefficients)), F())
                  for i in range(len(tables[0][0])))
            for s in range(len(tables[0]))]


def main():
    config = json.loads(INPUT.read_text())
    counters = {"kernels": 0, "rank_checks": 0, "mobius_entries": 0,
                "top_gamma_checks": 0, "mixed_context_checks": 0,
                "gamma_attainment_checks": 0, "operator_norm_checks": 0}
    for raw_weights in config["weight_vectors"]:
        weights = tuple(map(F, raw_weights))
        n = len(weights)
        for size in range(1, n + 1):
            for support in combinations(range(n), size):
                for degree in config["degrees"]:
                    rows = table(weights, support, degree)
                    coefficients = transform(rows)
                    assert all(v >= 0 for row in coefficients for v in row.values())
                    counters["mobius_entries"] += sum(map(len, coefficients))
                    rank = max((mask.bit_count() for row in coefficients
                                for mask, value in row.items() if value), default=0)
                    assert rank == min(degree, size - 1)
                    counters["kernels"] += 1
                    counters["rank_checks"] += 1
                    for q in range(1, n):
                        L = top(rows, q)
                        L_from_mobius = sum((comb(mask.bit_count(), q) * value
                                            for row in coefficients
                                            for mask, value in row.items()), F())
                        assert L == L_from_mobius
                        bad = degree >= q and size >= q + 1
                        assert (L > 0) == bad
                        if bad:
                            mass = sum(rows[-1], F())
                            assert L >= gamma(weights, q) * mass
                            counters["top_gamma_checks"] += 1
                            if degree == q:
                                W = sum((weights[j] for j in support), F())
                                eq = sum((prod(weights[j] for j in group)
                                          for group in combinations(support, q)), F())
                                exact_ratio = F(factorial(q) * (size-q), size) * eq/W**q
                                assert L/mass == exact_ratio
                                counters["gamma_attainment_checks"] += 1
                    # All contexts for first and second derivatives, not just top.
                    for i in range(n):
                        others = ((1 << n) - 1) ^ (1 << i)
                        for T in subsets(others):
                            if not 1 <= T.bit_count() <= 2:
                                continue
                            for R in subsets(others ^ T):
                                assert difference(rows, i, T, R) >= 0
                                counters["mixed_context_checks"] += 1
        # Reconstruct the linear functional itself; cancellations are accounted for.
        for q in range(1, n):
            l1 = 0
            for i in range(n):
                opponent_mask = ((1 << n)-1) ^ (1 << i)
                coefficients = {v: 0 for v in subsets(opponent_mask)}
                for T in subsets(opponent_mask):
                    if T.bit_count() != q:
                        continue
                    R = opponent_mask ^ T
                    for A in subsets(T):
                        coefficients[R | A] += (-1)**(q-A.bit_count())
                l1 += sum(abs(v) for v in coefficients.values())
            assert l1 == n * comb(n-1, q) * 2**q
            counters["operator_norm_checks"] += 1

    fixture = config["mixture_fixture"]
    weights = tuple(map(F, fixture["weights"]))
    terms = fixture["terms"]
    tables = [table(weights, x["support"], x["degree"]) for x in terms]
    coefficients = [F(x["coefficient"]) for x in terms]
    C = add(tables, coefficients)
    r = fixture["rank"]
    low_coefficients = [a if min(x["degree"], len(x["support"])-1) <= r else F()
                        for a, x in zip(coefficients, terms)]
    low = add(tables, low_coefficients)
    g, L = gamma(weights, r+1), top(C, r+1)
    error = max(C[s][i]-low[s][i] for s in range(len(C)) for i in range(len(weights)))
    bad_mass = sum((a * sum(t[-1], F()) for a, keep, t in
                    zip(coefficients, low_coefficients, tables) if not keep), F())
    assert bad_mass == L/g == F(27, 25)
    assert L == F(11, 50) and g == F(11, 54) and error == F(9, 25)
    assert all(F() <= C[s][i]-low[s][i] <= L/g
               for s in range(len(C)) for i in range(len(weights)))
    assert all(mask.bit_count() <= r or value == 0
               for row in transform(low) for mask, value in row.items())

    # Zero weight destroys nominal-support rank detection.
    z = config["zero_weight_boundary"]
    zrows = table(tuple(map(F, z["weights"])), z["support"], z["degree"])
    zrank = max(mask.bit_count() for row in transform(zrows)
                for mask, value in row.items() if value)
    assert zrank == z["observed_rank"] < min(z["degree"], len(z["support"])-1)

    closure = []
    last_error = None
    first_bottom = None
    for degree in config["closure_degrees"]:
        rows = table((F(1), F(2), F(3), F(4)), range(4), degree)
        mass = sum(rows[-1], F())
        normalized = [tuple(v/mass for v in row) for row in rows]
        limit = [tuple(F(1, 4) if state == 15 else F() for _ in range(4))
                 for state in range(16)]
        err = max(abs(normalized[s][i]-limit[s][i]) for s in range(16) for i in range(4))
        bottom = top(normalized, 2, bottom=True)
        if first_bottom is None:
            first_bottom = bottom
        assert top(normalized, 2) >= gamma((F(1), F(2), F(3), F(4)), 2)
        if last_error is not None:
            assert err < last_error
        last_error = err
        closure.append({"degree": degree, "unanimity_sup_error": str(err),
                        "bottom_L2": str(bottom), "top_L2": str(top(normalized, 2))})
    assert bottom < first_bottom
    # Explicit finite nonclosedness witness: pair singleton response ->0, joint stays1/2.
    pair = table((F(1), F(2)), (0, 1), 64)
    pair_mass = sum(pair[-1], F())
    assert pair[-1][0]/pair_mass == F(1, 2)
    assert F() < pair[1][0]/pair_mass < F(1, 10**20)

    report = {
        "schema_version": 1, "status": "PASS", "python_version": platform.python_version(),
        "command": "python3 tests/audits/positive_kernels/verify_rank_faces.py",
        "seed": None, "precision": "exact integers and fractions.Fraction",
        "error_control": "No floating point, solver or numerical tolerance",
        "input": str(INPUT.relative_to(ROOT)),
        "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "coverage": counters,
        "reuse": {"gamma": str(g), "L2": str(L), "bad_mass": str(bad_mass),
                  "reverse_L_over_gamma": str(L/g), "sup_error": str(error)},
        "zero_weight_boundary_rank": zrank, "closure_diagnostics": closure,
        "limitations": "Finite exact algebra checks only; no proof of arbitrary real weights, all degrees, cone closure or equilibrium existence."
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
