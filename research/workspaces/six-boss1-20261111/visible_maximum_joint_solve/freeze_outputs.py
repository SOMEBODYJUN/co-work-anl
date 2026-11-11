#!/usr/bin/env python3
"""Verify frozen dependencies and hash this completed one-call result package."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BASE = HERE.parent
SOURCE = BASE / "visible_maximum_joint"
sha = lambda p: sha256(p.read_bytes()).hexdigest()
dump = lambda p, v: p.write_text(json.dumps(v, indent=2) + "\n")
assert not (HERE / "freeze_manifest.json").exists(), "Completed output is already frozen."
source_pins = json.loads((SOURCE / "source_pins.json").read_text())["sources"]
verified = {}
for relative, digest in source_pins.items():
    target = REPO / relative
    assert sha(target) == digest, (relative, "source changed")
    verified[str(target.relative_to(REPO))] = digest
start_pins = json.loads((HERE / "source_pins_at_solve.json").read_text())
for relative, digest in start_pins.items():
    target = HERE / relative
    assert sha(target) == digest, (relative, "preparation/preflight changed")
    verified[str(target.resolve().relative_to(REPO))] = digest
assert sha(SOURCE / "exact_input.json") == "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33"
cert = json.loads((HERE / "exact_certificate.json").read_text())
disc = json.loads((HERE / "discovery_output.json").read_text())
independent = json.loads((HERE / "independent_check_result.json").read_text())
face = json.loads((HERE / "optimal_face.json").read_text())
branch = json.loads((HERE / "true_branch_equality_diagnostic.json").read_text())
assert cert["optimizer_calls"] == disc["optimizer_calls"] == 1 and disc["success"]
assert independent["status"].startswith("PASS")
assert face["certificate_sha256"] == branch["certificate_sha256"] == sha(HERE / "exact_certificate.json")
assert branch["face_sha256"] == sha(HERE / "optimal_face.json")
dump(HERE / "final_source_verification.json", {
    "status": "PASS_ALL_FROZEN_SOURCES_UNCHANGED", "direct_source_count": len(source_pins),
    "verified_file_count": len(verified), "sha256": verified,
    "optimizer_calls_in_verification": 0
})
excluded = {"freeze_manifest.json", "SHA256SUMS"}
artifacts = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size}
             for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in excluded}
adjacent = BASE / "visible_maximum_joint_solve.md"
artifacts["../visible_maximum_joint_solve.md"] = {"sha256": sha(adjacent), "bytes": adjacent.stat().st_size}
manifest = {
    "status": "FROZEN_EXACT_FULL_RAW_OPTIMUM_AND_FACE_EXCLUSION", "owner": "Boss1", "RUN": "six-boss1-20261111",
    "frozen_utc": datetime.now(timezone.utc).isoformat(),
    "input_sha256": cert["input_sha256"],
    "preparation_manifest_sha256": sha(SOURCE / "freeze_manifest.json"),
    "optimizer_calls": 1, "new_optimizer_calls_after_discovery": 0,
    "raw_inequalities": 1002, "nonnegative_columns": 513, "equalities": 2,
    "all_raw_rows_and_columns_preserved": True, "fixed_K": False, "point_completion": False,
    "objective": cert["objective"], "objective_decimal": cert["objective_decimal"],
    "independent_fraction_check": independent["status"],
    "zero_dual_residual_columns": len(face["zero_residual_columns"]),
    "positive_raw_rows": len(cert["dual"]["positive_raw_indices"]),
    "optimal_face_equation_rank": face["restricted_equation_rank"],
    "whole_optimal_face_true_SPE_excluded": True,
    "face_exclusion_gap": branch["uniform_strict_gap"],
    "half_status": "OPEN", "SPE_existence_claimed": False,
    "direct_source_count_verified_unchanged": len(source_pins),
    "source_pins": verified, "artifacts": artifacts,
    "write_scope": ["research/workspaces/six-boss1-20261111/visible_maximum_joint_solve/",
                    "research/workspaces/six-boss1-20261111/visible_maximum_joint_solve.md"],
    "scope_note": "Exact optimum of the frozen full necessary cone and nonattainment by a genuine complete ordered pure SPE; no quantified larger bound or half theorem claimed."
}
dump(HERE / "freeze_manifest.json", manifest)
entries = [(name, entry["sha256"]) for name, entry in artifacts.items()]
entries.append(("freeze_manifest.json", sha(HERE / "freeze_manifest.json")))
(HERE / "SHA256SUMS").write_text("".join(digest + "  " + name + "\n" for name, digest in sorted(entries)))
print(json.dumps({"status": manifest["status"], "manifest_sha256": sha(HERE / "freeze_manifest.json"),
                  "SHA256SUMS_sha256": sha(HERE / "SHA256SUMS"), "artifacts": len(artifacts),
                  "verified_sources": len(verified), "objective": cert["objective"]}, indent=2))
