"""Exact scalar and histogram reconstruction; product closure is proved separately."""

from fractions import Fraction as Q
import json

n = 64
r = n - 1
a, b, d = 63, 2016, 64

# The three constituent states are rebuilt directly from customer groups.
allbig_H = {(1, r): n}
ab_H = {(1, 0): 2}
overlap_H = {(1, r): n - 1, (1, 0): n - 1}


def add_histogram(*parts):
    ans = {}
    for factor, histogram in parts:
        for cell, count in histogram.items():
            ans[cell] = ans.get(cell, 0) + factor * count
    return ans


low_H = add_histogram((a, allbig_H), (b, ab_H))
up_H = add_histogram((d, overlap_H))
assert low_H == up_H == {(1, 63): 4032, (1, 0): 4032}

h = min(Q(j) + Q(n, j) for j in range(1, n + 1))
assert h == 16
low_P = (a + b) * r
low_F = a * (2 * n - h) + b * (2 * r - 1)
lower = low_F - 2 * low_P
root_u = d * (Q(n) - Q(1, n))
delta = d * Q(17 * n - 23, 6)
upper = 2 * root_u - delta
assert (low_P, low_F, lower, root_u, delta, upper) == (
    130977, 259056, -2898, 4095, 11360, -3170)
assert lower - upper == 272

# These differ, explaining why the exact theorem omits b=0 customers.
low_zero_H = {(0, r): b * r, (0, 0): a * r + b * (r - 1)}
up_zero_H = {(0, r): d * n * (n - 2), (0, 0): d * n * (n - 2)}
assert low_zero_H != up_zero_H

print(json.dumps(dict(
    scope="Exact products of analytic full-SPE families; no explicit product-tree enumeration",
    component_multiplicities=dict(allbig=a, AB=b, overlap=d),
    common_remaining_players=r,
    common_background_histogram={str(k): v for k, v in low_H.items()},
    low_tail_profit=low_P, low_optimal_tail_profit=str(low_F), lower_credit_bound=str(lower),
    upper_root_payoff=str(root_u), upper_root_profit_drop=str(delta), upper_credit_bound=str(upper),
    contradiction_gap=str(lower - upper),
    low_ignored_zero_background={str(k): v for k, v in low_zero_H.items()},
    upper_ignored_zero_background={str(k): v for k, v in up_zero_H.items()}), indent=2))
