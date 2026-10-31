"""Exact candidate attack: sum of row maxima versus adjacent-exit wallet.

This script checks one explicitly supplied 10-unit-customer instance and
one explicitly supplied full-history strategy. It performs no search for
instances, policies, or special-size positive results.
"""

from fractions import Fraction as F
from itertools import product, permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LABELS = ("C", "A", "B", "D")
CUSTOMERS = [frozenset((0, 1, 2)) for _ in range(6)] + [
    frozenset((1,)), frozenset((2, 3)),
    frozenset((3,)), frozenset((3,)),
]
SECOND = (0, 1, 2, 1)
LAST = ((3, 2, 1, 1), (2, 2, 2, 2),
        (1, 1, 1, 1), (1, 2, 1, 1))
M = 3


def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return SECOND[h[0]]
    return LAST[h[0]][h[1]]


def finish(h):
    h = tuple(h)
    while len(h) < M:
        h += (action(h),)
    return h


def utility(z, i):
    return sum((F(1, sum(a in x for a in z))
                for x in CUSTOMERS if z[i] in x), F(0))


def welfare(z):
    return sum(any(a in x for a in z) for x in CUSTOMERS)


def main():
    comparisons = 0
    ic_min = None
    prescribed_table = []
    for depth in range(M):
        for h in product(range(4), repeat=depth):
            actual_leaf = finish(h)
            actual_pay = utility(actual_leaf, depth)
            deviations = []
            for a in range(4):
                leaf = finish(h + (a,))
                pay = utility(leaf, depth)
                slack = actual_pay - pay
                assert slack >= 0, (h, a, slack)
                ic_min = slack if ic_min is None else min(ic_min, slack)
                comparisons += 1
                deviations.append(str(pay))
            prescribed_table.append({
                "history": [LABELS[a] for a in h],
                "action": LABELS[action(h)],
                "true_deviation_profits": deviations,
            })
    actual = finish(())
    profits = [utility(actual, i) for i in range(M)]
    W = welfare(actual)
    frozen = [[utility(actual[:i] + (a,) + actual[i+1:], i)
               for a in range(4)] for i in range(M)]
    row_max = [max(row) for row in frozen]
    adjacent = []
    for i in range(M-1):
        adjacent.append(sum((F(1, c*(c+1))
            for x in CUSTOMERS
            if actual[i] in x and actual[i+1] not in x
            for c in [sum(a in x for a in actual)]), F(0)))
    regret_sum = sum(row_max, F(0)) - W
    wallet = sum(adjacent, F(0))
    assert regret_sum > wallet
    all_tuples = list(product(range(4), repeat=M))
    OPT = max(map(welfare, all_tuples))
    optimal_multisets = sorted({tuple(sorted(z)) for z in all_tuples
                               if welfare(z) == OPT})
    matching = []
    for z in optimal_multisets:
        values = [(sum((frozen[i][a] for i, a in enumerate(p)), F(0)), p)
                  for p in sorted(set(permutations(z)))]
        value, perm = min(values)
        matching.append({"optimal_multiset": [LABELS[a] for a in z],
                         "best_assignment": [LABELS[a] for a in perm],
                         "minimum_Q": str(value)})
    report = {
        "status": "exact_counterexample_to_strong_adjacent_rowmax_only",
        "general_half": "OPEN",
        "weak_optimal_assignment_adjacent_budget": "not_refuted",
        "candidate": "sum_i max_T f_i(T)-W <= sum_j C_j",
        "labels": LABELS,
        "unit_customers": [sorted(x) for x in CUSTOMERS],
        "players": M,
        "actual": [LABELS[a] for a in actual],
        "actual_profits": list(map(str, profits)),
        "W": W, "OPT": OPT,
        "full_ordered_decision_histories": len(prescribed_table),
        "all_true_IC_including_self": comparisons,
        "minimum_IC_slack": str(ic_min),
        "frozen_payoff_matrix": [[str(v) for v in row] for row in frozen],
        "frozen_row_maxima": list(map(str, row_max)),
        "sum_static_row_regrets": str(regret_sum),
        "adjacent_wallets": list(map(str, adjacent)),
        "total_adjacent_wallet": str(wallet),
        "strict_candidate_violation": str(regret_sum-wallet),
        "optimal_assignments": matching,
        "complete_strategy_true_payoffs": prescribed_table,
    }
    output = HERE / "compact_adjacent_counterexample_exact.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "status", "actual", "actual_profits", "W", "OPT",
        "full_ordered_decision_histories", "all_true_IC_including_self",
        "sum_static_row_regrets", "total_adjacent_wallet",
        "strict_candidate_violation", "optimal_assignments")}, indent=2))


if __name__ == "__main__":
    main()
