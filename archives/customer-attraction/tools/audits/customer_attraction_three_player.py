"""Exact per-customer audit of the universal three-player 142/81 proof.

This checks algebra on all membership bits, not SPE instances, and is not
an experimental substitute for the proof in three_player_bound.md.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def payoff(own: int, *others: int) -> F:
    return F(own, own + sum(others)) if own else F(0)


def remaining(background: int, first: int, second: int) -> F:
    count = first + second
    return F(count, background + count) if count else F(0)


def check() -> dict[str, object]:
    pair_cases = last_cases = identity_cases = 0
    for a, t, s, r in product((0, 1), repeat=4):
        covered = int(t + s + r > 0)
        pair_sum = sum((remaining(a, x, y) for x, y in ((t, s), (t, r), (s, r))), F(0))
        assert pair_sum >= 2 * covered - a, (a, t, s, r)
        pair_cases += 1

    for a, b, t, s, r in product((0, 1), repeat=5):
        covered = int(t + s + r > 0)
        reply_sum = sum((payoff(x, a, b) for x in (t, s, r)), F(0))
        lower = F(covered) - F(a + b, 2) + F(a * b, 3)
        assert reply_sum >= lower, (a, b, t, s, r)
        last_cases += 1

    remainder_by_actual: dict[str, str] = {}
    for a, b, c, t, s, r in product((0, 1), repeat=6):
        u = payoff(a, b, c)
        v = payoff(c, a, b)
        tax = F(b, 2) - F(a * b, 3)
        welfare = int(a + b + c > 0)
        optimum = int(t + s + r > 0)
        h = F(welfare) - u + tax
        d = 3 * h + a - 2 * optimum
        e = 3 * v + F(a + b, 2) - F(a * b, 3) - optimum
        k = 3 * u - c
        only_a = a * (1 - b) * (1 - c)
        only_b = (1 - a) * b * (1 - c)
        only_c = (1 - a) * (1 - b) * c
        all_three = a * b * c
        residual = F(11 * only_a + 35 * only_b + 6 * only_c + 6 * all_three, 162)
        assert F(142, 81) * welfare - optimum == F(8, 27) * d + F(11, 27) * e + F(32, 81) * k + residual
        p = F(3 * h + a, 2)
        assert 24 * welfare - 13 * optimum == 12 * (p - optimum) + (9 * u - optimum) + 3 * (3 * u - b) + 6 * only_c
        assert residual >= 0
        remainder_by_actual[f"{a}{b}{c}"] = str(residual)
        identity_cases += 1

    # The coefficient of the independent optimum symbol is -1 in (10),
    # and -13 in (11); membership evaluation must not hide this check.
    assert -2 * F(8, 27) - F(11, 27) == -1
    assert -12 - 1 == -13
    assert F(142, 81) < 2
    assert F(5, 3) < F(142, 81)
    return {
        "claim": "CA-THREE-UPPER-142-81",
        "checks": {
            "pair_membership_cases": pair_cases,
            "last_reply_membership_cases": last_cases,
            "full_identity_membership_cases": identity_cases,
            "independent_optimum_symbol_coefficients": 2,
        },
        "upper_bound": "142/81",
        "actual_membership_remainders": remainder_by_actual,
        "all_checks_passed": True,
        "scope": "Exact algebraic audit; no finite game enumeration and no inference from sampling.",
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
