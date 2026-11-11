"""Main's separate exact arithmetic audit of an archived finite LP.

Only matrix arithmetic is independently checked here; the semantics of
inherited rows are not re-derived by this program.
"""
import argparse
from fractions import Fraction as F
import gzip
from hashlib import sha256
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("directory", type=Path)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
root = args.directory
matrix_path = root / "exact_matrix.json.gz"
point_path = root / "augmented_lp_exact.json"
dual_path = root / "exact_dual_certificate.json"
with gzip.open(matrix_path, "rt", encoding="utf-8") as stream:
    mat = json.load(stream)
point = json.loads(point_path.read_text())
dual = json.loads(dual_path.read_text())
assert [{k: v for k, v in col.items() if k != "weight"}
        for col in point["columns"]] == mat["columns"]
x = [F(col["weight"]) for col in point["columns"]]
assert min(x) >= 0
objective = list(map(F, mat["objective"]))
normalization = list(map(F, mat["normalization"]))
assert len(x) == len(objective) == len(normalization)
dot = lambda a, b: sum((v * w for v, w in zip(a, b)), F())
W = dot(objective, x)
assert dot(normalization, x) == F(point["O"]) == 1
assert W == F(point["W"]) == F(dual["normalization_multiplier"])
rows = [{int(j): F(v) for j, v in raw} for raw in mat["rows"]]
primal_slacks = [sum((v * x[j] for j, v in row.items()), F()) for row in rows]
assert min(primal_slacks) >= 0
dual_residual = [w - W * o for w, o in zip(objective, normalization)]
for i, weight in dual["row_multipliers"]:
    weight = F(weight)
    assert weight >= 0 and 0 <= i < len(rows)
    for j, v in rows[i].items():
        dual_residual[j] -= weight * v
assert min(dual_residual) >= 0
assert dual_residual == list(map(F, dual["residuals"]))
record = {
    "scope": "Main exact arithmetic audit of saved matrix; not an SPE or a full-row semantic derivation",
    "rows": len(rows), "columns": len(x),
    "original_positive_columns": sum(t > 0 for t in x[:4849]),
    "all_positive_columns": sum(t > 0 for t in x),
    "O": "1", "W": str(W), "W_float": float(W),
    "strict_half_gap": str(1 - 2 * W),
    "minimum_primal_slack": str(min(primal_slacks)),
    "minimum_dual_residual": str(min(dual_residual)),
    "nonnegative_primal_and_dual": True,
    "matched_exact_optimum": True,
    "inputs": [{"path": str(p), "sha256": sha256(p.read_bytes()).hexdigest()}
               for p in (matrix_path, point_path, dual_path)],
}
args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(record, ensure_ascii=False))
