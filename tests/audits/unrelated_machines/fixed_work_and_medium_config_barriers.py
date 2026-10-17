#!/usr/bin/env python3
"""Exact small checks for fixed-work and medium-config method boundaries.

These checks support the stated parameterized proofs; they are not a proof of the
universal claims.  All arithmetic is Fraction, and every enumerated assignment is
rechecked from the explicit machine loads.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product


def private_leaf_states(h: int, q: int):
    t = Fraction(h - 1, h * q)
    # Machine order: cores, then leaves; B is assigned to one core and every tiny
    # chooses its home core (0) or its private leaf (1).
    states = []
    for b in range(h):
        for bits in product((0, 1), repeat=h * q):
            loads = [Fraction(0)] * (h + h * q)
            loads[b] += 1
            pos = 0
            for i in range(h):
                for r in range(q):
                    if bits[pos] == 0:
                        loads[i] += t
                    else:
                        loads[h + i * q + r] += 1
                    pos += 1
            states.append((max(loads), sum(loads), b, bits, loads))
    return t, states


def check_private_family() -> None:
    for h, q in ((2, 1), (2, 2), (3, 1), (3, 2)):
        t, states = private_leaf_states(h, q)
        opt = min(row[0] for row in states)
        assert opt == 1
        bad_peak = Fraction(2) - Fraction(1, h)
        assert min(row[1] for row in states if row[0] == bad_peak) == h
        bad = {row[0] for row in states if row[1] == h}
        assert bad == {Fraction(2) - Fraction(1, h)}
        for C in {row[0] for row in states}:
            if 1 <= C <= Fraction(2) - Fraction(1, h):
                required = (Fraction(2) - Fraction(1, h) - C) / t
                R = (required.numerator + required.denominator - 1) // required.denominator
                formula = h + (1 - t) * R
                actual = min(row[1] for row in states if row[0] <= C)
                assert actual == formula, (h, q, C, actual, formula)

    h, q = 2, 4
    _, states = private_leaf_states(h, q)
    phi = lambda x: x * x
    min_phi = min(sum(phi(x) for x in row[4]) for row in states)
    min_phi_C = {row[0] for row in states if sum(phi(x) for x in row[4]) == min_phi}
    assert min_phi_C == {Fraction(3, 2)}


def check_medium_config_boundary() -> None:
    T = Fraction(5, 4)
    opt = Fraction(7, 4)
    ratio = opt / T
    assert ratio == Fraction(7, 5)
    for alpha in (Fraction(1, 6), Fraction(1, 10), Fraction(1, 100)):
        assert Fraction(1, 4) > alpha * T
        assert ratio > 1 + alpha


if __name__ == "__main__":
    check_private_family()
    check_medium_config_boundary()
    print("ok: private_leaf=(h,q) {(2,1),(2,2),(3,1),(3,2)}; convex=(2,4), f=L^2; medium=k4 alpha={1/6,1/10,1/100}")
