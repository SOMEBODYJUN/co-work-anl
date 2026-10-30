"""First source-informed characterization of the finite-palette audit helper.

This is not a rerun of the ten historical fixtures, a blind review, an LP
solver, or a test of the general rounding theorem.  It records the helper's
behavior on the model's exact zero-optimum branch and a positive control.
"""
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import argparse
import json
import platform


def independent_optimum(matrix):
    best = None
    witness = None
    for assignment in product(range(len(matrix)), repeat=len(matrix[0])):
        loads = [F(0) for _ in matrix]
        for j, i in enumerate(assignment):
            if matrix[i][j] is None:
                break
            loads[i] += matrix[i][j]
        else:
            value = max(loads)
            if best is None or value < best:
                best, witness = value, assignment
    return best, witness


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()
    source = Path(args.source).resolve()
    spec = spec_from_file_location("palette_audit_under_characterization", source)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = [
        ("all_finite_edges_zero", [[F(0)]]),
        ("zero_optimum_with_unused_positive_edge", [[F(0)], [F(1)]]),
        ("positive_optimum_control", [[F(1)]]),
    ]
    observations = []
    for name, matrix in cases:
        optimum, witness = independent_optimum(matrix)
        record = {
            "name": name,
            "matrix": [[None if p is None else str(p) for p in row] for row in matrix],
            "independent_optimum": str(optimum),
            "independent_witness": list(witness),
            "every_job_has_zero_edge": all(
                any(row[j] == 0 for row in matrix) for j in range(len(matrix[0]))
            ),
        }
        try:
            record["helper_result"] = module.check_one(name, matrix)
            record["helper_outcome"] = "returned"
        except AssertionError as exc:
            record["helper_outcome"] = "AssertionError"
            record["exception_message"] = str(exc)
        observations.append(record)
    payload = {
        "kind": "new source-informed interface characterization",
        "python": platform.python_version(),
        "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "characterization_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "observations": observations,
        "scope": (
            "The zero-optimum model branch is broader than this internal helper's "
            "all-finite-edges-zero shortcut.  The historical ten positive-optimum "
            "fixtures, generic LP solving and the universal theorem are not rerun here."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
