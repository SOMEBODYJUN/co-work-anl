"""Static delivery checks only; never import or rerun the mathematical audit."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    archive = repo / "archives/customer-attraction"
    evidence = archive / "tools/evidence/background-pair-saved-points"
    manifest = json.loads((evidence / "source-manifest.json").read_text())
    bindings = []
    for entry in manifest["bindings"]:
        path = repo / entry["path"]
        assert path.is_file(), str(path)
        assert path.stat().st_size == entry["bytes"], str(path)
        assert sha(path) == entry["sha256"], str(path)
        bindings.append(entry["path"])
    text_paths = [repo / manifest["formal_target"], evidence / "README.md"]
    links = []
    for path in text_paths:
        content = path.read_text()
        assert not any(ord(ch) < 32 and ch not in "\n\r\t" for ch in content)
        assert content.count("\\[") == content.count("\\]")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if target.startswith(("http:", "https:", "#")):
                continue
            linked = (path.parent / target.split("#")[0]).resolve()
            assert linked == evidence / "self-check.json" or linked.is_file(), (str(path), target)
            links.append({"from": str(path.relative_to(repo)), "target": str(linked.relative_to(repo))})
    parsed_json = []
    parsed_python = []
    for path in sorted(evidence.rglob("*")):
        if not path.is_file() or path.name == "self-check.json":
            continue
        if path.suffix == ".json":
            json.loads(path.read_text())
            parsed_json.append(str(path.relative_to(repo)))
        if path.suffix == ".py":
            ast.parse(path.read_text())
            parsed_python.append(str(path.relative_to(repo)))
    receipts = []
    for source in manifest["primary_sources"]:
        path = repo / "cleanup/workspaces/Boss7/receipts-round21" / (source["id"] + ".json")
        receipt = json.loads(path.read_text())
        assert receipt["id"] == source["id"]
        for key in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"):
            assert receipt[key] is True
        for key in ("read_note", "comparison_note", "decision_note"):
            assert len(receipt[key]) > 50
        assert receipt["disposition"] == "integrated"
        assert manifest["formal_target"] in receipt["targets"]
        for target in receipt["targets"]:
            assert repo / target == evidence / "self-check.json" or (repo / target).is_file(), target
        receipts.append({"path": str(path.relative_to(repo)), "sha256": sha(path), "target_count": len(receipt["targets"])})
    event = json.loads((evidence / "calibration/execution.json").read_text())
    audit = json.loads((evidence / "calibration/exact-calibration-audit.json").read_text())
    assert event["exit_code"] == 0 and event["stderr_bytes"] == 0
    assert event["sources_before"] == event["sources_after"]
    assert event["script_sha256"] == sha(evidence / "audit_calibrations.py")
    for name, item in event["artifacts"].items():
        assert sha(evidence / "calibration" / name) == item["sha256"]
    assert audit["status"] == "PASS"
    assert audit["policy_nodes"] == 4756 and audit["all_action_comparisons"] == 31737
    for key in ("original_main_calls", "original_helper_calls", "LP_calls", "solver_calls", "random_searches"):
        assert audit[key] == event[key] == 0
    for case in audit["cases"]:
        assert case["original_prefix_missing"] is True
        assert case["result"]["historical_exact_certificate"] is False
    summary = {"status": "PASS", "scope": "static bindings/JSON/Python AST/links/receipt/event check; no mathematical code invoked",
               "bindings": bindings, "local_links": links, "JSON_parsed": parsed_json, "Python_AST_parsed": parsed_python,
               "receipts": receipts, "formal_target": manifest["formal_target"],
               "formal_bytes": (repo / manifest["formal_target"]).stat().st_size,
               "formal_sha256": sha(repo / manifest["formal_target"]),
               "unique_math_event_preserved": True, "new_mathematical_runs": 0}
    (evidence / "self-check.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "bindings": len(bindings), "local_links": len(links),
                      "JSON": len(parsed_json), "Python_AST": len(parsed_python), "receipts": len(receipts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
