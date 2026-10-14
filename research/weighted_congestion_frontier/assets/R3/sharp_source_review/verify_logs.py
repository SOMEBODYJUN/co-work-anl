#!/usr/bin/env python3
"""Stable diagnostics for R3-SOURCE-SHARP-ASYMPTOTIC-v1 using Decimal.

Exact decimal-power integer degrees and reproducible floor/ceil checks are
used. Numerics are not proof or certified interval arithmetic.
"""
from __future__ import annotations
import argparse
from decimal import Decimal as R, localcontext, getcontext, ROUND_FLOOR, ROUND_CEILING
import json
import platform
from pathlib import Path


def show(x: R) -> str:
    with localcontext() as ctx:
        ctx.prec = 24
        return str(+x)


def log1p(x: R) -> R:
    # Integer-degree checks use m+guard digits for w~10^-m. Thus 1+w is
    # retained with ample guard precision before taking the logarithm.
    return (1 + x).ln()


def logadd(a: R, b: R) -> R:
    hi, lo = max(a, b), min(a, b)
    # Omit a tail below the working precision. Numerical diagnostics only.
    if lo - hi < -R(getcontext().prec) * R(10).ln():
        return hi
    return hi + log1p((lo - hi).exp())


def compute(m: int, guard: int) -> dict:
    with localcontext() as ctx:
        ctx.prec = m + guard
        d = R(10) ** m
        D = d.ln()
        H = D.ln()
        J = H - (2 * H).ln()
        c = R("0.5").exp() / 2
        if J <= 0:
            raise ValueError("Choose a larger degree: H-ln(2H) must be positive")
        w = D / (2 * d)
        N = 4 * d * H / D**2
        n = int(N.to_integral_value(rounding=ROUND_FLOOR))
        k = int((D / (2 * J)).to_integral_value(rounding=ROUND_CEILING))
        if not (n >= 1 and 1 <= k <= d and 0 < w <= 1):
            raise ArithmeticError("Illegal parameter choice")
        logn, logw = R(n).ln(), w.ln()
        x = n * w
        logS = (D + H.ln()) / 2 - D.ln()
        logq = c.ln() - logS
        logE = d * log1p(w)
        logbeta = logq - logE
        if logbeta > 0:
            raise ArithmeticError("beta exceeds one")
        logt, logr, logp = k * log1p(x), k * x.ln(), k * log1p(w)
        logA = logadd(R(0), logn + logq) - logadd(logt, logn + logbeta)
        logB = logadd(logp, logbeta + d * logw) - logadd(logr, logq)
        f = min(logA, logB).exp()
        logleft = 2 * (f - 1).ln() if f > 1 else R("-Infinity")
        logright = logn + logp - logt
        if logleft > logright + R("1e-40"):
            raise ArithmeticError("Exact inequality U3 failed numerically")
        if logr > -D / 2 + R("1e-40"):
            raise ArithmeticError("Exact lower inequality L5 failed numerically")
        return {
            "degree": f"10^{m}", "decimal_degree_exponent": m,
            "working_dps": m + guard, "n_integer": str(n), "k_integer": k,
            "D": show(D), "H": show(H), "nw": show(x), "k_nw": show(k * x),
            "log_beta": show(logbeta), "log_E": show(logE),
            "r_over_q": show((logr - logq).exp()),
            "n_beta": show((logn + logbeta).exp()),
            "A_over_S": show((logA - logS).exp()),
            "B_over_S": show((logB - logS).exp()),
            "min_over_S": show((min(logA, logB) - logS).exp()),
            "target": show(2 * R("-0.5").exp()),
            "U3_log_slack": show(logright - logleft),
        }


def continuous_proxy(m: int) -> dict:
    """Symbolic integer d=10**m, replacing floor(N) by N at 80 digits.

    The exact relative discrepancy due to n flooring is less than 1/N.
    This is explicitly a proxy, not a finite-degree certificate.
    """
    with localcontext() as ctx:
        ctx.prec = 80
        D = m * R(10).ln()
        H = D.ln()
        J = H - (2 * H).ln()
        c = R("0.5").exp() / 2
        k = int((D / (2 * J)).to_integral_value(rounding=ROUND_CEILING))
        logN = R(4).ln() + D + H.ln() - 2 * D.ln()
        logS = (D + H.ln()) / 2 - D.ln()
        logq = c.ln() - logS
        logw = D.ln() - R(2).ln() - D
        if logw < -1000:
            # Error logE-D/2=O(D^2 exp(-D)) is below shown precision.
            logE, logp = D / 2, R(0)
        else:
            w = logw.exp()
            logE, logp = D.exp() * log1p(w), k * log1p(w)
        x = 2 * H / D
        logt, logr, logbeta = k * log1p(x), k * x.ln(), logq - logE
        logA = logadd(R(0), logN + logq) - logadd(logt, logN + logbeta)
        # beta*w^d is below the displayed precision for these degrees.
        logB = logp - logadd(logr, logq)
        return {
            "degree_symbolic": f"10^{m}",
            "proxy_scope": "n=N, not floor(N); relative discrepancy < exp(-logN)",
            "logN": show(logN), "k_integer": k,
            "k_nw_proxy": show(k * x),
            "A_over_S_proxy": show((logA - logS).exp()),
            "B_over_S_proxy": show((logB - logS).exp()),
            "min_over_S_proxy": show((min(logA, logB) - logS).exp()),
            "target": show(2 * R("-0.5").exp()),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exponents", nargs="+", type=int, default=[32, 64, 128, 256, 512, 1024])
    parser.add_argument("--proxy-exponents", nargs="+", type=int, default=[10000, 1000000, 10**10, 10**20])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = []
    for m in args.exponents:
        low, high = compute(m, 60), compute(m, 100)
        if (low["n_integer"], low["k_integer"]) != (high["n_integer"], high["k_integer"]):
            raise ArithmeticError(f"Floor/ceil instability at degree 10^{m}")
        for key in ("A_over_S", "B_over_S", "min_over_S"):
            if abs(R(low[key]) - R(high[key])) > R("1e-21"):
                raise ArithmeticError(f"Precision instability: {key}, degree 10^{m}")
        high["floor_ceil_stable_at_two_precisions"] = True
        rows.append(high)
    output = {
        "claim": "R3-SOURCE-SHARP-ASYMPTOTIC-v1", "python": platform.python_version(),
        "runtime_dependency": "Python standard-library decimal",
        "evidence_scope": "arbitrary-precision diagnostics; not proof or rigorous interval arithmetic",
        "integer_degree_rows": rows,
        "continuous_proxy_rows": [continuous_proxy(m) for m in args.proxy_exponents],
    }
    serialized = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    else:
        print(serialized)


if __name__ == "__main__":
    main()
