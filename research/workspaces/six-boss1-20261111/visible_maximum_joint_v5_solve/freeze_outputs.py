#!/usr/bin/env python3
"""Freeze the actual one-call v5 result, all verification, proofs and real failure record."""
from datetime import datetime, timezone
from fractions import Fraction as F
import ast
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, REPO, OWNER, RUN, AGENT, PROFILE, N, M, Q, PLANNED_ROW_BLOCKS,
                      CERT_STATUS, CHECK_STATUS, FACE_CHECK_STATUS, digest, load_discovery,
                      read_json, require, write_new)


def main():
    require(len(sys.argv) == 1, "No alternate freeze scope")
    bundle, discovery = load_discovery()
    marker = read_json(HERE / "single_lp_consumed.json")
    cert = read_json(HERE / "exact_certificate.json")
    checked = read_json(HERE / "independent_check_result.json")
    face = read_json(HERE / "optimal_face.json")
    face_checked = read_json(HERE / "optimal_face_check_result.json")
    diagnostic = read_json(HERE / "true_branch_equality_diagnostic.json")
    source_checked = read_json(HERE / "true_branch_independent_check.json")
    require(cert["status"] == CERT_STATUS and checked["status"] == CHECK_STATUS
            and checked["certificate_sha256"] == digest(HERE / "exact_certificate.json"), "Exact verification changed")
    require(face_checked["status"] == FACE_CHECK_STATUS
            and face_checked["face_sha256"] == digest(HERE / "optimal_face.json"), "Full face verification changed")
    require(diagnostic["status"] == "PASS_FRESH_TRUE_SOURCE_EXCLUSION_OF_ENTIRE_V5_OPTIMAL_FACE"
            and source_checked["status"] == "PASS_INDEPENDENT_CURRENT_SOURCE_STATES_AND_FULL_FACE_SAFE_CONTRADICTION"
            and source_checked["diagnostic_sha256"] == digest(HERE / "true_branch_equality_diagnostic.json"),
            "Current true-branch verification changed")
    require(marker["optimizer_calls_consumed"] == discovery["optimizer_calls"] == cert["optimizer_calls"] == 1,
            "The single consumption/call/result contract changed")
    require((HERE / "proof.md").is_file() and "half" in (HERE / "proof.md").read_text(), "Actual scoped proof missing")
    scaffold = read_json(HERE / "scaffold_manifest.json")
    static_checks = {}
    for name, expected in scaffold["artifact_sha256"].items():
        actual = digest(HERE / name)
        require(actual == expected, "Released static artifact changed: " + name)
        static_checks[name] = actual
    final_pins = {}
    for relative, expected in bundle["pins"].items():
        path = (REPO / relative).resolve()
        path.relative_to(REPO)
        actual = digest(path)
        require(actual == expected, "A consumed source/input/evidence/code changed: " + relative)
        final_pins[relative] = actual
    optimizer_entries = []
    python_hashes = {}
    for path in sorted(HERE.glob("*.py")):
        tree = ast.parse(path.read_text(), filename=path.name)
        compile(tree, path.name, "exec")
        python_hashes[path.name] = digest(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "linprog":
                optimizer_entries.append({"file": path.name, "line": node.lineno})
    require(len(optimizer_entries) == 1 and optimizer_entries[0]["file"] == "solve_once.py", "Unexpected optimizer entry added")
    obstacle = read_json(HERE / "metadata_read_attempt1_obstacle.json")
    require(obstacle["sole_LP_rerun"] is False and obstacle["failed_attempt_optimizer_calls"] == 0,
            "Actual read-only failure record changed")
    verification = {
        "status": "PASS_FINAL_RELEASED_SOURCES_CORE_CODE_AND_RESULT_BINDINGS",
        "input_sha256": cert["input_sha256"], "main_release_sha256": digest(HERE / "main_release.json"),
        "all_consumed_pins_rechecked": len(final_pins), "consumed_pin_sha256": final_pins,
        "all_static_scaffold_artifacts_unchanged": True, "static_scaffold_artifact_sha256": static_checks,
        "all_python_program_sha256": python_hashes, "only_optimizer_entry": optimizer_entries[0],
        "actual_optimizer_calls": 1, "optimizer_calls_in_freeze": 0,
        "actual_read_only_metadata_failure_preserved": True, "new_lambda_source_files_read": False,
        "source_diags_from_actual_positive_weights": True, "half_status": "OPEN",
    }
    write_new(HERE / "final_source_verification.json", verification)
    files = [path for path in sorted(HERE.iterdir()) if path.is_file()
             and path.name not in {"freeze_manifest.json", "SHA256SUMS"}]
    artifacts = {path.name: {"sha256": digest(path), "bytes": path.stat().st_size} for path in files}
    adjacent = HERE.parent / "visible_maximum_joint_v5_solve.md"
    artifacts["../visible_maximum_joint_v5_solve.md"] = {"sha256": digest(adjacent), "bytes": adjacent.stat().st_size}
    manifest = {
        "schema": "visible_maximum_joint_v5_solve_final_freeze_v1",
        "status": "FROZEN_SINGLE_FULL3056_EXACT_OPTIMUM_AND_TRUE_SPE_FACE_EXCLUSION",
        "owner": OWNER, "RUN": RUN, "agent": AGENT, "profile": PROFILE,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_sha256": cert["input_sha256"],
        "preparation_manifest_sha256": bundle["release"]["preparation_manifest_sha256"],
        "main_release_sha256": digest(HERE / "main_release.json"),
        "consumption_marker_sha256": digest(HERE / "single_lp_consumed.json"),
        "discovery_sha256": digest(HERE / "discovery_output.json"),
        "raw_inequalities": M, "nonnegative_columns": N, "free_equalities": Q,
        "all_affine_rhs_minus_one_rows": 30, "literal_row_blocks": PLANNED_ROW_BLOCKS,
        "optimizer_calls_authorized": 1, "optimizer_calls_consumed": 1, "optimizer_calls_actual": 1,
        "solver": marker["solver"], "solver_options": marker["options"],
        "exact_objective": cert["objective"], "exact_objective_decimal": float(F(cert["objective"])),
        "positive_raw_indices": cert["dual"]["positive_raw_indices"],
        "new_positive_raw_indices": [i for i in cert["dual"]["positive_raw_indices"] if i >= 1586],
        "all_zero_dual_residual_columns": face["zero_residual_columns"],
        "full_face_equation_rank": face["restricted_equation_rank"],
        "unconstrained_affine_parameter_count": face["unconstrained_affine_parameter_count"],
        "all_raw_face_parameter_conditions": len(face["all_raw_inequality_restrictions"]),
        "exact_face_K": cert["K"], "exact_full_face_N5_minus_N4": source_checked["N5_minus_N4"],
        "independent_certificate_status": checked["status"],
        "independent_face_status": face_checked["status"],
        "independent_true_source_status": source_checked["status"],
        "source_pins_sha256": digest(HERE / "source_pins_at_solve.json"),
        "final_source_verification_sha256": digest(HERE / "final_source_verification.json"),
        "actual_read_only_metadata_failure": "metadata_read_attempt1_obstacle.json",
        "all_released_core_code_unchanged": True,
        "artifact_count_excluding_manifest_and_checksums": len(artifacts), "artifacts": artifacts,
        "scope": "Exact optimum of the complete frozen necessary system and a valid original-model lower bound; every positive-OPT normalized complete pure SPE is excluded from attaining this entire optimum face. No uniform positive epsilon, SPE construction, or half proof is claimed; half remains OPEN.",
    }
    write_new(HERE / "freeze_manifest.json", manifest)
    lines = [entry["sha256"] + "  " + filename for filename, entry in sorted(artifacts.items())]
    lines.append(digest(HERE / "freeze_manifest.json") + "  freeze_manifest.json")
    with (HERE / "SHA256SUMS").open("x") as output:
        output.write("\n".join(lines) + "\n")
    print(json.dumps({"status": manifest["status"], "objective": cert["objective"],
                      "freeze_manifest_sha256": digest(HERE / "freeze_manifest.json"),
                      "artifact_count": len(artifacts), "actual_optimizer_calls": 1,
                      "half_status": "OPEN"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
