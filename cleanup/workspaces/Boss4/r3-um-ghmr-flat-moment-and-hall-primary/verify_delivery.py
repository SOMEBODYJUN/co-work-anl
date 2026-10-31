"""Read-only exact delivery checks. Never imports or runs an original algorithm."""
from pathlib import Path
import ast
import hashlib
import json
import re

WS = Path(__file__).resolve().parent
STAGE = WS.parents[3]
REPO = STAGE.parent.parent / "boss4-research"
E = STAGE / "archives/unrelated-machines/tools/evidence/um-ghmr-flat-moment-and-hall-primary"

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    files = read(WS / "copy-files.json")
    assert len(files) == len(set(files))
    actual = {str(p.relative_to(STAGE)) for p in STAGE.rglob("*") if p.is_file()}
    assert set(files) == actual
    manifest = read(WS / "delivery-manifest.json")
    own = str((WS / "delivery-manifest.json").relative_to(STAGE))
    assert {d["path"] for d in manifest["files"]} == actual - {own}
    for d in manifest["files"]:
        p = STAGE / d["path"]
        assert p.stat().st_size == d["size"] and sha(p) == d["sha256"]
    claim = read(E / "claim-receipt.json")
    subset = read(E / "assigned-subset.json")
    assert claim["status"] == "pushed" and claim["actor"] == "Boss4"
    assert claim["local_sync"]["status"] == "synced"
    assert claim["remote_tip"] == "372a7d401e044cd87f4457e55b6ae7e79704565a"
    assert len(claim["ids"]) == subset["claim_total_ids"] == 20
    ids = set(subset["assigned_primary_ids"])
    assert len(ids) == 5 and ids < set(claim["ids"])
    assert set(subset["unassigned_claim_ids_not_primary_here"]) == set(claim["ids"]) - ids
    primary = read(E / "primary-inventory.json")
    compare = read(E / "comparison-inventory.json")
    assert len(primary) == 5 and len(compare) == 15
    assert {d["id"] for d in primary} == ids
    for d in primary + compare:
        p = STAGE / d["preserved_repo_path"]
        assert p.stat().st_size == d["size"] and sha(p) == d["sha256"]
        assert d["full_file_reviewed"] is True and len(d["read_scope"]) > 15
        if p.suffix == ".py":
            ast.parse(p.read_text())
    assert [d["actual_line_count"] for d in primary] == [359, 312, 258, 115, 510]
    receipts = read(WS / "semantic-receipts.json")
    assert len(receipts) == 5 and {d["id"] for d in receipts} == ids
    for d in receipts:
        assert all(d[k] is True for k in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"])
        assert all(len(d[k]) > 60 for k in ["read_note", "comparison_note", "decision_note"])
        assert d["disposition"] == "integrated"
        assert all((STAGE / target).is_file() for target in d["targets"])
        assert d["source_sha256"] == next(p["sha256"] for p in primary if p["id"] == d["id"])
    event = read(E / "runs/global-flat-original/execution.json")
    assert event["exit_code"] == 0 and event["source_algorithms_run"] == 1
    assert event["output_previously_existed"] is False
    assert event["source_sha256"] == primary[1]["sha256"]
    assert event["output_sha256"] == sha(E / "runs/global-flat-original/full-report.json")
    assert event["output_sha256"] == "6bd209971cc7ebe241263e6022054b04b706c5fee04f54efe35bc5b383c6c498"
    final = read(E / "runs/data-check-final/execution.json")
    assert final["exit_code"] == 0
    assert final["source_sha256"] == sha(E / "verify_saved_data.py")
    assert final["output_sha256"] == sha(E / "data-selfcheck.json")
    assert read(E / "runs/data-check-final/stdout") == read(E / "data-selfcheck.json")
    for name in ["global-flat-original", "data-check-final"]:
        assert (E / "runs" / name / "stderr").read_bytes() == b""
    data = read(E / "data-selfcheck.json")
    assert data["status"] == "passed" and data["inventory_files"] == 20
    assert data["new_original_program_runs"] == 1
    assert data["half_unit"]["primary_rows"] == 362
    assert data["hall"]["original_assignments_enumerated"] == 2152
    assert data["hall"]["all_original_output_jobs_checked"] == 46
    assert data["flat_moment"]["all_flat_moments_reconstructed"] == 211
    check = read(WS / "mathematical-selfcheck.json")
    assert check["status"] == "complete-substantive-read-and-passed-bounded-verification"
    assert check["git_claim_done_checkpoint_spawn_mutations"] == 0
    assert check["new_original_program_runs"] == 1 and check["other_four_new_original_runs"] == 0
    pages = sorted((STAGE / "archives/unrelated-machines/state/资源").glob("*.md"))
    assert len(pages) == 4
    links = 0
    for p in pages + [E / "README.md"]:
        text = p.read_text()
        assert text.count(r"\[") == text.count(r"\]")
        assert text.count(r"\(") == text.count(r"\)")
        assert not any(ord(c) < 32 and c not in "\n\t\r" for c in text)
        if p in pages:
            front = text.split("---", 2)[1]
            assert all(f"\n{k}:" in "\n" + front for k in ["id", "kind", "type_tag", "title", "status", "summary", "source_refs"])
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            path = (p.parent / target.split("#")[0]).resolve()
            relative = path.relative_to(STAGE)
            assert path.exists() or (REPO / relative).exists(), (p, target)
            links += 1
    suggestions = read(E / "unapplied-formal-clarifications.json")
    assert len(suggestions) == 3
    for d in suggestions:
        p = STAGE / d["snapshot_repo_path"]
        assert sha(p) == d["old_sha256"]
        assert p.read_text().splitlines()[d["old_line_number"] - 1] == d["exact_old_line"]
        assert d["old_shared_page_modified"] is False
    for r in read(E / "relationship-review.json")["relations"]:
        if "related_object" in r:
            assert (REPO / r["related_object"]).is_file()
    candidates = read(WS / "next-candidates.json")["candidates"]
    assert len(candidates) == len({d["id"] for d in candidates}) == 5
    assert not ids & {d["id"] for d in candidates}
    print(json.dumps({"status": "passed", "files": len(files),
                      "bytes": sum((STAGE / f).stat().st_size for f in files),
                      "primary_receipts": 5, "formal_objects": 4,
                      "original_and_comparison_files": 20, "local_links": links,
                      "new_original_program_runs": 1, "unapplied_old_page_suggestions": 3},
                     ensure_ascii=False))

if __name__ == "__main__":
    main()
