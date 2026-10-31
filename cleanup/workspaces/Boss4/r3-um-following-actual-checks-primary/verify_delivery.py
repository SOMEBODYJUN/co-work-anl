"""Read-only final exact-file/claim/scope/receipt/link checks; no original runs."""
from pathlib import Path
import ast
import hashlib
import json
import re
WS=Path(__file__).resolve().parent
STAGE=WS.parents[3]
REPO=STAGE.parent.parent/"boss4-research"
E=STAGE/"archives/unrelated-machines/tools/evidence/um-following-actual-checks-primary"
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    files=read(WS/"copy-files.json")
    assert len(files)==len(set(files))
    actual={str(p.relative_to(STAGE)) for p in STAGE.rglob("*") if p.is_file()}
    assert set(files)==actual
    own=str((WS/"delivery-manifest.json").relative_to(STAGE))
    manifest=read(WS/"delivery-manifest.json")
    assert {d["path"] for d in manifest["files"]}==actual-{own}
    for d in manifest["files"]:
        p=STAGE/d["path"]
        assert p.stat().st_size==d["size"] and sha(p)==d["sha256"]
    cap=read(E/"claim-receipt.json")
    assert cap["status"]=="pushed" and cap["actor"]=="Boss4"
    assert cap["local_sync"]["status"]=="synced"
    assert cap["remote_tip"]=="492eb43e668edea3bd8ca9fe2b2517717919c453"
    P=read(E/"primary-inventory.json");C=read(E/"comparison-inventory.json")
    assert len(P)==5 and len(C)==25
    assert set(cap["ids"])=={d["id"] for d in P}
    assert [d["actual_line_count"] for d in P]==[144,554,195,177,202]
    assert all(d["full_file_reviewed"] is True for d in P)
    assert {d["id"] for d in C if d["full_file_reviewed"] is False}=={
        "c43c08d4bf6fe07ad2bf","6e5b68e01092324cf1e7"}
    for d in P+C:
        p=STAGE/d["preserved_repo_path"]
        assert p.stat().st_size==d["size"] and sha(p)==d["sha256"]
        assert len(d["read_scope"])>15
        if p.suffix==".py":ast.parse(p.read_text())
    receipts=read(WS/"semantic-receipts.json")
    assert len(receipts)==5 and {d["id"] for d in receipts}==set(cap["ids"])
    for d in receipts:
        assert all(d[k] is True for k in ["full_file_reviewed","related_material_checked","unique_content_accounted_for"])
        assert all(len(d[k])>70 for k in ["read_note","comparison_note","decision_note"])
        assert d["disposition"]=="integrated"
        assert d["source_sha256"]==next(p["sha256"] for p in P if p["id"]==d["id"])
        assert all((STAGE/t).is_file() for t in d["targets"])
    event=read(E/"runs/activation-original/execution.json")
    assert event["exit_code"]==0 and event["original_main_new_runs"]==1
    assert event["new_empty_directory"] is True and event["source_sha256"]==P[0]["sha256"]
    assert event["stdout_sha256"]==sha(E/"runs/activation-original/stdout")
    assert (E/"runs/activation-original/stdout").read_text()=="multi_activation_cover_replication: PASS\n"
    run=read(E/"runs/data-check/execution.json")
    assert run["exit_code"]==0 and run["source_sha256"]==sha(E/"verify_saved_data.py")
    assert run["output_sha256"]==sha(E/"data-selfcheck.json")
    for name in ["activation-original","data-check"]:
        assert (E/"runs"/name/"stderr").read_bytes()==b""
    data=read(E/"data-selfcheck.json")
    assert data==read(E/"runs/data-check/stdout")
    assert data["status"]=="passed" and data["inventory_files"]==30
    assert data["new_original_main_runs"]==1
    assert data["outer"]["new_direct_outcomes_checked"]==4964
    assert data["fee"]["saved_witness_job_checks"]==824
    assert data["HS"]["all_saved_input_atoms_checked"]==168
    assert data["HS"]["feature_rank_pairs_checked"]==21
    assert data["HS"]["output_job_checks"]==86
    prefix=E/"versions/multi-outer-v1-exact-175-line-prefix.md"
    assert len(prefix.read_text().splitlines())==175
    assert sha(prefix)=="84d6031655ac43d9c5726ed2cac6f5241e709743232290e604d767602613778a"
    assert read(E/"version-relations.json")["multi_outer"]["current_file_read_in_full"] is False
    math=read(WS/"mathematical-selfcheck.json")
    assert math["all_five_primary_full_read"] is True
    assert math["new_original_main_runs"]==1 and math["remaining_four_new_original_runs"]==0
    assert math["git_claim_done_checkpoint_spawn_mutations"]==0
    suggestions=read(E/"unapplied-formal-corrections.json")
    assert len(suggestions)==3
    for d in suggestions:
        p=STAGE/d["snapshot_repo_path"]
        assert sha(p)==d["old_sha256"]
        assert p.read_text().splitlines()[d["old_line_number"]-1]==d["exact_old_line"]
        assert p.read_text().count(d["before_fragment"])==1
        assert d["old_shared_page_modified"] is False
    pages=sorted((STAGE/"archives/unrelated-machines/state/资源").glob("*.md"))
    assert len(pages)==5
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
            if "://" in target or target.startswith("#"):continue
            q=(p.parent/target.split("#")[0]).resolve()
            rel=q.relative_to(STAGE)
            assert q.is_file() or (REPO/rel).is_file(),(p,target)
            links+=1
    for d in read(E/"relationship-review.json")["relations"]:
        if "related_object" in d:assert (REPO/d["related_object"]).is_file()
    old=read(E/"existing-formal-comparison.json")
    assert len(old)==8 and all(d["shared_file_modified"] is False for d in old)
    candidates=read(WS/"next-candidates.json")["candidates"]
    assert len(candidates)==len({d["id"] for d in candidates})==5
    assert not set(cap["ids"]) & {d["id"] for d in candidates}
    print(json.dumps({"status":"passed","files":len(files),"bytes":sum((STAGE/f).stat().st_size for f in files),
                      "primary_receipts":5,"formal_resources":5,"original_and_comparison_files":30,
                      "comparison_partial_scopes_explicit":2,"links":links,"new_original_main_runs":1,
                      "unapplied_old_page_corrections":3},ensure_ascii=False))
if __name__=="__main__":main()
