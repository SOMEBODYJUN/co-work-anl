from fractions import Fraction as F
from itertools import combinations_with_replacement

N = 6
S = 7
PRIVATE = [F(1, 12)] * N
SHARED = [F(2, 42 - 5 * t) for t in range(N - 1)] + [F(7, 72)]
PAIRS = list(combinations_with_replacement(range(S), 2))

# Rows are M_0..M_5, L_0..L_6, then T_{jk}.
LAM = [F(17, 28), F(58, 95), F(49, 78), F(27, 41), F(0), F(0)]
LAM += [F(0), *([F(9, 98)] * 5), F(1, 5)]
LAM += [F(0), *([F(9, 83)] * 5), *([F(0)] * 22)]
assert len(LAM) == 6 + 7 + 28


def allowed(I, E):
    # Included singleton I={1},...,{5}: first four or penultimate position 4.
    if I.bit_count() != 1 or I in (1, 1 << 6):
        return True
    return bool(E & 0b1111) or bool(E & (1 << 4))


def rows(I, E):
    final = int(bool(I & 1))
    J = E | (final << 5)
    z = J.bit_count()
    share = [F((J >> t) & 1, z) if z else F(0) for t in range(N)]
    floor = PRIVATE if I.bit_count() == 1 else SHARED
    out = [share[t] - floor[t] for t in range(N)]
    out += [share[-1] - F((I >> j) & 1, E.bit_count() + 1)
            for j in range(S)]
    p = (E & 15).bit_count()
    d = (E >> 4) & 1
    for j, k in PAIRS:
        v = ((I >> j) & 1) + ((I >> k) & 1)
        comparison = F(v, p + v) if v else F(0)
        out.append(share[-2] + share[-1] - comparison
                   + F(d, (p + 1) * (p + 2)))
    return J, out


def main():
    count = 0
    minimum = None
    witness = None
    for I in range(1, 1 << S):
        for E in range(1 << (N - 1)):
            if not allowed(I, E):
                continue
            J, coeff = rows(I, E)
            target = F(int(bool(J)), 1)
            if I != (1 << 6):
                target -= F(1, 2)
            residual = target - sum(a * b for a, b in zip(LAM, coeff))
            if residual < 0:
                raise AssertionError((I, E, J, residual))
            if minimum is None or residual < minimum:
                minimum, witness = residual, (I, E, J)
            count += 1
    expected = F(3538309, 71456112)
    assert count == 4059, count
    assert minimum == expected, (minimum, expected, witness)
    print({"status": "passed", "columns": count, "minimum": str(minimum),
           "witness": witness})


if __name__ == "__main__":
    main()
