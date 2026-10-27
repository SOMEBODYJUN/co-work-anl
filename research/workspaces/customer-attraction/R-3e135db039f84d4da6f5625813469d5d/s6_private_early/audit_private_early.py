"""Exact certificate for a conditional seven-maxima, six-provider subclass.

The actual final maximal action is B0.  An optimal six-maxima portfolio is
B0,...,B5 (B6 is omitted).  Every singleton-incidence customer in B1,...,B5
is assumed to be covered by one of the first four actual providers.  Singleton
customers of B0 are covered by the final action; singleton customers of B6
are outside the chosen optimum and are unrestricted.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement

N = 6
S = 7

# n=6,s=7 suffix floors.  For a singleton incidence use the private floor
# alpha_t=min_{q>=t} A_q=1/12.  For incidences of size >=2 use the shared
# floor beta_t=2/(42-5t), with the final value 7/72.
PRIVATE = [F(1, 12)] * N
SHARED = [F(2, 42 - 5*t) for t in range(N-1)] + [F(7, 72)]

# Rows: M_0,...,M_5, L_0,...,L_6, then T_{jk}, 0<=j<=k<=6.
LAM = [F(207,355), F(417,710), F(253,426), F(133,213), F(0), F(0)]
LAM += [F(0)] + [F(8,71)] * 6
LAM += [F(0)] + [F(7,71)] * 6 + [F(0)] * 21
PAIRS = list(combinations_with_replacement(range(S), 2))


def row_coefficients(I, E):
    """Return actual membership J and all valid row coefficients."""
    final = int(bool(I & 1))  # final action is B0
    J = E | (final << (N - 1))
    z = J.bit_count()
    share = [F((J >> t) & 1, z) if z else F(0) for t in range(N)]
    singleton = I.bit_count() == 1
    floor = PRIVATE if singleton else SHARED
    rows = [share[t] - floor[t] for t in range(N)]

    rows += [share[-1] - F((I >> j) & 1, E.bit_count() + 1)
             for j in range(S)]

    p = (E & ((1 << (N - 2)) - 1)).bit_count()
    d = (E >> (N - 2)) & 1
    for j, k in PAIRS:
        v = ((I >> j) & 1) + ((I >> k) & 1)
        comparison = F(v, p + v) if v else F(0)
        rows.append(share[-2] + share[-1] - comparison
                    + F(d, (p + 1) * (p + 2)))
    return J, rows


def allowed(I, E):
    """Singleton B1..B5 customers must appear among first four positions."""
    if I.bit_count() != 1 or I == (1 << 6) or I == 1:
        return True
    return bool(E & 0b1111)


def main():
    count = 0
    minimum = None
    witness = None
    for I in range(1, 1 << S):
        for E in range(1 << (N - 1)):
            if not allowed(I, E):
                continue
            J, rows = row_coefficients(I, E)
            # The chosen optimum omits B6.  A singleton I={6} therefore
            # contributes W but zero to OPT; all other incidences contribute
            # 1/2 when actually covered and -1/2 when uncovered.
            target = F(int(bool(J)), 1)
            if I != (1 << 6):
                target -= F(1, 2)
            residual = target - sum(a*b for a, b in zip(LAM, rows))
            if residual < 0:
                raise AssertionError((I, E, J, residual))
            if minimum is None or residual < minimum:
                minimum, witness = residual, (I, E, J)
            count += 1
    expected = F(49, 2130)
    assert count == 4054, count
    assert minimum == expected, (minimum, expected, witness)
    print({"status": "passed", "columns": count, "minimum": str(minimum),
           "witness": witness})


if __name__ == "__main__":
    main()
