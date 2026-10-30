#!/usr/bin/env python3
"""Exact finite two-order certificates for WC-R1-SANDWICH-BARRIER v1.

Uses Fraction only for mathematical checks. Decimal formatting is presentation.
No claim is inferred from numerical optimization or a finite sample.
"""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
import argparse
import json
from pathlib import Path


def orders(d, n, t):
    eps = t / n
    heavy_last = (1 + t) ** d + eps * sum(((j * eps) ** d for j in range(1, n + 1)), Q(0))
    heavy_first = 1 + eps * sum(((1 + j * eps) ** d for j in range(1, n + 1)), Q(0))
    return heavy_last, heavy_first


def decimal(q):
    with localcontext() as ctx:
        ctx.prec = 24
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def check(d, n, t):
    assert d >= 1 and n >= 1 and t > 0
    a, b = orders(d, n, t)
    ai = (1 + t) ** d + t ** (d + 1) / (d + 1)
    bi = 1 + ((1 + t) ** (d + 1) - 1) / (d + 1)
    aerr = (t / n) * t ** d
    berr = (t / n) * ((1 + t) ** d - 1)
    assert ai <= a <= ai + aerr
    assert bi <= b <= bi + berr
    ratio = a / b
    lower = ai / (bi + berr)
    assert ratio >= lower
    # Any proposed common sandwich with alpha below this exact rational fails.
    certificate_target = Q(ratio.numerator * 1000 // ratio.denominator, 1000)
    if certificate_target == ratio:
        certificate_target -= Q(1, 1000)
    assert a > certificate_target * b
    return {
        "d": d, "light_players": n, "total_light_weight": str(t),
        "each_light_weight": str(t / n),
        "heavy_last_sum": str(a), "heavy_first_sum": str(b),
        "ratio_exact": str(ratio), "ratio_decimal": decimal(ratio),
        "ratio_over_d_decimal": decimal(ratio / d),
        "rigorous_lower_exact": str(lower),
        "strictly_excluded_rational_alpha": str(certificate_target),
        "riemann_bounds_exact": True,
    }


def check_upper_coefficients(max_degree):
    # Coefficientwise proof checks; these checks illustrate, not replace, proof.
    for d in range(1, max_degree + 1):
        for k in range(1, d + 1):
            coefficient_ratio = Q(1, d + 1 - k)
            assert Q(1, d) <= coefficient_ratio <= 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evidence.json")
    args = parser.parse_args()
    check_upper_coefficients(256)
    # A deterministic rational t≈2 log_2(d)/d; no transcendental evaluations.
    records = []
    for d in [2, 3, 4, 8, 16, 32, 64, 128, 256]:
        m = d.bit_length()  # ceil(log_2(d+1)), evaluated with integers.
        records.append(check(d, d, Q(2 * m, d)))
    # Boundary and small-mesh checks exercise n=1 and tiny positive t.
    for d, n, t in [(1, 1, Q(1)), (2, 1, Q(1, 1000)),
                    (3, 2, Q(100)), (7, 13, Q(1, 10000))]:
        check(d, n, t)
    payload = {
        "claim": "WC-R1-SANDWICH-BARRIER v1",
        "arithmetic": "fractions.Fraction exact; decimal display only",
        "checks": "two sums, exact Riemann brackets, rational strict target, coefficient bounds",
        "not_established_by_run": "universal theorem, novelty, or nonexistence of equilibrium",
        "records": records,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2) + "\n")
    for row in records:
        print(f"d={row['d']:3d}, n={row['light_players']:3d}, ratio={row['ratio_decimal']}, ratio/d={row['ratio_over_d_decimal']}")
    print("All exact checks passed.")


if __name__ == "__main__":
    main()
