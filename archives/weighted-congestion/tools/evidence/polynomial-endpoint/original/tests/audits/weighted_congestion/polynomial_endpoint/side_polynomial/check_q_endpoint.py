"""Exact rational sanity checks for WC-R1-Q-ENDPOINT v1.

The general proof is Q_ENDPOINT_REDUCTION.md. This finite check verifies
formula implementation and margin identities; it is not the proof.
"""
from fractions import Fraction as F


def value(coeff, x):
    return sum((a * x**j for j, a in enumerate(coeff)), F(0))


def endpoint(coeff, w):
    degree = len(coeff) - 1
    s = 1 + w
    a = s**degree
    c = (a * value(coeff, F(1)) - value(coeff, s)) / (a - 1)
    b = (value(coeff, s) - value(coeff, F(1))) / (a - 1)
    return c, b


def margins(p, q, n, w, alpha):
    h = value(p, F(1)) + n * value(q, 1 + w)
    h -= alpha * (value(p, 1 + n * w) + n * value(q, F(1)))
    l = value(p, 1 + w) + value(q, w)
    l -= alpha * (value(p, n * w) + value(q, 1 + w))
    return h, l


checked = 0
for d in range(1, 13):
    for denominator in range(1, 13):
        for numerator in range(1, denominator + 1):
            w = F(numerator, denominator)
            for j in range(d + 1):
                q = [F(0)] * (d + 1)
                q[j] = F(1)
                c, b = endpoint(q, w)
                assert c >= 0 and b >= 0
                qt = [c] + [F(0)] * (d - 1) + [b]
                assert value(qt, F(1)) == value(q, F(1))
                assert value(qt, 1 + w) == value(q, 1 + w)
                assert value(qt, w) >= value(q, w)
                checked += 1

            # A mixed example checks all coefficient sums and both margins.
            p = [F((7 * j + 3) % 11, j + 1) for j in range(d + 1)]
            q = [F((3 * j + 5) % 13, j + 2) for j in range(d + 1)]
            c, b = endpoint(q, w)
            qp = [F(0)] * d + [b]
            delta = c + b * w**d - value(q, w)
            assert delta >= 0
            for n in (1, 2, 7):
                for alpha in (F(3, 2), F(2), F(17, 3)):
                    old_h, old_l = margins(p, q, n, w, alpha)
                    new_h, new_l = margins(p, qp, n, w, alpha)
                    assert new_h == old_h + n * (alpha - 1) * c
                    assert new_l == old_l + delta + (alpha - 1) * c
                    checked += 1

# Exact boundary counterexample: extending at fixed P to w > 1 fails.
p = [F(0), F(0), F(9, 40)]
q = [F(0), F(1), F(0)]
assert value(p, F(1)) + value(q, F(3)) == F(129, 40)
assert value(p, F(3)) + value(q, F(1)) == F(121, 40)
assert value(p, F(3)) + value(q, F(2)) == F(161, 40)
assert value(p, F(2)) + value(q, F(3)) == F(156, 40)
assert F(129, 121) > F(51, 50)
assert F(161, 156) > F(51, 50)

print(f"PASS: {checked} exact rational endpoint/margin cases; w>1 boundary counterexample")
