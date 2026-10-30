#!/usr/bin/env python3
"""New exact supplement: interpolate integer sums, without Bernoulli recurrence.

This is not the frozen audit.  It independently checks its two values and
adds the missing derivative sign needed to diagnose nonmonotonicity.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import sys


def polynomial_from_integer_sums(m):
    # Newton's forward formula S(x)=sum_k Delta^k S(0) binom(x,k).
    values = [Q(sum(j**m for j in range(1, n + 1))) for n in range(m + 2)]
    leading_differences = []
    while values:
        leading_differences.append(values[0])
        values = [b - a for a, b in zip(values, values[1:])]
    result = [Q(0)] * (m + 2)
    basis = [Q(1)]
    for k, difference in enumerate(leading_differences):
        for i, coefficient in enumerate(basis):
            result[i] += difference * coefficient
        # binom(x,k+1)=binom(x,k)*(x-k)/(k+1).
        next_basis = [Q(0)] * (len(basis) + 1)
        for i, coefficient in enumerate(basis):
            next_basis[i] -= coefficient * Q(k, k + 1)
            next_basis[i + 1] += coefficient / (k + 1)
        basis = next_basis
    assert result[0] == 0 and result[-1] == Q(1, m + 1)
    return result


def evaluate(coefficients, x):
    result = Q(0)
    for coefficient in reversed(coefficients):
        result = result * x + coefficient
    return result


def normalized_derivative(coefficients, m, x):
    derivative = [i * coefficients[i] for i in range(1, len(coefficients))]
    return (x * evaluate(derivative, x) - (m + 1) * evaluate(coefficients, x)) / x ** (m + 2)


def main():
    polynomials = {m: polynomial_from_integer_sums(m) for m in range(1, 22)}
    integer_checks = 0
    for m, coefficients in polynomials.items():
        for n in [*range(9), m + 2, m + 3]:
            assert evaluate(coefficients, Q(n)) == sum(j**m for j in range(1, n + 1))
            integer_checks += 1
    records = []
    for m, x, expected in [
        (1, Q(1), Q(-1, 2)),
        (1, Q(3, 2), Q(-2, 9)),
        (14, Q(1), Q(1, 6)),
        (14, Q(3, 2), Q(-19246442, 43046721)),
    ]:
        actual = normalized_derivative(polynomials[m], m, x)
        assert actual == expected
        value = evaluate(polynomials[m], x)
        normalized = value / x ** (m + 1)
        records.append({
            "degree": m, "x": str(x), "faulhaber_value": str(value),
            "S_over_x_power_derivative": str(actual),
            "reciprocal_derivative": str(-actual / normalized**2),
        })
    negative = evaluate(polynomials[20], Q(6, 5))
    assert negative == Q(-19909582690061549, 476837158203125)
    source = Path(__file__).resolve()
    print(json.dumps({
        "provenance": "new supplement; not a historical output or a modified original audit",
        "method": "Newton forward interpolation of exact integer power sums; no Bernoulli recurrence or original-code import",
        "arithmetic": "fractions.Fraction only",
        "integer_checks": integer_checks,
        "derivative_checks": records,
        "negative_value": {"degree": 20, "x": "6/5", "value": str(negative)},
        "correction": "The original negative derivative alone does not prove failure of the low-degree decreasing direction. At degree 14 the added +1/6 at x=1 and the original negative derivative at x=3/2 together prove neither monotonic direction holds on [1,2].",
        "coefficients": {str(m): [str(c) for c in coefficients] for m, coefficients in polynomials.items()},
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "python": sys.version,
        "platform": platform.platform(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
