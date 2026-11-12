#!/usr/bin/env python3
"""Freeze this isolated stage only; never write into the source repository."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

P=Path(__file__).resolve().parent


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def hygiene(p):
    text=p.read_text(encoding="utf-8")
    assert text.endswith("\n") and not text.endswith("\n\n"),str(p)
    assert "\r" not in text and "\t" not in text,str(p)
    assert all(line==line.rstrip(" \t") for line in text.splitlines()),str(p)


def main():
    assert not (P/"freeze_manifest.json").exists(),"Already frozen."
    check=json.loads((P/"literal_checker_output.json").read_text())
    interp=json.loads((P/"four_corner_interpolation_checks.json").read_text())
    assert check["status"]==interp["status"]=="PASS"
    assert check["counts"]["independent_full_cells"]==150
    assert interp["local_condition_identities"]==3216
    pins=json.loads((P/"source_pins.json").read_text())
    source=Path(pins["source_repo"])
    assert all(digest(source/r["path"])==r["sha256"] for r in pins["files"])
    files=sorted(p for p in P.rglob("*") if p.is_file() and p.name not in ("freeze_manifest.json","SHA256SUMS"))
    for p in files: hygiene(p)
    records=[dict(path=str(p.relative_to(P)),bytes=p.stat().st_size,sha256=digest(p)) for p in files]
    manifest=dict(schema="cap3-full-delta-isolated-stage-v1",boss="Boss1",run="six-boss1-20261111",
                  agent_id="/root/source2_cap3_tradeoff",status="FROZEN-PASS",
                  frozen_utc=datetime.now(timezone.utc).isoformat(),files=records,
                  conditions=96,tail_planes=1536,cells=150,edges=369,vertices=225,
                  matrices_materialized=False,source_repository_access="read-only",
                  old_frozen_package_modified=False,optimization_calls=0,LP_point_inputs_read=0,
                  source_pins_unchanged=True,text_hygiene="exactly one final newline; no trailing spaces or tabs; no tabs",
                  note="Manifest excludes itself and SHA256SUMS; SHA256SUMS includes manifest but excludes itself.")
    (P/"freeze_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    covered=files+[P/"freeze_manifest.json"]
    (P/"SHA256SUMS").write_text("\n".join(f"{digest(p)}  {p.relative_to(P)}" for p in sorted(covered))+"\n",encoding="utf-8")
    hygiene(P/"freeze_manifest.json")
    hygiene(P/"SHA256SUMS")
    assert all(digest(P/r["path"])==r["sha256"] for r in records)
    print(json.dumps(dict(status="FROZEN-PASS",covered_files=len(covered),
                          manifest_sha256=digest(P/"freeze_manifest.json"),
                          SHA256SUMS_sha256=digest(P/"SHA256SUMS"),
                          proof_sha256=digest(P/"proof.md"),
                          envelopes_sha256=digest(P/"exact_envelopes_2d.json")),ensure_ascii=False,indent=2))


if __name__=="__main__": main()
