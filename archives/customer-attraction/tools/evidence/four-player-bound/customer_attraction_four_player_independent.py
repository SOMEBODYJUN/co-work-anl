"""Independent exact audit of CA-FOUR-UPPER-1499-750.

This file independently transcribes the manuscript definitions.  It imports
neither the search program nor the primary four-player audit.  Its finite
checks verify the displayed universal pointwise identities, not equilibrium
existence or the welfare theorem's quantifiers.
"""

from fractions import Fraction as F
from itertools import product
import json


WEIGHTS = {
    "KC": 341, "KD": 302, "KQ": 306, "KR": 302, "KS": 355,
    "E": 354, "P": 646, "root": 1267,
    "QS": 24, "RC": 8, "RS": 17, "SB": 108,
}
TABLE = (
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


def dividend(member, total):
    # The manuscript uses zero for a zero numerator, even at zero total.
    if not member:
        return F(0)
    assert total > 0
    return F(member, total)


def coefficients(bits):
    a, b, c, d, q, r, s = bits
    actual_total = a + b + c + d
    deviation_total = d + q + r + s
    ua, ub, uc, ud = (dividend(x, actual_total) for x in (a, b, c, d))
    zd, zq, zr, zs = (dividend(x, deviation_total) for x in (d, q, r, s))
    background = a + b
    h = uc + ud + F(c, (background + 1) * (background + 2))
    result = {"K" + name: ub - F(member, a + 3)
              for name, member in zip("CDQRS", (c, d, q, r, s))}
    result.update({
        "P": 2 * h + F(background, background + 1),
        "E": 4 * ud + F(a + b + c, a + b + c + 1),
        "root": ua - zd,
        "QS": zq - F(s, d + 3),
        "RC": zr - F(c, d + q + 2),
        "RS": zr - F(s, d + q + 2),
        "SB": zs - F(b, d + q + r + 1),
    })
    return result


def main():
    residuals = []
    for bits in product((0, 1), repeat=7):
        a, b, c, d, q, r, s = bits
        lhs = F(1499, 750) * bool(a + b + c + d)
        weighted = sum(F(WEIGHTS[k], 1000) * value
                       for k, value in coefficients(bits).items())
        rho = lhs - weighted
        actual_index = 8 * a + 4 * b + 2 * c + d
        deviation_index = 4 * q + 2 * r + s
        assert rho >= 0, (bits, rho)
        assert 12000 * rho == TABLE[actual_index][deviation_index], (bits, rho)
        # Independently varying O isolates its algebraic coefficient.
        for o in (F(-17, 3), F(0), F(5, 7)):
            with_o = dict(coefficients(bits))
            with_o["P"] -= o
            with_o["E"] -= o
            rhs = sum(F(WEIGHTS[k], 1000) * value
                      for k, value in with_o.items()) + rho
            assert lhs - o == rhs, (bits, o, lhs - o, rhs)
        residuals.append(rho)

    pairs_checked = 0
    for a, b, *t in product((0, 1), repeat=6):
        p = a + b
        pair_sum = sum(dividend(t[i] + t[j], p + t[i] + t[j])
                       for i in range(4) for j in range(i + 1, 4))
        lower = 3 * bool(sum(t)) - 3 * F(p, p + 1)
        assert pair_sum >= lower, (a, b, t, pair_sum, lower)
        pairs_checked += 1

    last_checked = 0
    for a, b, c, *t in product((0, 1), repeat=7):
        p = a + b + c
        payoff_sum = F(sum(t), p + 1)
        lower = bool(sum(t)) - F(p, p + 1)
        assert payoff_sum >= lower, (a, b, c, t, payoff_sum, lower)
        last_checked += 1

    general_pair_checked = 0
    general_denominator_checked = 0
    for m in range(1, 10):
        for i in range(1, m + 1):
            remaining = m - i + 1
            for p in range(i):
                assert p + remaining >= 1
                for memberships in range(m + 1):
                    lower = bool(memberships) - F(p, p + remaining)
                    assert remaining * F(memberships, p + remaining) >= lower
                    general_denominator_checked += 1
        if m < 2:
            continue
        for p in range(m - 1):
            for t in product((0, 1), repeat=m):
                pair_sum = sum(dividend(t[i] + t[j], p + t[i] + t[j])
                               for i in range(m) for j in range(i + 1, m))
                lower = (m - 1) * (bool(sum(t)) - F(p, p + 1))
                assert pair_sum >= lower
                general_pair_checked += 1

    assert F(WEIGHTS["P"] + WEIGHTS["E"], 1000) == 1
    assert F(1499, 750) < 2
    print(json.dumps({
        "status": "all exact pointwise checks passed",
        "membership_masks": len(residuals),
        "nonnegative_residuals": len(residuals),
        "minimum_residual": str(min(residuals)),
        "zero_residual_masks": sum(x == 0 for x in residuals),
        "four_optimum_pair_masks": pairs_checked,
        "four_optimum_last_node_masks": last_checked,
        "general_denominator_checks_m_1_to_9": general_denominator_checked,
        "general_pair_checks_m_2_to_9": general_pair_checked,
    }, indent=2))


if __name__ == "__main__":
    main()
