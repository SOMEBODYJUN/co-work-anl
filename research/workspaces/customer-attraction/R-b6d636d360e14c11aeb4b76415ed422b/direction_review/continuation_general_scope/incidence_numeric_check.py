#!/usr/bin/env python3
"""Read-only independent arithmetic audit of incidence-LP draft statements.

This script has no repository imports and writes no evidence files. It attacks
the draft's exact general intermediate claim and checks the published formulas;
it does not search for positive special classes or for a Q-CAG-HALF counterexample.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
import json


def ratio(value):
    return {"exact": str(value), "decimal": str(float(value))}


def old_sum(n, tau):
    return sum((F(1) / (n + (tau - 1) * r) for r in range(1, n + 1)), F())


def product_bound(n, tau):
    product = F(1)
    for r in range(1, n + 1):
        product *= 1 - F(1) / (r * tau)
    return 1 - product


def reverse_half_threshold(n):
    """Numerical inversion of sum_r 1/[n+(tau-1)r]=1/2."""
    with localcontext() as ctx:
        ctx.prec = 60
        lower, upper = Decimal(1), Decimal(10)
        for _ in range(250):
            middle = (lower + upper) / 2
            value = sum(
                (1 / (Decimal(n) + (middle - 1) * Decimal(r))
                 for r in range(1, n + 1)),
                Decimal(0),
            )
            if value >= Decimal("0.5"):
                lower = middle
            else:
                upper = middle
        return str(lower)


def main():
    # Exact LP primal and dual for the published five-maxima pattern.
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2, 3, 4)]
    primal = [F(3, 4)] + [F(1, 4)] * 4
    dual = [F(1, 4)] * 4 + [F(3, 4)]
    primal_loads = [sum(primal[j] for j in edge) for edge in edges]
    dual_loads = [sum(dual[k] for k, edge in enumerate(edges) if j in edge)
                  for j in range(5)]
    assert all(value >= 1 for value in primal_loads)
    assert all(value <= 1 for value in dual_loads)
    assert sum(primal) == sum(dual) == F(7, 4)
    assert min(map(len, edges)) == 2

    sums = {n: old_sum(n, F(3)) for n in range(1, 8)}
    assert all(sums[n] < F(1, 2) for n in range(1, 7))
    assert sums[7] > F(1, 2)
    assert sums[6] == F(2509, 5040)
    assert sums[7] == F(7342919, 14549535)

    # Same exact coefficient as the old direct prefix estimate, contrasted with
    # the stronger already proved product estimate. General dominance is proved
    # in fractional_cover_path_budget.md (16)-(17), not by these finite checks.
    comparisons = {}
    for n in (5, 6, 7):
        direct = old_sum(n, F(3))
        product = product_bound(n, F(3))
        assert product >= direct
        comparisons[n] = {
            "direct_sum": ratio(direct),
            "existing_product": ratio(product),
            "difference": ratio(product - direct),
        }
    assert old_sum(5, F(3)) == F(22003, 45045)
    assert product_bound(5, F(3)) == F(421, 729)

    with localcontext() as ctx:
        ctx.prec = 60
        log3 = Decimal(3).ln()
        rational_log_bound = Decimal(7379) / Decimal(6720)
        trapezoid_n7 = log3 / 2 - Decimal(1) / Decimal(21)
        assert log3 > rational_log_bound
        assert trapezoid_n7 > Decimal("0.5")
        decimal_log3 = str(log3)
        decimal_trapezoid = str(trapezoid_n7)
    rational_n7 = F(7379, 13440) - F(1, 21)
    assert rational_n7 == F(6739, 13440)
    assert rational_n7 - F(1, 2) == F(19, 13440)

    # Literal core double count: the only provider chooses one of two legal
    # two-customer maxima, with exactly one common core customer.
    core, maxima, n = {"x"}, [{"x", "a"}, {"x", "b"}], 1
    actual_payoff = F(len(maxima[0]))
    literal_f = F(1) + F(1)  # private a plus the core x counted by (1)
    literal_claim_rhs = F(len(core), n) + literal_f
    assert actual_payoff == 2 < literal_claim_rhs == 3

    # Distinct from the core typo: the direct f-bound is only a no-follower
    # bound. With disjoint maxima of sizes 100 and 1, a last player responding
    # to B1 repeats B1 since 50>1. The first deviator gets 50, not f1=100.
    first_payoff = F(100, 2)
    last_alternative = F(1)
    assert first_payoff > last_alternative
    assert first_payoff < 100

    result = {
        "status": "all assertions passed",
        "scope": "arithmetic/general-intermediate-claim audit; no Q-CAG-HALF counterexample",
        "star_five_maxima": {
            "tau_exact": str(sum(primal)),
            "primal": list(map(str, primal)),
            "dual": list(map(str, dual)),
            "primal_edge_loads": list(map(str, primal_loads)),
            "dual_vertex_loads": list(map(str, dual_loads)),
            "minimum_noncore_incidence": min(map(len, edges)),
        },
        "tau_three_sums": {n: ratio(value) for n, value in sums.items()},
        "existing_product_comparisons": comparisons,
        "log3": decimal_log3,
        "trapezoid_n7": decimal_trapezoid,
        "rational_n7_bound": ratio(rational_n7),
        "rational_n7_half_margin": ratio(rational_n7 - F(1, 2)),
        "reverse_tau_half_threshold": {
            n: reverse_half_threshold(n) for n in (6, 7)
        },
        "literal_core_counterexample": {
            "provider_count": n,
            "maxima": [sorted(theme) for theme in maxima],
            "actual_payoff": str(actual_payoff),
            "literal_draft_rhs": str(literal_claim_rhs),
        },
        "same_route_follower_counterexample": {
            "provider_count": 2,
            "disjoint_maximal_sizes": [100, 1],
            "deviation_payoff_after_credible_repeat": str(first_payoff),
            "draft_unconditional_f_rhs": "100",
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
