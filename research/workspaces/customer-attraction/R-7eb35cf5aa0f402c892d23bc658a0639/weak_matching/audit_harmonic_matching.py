from fractions import Fraction as F
from itertools import product


def harmonic(m):
    return sum((F(1, r) for r in range(1, m + 1)), F(0))


expected = {1: F(0), 2: F(1, 3), 3: F(7, 13), 4: F(23, 35),
            5: F(163, 223), 6: F(71, 91)}
patterns = 0
for m in range(1, 13):
    h = harmonic(m)
    denominator = m - h + 1
    assert denominator > 0
    threshold = 1 - 1 / denominator
    if m in expected:
        assert threshold == expected[m]
    # Work with integer union / difference counts so this is also an exact
    # sanity check on the reparameterization q=W/Q, D=Q-W+A.
    for Q in (1, 7, 13):
        for W in (0, Q // 2, Q, 2 * Q):
            for A in (0, 1, 4):
                D = Q - W + A
                if D < 0:
                    continue
                direct = (Q + (h - 1) * D) / m - (Q - W)
                transformed = (1 - denominator * (1 - F(W, Q))) * Q / m + (h - 1) * A / m
                assert direct == transformed
    if m <= 8:
        for covered in product((0, 1), repeat=m):
            b = 0
            value = F(0)
            for i, indicator in enumerate(covered, 1):
                value += F(1, b + m - i + 1)
                b += indicator
            lower = F(b, m) + h - harmonic(b)
            assert value >= lower >= 1
            if covered == (1,) * b + (0,) * (m - b):
                assert value == lower
            if b == 0:
                assert value == h
            patterns += 1
    print(f'm={m}, H={h}, threshold={threshold}')

assert F(2, 3) > expected[2]
assert F(3, 5) > expected[3]
assert F(750, 1499) < expected[4]
print(f'exact checks passed; {patterns} single-customer position patterns')
