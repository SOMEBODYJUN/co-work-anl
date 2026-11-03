#!/usr/bin/env python3
"""Deterministic exact attack on universal existence of a UV optimum chain.

This reuses the m=4 member of the all-big lower-bound family already described
in co-work-anl/research/questions/customer_attraction_half_coverage.md:23 and in
the reviewed actor's counterexample_attack/owner_tax_exhaustive.py:80-100.
It does not attack the conditional UV=>half implication, THRESHOLD, or half.

Run from any directory. Writes only the requested JSON next to this script.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys

REPO = next(p for p in Path(__file__).resolve().parents if (p / "customer_attraction" / "__init__.py").is_file())
sys.path.insert(0, str(REPO))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()

    # The seven unit clients are individually represented, with disjoint themes.
    interests = (frozenset({0}),) * 4 + tuple(frozenset({a}) for a in (1, 2, 3))
    clients = [f"b{i}" for i in range(1, 5)] + ["s1", "s2", "s3"]
    m, p = 4, 4

    def covered(path, x):
        return any(a in interests[x] for a in path)

    def welfare(path):
        return sum(covered(path, x) for x in range(len(interests)))

    def share(path, i, x):
        if path[i] not in interests[x]:
            return F(0)
        return F(1, sum(a in interests[x] for a in path))

    def utility(path, i):
        return sum((share(path, i, x) for x in range(len(interests))), F(0))

    def follow(h):
        return h + (0,) * (m - len(h))

    # Complete pure strategy: B at every ordered history, including every off-path node.
    history_rows = []
    margins = []
    for depth in range(m):
        for h in product(range(p), repeat=depth):
            prescribed = follow(h)
            base = utility(prescribed, depth)
            deviations = []
            for action in range(p):
                branch = follow(h + (action,))
                value = utility(branch, depth)
                margin = base - value
                assert margin >= 0, (h, action, margin)
                margins.append(margin)
                deviations.append({"action": action, "terminal": branch,
                                   "payoff": str(value), "IC_margin": str(margin)})
            history_rows.append({"history": h, "prescribed_action": 0,
                                 "prescribed_terminal": prescribed,
                                 "prescribed_payoff": str(base), "deviations": deviations})
    assert len(history_rows) == 85 and len(margins) == 340

    all_terminals = list(product(range(p), repeat=m))
    optimum = max(map(welfare, all_terminals))
    optimal_tuples = [t for t in all_terminals if welfare(t) == optimum]
    assert optimum == 7 and len(optimal_tuples) == 24
    assert all(set(t) == set(range(p)) for t in optimal_tuples)
    actual = follow(())
    W = welfare(actual)

    # Independently compute each chain using unit-client shares, not solver data.
    variation_rows = []
    for target in optimal_tuples:
        d = [F(0)] * len(interests)
        chain = []
        for k, action in enumerate(target):
            h = target[:k]
            minus = follow(h)
            plus = follow(h + (action,))
            client_changes = [share(minus, k, x) - share(plus, k, x)
                              for x in range(len(interests))]
            d = [old + change for old, change in zip(d, client_changes)]
            ic_gain = utility(minus, k) - utility(plus, k)
            assert ic_gain >= 0
            chain.append({"k": k + 1, "prefix": h, "prescribed_action": 0,
                          "forced_action": action, "Z_minus": minus, "Z_plus": plus,
                          "client_share_changes": list(map(str, client_changes)),
                          "IC_gain": str(ic_gain)})
        y0 = [int(covered(actual, x)) for x in range(len(interests))]
        ym = [int(covered(target, x)) for x in range(len(interests))]
        V = [F(ym[x] - y0[x]) + d[x] - y0[x] for x in range(len(interests))]
        assert d == [F(13, 12)] * 4 + [F(-1)] * 3
        assert V == [F(1, 12)] * 4 + [F(0)] * 3
        assert sum(d) == F(4, 3)
        assert sum(V) == F(optimum - 2 * W) + sum(d) == F(1, 3)
        variation_rows.append({"optimal_tuple": target, "chain": chain,
                               "d_per_unit_client": list(map(str, d)),
                               "V_per_unit_client": list(map(str, V)),
                               "IC_sum": str(sum(d)), "UV_holds": all(v <= 0 for v in V)})
    assert not any(row["UV_holds"] for row in variation_rows)

    # A separate canonical set-valued BI calculation checks L and Theta for this
    # same fixed witness; this is not a scan or a fixed continuation selector.
    instance = Instance(("B", "s1", "s2", "s3"),
                        tuple(CustomerType(frozenset({a}), 4 if a == 0 else 1)
                              for a in range(p)), m)
    solver = ExactSPESolver(instance)
    L, theta, child_rows = [], [], []
    for i in range(m):
        row, outcomes = [], []
        for action in range(p):
            counts = instance.counts(actual[:i] + (action,))
            child = sorted(solver.outcomes(counts))
            values = [instance.topic_payoff(action, q) for q in child]
            row.append(min(values))
            outcomes.append({"forced_action": action, "child_prefix_counts": counts,
                             "all_SPE_terminal_counts": child,
                             "current_payoffs": list(map(str, values)),
                             "L": str(row[-1])})
        L.append(row)
        theta.append(max(row))
        child_rows.append({"actual_prefix": actual[:i], "children": outcomes})
    assert L == [[F(1)] * p for _ in range(m)]
    sm_values = [sum((L[i][action] for i, action in enumerate(t)), F(0))
                 for t in optimal_tuples]
    assert min(sm_values) == 4 >= optimum - W == 3
    assert W + sum(theta) - optimum == 1

    result = {
        "status": "exact_counterexample_to_universal_UV_optimum_chain_existence_only",
        "source_family": "co-work-anl/research/questions/customer_attraction_half_coverage.md:23",
        "reviewed_UV": "R-f399f831353446a49502f49d8abd2cb7/probabilistic_route/variation_bridge.md:111",
        "labels": list(instance.topics), "unit_clients": clients,
        "unit_client_interests": [sorted(t) for t in interests],
        "instance": instance.to_dict(), "actual_path": actual,
        "W": W, "OPT": optimum, "half_slack_2W_minus_OPT": 2 * W - optimum,
        "decision_histories_checked": len(history_rows),
        "comparisons_including_self": len(margins), "nonself_comparisons": 255,
        "minimum_IC_margin": str(min(margins)),
        "complete_strategy_and_all_deviations": history_rows,
        "all_terminal_tuples_checked_for_OPT": len(all_terminals),
        "all_optimal_ordered_tuples": optimal_tuples,
        "all_optimal_chain_variation_audits": variation_rows,
        "any_optimal_chain_satisfies_UV": False,
        "set_valued_BI_child_audits": child_rows,
        "L_matrix": [list(map(str, row)) for row in L],
        "Theta": list(map(str, theta)), "sum_Theta": str(sum(theta)),
        "all_optimal_tuple_SM_sums": list(map(str, sm_values)),
        "SM_right_side_OPT_minus_W": optimum - W,
        "TB_slack_W_plus_sumTheta_minus_OPT": str(W + sum(theta) - optimum),
        "scope": "UV conditional implication remains true; SM, THRESHOLD and Q-CAG-HALF are not refuted.",
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "decision_histories_checked", "comparisons_including_self",
        "all_terminal_tuples_checked_for_OPT", "any_optimal_chain_satisfies_UV",
        "W", "OPT", "L_matrix", "Theta", "TB_slack_W_plus_sumTheta_minus_OPT")}, indent=2))


if __name__ == "__main__":
    main()
