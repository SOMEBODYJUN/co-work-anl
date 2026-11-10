"""Verify the rational three-player specialization of last_three_lp.py."""
from fractions import Fraction
from itertools import product


def share(member, load):
    return Fraction(member, load) if member else Fraction(0)


def remainder(memberships, comparison_count, actual_reply_count):
    current, penultimate, last, branch_second, branch_last = memberships
    actual_load = current + penultimate + last
    branch_load = last + branch_second + branch_last
    current_share = share(current, actual_load)
    last_share = share(last, actual_load)
    branch_last_share = share(branch_last, branch_load)
    d, ell = comparison_count, actual_reply_count

    actual_menu = (
        3 * share(penultimate, actual_load) + last_share / 2
        - Fraction(d, current + 1) - Fraction(ell, 6 * (current + penultimate + 1))
        + Fraction(d * ell, 3 * (current + 1) * (current + 2))
    )
    source = current_share - share(last, branch_load)
    floor_second = current_share - Fraction(branch_second, 3)
    floor_last = current_share - Fraction(branch_last, 3)
    actual_last_comparisons = 3 * last_share - Fraction(d, current + penultimate + 1)
    branch_last_comparisons = 3 * branch_last_share - Fraction(d, last + branch_second + 1)
    payment = (
        Fraction(20, 51) * actual_menu
        + Fraction(79, 102) * source
        + Fraction(1, 34) * floor_second
        + Fraction(3, 17) * floor_last
        + Fraction(10, 17) * actual_last_comparisons
        + Fraction(1, 51) * branch_last_comparisons
    )
    return Fraction(5, 3) * bool(actual_load) - bool(d) - payment


def main():
    all_remainders = []
    minimum_by_membership = []
    for memberships in product(range(2), repeat=5):
        # The branch reply count has zero coefficient. Keep both endpoints
        # to match the full enlarged coefficient domain of the original generator.
        remainders = [
            remainder(memberships, d, ell)
            for d, ell, _ in product((0, 1, 3), (0, 3), (0, 3))
        ]
        all_remainders.extend(remainders)
        minimum_by_membership.append(612 * min(remainders))

    expected = [
        0, 0, 0, 18, 288, 69, 55, 0, 60, 60, 60, 78, 288, 69, 55, 0,
        120, 120, 120, 138, 288, 69, 55, 0, 0, 0, 0, 18, 288, 69, 55, 0,
    ]
    assert minimum_by_membership == expected
    assert len(all_remainders) == 384
    assert min(all_remainders) == 0
    assert all_remainders.count(0) == 40
    print("384 rational endpoint inequalities, minimum 0, 40 equalities")
    print("612 times each membership minimum:", expected)


if __name__ == "__main__":
    main()
