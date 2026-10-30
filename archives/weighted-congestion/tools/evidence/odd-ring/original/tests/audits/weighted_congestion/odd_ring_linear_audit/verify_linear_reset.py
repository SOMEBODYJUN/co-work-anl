#!/usr/bin/env python3
"""Reproduce the linear-reset certificate with exact rational decisions.

This independent audit does not import the original ring programs.  Decimal
checks are explicitly diagnostic; the universal proof is in the current note.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import prod
from pathlib import Path
import json
import platform


def reset_certificate(d, t, alpha):
    if not isinstance(d, int) or d < 1 or not 0 < t < 1 or alpha <= 1:
        raise ValueError("require integer d>=1, 0<t<1, alpha>1")
    y = (1 + t) ** d
    threshold = (y + t ** (d + 1)) / (1 + t * y)
    if not alpha < threshold:
        raise ValueError("strict alpha<H_d(t) is required")
    P, Q = alpha * y - t**d, y - alpha
    B = Q / P
    assert P > 0 and Q > 0 and B > t
    R = 5
    while not (t**R < 1 / (4 * alpha) and (B / t)**R > 8 * alpha**2):
        R += 4
    m = (R + 1) // 2
    x = t**R
    n = int(1 / (2 * alpha * x))
    N, M = 1 + x - alpha * n * x, alpha * (1 + n * x) - 1
    assert m >= 3 and m % 2 == 1 and n > 1 / (4 * alpha * x)
    assert N > F(1, 2) and 0 < M < alpha
    A = n * N / M
    assert A > 1 / (8 * alpha**2 * x)
    G = A * B**R
    assert G > (B / t)**R / (8 * alpha**2) > 1
    # Back-check the independent factored product against every ring position.
    xs, ns, ks = [x] + [1 / t] * (m - 1), [n] + [1] * (m - 1), [1] + [d] * (m - 1)
    NN = [(1 + xx)**kk - alpha * (nn * xx)**kk for xx, nn, kk in zip(xs, ns, ks)]
    MM = [alpha * (1 + nn * xx)**kk - 1 for xx, nn, kk in zip(xs, ns, ks)]
    assert prod(xs) == t**m
    direct = prod(nn * ni * Q / (mi * P) for nn, ni, mi in zip(ns, NN, MM))
    assert direct == G and all(z > 0 for z in NN + MM)
    return dict(degree=d, t=str(t), alpha=str(alpha), threshold=str(threshold),
                R=R, hubs=m, reset_cohort=str(n), weight_cycle_exact=True,
                product_identity_exact=True, strict_product_gt_one=True,
                product_numerator_bits=G.numerator.bit_length(),
                product_denominator_bits=G.denominator.bit_length())


def source_ceiling_checks():
    count = 0
    for d in (2, 3, 4, 10, 32):
        for k in range(1, d + 1):
            for n in (1, 2, 10, 100):
                for w in (F(0), F(1, 1000), F(1, 10), F(1, 2), F(1)):
                    for beta in (F(0), F(1, 100), F(1, 2), F(1)):
                        E = (1 + w)**d
                        a = (1 + n * beta * E) / ((1 + n * w)**k + n * beta)
                        den = (n * w)**k + beta * E
                        if not den:
                            # w=beta=0: the first ratio is 1, hence min<=1.
                            assert a == 1
                            count += 1
                            continue
                        b = ((1 + w)**k + beta * w**d) / den
                        f = min(a, b)
                        if f > 1:
                            assert 0 < w <= 1 and beta > 0
                            assert f <= E
                            assert (f - 1)**2 <= n * (1 + w)**k / (1 + n * w)**k <= n
                            assert n * w < 1 + w
                        if f >= 4:
                            assert f**2 < 2 * d
                        count += 1
    return dict(exact_parameter_cases=count, scope="finite regression, not the global upper proof")


def decimal_diagnostics():
    rows = []
    with localcontext() as ctx:
        ctx.prec = 80
        for d in (2, 3, 4, 5, 10, 32, 100, 1000, 1000000):
            dd = Decimal(d)
            root = (dd.ln() / (dd + 1)).exp()
            t = root - 1
            E = dd / ((dd + 1) * root - dd)
            y = (1 + t)**d
            H = (y + t**(d + 1)) / (1 + t * y)
            reciprocal = 1 / (t + (1 + t)**(-d))
            assert abs(root**(d + 1) / dd - 1) < Decimal("1e-70")
            assert abs(reciprocal / E - 1) < Decimal("1e-70")
            assert E > 1
            # At enormous d the positive correction rounds to zero.  The
            # strict inequality is proved symbolically, not inferred here.
            assert H / E - 1 > -Decimal("1e-70")
            if d >= 4:
                tu = dd.ln() / dd
                yu = (1 + tu)**d
                Hu = (yu + tu**(d + 1)) / (1 + tu * yu)
                assert yu > dd / 2 and Hu > dd / (dd.ln() + 2) > 1
            rows.append(dict(degree=d, E_display=str(E), H_at_optimizer_display=str(H)))
    return dict(precision_digits=80, arithmetic="Decimal; diagnostic only", cases=rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    fixtures = [(2, F(1, 2), F(11, 10)), (3, F(1, 3), F(5, 4)),
                (4, F(3, 8), F(6, 5)), (10, F(1, 5), F(5, 2)),
                (32, F(1, 8), F(5)), (100, F(1, 20), F(16)),
                (1000, F(1, 125), F(100))]
    exact = [reset_certificate(*row) for row in fixtures]
    rejection_count = 0
    for row in ((0, F(1, 2), F(2)), (1, F(1, 2), F(101, 100)),
                (2, F(0), F(11, 10)), (2, F(1), F(11, 10)),
                (2, F(1, 2), F(1)), (2, F(1, 2), F(19, 17))):
        try:
            reset_certificate(*row)
        except ValueError:
            rejection_count += 1
        else:
            raise AssertionError(("unrejected invalid or strict-boundary input", row))
    assert rejection_count == 6
    result = dict(python_version=platform.python_version(), seed=None,
                  arithmetic="Fraction exact; no solver or floating tolerance",
                  exact_linear_reset_cases=exact, rejected_boundary_cases=rejection_count,
                  source_ceiling_regression=source_ceiling_checks(),
                  envelope_diagnostics=decimal_diagnostics(),
                  limitations="Finite evidence validates implementation; universal claims use the general proofs.")
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(exact_fixtures=len(exact), rejected_boundaries=rejection_count,
                         source_cases=result['source_ceiling_regression']['exact_parameter_cases'],
                         output=str(args.output)), ensure_ascii=False))


if __name__ == "__main__":
    main()
