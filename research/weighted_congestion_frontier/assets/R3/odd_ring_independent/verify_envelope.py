#!/usr/bin/env python3
"""Exact finite checks for the independently reconstructed ring envelope.

All acceptance uses Fraction/integer inequalities. The universal assertions are
proved in EXACT_ENVELOPE_REVIEW.md; samples are not substitutes for that proof.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

from verify_literal import normalized, rational_coefficients


def f(degree, y):
    return (y * (1 + y) ** degree + 1) / ((1 + y) ** degree + y ** (degree + 1))


def factor(k, n, x, alpha):
    return x * n * ((1 + x) ** k - alpha * (n * x) ** k) / (
        alpha * (1 + n * x) ** k - 1)


def ceil_fraction(value):
    return (value.numerator + value.denominator - 1) // value.denominator


def elementary_identity_checks():
    points = [F(1, 8), F(1, 2), F(1), F(3, 2), F(3), F(8)]
    alphas = [F(11, 10), F(3, 2), F(3)]
    checks = 0
    for degree in range(1, 13):
        for y in points:
            value = f(degree, y)
            if y <= 1:
                assert value <= 1
            else:
                assert value >= 1
                for k in range(degree + 1):
                    assert f(k, y) <= value
                    checks += 1
            for alpha in alphas:
                assert (factor(degree, 1, y, alpha) > 1) == (alpha < value)
                t = 1 / y
                pp = alpha * (1 + t) ** degree - t ** degree
                qq = (1 + t) ** degree - alpha
                assert factor(degree, 1, y, alpha) == qq / (t * pp)
                for n in range(1, 6):
                    assert factor(degree, n, y, alpha) <= factor(degree, 1, n * y, alpha)
                    checks += 1
                checks += 2
            if degree >= 2 and y > 1:
                # Exact endpoint at a rational f_d(y), not an approximation to T_d.
                assert factor(degree, 1, y, value) == 1
                checks += 1
    for y in points:
        assert f(0, y) == f(1, y) == 1
        checks += 2
    return {"degrees": [1, 12], "exact_checks": checks,
            "d1_result": "f_1(R)=1 at every sampled R; general identity proved in review"}


def homogeneous_degree_certificate(degree):
    rr = F(3)
    alpha = (1 + f(degree, rr)) / 2
    assert 1 < alpha < f(degree, rr)
    ee = (1 + 1 / rr) ** degree
    qq = (ee - alpha) / (alpha * ee - rr ** (-degree))
    growth = rr * qq
    assert growth > 1 and 0 < qq < 1 / alpha < 1
    bb = ceil_fraction(4 * alpha * degree)
    m, ell = 3, 5
    value = growth ** ell
    while value <= 12 * bb * alpha:
        m += 2
        ell += 4
        value *= growth ** 4
    assert ell == 2 * m - 1 and m % 2 == 1
    reset_scale = rr ** ell
    assert reset_scale / bb > 2
    n0 = (reset_scale / bb).numerator // (reset_scale / bb).denominator
    x0 = 1 / reset_scale
    nn = (1 + x0) ** degree - alpha * (n0 * x0) ** degree
    mm = alpha * (1 + n0 * x0) ** degree - 1
    gain = n0 * nn / mm * qq ** ell
    assert nn > F(3, 4) and 0 < mm < 3 * alpha
    assert n0 >= reset_scale / (2 * bb)
    assert gain > value / (8 * bb * alpha) > F(3, 2)
    u = [rr ** ell] + [rr ** (2 * i - 1) for i in range(1, m)]
    v = [F(1)] + [rr ** (2 * i) for i in range(1, m)]
    n, k = [n0] + [1] * (m - 1), [degree] * m
    assert normalized(u, v, n, k, degree, alpha)[-1] == gain
    a, b, checked_gain = rational_coefficients(u, v, n, k, degree, alpha)
    assert checked_gain == gain and all(z > 0 for z in a + b)
    return {"degree_of_every_resource": degree, "R": str(rr), "a": str(alpha),
            "f_d_R": str(f(degree, rr)), "R_q": str(growth), "B": bb,
            "m": m, "ell": ell, "n0": n0,
            "player_count": m + sum(n),
            "gain_floor": gain.numerator // gain.denominator,
            "positive_rational_coefficients_constructed": len(a) + len(b),
            "max_coefficient_denominator_bits": max(z.denominator.bit_length() for z in a + b),
            "state_enumeration": False}


def strict_H_separation_witness(degree):
    # Isolate c = d^(1/(d+1)) without ever evaluating an irrational number.
    lo, hi = F(1), F(2)
    for _ in range(96):
        mid = (lo + hi) / 2
        if mid ** (degree + 1) < degree:
            lo = mid
        else:
            hi = mid
    cc = (lo + hi) / 2
    rr = 1 / (cc - 1)
    assert rr > 1
    ff = f(degree, rr)
    # f(R)>H_d iff [d(f+1)/((d+1)f)]^(d+1)<d.
    lower_threshold = degree * (ff + 1) / ((degree + 1) * ff)
    assert lower_threshold ** (degree + 1) < degree
    # Check the proposed upper bound at this witness as a separate exact inequality.
    shifted = ff - F(1, 2 ** degree + 1)
    assert shifted > 0
    upper_threshold = degree * (shifted + 1) / ((degree + 1) * shifted)
    assert upper_threshold ** (degree + 1) > degree
    return {"degree": degree, "rational_R": str(rr),
            "H_d_less_than_f_d_R": True,
            "f_d_R_less_than_H_d_plus_1_over_2_power_d_plus_1": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    witnesses = [strict_H_separation_witness(degree) for degree in range(2, 33)]
    result = {"arithmetic": "Python Fraction; exact integer/rational comparisons only",
              "identity_checks": elementary_identity_checks(),
              "all_degree_d_certificates": [homogeneous_degree_certificate(d) for d in range(2, 9)],
              "H_separation": {"all_degrees_checked": [2, 32], "count": len(witnesses),
                               "selected_witnesses": [w for w in witnesses if w["degree"] in (2, 3, 4, 8, 16, 32)]},
              "scope": "Finite checks; exact universal envelope and endpoint proved in companion review"}
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
