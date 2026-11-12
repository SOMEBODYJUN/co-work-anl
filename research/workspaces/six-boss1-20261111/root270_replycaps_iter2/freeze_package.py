#!/usr/bin/env python3
"""Freeze iteration two and the independent text erratum without old-package writes."""
from pathlib import Path
import hashlib
import json
import os

P=Path(__file__).resolve().parent
REPO=Path(os.environ.get("ROOT270_SOURCE_REPO","/workspace/scratch/b0fef5ec503f/co-work-anl-boss1"))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if (P/"freeze_manifest.json").exists() or (P/"SHA256SUMS").exists():
        raise SystemExit("Frozen; use a fresh replay copy.")
    for item in json.loads((P/"source_pins.json").read_text())["sources"]:
        assert sha(REPO/item["path"])==item["sha256"],item["path"]
    for name in ("generator_output.json","literal_checker_output.json"):
        value=json.loads((P/name).read_text())
        assert value["status"].startswith("PASS") and value["optimizer_calls"]==0
    artifacts=[]
    for file in sorted(p for p in P.rglob("*") if p.is_file()):
        data=file.read_bytes()
        assert data.endswith(b"\n") and not data.endswith(b"\n\n"),file
        assert all(x>=32 or x==10 for x in data),(file,"control byte")
        assert all(line==line.rstrip(b" \t") for line in data.splitlines()),file
        artifacts.append({"path":file.relative_to(P).as_posix(),"sha256":sha(file),"bytes":len(data)})
    result={
        "schema":"root270_replycaps_iter2_existing_budget_reweighting_v1",
        "status":"FROZEN_COMPLETE_EXISTING_BUDGET_PARAMETER_FAMILY",
        "actual_agent_id":"/root/high_lambda_closure","run":"six-boss1-20261111",
        "write_scope":"root270_replycaps_iter2_stage only",
        "old_frozen_packages_unchanged":True,
        "independent_erratum":"root270_reply_cap_erratum.md",
        "new_row":"ROOT270_REPLY_CAP_REWEIGHTED.json",
        "new_K_coefficient":"66400039579513467522586981249/633435930915908109658396979040",
        "K_gain_over_reply_cap":"13706626228836464340271835/190030779274772432897519093712",
        "t_domain":["0","146931707350/112446727090671"],
        "s_domain":["0","146931707350/112593658798021"],
        "no_new_true_budget_added":True,"optimizer_calls":0,
        "independent_checker_status":"PASS","source_pins_unchanged":True,
        "global_welfare_combination_performed":False,
        "extra_uniform_gap_from_endpoint_SAFE_PAIR_obstruction_claimed":False,
        "single_EOF_newline_no_trailing_space_no_tab_or_control_bytes":True,
        "artifacts":artifacts,
        "manifest_and_SHA256SUMS_excluded_from_self_hashes":True,
        "stop_writes_after_freeze":True,
    }
    (P/"freeze_manifest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    sums=[f"{a['sha256']}  {a['path']}" for a in artifacts]
    sums.append(f"{sha(P/'freeze_manifest.json')}  freeze_manifest.json")
    (P/"SHA256SUMS").write_text("\n".join(sums)+"\n")
    print(json.dumps({
        "status":result["status"],"artifact_count":len(artifacts),
        "total_artifact_bytes":sum(a["bytes"] for a in artifacts),
        "new_row_sha256":sha(P/"ROOT270_REPLY_CAP_REWEIGHTED.json"),
        "erratum_sha256":sha(P/"root270_reply_cap_erratum.md"),
        "freeze_manifest_sha256":sha(P/"freeze_manifest.json"),
        "SHA256SUMS_sha256":sha(P/"SHA256SUMS"),
    },ensure_ascii=False,indent=2))


if __name__=="__main__":main()
