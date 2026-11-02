"""Post-reading data/coverage expansion, not a second audit or discovery run.

Extracts all 156 saved actions without calling finish/payoff/BI, compares the
discovery metadata to the independently replayed report, and expands the 70
four-slot coverage values so the original prose's uniqueness claim is explicit.
"""
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

base = Path(__file__).resolve().parent
candidate = json.loads((base / "replay/positive_fresh_candidate.json").read_text())
report = json.loads((base / "replay/positive_fresh_audit.json").read_text())
m, k, weights = candidate["players"], candidate["topics"], candidate["weights"]
actions = {tuple(row["history"]): row["action"] for row in candidate["strategy"]}
histories = {h for depth in range(m) for h in product(range(k), repeat=depth)}
assert len(candidate["strategy"]) == len(actions) == len(histories) == 156
assert set(actions) == histories
assert all(0 <= a < k for a in actions.values())
assert len(weights) == 1 << k and all(isinstance(w, int) and w >= 0 for w in weights)
for key, report_key in [("actual", "actual"), ("context", "positive_context"),
                        ("i", "role_zero_based"), ("B", "B"), ("A", "A")]:
    assert candidate[key] == report[report_key]
assert candidate["q"] == report["positive_edges_zero_based"][str(candidate["j"])]

coverage_rows = []
for choices in combinations_with_replacement(range(k), m):
    union_mask = sum(1 << a for a in set(choices))
    coverage = sum(w for mask, w in enumerate(weights) if mask & union_mask)
    coverage_rows.append({"T": choices, "coverage": coverage})
optimum = max(row["coverage"] for row in coverage_rows)
assert len(coverage_rows) == 70 and optimum == report["OPT"] == 434
optima = [row["T"] for row in coverage_rows if row["coverage"] == optimum]
assert optima == [(0, 1, 2, 3)]
out = {
    "scope": "one post-reading extraction/coverage expansion; no payoff, IC, BI or random search",
    "candidate_top_level_fields": list(candidate),
    "report_top_level_fields": list(report),
    "all_discovery_metadata_matches_recomputed_report": True,
    "players": m, "topics": k, "unit_clients": sum(weights),
    "positive_interest_types": sum(w > 0 for w in weights),
    "topic_sizes": [sum(w for mask, w in enumerate(weights) if mask & (1 << a))
                    for a in range(k)],
    "weights_by_integer_mask": weights,
    "complete_history_count": len(actions),
    "root_action": actions[()],
    "second_actions_by_first": [actions[(a,)] for a in range(k)],
    "third_actions_by_first_second": [[actions[(a, b)] for b in range(k)]
                                      for a in range(k)],
    "fourth_rows_by_first_second": [
        {"prefix": [a, b], "by_third_0_to_4": [actions[(a, b, c)] for c in range(k)]}
        for a, b in product(range(k), repeat=2)
    ],
    "coverage_rows": coverage_rows,
    "optimal_multisets": optima,
    "proper_IC_comparisons_from_original_loop_count": report["IC_comparisons_including_self"] - len(actions),
    "current_original_audit_executions": 1,
    "extra_original_audit_executions": 0,
}
(base / "complete-fixture-expansion.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"unit_clients": out["unit_clients"], "positive_types": out["positive_interest_types"],
                  "history_count": len(actions), "coverage_rows": len(coverage_rows),
                  "optimal_multisets": optima, "metadata_matches": True}))
