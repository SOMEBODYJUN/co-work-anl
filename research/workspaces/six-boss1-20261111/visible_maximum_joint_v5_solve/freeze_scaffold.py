#!/usr/bin/env python3
"""Fingerprint this waiting scaffold only. Never reads the prepared input/source tree."""
from datetime import datetime, timezone
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, OWNER, RUN, AGENT, PROFILE, WAITING, CORE_CODE, PLANNED_DIMENSIONS,
                      PLANNED_ROW_BLOCKS, digest, read_json, require, write_new)


def main():
    require(len(sys.argv) == 1, "No alternate freeze scope is supported")
    require(not (HERE / "main_release.json").exists() and not (HERE / "single_lp_consumed.json").exists(),
            "This is a pre-release scaffold freeze only")
    checked = read_json(HERE / "scaffold_static_check.json")
    require(checked["status"] == "PASS_STATIC_SCAFFOLD_ONLY_NOT_INPUT_OR_SOURCE_VALIDATION", "Actual static check required")
    code_hashes = {name: digest(HERE / name) for name in CORE_CODE}
    require(code_hashes == checked["code_sha256"], "Code changed since the static check")
    other = ["main_release.template.json", "expected_outputs.json", "source_reference_pins.json",
             "source_review.md", "scaffold_summary_before_release.md", "scaffold_static_check.json"]
    artifacts = {name: digest(HERE / name) for name in CORE_CODE + other}
    manifest = {
        "status": "HASHED_WAITING_SCAFFOLD_NOT_INPUT_OR_AUTHORIZATION",
        "state": WAITING, "owner": OWNER, "RUN": RUN, "agent": AGENT, "profile": PROFILE,
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        "optimizer_calls": 0, "optimizer_calls_currently_authorized": 0,
        "input_sha256": None, "input_or_active_sources_read": False, "actual_input_counts": None,
        "old_solver_imported_or_executed": False, "old_input_or_point_bound": False,
        "planned_dimensions_reference_only": PLANNED_DIMENSIONS,
        "planned_row_blocks_reference_only": PLANNED_ROW_BLOCKS,
        "code_artifact_sha256": code_hashes, "artifact_sha256": artifacts,
        "artifact_count_excluding_manifest_and_checksums": len(artifacts),
        "scope": "Only static scaffolding is frozen. This is not an input freeze, an optimizer release, a numerical result, or a mathematical certificate.",
    }
    write_new(HERE / "scaffold_manifest.json", manifest)
    lines = [value + "  " + name for name, value in sorted(artifacts.items())]
    lines.append(digest(HERE / "scaffold_manifest.json") + "  scaffold_manifest.json")
    with (HERE / "SCAFFOLD_SHA256SUMS").open("x") as output:
        output.write("\n".join(lines) + "\n")
    print(json.dumps({"status": manifest["status"], "scaffold_manifest_sha256": digest(HERE / "scaffold_manifest.json"),
                      "static_artifacts": len(artifacts), "optimizer_calls": 0, "input_read": False}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
