"""Exact delivery/claim/receipt/link checks; no original program execution."""
from pathlib import Path
import hashlib
import json
import re

WS = Path(__file__).resolve().parent
STAGE = WS.parents[3]
REPO = STAGE.parent.parent / "boss4-research"
E = STAGE / "archives/unrelated-machines/tools/evidence/um-following-palette-and-distortion-primary"

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    files = read(WS / "copy-files.json")
    assert len(files) == len(set(files))
    assert set(files) == {str(p.relative_to(STAGE)) for p in STAGE.rglob("*") if p.is_file()}
    delivery = read(WS / "delivery-manifest.json")
    for d in delivery["files"]:
        p = STAGE/d["path"]
        assert p.stat().st_size == d["size"] and sha(p) == d["sha256"]
    claim = read(E/"claim-receipt.json")
    assert claim["status"] == "pushed" and claim["actor"] == "Boss4"
    assert claim["local_sync"]["status"] == "synced"
    assert claim["remote_tip"] == "46517e4362599a3681dfc1c9f9c2d4761f0e1433"
    receipts = read(WS/"semantic-receipts.json")
    assert len(receipts) == 5 and {d["id"] for d in receipts} == set(claim["ids"])
    for d in receipts:
        assert all(d[k] is True for k in ["full_file_reviewed","related_material_checked","unique_content_accounted_for"])
        assert all(len(d[k])>40 for k in ["read_note","comparison_note","decision_note"])
        assert d["disposition"] == "integrated"
        assert all((STAGE/target).is_file() for target in d["targets"])
    old = read(E/"saved-data-check-execution/execution.json")
    final = read(E/"saved-data-final-matrix-check-execution/execution.json")
    assert old["exit_code"] == final["exit_code"] == 0
    assert old["script_sha256"] == sha(E/"saved-data-check-execution/executed-script.py")
    assert final["script_sha256"] == sha(E/"verify_saved_data.py")
    for name in ["saved-data-check-execution","saved-data-final-matrix-check-execution"]:
        assert (E/name/"stderr").read_bytes() == b""
        assert read(E/name/"stdout")["status"] == "passed"
    assert read(E/"saved-data-selfcheck.json") == read(E/"saved-data-final-matrix-check-execution/stdout")
    assert read(E/"saved-data-selfcheck.json")["original_program_new_runs"] == 0
    primary = read(E/"primary-inventory.json")
    compare = read(E/"comparison-inventory.json")
    assert len(primary) == 5 and len(compare) == 14
    for d in primary+compare:
        p = STAGE/d["preserved_repo_path"]
        assert sha(p) == d["sha256"] and p.stat().st_size == d["size"]
    assert next(d for d in compare if d["id"]=="2fbfc0ca1d7366227c6e")["full_file_reviewed"] is False
    pages = list((STAGE/"archives/unrelated-machines/state/资源").glob("*.md"))
    assert len(pages) == 4
    links = 0
    for p in pages+[E/"README.md"]:
        text = p.read_text()
        assert text.count(r"\[") == text.count(r"\]")
        assert text.count(r"\(") == text.count(r"\)")
        assert not any(ord(c)<32 and c not in "\n\t\r" for c in text)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",text):
            if "://" in target or target.startswith("#"):
                continue
            path = (p.parent/target.split("#")[0]).resolve()
            relative = path.relative_to(STAGE)
            assert path.exists() or (REPO/relative).exists(), (p,target)
            links += 1
    for d in read(E/"unapplied-formal-clarifications.json"):
        p = E/"existing-formal-snapshots"/Path(d["target_repo_path"]).name
        assert sha(p) == d["old_sha256"] and d["exact_old_line"] in p.read_text()
        assert d["old_shared_page_modified"] is False
    print(json.dumps({"status":"passed","files":len(files),"bytes":sum((STAGE/f).stat().st_size for f in files),
                      "primary_receipts":5,"formal_objects":4,"local_links":links,
                      "new_original_program_runs":0},ensure_ascii=False))

if __name__ == "__main__":
    main()
