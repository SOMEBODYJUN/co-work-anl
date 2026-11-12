#!/usr/bin/env python3
"""Static checks and separately authorized zero-optimizer schema-repair input checks."""
from collections import defaultdict
from datetime import datetime, timezone
import ast
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, N, M, Q, PREFIX_ROWS, APPENDED_ROWS, WAITING, CORE_CODE,
                      PLANNED_DIMENSIONS, PLANNED_ROW_BLOCKS, SOURCE_SCOPE_KEYS,
                      PLANNED_APPENDED_SCALING, SOLVER_OPTIONS,
                      RELEASE_SCHEMA, SOLVER_PACKAGE, SOURCE_PIN_SCHEMA, SOURCE_PIN_READ_SCOPE,
                      EXPECTED_SOURCE_PIN_ENTRIES, ORIGINAL_RELEASE_REFERENCE_SHA256,
                      validate_source_pin_entries, load_repair_read_only,
                      canonical_digest, digest, load_released, read_json, require, write_new)

FORBIDDEN_BEFORE_RELEASE = [
    "main_release.json", "single_lp_consumed.json", "source_pins_at_solve.json",
    "discovery_output.json", "numerical_summary.json", "exact_certificate.json",
    "all4177_raw_row_checks.json", "all513_column_checks.json", "exact_recovery_summary.json",
    "recovery_obstacle.json", "independent_check_result.json", "optimal_face.json",
    "optimal_face_check_result.json", "positive_payment_diagnostic_queue.json",
    "true_branch_equality_diagnostic.json", "proof.md", "freeze_manifest.json", "SHA256SUMS",
    "released_preflight_result.json",
]


def now():
    return datetime.now(timezone.utc).isoformat()


def static_check():
    """Only own scaffold files; no SOURCE stat/open/glob and no optimizer import."""
    absent = {name: not (HERE / name).exists() for name in FORBIDDEN_BEFORE_RELEASE}
    require(all(absent.values()), "Static preparation must not coexist with release, consumption or numerical results")
    trees, hashes = {}, {}
    for filename in CORE_CODE:
        path = HERE / filename
        source = path.read_text()
        trees[filename] = ast.parse(source, filename=filename)
        compile(trees[filename], filename, "exec")  # Compilation does not execute imports/functions.
        hashes[filename] = digest(path)
    optimizer_calls = []
    optimizer_imports = []
    for filename, tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("scipy.optimize"):
                optimizer_imports.append((filename, node.lineno))
                require(node.module == "scipy.optimize" and [alias.name for alias in node.names] == ["linprog"],
                        "Unexpected optimizer import")
            if isinstance(node, ast.Import):
                require(not any(alias.name.startswith(("scipy.optimize", "subprocess", "importlib")) for alias in node.names),
                        "Unexpected dynamic/optimizer entry")
            if isinstance(node, ast.Call):
                called = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", "")
                require(called not in {"eval", "exec", "__import__", "system", "popen", "minimize", "milp"},
                        "Forbidden alternate execution/optimization path")
                if called == "linprog":
                    optimizer_calls.append((filename, node))
    require(len(optimizer_calls) == 1 and optimizer_calls[0][0] == "solve_once.py", "Exactly one visible optimizer call site is required")
    require(len(optimizer_imports) == 1 and optimizer_imports[0][0] == "solve_once.py", "Optimizer import must occur only in the one-call entry")
    independent_programs = ["verify_certificate.py", "verify_optimal_face.py", "contract.py"]
    safe_imports = {"fractions", "hashlib", "pathlib", "json", "sys", "os", "re", "contract"}
    for filename in independent_programs:
        for node in ast.walk(trees[filename]):
            if isinstance(node, ast.Import):
                require(all(alias.name in safe_imports for alias in node.names),
                        "Independent checker or gate imports a non-stdlib/source-builder/solver module")
            elif isinstance(node, ast.ImportFrom):
                require(node.level == 0 and node.module in safe_imports,
                        "Independent checker or gate imports a source builder, solver or recovery program")
    solver = trees["solve_once.py"]
    option_node = next(node.value for node in solver.body if isinstance(node, ast.Assign)
                       and any(isinstance(target, ast.Name) and target.id == "OPTIONS" for target in node.targets))
    options = ast.literal_eval(option_node)
    require(options == SOLVER_OPTIONS, "Gate and one-call entry must bind identical numerical settings")
    require(options == {"time_limit": 60.0, "presolve": False,
                        "primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9},
            "Single-run numerical settings changed")
    call = optimizer_calls[0][1]
    keywords = {keyword.arg: keyword.value for keyword in call.keywords}
    require(set(keywords) == {"A_ub", "b_ub", "A_eq", "b_eq", "bounds", "method", "options"}, "Unexpected optimizer arguments")
    require(ast.literal_eval(keywords["method"]) == "highs-ds"
            and ast.literal_eval(keywords["bounds"]) == (0, None), "Full-domain solver method or bounds changed")
    for key, name in {"A_ub": "A", "b_ub": "b", "A_eq": "E", "b_eq": "h", "options": "OPTIONS"}.items():
        require(isinstance(keywords[key], ast.Name) and keywords[key].id == name, "Unexpected matrix routing")
    marker_lines = [node.lineno for node in ast.walk(solver) if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name) and node.func.id == "write_new"
                    and any(isinstance(item, ast.Constant) and item.value == "single_lp_consumed.json"
                            for item in ast.walk(node))]
    gate_lines = [node.lineno for node in ast.walk(solver) if isinstance(node, ast.Call)
                  and isinstance(node.func, ast.Name) and node.func.id == "load_released"]
    require(len(marker_lines) == len(gate_lines) == 1
            and gate_lines[0] < optimizer_imports[0][1] < marker_lines[0] < call.lineno,
            "Full release gate/import/exclusive consumption/optimizer ordering changed")
    require(not any(isinstance(node, ast.Name) and node.id in {"load_repair_read_only", "_load_pinned_input"}
                    for node in ast.walk(solver)), "The numerical entry may not use a repair-only input loader")
    contract_tree = trees["contract.py"]
    status_node = next(node for node in contract_tree.body if isinstance(node, ast.FunctionDef) and node.name == "status")
    require(not any(isinstance(node, ast.Name) and node.id in {"SOURCE", "PARENT_SOURCE", "load_released"}
                    for node in ast.walk(status_node)), "Waiting status must not probe a source directory")
    writer_node = next(node for node in contract_tree.body if isinstance(node, ast.FunctionDef) and node.name == "write_new")
    require(any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "open"
                and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == "x"
                for node in ast.walk(writer_node)), "Consumption writer is not exclusive")
    require(any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "fsync"
                for node in ast.walk(writer_node)), "Consumption writer is not durable")
    template = read_json(HERE / "main_release.template.json")
    require(template["schema"] == RELEASE_SCHEMA and template["solver_package"] == SOLVER_PACKAGE,
            "A fresh solver-v2 release template is mandatory")
    require(template["status"] == WAITING and template["authorized_by"] is None
            and template["optimizer_calls_authorized"] == 0
            and template["input_read_authorized"] is False and template["source_closure_read_authorized"] is False
            and template["planning_contract_confirmed"] is False, "Template may not grant authority")
    for key in ["input_sha256", "preparation_manifest_sha256", "scaling_sha256", "row_catalog_sha256", "source_review_sha256",
                "source_pins_sha256", "scaffold_manifest_sha256", "raw_row_order_sha256",
                "required_evidence", "explicit_main_instruction", "expected_dimensions", "expected_row_blocks",
                "expected_appended_scaling", "solver", "solver_options"]:
        require(template[key] is None, "Release field must remain empty during scaffolding: " + key)
    require(all(template["source_validity_scope"].get(key) is False for key in SOURCE_SCOPE_KEYS), "Source review cannot be pre-certified")
    require(template["planned_dimensions_reference_only"] == PLANNED_DIMENSIONS
            and template["planned_row_blocks_reference_only"] == PLANNED_ROW_BLOCKS
            and template["planned_appended_scaling_reference_only"] == PLANNED_APPENDED_SCALING,
            "Planning reference mismatch")
    require(sum(block["count"] for block in PLANNED_ROW_BLOCKS) == M
            and PREFIX_ROWS + APPENDED_ROWS == M, "Planning arithmetic mismatch")
    require(all(block["count"] == block["stop"] - block["start"] for block in PLANNED_ROW_BLOCKS)
            and all(left["stop"] == right["start"] for left, right in zip(PLANNED_ROW_BLOCKS, PLANNED_ROW_BLOCKS[1:])),
            "Planning ranges are not contiguous")
    refs = read_json(HERE / "source_reference_pins.json")
    require(refs["old_numerical_solver_entry_invoked"] is False
            and refs["old_solution_or_certificate_or_face_read"] is False
            and refs["original_authorized_preflight_and_contract_executed"] is True,
            "Actual original preflight/zero-optimizer history must be recorded accurately")
    require(refs["frozen_v6_input_bytes_read_under_original_release"] is True
            and refs["actual_v6_source_pins_read_for_authorized_repair"] is True
            and len(refs["sources"]) == len(CORE_CODE), "Authorized repair reading scope must be explicit")
    parser_cases = source_pin_parser_cases()
    outputs = read_json(HERE / "expected_outputs.json")
    require(outputs["status"] == WAITING and outputs["optimizer_calls_currently_authorized"] == 0
            and outputs["input_sha256"] is None, "Expected outputs are not actual results")
    require("scipy.optimize" not in sys.modules and "scipy" not in sys.modules
            and "sympy" not in sys.modules, "Static check imported numerical or algebraic engines")
    return {
        "status": "PASS_STATIC_SCAFFOLD_ONLY_NOT_INPUT_OR_SOURCE_VALIDATION",
        "state": WAITING, "checked_at_utc": now(), "code_sha256": hashes,
        "planned_dimensions_not_certified": PLANNED_DIMENSIONS,
        "planned_blocks_not_certified": PLANNED_ROW_BLOCKS,
        "planned_appended_scaling_not_certified": PLANNED_APPENDED_SCALING,
        "python_files_parsed_and_compiled_without_execution": len(trees),
        "optimizer_call_sites": 1, "optimizer_calls_during_check": 0,
        "optimizer_imported_during_check": False, "sympy_imported_during_check": False,
        "input_or_active_source_directory_probed_by_static_check": False,
        "input_or_active_source_read_by_static_check": False,
        "authorized_repair_stage_has_prior_input_and_source_pin_reads": True,
        "main_release_created": False, "consumption_marker_created": False,
        "independent_checkers_and_gate_import_only_stdlib_or_contract": True,
        "strict_source_pin_parser_cases": parser_cases,
        "numerical_entry_cannot_use_read_only_repair_loader": True,
        "all_forbidden_before_release_files_absent": absent,
        "exact_input_sha256": None, "actual_input_counts": None,
        "scope": "Static code/template/parser checks only. A separate zero-optimizer repair report validates actual pinned input. Neither report authorizes optimization or asserts an optimum/SPE.",
    }


def source_pin_parser_cases():
    """Pure schema rejection cases: no file reads or numerical engine imports."""
    good = {"schema": SOURCE_PIN_SCHEMA, "read_scope": SOURCE_PIN_READ_SCOPE,
            "files": [{"path": name, **entry} for name, entry in EXPECTED_SOURCE_PIN_ENTRIES.items()]}
    require(validate_source_pin_entries(good) == {name: entry["sha256"] for name, entry in EXPECTED_SOURCE_PIN_ENTRIES.items()},
            "The exact frozen 44-entry interface was not accepted")
    cases = {}
    def rejected(label, change):
        value = json.loads(json.dumps(good))
        change(value)
        try:
            validate_source_pin_entries(value)
        except (ValueError, TypeError):
            cases[label] = "REJECTED"
        else:
            raise ValueError("Strict source-pin parser accepted forbidden case: " + label)
    rejected("unknown_schema", lambda v: v.update(schema="other"))
    rejected("missing_file", lambda v: v["files"].pop())
    rejected("duplicate_file", lambda v: v["files"].__setitem__(1, dict(v["files"][0])))
    rejected("unknown_path", lambda v: v["files"][0].update(path="unknown/source.md"))
    rejected("absolute_path", lambda v: v["files"][0].update(path="/unknown/source.md"))
    rejected("parent_path", lambda v: v["files"][0].update(path="../unknown/source.md"))
    rejected("missing_sha", lambda v: v["files"][0].pop("sha256"))
    rejected("incomplete_sha", lambda v: v["files"][0].update(sha256="abcd"))
    rejected("changed_sha", lambda v: v["files"][0].update(sha256="0" * 64))
    rejected("changed_bytes", lambda v: v["files"][0].update(bytes=v["files"][0]["bytes"] + 1))
    rejected("boolean_bytes", lambda v: v["files"][0].update(bytes=True))
    rejected("unknown_entry_field", lambda v: v["files"][0].update(extra="not allowed"))
    rejected("unknown_document_field", lambda v: v.update(sources={}))
    rejected("changed_file_order", lambda v: v["files"].reverse())
    return {"exact_frozen_interface": "ACCEPTED", "rejection_case_count": len(cases), "cases": cases}


def describe_full_input(bundle, status_value, active_release_sha256):
    groups = defaultdict(list)
    zero_rows = []
    for i, (row, rhs) in enumerate(zip(bundle["A"], bundle["b"])):
        signature = canonical_digest({"a": {str(j): str(value) for j, value in row.items() if value}, "rhs": str(rhs)})
        groups[signature].append(i)
        if not any(row.values()):
            zero_rows.append(i)
    return {
        "status": status_value,
        "input_sha256": bundle["release"]["input_sha256"],
        "active_main_release_sha256": active_release_sha256,
        "verified_dimensions": PLANNED_DIMENSIONS, "verified_row_blocks": PLANNED_ROW_BLOCKS,
        "literal_parent_rows_preserved": PREFIX_ROWS, "original_scaling_strings_preserved": True,
        "verified_appended_scaling_blocks": PLANNED_APPENDED_SCALING,
        "appended_lambda_delta_rows_divisor_25": 1120, "root270_final_row_divisor_1": 1,
        "actual_metadata_catalog_entries": len(bundle["catalog"]),
        "all_affine_rhs_minus_one_indices": [i for i, rhs in enumerate(bundle["b"]) if rhs == -1],
        "all_zero_coefficient_row_indices_retained": zero_rows,
        "all_exact_duplicate_constraint_classes_retained": [indices for indices in groups.values() if len(indices) > 1],
        "all_raw_rows_checked": M, "all_nonnegative_columns_checked": N, "free_equalities_checked": Q,
        "source_files_SHA_checked": len(bundle["pins"]), "optimizer_calls_by_preflight": 0,
        "exact_source_pin_file_contents_SHA_checked": bundle["source_pin_files_checked"],
        "exact_source_pin_file_byte_counts_checked": bundle["source_pin_byte_counts_checked"],
        "mandatory_independent_X_erratum": bundle["mandatory_model_erratum"],
        "scope": "Exact release/domain/literal/scale preflight; source semantics remain the explicitly released Main audit evidence.",
    }


def released_check():
    bundle = load_released()
    return describe_full_input(bundle, "PASS_RELEASED_EXACT_INPUT_GATE_WITH_ZERO_OPTIMIZER_CALLS",
                               digest(HERE / "main_release.json"))


def repair_check():
    bundle = load_repair_read_only()
    require(bundle["repair_read_only"] is True and bundle["optimizer_calls_authorized"] == 0,
            "Repair check must have zero optimizer authority")
    result = describe_full_input(bundle, "PASS_ZERO_OPTIMIZER_REPAIR_FULL4177_SOURCE_PIN_INTERFACE", None)
    result.update(
        optimizer_calls_authorized=0, total_optimizer_calls=0, new_main_release_created=False,
        withdrawn_release_reference_sha256=ORIGINAL_RELEASE_REFERENCE_SHA256,
        withdrawn_release_used_only_for_exact_input_pins=True,
        original_release_reactivated=False, original_consumption_marker_exists=False,
        repair_code_sha256={name: digest(HERE / name) for name in CORE_CODE},
        verified_read_pin_map=bundle["pins"],
        scope="Main-authorized zero-optimizer repair validation of the identical full input, every source-pin file and corrected X scope. This is not a new Main release or numerical result.",
    )
    return result


def main():
    if sys.argv[1:] in (["--static"], ["--static", "--write-report"]):
        report = static_check()
        if "--write-report" in sys.argv:
            write_new(HERE / "scaffold_static_check.json", report)
    elif sys.argv[1:] == ["--released"]:
        report = released_check()
        write_new(HERE / "released_preflight_result.json", report)
    elif sys.argv[1:] in (["--repair-read-only"], ["--repair-read-only", "--write-report"]):
        report = repair_check()
        if "--write-report" in sys.argv:
            write_new(HERE / "repair_preflight_result.json", report)
    else:
        raise ValueError("Use --static [--write-report], --repair-read-only [--write-report], or --released after a new v2 Main release")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
