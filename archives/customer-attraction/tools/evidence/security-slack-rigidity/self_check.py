"""Static package check: no imports or execution of mathematical source programs."""
import ast
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = next(p for p in BASE.parents if (p / "cleanup" / "OBJECTS.md").is_file())


def js(p):
    return json.loads(p.read_text())


def main():
    manifest = js(BASE / "source-manifest.json")
    comparison = js(BASE / "comparison.json")
    mapping = js(BASE / "source-to-object.json")
    hashes = 0
    parsed_json, parsed_py = set(), set()
    for row in manifest["artifacts"] + comparison["read_material"]:
        p = ROOT / row["path"]
        raw = p.read_bytes()
        assert len(raw) == row["bytes"], row["path"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"], row["path"]
        hashes += 1
        if p.suffix == ".json":
            js(p)
            parsed_json.add(row["path"])
        if p.suffix == ".py":
            ast.parse(raw.decode(), filename=str(p))
            parsed_py.add(row["path"])
    source = (BASE / "original/security_slack_rigidity.md").read_text()
    heads = [x for x in source.splitlines() if x.startswith("##")]
    assert heads == [x["source_heading"] for x in mapping["sections"]]
    assert len(heads) == 6
    obj = ROOT / manifest["object"]
    body = obj.read_text()
    for row in mapping["sections"]:
        assert row["accounted_for"]
        for head in row["target_headings"]:
            assert head in body
    assert body.count("$") % 2 == 0
    assert body.count(r"\[") == body.count(r"\]") == 38
    assert not any(ord(c) < 32 and c not in "\n\t" for c in body)
    assert "R_{\\rm ov}+R_{\\rm out}\n+\\sum_{j=1}^n" in body
    assert "\n+(n-1)\\sum_Aq_A(\\delta_A+J_A)." in body
    for token in ("n\\ge2", "唯一", "不能", "1308", "1299", "1275", "80", "700"):
        assert token in body, token
    links = 0
    for p in (obj, BASE / "README.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", p.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            assert (p.parent / target.split("#")[0]).resolve().exists(), (p, target)
            links += 1
    receipt = js(ROOT / manifest["receipt"])
    assert receipt["id"] == "5c735a989e8198af4037"
    for key in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"):
        assert receipt[key] is True
    for target in receipt["targets"]:
        if target != str((BASE / "self-check.json").relative_to(ROOT)):
            assert (ROOT / target).is_file(), target
    event = js(ROOT / comparison["shared_successor_event"])
    assert event["original_successor_main_calls"] == 1
    assert event["author_main_calls"] == 0
    assert event["LP_calls"] == 0 and event["SPE_solver_calls"] == 0
    assert event["new_output_byte_identical_to_frozen"] is True
    report = js(ROOT / comparison["author_frozen_report"])
    assert len(report["cases"]) == 12
    assert [report[k] for k in ("scalar_tangent_checks", "full_background_checks", "sharp_identity_checks")] == [700, 1308, 1299]
    result = {
        "status": "PASS",
        "scope": "Static integrity, parsing, formula-text, section coverage, links and receipt only.",
        "hash_records_checked": hashes,
        "json_files_parsed": len(parsed_json),
        "python_files_parsed_not_executed": len(parsed_py),
        "primary_semantic_headings_accounted_for": 6,
        "display_math_pairs_checked": 38,
        "links_checked": links,
        "receipt_targets_checked": len(receipt["targets"]),
        "original_main_calls_here": 0,
        "new_math_runs_here": 0,
        "new_BI_LP_SPE_calls_here": 0,
        "shared_successor_event_metadata_read_without_rerun": True,
        "manual_draft_correction": "Before formal publication, two missing displayed plus signs in the slack identity were restored and all 38 displayed formulas were read. No mathematical program was rerun.",
    }
    (BASE / "self-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
