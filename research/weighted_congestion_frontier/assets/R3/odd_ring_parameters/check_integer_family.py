#!/usr/bin/env python3
"""Exact arithmetic checks of the constant-one integer family."""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import isqrt
import json
from pathlib import Path


def exp_bounds(j: int, terms: int = 64) -> tuple[Fraction, Fraction]:
    """Strict rational lower/upper bounds on exp(j), j positive integer."""
    assert j > 0 and terms + 2 > j
    term = Fraction(1)
    partial = term
    for h in range(1, terms + 1):
        term *= Fraction(j, h)
        partial += term
    next_term = term * Fraction(j, terms + 1)
    tail_upper = next_term / (1 - Fraction(j, terms + 2))
    return partial, partial + tail_upper


def ceil_log(r: int) -> int:
    """Locate ceil(log(r)) with exp bounds, without binary floating point."""
    j = 1
    while True:
        terms = max(64, 2 * j)
        while True:
            lower, upper = exp_bounds(j, terms)
            if upper < r:
                j += 1
                break
            if lower > r:
                if j > 1:
                    assert exp_bounds(j - 1, terms)[1] < r
                return j
            terms *= 2


def verify(r: int) -> dict[str, object]:
    assert r >= 64
    log_ceil = ceil_log(r)
    t = isqrt(log_ceil)
    d = r * (log_ceil + 4 * t)
    m = 6 * t * log_ceil
    m += 1 - m % 2
    exponent = 2 * m - 1
    k = 1
    while t**k < 2 * r:
        k += 1
    assert log_ceil >= 5 and t >= 2 and k < d
    assert k < t * log_ceil
    assert 4 * log_ceil <= r
    assert log_ceil + 4 * t < t * (r + 1)
    assert exponent > 3 * log_ceil * (2 * t + 1)
    alpha = Fraction(r * t, t + 1)
    B = r**exponent
    n = B // t
    # The common positive denominators cancel from N/M and Q/P.
    N0 = (t + 1) * (B + 1) ** k - r * t * n**k
    M0 = r * t * (B + n) ** k - (t + 1) * B**k
    Q = (t + 1) * (r + 1) ** d - r * t * r**d
    P = r * t * (r + 1) ** d - (t + 1)
    assert min(N0, M0, Q, P) > 0
    assert 2 * N0 > (t + 1) * B**k
    assert 2 * n * t >= B
    assert 2 * t * r * Q > (2 * t + 1) * P
    assert (r * Q) ** exponent > r**3 * P**exponent
    lhs = n * N0 * Q**exponent
    rhs = M0 * P**exponent
    assert lhs > rhs
    return {
        "r": r,
        "ceil_ln_r": log_ceil,
        "ceil_ln_r_certified_by_rational_exponential_bounds": True,
        "t": t,
        "degree": d,
        "alpha": str(alpha),
        "exceptional_degree_k": k,
        "odd_ring_length": m,
        "n0_decimal_digits": len(str(n)),
        "all_four_signs_positive": True,
        "exact_r_Q_over_P_above_1_plus_1_over_2t": True,
        "exact_product_strictly_above_one": True,
        "comparison_lhs_bits": lhs.bit_length(),
        "comparison_rhs_bits": rhs.bit_length(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r", type=int, nargs="+", default=[64, 65, 128])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "arithmetic": "integers and fractions only; no binary floating point",
        "scope": "finite check; integer_family_review.md proves every r >= 64",
        "cases": [verify(r) for r in args.r],
    }
    body = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body, end="")


if __name__ == "__main__":
    main()
