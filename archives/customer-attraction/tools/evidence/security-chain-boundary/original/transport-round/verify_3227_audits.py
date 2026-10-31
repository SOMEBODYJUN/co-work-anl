#!/usr/bin/env python3
"""Independent stdlib-only consistency checks for the frozen 3227 transport bundle."""
from __future__ import annotations
import hashlib, json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
inp = json.loads((ROOT / "local_security_increment_initial_3227_input.json").read_text())
aud = json.loads((ROOT / "local_security_increment_initial_3227_audit.json").read_text())
ind = json.loads((ROOT / "local_security_increment_initial_3227_independent_audit.json").read_text())

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def f(x):
    return Fraction(str(x))

multiplicity_sum = sum(c["multiplicity"] for c in inp["customers"])
comparisons = ind["spe_comparisons"]
slacks = [f(z["slack"]) for z in comparisons]
policy = {}
for z in comparisons:
    policy.setdefault(tuple(z["history"]), set()).add(z["prescribed"])
per_history_alternatives = {}
for z in comparisons:
    per_history_alternatives.setdefault(tuple(z["history"]), []).append(z["alternative"])
terminal_histories = {tuple(z["actual_terminal"]) for z in comparisons} | {tuple(z["deviation_terminal"]) for z in comparisons}

checks = {
    "input_sha256": sha(ROOT / "local_security_increment_initial_3227_input.json"),
    "independent_declared_input_sha256": ind["source_sha256"]["input"],
    "input_sha_matches_independent": sha(ROOT / "local_security_increment_initial_3227_input.json") == ind["source_sha256"]["input"],
    "unit_customer_sum": multiplicity_sum,
    "declared_unit_customers": ind["distinct_unit_clients"],
    "customer_type_count": len(inp["customers"]),
    "declared_customer_type_count": ind["customer_types"],
    "history_count_from_comparisons": len(policy),
    "declared_decision_histories": ind["decision_histories"],
    "comparison_count": len(comparisons),
    "six_alternatives_per_history": all(sorted(v) == list(range(6)) for v in per_history_alternatives.values()),
    "terminal_history_count": len(terminal_histories),
    "declared_terminal_history_count": ind["terminal_histories"],
    "declared_comparison_count": ind["all_action_comparisons"],
    "negative_slack_count": sum(s < 0 for s in slacks),
    "zero_slack_count": sum(s == 0 for s in slacks),
    "declared_negative_comparisons": ind["negative_comparisons"],
    "declared_tied_comparisons": ind["tied_comparisons"],
    "global_saddle_match": ind["global_saddle"]["primal_minimum"] == ind["global_saddle"]["dual_maximum"] == ind["global_saddle"]["value"],
    "local_saddle_match": ind["local_saddle"]["primal_minimum"] == ind["local_saddle"]["dual_maximum"] == ind["local_saddle"]["value"],
    "audit_independent_path_match": aud["outcome"] == ind["path"],
    "audit_independent_welfare_match": aud["W"] == ind["welfare"],
    "audit_independent_optimum_match": aud["OPT"] == ind["optimum"],
    "audit_independent_v3_match": aud["v3"] == ind["on_path_security_values"][0],
    "audit_independent_v2_match": aud["v2_after_root_A0"] == ind["on_path_security_values"][1],
    "aggregate_margin": aud["aggregate_n_bridge_margin"],
    "weak_margin": aud["global_weak_bridge_margin"],
    "double_half_margin": aud["half_coverage_margin"],
    "recomputed_double_half_margin": 2 * aud["W"] - aud["OPT"],
    "scope_matches": ("one-step" in aud["scope"] and "one-step" in ind["scope"] and "half" in aud["scope"] and "half" in ind["scope"] and "no aggregate" in ind["scope"]),
    "independent_declares_no_math_errors": ind["mathematical_errors_in_witness"] == [],
}
checks["pass"] = (
    checks["input_sha_matches_independent"]
    and checks["unit_customer_sum"] == checks["declared_unit_customers"] == 3227
    and checks["customer_type_count"] == checks["declared_customer_type_count"] == 22
    and checks["history_count_from_comparisons"] == checks["declared_decision_histories"] == 43
    and checks["comparison_count"] == checks["declared_comparison_count"] == 258
    and checks["six_alternatives_per_history"]
    and checks["terminal_history_count"] == checks["declared_terminal_history_count"] == 216
    and checks["negative_slack_count"] == checks["declared_negative_comparisons"] == 0
    and checks["zero_slack_count"] == checks["declared_tied_comparisons"] == 92
    and checks["global_saddle_match"] and checks["local_saddle_match"]
    and checks["audit_independent_path_match"] and checks["audit_independent_welfare_match"]
    and checks["audit_independent_optimum_match"] and checks["audit_independent_v3_match"]
    and checks["audit_independent_v2_match"]
    and checks["double_half_margin"] == checks["recomputed_double_half_margin"] == 2673
    and checks["scope_matches"] and checks["independent_declares_no_math_errors"]
)
print(json.dumps(checks, ensure_ascii=False, indent=2, sort_keys=True))
