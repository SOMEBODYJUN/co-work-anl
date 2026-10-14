#!/usr/bin/env python3
"""Finite exact checks of the rational special-block envelope construction."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


def ceil_fraction(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def verify(d: int, R: Fraction, a: Fraction) -> dict[str, object]:
    assert d >= 2 and R > 1 and a > 1
    f = (R * (1 + R) ** d + 1) / ((1 + R) ** d + R ** (d + 1))
    assert a < f
    E = (1 + 1 / R) ** d
    q = (E - a) / (a * E - R ** (-d))
    assert 0 < q < 1 and R * q > 1
    B = ceil_fraction(4 * a * d)
    m = 3
    while (R * q) ** (2 * m - 1) <= 12 * B * a:
        m += 2
    L = 2 * m - 1
    special_x = R ** (-L)
    n = (R**L / B).__floor__()
    N0 = (1 + special_x) ** d - a * (n * special_x) ** d
    M0 = a * (1 + n * special_x) ** d - 1
    assert N0 >= Fraction(3, 4) and M0 > 0
    assert n >= R**L / (2 * B)
    T = n * N0 / M0 * q**L
    assert T > 1

    # Check exactly, index by index, rather than solely by telescoping.
    xs = [special_x] + [R] * (m - 1)
    ns = [n] + [1] * (m - 1)
    ts = [1 / R] * m
    us = [Fraction(1)] + [R ** (-2 * (m - i)) for i in range(1, m)]
    vs = [xs[i] * us[i] for i in range(m)]
    assert all(vs[i] / us[(i + 1) % m] == ts[i] for i in range(m))
    P = a * (1 + 1 / R) ** d - R ** (-d)
    Q = (1 + 1 / R) ** d - a
    direct = Fraction(1)
    for x, count in zip(xs, ns):
        N = (1 + x) ** d - a * (count * x) ** d
        M = a * (1 + count * x) ** d - 1
        assert min(N, M, P, Q) > 0
        direct *= count * N * Q / (M * P)
    assert direct == T and direct > 1
    return {
        "d": d,
        "R": str(R),
        "a": str(a),
        "exact_f_d_R": str(f),
        "B": B,
        "odd_ring_length": m,
        "n0_decimal_digits": len(str(n)),
        "all_signs_positive": True,
        "cyclic_weights_exactly_consistent": True,
        "product_above_one_exactly": True,
        "product_numerator_bits": T.numerator.bit_length(),
        "product_denominator_bits": T.denominator.bit_length(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cases = [(2, Fraction(3), Fraction(9, 8)),
             (4, Fraction(4), Fraction(3, 2)),
             (8, Fraction(5), Fraction(2))]
    result = {
        "arithmetic": "fractions and integers only",
        "scope": "finite construction checks, not the all-states game reduction",
        "cases": [verify(*case) for case in cases],
    }
    body = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body, end="")


if __name__ == "__main__":
    main()
