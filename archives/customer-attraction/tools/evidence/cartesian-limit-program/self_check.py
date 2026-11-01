"""Static closure of the archived package; no original/helper/math execution."""
import ast
import hashlib
import json
from pathlib import Path
import re

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[4]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((PACKAGE / "artifact-manifest.json").read_text())
    hashes = 0
    for row in manifest["files"]:
        p = REPO / row["path"]
        assert p.is_file(), row["path"]
        assert p.stat().st_size == row["bytes"] and sha(p) == row["sha256"], row["path"]
        hashes += 1
    source = json.loads((PACKAGE / "source-manifest.json").read_text())
    for row in source["frozen_sources"] + source["related_full_reads"]:
        p = REPO / row["local_path"]
        assert p.stat().st_size == row["bytes"] and sha(p) == row["sha256"], row["local_path"]
        hashes += 1
    parsed_json = parsed_python = 0
    for p in sorted(PACKAGE.rglob("*")):
        if p.suffix == ".json" and p.name != "self-check.json":
            json.loads(p.read_text())
            parsed_json += 1
        elif p.suffix == ".py":
            ast.parse(p.read_text(), filename=str(p))
            parsed_python += 1
    old = json.loads((PACKAGE / "original/cartesian_limit_k6.json").read_text())
    new = json.loads((PACKAGE / "replay/new-analysis.json").read_text())
    event = json.loads((PACKAGE / "replay/execution.json").read_text())
    exact = json.loads((PACKAGE / "exact/exact-k6-audit.json").read_text())
    assert len(old) == 5 and len(old["best"]) == 16 and len(new) == 18
    assert all(new[k] == v for k, v in old["best"].items())
    assert set(new) - set(old["best"]) == {"pure_root_floor", "pure_root_floor_by_action"}
    assert event["status"] == exact["status"] == "PASS"
    assert event["call_counts"] == {"original_analyze": 1, "original_main": 0, "linprog": 9}
    assert event["linprog_statuses"] == [0]*6+[2, 0, 0]
    assert event["historical_random_scan_replayed"] is False
    assert exact["strict_root_positive_margin_infeasible"] is True
    assert exact["weak_root_feasible_support"] == [[0, 0, 0]]
    assert len(exact["all_terminal_payoffs"]) == 216
    assert len(exact["all_last_reply_rows"]) == 36
    assert len(exact["all_second_menu_rows"]) == 6
    assert len(exact["security_background_rows"]) == 21
    assert len(exact["all_complete_strategy_comparisons"]) == 258
    assert exact["complete_constant_zero_strategy"]["decision_histories"] == 43
    assert exact["complete_constant_zero_strategy"]["strict_nonself_comparisons"] == 215
    assert exact["observed_original_occupied_pay_entries_compared_exactly"] == 648
    assert exact["observed_LP_float_scalars_compared_to_exact_data"] == 843
    assert exact["all_nine_original_LP_argument_blocks_checked"] is True
    assert exact["original_analyze_calls"] == exact["LP_calls"] == 0
    assert exact["canonical_SPE_solver_calls"] == 0
    assert exact["independent_exact_point_audit_runs"] == 1
    links = formula_pairs = 0
    for rel in manifest["markdown_objects"]:
        p = REPO / rel
        s = p.read_text()
        assert s.count(r"\[") == s.count(r"\]"), rel
        formula_pairs += s.count(r"\[")
        assert "\x00" not in s and "\x07" not in s
        for match in re.finditer(r"\]\(([^)]+)\)", s):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target:
                continue
            assert (p.parent / target).resolve().exists(), (rel, target)
            links += 1
    receipt_targets = 0
    for rid in ["0668a7eadde334207c8a", "b25ffb3be50288f87850"]:
        p = REPO / "cleanup/workspaces/Boss7/receipts-round20" / (rid+".json")
        r = json.loads(p.read_text())
        assert r["id"] == rid and r["disposition"] == "integrated"
        assert all(r[k] is True for k in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"])
        assert all(r[k].strip() for k in ["read_note", "comparison_note", "decision_note"])
        for target in r["targets"]:
            assert (REPO / target).is_file() or (REPO / target) == PACKAGE / "self-check.json", target
            receipt_targets += 1
    out = {"status": "PASS", "scope": "static archived-file closure only; no math execution",
           "sha256_bindings_checked": hashes, "JSON_files_parsed": parsed_json,
           "Python_ASTs_parsed": parsed_python, "local_links_checked": links,
           "display_formula_pairs": formula_pairs, "receipt_count": 2,
           "receipt_target_entries": receipt_targets,
           "new_original_calls": 0, "new_LP_calls": 0, "new_payoff_or_IC_enumerations": 0,
           "original_event_identity": "one analyze, zero main, nine LP including failed strict guard",
           "independent_event_identity": "one raw-unit-client Fraction audit, zero LP"}
    (PACKAGE / "self-check.json").write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
