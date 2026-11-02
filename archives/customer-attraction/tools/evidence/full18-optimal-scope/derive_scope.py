"""Check the exact arithmetic needed by the true-OPT scope corollary.

This consumes a previously published exhaustive-potential report. It does not
rerun its enumeration, solve an LP, or certify a complete SPE.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    dependencies = json.loads((package / "reused-dependencies.json").read_text())
    for item in dependencies:
        data = (args.repo / item["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
    prefix = args.repo / "archives/customer-attraction/tools/evidence/potential-menu-joint/replay"
    point = json.loads((prefix / "potential_menu_joint.json").read_text())
    old_report = json.loads((prefix / "audit_normal.json").read_text())
    rows = [(tuple(t), F(mass)) for t, mass in point["positive_types"]]
    assert len(rows) == 19
    assert all(mass > 0 and t[1] == 1 for t, mass in rows)
    total = sum((mass for _, mass in rows), F(0))
    actual = sum((mass for (mask, _, _, _), mass in rows if mask), F(0))
    assert actual == 1
    assert total == F(point["exact_value"])
    assert total == F(old_report["maximum_potential"])
    assert total == F(old_report["budget_W_plus_C"])
    assert old_report["argmax"] == [0] * 6 + [1] * 6 + [0] * 6
    scale = old_report["scale"]
    per_row = [mass * scale / 6 for _, mass in rows]
    assert all(x.denominator == 1 and x > 0 for x in per_row)
    assert 6 * sum(per_row) == old_report["unit_customer_count"]
    assert old_report["customer_types"] == 6 * len(rows) == 114
    slacks = list(map(F, old_report["penultimate_all_alternatives_support_slack"]))
    assert len(slacks) == 18
    assert slacks[5] == -F(168357318739, 9225781201100)
    assert slacks[12:] == [-F(480277410963, 9225781201100)] * 6
    report = {
        "status": "PASS_EXACT_TYPE_ARITHMETIC_AND_EXISTING_REPORT_BINDING",
        "original_program_runs_this_batch": 0,
        "exhaustive_potential_enumerations_this_batch": 0,
        "new_full_SPE_checks_this_batch": 0,
        "positive_symmetric_rows": len(rows),
        "all_comparison_degrees_equal_one": True,
        "each_symmetric_row_expands_to_six_positive_integer_types": True,
        "per_expanded_type_unit_counts_in_source_order": [int(x) for x in per_row],
        "scale": scale,
        "unit_customer_count": old_report["unit_customer_count"],
        "actual_normalized_coverage": str(actual),
        "comparison_union_normalized_coverage": str(total),
        "comparison_union_equals_entire_customer_universe": True,
        "previously_reported_maximum_potential": old_report["maximum_potential"],
        "previously_reported_potential_multisets": old_report["potential_multisets"],
        "previously_reported_argmax": old_report["argmax"],
        "true_static_OPT_from_covering_all_clients": str(total),
        "normalized_half_gap": str(total - 2 * actual),
        "previously_reported_penultimate_actual_last_slack": str(slacks[5]),
        "previously_reported_penultimate_each_reply_slack": str(slacks[12]),
        "complete_SPE_claim": False,
        "exhaustive_maximum_claim_is_reused_not_independently_recomputed": True,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    with args.output.open("x") as stream:
        stream.write(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
