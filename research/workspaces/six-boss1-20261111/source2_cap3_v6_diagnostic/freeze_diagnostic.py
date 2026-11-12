#!/usr/bin/env python3
"""Freeze this completed, independently checked diagnostic exactly once."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import shutil

P=Path(__file__).resolve().parent
assert not (P/"freeze_manifest.json").exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda n:json.loads((P/n).read_text())
summary=read("diagnostic_summary.json")
independent=read("independent_diagnostic_check.json")
assert summary["status"]=="PASS_COMPLETED_NEW_V6_TRUE_DIAGNOSTIC"
assert independent["status"]=="PASS_INDEPENDENT_DIAGNOSTIC_CHECK"
assert read("positive_true_payment_support.json")["count"]==3
binding=read("input_binding.json")
for ref in binding["inputs"].values(): assert sha(Path(ref["path"]))==ref["sha256"]
assert sha(Path(binding["source"]["path"])/"freeze_manifest.json")==binding["source"]["manifest_sha256"]
cache=P/"__pycache__"
if cache.exists(): shutil.rmtree(cache)
failures=read("failure_log.json") if (P/"failure_log.json").exists() else []
if not (P/"failure_log.json").exists(): (P/"failure_log.json").write_text("[]\n")
resolution=dict(failures_retained=len(failures),current_independent_status=independent["status"],
    resolution="The sole launch-time UnboundLocalError came from a local variable named load shadowing the JSON reader; renamed to actual_load and reran successfully.",
    mathematical_failures_removed=0,old_packages_modified=False)
(P/"failure_resolution.json").write_text(json.dumps(resolution,ensure_ascii=False,indent=2)+"\n")
files=[]
for path in sorted(P.iterdir()):
    assert path.is_file(),f"Unexpected non-file in isolated freeze: {path.name}"
    if path.name in ("freeze_manifest.json","SHA256SUMS"): continue
    raw=path.read_bytes()
    text=raw.decode("utf-8")
    assert text.endswith("\n") and not text.endswith("\n\n"),f"EOF newline: {path.name}"
    assert "\t" not in text,f"Tab: {path.name}"
    assert all(line==line.rstrip(" \t") for line in text.splitlines()),f"Trailing whitespace: {path.name}"
    files.append(dict(path=path.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
manifest=dict(schema="cap3-new-v6-true-diagnostic-frozen-v1",status="FROZEN-PASS",frozen_utc=datetime.now(timezone.utc).isoformat(),
    boss="Boss1",run="six-boss1-20261111",agent_id="/root/source2_cap3_tradeoff",solve="full4177_v6",
    files=files,input_binding=binding["inputs"],source_manifest_sha256=binding["source"]["manifest_sha256"],
    rows=585,raw_columns=513,source_vertices=225,point_positive=580,point_zero=5,point_negative=0,
    exact_zero_face_parameter_coefficients=5265,complete_face_raw_inequalities=4177,complete_face_nonnegative_conditions=513,
    affine_parameter_count=9,relative_feasible_dimension="not asserted",negative_row_face_exclusion=False,
    conditional_zero_payment_SPE_face_exclusion=True,unconditional_new_row_constructed=False,
    optimizer_calls=0,old_v5_read=False,old_packages_modified=False,failures_retained=len(failures),
    text_hygiene="UTF-8; exactly one final newline; no tabs or trailing spaces",note="Original bytes frozen; future universal SAFE4 construction must use another isolated directory.")
(P/"freeze_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
checks=files+[dict(path="freeze_manifest.json",sha256=sha(P/"freeze_manifest.json"))]
(P/"SHA256SUMS").write_text("".join(r["sha256"]+"  "+r["path"]+"\n" for r in checks))
print(json.dumps(dict(status="FROZEN-PASS",files=len(files),manifest_sha256=sha(P/"freeze_manifest.json"),SHA256SUMS_sha256=sha(P/"SHA256SUMS"),proof_sha256=sha(P/"proof.md"),independent_checker_sha256=sha(P/"check_diagnostic.py")),ensure_ascii=False))
