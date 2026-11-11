"""Standard-library verification of the saved exact matrix and certificates.

This checks exact arithmetic on the matrix built by the archived constructor;
it is not a second independent derivation of all inherited mathematical rows.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import gzip
import json
import sys
import time

HERE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent


def main():
    started = time.time()
    with gzip.open(HERE / "exact_matrix.json.gz", "rt", encoding="utf-8") as stream:
        matrix = json.load(stream)
    point = json.loads((HERE / "augmented_lp_exact.json").read_text())
    strip = lambda col: {k: v for k, v in col.items() if k != "weight"}
    assert len(point["columns"]) == len(matrix["columns"])
    assert [strip(col) for col in point["columns"]] == matrix["columns"]
    rows = [{j: F(value) for j, value in row} for row in matrix["rows"]]
    assert len(rows) == len(matrix["row_names"]) == point["verified_rows"]
    assert len(rows) == matrix["original_rows"] + matrix["appended_unique_rows"]
    values = [F(col["weight"]) for col in point["columns"]]
    assert min(values) >= 0
    obj, norm = list(map(F, matrix["objective"])), list(map(F, matrix["normalization"]))
    O = sum((a*b for a,b in zip(norm, values)), F())
    W = sum((a*b for a,b in zip(obj, values)), F())
    assert O == F(point["O"]) == 1 and W == F(point["W"])
    assert 1-2*W == F(point["strict_half_gap"])
    slacks = [sum((v * values[j] for j,v in row.items()), F()) for row in rows]
    assert min(slacks) >= 0
    assert str(min(slacks)) == point["minimum_slack"]
    assert point["positive_columns"] == sum(v > 0 for v in values)
    report = {"scope": "exact arithmetic check of saved finite necessary LP; not independent full-row derivation or SPE",
              "rows": len(rows), "columns": len(values), "O": str(O), "W": str(W), "W_float": float(W),
              "below_half": W < F(1,2), "minimum_slack": str(min(slacks)), "exact_primal_verified": True,
              "matrix_sha256": sha256((HERE / "exact_matrix.json.gz").read_bytes()).hexdigest(),
              "point_sha256": sha256((HERE / "augmented_lp_exact.json").read_bytes()).hexdigest()}
    dual_path = HERE / "exact_dual_certificate.json"
    if dual_path.exists():
        dual = json.loads(dual_path.read_text())
        lower = F(dual["normalization_multiplier"])
        residuals = [c-lower*n for c,n in zip(obj, norm)]
        for i, weight in dual["row_multipliers"]:
            weight = F(weight)
            assert weight >= 0 and 0 <= i < len(rows)
            for j, coefficient in rows[i].items():
                residuals[j] -= weight*coefficient
        assert min(residuals) >= 0
        assert residuals == list(map(F, dual["residuals"]))
        assert lower == W
        old_W = F(json.loads((HERE / "old_point_audit.json").read_text())["W"])
        report.update({"exact_dual_verified": True, "minimum_dual_residual": str(min(residuals)),
                       "exact_optimum": str(lower), "strictly_above_old_W": lower > old_W,
                       "exact_optimum_increase": str(lower-old_W),
                       "dual_sha256": sha256(dual_path.read_bytes()).hexdigest()})
    report["seconds"] = time.time()-started
    (HERE / "certificate_verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
