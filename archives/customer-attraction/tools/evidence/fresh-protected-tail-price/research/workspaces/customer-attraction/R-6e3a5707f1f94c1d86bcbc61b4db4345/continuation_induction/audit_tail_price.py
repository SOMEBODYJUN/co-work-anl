"""Exact finite implementation check; universal statements use the analytic proof.

No game solver or previous proof audit is imported. Run from any directory.
"""

from fractions import Fraction as F
from itertools import product


def main():
    expansion_checks = 0
    for p in range(5):
        for a, b, t1, t2, r1, r2 in product((0, 1), repeat=6):
            alpha = F(a, p + a + b) if a else F(0)
            beta = F(b, p + a + b) if b else F(0)

            def utility(x, y):
                return F(x, p + 1 + y)

            for z1, z2 in ((F(1), F(1)), (F(1, 2), F(1)),
                           (F(1), F(0)), (F(2), F(3))):
                tau = z1 + z2
                s = tau * alpha - z1 * utility(t1, r1) - z2 * utility(t2, r2)
                z = tau * beta - z1 * utility(r1, a) - z2 * utility(r2, a)
                v = z1 * z2 * (utility(r1, t1) - utility(r2, t1)
                               + utility(r2, t2) - utility(r1, t2))
                direct = s + z / (2 * tau) + v / tau
                d, ell = z1 * t1 + z2 * t2, z1 * r1 + z2 * r2
                expanded = (tau * alpha + beta / 2 - d / F(p + 1)
                            - ell / (2 * tau * (p + a + 1))
                            + d * ell / (tau * (p + 1) * (p + 2)))
                assert direct == expanded
                expansion_checks += 1

    corner_checks = 0
    for p, a in product(range(9), (0, 1)):
        for tau in (F(1), F(3, 2), F(2), F(5), F(13)):
            for d, ell in product(sorted({F(0), F(1), tau}), (F(0), tau)):
                r0 = (-d / F(p + 1) - ell / (2 * tau * (p + a + 1))
                      + d * ell / (tau * (p + 1) * (p + 2)))
                assert r0 <= 0
                if p == 0:
                    assert min(F(1), d) + r0 <= F(a, 4)
                corner_checks += 1
    print({"raw_row_expansion_checks": expansion_checks,
           "corner_checks": corner_checks,
           "status": "passed; universal proof is analytic"})


if __name__ == "__main__":
    main()
