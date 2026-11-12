#!/usr/bin/env python3
"""Freeze only this new local package and its same-name index."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]


def fingerprint(path):
    data=path.read_bytes()
    return dict(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))


def main():
    checker=json.loads((HERE/"literal_checker_output.json").read_text())
    geometry=json.loads((HERE/"geometry_generator_output.json").read_text())
    generation=json.loads((HERE/"family_generator_output.json").read_text())
    pins=json.loads((HERE/"source_pins.json").read_text())
    assert checker["status"]==geometry["status"]==generation["status"]=="PASS"
    for pin in pins:
        assert fingerprint(ROOT/pin["repository_relative_path"])=={k:pin[k] for k in ("sha256","bytes")}
    for name,sha in checker["verified_input_sha256"].items():
        assert fingerprint(HERE/name)["sha256"]==sha
    assert fingerprint(HERE/"check_literal.py")["sha256"]==checker["verifier_sha256"]
    index=HERE.parent/"later_sources_lambda_cells.md"
    artifacts=[]
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.name not in {"freeze_manifest.json","SHA256SUMS"}:
            artifacts.append(dict(path=p.name,**fingerprint(p)))
    artifacts.append(dict(path="../later_sources_lambda_cells.md",**fingerprint(index)))
    manifest=dict(status="FROZEN",package="later_sources_lambda_cells",research_id="six-boss1-20261111",
                  scope="sources 3,4,5; q0 1/6 and 1/5; all full-middle minimum-terminal anchors over lambda in [0,25]",
                  optimizer_calls=0,global_LP_inputs_points_faces_read=False,current_3056_plan_modified=False,
                  source2_lambda_anchor_complete_read=False,git_RUN_registry_or_old_packages_modified=False,
                  rows=dict(six_general_eight_targets=440,six_C_only=55,ordered_same_six_menu=55,total_raw=550,
                            distinct_exact_vectors=364,old_window_raw=190,all_old_parameter_occurrences=260,
                            old_parameter_column_identities=133380,lambda_below_16_raw_occurrences=290),
                  columns_per_row=513,numerical_positive_divisor="25",all_weak_ties_and_raw_duplicates_retained=True,
                  geometry=geometry,independent_checker_counts=checker["counts"],generator_status="PASS",literal_checker_status="PASS",
                  continuous_analytic_review="PASS",all_nine_source_pins_unchanged=True,sources=pins,artifacts=artifacts,
                  checksum_note="SHA256SUMS covers every listed artifact and this manifest; no circular self hash",
                  post_freeze_rule="stop writing this package and its same-name index")
    (HERE/"freeze_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    lines=[f"{a['sha256']}  {a['path']}" for a in artifacts]
    lines.append(f"{fingerprint(HERE/'freeze_manifest.json')['sha256']}  freeze_manifest.json")
    (HERE/"SHA256SUMS").write_text("\n".join(lines)+"\n")
    for line in lines:
        sha,name=line.split("  ",1)
        assert fingerprint(HERE/name)["sha256"]==sha
    print(json.dumps(dict(status="FROZEN",checksums_verified=len(lines),manifest_sha256=fingerprint(HERE/"freeze_manifest.json")["sha256"],
                          exact_family_sha256=fingerprint(HERE/"exact_family.json")["sha256"],
                          proof_sha256=fingerprint(HERE/"proof.md")["sha256"],
                          checker_sha256=fingerprint(HERE/"literal_checker_output.json")["sha256"],
                          checksum_file_sha256=fingerprint(HERE/"SHA256SUMS")["sha256"]),ensure_ascii=False))


if __name__=="__main__":main()
