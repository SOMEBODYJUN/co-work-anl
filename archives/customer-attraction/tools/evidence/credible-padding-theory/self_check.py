"""Static package check only. Does not import or execute mathematical programs."""
import ast
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = next(p for p in BASE.parents if (p / "cleanup" / "OBJECTS.md").is_file())


def read_json(path):
    return json.loads(path.read_text())


def main():
    manifest = read_json(BASE / "source-manifest.json")
    comparison = read_json(BASE / "comparison.json")
    mapping = read_json(BASE / "source-to-object.json")
    checked_hashes = 0
    json_files = set()
    ast_files = set()
    for row in manifest["artifacts"] + comparison["read_material"]:
        p = ROOT / row["path"]
        raw = p.read_bytes()
        assert len(raw) == row["bytes"], row["path"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"], row["path"]
        checked_hashes += 1
        if p.suffix == ".json":
            read_json(p)
            json_files.add(row["path"])
        if p.suffix == ".py":
            ast.parse(raw.decode(), filename=str(p))
            ast_files.add(row["path"])
    obj = ROOT / manifest["object"]
    body = obj.read_text()
    source = (BASE / "original" / "all_k_padding.md").read_text()
    headings = [line for line in source.splitlines() if line.startswith("## ")]
    assert headings == [row["source_heading"] for row in mapping["sections"]]
    assert len(headings) == 7
    for row in mapping["sections"]:
        for heading in row["target_headings"]:
            assert heading in body, heading
    assert body.startswith("---\n")
    assert body.count("$") % 2 == 0
    assert "$$" not in body
    for malformed in ("$Delta_", "$sum_", "$operatorname", "$\\theta$d"):
        assert malformed not in body, malformed
    assert not any(ord(c) < 32 and c not in "\n\t" for c in body)
    assert "| 5 | 8 | 3064 | 1771 | 10626 |" in body
    assert "18675" in body and "18669" in body
    assert "完整有序历史" in body and "默认" in body and "正有理阈值" in body
    checked_links = 0
    for p in (obj, BASE / "README.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", p.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            destination = (p.parent / target.split("#")[0]).resolve()
            assert destination.exists(), (str(p), target)
            checked_links += 1
    receipt = read_json(ROOT / manifest["receipt"])
    assert receipt["id"] == "d6cb467c51e97a499f39"
    for field in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"):
        assert receipt[field] is True
    for target in receipt["targets"]:
        if target != str((BASE / "self-check.json").relative_to(ROOT)):
            assert (ROOT / target).is_file(), target
    execution = read_json(ROOT / comparison["shared_events"]["original_k1"]["path"])
    assert execution["call_events"]["all_k_padding.py:main"] == 1
    assert execution["additional_original_calls"] == 0
    assert execution["new_independent_DAG_or_IC_audits"] == 0
    terminal = read_json(ROOT / comparison["shared_events"]["terminal_points"]["path"])
    assert terminal["BI_calls"] == 0 and terminal["full_DAG_IC_checks"] == 0
    assert terminal["coverage_supports_checked"] == 185
    assert [p["k"] for p in terminal["points"]] == [1, 5, 10]
    result = {
        "status": "PASS",
        "scope": "Static bytes, parsing, source-section mapping, links and receipt checks only.",
        "hash_records_checked": checked_hashes,
        "json_files_parsed": len(json_files),
        "python_files_parsed_not_executed": len(ast_files),
        "primary_source_sections_accounted_for": 7,
        "links_checked": checked_links,
        "receipt_targets_checked": len(receipt["targets"]),
        "new_original_main_calls_here": 0,
        "new_math_runs_here": 0,
        "new_LP_or_BI_calls_here": 0,
        "shared_event_metadata_checked_without_rerun": ["one original k1 main", "one independent terminal audit"],
        "development_note": "Before the first static package run, manual full-body review corrected a k5 transcription and inline TeX escaping. No mathematical program was rerun.",
    }
    (BASE / "self-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
