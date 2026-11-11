#!/usr/bin/env python3
"""Metadata-only freeze after exact generation and literal checks; no optimizer."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import ast
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(name, value):
    with (HERE / name).open("x") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    assert not (HERE / "freeze_manifest.json").exists()
    assert not (HERE / "SHA256SUMS").exists()
    domain = read(HERE / "domain_result.json")
    build = read(HERE / "family_build_result.json")
    literal = read(HERE / "literal_checker_output.json")
    assert domain["total_vertices"] == 109 and domain["optimizer_calls"] == 0
    assert build["raw_rows"] == 1096 and build["vertices"] == 137
    assert literal["literal_coefficients"] == 562248 and literal["optimizer_calls"] == 0
    assert literal["exact_family_sha256"] == digest(HERE / "exact_family.json")
    pins = read(HERE / "family_source_manifest.json")["sources"]
    source2 = HERE.parent / "source2_minimal_cap_safe"
    source2_manifest = read(source2 / "freeze_manifest.json")
    expected_source2_manifest = "d63c117b0adf2353f70ffaf7d959dd91e8c4ee378838f7e5f4af6e99c86861ec"
    assert digest(source2 / "freeze_manifest.json") == expected_source2_manifest
    added = {}
    for name in ["hidden_state_checks.json", "minimum_tables.json"]:
        path = source2 / name
        relative = str(path.relative_to(REPO))
        expected = source2_manifest["artifacts"][relative]["sha256"]
        assert digest(path) == expected
        pins[relative] = expected
        added[relative] = expected
    for relative, expected in pins.items():
        assert digest(REPO / relative) == expected, relative
    write("source_pin_completion.json", {
        "status": "PASS_ALL12_ACTUAL_DIRECT_SOURCE_FILES_PINNED_UNCHANGED",
        "initial_generation_and_checker_entry_pins": 10,
        "two_comparison_tables_additionally_bound_to_preexisting_source2_manifest": added,
        "source2_manifest_sha256": expected_source2_manifest,
        "all_actual_source_sha256": pins,
        "explanation": "The literal checker additionally reads the frozen source2 hidden-state and minimum tables. Their exact preexisting hashes are verified here against the already pinned source2 manifest; no arithmetic or source output is changed.",
        "optimizer_calls": 0,
    })
    write("scope_record.json", {
        "owner": "visible_maximum_joint_solve", "Boss": "Boss1", "RUN": "six-boss1-20261111",
        "initial_mathematical_scope": [1, 3, 4, 5],
        "initial_domain_vertices": 109,
        "Main_later_explicit_extension": "Reuse frozen source2 28 vertices and generate all eight legal pure targets from the pre-C-equality universal budget.",
        "final_sources": [1, 2, 3, 4, 5], "final_parameter_vertices": 137,
        "targets": ["A1", "A2", "A3", "A4", "A5", "A6", "X", "C"],
        "final_raw_rows": 1096, "all_columns": 513,
        "root_intersection_enumeration_explicitly_approved": 11628,
        "optimizer_calls": 0, "numeric_point_or_global_input_read": False,
        "fixed_support_or_fixed_K": False, "phaseI_or_734_completion": False,
        "source2_domain_rediscovered": False,
        "write_scope": [str(HERE.relative_to(REPO)) + "/", str(HERE.with_suffix(".md").relative_to(REPO))],
        "Git_RUN_registry_credentials_changed": False,
    })
    programs = {}
    for path in sorted(HERE.glob("*.py")):
        tree = ast.parse(path.read_text())
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.append(node.module)
        assert not any(name.split(".")[0] in {"scipy", "numpy", "subprocess", "gurobipy", "pulp", "cvxpy", "highspy"} for name in modules)
        programs[path.name] = {"sha256": digest(path), "imports": sorted(set(modules))}
    review = {
        "status": "PASS_PROOF_AND_SCOPE_REVIEW_AFTER_LITERAL_ARITHMETIC",
        "reviewer": "visible_maximum_joint_solve; not an additional independent human or agent review",
        "proof_sha256": digest(HERE / "proof.md"),
        "source_review_sha256": digest(HERE / "source_review.md"),
        "specific_obligations": {
            "full_labeled_complete_history_model_preserved": True,
            "true_internal_node_payoffs_not_original_actual_payoffs": True,
            "all_t0_analytic_payment_terms_nonnegative": True,
            "root_all_multimissing_states_paid_and_pair_facets_retained": True,
            "root_counterexample_exact_negative_one_over192_preserved": True,
            "source_IC_nonnegative_condition_explicit_and_strict_lower_bounds_proved": True,
            "source3_to5_all_true_D_values_and_H_denominators_retained": True,
            "source2_general_T_rebuilt_before_C_equality": True,
            "negative_free_C_equality_multiplier_preserved": True,
            "all_weak_attaining_states_retained": True,
            "all1096_raw_rows_and_all513_columns_retained": True,
            "no_SPE_realizability_or_new_global_bound_claimed": True,
        },
        "independent_program_result_sha256": digest(HERE / "literal_checker_output.json"),
        "program_import_audit": programs,
        "optimizer_calls": 0, "open_mathematical_obstacle_in_stated_family": None,
    }
    write("proof_review.json", review)
    excluded = {"freeze_manifest.json", "SHA256SUMS"}
    artifacts = [path for path in HERE.iterdir() if path.is_file() and path.name not in excluded]
    artifacts.append(HERE.with_suffix(".md"))
    artifacts = sorted(artifacts)
    assert all(path.exists() for path in artifacts)
    for path in artifacts:
        if path.suffix in {".md", ".py", ".json"}:
            assert all(line == line.rstrip() for line in path.read_text().splitlines()), path
    artifact_map = {str(path.relative_to(REPO)): {"sha256": digest(path), "bytes": path.stat().st_size} for path in artifacts}
    manifest = {
        "status": "FROZEN_POINT_FREE_COMPLETE_FIVE_SOURCE_MINIMAL_CAP_SAFE_FAMILY",
        "owner": "visible_maximum_joint_solve", "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_count": 5, "parameter_vertices": 137, "irredundant_facets": 45,
        "per_source": build["per_source"],
        "raw_rows": 1096, "columns": 513, "literal_coefficients": 562248,
        "raw_scale": "terminal BR mean1 and terminal CAP1; original K weight S preserved",
        "numerical_divisor": "25", "all_eight_legal_pure_targets_retained": True,
        "source2_frozen_domain_reused": True,
        "independent_owned_domain_intersections": literal["owned_domain_intersections_independently_replayed"],
        "full_affine_hidden_states": 456, "vertex_hidden_states": 16656,
        "all_minimum_and_weak_tie_tables": 848, "six_query_membership_patterns": 14592,
        "source2_C_signed_identity_columns": 14364, "negative_C_free_multiplier": "-11/20",
        "root_multimissing_counterexample_residual": "-1/192",
        "optimizer_calls": 0, "numeric_input_or_point_read": False,
        "new_global_optimum_or_SPE_implementation_claimed": False, "six_player_half_status": "OPEN",
        "source_sha256": pins, "source_files_unchanged": len(pins),
        "artifacts": artifact_map,
        "exact_family_sha256": digest(HERE / "exact_family.json"),
        "proof_sha256": digest(HERE / "proof.md"),
        "independent_literal_result_sha256": digest(HERE / "literal_checker_output.json"),
        "outstanding_errors": [],
    }
    write("freeze_manifest.json", manifest)
    sum_paths = artifacts + [HERE / "freeze_manifest.json"]
    with (HERE / "SHA256SUMS").open("x") as out:
        out.write("".join(digest(path)+"  "+str(path.relative_to(REPO))+"\n" for path in sorted(sum_paths)))
    print(json.dumps({
        "status": manifest["status"], "artifacts_excluding_manifest_and_sums": len(artifacts),
        "checksum_entries": len(sum_paths), "source_files": len(pins),
        "manifest_sha256": digest(HERE / "freeze_manifest.json"),
        "SHA256SUMS_sha256": digest(HERE / "SHA256SUMS"),
        "exact_family_sha256": digest(HERE / "exact_family.json"),
        "proof_sha256": digest(HERE / "proof.md"),
        "parameter_families_sha256": digest(HERE / "parameter_families.json"),
        "literal_result_sha256": digest(HERE / "literal_checker_output.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
