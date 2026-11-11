"""Freeze the next exact ZZ separation at this round's certified point."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent


def signature(row):
    return tuple((j, str(F(value))) for j, value in sorted(row) if F(value))


def main():
    point_path = HERE / "augmented_lp_exact.json"
    audit_path = HERE / "zz-at-certified-point.json"
    matrix_path = HERE / "exact_matrix.json.gz"
    audit = json.loads(audit_path.read_text())
    assert audit["input_sha256"] == sha256(point_path.read_bytes()).hexdigest()
    assert audit["matrix_sha256"] == sha256(matrix_path.read_bytes()).hexdigest()
    point = json.loads(point_path.read_text())
    values = [F(col["weight"]) for col in point["columns"]]
    with gzip.open(matrix_path, "rt") as stream:
        matrix = json.load(stream)
    seen = {signature(row): i for i, row in enumerate(matrix["rows"])}
    records = []
    new = []
    for candidate in audit["known_ZZ_frechet_bounds_at_this_point"]:
        row = candidate["row"]
        slack = sum((F(value)*values[j] for j, value in row), F())
        assert slack == F(candidate["value"]) == F(candidate["direct_frechet_value"])
        key = signature(row)
        record = {"name": candidate["name"], "slack": str(slack),
                  "row": row, "zero_self": not row, "already_in_matrix": key in seen,
                  "existing_row": seen.get(key), "literal_pair_hist_terms": candidate["literal_pair_hist_terms"]}
        records.append(record)
        if row and key not in seen:
            seen[key] = len(matrix["rows"])+len(new)
            new.append(record)
    package = {"scope": "next valid ZZ necessary cuts; this package is not yet optimized or included in the certified matrix",
               "direction": "dot(row,x) >= 0", "input_sha256": audit["input_sha256"],
               "source_audit_sha256": sha256(audit_path.read_bytes()).hexdigest(),
               "matrix_sha256": audit["matrix_sha256"], "W": point["W"],
               "columns": len(values), "original_columns": 4849,
               "original_columns_sha256": audit["original_columns_sha256"],
               "records": records, "selected_rows": new, "new_distinct_rows": len(new),
               "negative_rows": sum(F(record["slack"]) < 0 for record in records),
               "zero_self_rows": sum(record["zero_self"] for record in records)}
    path = HERE / "next_zz_cuts.json"
    path.write_text(json.dumps(package, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({k: v for k, v in package.items() if k not in ("records", "selected_rows")}, indent=2))


if __name__ == "__main__":
    main()
