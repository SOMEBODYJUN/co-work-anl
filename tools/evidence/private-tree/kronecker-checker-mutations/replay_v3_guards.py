#!/usr/bin/env python3
"""New targeted replay of five documented v3 sparse-input guards.

This is not the unavailable historical mutation harness. It runs unchanged
final-v3 code on newly specified independent fixtures. Every expected failure
occurs before seed enumeration or certificate/fourth-power verification.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import platform
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CANON = HERE.parent / "actual-kronecker"
CODE = "tests/audits/unrelated_machines/actual_kronecker_product.py"
INPUT = "examples/unrelated_machines/actual_kronecker_square_input.json"
CERTS = [
    "evidence/certificates/unrelated_machines/actual_kronecker_square_assignment.json",
    "evidence/certificates/unrelated_machines/actual_kronecker_square_independent_assignment.json",
]
EXPECTED_CODE_HASH = "8e95e8c4b00654b2e85efbd37e294837796755ce189e7e933e5200752abebbb3"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.work_dir.exists() or args.output.exists():
        raise SystemExit("Use new work-dir and output paths")
    assert digest(CANON / CODE) == EXPECTED_CODE_HASH
    original_hashes = {p: digest(CANON / p) for p in [CODE, INPUT] + CERTS}
    source_input = json.loads((CANON / INPUT).read_text())
    cases = [
        ("duplicate_same_endpoint_appended", "assert len(row) == 4",
         "Append a copy of row 0 entry 0 as its fifth record."),
        ("duplicate_same_endpoint_replaces_distinct", "assert len(set(ids)) == 4",
         "Replace row 0 entry 1 by a copy of row 0 entry 0."),
        ("row_boolean_id", "assert all(type(i) is int and 0 <= i < 64 for i in ids)",
         "Replace machine ID 0 at row 0 entry 0 by JSON false."),
        ("fifth_entry_in_row", "assert len(row) == 4",
         "Append [2, '1'] to row 0; ID 2 differs from its four original IDs."),
        ("extra_101st_finite_row", "assert len(inp['finite_edges']) == 100",
         "Append a copy of finite row 0 as row 100."),
    ]
    args.work_dir.mkdir(parents=True)
    results = []
    for name, expected_assertion, operation in cases:
        fixture = args.work_dir / name
        for rel in [CODE, INPUT] + CERTS:
            dest = fixture / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(CANON / rel, dest)
        data = copy.deepcopy(source_input)
        rows = data["finite_edges"]
        if name == "duplicate_same_endpoint_appended":
            rows[0].append(copy.deepcopy(rows[0][0]))
        elif name == "duplicate_same_endpoint_replaces_distinct":
            rows[0][1] = copy.deepcopy(rows[0][0])
        elif name == "row_boolean_id":
            assert rows[0][0][0] == 0
            rows[0][0][0] = False
        elif name == "fifth_entry_in_row":
            assert 2 not in [i for i, _ in rows[0]]
            rows[0].append([2, "1"])
        else:
            rows.append(copy.deepcopy(rows[0]))
        (fixture / INPUT).write_text(json.dumps(data, indent=2) + "\n")
        success_output = fixture / "should_not_exist.json"
        proc = subprocess.run(
            [sys.executable, str((fixture / CODE).resolve()),
             "--output", str(success_output.resolve())],
            capture_output=True, text=True, timeout=15,
        )
        assert proc.returncode == 1, (name, proc.returncode)
        assert proc.stdout == "", (name, proc.stdout)
        assert not success_output.exists(), name
        assert expected_assertion in proc.stderr, (name, proc.stderr)
        assert proc.stderr.rstrip().endswith("AssertionError"), name
        results.append({
            "case": name,
            "exact_new_mutation": operation,
            "returncode": proc.returncode,
            "rejected_at_expected_guard": True,
            "expected_assertion": expected_assertion,
            "stdout": proc.stdout,
            "no_success_output_created": True,
            "mutated_input_sha256": digest(fixture / INPUT),
            "finite_row_count": len(rows),
            "first_finite_row": rows[0],
            "guard_precedes_seed_enumeration_in_original_code": True,
        })
    assert original_hashes == {p: digest(CANON / p) for p in original_hashes}
    report = {
        "status": "five_targeted_v3_guards_replayed",
        "python": platform.python_version(),
        "driver_sha256": digest(Path(__file__)),
        "canonical_code_sha256": EXPECTED_CODE_HASH,
        "canonical_resource_hashes": original_hashes,
        "canonical_resources_unchanged": True,
        "cases": results,
        "limits": [
            "New explicitly specified fixtures, not byte-for-byte replay of missing historical harness.",
            "No v2 mutations or v1 acceptance experiment executed.",
            "All failures precede seed enumeration, certificate checks, and fourth-power construction.",
            "No repeated correct-input full Kronecker audit and no exhaustive invalid-input testing.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
        out.write("\n")
    print(json.dumps({"status": report["status"], "cases": len(results),
                      "canonical_resources_unchanged": True}))


if __name__ == "__main__":
    main()
