#!/usr/bin/env python3
"""Structural and byte checks only. Never imports or reruns the math audit."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import sys

ST = Path(__file__).resolve().parents[3]
REPO = ST.parents[1] / "boss4-research"
E = Path("tools/evidence/um-missing-one-pin-kernel-primary")
W = Path("cleanup/workspaces/Boss4/r3-um-missing-one-and-pin-kernel-primary")
M = W / "copy-files.json"
V = E / "validation.json"


def read(p):
    return json.loads((ST/p).read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def validate(check_manifest=True):
    source = read(E/"source-manifest.json")
    ids = {s["id"] for s in source}
    assert ids == {"dfb63d624df20561d5c2", "fa8aa02838496fdcc909", "61a03c090144ca4e8673", "f898a9baa38fb0fd0651", "08baacbc6f2f2edb158e"}
    claim = read(E/"actual-claim.json")
    assert claim["status"] == "pushed" and claim["actor"] == "Boss4" and claim["operation"] == "claim"
    assert ids <= set(claim["ids"]) and claim["local_sync"]["status"] == "synced"
    assert claim["remote_tip"] == "c59d0557ab194d2f8e0cf6563e29b97427609a1e"
    coverage = read(E/"primary-read-coverage.json")
    for s in source:
        p = ST/s["preserved_path"]
        assert sha(p) == s["sha256"] and p.stat().st_size == s["size"]
        assert len(p.read_text().splitlines()) == s["lines"] and s["actual_full_read"]
        ranges = sorted((a["first_line"], a["last_line"]) for a in coverage if a["id"] == s["id"])
        assert ranges[0][0] == 1 and ranges[-1][1] == s["lines"]
        assert all(a[1]+1 == b[0] for a, b in zip(ranges, ranges[1:]))
        assert all(a["actual_read"] for a in coverage if a["id"] == s["id"])
    layout = read(E/"formal-layout.json")
    assert len(layout) == 7 and len({a["id"] for a in layout}) == 7
    checked_links = 0
    for a in layout:
        p = ST/a["path"]
        b = p.read_text()
        assert b.startswith("---\n") and "\n---\n" in b[4:]
        header = b.split("\n---\n", 1)[0][4:]
        fields = {}
        for line in header.splitlines():
            k, v = line.split(": ", 1)
            fields[k] = json.loads(v)
        assert fields["id"] == a["id"] and fields["kind"] == "review" and fields["type_tag"] == "审查"
        assert fields["status"] and fields["summary"] and fields["source_refs"]
        for k in ("id", "kind", "type_tag", "title", "status", "summary", "source_refs"):
            assert k in fields
        for target in re.findall(r"\]\(([^)]+)\)", b):
            target = target.split("#", 1)[0]
            if not target or "://" in target:
                continue
            q = (p.parent/target).resolve()
            rel = q.relative_to(ST)
            assert q.exists() or (REPO/rel).exists(), (a["path"], target)
            checked_links += 1
        # A new ID may already have been copied to the exact same destination later;
        # another current formal with the same ID would be a duplicate object.
        for old in (REPO/"archives/unrelated-machines/state").rglob("*.md"):
            if old.relative_to(REPO).as_posix() == a["path"]:
                continue
            first = old.read_text().split("\n---\n", 1)[0]
            assert not re.search(r'^id:\s*["\']?'+re.escape(a["id"])+r'["\']?\s*$', first, re.M)
    receipts = read(W/"semantic-receipts.json")
    assert {a["id"] for a in receipts} == ids
    for a in receipts:
        assert all(a[k] is True for k in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"))
        assert a["disposition"] == "integrated" and a["read_note"] and a["comparison_note"] and a["decision_note"]
        assert a["targets"] == [x["path"] for x in layout if a["id"] in x["primary_ids"]]
    support = read(E/"supporting-source-manifest.json")
    assert len(support) == 4
    for a in support:
        assert sha(ST/a["preserved_path"]) == a["sha256"] and not a["extra_receipt"]
    ab = next(a for a in support if a["id"] == "ab79c520ba1a75adf3ef")
    assert ab["actual_read_ranges"] == [[1, 104]] and not ab["full_file_read_this_batch"]
    prior = next(a for a in support if a["id"] == "8ce8667e13d3c4d60937")
    assert prior["prior_full_actual_lines_reused"] == 624 and not prior["full_file_read_this_batch"]
    comparisons = read(E/"comparison-manifest.json")
    assert len(comparisons) == 7
    for a in comparisons:
        assert sha(ST/a["snapshot"]) == a["sha256"]
        assert a["actual_read_ranges"] == [[1, a["lines"]]] and not a["extra_receipt"]
    versions = read(E/"version-and-scope-checks.json")
    for a in versions["embedded_exact_byte_bindings"]:
        b = (ST/E/"original"/(a["source_id"]+".md")).read_bytes()
        if a["source_id"] == "fa8aa02838496fdcc909":
            marker = "# 多输入缺一输出三半计数：作者完整证明实读后攻击".encode()
            block = b[b.index(marker):]
        else:
            block = b.split(b"\n---\n\n", 1)[1]
        assert hashlib.sha256(block).hexdigest() == a["body_sha256"] and len(block) == a["body_bytes"]
    audit = read(E/"run-small-exact/report.json")
    assert audit["status"] == "all exact Fraction assertions passed"
    assert audit["code_sha256"] == sha(ST/E/"independent-small-audit.py")
    assert audit["new_independent_math_audit_runs"] == 1 and audit["archived_program_runs"] == 0
    assert audit["external_solver_calls"] == 0 and audit["archived_module_imports"] == 0
    assert audit["tiny_heavy_count"]["assignments"] == 81 and not audit["tiny_heavy_count"]["lp_opt_computed"]
    assert audit["requested_pin_q2"]["complete_assignments_checked"] == 16384
    assert audit["requested_pin_q2"]["threshold_predicate_comparisons"] == 144
    assert audit["weighted_one_edge"]["selected_right_query_stays_root"] and not audit["weighted_one_edge"]["OPT_computed"]
    er = E/"errata-prefix-convexification"
    em = read(er/"errata-manifest.json")
    before, proposed = (ST/er/"before.md").read_text(), (ST/er/"proposed.md").read_text()
    assert sha(ST/er/"before.md") == em["before_sha256"] and sha(ST/er/"proposed.md") == em["proposed_sha256"]
    assert before.count(em["exact_original_subparagraph"]) == 1
    assert before.replace(em["exact_original_subparagraph"], em["exact_replacement"]) == proposed
    patch = ''.join(difflib.unified_diff(before.splitlines(True), proposed.splitlines(True),
                    fromfile='a/'+em["target_path"], tofile='b/'+em["target_path"]))
    assert patch == (ST/er/"correction.patch").read_text()
    assert before[:before.index(em["exact_original_subparagraph"])].count("\n")+1 == em["original_paragraph_line"] == 59
    relations = read(W/"relations.json")["relations"]
    assert len(relations) == 12 and all(a["common_premises"] and a["evidence"] and a["gap"] and not a["phase3_graph_written"] for a in relations)
    json_files = list(ST.rglob("*.json"))
    for p in json_files:
        json.loads(p.read_text())
    expected_paths = {p.relative_to(ST).as_posix() for p in ST.rglob("*") if p.is_file()} | {M.as_posix(), V.as_posix()}
    if check_manifest:
        m = read(M)
        assert m["ready"] is True and m["external_root"] == str(ST)
        assert set(m["copy_paths"]) == expected_paths
        assert len(m["copy_paths"]) == len(set(m["copy_paths"]))
        assert set(m["files"]) == expected_paths-{M.as_posix()}
        for path, a in m["files"].items():
            p = ST/path
            assert sha(p) == a["sha256"] and p.stat().st_size == a["bytes"], path
    return {"status": "all structural and byte checks passed", "primary_sources": 5,
            "primary_bytes": sum(s["size"] for s in source), "primary_lines": sum(s["lines"] for s in source),
            "contiguous_actual_read_blocks": len(coverage), "formal_pages": 7,
            "formal_lines": sum(len((ST/a["path"]).read_text().splitlines()) for a in layout),
            "formal_local_links_checked": checked_links, "supporting_sources": 4,
            "support_prior_full_actual_lines_reused": 624, "support_selected_ab79_lines": 104,
            "current_formal_comparisons": 7, "comparison_actual_lines": sum(a["lines"] for a in comparisons),
            "receipts": 5, "relations": 12, "exact_copy_files": len(expected_paths),
            "embedded_byte_hashes_matched": 3, "new_math_audit_runs_recorded": 1,
            "archived_math_program_runs": 0, "new_errata_replacements_proposed": 1,
            "verification_limit": "structural and byte checks do not prove mathematics, historical independence, or archived program correctness"}


if __name__ == "__main__":
    preparing = "--prepare-validation" in sys.argv
    result = validate(check_manifest=not preparing)
    report = json.dumps(result, ensure_ascii=False, indent=2)+"\n"
    if preparing:
        (ST/V).write_text(report)
        print(json.dumps({"status": "prepared report for final manifest validation; not READY yet", **result}, ensure_ascii=False))
    else:
        assert (ST/V).read_text() == report
        print(json.dumps(result, ensure_ascii=False))
