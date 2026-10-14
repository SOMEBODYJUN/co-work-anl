#!/usr/bin/env python3
"""Exact rational tests of polynomial-mixture envelope identities."""

from __future__ import annotations

from fractions import Fraction
import argparse
import json
from pathlib import Path
import random


def evaluate(coeffs: list[int], z: Fraction) -> Fraction:
    return sum((c * z**k for k, c in enumerate(coeffs)), Fraction(0))


def verify_case(d: int, coefficients_f: list[int], coefficients_g: list[int],
                u: Fraction, v: Fraction, next_u: Fraction, n: int) -> bool:
    # The exact envelope satisfies T_d < d, so this is above that envelope.
    a = Fraction(d)
    x, t = v / u, v / next_u
    N = evaluate(coefficients_f, u + v) - a * evaluate(coefficients_f, n * v)
    M = a * evaluate(coefficients_f, u + n * v) - evaluate(coefficients_f, u)
    P = a * evaluate(coefficients_g, next_u + v) - evaluate(coefficients_g, v)
    Q = evaluate(coefficients_g, next_u + v) - a * evaluate(coefficients_g, next_u)
    assert M > 0 and P > 0
    weights_f = []
    weights_g = []
    factors_f = []
    factors_g = []
    for k in range(d + 1):
        Nk = (1 + x)**k - a * (n * x)**k
        Mk = a * (1 + n * x)**k - 1
        Pk = a * (1 + t)**k - t**k
        Qk = (1 + t)**k - a
        assert Mk > 0 and Pk > 0
        first = n * x * Nk / Mk
        y = n * x
        merged = y * ((1 + y)**k - a * y**k) / (a * (1 + y)**k - 1)
        second = Qk / (t * Pk)
        inverse_t = 1 / t
        rewritten = inverse_t * ((1 + inverse_t)**k - a * inverse_t**k) / (
            a * (1 + inverse_t)**k - 1)
        assert first <= merged <= 1 and second == rewritten <= 1
        if k == 0:
            assert first == -n * x and second == -1 / t
        weights_f.append(coefficients_f[k] * u**k * Mk / M)
        weights_g.append(coefficients_g[k] * next_u**k * Pk / P)
        factors_f.append(first)
        factors_g.append(second)
    assert sum(weights_f) == sum(weights_g) == 1
    assert min(weights_f + weights_g) >= 0
    assert sum((w * z for w, z in zip(weights_f, factors_f)), Fraction(0)) == n*x*N/M
    assert sum((w * z for w, z in zip(weights_g, factors_g)), Fraction(0)) == Q/(t*P)
    assert n*x*N/M <= 1 and Q/(t*P) <= 1
    return N > 0 and Q > 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    seed = 20261014
    rng = random.Random(seed)
    cases = 0
    positive_cases = 0
    for d in (2, 4, 8):
        for _ in range(20):
            cf = [rng.randrange(6) for _ in range(d + 1)]
            cg = [rng.randrange(6) for _ in range(d + 1)]
            cf[0] = max(1, cf[0])
            cg[0] = max(1, cg[0])
            cf[-1] = max(1, cf[-1])
            cg[-1] = max(1, cg[-1])
            u = Fraction(rng.randrange(1, 10), rng.randrange(1, 8))
            v = Fraction(rng.randrange(1, 10), rng.randrange(1, 8))
            next_u = Fraction(rng.randrange(1, 10), rng.randrange(1, 8))
            n = rng.randrange(1, 5)
            positive_cases += verify_case(d, cf, cg, u, v, next_u, n)
            cases += 1
        const = [1] + [0] * d
        verify_case(d, const, const, Fraction(2), Fraction(1, 3), Fraction(3), 2)
        assert evaluate([0] * (d + 1), Fraction(2)) == 0
        cases += 1
    # Guaranteed positive mixed case, with nonzero constant coefficients.
    positive_cases += verify_case(
        2, [1, 0, 100], [1, 0, 100],
        Fraction(1), Fraction(1, 2), Fraction(1), 1)
    cases += 1
    result = {
        "arithmetic": "integers and fractions only",
        "seed": seed,
        "degrees": [2, 4, 8],
        "checked_nonzero_polynomial_pairs": cases,
        "pairs_with_positive_N_and_Q": positive_cases,
        "convex_identities_exact": True,
        "constant_monomial_factors_checked": True,
        "zero_shapes_excluded_without_division": True,
        "factor_above_the_envelope": "alpha=d",
        "scope": "finite algebra checks; no actual-topology existence conclusion",
    }
    body = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body, end="")


if __name__ == "__main__":
    main()
