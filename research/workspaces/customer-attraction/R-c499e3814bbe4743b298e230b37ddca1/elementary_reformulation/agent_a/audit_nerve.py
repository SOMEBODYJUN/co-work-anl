"""Exact arithmetic check for the six-topic weighted-nerve example.

The general identity is proved in exact_tree_cone_and_nerve.md.
This script only checks its stated six-topic numerical values.
"""

from fractions import Fraction


def main():
    p = 6
    r_plus = {b: 2 + (-1) ** (p - b.bit_count()) for b in range(1, 1 << p)}
    r_minus = {b: 2 - (-1) ** (p - b.bit_count()) for b in range(1, 1 << p)}
    for a in range(1, (1 << p) - 1):
        plus = sum(r for b, r in r_plus.items() if b & a == a)
        minus = sum(r for b, r in r_minus.items() if b & a == a)
        assert plus == minus
    assert all(r in {1, 3} for r in [*r_plus.values(), *r_minus.values()])
    assert r_plus[(1 << p) - 1] == 3
    assert r_minus[(1 << p) - 1] == 1
    assert sum(r_plus.values()) == 125
    assert sum(r_minus.values()) == 127
    for a in range(p):
        plus = sum(
            (Fraction(r, b.bit_count()) for b, r in r_plus.items() if b & (1 << a)),
            Fraction(),
        )
        minus = sum(
            (Fraction(r, b.bit_count()) for b, r in r_minus.items() if b & (1 << a)),
            Fraction(),
        )
        assert plus == Fraction(125, 6)
        assert minus == Fraction(127, 6)
        assert plus - minus == Fraction(-1, 3)
    print("PASS: equal intersection orders 1..5; full intersections 3/1;")
    print("coverage 125/127; each terminal payoff 125/6 versus 127/6.")


if __name__ == "__main__":
    main()
