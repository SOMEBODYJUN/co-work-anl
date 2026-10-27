"""Exact audit for a dense seven-maxima, six-provider half certificate.

Scope: every customer has incidence in at least two of the seven distinct
inclusion-maximal coverages.  The rows are the mixed shared floor, the six
final-player BR rows L_j (j=1..6), and the six genuine two-remaining tax rows
T_{0j} (j=1..6).  This is a necessary-row certificate, not a proof for
singleton incidence types.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement

N = 6
S = 7
PAIRS = list(combinations_with_replacement(range(S), 2))
PAIRS.sort()

# Shared part of the seven-maxima mixed floor (the suffix envelope is already
# nondecreasing for n=6): B_t=2/(7n-5t), t<=n-2; B_{n-1}=(n+1)/(n(n+6)).
B = [F(1, 21), F(2, 37), F(1, 16), F(2, 27), F(1, 11), F(7, 72)]

# Multipliers on [M_0,...,M_5,L_0,...,L_6,T_{00},...,T_{66}].
LAM = [F(207,355), F(417,710), F(253,426), F(133,213), F(0), F(0)]
LAM += [F(0), *([F(8,71)] * 6)]  # L_0=0, L_1=...=L_6=8/71
LAM += [F(0), *([F(7,71)] * 6)]  # T_00=0, T_0j=7/71, j=1..6
LAM += [F(0)] * 21
assert len(LAM) == 6 + 7 + 28


def rows(I, E):
    # E is the membership bitmask of positions 0..4.  The final action is
    # B_0 after relabelling, hence position 5 belongs iff 0 in I.
    final = int(bool(I & 1))
    J = E | (final << (N - 1))
    z = J.bit_count()
    share = [F((J >> t) & 1, z) if z else F(0) for t in range(N)]
    m = I.bit_count()
    # All columns here are nonprivate (m>=2).
    M = [share[t] - B[t] for t in range(N)]
    L = [share[-1] - F((I >> j) & 1, E.bit_count() + 1) for j in range(S)]
    h = (E & ((1 << (N - 2)) - 1)).bit_count()
    d = (E >> (N - 2)) & 1
    T = []
    for j, k in PAIRS:
        v = ((I >> j) & 1) + ((I >> k) & 1)
        tax = F(d, (h + 1) * (h + 2))
        T.append(share[-2] + share[-1] - (F(v, h + v) if v else F(0)) + tax)
    return J, [*M, *L, *T]


def main():
    minimum = None
    arg = None
    count = 0
    for I in range(1, 1 << S):
        if I.bit_count() < 2:
            continue
        for E in range(1 << (N - 1)):
            J, coeff = rows(I, E)
            target = F(int(bool(J)), 1) - F(1, 2)
            residual = target - sum(a * b for a, b in zip(LAM, coeff))
            assert residual >= 0, (I, E, J, residual)
            if minimum is None or residual < minimum:
                minimum, arg = residual, (I, E, J)
            count += 1
    expected = F(15591089, 238321440)
    assert count == 3840
    assert minimum == expected, (minimum, expected)
    print({"columns": count, "minimum": str(minimum), "minimum_float": float(minimum), "arg": arg})


if __name__ == "__main__":
    main()
