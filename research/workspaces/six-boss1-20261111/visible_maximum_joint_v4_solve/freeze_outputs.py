#!/usr/bin/env python3
"""Freeze the actual single-call result and all exact output/source fingerprints."""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import ast
import json
import os
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE = HERE.parent / "visible_maximum_joint_v4"
ADJACENT = HERE.with_suffix(".md")
MANIFEST = HERE / "freeze_manifest.json"
SUMS = HERE / "SHA256SUMS"
INPUT_SHA = "fbd3b0cb65736b5c41b64dd630b442e9647b701e446c36819e3f726c620ac839"
RELEASE_SHA = "3c70842209dc14c79d040126a536f09cd89b9675399df81fe3c28c8bf577263e"
PREPARATION_SHA = "21da98ff5b72702363824200e25320fc7d510633be48d91de6e2eea5e708c337"
digest = lambda path: sha256(path.read_bytes()).hexdigest()
read = lambda name: json.loads((HERE / name).read_text())

assert not MANIFEST.exists() and not SUMS.exists(), "Already frozen; no overwrite."
assert digest(SOURCE / "exact_input.json") == INPUT_SHA
assert digest(SOURCE / "freeze_manifest.json") == PREPARATION_SHA
assert digest(HERE / "main_release.json") == RELEASE_SHA
cert = read("exact_certificate.json")
disc = read("discovery_output.json")
marker = read("single_lp_consumed.json")
verified = read("independent_check_result.json")
face = read("optimal_face.json")
diagnostic = read("true_branch_equality_diagnostic.json")
fixed = read("true_branch_face_functionals.json")
snapshot = read("scaffold_snapshot_recheck.json")
assert cert["status"] == "PASS_EXACT_PRIMAL_DUAL_FULL1586"
assert verified["status"] == "PASS_FULL1586_RAW_FRACTION_VERIFICATION"
assert face["status"] == "EXACT_FULL_COMPLEMENTARITY_OPTIMAL_FACE"
assert diagnostic["status"] == "WHOLE1586_OPTIMAL_FACE_EXCLUDED_BY_TRUE_C_INTERMEDIATE_SAFE"
assert all(item["input_sha256"] == INPUT_SHA for item in [cert, disc, marker, verified, face, diagnostic])
assert cert["optimizer_calls"] == disc["optimizer_calls"] == marker["optimizer_calls_consumed"] == 1
assert disc["success"] and disc["status"] == 0 and disc["iterations"] == 65
assert marker["options"]["time_limit"] == 60.0 and marker["options"]["presolve"] is False
assert (marker["raw_inequalities"], marker["nonnegative_columns"], marker["equalities"]) == (1586, 513, 2)
assert marker["solver_script_sha256"] == digest(HERE / "solve_once.py")
assert marker["contract_script_sha256"] == digest(HERE / "contract.py")
assert marker["release_sha256"] == RELEASE_SHA
assert marker["source_pins_sha256"] == digest(HERE / "source_pins_at_solve.json")
assert cert["discovery_sha256"] == digest(HERE / "discovery_output.json")
assert verified["certificate_sha256"] == face["certificate_sha256"] == diagnostic["certificate_sha256"] == digest(HERE / "exact_certificate.json")
assert diagnostic["face_sha256"] == fixed["face_sha256"] == digest(HERE / "optimal_face.json")
assert diagnostic["fixed_functionals_sha256"] == digest(HERE / "true_branch_face_functionals.json")
assert len(cert["primal"]) == len(cert["dual"]["nonnegative_column_residual"]) == 513
assert len(cert["dual"]["raw_row_weights"]) == len(cert["raw_row_slacks"]) == 1586
assert len(cert["dual"]["equality_multipliers"]) == len(cert["equality_residuals"]) == 2
assert len(face["zero_residual_columns"]) == 20 and face["restricted_equation_rank"] == 13
assert len(face["all1586_raw_inequality_restrictions"]) == 1586
assert len(diagnostic["all256_endpoint_states"]) == 256
assert diagnostic["all_common_zero_states_count"] == 13 and diagnostic["literal_menu_checks"] == 8192
assert all(F(value) < 0 for value in diagnostic["whole_face_contradiction_gaps"].values())
assert diagnostic["unfrozen_ordered_menu_rows_used"] is False
assert diagnostic["fixed_C_734_bound"] is False and diagnostic["phaseI_calls"] == 0
assert not (HERE / "recovery_obstacle.json").exists()

sources = {}
source_maps = [
    read("source_pins_at_solve.json"),
    read("diagnostic_source_pins.json"),
    read("source_reference_pins.json")["sources"],
]
for source_map in source_maps:
    for relative, expected in source_map.items():
        assert relative not in sources or sources[relative] == expected, relative
        assert digest(REPO / relative) == expected, relative
        sources[relative] = expected
assert snapshot["status"] == "PASS_ORIGINAL_WAITING_SCAFFOLD_SNAPSHOT"
for relative, record in snapshot["original_snapshot_checks"].items():
    assert digest(REPO / record["actual_snapshot_location"]) == record["sha256"], relative
assert snapshot["original_scaffold_manifest_sha256"] == digest(HERE / "scaffold_manifest.json")

# A preparatory summary is preserved as an exact byte snapshot; its historical
# relative links retain the original adjacent summary's base directory.
link_counts = {"current_artifact_links": 0, "historical_summary_links_in_original_context": 0}
pre_files = [path for path in HERE.iterdir() if path.is_file()] + [ADJACENT]
assert all(path.is_file() for path in HERE.iterdir()), "Unexpected subdirectory."
for path in pre_files:
    text = path.read_text()
    assert text.endswith("\n") and not any(line.endswith((" ", "\t")) for line in text.splitlines()), path
    if path.suffix == ".json":
        json.loads(text)
    if path.suffix == ".py":
        ast.parse(text)
    if path.suffix == ".md":
        historical = path.name == "scaffold_summary_before_release.md"
        link_base = ADJACENT.parent if historical else path.parent
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            assert not link.startswith(("http:", "https:", "file:")), link
            assert (link_base / link).is_file(), (path.name, link)
            key = "historical_summary_links_in_original_context" if historical else "current_artifact_links"
            link_counts[key] += 1
with (HERE / "final_source_verification.json").open("x") as output:
    output.write(json.dumps({
        "status": "PASS_ALL_ACTUAL_INPUT_DIAGNOSTIC_AND_REFERENCE_SOURCE_BYTES",
        "input_sha256": INPUT_SHA, "release_sha256": RELEASE_SHA,
        "preparation_manifest_sha256": PREPARATION_SHA,
        "actual_solve_source_pins": len(source_maps[0]),
        "merged_source_count": len(sources), "source_sha256": sources,
        "original_scaffold_snapshot_checks": len(snapshot["original_snapshot_checks"]),
        "link_checks": link_counts,
        "all_core_solver_code_unchanged_since_preparation_and_entry": True,
        "new_optimizer_calls": 0,
    }, ensure_ascii=False, indent=2) + "\n")
files = sorted(path for path in HERE.iterdir() if path.is_file()) + [ADJACENT]
artifacts = {
    os.path.relpath(path, HERE): {"sha256": digest(path), "bytes": path.stat().st_size}
    for path in files
}
manifest = {
    "status": "FROZEN_EXACT_FULL1586_OPTIMUM_AND_WHOLE_FACE_TRUE_SPE_EXCLUSION",
    "owner": "Boss1", "RUN": "six-boss1-20261111",
    "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
    "input_sha256": INPUT_SHA, "preparation_manifest_sha256": PREPARATION_SHA,
    "main_release_sha256": RELEASE_SHA,
    "optimizer_calls": 1, "new_optimizer_calls_in_exact_followup": 0,
    "numerical_options": marker["options"], "numerical_iterations": disc["iterations"],
    "raw_inequalities": 1586, "nonnegative_columns": 513, "equalities": 2,
    "objective": cert["objective"], "objective_decimal": cert["objective_decimal"],
    "raw_positive_payment_count": len(cert["dual"]["positive_raw_indices"]),
    "raw_positive_payment_indices": cert["dual"]["positive_raw_indices"],
    "full_zero_residual_column_count": len(face["zero_residual_columns"]),
    "full_face_restricted_equation_rank": face["restricted_equation_rank"],
    "free_affine_columns": [entry["column"] for entry in face["parameters"]],
    "source_budget_endpoint_states": 256, "all_common_weak_zero_states": 13,
    "literal_same_menu_difference_checks": 8192,
    "whole_face_contradiction_gaps": diagnostic["whole_face_contradiction_gaps"],
    "whole_face_exclusion": diagnostic["status"],
    "fixed_K": False, "model_support_restricted": False,
    "old_LP_rerun": False, "upstream1050_solved": False,
    "fixed_C_734_bound": False, "phaseI_calls": 0,
    "unfrozen_ordered_menu_rows_used": False, "new_input_rows_added": False,
    "source_count": len(sources), "source_sha256": sources,
    "artifact_count_excluding_manifest_and_checksums": len(artifacts),
    "artifacts": artifacts,
    "initial_scaffold_is_historical": {
        "manifest_sha256": digest(HERE / "scaffold_manifest.json"),
        "old_adjacent_summary_preserved_at": "scaffold_summary_before_release.md",
        "snapshot_verification": "scaffold_snapshot_recheck.json",
        "all_core_code_unchanged": True,
    },
    "scope": (
        "Exact optimum of the full frozen necessary cone and a universal bound. "
        "All normalized positive-OPT complete pure SPEs are excluded from attaining "
        "this optimum face. This does not supply a uniform larger epsilon or prove "
        "the original six-player half statement; it remains OPEN."
    ),
}
with MANIFEST.open("x") as output:
    output.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
with SUMS.open("x") as output:
    for path in sorted([*files, MANIFEST]):
        output.write(digest(path) + "  " + os.path.relpath(path, HERE) + "\n")
for relative, expected in sources.items():
    assert digest(REPO / relative) == expected, relative
for relative, entry in artifacts.items():
    assert digest((HERE / relative).resolve()) == entry["sha256"], relative
print(json.dumps({
    "status": manifest["status"],
    "freeze_manifest_sha256": digest(MANIFEST), "SHA256SUMS_sha256": digest(SUMS),
    "artifact_count_excluding_manifest_and_checksums": len(artifacts),
    "checksum_entries": len(artifacts) + 1,
    "all_source_files_unchanged": len(sources),
    "optimizer_calls_total": 1, "new_optimizer_calls_in_freeze": 0,
}, indent=2))
