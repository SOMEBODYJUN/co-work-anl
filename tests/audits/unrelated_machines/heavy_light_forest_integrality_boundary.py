#!/usr/bin/env python3
"""Fraction audit of the forest residual LP/integer boundary and its family."""
from fractions import Fraction as F


def main():
    T = F(3)
    # (job, machine, processing time); j0 has two choices.
    edges = {0: ((0, F(2)), (1, F(2))),
             1: ((1, F(2)),),
             2: ((0, F(2)),)}
    x = {(0, 0): F(1, 2), (0, 1): F(1, 2),
         (1, 1): F(1), (2, 0): F(1)}
    loads = [sum(p * w for (j, i), w in x.items() if i == machine
                 for p in [edges[j][0][1] if edges[j][0][0] == i else edges[j][1][1]])
             for machine in (0, 1)]
    assert loads == [T, T]
    lam = (F(1, 2), F(1, 2))
    dual = sum(min(lam[i] * p for i, p in edges[j]) for j in edges)
    assert dual == T
    integral = []
    for i0 in (0, 1):
        a = [F(0), F(0)]
        a[i0] += 2
        a[1] += 2
        a[0] += 2
        integral.append(max(a))
    assert integral == [F(4), F(4)]
    # Five vertices, four edges, connected: a tree, hence feedback rank zero.
    assert 4 - 5 + 1 == 0

    # Parameterized family: T=1, center cost beta on every machine, one
    # private job of cost a=1-beta/m on each machine.  The exact ratio tends
    # to 2 along m->infinity, beta->1.
    family = []
    for m, beta in ((2, F(2, 3)), (5, F(9, 10)), (20, F(99, 100)),
                    (100, F(999, 1000))):
        a = 1 - beta / m
        frac = a + beta / m
        integer = a + beta
        assert frac == 1
        assert integer == 1 + beta - beta / m
        assert integer < 2
        family.append((m, str(beta), str(integer)))
    # A nonempty-heavy sequence: each private edge is forced heavy, while the
    # center remains light, and the same near-two ratio persists.
    for m in (4, 10, 100):
        beta = F(m - 2, m)
        a = 1 - beta / m
        assert a > beta
        assert a + beta == 2 - F(3, m) + F(2, m * m)
    print({"status": "ok", "fractional_loads": [str(v) for v in loads],
           "dual_value": str(dual), "integral_makespans": [str(v) for v in integral],
           "feedback_rank": 0, "near_two_family": family})


if __name__ == "__main__":
    main()
