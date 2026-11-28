"""Bind a completed, rejected release review without hashing a file from inside itself."""
import argparse
import gzip
import hashlib
import io
import json
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]
REPO = HERE.parents[4]
PREFIX = str(W.relative_to(REPO)) + "/"
OWN = str(HERE.relative_to(W)) + "/"
ACTOR = "boss 1"
REVIEWER = "/root/release_audit"
RUN = "35440ff34fc845dbaa2b3d94cf6d2c00"
REQUIRED = ["sources","frameworks","models","hyperedges","judgments","household_engine","offline_ui","independent_review","fresh_restore"]
FORMAL = ["formal/report.md","formal/judgments.json","formal/scenarios.json","formal/calculator.html"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    return sha(path.read_bytes())


def obj(path):
    return json.loads(path.read_text())


def write(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")


def canonical(data):
    return json.dumps(data,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()


def git(*args):
    return subprocess.check_output(["git",*args],cwd=REPO)


def workspace_path(raw):
    assert raw and not Path(raw).is_absolute() and ".." not in Path(raw).parts
    real = (W/raw).resolve()
    assert real.is_relative_to(W) and real.is_file(), raw
    return real


def index_archive(container,label,index):
    with zipfile.ZipFile(container) as archive:
        members={}
        for name in sorted(archive.namelist()):
            if name.endswith("/"):
                continue
            data=archive.read(name)
            members[name]=sha(data)
            if Path(name).suffix in {".npz",".zip"}:
                index_archive(io.BytesIO(data),label+"!"+name,index)
        index[label]=members


def registered_versions(state):
    rows=[]
    for sid, latest in sorted(state["sources"].items()):
        versions = latest.get("versions",[]) + [latest]
        for v in versions:
            p=workspace_path(v["blob"])
            actual=digest(p)
            assert actual==v["body_sha256"] and p.stem==actual, (sid,v["revision"])
            rows.append({
                "id":sid,"revision":v["revision"],"current":v["revision"]==latest["revision"],
                "kind":v["kind"],"stored_body":v["blob"],"sha256":actual,"bytes":p.stat().st_size,
                "source_family":v.get("source_family"),"locator_or_url":v["url"],
                "publication_as_recorded":v.get("published_at"),"observation_period":v.get("observation_period"),
                "separately_recorded_publisher_file_sha256":v.get("sha256_original")
            })
    known={r["stored_body"] for r in rows}
    assert known=={str(p.relative_to(W)) for p in (W/"source_blobs").glob("*.bin")}
    return rows


def historical_receipts():
    econ="research/tasks/research_independent_review/"
    family="research/tasks/household_independent_audit/"
    engine="research/tasks/household_engine/"
    restore="research/tasks/fresh_restore/"
    econ_doc=obj(W/(econ+"economic_checks.json"))
    old_num=obj(W/(family+"numeric_report.json"))
    old_receipt=obj(W/(family+"engine_receipt.json"))
    initial=obj(W/(restore+"receipt.json"))
    bindings = [
        (econ+"economic_checks.json","6aedb5a",econ_doc["file_sha256"]),
        (econ+"economic_delta.json","d139823",obj(W/(econ+"economic_delta.json"))["current_file_sha256"]),
        (family+"engine_receipt.json","f4be661",{family+k:v for k,v in old_receipt["artifacts"].items()}),
        (family+"numeric_report.json","f4be661",{engine+k:v for k,v in old_num["reviewedArtifacts"].items()}),
        (restore+"receipt.json","5f5f74b",initial["artifact_sha256"]),
        (restore+"receipt.json",initial["source_commit"],initial["frozen_formal_sha256"]),
        (OWN+"pre_repair_results.json","1580e86",{"formal/calculator.html":obj(HERE/"pre_repair_results.json")["htmlSha256"]}),
    ]
    evidence=[]
    for src,revision,mapping in bindings:
        commit=git("rev-parse",revision).decode().strip()
        rows={}
        for rel,expected in mapping.items():
            git_path=PREFIX+rel
            old=git("show",commit+":"+git_path)
            assert sha(old)==expected,(src,rel,commit)
            current=(W/rel).is_file() and digest(W/rel)==expected
            rows[rel]={"sha256":expected,"also_current_bytes":current}
        evidence.append({"receipt":src,"commit_containing_reviewed_bytes":commit,"files":rows})
    return evidence


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--formal-commit",required=True)
    args=ap.parse_args()
    commit=git("rev-parse",args.formal_commit).decode().strip()
    head=git("rev-parse","HEAD").decode().strip()
    assert subprocess.run(["git","merge-base","--is-ancestor",commit,head],cwd=REPO).returncode==0
    state_path=W/"research_state.json"
    state_bytes=state_path.read_bytes()
    state=json.loads(state_bytes)
    rt=state["runtime"]
    assert (rt["actor"],rt["run_id"],rt["location"]["workspace_key"],state["cycle"],state["mode"]) == (ACTOR,RUN,"work/boss 1",1,"first")
    assert state["release"] is None
    acceptance = obj(W/"research/acceptance.json")
    audit = obj(HERE/"content_review.json")
    assert (acceptance["author"],acceptance["reviewer"],acceptance["input_kind"],acceptance["cycle"]) == (ACTOR,REVIEWER,"real_research",1)
    selected = {item["id"]:item["verdict"] for item in acceptance["checks"]}
    assert selected=={item["id"]:item["verdict"] for item in audit["checks"]}
    assert set(selected)==set(REQUIRED) and selected["offline_ui"]=="blocked" and audit["overall_release_verdict"]=="reject"
    assert acceptance["overall_verdict"] in {"blocked","reject"} and acceptance["reviewed_content_commit"]==commit
    assert audit["acceptance_sha256"]==digest(W/"research/acceptance.json")
    assert digest(HERE/"final_review.md")==digest(W/"research/final_review.md")
    formal={}
    for rel in FORMAL:
        data=git("show",commit+":"+PREFIX+rel)
        assert sha(data)==digest(W/rel), rel
        formal[rel]=sha(data)
    assert formal==audit["formal_sha256"]==acceptance["formal_sha256"]
    stage_map={}
    for stage,d in state["stages"].items():
        stage_map[stage]={}
        for rel,expected in d["files"].items():
            p=workspace_path(rel)
            assert digest(p)==expected, (stage,rel)
            stage_map[stage][rel]=expected
    assert len(stage_map)==17 and sorted(stage_map)[-1]=="s17_writing"
    acceptance_map={c["id"]:{p:digest(workspace_path(p)) for p in c["artifacts"]} for c in acceptance["checks"]}
    for paths in acceptance_map.values():
        assert not ({OWN+"receipt.json",OWN+"reviewed_files.json"}&paths.keys())
    rows=registered_versions(state)
    write(HERE/"source_blob_inventory.json",{
        "snapshot_run_id":RUN,"actor":ACTOR,"cycle":1,"schema":"research-source-body-inventory.v1",
        "meaning":"SHA-256 covers the actual stored bytes for each current or superseded registered record. Many are extracts or research records. A separately supplied publisher PDF/XLS checksum describes the original disclosed file, which can differ from these bytes.",
        "active_records":len(state["sources"]),"version_records":len(rows),"distinct_body_files":len({v["stored_body"] for v in rows}),
        "registered_versions":rows})
    # The review command appends an event and changes the live state byte hash. Preserve its exact pre-command bytes.
    (HERE/"state_before_review.json.gz").write_bytes(gzip.compress(state_bytes,mtime=0))
    durable={}
    local_caches={}
    archive_contents={}
    gzip_payloads={}
    for p in sorted(W.rglob("*")):
        if not p.is_file() or p.is_symlink():
            continue
        rel=p.relative_to(W)
        rel_name=str(rel)
        if any(s in rel.parts for s in ["__pycache__","browser_tmp",".pytest_cache"]) or p.name.startswith("."):
            continue
        if rel.parent == HERE.relative_to(W) and p.name in {"reviewed_files.json","receipt.json"}:
            continue
        if "cache" in rel.parts:
            local_caches[rel_name]={"sha256":digest(p),"bytes":p.stat().st_size}
            continue
        durable[rel_name]=digest(p)
        if p.suffix in {".zip",".npz"}:
            index_archive(p,rel_name,archive_contents)
        if p.suffix==".gz":
            gzip_payloads[rel_name]=sha(gzip.decompress(p.read_bytes()))
    assert all(p in durable for group in [*acceptance_map.values(),*stage_map.values()] for p in group)
    assert all(durable[v["stored_body"]]==v["sha256"] for v in rows)
    repo_files={}
    for entry in git("ls-tree","-r","-z",commit).split(b"\0"):
        if not entry:
            continue
        meta,name=entry.split(b"\t",1)
        rel=name.decode()
        if rel.startswith("work/"):
            continue
        mode,kind,blob=meta.split()
        if kind!=b"blob":
            continue
        frozen=git("cat-file","blob",blob.decode())
        actual=(REPO/rel)
        assert actual.is_file() and digest(actual)==sha(frozen), rel
        repo_files[rel]={"sha256":sha(frozen),"git_blob":blob.decode()}
    projection={k:v for k,v in state.items() if k not in ["review","release","history"]}
    manifest={
        "schema":"independent-release-reviewed-files.v1","author":ACTOR,"reviewer":REVIEWER,"run_id":RUN,"cycle":1,
        "economic_as_of":"2026-11-27 America/Los_Angeles","branch":rt["location"]["branch"],"workspace":rt["location"]["workspace_key"],
        "frozen_formal_commit":commit,"observed_git_head_before_cli_reject":head,"formal_sha256":formal,
        "observed_pre_review":{"state_file":"research_state.json","pre_review_state_sha256":sha(state_bytes),
          "exact_copy_gzip":OWN+"state_before_review.json.gz","state_without_review_release_and_event_log_sha256":sha(canonical(projection)),
          "state_projection_keys":sorted(projection),"research_revision":state["revision"],"stages_count":len(stage_map),
          "stage_file_occurrences":sum(map(len,stage_map.values())),"distinct_stage_files":len({p for d in stage_map.values() for p in d}),
          "source_ids":len(state["sources"]),"source_versions":len(rows),"nodes":len(state["nodes"]),"edges":len(state["edges"]),
          "proposals":dict(Counter(p["status"] for p in state["proposals"].values()))},
        "basis":"Workspace evidence is SHA-256 of actual bytes. The workspace list intentionally covers every durable file under this identity, including all stage and acceptance files, acquisition records, every source revision, check scripts, inputs, results and preserved failures. The separately listed repository inputs, implementation, vendor code, tests and workflow documents are bound to the same repository. Inventory membership is not a claim of reading every publication in full.",
        "signed_acceptance_sha256":digest(W/"research/acceptance.json"),"acceptance_direct_files":acceptance_map,
        "stage_files_by_stage":stage_map,"source_blob_inventory":OWN+"source_blob_inventory.json",
        "workspace_files":durable,"repository_files_outside_workspace":repo_files,
        "ignored_local_cache_support_only":local_caches,"archived_member_sha256":archive_contents,"gzip_uncompressed_sha256":gzip_payloads,
        "historical_receipt_bytes":historical_receipts(),
        "exclusion":"This manifest and its enclosing receipt are outside the manifest's own hash set. The CLI reject will mutate research_state.json; the exact pre-command state is included separately. Scratch caches are recorded in a separate optional section for audit provenance, not as required files in a clean clone."}
    write(HERE/"reviewed_files.json",manifest)
    receipt={"schema":"independent-release-decision.v1","author":ACTOR,"reviewer":REVIEWER,"run_id":RUN,"cycle":1,
        "overall_release_verdict":"reject","release":False,"checks":selected,"frozen_formal_commit":commit,
        "pre_review_state_sha256":sha(state_bytes),"formal_sha256":formal,
        "sha256":{str(p.relative_to(W)):digest(p) for p in [W/"research/acceptance.json",HERE/"content_review.json",
                  HERE/"reviewed_files.json",HERE/"final_review.md",W/"research/final_review.md",HERE/"source_blob_inventory.json",
                  HERE/"state_before_review.json.gz",HERE/"review_process_evidence.json",Path(__file__)]},
        "workspace_file_count":len(durable),"repository_dependency_file_count":len(repo_files),
        "stored_source_body_count":len({v["stored_body"] for v in rows}),"archive_member_count":sum(map(len,archive_contents.values())),
        "verdict_scope":"Independent audit completed. Offline UI remains blocked; no release approval or publication.",
        "signature_scheme":"Actual independent reviewer identity and SHA-256 content hashes; no cryptographic identity key or publisher signature is asserted. This file is checked externally by its SHA-256 in the CLI rejection note."}
    write(HERE/"receipt.json",receipt)
    print(json.dumps({"overall":receipt["overall_release_verdict"],"receipt_sha256":digest(HERE/"receipt.json"),
        "reviewed_files_sha256":digest(HERE/"reviewed_files.json"),"workspace_files":len(durable),
        "repository_files":len(repo_files),"source_bodies":receipt["stored_source_body_count"]},ensure_ascii=False))


if __name__=="__main__":
    main()
