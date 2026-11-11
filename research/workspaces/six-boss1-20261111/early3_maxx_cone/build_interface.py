#!/usr/bin/env python3
"""Build 17 new rows by the exact affine update, before any point read."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
OLD_ROWS = WORK / "early_x_anchor_queries/rows_51.json"
COLUMNS = WORK / "early_x_anchor_queries/columns_21021.json.gz"
OLD_FREEZE = WORK / "early_x_anchor_queries/freeze_manifest.json"
MATH_FREEZE = HERE / "math_freeze_manifest.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def save(name, data):
    path = HERE / name
    assert not path.exists(), ("refuse overwrite", str(path))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def add(row, index, value):
    row[index] = row.get(index, F(0)) + value
    if not row[index]:
        del row[index]


math_manifest = json.loads(MATH_FREEZE.read_text())
assert math_manifest["constant"] == "61/3" and math_manifest["point_weight_reads"] == 0
for entry in math_manifest["files"]:
    assert digest(REPO / entry["path"]) == entry["sha256"]
old_manifest = json.loads(OLD_FREEZE.read_text())
for path in (OLD_ROWS, COLUMNS):
    entry = next(item for item in old_manifest["assets"] if item["path"] == str(path.relative_to(REPO)))
    assert digest(path) == entry["sha256"]
old = json.loads(OLD_ROWS.read_text())
columns = json.loads(gzip.decompress(COLUMNS.read_bytes()))
assert len(columns) == old["full_dimension"] == 21021
canonical_columns_sha = sha256(json.dumps(columns, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
assert canonical_columns_sha == old["columns_canonical_sha256"]
hist = {i: column for i, column in enumerate(columns) if column["kind"] == "hist"}
xcols = {column["hist_column"]: i for i, column in enumerate(columns) if column["kind"] == "common-X-mass"}
upper = {i for i, column in enumerate(columns) if column["kind"] == "X-query-overlap-upper"}
assert len(hist) == 16 and set(hist) == set(xcols)
assert len(upper) == 420
assert sorted(xcols.values()) == list(range(20585, 20601))
assert sorted(upper) == list(range(20601, 21021))
safe, hist_records = {}, []
for h, column in sorted(hist.items()):
    bits = tuple(map(int, column["actual_bits"]))
    assert len(bits) == 6
    b = sum(bits[:2])
    income = F(bits[2], sum(bits)) if bits[2] else F(0)
    add(safe, h, income)
    add(safe, xcols[h], -F(1, b + 4))
    hist_records.append({"hist_column": h, "actual_bits": column["actual_bits"], "b": b,
                         "actual_player3_income_coefficient": str(income), "X_column": xcols[h],
                         "kappa_X_coefficient": str(F(1, b + 4))})
assert all(index not in upper for index in safe)
safe_sparse = [[i, str(value)] for i, value in sorted(safe.items())]
save("safe3_from_actual_bits.json", {"formula": "u3 - kappa_X >= 0", "full_dimension": 21021,
     "histogram_count": 16, "histograms": hist_records, "row": safe_sparse})

updated = []
for old_index, record in enumerate(old["rows"]):
    if record["actual_player"] != 3:
        continue
    assert record["C"] == "23" and record["remaining_players"] == 4
    row = {index: F(value) for index, value in record["row"]}
    for index, value in safe.items():
        add(row, index, -F(8, 3) * value)
    assert all(0 <= index < 21021 for index in row)
    assert all(row.get(index, F(0)) < 0 for index in xcols.values())
    assert all(row[index] > 0 for index in upper.intersection(row))
    old_upper = {index: F(value) for index, value in record["row"] if index in upper}
    assert old_upper == {index: value for index, value in row.items() if index in upper}
    updated.append({"name": ["common-X-early-max-P-anchor", 3, *record["name"][2:]],
        "actual_player": 3, "remaining_players": 4, "C": "61/3", "source_history": ["A1", "A2"],
        "X_source": "one fixed argmax of f_P over the common catalogue; P is actual A1..A4 load",
        "orbit_id": record["orbit_id"], "orbit_size": record["orbit_size"],
        "query_members": record["query_members"], "histogram_frequencies": record["histogram_frequencies"],
        "old_row_index": old_index, "old_row_name": record["name"],
        "affine_update": "row61/3 = row23 - (8/3)*SAFE3",
        "row": [[index, str(value)] for index, value in sorted(row.items())], "rhs": "0"})
assert len(updated) == 17
source_hashes = {"old_rows_51": digest(OLD_ROWS), "columns_21021": digest(COLUMNS),
                 "old_rows_freeze": digest(OLD_FREEZE), "math_freeze": digest(MATH_FREEZE)}
packet = {"status": "POINT_FREE_EXACT_61_OVER_3_17_ROW_PACKAGE",
    "source_claim": "early3_maxx_cone: independently paid actual-player3 common-X f_P-max lemma",
    "source_proof": "../early3_maxx_cone.md", "formula": "(61/3)u3-(58/3)kappa_X-avg_Q L_b,4(X,Q)>=0",
    "inequality_convention": "Every sparse row has value >= 0; homogeneous RHS 0.",
    "full_dimension": 21021, "new_columns": 0, "row_count": 17,
    "nonzero_count": sum(len(record["row"]) for record in updated),
    "columns_file": "../early_x_anchor_queries/columns_21021.json.gz",
    "columns_canonical_sha256": canonical_columns_sha, "base_matrix_sha256": old["base_matrix_sha256"],
    "common_X_columns": sorted(xcols.values()), "overlap_upper_columns": sorted(upper),
    "all_overlap_coefficients_unchanged_and_strictly_positive": True,
    "canonical_min_normalization_preserved": True,
    "all_zero_histograms_retained": old["all_zero_histograms_retained"],
    "source_sha256": source_hashes, "point_weights_read": False, "fixed_point_evaluated": False,
    "optimizer_called": False, "old_rows_mutated": False, "matrix_mutated": False, "rows": updated}
save("rows_17.json", packet)
print(json.dumps({"status": packet["status"], "rows": 17, "columns": 21021, "new_columns": 0,
                  "nonzeros": packet["nonzero_count"], "point_weights_read": False,
                  "source_sha256": source_hashes}, indent=2))
