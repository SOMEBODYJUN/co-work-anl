#!/usr/bin/env python3
"""Freeze only this new package and its explicit sibling summary."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

P=Path(__file__).resolve().parent
REPO=P.parents[3]
SUMMARY=P.parent/(P.name+".md")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def record(p):
    return dict(path=str(p.relative_to(REPO)),bytes=p.stat().st_size,sha256=sha(p))


def hygiene(p):
    raw=p.read_bytes()
    text=raw.decode("utf-8")
    assert text.endswith("\n") and not text.endswith("\n\n"),f"Not exactly one terminal newline: {p}"
    assert "\r" not in text,f"CR newline: {p}"
    assert all(line==line.rstrip(" \t") for line in text.splitlines()),f"Trailing whitespace: {p}"
    assert "\t" not in text,f"Unexpected tab: {p}"


def main():
    assert not (P/"freeze_manifest.json").exists(),"Already frozen; do not modify."
    check=json.loads((P/"literal_checker_output.json").read_text())
    assert check["status"]=="PASS" and check["checked_endpoint_rows"]==186 and check["checked_affine_rows"]==126
    pins=json.loads((P/"source_pins.json").read_text())
    assert all(sha(REPO/r["path"])==r["sha256"] for r in pins["files"])
    files=sorted(p for p in P.rglob("*") if p.is_file() and p.name not in ("freeze_manifest.json","SHA256SUMS"))
    assert SUMMARY.is_file()
    for p in files+[SUMMARY]: hygiene(p)
    manifest=dict(schema="source2-cap3-freeze-v1",run="six-boss1-20261111",agent_id="/root/source2_cap3_tradeoff",
                  frozen_utc=datetime.now(timezone.utc).isoformat(),status="FROZEN-PASS",
                  source_pins_unchanged=True,optimization_calls=0,candidate_point_inputs_read=0,
                  endpoint_rows=186,affine_rows=126,tail_affines=3072,physical_conditions=192,
                  zero_length_weak_intervals=72,text_hygiene="one final newline; no trailing spaces or tabs; no tabs",
                  files=[record(p) for p in files],external_files=[record(SUMMARY)],
                  note="Manifest excludes itself and SHA256SUMS. SHA256SUMS includes manifest and explicit summary, but excludes itself.")
    (P/"freeze_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    covered=files+[SUMMARY,P/"freeze_manifest.json"]
    lines=[f"{sha(p)}  {p.relative_to(REPO)}" for p in sorted(covered)]
    (P/"SHA256SUMS").write_text("\n".join(lines)+"\n",encoding="utf-8")
    hygiene(P/"freeze_manifest.json")
    hygiene(P/"SHA256SUMS")
    assert all(sha(REPO/r["path"])==r["sha256"] for r in manifest["files"]+manifest["external_files"])
    print(json.dumps(dict(status="FROZEN-PASS",covered_files=len(covered),
                          manifest_sha256=sha(P/"freeze_manifest.json"),
                          SHA256SUMS_sha256=sha(P/"SHA256SUMS"),
                          exact_family_sha256=sha(P/"exact_family.json"),
                          affine_family_sha256=sha(P/"affine_family.json"),
                          proof_sha256=sha(P/"proof.md")),ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
