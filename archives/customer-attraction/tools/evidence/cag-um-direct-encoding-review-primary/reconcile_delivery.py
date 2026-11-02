#!/usr/bin/env python3
"""Static reconciliation only; does not import or run any mathematical program."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path,
                        help="repository root used only to resolve inherited links")
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    stage = next(parent for parent in package.parents if (parent / "archives").is_dir())
    manifest = json.loads((package / "manifest.json").read_text())
    receipts = json.loads((package / "receipts.json").read_text())
    assert manifest["primary_count"] == len(manifest["sources"]) == len(receipts) == 7
    assert manifest["primary_bytes"] == sum(row["size"] for row in manifest["sources"]) == 52753
    assert {row["id"] for row in manifest["sources"]} == {row["id"] for row in receipts}
    source_checks = []
    for row in manifest["sources"]:
        path = package / row["package_path"]
        assert path.stat().st_size == row["size"]
        assert digest(path) == row["sha256"]
        assert len(row["sources"]) == 2
        assert all(len(source["commit"]) == 40 and source["path"] == row["path"]
                   for source in row["sources"])
        source_checks.append({"id": row["id"], "size": row["size"], "sha256": digest(path)})
    for row in receipts:
        assert all(row[key] is True for key in
                   ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"))
        assert row["disposition"] == "integrated"
        assert all(row[key] for key in ("read_note", "comparison_note", "decision_note", "targets"))
        assert all((stage / target).is_file() for target in row["targets"])
    event_dir = package / "original-entry-001"
    event = json.loads((event_dir / "execution-record.json").read_text())
    frozen_report = package / "original/equivalence_audit/encoding_audit.json"
    assert (event_dir / "stdout.txt").read_bytes() == frozen_report.read_bytes()
    assert (event_dir / "stderr.txt").read_bytes() == b""
    assert event["exit_code"] == 0 and event["stdout_bytes"] == 3002 and event["stderr_bytes"] == 0
    assert event["stdout_sha256"] == digest(frozen_report)
    assert event["original_CLI_calls"] == 1
    assert all(event[key] == 0 for key in ("new_mathematical_kernel_calls",
               "LP_or_random_search_calls", "project_solver_or_verifier_calls"))
    assert event["source_and_frozen_report_unchanged"] is True
    report = json.loads(frozen_report.read_text())
    reciprocal = report["reciprocal_objective_family"]
    union = report["union_configuration_family"]
    assert len(reciprocal) == 5 and len(union) == 4
    program = stage / "archives/customer-attraction/state/程序/两个自然编码的原Fraction审计与有限范围--程序.md"
    prose = program.read_text()
    table_rows = []
    for row in reciprocal:
        cells = [row[key] for key in ("players", "ordered_histories_checked",
                 "deviation_comparisons_including_self", "reciprocal_checks", "cag_welfare",
                 "cag_optimum", "cag_ratio", "scheduling_makespan", "scheduling_optimum")]
        literal = "| " + " | ".join(map(str, cells)) + " |"
        assert literal in prose
        table_rows.append(literal)
    for row in union:
        cells = [row[key] for key in ("machines_and_jobs", "threshold", "ordered_histories_checked",
                 "deviation_comparisons_including_self", "union_catalog_full_spe_welfare",
                 "union_catalog_optimum", "original_scheduling_optimum")]
        cells.append(str(row["grouped_catalog_can_cover_all"]).lower())
        literal = "| " + " | ".join(map(str, cells)) + " |"
        assert literal in prose
        table_rows.append(literal)
    sums = {
        "reciprocal_histories": sum(row["ordered_histories_checked"] for row in reciprocal),
        "reciprocal_comparisons_including_self": sum(row["deviation_comparisons_including_self"] for row in reciprocal),
        "reciprocal_identity_checks": sum(row["reciprocal_checks"] for row in reciprocal),
        "union_histories": sum(row["ordered_histories_checked"] for row in union),
        "union_comparisons_including_self": sum(row["deviation_comparisons_including_self"] for row in union),
    }
    assert list(sums.values()) == [10213, 60276, 3578, 1736, 10206]
    assert sums["reciprocal_histories"] + sums["union_histories"] == 11949
    assert sums["reciprocal_comparisons_including_self"] + sums["union_comparisons_including_self"] == 70482
    assert sum(row["machines_and_jobs"] ** row["machines_and_jobs"] for row in union) == 3412
    formal = sorted({stage / target for row in receipts for target in row["targets"]
                     if target.startswith("archives/customer-attraction/state/")})
    assert len(formal) == 4
    checked_links = []
    for page in formal + [package / "README.md"]:
        text = page.read_text()
        if page in formal:
            assert text.startswith("---\nid: ") and "\nsource_refs:\n" in text
            assert re.search(r"source:[0-9a-f]{40}:research/", text)
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
                continue
            linked = (page.parent / link.split("#", 1)[0]).resolve()
            if linked.is_file():
                location = "stage"
            else:
                relative = linked.relative_to(stage)
                assert (args.repo / relative).is_file(), (str(page), link)
                location = "inherited-repository"
            checked_links.append({"page": str(page.relative_to(stage)), "link": link, "resolved": location})
    literature = json.loads((package / "literature-read-record.json").read_text())
    assert len(literature["primary_sources"]) == 8
    assert all(row["url"].startswith("https://") and row["locations"] and row["scope"]
               and row["version"] and row["retrieval_refs"] for row in literature["primary_sources"])
    assert all(literature[key] is False for key in ("full_paper_reproof_claimed",
               "global_latest_literature_search_claimed", "downloaded_binary_identity_with_frozen_PDF_claimed",
               "verbatim_paper_excerpts_stored"))
    comparison = json.loads((package / "comparison-record.json").read_text())
    publication = json.loads((package / "parent-publication-review.json").read_text())
    corrections = {row["path"]: row for row in publication["mature_final_versions"]}
    comparison_checks = []
    for row in comparison["directly_related_formal_objects"]:
        inherited = args.repo / row["path"]
        expected = corrections.get(row["path"], {"bytes": row["size"], "sha256": row["sha256"]})
        assert inherited.stat().st_size == expected["bytes"] and digest(inherited) == expected["sha256"]
        comparison_checks.append(row["path"])
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "identity": "Boss3",
        "scope": "static hashes, receipt targets, existing event and exact report transcription, local links, literature reading metadata; no mathematical re-execution",
        "primary_source_checks": source_checks,
        "receipt_count": len(receipts),
        "formal_object_count": len(formal),
        "exact_report_rows_checked": len(table_rows),
        "report_field_sums": sums,
        "markdown_links_checked": checked_links,
        "mature_comparison_hash_checks": comparison_checks,
        "primary_publication_records_checked": 8,
        "mathematical_kernel_calls_in_this_static_check": 0,
        "original_CLI_calls_in_this_static_check": 0,
        "all_checks_passed": True,
    }
    (package / "publication-self-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"ok": True, "primary_sources": 7, "receipts": 7,
                      "formal_objects": 4, "report_rows": 9, "links": len(checked_links),
                      "mathematical_reexecutions": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
