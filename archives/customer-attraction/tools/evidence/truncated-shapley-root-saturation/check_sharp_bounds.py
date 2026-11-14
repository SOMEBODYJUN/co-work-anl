from fractions import Fraction as F
from itertools import combinations
from math import comb
import sympy as sp

m, r = sp.symbols("m r", positive=True)
delta = (m - 2) / (m * (m - 1))
lower = (1 - (m - r) / ((m - 1) * (r + 1))) / r
upper = delta + 1 / ((m - 1) * r)
assert sp.factor(lower - upper - (m - r) * ((m - 2) * r - 2) / (m * (m - 1) * r * (r + 1))) == 0

for m in range(2, 31):
    delta = F(m - 2, m * (m - 1))
    singleton = F(2, m)
    assert (singleton + (m - 1) * delta) / m == F(1, m)
    assert 1 + (m - 1) * delta == 2 - F(2, m)
    assert 1 + m * delta == 2 - F(1, m - 1)
    for k in range(1, m + 1):
        crossing = F(k - 1, m)
        for sum_of_marginals in (F(0), crossing, 2 * crossing + F(1, m * m)):
            assert min(1 + sum_of_marginals, k - (m - 1) * sum_of_marginals) <= 2 - F(1, m)
    assert (m - 1) + F(m, m) == F(m * m, m)
    assert F(2 * m * m - m, m * m) == 2 - F(1, m)
    for r in range(1, m + 1):
        lower = (1 - F(m - r, (m - 1) * (r + 1))) / r
        upper = delta + F(1, (m - 1) * r)
        assert lower - upper == F((m - r) * ((m - 2) * r - 2), m * (m - 1) * r * (r + 1))
        if m >= 4:
            assert lower >= upper


def low_m_check(m):
    old = tuple(range(1, m))
    a = 0
    fresh = m

    def C(xs):
        labels = set(xs)
        if a in labels:
            return 1 + F((m - 2) * (len(labels) - 1), m * (m - 1))
        return F(2 * len(labels), m)

    def utility(query):
        return sum(
            (C((*h, query)) - C(h)) / (m * comb(m - 1, size))
            for size in range(m)
            for h in combinations(old, size)
        )

    assert utility(a) == F(1, 2) < utility(fresh) == F(2, m)


for m in (2, 3):
    low_m_check(m)
print("Symbolic and exact checks passed. The all-A policy fails off-path for m=2,3 in this family.")

# Exhaust the two-label unit example, including both off-path comparisons.
customer_sets = ({0, 1}, {2})
a, b = 0, 1
def two_player_utility(own, other):
    return sum(F(1, 1 + int(customer in customer_sets[other])) for customer in customer_sets[own])

assert two_player_utility(a, a) == two_player_utility(b, a) == 1
assert two_player_utility(a, b) == 2 > two_player_utility(b, b) == F(1, 2)
assert len(customer_sets[a] | customer_sets[b]) == F(3, 2) * len(customer_sets[a])
print("Two-player root-saturated unit witness verified at both legal histories.")
