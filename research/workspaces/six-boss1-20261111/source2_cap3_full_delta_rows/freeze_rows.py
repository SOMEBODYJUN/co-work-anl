#!/usr/bin/env python3
"""Freeze only this isolated 585-row artifact; source repositories stay read-only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

P=Path(__file__).resolve().parent


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def hygiene(p):
    text=p.read_text(encoding="utf-8")
    assert text.endswith("\n") and not text.endswith("\n\n"),str(p)
    assert "\r" not in text and "\t" not in text,str(p)
    assert all(line==line.rstrip(" \t") for line in text.splitlines()),str(p)


def main():
    assert not (P/"freeze_manifest.json").exists(),"Already frozen."
    check=json.loads((P/"literal_checker_output.json").read_text())
    contain=json.loads((P/"old186_containment.json").read_text())
    summary=json.loads((P/"materialization_summary.json").read_text())
    assert check["status"]==contain["status"]=="PASS"
    assert check["counts"]["full_row_coefficient_checks"]==300105
    assert summary["rows"]==585 and summary["source_vertex_records"]==225 and summary["rows_deleted"]==0
    binding=json.loads((P/"source_binding.json").read_text())
    source=Path(binding["two_dimensional_package"]["path"])
    assert sha(source/"freeze_manifest.json")==binding["two_dimensional_package"]["freeze_manifest_sha256"]
    old_manifest=json.loads((source/"freeze_manifest.json").read_text())
    assert all(sha(source/r["path"])==r["sha256"] for r in old_manifest["files"])
    assert all(sha(Path(r["path"]))==r["sha256"] for r in binding["previous_families"].values())
    files=sorted(p for p in P.rglob("*") if p.is_file() and p.name not in ("freeze_manifest.json","SHA256SUMS"))
    for p in files: hygiene(p)
    entries=[dict(path=str(p.relative_to(P)),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
    manifest=dict(schema="source2-cap3-full-delta-rows-frozen-v1",boss="Boss1",run="six-boss1-20261111",
        agent_id="/root/source2_cap3_tradeoff",status="FROZEN-PASS",frozen_utc=datetime.now(timezone.utc).isoformat(),
        files=entries,rows=585,columns=513,source_vertices=225,coefficient_records=300105,
        source_bundle_manifest_sha256=binding["two_dimensional_package"]["freeze_manifest_sha256"],
        original_scale=True,divisor_applied=False,rows_deleted=0,isolated_weak_records=9,
        old_literal_matches=check["old_literal_matches"],old186_contained=True,
        optimization_calls=0,LP_points_or_faces_read=0,old_packages_modified=False,
        source_pins_unchanged=True,text_hygiene="exactly one final newline, no trailing whitespace or tabs",
        note="Manifest excludes itself and SHA256SUMS; SHA256SUMS includes manifest but not itself.")
    (P/"freeze_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    covered=files+[P/"freeze_manifest.json"]
    (P/"SHA256SUMS").write_text("\n".join(f"{sha(p)}  {p.relative_to(P)}" for p in sorted(covered))+"\n",encoding="utf-8")
    hygiene(P/"freeze_manifest.json")
    hygiene(P/"SHA256SUMS")
    assert all(sha(P/r["path"])==r["sha256"] for r in entries)
    print(json.dumps(dict(status="FROZEN-PASS",covered_files=len(covered),
        manifest_sha256=sha(P/"freeze_manifest.json"),SHA256SUMS_sha256=sha(P/"SHA256SUMS"),
        exact_family_sha256=sha(P/"exact_family.json"),proof_sha256=sha(P/"proof.md"),
        checker_sha256=sha(P/"check_literal.py")),ensure_ascii=False,indent=2))


if __name__=="__main__": main()
