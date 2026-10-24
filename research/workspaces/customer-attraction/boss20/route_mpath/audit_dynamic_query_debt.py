#!/usr/bin/env python3
"""Exact Fraction audit of the dynamic query-debt identity.

This audit samples finite action labels with an arbitrary continuation load h_A(x).
It checks the identity directly from definitions; it is not evidence for the
unrestricted Mpath bridge.
"""
from fractions import Fraction
from random import Random


def check(seed: int = 20261024, trials: int = 5000):
    rng = Random(seed)
    for _ in range(trials):
        actions = tuple(range(rng.randint(2, 8)))
        # Build a rational distribution by integer masses.
        masses = [rng.randint(1, 9) for _ in actions]
        total = sum(masses)
        probs = [Fraction(v, total) for v in masses]
        customers = tuple(range(rng.randint(1, 9)))
        q = {x: Fraction(0) for x in customers}
        # Use a fixed action membership table; each customer's q is exact.
        membership = {
            x: {a: bool(rng.getrandbits(1)) for a in actions}
            for x in customers
        }
        q = {x: sum((probs[a] for a in actions if membership[x][a]), Fraction(0)) for x in customers}
        h = {x: {a: rng.randint(0, 7) for a in actions} for x in customers}
        CminusD = Fraction(0)
        rhs = Fraction(0)
        for x in customers:
            qx = q[x]
            for a in actions:
                I = int(membership[x][a])
                ha = h[x][a]
                CminusD += probs[a] * (qx / (ha + I + 1) - Fraction(I, ha + 1))
            if qx == 0 or qx == 1:
                # The expression below is zero for q=0 and uses only the
                # positive conditional event for q=1.
                if qx == 1:
                    H1 = sum(probs[a] * Fraction(1, h[x][a] + 1)
                             for a in actions if membership[x][a])
                    J1 = sum(probs[a] * Fraction(1, (h[x][a] + 1) * (h[x][a] + 2))
                             for a in actions if membership[x][a])
                    H1 /= qx
                    J1 /= qx
                    rhs += -qx * qx * J1
                continue
            H0 = sum(probs[a] * Fraction(1, h[x][a] + 1)
                     for a in actions if not membership[x][a]) / (1 - qx)
            H1 = sum(probs[a] * Fraction(1, h[x][a] + 1)
                     for a in actions if membership[x][a]) / qx
            J1 = sum(probs[a] * Fraction(1, (h[x][a] + 1) * (h[x][a] + 2))
                     for a in actions if membership[x][a]) / qx
            rhs += qx * (1 - qx) * (H0 - H1) - qx * qx * J1
        assert CminusD == rhs, (CminusD, rhs)
    return {"seed": seed, "trials": trials, "status": "exact_fraction_identity_passed"}


if __name__ == "__main__":
    print(check())
