#!/usr/bin/env python3
"""Exact customer-coefficient certificate for CA-FIVE-UPPER-221-100.

No LP, strategy sampler, game solver, or previous audit is imported.  The
universal proof consists of legal SPE slacks and this complete 1024-type
nonnegative identity; tests of finite games are not used as proof.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

CLAIM = "CA-FIVE-UPPER-221-100"
LABELS = ("A", "B", "C", "D", "E", "U", "V", "W", "X", "Y")
D = 10967499015623
COMMON = 4 * D
BOUND = F(24236714656727, D)
HEADLINE_BOUND = F(221, 100)
SCALE = 120 * COMMON
# Each multiplier is its listed numerator / COMMON.
NUMERATORS = {
    "K1C": 2158272647885, "K1D": 6883399216180,
    "K1V": 5857473123795, "K1W": 20012937826300,
    "K1Y": 23697125099850,
    "K2V": 9623771688884, "K2X": 12775841358180,
    "K5U": 3700985415540, "K5V": 1099212654100,
    "K5W": 1099212654100, "K5X": 9478850039940,
    "K5Y": 9478850039940,
    "E0": 14896804574020, "P0": 22906683139384,
    "JUD": 941870809728,
    "E2": 425150018280, "P2": 1190420051184,
    "E3": 1236371744340, "P3": 3214566535284,
    "F2": 49834122911928, "F3": 64909516577850,
}
O_ROWS = ("E0", "P0", "E2", "P2", "E3", "P3")
EXPECTED_MINIMA = (
    0, 0, 0, 332688332337360, 993386564989560, 1794062129187600,
    0, 2186786218207960, 364356401322240, 737788535606460, 0,
    1419179762848760, 77554100389920, 1659008745923760, 0,
    2101769924279340, 1968318321798240, 1025102379416916,
    799055782761800, 1450336073983208, 886028591249000,
    1695816281916576, 460902300254080, 2007673081504968,
    305758119238760, 822293980458916, 103771264015760,
    1302181474258128, 0, 1280489522394636, 0, 1689401463299220,
)


def share(numerator: int, denominator: int) -> F:
    return F(numerator, denominator) if numerator else F(0)


def rows(bits: tuple[int, ...], optimum: F = F(0)) -> dict[str, F]:
    """One customer's slack contributions; optimum is an independent symbol."""
    a, b, c, d, e, u, v, w, x, y = bits
    actual = a + b + c + d + e
    s2, s3 = a + e + u + v + w, a + b + e + x + y
    ua, ub, uc, ud, ue = (share(t, actual) for t in (a, b, c, d, e))
    ze2, zu, zv, zw = (share(t, s2) for t in (e, u, v, w))
    ze3, zx, zy = (share(t, s3) for t in (e, x, y))
    bit = dict(zip(LABELS, bits))
    result = {"K1" + label: ua - F(bit[label], 5) for label in ("C", "D", "V", "W", "Y")}
    result.update({"K2" + label: ub - F(bit[label], a + 4) for label in ("V", "X")})
    result.update({"K5" + label: ue - F(bit[label], a + b + c + d + 1) for label in ("U", "V", "W", "X", "Y")})
    h0 = ud + ue + F(d, (a + b + c + 1) * (a + b + c + 2))
    h2 = zv + zw + F(v, (a + e + u + 1) * (a + e + u + 2))
    h3 = zx + zy + F(x, (a + b + e + 1) * (a + b + e + 2))
    result.update({
        "E0": 5 * ue + F(a + b + c + d, a + b + c + d + 1) - optimum,
        "P0": F(5, 2) * h0 + F(a + b + c, a + b + c + 1) - optimum,
        "JUD": zu - F(d, a + e + 3),
        "E2": 5 * zw + F(a + e + u + v, a + e + u + v + 1) - optimum,
        "P2": F(5, 2) * h2 + F(a + e + u, a + e + u + 1) - optimum,
        "E3": 5 * zy + F(a + b + e + x, a + b + e + x + 1) - optimum,
        "P3": F(5, 2) * h3 + F(a + b + e, a + b + e + 1) - optimum,
        "F2": ub - ze2, "F3": uc - ze3,
    })
    assert result.keys() == NUMERATORS.keys()
    return result


def weighted_rows(bits: tuple[int, ...], optimum: F = F(0)) -> F:
    values = rows(bits, optimum)
    return sum((F(n, COMMON) * values[name] for name, n in NUMERATORS.items()), F(0))


def check() -> dict[str, object]:
    assert F(2) < BOUND < HEADLINE_BOUND < F(89, 40)
    assert all(n > 0 for n in NUMERATORS.values())
    assert sum(NUMERATORS[name] for name in O_ROWS) == COMMON
    pair_cases = last_cases = guarantee_cases = 0
    for p in range(4):
        for optimal in product((0, 1), repeat=5):
            total = sum((share(optimal[i] + optimal[j], p + optimal[i] + optimal[j])
                         for i, j in combinations(range(5), 2)), F(0))
            assert total >= 4 * int(any(optimal)) - F(4 * p, p + 1)
            pair_cases += 1
    for p in range(5):
        for optimal in product((0, 1), repeat=5):
            total = sum((F(t, p + 1) for t in optimal), F(0))
            assert total >= int(any(optimal)) - F(p, p + 1)
            last_cases += 1
    for k in range(1, 6):
        for p in range(6 - k):
            for later_load in range(k):
                assert F(1, p + 1 + later_load) >= F(1, p + k)
                guarantee_cases += 1
    table, minima, zero_count = [], [], 0
    for actual in product((0, 1), repeat=5):
        current = []
        for auxiliary in product((0, 1), repeat=5):
            bits = actual + auxiliary
            welfare = int(any(actual))
            residual = BOUND * welfare - weighted_rows(bits)
            assert residual >= 0, (bits, residual)
            scaled = SCALE * residual
            assert scaled.denominator == 1
            current.append(int(scaled))
            zero_count += residual == 0
            for optimum in (F(0), F(1)):
                assert BOUND * welfare - optimum == weighted_rows(bits, optimum) + residual
        table.append(current)
        minima.append(min(current))
    assert tuple(minima) == EXPECTED_MINIMA
    return {
        "claim": CLAIM, "headline_bound": str(HEADLINE_BOUND),
        "exact_certificate_bound": str(BOUND),
        "common_multiplier_denominator": COMMON,
        "multiplier_numerators": NUMERATORS,
        "labels": LABELS,
        "ordered_paths": {"actual": ["A", "B", "C", "D", "E"],
                          "player2_deviation": ["A", "E", "U", "V", "W"],
                          "player3_deviation": ["A", "B", "E", "X", "Y"]},
        "customer_memberships": 1024, "zero_residual_memberships": zero_count,
        "independent_optimum_identity_cases": 2048,
        "pair_aggregation_cases": pair_cases, "last_aggregation_cases": last_cases,
        "worst_denominator_cases": guarantee_cases,
        "residual_table_scale": SCALE,
        "minimum_scaled_residual_by_actual_ABCDE": minima,
        "residual_table_rows_ABCDE_columns_UVWXY": table,
        "all_exact_checks_passed": True,
        "scope": "All binary customer coefficient types, not sampled games; ordered-node legitimacy is proved in the companion manuscript.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-table", action="store_true")
    args = parser.parse_args()
    result = check()
    if not args.include_table:
        result.pop("residual_table_rows_ABCDE_columns_UVWXY")
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
