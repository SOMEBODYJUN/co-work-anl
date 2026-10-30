#!/usr/bin/env python3
"""Exact integer checks of the independently derived odd-ring parameters."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def verify(s: int) -> dict[str, object]:
    assert s >= 6
    r = 1 << s
    d = 2 * s * r
    alpha = r // 4
    m = s if s % 2 else s + 1
    ell = 2 * m - 1
    B = r**ell
    n = B // s

    # N_0 and M_0 have the common positive denominator B**s.
    N0 = (B + 1) ** s - alpha * n**s
    M0 = alpha * (B + n) ** s - B**s
    # Q and P have the common positive denominator r**d.
    U = (r + 1) ** d
    V = r**d
    Q = U - alpha * V
    P = alpha * U - 1
    assert min(N0, M0, Q, P) > 0
    assert U >= r * r * V
    assert 2 * n * s >= B
    assert 2 * N0 > B**s
    assert M0 < 3 * alpha * B**s
    assert r * Q >= 3 * P
    lhs = n * N0 * Q**ell
    rhs = M0 * P**ell
    assert lhs > rhs
    assert 3 ** (2 * m - 2) > s * r

    # u_i exponents realize x_i and t_i with cyclic closure.
    u_exps = [0] + [-2 * (m - i) for i in range(1, m)]
    x_exps = [-ell] + [1] * (m - 1)
    v_exps = [u + x for u, x in zip(u_exps, x_exps)]
    assert sum(x_exps) == -m
    assert [v_exps[i] - u_exps[(i + 1) % m] for i in range(m)] == [-1] * m

    return {
        "s": s,
        "r": r,
        "degree": d,
        "alpha": alpha,
        "odd_ring_length": m,
        "n0": str(n),
        "weights_exactly_consistent": True,
        "all_four_signs_positive": True,
        "exact_product_strictly_above_one": True,
        "comparison_lhs_bits": lhs.bit_length(),
        "comparison_rhs_bits": rhs.bit_length(),
        "simple_bound_numerator": str(3 ** (2 * m - 2)),
        "simple_bound_denominator": s * r,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s", type=int, nargs="+", default=[6, 7, 8])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "arithmetic": "integer only; all rational denominators cleared exactly",
        "scope": "finite check; independent_parameters.md supplies the uniform proof",
        "cases": [verify(s) for s in args.s],
    }
    body = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body, end="")


if __name__ == "__main__":
    main()
