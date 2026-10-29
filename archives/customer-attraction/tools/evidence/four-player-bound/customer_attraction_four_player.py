"""Exact coefficient audit for the universal four-player 1499/750 proof.

This enumerates customer memberships and rational identities, not games or
strategies. It cannot certify a universal welfare claim by finite sampling.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


BOUND = F(1499, 750)
MULTIPLIERS = {
    "K_C": F(341, 1000),
    "K_D": F(302, 1000),
    "K_Q": F(306, 1000),
    "K_R": F(302, 1000),
    "K_S": F(355, 1000),
    "E": F(354, 1000),
    "P": F(646, 1000),
    "F": F(1267, 1000),
    "L_QS": F(24, 1000),
    "L_RC": F(8, 1000),
    "L_RS": F(17, 1000),
    "L_SB": F(108, 1000),
}
# Rows ABCD, columns QRS, both in product((0, 1), repeat=...) order.
EXPECTED_RESIDUAL_TABLE = (
    (0, 322, 908, 2028, 936, 2016, 2138, 3388),
    (7900, 1210, 1356, 0, 1378, 3, 0, 1),
    (16, 338, 924, 2044, 936, 2016, 2138, 3388),
    (7916, 1226, 1372, 16, 1386, 11, 8, 9),
    (8, 330, 268, 1388, 296, 1376, 1282, 2532),
    (9160, 2470, 2400, 1044, 2422, 1047, 936, 937),
    (12, 334, 272, 1392, 284, 1364, 1270, 2520),
    (10724, 4034, 3964, 2608, 3978, 2603, 2492, 2493),
    (2780, 2747, 3386, 4151, 3410, 4135, 4310, 5205),
    (10244, 3199, 3398, 1687, 3416, 1686, 1736, 1382),
    (409, 376, 1015, 1780, 1023, 1748, 1923, 2818),
    (10789, 3744, 3943, 2232, 3953, 2223, 2273, 1919),
    (42, 9, 0, 765, 24, 749, 708, 1603),
    (10418, 3373, 3356, 1645, 3374, 1644, 1586, 1232),
    (45, 12, 3, 768, 11, 736, 695, 1590),
    (11532, 4487, 4470, 2759, 4480, 2750, 2692, 2338),
)


def share(own: int, *others: int) -> F:
    return F(own, own + sum(others)) if own else F(0)


def remaining(background: int, first: int, second: int) -> F:
    count = first + second
    return F(count, background + count) if count else F(0)


def customer_slacks(bits: tuple[int, ...], optimum: int = 0) -> dict[str, F]:
    a, b, c, d, q, r, s = bits
    u1 = share(a, b, c, d)
    u2 = share(b, a, c, d)
    u3 = share(c, a, b, d)
    u4 = share(d, a, b, c)
    h = u3 + u4 + F(c, (a + b + 1) * (a + b + 2))
    z_d = share(d, q, r, s)
    z_q = share(q, d, r, s)
    z_r = share(r, d, q, s)
    z_s = share(s, d, q, r)
    values = {
        f"K_{name}": u2 - F(bit, a + 3)
        for name, bit in zip("CDQRS", (c, d, q, r, s))
    }
    values.update({
        "E": 4 * u4 + F(a + b + c, a + b + c + 1) - optimum,
        "P": 2 * h + F(a + b, a + b + 1) - optimum,
        "F": u1 - z_d,
        "L_QS": z_q - F(s, d + 3),
        "L_RC": z_r - F(c, d + q + 2),
        "L_RS": z_r - F(s, d + q + 2),
        "L_SB": z_s - F(b, d + q + r + 1),
    })
    return values


def weighted_slacks(bits: tuple[int, ...], optimum: int = 0) -> F:
    return sum((MULTIPLIERS[name] * value
                for name, value in customer_slacks(bits, optimum).items()), F(0))


def check() -> dict[str, object]:
    pair_cases = last_cases = identity_cases = denominator_cases = general_pair_cases = 0
    for a, b, *optimal in product((0, 1), repeat=6):
        covered = int(any(optimal))
        pair_sum = sum((remaining(a + b, optimal[i], optimal[j])
                        for i, j in combinations(range(4), 2)), F(0))
        assert pair_sum >= 3 * covered - F(3 * (a + b), a + b + 1)
        pair_cases += 1

    for a, b, c, *optimal in product((0, 1), repeat=7):
        covered = int(any(optimal))
        comparison_sum = sum((F(t, a + b + c + 1) for t in optimal), F(0))
        assert comparison_sum >= covered - F(a + b + c, a + b + c + 1)
        last_cases += 1

    assert sum(MULTIPLIERS[key] for key in ("E", "P")) == 1
    assert all(value >= 0 for value in MULTIPLIERS.values())
    table = []
    for row_index, actual in enumerate(product((0, 1), repeat=4)):
        row = []
        for column_index, offpath in enumerate(product((0, 1), repeat=3)):
            bits = actual + offpath
            welfare = int(any(actual))
            residual = BOUND * welfare - weighted_slacks(bits)
            assert residual >= 0, bits
            scaled = 12000 * residual
            assert scaled.denominator == 1
            assert scaled == EXPECTED_RESIDUAL_TABLE[row_index][column_index], bits
            row.append(int(scaled))
            for optimum in (0, 1):
                assert BOUND * welfare - optimum == weighted_slacks(bits, optimum) + residual
                identity_cases += 1
        table.append(row)

    # Audit the two general per-customer formulas used to derive (11) and (12).
    # The universal proofs are denominator monotonicity and pair counting.
    for m in range(1, 9):
        for remaining_players in range(1, m + 1):
            for background in range(m - remaining_players + 1):
                for later_load in range(remaining_players):
                    assert F(1, background + 1 + later_load) >= F(1, background + remaining_players)
                    denominator_cases += 1
                for count in range(m + 1):
                    lower = F(int(count > 0), remaining_players) - F(
                        background, remaining_players * (background + remaining_players))
                    assert F(count, background + remaining_players) >= lower
                    denominator_cases += 1
        if m >= 2:
            for background in range(m - 1):
                for optimal in product((0, 1), repeat=m):
                    pair_sum = sum((remaining(background, optimal[i], optimal[j])
                                    for i, j in combinations(range(m), 2)), F(0))
                    lower = (m - 1) * int(any(optimal)) - F(
                        (m - 1) * background, background + 1)
                    assert pair_sum >= lower
                    general_pair_cases += 1

    assert BOUND < 2
    return {
        "claim": "CA-FOUR-UPPER-1499-750",
        "upper_bound": str(BOUND),
        "checks": {
            "optimal_pair_memberships": pair_cases,
            "last_comparison_memberships": last_cases,
            "seven_topic_residual_memberships": 128,
            "full_identity_memberships_with_independent_optimum": identity_cases,
            "independent_optimum_symbol_coefficients": 1,
            "general_denominator_and_aggregate_cases_m_1_through_8": denominator_cases,
            "general_pair_cases_m_2_through_8": general_pair_cases,
        },
        "multipliers": {name: str(value) for name, value in MULTIPLIERS.items()},
        "residual_table_scale": 12000,
        "residual_table_rows_ABCD_columns_QRS": table,
        "all_checks_passed": True,
        "scope": "Exact customer-mask algebra; no strategy sampling or universal inference from finite games.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
