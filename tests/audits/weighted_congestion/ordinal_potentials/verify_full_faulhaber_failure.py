"""Exact Bernoulli/Faulhaber failure checks.

This audit only tests the two stated rational witnesses.  It makes no claim
about pure equilibrium existence or about other potential constructions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from math import comb
from pathlib import Path


def bernoulli_numbers(n: int) -> list[Q]:
    """Return B_0,...,B_n with the convention B_1=-1/2."""
    values = [Q(1)]
    for m in range(1, n + 1):
        values.append(-sum(Q(comb(m + 1, k)) * values[k] for k in range(m)) / (m + 1))
    return values


def faulhaber_coefficients(m: int) -> list[Q]:
    """Coefficients of [B_(m+1)(x+1)-B_(m+1)(0)]/(m+1)."""
    n = m + 1
    b = bernoulli_numbers(n)
    coefficients = [Q(0) for _ in range(n + 1)]
    # B_n(y)=sum_j binom(n,j) B_(n-j) y^j, then y=x+1.
    for j in range(n + 1):
        for p in range(j + 1):
            coefficients[p] += Q(comb(n, j) * comb(j, p)) * b[n - j]
    coefficients[0] -= b[n]
    return [value / n for value in coefficients]


def evaluate(coefficients: list[Q], x: Q) -> Q:
    return sum(value * x**power for power, value in enumerate(coefficients))


def derivative_of_normalized(coefficients: list[Q], m: int, x: Q) -> Q:
    value = evaluate(coefficients, x)
    derivative = sum(
        power * coefficient * x ** (power - 1)
        for power, coefficient in enumerate(coefficients)
        if power
    )
    return derivative / x ** (m + 1) - Q(m + 1) * value / x ** (m + 2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()

    checks = 0
    # Integer values recover the ordinary Faulhaber sums.
    for m in range(1, 22):
        coefficients = faulhaber_coefficients(m)
        for n in range(1, 9):
            assert evaluate(coefficients, Q(n)) == sum(Q(j**m) for j in range(1, n + 1))
            checks += 1

    degree14 = faulhaber_coefficients(14)
    monotonicity_witness = derivative_of_normalized(degree14, 14, Q(3, 2))
    assert monotonicity_witness == Q(-19246442, 43046721)
    assert monotonicity_witness < 0
    checks += 1

    degree20 = faulhaber_coefficients(20)
    positivity_witness = evaluate(degree20, Q(6, 5))
    assert positivity_witness == Q(-19909582690061549, 476837158203125)
    assert positivity_witness < 0
    checks += 1

    source = repo / "tests/audits/weighted_congestion/ordinal_potentials/verify_full_faulhaber_failure.py"
    result = {
        "schema_version": 1,
        "arithmetic": "fractions.Fraction, exact Bernoulli recurrence",
        "checks": checks,
        "monotonicity_witness": {
            "degree": 14,
            "x": "3/2",
            "normalized_derivative": str(monotonicity_witness),
        },
        "positivity_witness": {
            "degree": 20,
            "x": "6/5",
            "faulhaber_value": str(positivity_witness),
        },
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "scope": "method obstruction only; no WC-TARGET conclusion",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
