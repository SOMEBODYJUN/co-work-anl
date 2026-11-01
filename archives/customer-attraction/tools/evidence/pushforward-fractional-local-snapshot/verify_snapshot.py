"""New exact reconstruction of one historical floating snapshot.

Uses only Python's standard library.  No original search/LP, project module,
or sibling audit is executed or imported.  The original generator is unknown.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import hashlib
import json
import platform


BASE = Path(__file__).resolve().parent
SOURCE = BASE / "original/pushforward_fractional_candidate_local_security_increment_0.json"
raw_text = SOURCE.read_text()
raw = json.loads(raw_text, parse_float=F)
tokens = json.loads(raw_text, parse_float=str)
floats = json.loads(raw_text)
game = json.loads((BASE / "related/local_security_increment_input.json").read_text())
certificate = json.loads((BASE / "related/local_security_increment_certificate.json").read_text())
assert set(raw) == {"p", "weights", "extra", "name", "masklist", "gap"}
assert raw["extra"] == 0 and raw["name"] == "local_security_increment"
N, K = game["players"], len(game["topics"])
assert (N, K) == (3, 6)
MASKS = tuple(range(1, 1 << K))
assert raw["masklist"] == list(MASKS) and len(raw["weights"]) == len(MASKS)
assert len(raw["p"]) == K and all(v >= 0 for v in raw["p"] + raw["weights"])
actions_list = certificate["strategy"]["actions"]
actions = {tuple(entry["history"]): entry["action"] for entry in actions_list}
histories = [h for depth in range(N) for h in product(range(K), repeat=depth)]
assert len(actions_list) == len(actions) == len(histories) == 43
assert set(actions) == set(histories) and all(a in range(K) for a in actions.values())


def closed_rule(history):
    if not history:
        return 0
    if len(history) == 1:
        return 3 if history[0] < 3 else 0
    group = range(0, 3) if history[1] < 3 else range(3, 6)
    return min(a for a in group if a not in history)


assert all(actions[h] == closed_rule(h) for h in histories)


def finish(history):
    history = tuple(history)
    while len(history) < N:
        history += (actions[history],)
    return history


def utility(outcome, actor, weights):
    a = outcome[actor]
    return sum((weights[m - 1] / sum(bool(m >> b & 1) for b in outcome)
                for m in MASKS if m >> a & 1), F(0))


def coverage(outcome, weights):
    return sum((weights[m - 1] for m in MASKS if any(m >> a & 1 for a in outcome)), F(0))


def audit(weights, save_rows=False):
    rows = []
    for history in histories:
        selected = finish(history)
        selected_pay = utility(selected, len(history), weights)
        for a in range(K):
            changed = finish(history + (a,))
            deviation_pay = utility(changed, len(history), weights)
            rows.append({"history": list(history), "selected_action": actions[history],
                         "deviation_action": a, "selected_outcome": list(selected),
                         "deviation_outcome": list(changed),
                         "selected_payoff": str(selected_pay), "deviation_payoff": str(deviation_pay),
                         "slack": str(selected_pay - deviation_pay)})
    values = [F(row["slack"]) for row in rows]
    profiles = list(product(range(K), repeat=N))
    for outcome in profiles:
        assert sum(utility(outcome, i, weights) for i in range(N)) == coverage(outcome, weights)
    actual = finish(())
    result = {"histories": len(histories), "comparisons_including_self": len(rows),
              "negative_count": sum(v < 0 for v in values), "zero_count": sum(v == 0 for v in values),
              "minimum_IC": str(min(values)),
              "minimum_example": rows[values.index(min(values))],
              "actual_path": list(actual), "actual_terminal_counts": [actual.count(a) for a in range(K)],
              "utilities": [str(utility(actual, i, weights)) for i in range(N)],
              "welfare": str(coverage(actual, weights)),
              "OPT3": str(max(coverage(h, weights) for h in profiles)),
              "profile_count_for_OPT_and_budget_identity": len(profiles)}
    if save_rows:
        (BASE / "rationalized-IC-table.json").write_text(json.dumps(rows, indent=2) + "\n")
    return result


# Explicit new small-denominator proposal, NOT a replacement of the old float.
weights = [v.limit_denominator(10**6) for v in raw["weights"]]
assert max(abs(a - b) for a, b in zip(weights, raw["weights"])) < F(1, 10**12)
denominator = lcm(*(v.denominator for v in weights))
integer_weights = [int(v * denominator) for v in weights]
assert denominator == 158 and sum(integer_weights) == 585
theme_signatures = [tuple(m for m in MASKS if weights[m - 1] and m >> a & 1) for a in range(K)]
assert all(theme_signatures) and len(set(theme_signatures)) == K
new_audit = audit(weights, save_rows=True)
assert new_audit["negative_count"] == 0 and new_audit["utilities"][0] == "1"
decimal_audit = audit(raw["weights"])
binary_audit = audit([F.from_float(v) for v in floats["weights"]])
seed_weights = [F(0)] * len(MASKS)
for customer in game["customers"]:
    mask = sum(1 << a for a in customer["topics"])
    seed_weights[mask - 1] += customer["multiplicity"]
seed_audit = audit(seed_weights)
assert sum(seed_weights) == 113 and seed_audit["negative_count"] == 0
assert seed_audit["actual_terminal_counts"] == certificate["strategy"]["terminal_counts"]


def query_values(load, ws):
    return [sum((ws[m - 1] / (1 + sum(load[t] for t in range(K) if m >> t & 1))
                 for m in MASKS if m >> a & 1), F(0)) for a in range(K)]


probability_sum = sum(raw["p"], F(0))
probability = [v / probability_sum for v in raw["p"]]
assert sum(probability) == 1
tails = [finish((a,))[1:] for a in range(K)]
tail_counts = [[tail.count(t) for t in range(K)] for tail in tails]
tail_load = [sum((probability[a] * tail_counts[a][t] for a in range(K)), F(0)) for t in range(K)]
assert sum(tail_load) == 2
values = query_values(tail_load, weights)
gap = sum((p * g for p, g in zip(probability, values)), F(0)) - 1
assert F(1, 400) < gap < F(1, 380)
full_load = [tail_load[t] + probability[t] for t in range(K)]
full_values = query_values(full_load, weights)
full_gap = sum((p * g for p, g in zip(probability, full_values)), F(0)) - 1
assert full_gap < 0 and sum(full_load) == 3

# An explicit free total-mass-two background, without numerical optimization.
# L = 2q, q = (1/4,1/8,1/8,1/4,1/8,1/8).
free_load = [F(1, 2), F(1, 4), F(1, 4), F(1, 2), F(1, 4), F(1, 4)]
assert sum(free_load) == 2
free_values = query_values(free_load, weights)
assert max(free_values) == F(153, 158) < 1

# Floating formula comparison only, with original arrays and no normalization.
float_load = [sum(floats["p"][a] * tail_counts[a][t] for a in range(K)) for t in range(K)]
float_values = query_values(float_load, floats["weights"])
float_root = utility(finish(()), 0, floats["weights"])
float_gap = sum(p * v for p, v in zip(floats["p"], float_values)) - float_root
assert abs(float_gap - floats["gap"]) < 1e-12

result = {
    "status": "CURRENT reconstruction: original float is not an exact certificate; new 585-client point passes complete SPE",
    "environment": {"python": platform.python_version(), "libraries": "Python standard library only"},
    "original_generator": "Not located by frozen *.py searches for pushforward_fractional and masklist; no original optimization replay",
    "original_source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "original_source_bytes": len(SOURCE.read_bytes()),
    "original_fields": list(raw), "masklist": list(MASKS), "p_decimal_tokens": tokens["p"],
    "extra": raw["extra"], "name": raw["name"], "saved_gap_decimal_token": tokens["gap"],
    "p_decimal_exact_sum": str(probability_sum), "p_decimal_sum_minus_one": str(probability_sum - 1),
    "negative_zero_weight_masks": [m for m, t in zip(MASKS, tokens["weights"]) if t == "-0.0"],
    "original_weights_decimal_audit": decimal_audit,
    "original_weights_binary64_audit": binary_audit,
    "rationalization_rule": "Each exact JSON decimal weight limit_denominator(1000000); original p exact decimals divided by their exact sum",
    "new_rational_weights_total": str(sum(weights)),
    "new_rational_positive_type_count": sum(v > 0 for v in weights),
    "new_unit_customer_scale": denominator, "new_unit_customer_total": sum(integer_weights),
    "new_six_themes_nonempty_and_pairwise_distinct": True,
    "new_positive_weights": [[m, str(weights[m - 1]), integer_weights[m - 1]] for m in MASKS if weights[m - 1]],
    "all_weight_tokens_proposals_and_deltas": [[m, tokens["weights"][m - 1], str(weights[m - 1]),
        str(raw["weights"][m - 1] - weights[m - 1])] for m in MASKS],
    "new_rational_complete_strategy_audit": new_audit,
    "source_named_113_client_audit": seed_audit,
    "source_named_input_positive_type_count": sum(v > 0 for v in seed_weights),
    "full_43_action_table_matches_closed_rule": True,
    "root_forced_tails": [list(t) for t in tails], "root_forced_tail_counts": tail_counts,
    "new_probability": list(map(str, probability)), "new_tail_load_mass_two": list(map(str, tail_load)),
    "new_six_tail_query_values": list(map(str, values)), "new_six_tail_query_values_float": list(map(float, values)),
    "new_exact_tail_gap": str(gap), "new_exact_tail_gap_float": float(gap),
    "new_exact_tail_gap_bounds": "1/400 < gap < 1/380",
    "float_formula_gap_original_arrays": float_gap, "float_saved_gap": floats["gap"],
    "float_formula_absolute_error": abs(float_gap - floats["gap"]),
    "new_full_load_mass_three": list(map(str, full_load)),
    "new_full_terminal_gap": str(full_gap), "new_full_terminal_gap_float": float(full_gap),
    "new_free_load_mass_two": list(map(str, free_load)),
    "new_free_probability": [str(v / 2) for v in free_load],
    "new_free_six_query_values": list(map(str, free_values)),
    "new_free_cap": str(max(free_values)), "new_free_cap_claim": "feasible upper bound only; no minimization or optimality claim",
    "new_integer_welfare": int(F(new_audit["welfare"]) * denominator),
    "new_integer_OPT3": int(F(new_audit["OPT3"]) * denominator),
    "new_integer_twice_welfare_minus_OPT": int((2 * F(new_audit["welfare"]) - F(new_audit["OPT3"])) * denominator),
}
(BASE / "reconstruction.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"new_clients": sum(integer_weights), "new_exact_SPE_negative_IC": new_audit["negative_count"],
                  "old_decimal_negative_IC": decimal_audit["negative_count"],
                  "old_binary64_negative_IC": binary_audit["negative_count"],
                  "exact_tail_gap_approx": float(gap), "free_cap": str(max(free_values)),
                  "W": result["new_integer_welfare"], "OPT": result["new_integer_OPT3"]}, ensure_ascii=False))
