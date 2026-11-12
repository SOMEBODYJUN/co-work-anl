#!/usr/bin/env python3
"""Static scaffold checks now; exact released input preflight only after Main release."""
from collections import defaultdict
from datetime import datetime, timezone
import ast
import json
import sys

sys.dont_write_bytecode = True
from contract import (HERE, N, M, Q, PREFIX_ROWS, APPENDED_ROWS, WAITING, CORE_CODE,
                      PLANNED_DIMENSIONS, PLANNED_ROW_BLOCKS, SOURCE_SCOPE_KEYS,
                      PLANNED_APPENDED_SCALING, SOLVER_OPTIONS,
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
    require(refs["old_solver_imported_or_executed"] is False and refs["old_input_or_point_read"] is False,
            "Only frozen program interfaces may be referenced at this stage")
    require(refs["old_optimal_face_or_certificate_read"] is False
            and refs["prepared_v6_input_or_sources_read"] is False
            and len(refs["sources"]) == len(CORE_CODE), "Static source reference scope changed")
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
        "input_or_active_source_directory_probed": False, "input_or_active_source_read": False,
        "main_release_created": False, "consumption_marker_created": False,
        "independent_checkers_and_gate_import_only_stdlib_or_contract": True,
        "all_forbidden_before_release_files_absent": absent,
        "exact_input_sha256": None, "actual_input_counts": None,
        "scope": "Static program and waiting-template checks only. This does not certify the planned sources, prepared input, exact optimum, or any SPE assertion.",
    }


def released_check():
    bundle = load_released()
    groups = defaultdict(list)
    zero_rows = []
    for i, (row, rhs) in enumerate(zip(bundle["A"], bundle["b"])):
        signature = canonical_digest({"a": {str(j): str(value) for j, value in row.items() if value}, "rhs": str(rhs)})
        groups[signature].append(i)
        if not any(row.values()):
            zero_rows.append(i)
    return {
        "status": "PASS_RELEASED_EXACT_INPUT_GATE_WITH_ZERO_OPTIMIZER_CALLS",
        "input_sha256": bundle["release"]["input_sha256"],
        "main_release_sha256": digest(HERE / "main_release.json"),
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
        "scope": "Exact release/domain/literal/scale preflight; source semantics remain the explicitly released Main audit evidence.",
    }


def main():
    if sys.argv[1:] in (["--static"], ["--static", "--write-report"]):
        report = static_check()
        if "--write-report" in sys.argv:
            write_new(HERE / "scaffold_static_check.json", report)
    elif sys.argv[1:] == ["--released"]:
        report = released_check()
        write_new(HERE / "released_preflight_result.json", report)
    else:
        raise ValueError("Use --static [--write-report] now; --released requires Main's actual final release")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
