#!/usr/bin/env python3
"""Freeze the isolated ROOT270 equality stage; no repository writes."""
from pathlib import Path
import hashlib
import json
import os

P=Path(__file__).resolve().parent
REPO=Path(os.environ.get("ROOT270_SOURCE_REPO","/workspace/scratch/b0fef5ec503f/co-work-anl-boss1"))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if (P/"freeze_manifest.json").exists() or (P/"SHA256SUMS").exists():
        raise SystemExit("Frozen package: replay in a fresh copy.")
    for item in json.loads((P/"source_pins.json").read_text())["sources"]:
        assert sha(REPO/item["path"])==item["sha256"],item["path"]
    for name in ["generator_output.json","literal_checker_output.json"]:
        report=json.loads((P/name).read_text())
        assert report["status"].startswith("PASS") and report["optimizer_calls"]==0
        assert report["sources_unchanged"]
    artifacts=[]
    for file in sorted(p for p in P.rglob("*") if p.is_file()):
        data=file.read_bytes()
        assert data.endswith(b"\n") and not data.endswith(b"\n\n"),file
        assert all(ch>=32 or ch==10 for ch in data),(file,"control byte")
        assert all(line==line.rstrip(b" \t") for line in data.splitlines()),file
        artifacts.append({"path":file.relative_to(P).as_posix(),"sha256":sha(file),"bytes":len(data)})
    manifest={
        "schema":"root270_equality_and_true_R4_cap_completion_v1",
        "status":"FROZEN_TRUE_HISTORY_UNIFORM_ROOT_GAIN",
        "run":"six-boss1-20261111","actual_agent_id":"/root/high_lambda_closure",
        "scope":"isolated root270_equality_stage only; frozen high_lambda_closure unchanged",
        "equality_result":"old strict ROOT270 equality iff K=0",
        "new_root_row":"ROOT270_C30_R4_CAP_STRICT.json",
        "uniform_K_gain":"14693170735/3375514772384544",
        "epsilon":"215/3",
        "complete_parameter_breakpoints":["0","43/6","215/12","301/15","215/3"],
        "global_first_C30_breakpoint":"43/6",
        "fixed_root_payment_first_upper_limit":"215/3",
        "independent_literal_status":"PASS",
        "source_pins_unchanged":True,"optimizer_calls":0,
        "global_welfare_combination_performed":False,
        "full_SPE_construction_claimed":False,
        "single_EOF_newline_no_trailing_spaces_no_tabs":True,
        "artifacts":artifacts,
        "freeze_manifest_and_SHA256SUMS_excluded_from_self_hashes":True,
        "stop_writes_after_freeze":True,
    }
    (P/"freeze_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    lines=[f"{a['sha256']}  {a['path']}" for a in artifacts]
    lines.append(f"{sha(P/'freeze_manifest.json')}  freeze_manifest.json")
    (P/"SHA256SUMS").write_text("\n".join(lines)+"\n")
    print(json.dumps({
        "status":manifest["status"],"artifact_count":len(artifacts),
        "total_artifact_bytes":sum(a["bytes"] for a in artifacts),
        "new_row_sha256":sha(P/"ROOT270_C30_R4_CAP_STRICT.json"),
        "freeze_manifest_sha256":sha(P/"freeze_manifest.json"),
        "SHA256SUMS_sha256":sha(P/"SHA256SUMS"),
    },ensure_ascii=False,indent=2))


if __name__=="__main__":main()
