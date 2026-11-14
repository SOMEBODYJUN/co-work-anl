"""Exact scalar projections of the frozen R275 no-floor point."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import sys

repo = Path(sys.argv[1]).resolve()
archive = repo / "archives/customer-attraction"
frozen = archive / "tools/evidence/R275-credible-search-20261031/original/633b64cbcf0233d0f667__submodular_joint_m5p7_q32.json"
shared = archive / "tools/evidence/shared-root-exact61-primary/original/dual/exact_shared_root.json"

frozen_bytes = frozen.read_bytes()
assert sha256(frozen_bytes).hexdigest() == "dbf83fe8561340f29505cb33e37c83cf79e521ab2c1bcb4f5dd959d2b0968d6d"
data = json.loads(frozen_bytes)
values = {
    tuple(orbit): Fraction(value)
    for orbit, value in zip(data["moment_orbits"], data["exact_candidate"]["values"], strict=True)
}
labels = tuple(range(data["milp"]["topics"]))
actual = tuple(data["milp"]["path"])
portfolio = tuple(data["milp"]["portfolio"])
occupied = set(actual)
outside = set(portfolio)
assert occupied == {0, 1} and len(outside) == 5


def coverage(support):
    support = set(support)
    if not support:
        return Fraction(0)
    assert len(support) <= len(actual)
    return values[(sum(1 << label for label in support & occupied), len(support & outside))]


def utility(first, other_players):
    n = len(other_players) + 1
    return sum(
        (coverage((*predecessors, first)) - coverage(predecessors)) / (n * comb(n - 1, size))
        for size in range(n)
        for predecessors in combinations(other_players, size)
    )


def safe_query(t, q):
    return Fraction(4, 5) * (coverage({t, q}) - coverage({t})) + coverage({q}) / 5


def intersection(a, b):
    return coverage({a}) + coverage({b}) - coverage({a, b})


welfare = coverage(actual)
optimum = max(coverage(support) for size in range(6) for support in combinations(labels, size))
capacity = max(coverage({label}) for label in labels)
root_payoff = utility(actual[0], actual[1:])
assert (welfare, optimum, capacity, root_payoff) == (1, 2, 1, Fraction(1, 5))
assert coverage(portfolio) == optimum

direct_lhs_minus_rhs = {
    str(i): a * optimum + b * capacity - c * root_payoff
    for i, (a, b, c) in enumerate([
        (12380, 26881, 326100),
        (23888, 64639, 678285),
        (1753, 4851, 50200),
        (3506, 29147, 178180),
        (5365, 56053, 328550),
    ], start=1)
}
assert tuple(direct_lhs_minus_rhs.values()) == (-13579, -23242, -1683, 523, 1073)

four_tail_gap = 1000000 * optimum + 7896499 * capacity - 48741762 * root_payoff
four_tail_weak_gap = optimum + 8 * capacity - 50 * root_payoff
assert four_tail_gap == Fraction(740733, 5) and four_tail_weak_gap == 0

third_gaps = {
    (t, q): 763 * safe_query(t, q) - (11033 * root_payoff + 2085 * capacity - 4139 * coverage({t}))
    for t, q in product(labels, repeat=2)
}
assert len(third_gaps) == 49 and max(third_gaps.values()) == 0
assert [key for key, gap in third_gaps.items() if gap == 0] == [(t, q) for t in (0, 1) for q in labels]
third_portfolio = sum(safe_query(actual[0], q) for q in portfolio)
third_portfolio_required = optimum - Fraction(4, 5) * capacity
third_aggregate_gap = 3815 * optimum + 48298 * capacity - 275825 * root_payoff
assert (third_portfolio, third_portfolio_required, third_aggregate_gap) == (1, Fraction(6, 5), 763)

shared_bytes = shared.read_bytes()
assert sha256(shared_bytes).hexdigest() == "bfc96c49c3b6da6edb76e8bbb5708672aad00965b03d922e720372121a663e44"
shared_data = json.loads(shared_bytes)
beta = Fraction(shared_data["dual_beta"])
assert 2 < beta < Fraction(5043, 2500)
multipliers = shared_data["integer_multipliers"]
capacity_rows = {
    "MAX:fixed:2": 1, "MAX:fixed:6": 1, "MAX:fixed:7": 1, "MAX:fixed:8": 1, "MAX:fixed:9": 1,
    "KRS:fixed:3:4": 78, "KRS:fixed:5:3": 78, "KCAP:4": -88940,
}
assert len(multipliers) == 61 and all(int(value) > 0 for value in multipliers.values())
assert sum(int(multipliers[key]) * coefficient for key, coefficient in capacity_rows.items()) == 0
assert beta == Fraction(int(shared_data["beta_numerator"]), int(shared_data["common_denominator"]))
assert beta * welfare - optimum > 0

pair_separator = (
    coverage({0}) - sum(intersection(0, q) for q in portfolio)
    + sum(intersection(q, r) for q, r in combinations(portfolio, 2))
)
boolean_values = [z - z * count + comb(count, 2) for z, count in product((0, 1), range(6))]
assert min(boolean_values) == 0 and pair_separator == -Fraction(1, 4)
a, b = {0, 2, 3, 4, 5}, {0, 2, 3, 4, 6}
extension_bound = coverage(a) + coverage(b) - coverage(a & b)
assert extension_bound == Fraction(7, 4) < coverage(portfolio)

print(json.dumps({
    "welfare": str(welfare),
    "optimal_welfare": str(optimum),
    "maximum_singleton": str(capacity),
    "first_payoff": str(root_payoff),
    "direct_lhs_minus_rhs": {key: str(value) for key, value in direct_lhs_minus_rhs.items()},
    "four_tail_lhs_minus_rhs": str(four_tail_gap),
    "four_tail_weaker_lhs_minus_rhs": str(four_tail_weak_gap),
    "third_safe_pair_lhs_minus_rhs": {f"{t},{q}": str(gap) for (t, q), gap in third_gaps.items()},
    "third_portfolio_sum": str(third_portfolio),
    "third_portfolio_lower_bound_in_unit_domain": str(third_portfolio_required),
    "third_maximum_root_aggregate_lhs_minus_rhs": str(third_aggregate_gap),
    "shared_k_beta": str(beta),
    "shared_k_cancellation": 0,
    "shared_k_welfare_rhs_minus_lhs": str(beta * welfare - optimum),
    "quadratic_boolean_separator": str(pair_separator),
    "hypothetical_global_submodular_extension_upper_bound": str(extension_bound),
}, indent=2, ensure_ascii=False))
