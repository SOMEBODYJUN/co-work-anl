#!/usr/bin/env python3
"""Compare saved finite tables and exact source identities; do not replay a game.

No author's or independent audit code is imported or executed. The previously
certified independent reports are read only as saved data.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "payoff-cap-independent-two-versions-boss1"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    author = json.loads((HERE / "original/payoff_cap_audit.json").read_text())
    assert len(author["reports"]) == 2
    result = {
        "operation": "saved-table and identity comparison only; no game replay",
        "author_audit_executed": False,
        "independent_audit_executed": False,
        "reports": [],
    }
    for report, prior_name in zip(author["reports"], (
        "payoff_cap_independent_audit.json",
        "payoff_cap_independent_audit_markov.json",
    )):
        source = HERE / "original" / report["input"]
        old_source = PRIOR / "replay-root/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/credible_counterexample" / report["input"]
        prior_path = PRIOR / "original" / prior_name
        prior = json.loads(prior_path.read_text())
        assert source.read_bytes() == old_source.read_bytes()
        assert digest(source) == prior["source_sha256"]
        mapping = {
            "players": "players", "topics": "topics", "unit_customers": "units",
            "path": "root", "payoffs": "payoffs", "welfare": "welfare",
            "optimum": "optimum", "complete_histories": "decision_histories",
            "all_action_comparisons": "including_self_comparisons",
            "strict_deviation_inequalities": "strict_proper_deviations",
        }
        for a, b in mapping.items():
            assert report[a] == prior[b], (report["input"], a)
        prior_nodes = {tuple(row["history"]): row for row in prior["node_checks"]}
        assert len(prior_nodes) == len(report["all_comparisons"]) == 31
        all_histories = []
        for row in report["all_comparisons"]:
            h = tuple(row["history"])
            node = prior_nodes[h]
            assert row["action"] == node["selected"]
            assert [item["action"] for item in node["all_action_branches"]] == list(range(5))
            assert row["deviation_payoffs"] == [item["own_payoff"] for item in node["all_action_branches"]]
            all_histories.append(row["history"])
        rows = {tuple(row["history"]): row for row in report["all_comparisons"]}
        assert report["root_deviation_payoffs"] == rows[()]["deviation_payoffs"]
        assert report["second_deviation_payoffs"] == [rows[(a,)]["deviation_payoffs"] for a in range(5)]
        # Last maxima are compared to the previously certified node's selected
        # payoff, rather than recomputing any customer utility here.
        assert report["last_maxima"] == [[prior_nodes[(a, b)]["actual_own_payoff"] for b in range(5)] for a in range(5)]
        expected_markov = report["input"].endswith("_markov.json")
        assert report["count_markov"] is expected_markov
        if "same_count_histories_same_action" in prior:
            assert prior["same_count_histories_same_action"] is expected_markov
        result["reports"].append({
            "input": report["input"], "input_sha256": digest(source),
            "prior_report": str(prior_path.relative_to(HERE.parents[4])),
            "prior_report_sha256": digest(prior_path),
            "same_input_bytes_as_prior_success": True,
            "mapped_scalar_fields": mapping,
            "all_31_history_action_records_and_155_payoff_entries_equal": True,
            "all_histories_compared": all_histories,
            "three_summary_tables_equal": True,
            "strict": report["strict_deviation_inequalities"],
            "proper_ties": prior["tied_proper_deviations"],
            "count_markov": report["count_markov"],
            "prior_markov_flag_present": "same_count_histories_same_action" in prior,
        })
    markov = HERE / "original/payoff_cap_failure_markov.json"
    cone = HERE / "original/payoff_cap_markov_cone_optimum.json"
    assert markov.read_bytes() == cone.read_bytes()
    cone_record = json.loads(cone.read_text())
    assert set(cone_record) == {"value", "instance", "strategy", "path", "payoffs", "welfare", "optimum", "objective_action", "exact_dual_bound", "checked_histories", "checked_deviations"}
    assert isinstance(cone_record["exact_dual_bound"], str)
    result["markov_cone_alias"] = {
        "same_bytes": True, "sha256": digest(markov), "bytes_each": markov.stat().st_size,
        "new_dual_vector_present": False,
        "interpretation": "same complete finite primal record under a different filename; scalar exact_dual_bound is not a saved dual vector",
    }
    (HERE / "saved-table-comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"reports": 2, "histories_compared": 62, "payoff_entries_compared": 310, "markov_cone_same_bytes": True, "game_replays": 0}))


if __name__ == "__main__":
    main()
