"""Independent exact algebra audit for CA-UNIFORM-PORTFOLIO-TWO.

This checks the complete customer-membership identity, not a sample of SPE
games. Legal-history comparisons and the universal interpretation are proved
in the mathematical note; this file imports neither the model nor solver.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def utility(own: int, other: int, background: F) -> F:
    return F(1, background + 1 + other) if own else F(0)


def remaining(first: int, second: int, background: F) -> F:
    return utility(first, second, background) + utility(second, first, background)


def polynomial(bits: tuple[int, ...]) -> int:
    a, b, t, s, q, r = bits
    return (6*a + 2*b + 2*q + 2*r - 4*a*b + 12*t*s
            - 2*t*q - 2*s*r - 3*t*a - 3*s*a - a*q - a*r - t*r - s*q)


def table_entry(bits: tuple[int, ...]) -> int:
    a, b, t, s, q, r = bits
    if (t, s) == (0, 0):
        return 6 - 2*b + q + r if a else 2*b + 2*q + 2*r
    if (t, s) == (1, 0):
        return 3 - 2*b - q if a else 2*b + r
    if (t, s) == (0, 1):
        return 3 - 2*b - r if a else 2*b + q
    return 12 - 2*b - 2*q - 2*r if a else 12 + 2*b - q - r


def add(*pairs: tuple[F, F]) -> tuple[F, F]:
    return tuple(sum((pair[i] for pair in pairs), F(0)) for i in range(2))


def scale(pair: tuple[F, F], coefficient: F) -> tuple[F, F]:
    return tuple(coefficient * x for x in pair)


def utility_numerator(own: int, other: int) -> tuple[F, F]:
    """Constant and d coefficient over the denominator (d+1)(d+2)."""
    return F(own * (2-other)), F(own)


def symbolic_remainder(bits: tuple[int, ...]) -> tuple[F, F]:
    a, b, t, s, q, r = bits
    U = utility_numerator
    difference = add(U(a, b), U(b, a), U(t, q), U(s, r), U(t, a), U(s, a),
                     scale(add(U(t, s), U(s, t)), F(-2)))
    slacks = add(U(b, a), scale(U(q, a), F(-1)),
                 U(b, a), scale(U(r, a), F(-1)),
                 U(q, t), scale(U(r, t), F(-1)),
                 U(r, s), scale(U(q, s), F(-1)))
    return add(difference, scale(slacks, F(-1, 3)))


def check() -> dict[str, object]:
    table_checks = polynomial_checks = direct_checks = 0
    minimum_polynomial = None
    backgrounds = tuple(map(F, (0, 1, 2, 7, 101, 10**6))) + (F(1, 2), F(4, 3), F(1001, 37))
    for bits in product((0, 1), repeat=6):
        a, b, t, s, q, r = bits
        P = polynomial(bits)
        assert P == table_entry(bits)
        assert P >= 0
        minimum_polynomial = P if minimum_polynomial is None else min(minimum_polynomial, P)
        table_checks += 1

        # Exact affine numerators verify both coefficients for arbitrary d.
        constant, slope = symbolic_remainder(bits)
        assert constant == F(P, 3)
        assert slope == F(3*a+b+q+r, 3)
        assert constant >= 0 and slope >= 0
        polynomial_checks += 1

        for d in backgrounds:
            U = lambda own, other: utility(own, other, d)
            left = (remaining(a, b, d) + U(t, q) + U(s, r) + U(t, a) + U(s, a)
                    - 2*remaining(t, s, d))
            four_slacks = U(b, a) - U(q, a) + U(b, a) - U(r, a)
            four_slacks += U(q, t) - U(r, t) + U(r, s) - U(q, s)
            remainder = F(P + d*(3*a+b+q+r), 3*(d+1)*(d+2))
            assert left == four_slacks/3 + remainder
            assert remainder >= 0
            direct_checks += 1

        # At the root the remaining profit of two players is coverage.
        assert remaining(a, b, F(0)) == int(bool(a or b))
        assert remaining(t, s, F(0)) == int(bool(t or s))

    return {
        "claim": "CA-UNIFORM-PORTFOLIO-TWO",
        "checks": {
            "all_six_theme_memberships": table_checks,
            "complete_eight_case_table_entries": table_checks,
            "symbolic_constant_and_background_slope": polynomial_checks,
            "direct_fraction_identities": direct_checks,
            "root_profit_equals_coverage": 2*table_checks,
        },
        "background_samples": [str(x) for x in backgrounds],
        "minimum_nonnegative_polynomial": minimum_polynomial,
        "all_checks_passed": True,
        "scope": "Exact customer-mask algebra; no game sampling or arbitrary-player inference.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(check(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
