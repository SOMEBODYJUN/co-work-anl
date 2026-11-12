#!/usr/bin/env python3
"""Freeze only this package and its sibling index, after all exact checks pass."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest=HERE/"freeze_manifest.json"
    sums=HERE/"SHA256SUMS"
    if manifest.exists() or sums.exists():
        raise SystemExit("Already frozen; replay in a fresh copy instead of modifying the freeze.")
    pins=json.loads((HERE/"source_pins.json").read_text())
    for item in pins["sources"]:
        assert digest(ROOT/item["path"])==item["sha256"],item["path"]
    for name in ("generator_output.json","literal_checker_output.json"):
        result=json.loads((HERE/name).read_text())
        assert result["status"]=="PASS" and result["optimizer_calls"]==0
        assert result["source_pins_unchanged"]
    index=HERE.parent/(HERE.name+".md")
    paths=sorted(p for p in HERE.rglob("*") if p.is_file())+[index]
    records=[]
    for path in paths:
        data=path.read_bytes()
        assert data.endswith(b"\n") and not data.endswith(b"\n\n"),(path,"single final newline required")
        assert b"\r" not in data and b"\t" not in data,(path,"CR or TAB")
        assert all(value >= 32 or value == 10 for value in data),(path,"unexpected ASCII control byte")
        assert all(line==line.rstrip(b" \t") for line in data.splitlines()),(path,"trailing whitespace")
        relative="../"+index.name if path==index else path.relative_to(HERE).as_posix()
        records.append({"path":relative,"sha256":digest(path),"bytes":len(data)})
    result={
        "schema":"high_lambda_closure_freeze_v1",
        "status":"FROZEN_EXACT_WHOLE_DOMAIN_CLOSURE",
        "run":"six-boss1-20261111",
        "owner":"/root/high_lambda_closure",
        "write_scope":"high_lambda_closure/ and high_lambda_closure.md only",
        "mathematical_scope":"all five sources, q0=1/6 and 1/5, lambda>=25, all nonnegative tau in the exact anchor domain",
        "outcome":"no new inequality information beyond existing lambda=25 endpoints, actual SAFE for every legal label, customer nonnegativity, and the genuine C equality where used",
        "sources_sha256":digest(HERE/"source_pins.json"),
        "source_files_unchanged":True,
        "independent_checker_status":"PASS",
        "files_have_single_EOF_newline_no_trailing_space_no_tabs":True,
        "new_raw_matrix_materialized":False,
        "files":records,
        "manifest_and_SHA256SUMS_excluded_from_self_hashes":True,
        "stop_writes_after_this_freeze":True,
    }
    manifest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    sumlines=[f"{r['sha256']}  {r['path']}" for r in records]
    sumlines.append(f"{digest(manifest)}  freeze_manifest.json")
    sums.write_text("\n".join(sumlines)+"\n")
    print(json.dumps({"status":result["status"],"artifact_count":len(records),"freeze_manifest_sha256":digest(manifest),"SHA256SUMS_sha256":digest(sums),"total_artifact_bytes":sum(r["bytes"] for r in records)},ensure_ascii=False,indent=2))


if __name__=="__main__":main()
