"""Reuse audited coefficient rows to resolve the five pending cuts on 5692.

This does not reconstruct any complete matrix or run an optimizer.  The
coefficient file is the output of audit_cut_packs.py.  Column descriptors and
all zero extensions are checked before comparing exact rational slacks.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = Path("research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1")
EXPECTED_NEW_SHA = "46e52c1cec4a5cac3e6d7fe3bbe8d227cd663e428ca7f4e955182343eedb418e"
DEFAULT_NEW = HERE.parents[2] / "tools/evidence/b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json"


def descriptors(point):
    return [{key: value for key, value in column.items() if key != "weight"}
            for column in point["columns"]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-point", type=Path, default=DEFAULT_NEW)
    args = parser.parse_args()
    r5 = HERE / "original" / BASE / "research_5"
    first = json.loads((r5 / "combined_branch_latest_exact.json").read_text())
    old = json.loads((r5 / "coupled_latest_exact.json").read_text())
    new_raw = args.new_point.read_bytes()
    assert hashlib.sha256(new_raw).hexdigest() == EXPECTED_NEW_SHA
    new = json.loads(new_raw)
    assert len(first["columns"]) == 1905
    assert len(old["columns"]) == 2033
    assert len(new["columns"]) == 4849
    assert descriptors(first) == descriptors(old)[:1905] == descriptors(new)[:1905]
    assert new["verified_rows"] == 5692
    row_file = HERE / "runs/all-sparse-row-coefficients.json"
    rows = json.loads(row_file.read_text())
    assert len(rows) == 27
    groups = defaultdict(list)
    results = []
    for item in rows:
        row = [F(0)] * item["length"]
        for index, value in item["nonzero"]:
            assert row[index] == 0
            row[index] = F(value)
        encoded = json.dumps(list(map(str, row)), separators=(",", ":")).encode()
        assert hashlib.sha256(encoded).hexdigest() == item["row_sha256"]
        assert all(value == 0 for value in row[1905:])
        groups[tuple(row[:1905])].append({key: item[key] for key in ("pack", "field", "number")})
        if item["pack"] == "coupled_pending_cuts.json":
            old_value = sum(row[i] * F(old["columns"][i]["weight"]) for i in range(1905))
            new_value = sum(row[i] * F(new["columns"][i]["weight"]) for i in range(1905))
            assert old_value < 0
            results.append({key: item[key] for key in ("pack", "field", "number")} |
                           {"old_5277_slack": str(old_value), "new_5692_slack": str(new_value),
                            "new_sign": (new_value > 0) - (new_value < 0)})
    assert len(results) == 5
    report = {
        "status": "passed",
        "audited_coefficient_file_sha256": hashlib.sha256(row_file.read_bytes()).hexdigest(),
        "new_point_dependency": "archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json",
        "new_point_source_id": "4b4bfa195d256d412c82",
        "new_point_sha256": EXPECTED_NEW_SHA,
        "new_point_rows": 5692,
        "new_point_columns": 4849,
        "common_descriptor_count": 1905,
        "all_other_coefficients_zero": True,
        "records": 27,
        "distinct_coefficient_rows_on_common_domain": len(groups),
        "repeated_row_record_groups": [items for items in groups.values() if len(items) > 1],
        "pending_rows_at_new_point": results,
        "new_original_CLI_calls": 0,
        "new_discovery_LP_calls": 0,
        "new_whole_matrix_replays": 0,
    }
    (HERE / "runs/pending-at-5692-and-record-identities.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "passed", "distinct_rows": len(groups), "new_signs": [r["new_sign"] for r in results]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
