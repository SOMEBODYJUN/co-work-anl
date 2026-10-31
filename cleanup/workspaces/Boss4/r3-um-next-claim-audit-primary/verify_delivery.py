"""Read-only exact copy/source/receipt/link checks; never run original programs."""
from pathlib import Path
import ast
import hashlib
import json
import re

WS=Path(__file__).resolve().parent
STAGE=WS.parents[3]
REPO=STAGE.parent.parent/"boss4-research"
E=STAGE/"archives/unrelated-machines/tools/evidence/um-next-claim-audit-primary"
def read(p):
    return json.loads(p.read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    files=read(WS/"copy-files.json")
    assert len(files)==len(set(files))
    actual={str(p.relative_to(STAGE)) for p in STAGE.rglob("*") if p.is_file()}
    assert set(files)==actual
    manifest=read(WS/"delivery-manifest.json")
    own=str((WS/"delivery-manifest.json").relative_to(STAGE))
    assert {d["path"] for d in manifest["files"]}==actual-{own}
    for d in manifest["files"]:
        p=STAGE/d["path"]
        assert p.stat().st_size==d["size"] and sha(p)==d["sha256"]
    cap=read(E/"claim-receipt.json")
    assert cap["status"]=="pushed" and cap["actor"]=="Boss4"
    assert cap["local_sync"]["status"]=="synced"
    assert cap["remote_tip"]=="b01e708c20459c0dbd24243bc8bc92500b7c4e7b"
    assert len(cap["ids"])==5
    pri=read(E/"primary-inventory.json");comp=read(E/"comparison-inventory.json")
    assert len(pri)==5 and len(comp)==14
    assert {d["id"] for d in pri}==set(cap["ids"])
    assert [d["actual_line_count"] for d in pri]==[178,66,95,133,148]
    for d in pri+comp:
        p=STAGE/d["preserved_repo_path"]
        assert p.stat().st_size==d["size"] and sha(p)==d["sha256"]
        assert d["full_file_reviewed"] is True and len(d["read_scope"])>10
        if p.suffix==".py":
            ast.parse(p.read_text())
    receipts=read(WS/"semantic-receipts.json")
    assert len(receipts)==5 and {d["id"] for d in receipts}==set(cap["ids"])
    for d in receipts:
        assert all(d[k] is True for k in ["full_file_reviewed","related_material_checked","unique_content_accounted_for"])
        assert all(len(d[k])>70 for k in ["read_note","comparison_note","decision_note"])
        assert d["disposition"]=="integrated"
        assert d["source_sha256"]==next(p["sha256"] for p in pri if p["id"]==d["id"])
        assert all((STAGE/t).is_file() for t in d["targets"])
    event=read(E/"runs/saved-data-check/execution.json")
    assert event["exit_code"]==0
    assert event["source_sha256"]==sha(E/"verify_saved_data.py")
    assert event["output_sha256"]==sha(E/"data-selfcheck.json")
    assert (E/"runs/saved-data-check/stderr").read_bytes()==b""
    check=read(E/"data-selfcheck.json")
    assert check==read(E/"runs/saved-data-check/stdout")
    assert check["status"]=="passed" and check["new_original_main_runs"]==0
    assert check["inventory_files"]==19
    assert check["pairwise"]["new_explicit_atoms_verified"]==52
    assert check["pairwise"]["new_original_job_checks"]==468
    assert check["row"]["old_legal_assignment_total"]==281090
    assert check["subdivision"]["documented_original_subdivision_inputs"]==260
    assert read(E/"version-relations.json")==check["versions"]
    math=read(WS/"mathematical-selfcheck.json")
    assert math["new_original_program_runs"]==math["git_claim_done_checkpoint_spawn_mutations"]==0
    assert math["all_primary_full_file_reviewed"] is True
    assert math["source_algorithms_imported_by_new_helper"] is False
    pages=sorted((STAGE/"archives/unrelated-machines/state/资源").glob("*.md"))
    assert len(pages)==4
    links=0
    for p in pages+[E/"README.md"]:
        text=p.read_text()
        assert text.count(r"\[")==text.count(r"\]")
        assert text.count(r"\(")==text.count(r"\)")
        assert not any(ord(c)<32 and c not in "\n\t\r" for c in text)
        if p in pages:
            front=text.split("---",2)[1]
            assert all("\n"+k+":" in "\n"+front for k in ["id","kind","type_tag","title","status","summary","source_refs"])
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",text):
            if "://" in target or target.startswith("#"):
                continue
            q=(p.parent/target.split("#")[0]).resolve()
            rel=q.relative_to(STAGE)
            assert q.is_file() or (REPO/rel).is_file(),(p,target)
            links+=1
    for d in read(E/"relationship-review.json")["relations"]:
        if "related_object" in d:
            assert (REPO/d["related_object"]).is_file()
    prior=read(E/"existing-formal-comparison.json")
    assert len(prior)==6 and all(d["full_file_reviewed"] is True and d["shared_file_modified"] is False for d in prior)
    candidates=read(WS/"next-candidates.json")["candidates"]
    assert len(candidates)==len({d["id"] for d in candidates})==5
    assert not set(cap["ids"]) & {d["id"] for d in candidates}
    print(json.dumps({"status":"passed","files":len(files),"bytes":sum((STAGE/f).stat().st_size for f in files),
                      "primary_receipts":5,"formal_objects":4,"originals_and_comparisons":19,
                      "links":links,"new_original_main_runs":0},ensure_ascii=False))
if __name__=="__main__":
    main()
