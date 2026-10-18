#!/usr/bin/env python3
"""Exact finite audit of the matroid-intersection capacity obstruction."""

from fractions import Fraction
from itertools import combinations
from math import comb
import json
import hashlib
from pathlib import Path
import platform


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        for chosen in combinations(items, size):
            yield frozenset(chosen)


def ceil_fraction(value):
    return (value.numerator + value.denominator - 1) // value.denominator


def is_independent(chosen, circuit):
    return not circuit <= chosen


def check_matroid_axioms(ground, circuit):
    independent = [chosen for chosen in subsets(ground)
                   if is_independent(chosen, circuit)]
    assert frozenset() in independent
    for chosen in independent:
        for item in chosen:
            assert is_independent(chosen - {item}, circuit)
    for smaller in independent:
        for larger in independent:
            if len(smaller) < len(larger):
                assert any(is_independent(smaller | {item}, circuit)
                           for item in larger - smaller)
    return len(independent)


def run():
    parameter_cases = 0
    circuit_cases = 0
    explicit_exclusion_checks = 0
    records = []
    for k in range(3, 10):
        tiny = frozenset(range(k))
        for r in range(1, (k - 1) // 2 + 1):
            parameter_cases += 1
            complements = list(combinations(range(k), r))
            witnesses = [tiny - frozenset(comp) for comp in complements]
            denominator = comb(k - r - 1, r)
            ratio = Fraction(comb(k, r), denominator)
            product = Fraction(1)
            for t in range(r):
                product *= Fraction(k - t, k - r - 1 - t)
            assert ratio == product
            assert ratio >= Fraction(k, k - r - 1) ** r
            big_weight = Fraction(k - r, k)
            expected_load = Fraction(2 * k - 2 * r, k)
            assert big_weight + Fraction(k - r, k) == expected_load
            worst_count = 0
            for d_size in range(r + 1, k + 1):
                for chosen in combinations(range(k), d_size):
                    circuit_cases += 1
                    circuit_tiny = frozenset(chosen)
                    actual = sum(circuit_tiny <= witness for witness in witnesses)
                    explicit_exclusion_checks += len(witnesses)
                    expected = comb(k - d_size, r) if k - d_size >= r else 0
                    assert actual == expected
                    assert actual <= denominator
                    worst_count = max(worst_count, actual)
            assert worst_count == denominator
            records.append({
                "k": k, "r": r,
                "witness_load": str(expected_load),
                "witness_count": comb(k, r),
                "max_witnesses_excluded_per_matroid": denominator,
                "q_lower": ceil_fraction(ratio),
                "ratio": str(ratio),
            })

    endpoint_records = []
    for k in (3, 5, 7, 9):
        r = (k - 1) // 2
        tiny = frozenset(range(k))
        big = k
        ground = tiny | {big}
        circuits = [frozenset(chosen) | {big}
                    for chosen in combinations(range(k), r + 1)]
        accepted = []
        for chosen in subsets(ground):
            actual = all(is_independent(chosen, circuit) for circuit in circuits)
            expected = big not in chosen or len(chosen - {big}) <= r
            assert actual == expected
            if actual:
                accepted.append(chosen)
                weight = (Fraction(len(chosen - {big}), k)
                          + (Fraction(k - r, k) if big in chosen else 0))
                assert weight <= 1
        assert len(circuits) == comb(k, r)
        augmentation_checked = k <= 5
        if augmentation_checked:
            for circuit in circuits:
                check_matroid_axioms(ground, circuit)
        endpoint_records.append({
            "k": k, "r": r,
            "exact_q": len(circuits),
            "common_independent_sets": len(accepted),
            "augmentation_axiom_checked": augmentation_checked,
        })

    return {
        "status": "all exact checks passed",
        "arithmetic": "integers and fractions.Fraction; no random seed",
        "python_version": platform.python_version(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "command": "python3 tests/audits/unrelated_machines/knapsack_matroid_exponential.py",
        "parameter_cases": parameter_cases,
        "fundamental_circuit_cases": circuit_cases,
        "explicit_circuit_witness_checks": explicit_exclusion_checks,
        "cases": records,
        "exact_endpoints": endpoint_records,
        "limitations": "Finite formula and construction audit; not a substitute for the matroid proof.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
