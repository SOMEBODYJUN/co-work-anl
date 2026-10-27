"""Exact obstruction to a naive seven-maxima extension of the joint rows.

This is a barrier certificate, not a customer-attraction counterexample.
It uses the six-provider route a=(0,0,0,0,1,0), seven maximal-set labels,
the natural seven-maxima mixed floors, all seven final-player BR rows and
all 28 two-player tax rows.  The listed nonnegative rational combination of
columns has nonnegative average coefficient in every row but negative average
target base, so no nonnegative combination of these rows can prove W-U/2>=0
on this route domain.
"""

from fractions import Fraction as F
from itertools import combinations_with_replacement

Q = 7
N = 6
ROUTE = (0, 0, 0, 0, 1, 0)
PAIRS = list(combinations_with_replacement(range(Q), 2))


def rows(incidence: int, true_membership: int):
    """Return the 41 exact slack coefficients for one customer column."""
    count = true_membership.bit_count()
    pay = [
        F((true_membership >> t) & 1, count) if count else F(0)
        for t in range(N)
    ]
    incidence_size = incidence.bit_count()
    out = []
    for t in range(N):
        if incidence_size == Q:
            floor = F(1, N)  # core
        elif incidence_size == 1:
            floor = F(1, 2 * N)  # globally private
        elif t < N - 1:
            denominator = max(
                F(t) + F(Q * (N - t), 2),
                F(N + Q - 1),
            )
            floor = 1 / denominator
        else:
            # Seven-maxima version of (n+1)/(n(n+s-1)).
            floor = F(N + 1, N * (N + Q - 1))
        out.append(pay[t] - floor)

    prior = (true_membership & ((1 << (N - 1)) - 1)).bit_count()
    out.extend(
        pay[-1] - F((incidence >> j) & 1, prior + 1)
        for j in range(Q)
    )

    prefix = (true_membership & ((1 << (N - 2)) - 1)).bit_count()
    tax = F((true_membership >> (N - 2)) & 1, (prefix + 1) * (prefix + 2))
    suffix = pay[-2] + pay[-1]
    for first, second in PAIRS:
        covers = ((incidence >> first) & 1) + ((incidence >> second) & 1)
        comparison = F(covers, prefix + covers) if covers else F(0)
        out.append(suffix + tax - comparison)
    assert len(out) == 6 + 7 + 28
    return out


def columns():
    """All broadened true-membership columns for ROUTE.

    An incidence mask is a nonempty subset of the seven maximal labels.  A
    true membership bit is allowed only at a route position whose assigned
    maximal label contains the customer.  The final action is maximal, so its
    membership bit is forced to equal the incidence bit of ROUTE[-1].
    """
    result = []
    for incidence in range(1, 1 << Q):
        eligible = 0
        for position, label in enumerate(ROUTE):
            if (incidence >> label) & 1:
                eligible |= 1 << position
        required_last = bool((incidence >> ROUTE[-1]) & 1)
        subset = eligible
        while True:
            if bool((subset >> (N - 1)) & 1) == required_last:
                result.append((incidence, subset))
            if subset == 0:
                break
            subset = (subset - 1) & eligible
    return result


# These are the exact support columns of a dual solution.  Masks are printed
# in binary in the note below; the integer masks are less error-prone here.
SUPPORT = [
    (1, 40), (1, 32), (2, 16), (2, 0), (3, 63), (4, 0),
    (5, 46), (5, 44), (8, 0), (9, 47), (16, 0), (17, 47),
    (32, 0), (33, 47), (64, 0), (65, 47), (65, 44),
]
WEIGHTS = [
    F(21238, 2249025), F(78121, 2998700), F(300193, 7496750),
    F(300193, 14993500), F(1947217, 7496750), F(754001, 7496750),
    F(7872, 749675), F(1082, 149935), F(444629, 4498050),
    F(25333, 749675), F(444629, 4498050), F(25333, 749675),
    F(444629, 4498050), F(25333, 749675), F(223484, 2249025),
    F(38971, 1499350), F(2339, 749675),
]


def main():
    cols = columns()
    assert all(column in cols for column in SUPPORT)
    assert sum(WEIGHTS, F(0)) == 1
    averages = [
        sum((weight * rows(*column)[j] for weight, column in zip(WEIGHTS, SUPPORT)), F(0))
        for j in range(41)
    ]
    base_average = sum(
        (weight * (F(int(true != 0)) - F(1, 2))
         for weight, (_, true) in zip(WEIGHTS, SUPPORT)),
        F(0),
    )
    assert min(averages) >= 0
    assert base_average == F(-148577, 8996100)
    print({
        "status": "passed",
        "route": ROUTE,
        "column_count": len(cols),
        "support_count": len(SUPPORT),
        "base_average": str(base_average),
        "minimum_row_average": str(min(averages)),
        "row_count": len(averages),
    })


if __name__ == "__main__":
    main()
