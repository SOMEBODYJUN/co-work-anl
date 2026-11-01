"""Exact Farkas obstruction for a stronger seven-maxima row family.

This is a mechanism boundary, not a game counterexample.  We fix the
restricted-growth route (0,0,0,0,1,0), six providers, and seven maximal
coverages.  In addition to the earlier mixed-floor M, final-BR L and genuine
two-remaining tax T rows, we add *every* full maximal-deviation floor

    D[t,j] = u_t - sum_{I contains j} 1/(p_I(t)+6-t).

The D rows are valid SPE inequalities: forcing provider t to choose B_j gives
each customer of maximal incidence I containing j denominator at most
p_I(t)+6-t.  The frozen rational column distribution below has nonnegative
average for every one of the 83 rows but negative average for
W-(U-|X_{6}|)/2.  Hence this strengthened row family cannot close the hard
route; no realizable customer instance or strategy is claimed.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement

N, S = 6, 7
ROUTE = (0, 0, 0, 0, 1, 0)
PAIRS = list(combinations_with_replacement(range(S), 2))

# Shared mixed-floor suffix values used by the existing seven-maxima source.
B = [F(1, 21), F(2, 37), F(1, 16), F(2, 27), F(1, 11), F(7, 72)]
PRIVATE = [F(1, 12)] * N

# Column support: (incidence mask I, true path membership mask J, weight).
SUPPORT = [
    (1, 32, F(691907, 21293503)),
    (2, 16, F(119549, 2505118)),
    (2, 0, F(5307287, 127761018)),
    (3, 63, F(903515, 42587006)),
    (4, 0, F(28410365, 255522036)),
    (8, 0, F(28410365, 255522036)),
    (16, 0, F(28410365, 255522036)),
    (32, 0, F(28410365, 255522036)),
    (65, 47, F(5059590, 21293503)),
    (65, 46, F(903286, 21293503)),
    (65, 45, F(9600, 276539)),
    (65, 43, F(208534, 5807319)),
    (65, 36, F(45992, 5807319)),
    (66, 16, F(4517575, 127761018)),
    (68, 0, F(83729, 18251574)),
    (72, 0, F(83729, 18251574)),
    (80, 0, F(83729, 18251574)),
    (96, 0, F(83729, 18251574)),
]


def valid_column(inc, true):
    """Route legality: J is a subset of eligible positions, final is forced."""
    eligible = sum(1 << t for t, j in enumerate(ROUTE) if inc >> j & 1)
    return true & ~eligible == 0 and ((true >> 5) & 1) == (inc & 1)


def row_coefficients(inc, true):
    assert valid_column(inc, true)
    z = true.bit_count()
    pay = [F((true >> t) & 1, z) if z else F(0) for t in range(N)]
    bits = inc.bit_count()

    # M_t: source mixed-floor rows.  Singleton incidence has the private
    # floor 1/12; shared incidence uses the seven-maxima suffix floor B[t].
    M = [pay[t] - (PRIVATE[t] if bits == 1 else B[t]) for t in range(N)]

    # L_j: last-player comparison to maximal B_j.
    prior = (true & ((1 << 5) - 1)).bit_count()
    L = [pay[-1] - F((inc >> j) & 1, prior + 1) for j in range(S)]

    # T_jk: genuine two-remaining tax rows.
    pref = (true & ((1 << 4) - 1)).bit_count()
    d = (true >> 4) & 1
    suff = pay[-2] + pay[-1]
    tax = F(d, (pref + 1) * (pref + 2))
    T = []
    for j, k in PAIRS:
        v = ((inc >> j) & 1) + ((inc >> k) & 1)
        T.append(suff + tax - (F(v, pref + v) if v else F(0)))

    # D_tj: full maximal-deviation floor rows.
    D = []
    for t in range(N):
        r = N - t
        prior_counts = [sum(ROUTE[q] == h for q in range(t)) for h in range(S)]
        for j in range(S):
            c = pay[t]
            if inc >> j & 1:
                pI = sum(prior_counts[h] for h in range(S) if inc >> h & 1)
                c -= F(1, pI + r)
            D.append(c)
    return M + L + T + D


def target(inc, true):
    # OPT portfolio omits maximal B_6; singleton {6} is therefore outside OPT.
    return F(int(bool(true))) - (F(0) if inc == (1 << 6) else F(1, 2))


def main():
    assert sum((w for _, _, w in SUPPORT), F(0)) == 1
    for inc, true, _ in SUPPORT:
        assert valid_column(inc, true), (inc, true)
    rows = [row_coefficients(*SUPPORT[0][:2])]
    row_count = len(rows[0])
    averages = []
    for j in range(row_count):
        averages.append(sum(w * row_coefficients(i, t)[j] for i, t, w in SUPPORT))
    obj = sum(w * target(i, t) for i, t, w in SUPPORT)
    assert min(averages) >= 0, min(averages)
    assert obj == F(-42280, 9125787), obj
    print({
        "status": "passed exact Fraction Farkas obstruction",
        "route": list(ROUTE),
        "columns_in_support": len(SUPPORT),
        "rows": row_count,
        "minimum_row_average": str(min(averages)),
        "target_average": str(obj),
        "scope": "method obstruction only; not a Q-CAG-HALF-6 counterexample",
    })


if __name__ == "__main__":
    main()
