#!/usr/bin/env python3
"""Fingerprint this waiting scaffold only. Never reads the prepared input/source tree."""
from datetime import datetime, timezone
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, OWNER, RUN, AGENT, PROFILE, WAITING, CORE_CODE, PLANNED_DIMENSIONS,
                      PLANNED_ROW_BLOCKS, PLANNED_APPENDED_SCALING, SOLVER_OPTIONS,
                      digest, read_json, require, write_new)


def main():
    require(len(sys.argv) == 1, "No alternate freeze scope is supported")
    require(not (HERE / "main_release.json").exists() and not (HERE / "single_lp_consumed.json").exists(),
            "This is a pre-release scaffold freeze only")
    checked = read_json(HERE / "scaffold_static_check.json")
    require(checked["status"] == "PASS_STATIC_SCAFFOLD_ONLY_NOT_INPUT_OR_SOURCE_VALIDATION", "Actual static check required")
    code_hashes = {name: digest(HERE / name) for name in CORE_CODE}
    require(code_hashes == checked["code_sha256"], "Code changed since the static check")
    repaired = read_json(HERE / "repair_preflight_result.json")
    require(repaired["status"] == "PASS_ZERO_OPTIMIZER_REPAIR_FULL4177_SOURCE_PIN_INTERFACE"
            and repaired["optimizer_calls_authorized"] == repaired["total_optimizer_calls"] == 0
            and repaired["exact_source_pin_file_contents_SHA_checked"] == 44
            and repaired["exact_source_pin_file_byte_counts_checked"] == 44
            and repaired["repair_code_sha256"] == code_hashes,
            "Actual complete zero-optimizer repair check with matching code is mandatory")
    other = ["main_release.template.json", "expected_outputs.json", "source_reference_pins.json",
             "source_review.md", "scaffold_summary_before_release.md", "scaffold_static_check.json",
             "repair_read_plan.json", "repair_preflight_result.json", "core_interface_patch.diff",
             "repair_scope.md", "predecessor_obstacle_pins.json"]
    artifacts = {name: digest(HERE / name) for name in CORE_CODE + other}
    manifest = {
        "status": "HASHED_WAITING_SCAFFOLD_NOT_INPUT_OR_AUTHORIZATION",
        "state": WAITING, "owner": OWNER, "RUN": RUN, "agent": AGENT, "profile": PROFILE,
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        "optimizer_calls": 0, "optimizer_calls_currently_authorized": 0,
        "input_sha256": repaired["input_sha256"], "input_or_active_sources_read_by_freeze": False,
        "authorized_repair_stage_read_actual_input_and_source_closure": True,
        "actual_input_counts_from_zero_optimizer_repair_check": repaired["verified_dimensions"],
        "old_numerical_solver_entry_invoked": False, "old_solution_or_face_bound": False,
        "original_release_withdrawn_by_main": True, "new_main_release_created": False,
        "zero_optimizer_repair_check_sha256": digest(HERE / "repair_preflight_result.json"),
        "planned_dimensions_reference_only": PLANNED_DIMENSIONS,
        "planned_row_blocks_reference_only": PLANNED_ROW_BLOCKS,
        "planned_appended_scaling_reference_only": PLANNED_APPENDED_SCALING,
        "planned_solver_options_reference_only": SOLVER_OPTIONS,
        "source_reference_pins_sha256": digest(HERE / "source_reference_pins.json"),
        "code_artifact_sha256": code_hashes, "artifact_sha256": artifacts,
        "artifact_count_excluding_manifest_and_checksums": len(artifacts),
        "scope": "Solver-v2 static scaffold plus separately authorized complete zero-optimizer repair validation. Original input remains frozen unchanged. This is not an optimizer release, numerical result or mathematical certificate.",
    }
    write_new(HERE / "scaffold_manifest.json", manifest)
    lines = [value + "  " + name for name, value in sorted(artifacts.items())]
    lines.append(digest(HERE / "scaffold_manifest.json") + "  scaffold_manifest.json")
    with (HERE / "SCAFFOLD_SHA256SUMS").open("x") as output:
        output.write("\n".join(lines) + "\n")
    print(json.dumps({"status": manifest["status"], "scaffold_manifest_sha256": digest(HERE / "scaffold_manifest.json"),
                      "static_artifacts": len(artifacts), "optimizer_calls": 0,
                      "input_read_by_freeze": False, "prior_authorized_repair_reads": True}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
