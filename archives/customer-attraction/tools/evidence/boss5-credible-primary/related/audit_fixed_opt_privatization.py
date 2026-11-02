"""Independent unit-client, ordered-history audit of fixed-opt privatization.

No repository model, SPE solver, verifier, or discoverer's program is imported.
The exhaustive backward induction caches only complete ordered histories.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    root = next(p for p in here.parents if (p / "AGENTS.md").is_file())
    source = root / "examples/customer_attraction/aggregate_theta_failure.json"
    raw = json.loads(source.read_text())
    labels = tuple(raw["topics"])
    m = raw["players"]
    k = len(labels)
    # Each list entry below is a separate unit customer, including all copies.
    old_clients = tuple(
        frozenset(entry["topics"])
        for entry in raw["customers"]
        for _ in range(entry.get("multiplicity", 1))
    )
    assert (labels, m, len(old_clients)) == (
        ("X0", "X1", "X2", "Y0", "Y1", "Y2"), 3, 36
    )

    def utility(clients, terminal, position):
        topic = terminal[position]
        return sum(
            (Fraction(1, sum(action in likes for action in terminal))
             for likes in clients if topic in likes),
            Fraction(0),
        )

    def welfare(clients, terminal):
        return sum(any(topic in likes for topic in terminal) for likes in clients)

    def actual_action(history):
        if not history:
            return 0
        if len(history) == 1:
            return 3 if history[0] < 3 else 0
        group = range(3) if history[1] < 3 else range(3, 6)
        return next(a for a in group if a not in history)

    def follow(history):
        while len(history) < m:
            history += (actual_action(history),)
        return history

    old_comparisons = 0
    old_min_slack = None
    for depth in range(m):
        for history in product(range(k), repeat=depth):
            on = follow(history)
            chosen = utility(old_clients, on, depth)
            for action in range(k):
                deviated = follow(history + (action,))
                slack = chosen - utility(old_clients, deviated, depth)
                assert slack >= 0, (history, action, slack)
                old_comparisons += 1
                old_min_slack = slack if old_min_slack is None else min(old_min_slack, slack)
    old_actual = follow(())
    assert old_actual == (0, 3, 4)
    assert welfare(old_clients, old_actual) == 34
    C = (3, 4, 5)
    assert welfare(old_clients, C) == len(old_clients) == 36
    omitted = tuple(i for i, likes in enumerate(old_clients)
                    if not any(a in likes for a in old_actual))
    assert Counter(old_clients[i] for i in omitted) == Counter(
        {frozenset({1, 5}): 1, frozenset({2, 5}): 1}
    )
    c_support = frozenset(C)
    new_clients = tuple(
        likes & c_support if i in omitted else likes
        for i, likes in enumerate(old_clients)
    )
    assert all(new_clients[i] == frozenset({5}) for i in omitted)
    assert all(new_clients[i] == old_clients[i] for i in range(36) if i not in omitted)

    def all_spe_outcomes(clients):
        thresholds = {}

        @lru_cache(None)
        def solve(history):
            if len(history) == m:
                return frozenset({history})
            position = len(history)
            children = tuple(solve(history + (a,)) for a in range(k))
            floors = tuple(min(utility(clients, z, position) for z in child)
                           for child in children)
            floor = max(floors)
            thresholds[history] = floor
            result = frozenset(z for child in children for z in child
                               if utility(clients, z, position) >= floor)
            assert result
            return result

        outcomes = solve(())
        root_children = []
        for a in range(k):
            child = solve((a,))
            values = [utility(clients, z, 0) for z in child]
            root_children.append({
                "root_action": a,
                "root_action_label": labels[a],
                "child_SPE_ordered_outcomes": len(child),
                "root_payoff_min": str(min(values)),
                "root_payoff_max": str(max(values)),
                "second_player_threshold": str(thresholds[(a,)]),
                "root_retained_ordered_outcomes": len([z for z in child
                    if utility(clients, z, 0) >= thresholds[()]]),
            })
        return outcomes, thresholds, solve.cache_info(), root_children

    old_outcomes, old_thresholds, old_stats, old_root_children = all_spe_outcomes(old_clients)
    new_outcomes, new_thresholds, new_stats, new_root_children = all_spe_outcomes(new_clients)
    alternative_C = (0, 1, 2)
    alternative_clients = tuple(
        likes & frozenset(alternative_C) if i in omitted else likes
        for i, likes in enumerate(old_clients)
    )
    alternative_outcomes, _, _, _ = all_spe_outcomes(alternative_clients)
    assert old_actual in alternative_outcomes
    assert welfare(alternative_clients, old_actual) == 34
    y0_table = []
    for a in range(k):
        last_values = tuple(utility(new_clients, (3, a, t), 2) for t in range(k))
        replies = tuple(t for t, value in enumerate(last_values) if value == max(last_values))
        second_values = {utility(new_clients, (3, a, t), 1) for t in replies}
        root_values = {utility(new_clients, (3, a, t), 0) for t in replies}
        assert len(second_values) == len(root_values) == 1
        y0_table.append({
            "second_action": a,
            "last_best_replies": replies,
            "second_payoff": str(next(iter(second_values))),
            "root_payoff": str(next(iter(root_values))),
        })

    def counts(z):
        return tuple(z.count(a) for a in range(k))

    unique_new_counts = sorted({counts(z) for z in new_outcomes})
    assert unique_new_counts == [(0, 0, 0, 1, 1, 1)]
    assert len(new_outcomes) == 6
    assert {welfare(new_clients, z) for z in new_outcomes} == {36}
    assert min(welfare(new_clients, z) for z in old_outcomes) <= 34
    # All root actions X are excluded in the new game; this independently
    # confirms that the old prescribed actual root action is no longer best.
    assert {z[0] for z in new_outcomes} == {3, 4, 5}
    assert welfare(new_clients, C) == 36

    report = {
        "identity": "Independent audit of fixed-C missed-customer privatization",
        "status": "PASS: fixed-C preservation W_new<=W_old fails; not a half counterexample",
        "input_source": str(source.relative_to(root)),
        "unit_customer_count": len(old_clients),
        "old_actual": old_actual,
        "old_actual_welfare": welfare(old_clients, old_actual),
        "old_actual_payoffs": [str(utility(old_clients, old_actual, i)) for i in range(m)],
        "old_strategy_histories": sum(k**d for d in range(m)),
        "old_strategy_comparisons_including_self": old_comparisons,
        "old_strategy_minimum_slack": str(old_min_slack),
        "fixed_optimal_tuple": C,
        "old_optimum": 36,
        "changed_unit_clients": [
            {"unit_id": i, "old_likes": sorted(old_clients[i]),
             "new_likes": sorted(new_clients[i])} for i in omitted
        ],
        "old_all_SPE_outcome_count": len(old_outcomes),
        "old_all_SPE_minimum_welfare": min(welfare(old_clients, z) for z in old_outcomes),
        "old_root_threshold": str(old_thresholds[()]),
        "new_all_SPE_outcomes": sorted(new_outcomes),
        "new_all_SPE_count_vectors": unique_new_counts,
        "new_all_SPE_welfares": sorted({welfare(new_clients, z) for z in new_outcomes}),
        "new_root_threshold": str(new_thresholds[()]),
        "new_root_children": new_root_children,
        "new_Y0_child_direct_last_reply_table": y0_table,
        "alternative_optimum_tuple": alternative_C,
        "alternative_privatization_preserves_old_ordered_SPE_outcome": True,
        "new_optimum": 36,
        "new_ordered_history_states": new_stats.currsize,
        "new_nonterminal_history_states": len(new_thresholds),
        "old_ordered_history_states": old_stats.currsize,
        "old_nonterminal_history_states": len(old_thresholds),
        "imports": "Python standard library only; no discoverer or repository solver",
    }
    out = here / "audit_fixed_opt_privatization_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
