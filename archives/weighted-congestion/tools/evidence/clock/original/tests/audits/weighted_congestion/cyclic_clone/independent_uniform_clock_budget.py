#!/usr/bin/env python3
"""锚定三元统一泄漏预算：独立有理区间审计。

仅审计满足必要条件 alpha < max(w)/min(w) 的算术参数；不声称
每组参数都来自真实拥塞博弈的双轮改善环。所有判定使用 Fraction。
不导入作者代码，不依赖浮点、随机数或外部包。
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
import sys


def atanh_log_interval(x: F, terms: int = 24) -> tuple[F, F]:
    """For 1 <= x <= 2, enclose log(x) by its positive odd-power series."""
    assert F(1) <= x <= F(2)
    z = (x - 1) / (x + 1)
    partial = F(0)
    power = z
    for k in range(terms):
        partial += 2 * power / (2 * k + 1)
        power *= z * z
    # Every tail denominator is >= 2*terms+1.
    error = 2 * power / ((2 * terms + 1) * (1 - z * z))
    return partial, partial + error


def log_interval(x: F) -> tuple[F, F]:
    """A rational enclosure; exact scaling keeps the series ratio <= 1/3."""
    assert x >= 1
    k = 0
    y = x
    while y >= 2:
        y /= 2
        k += 1
    lo2, hi2 = atanh_log_interval(F(2))
    loy, hiy = atanh_log_interval(y)
    return k * lo2 + loy, k * hi2 + hiy


def anchor_delta(weights: tuple[F, ...], anchor: int) -> F:
    others = tuple(i for i in range(len(weights)) if i != anchor)
    values = []
    for i, j in combinations(others, 2):
        triple = (weights[anchor], weights[i], weights[j])
        values.append(1 - min(triple) / sum(triple))
    return max(values)


def least_budget_degree(delta: F, target: F) -> int:
    assert 0 < delta < 1 and 0 < target < 1
    lo, hi = 0, 1
    while delta ** hi > target:
        lo, hi = hi, 2 * hi
    while lo + 1 < hi:
        middle = (lo + hi) // 2
        if delta ** middle <= target:
            hi = middle
        else:
            lo = middle
    assert delta ** hi <= target < delta ** (hi - 1)
    return hi


def weight_cases() -> list[tuple[F, ...]]:
    # Exhaustive n=3 includes all placements of both extrema and duplicates.
    cases = set(product((F(1, 4), F(1), F(4)), repeat=3))
    palette = (F(1, 8), F(1, 2), F(1), F(2), F(8))
    for n in range(4, 8):
        for offset in range(len(palette)):
            row = tuple(palette[(2 * i + offset) % len(palette)] for i in range(n))
            cases.add(row)
            cases.add(tuple(reversed(row)))
        cases.add(tuple(F(1) for _ in range(n)))
    return sorted(cases, key=lambda row: (len(row), row))


def audit() -> dict:
    totals = dict(weight_vectors=0, anchors=0, parameter_cases=0, q_checks=0,
                  equal_weight_cases=0, max_minimal_degree=0)
    least_gap = None
    least_gap_case = None
    alphas = (F(1), F(3, 2), F(3), F(7))
    margins = (F(1), F(1, 1000))  # eta/B; B may be scaled to 1.
    for weights in weight_cases():
        totals["weight_vectors"] += 1
        ratio = max(weights) / min(weights)
        n = len(weights)
        L = F((n - 1) * (n - 2), 2)
        if ratio == 1:
            totals["equal_weight_cases"] += 1
            assert not any(alpha < ratio for alpha in alphas)
        for anchor in range(n):
            totals["anchors"] += 1
            delta = anchor_delta(weights, anchor)
            assert delta >= (ratio + 1) / (ratio + 2)
            for alpha, margin in product(alphas, margins):
                if alpha >= ratio:
                    continue
                target = margin / (4 * alpha * alpha * L)
                D0 = least_budget_degree(delta, target)
                totals["parameter_cases"] += 1
                totals["max_minimal_degree"] = max(totals["max_minimal_degree"], D0)
                _, log_A_hi = log_interval(4 * alpha * alpha * L)
                assert D0 > (ratio + 1) * log_A_hi
                _, log_2a_hi = log_interval(2 * alpha)
                assert D0 > 2 * (alpha + 1) * log_2a_hi
                for D in (D0, D0 + 1, 2 * D0):
                    assert delta ** D <= target
                    for p in (0, D - 1, D, D + 1, 2 * D):
                        q = max(p, D)
                        _, log_q_hi = log_interval(F(q))
                        # Stronger than alpha*log(q)/q < 1.
                        gap = q - (alpha + 1) * log_q_hi
                        assert gap > 0
                        totals["q_checks"] += 1
                        if least_gap is None or gap < least_gap:
                            least_gap = gap
                            least_gap_case = dict(weights=list(map(str, weights)), anchor=anchor,
                                                  alpha=str(alpha), eta_over_B=str(margin),
                                                  D=D, p=p, q=q)
    assert least_gap is not None
    return {
        "title": "锚定三元统一泄漏预算的独立有理区间审计",
        "scope": "Finite arithmetic parameter audit only; alpha<R is necessary for a real strict cycle, not sufficient. No general theorem is inferred from sampling.",
        "arithmetic": "fractions.Fraction; log enclosure uses 24 odd-power terms after exact power-of-two reduction and a proved geometric tail bound",
        "parameters": {"alphas": list(map(str, alphas)), "eta_over_B": list(map(str, margins)),
                       "degree_choices": "D_min,D_min+1,2D_min; p=0,D-1,D,D+1,2D", "seed": "none"},
        "checks": ["all anchors: delta >= (R+1)/(R+2)",
                   "minimal D satisfies budget and D-1 fails",
                   "D > (R+1) log(4 alpha^2 L)",
                   "D > 2(alpha+1) log(2 alpha)",
                   "q > (alpha+1) log(q), using rational upper log bounds"],
        "totals": totals,
        "smallest_certified_gap": str(least_gap),
        "smallest_gap_case": least_gap_case,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "command": " ".join(sys.argv),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
