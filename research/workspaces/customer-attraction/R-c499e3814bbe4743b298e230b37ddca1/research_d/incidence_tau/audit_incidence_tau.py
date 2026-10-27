"""Exact audit for the independent six-player incidence-LP reconstruction.

This checks the rational numerical threshold and explicit incidence-cover
certificates. The proof of the SPE bound is in README.md; this script does
not enumerate strategies or claim the unrestricted Q-CAG-HALF-6 theorem.
"""
from fractions import Fraction as F
from itertools import combinations


def coeff(tau):
    return sum((F(1, 6 + (tau - 1) * r) for r in range(1, 7)), F(0))


def check_min_incidence(s, d):
    """alpha_j=1/d covers every nonempty incidence of size >=d."""
    alpha = [F(1, d)] * s
    checked = 0
    for k in range(d, s + 1):
        for I in combinations(range(s), k):
            assert sum((alpha[j] for j in I), F(0)) >= 1
            checked += 1
    return checked, sum(alpha, F(0))


def main():
    tau = F(149, 50)
    c = coeff(tau)
    assert c == F(1006430343355, 2012347307572)
    assert 2 * c - 1 == F(256689569, 1006173653786)

    source_tau = F(8, 3)
    source_c = coeff(source_tau)
    assert source_c == F(12494367, 23150512)
    assert 2 * source_c - 1 == F(919111, 11575256)

    boundary = coeff(F(3, 1))
    assert boundary == F(2509, 5040)
    assert 2 * boundary - 1 == -F(11, 2520)

    # The sum is decreasing in tau, so this one exact endpoint certifies all
    # tau <=149/50. These explicit hypergraph covers show the structural cases.
    cases = []
    for s, d in ((8, 3), (11, 4), (14, 5)):
        checked, total = check_min_incidence(s, d)
        assert total <= tau
        cases.append((s, d, checked, str(total)))

    print({
        "tau_endpoint": str(tau),
        "coefficient": str(c),
        "margin_2c_minus_1": str(2 * c - 1),
        "source_tau_8_over_3_coefficient": str(source_c),
        "tau_3_coefficient": str(boundary),
        "structural_cases": cases,
    })


if __name__ == "__main__":
    main()
