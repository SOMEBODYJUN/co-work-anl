"""Append approved old-Z/old-Z Frechet rows to the exact sorting system.

All inequalities are exact row*x >= 0; all variables are nonnegative.
The entire 12803-column descriptor order is preserved, including the original
4849-column prefix. This is a fixed-16hist necessary relaxation only.
"""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json
import platform
import shutil
import time
import traceback

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
BASE = RUN / "sorting_closure_lp"
REPO = RUN.parents[2]
CUTS = RUN / "common_coupling_math" / "zz-cuts-two-points.json"
GENERATOR = RUN / "common_coupling_math" / "audit_boolean.py"
PACKAGER = RUN / "common_coupling_math" / "package_zz_cuts.py"
START = time.time()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def log(event, **fields):
    record = {"event": event, "utc": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": time.time() - START, **fields}
    line = json.dumps(record, ensure_ascii=False)
    print(line, flush=True)
    with (HERE / "progress.jsonl").open("a") as stream:
        stream.write(line + "\n")


def dot(row, values):
    return sum((v * values[j] for j, v in row.items() if values[j]), F())


def signature(row):
    return tuple((j, str(value)) for j, value in sorted(row.items()) if value)


def parse_row(encoded):
    result = {}
    for j, value in encoded:
        assert isinstance(j, int) and j not in result
        value = F(value)
        if value:
            result[j] = value
    return result


def main():
    log("start", scope="fixed16hist necessary LP, no SPE or universal half claim")
    point_path = BASE / "augmented_lp_exact.json"
    matrix_path = BASE / "exact_matrix.json.gz"
    structure_path = BASE / "epigraph_structure.json"
    input_paths = [point_path, matrix_path, structure_path, CUTS, GENERATOR, PACKAGER, Path(__file__)]
    hashes = {str(path.relative_to(RUN)): sha256(path.read_bytes()).hexdigest() for path in input_paths}
    point_hash = sha256(point_path.read_bytes()).hexdigest()
    assert point_hash == "6bfe2ff663803e80aa30b900f609b300617ee6f62f02f898349e2bb4c95a8f07"
    assert sha256(matrix_path.read_bytes()).hexdigest() == "42d37c6d255152fcccc74645c1d84cf1feafbfa1af67b9f069db53db406b79a7"
    point = json.loads(point_path.read_text())
    with gzip.open(matrix_path, "rt", encoding="utf-8") as stream:
        matrix = json.load(stream)
    cuts = json.loads(CUTS.read_text())
    assert cuts["direction"] == "dot(row,x) >= 0"
    assert cuts["columns"] == 4849
    assert cuts["source_sha256"] == sha256(PACKAGER.read_bytes()).hexdigest()
    audited_points = []
    baseline_audit_index = None
    for ai, record in enumerate(cuts["audits"]):
        audit_path = Path(record["path"])
        audit_point_path = Path(record["input_path"])
        if not audit_point_path.is_absolute():
            audit_point_path = REPO / audit_point_path
        assert sha256(audit_path.read_bytes()).hexdigest() == record["sha256"]
        assert sha256(audit_point_path.read_bytes()).hexdigest() == record["input_sha256"]
        assert record["generator_sha256"] == sha256(GENERATOR.read_bytes()).hexdigest()
        hashes[str(audit_path.relative_to(RUN))] = record["sha256"]
        hashes[str(audit_point_path.relative_to(RUN))] = record["input_sha256"]
        audit_point = json.loads(audit_point_path.read_text())
        audited_points.append([F(col["weight"]) for col in audit_point["columns"][:4849]])
        if record["input_sha256"] == point_hash:
            assert baseline_audit_index is None
            baseline_audit_index = ai
    assert baseline_audit_index is not None
    strip = lambda col: {k: v for k, v in col.items() if k != "weight"}
    columns = [strip(col) for col in point["columns"]]
    assert columns == matrix["columns"]
    base_n, n = 4849, len(columns)
    metadata_hash = sha256(json.dumps(columns[:base_n], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    assert cuts["original_columns_sha256"] == metadata_hash
    rows = [parse_row(row) for row in matrix["rows"]]
    names = list(matrix["row_names"])
    base_m = len(rows)
    assert (base_m, n) == (13853, 12803)
    assert all(0 <= j < n for row in rows for j in row)
    old_values = [F(col["weight"]) for col in point["columns"]]
    assert min(old_values) >= 0
    old_slacks = [dot(row, old_values) for row in rows]
    assert min(old_slacks) >= 0
    obj, norm = list(map(F, matrix["objective"])), list(map(F, matrix["normalization"]))
    assert sum((a*b for a, b in zip(norm, old_values)), F()) == 1
    assert sum((a*b for a, b in zip(obj, old_values)), F()) == F(point["W"])
    structure = json.loads(structure_path.read_text())
    assert structure["original_columns"] == base_n
    thresholds = dict(structure["thresholds"])
    assert len(thresholds) == 7954 and set(thresholds) == set(range(base_n, n))
    for j, i in thresholds.items():
        assert rows[i][j] == 1
        assert set(k for k in rows[i] if k >= base_n) == {j}
        assert old_values[j] == max(F(), -dot({k: v for k, v in rows[i].items() if k < base_n}, old_values))
    records = cuts["cuts"]
    assert isinstance(records, list) and len(records) == cuts["distinct_nonzero_cut_count"] == 78
    assert cuts["record_count"] == 84 and cuts["zero_self_records"] == 6
    seen = {signature(row): i for i, row in enumerate(rows)}
    imported = []
    for record in records:
        row = parse_row(record.get("coefficients", record.get("row")))
        assert all(0 <= j < base_n and columns[j]["kind"] == "joint-reply" for j in row)
        slack = dot(row, old_values)
        assert slack == F(record["values_at_inputs"][baseline_audit_index])
        assert [dot(row, values) for values in audited_points] == list(map(F, record["values_at_inputs"]))
        assert sha256(json.dumps(record["row"], separators=(",", ":")).encode()).hexdigest() == record["sparse_sha256"]
        name = record["name"]
        name_string = name if isinstance(name, str) else json.dumps(name, separators=(",", ":"))
        key = signature(row)
        added = bool(row) and key not in seen
        if added:
            seen[key] = len(rows)
            rows.append(row)
            names.append("ZZ-frechet:" + name_string)
        imported.append({"name": name, "row": seen.get(key), "added": added,
                         "zero_self_row": not row, "baseline_slack": str(slack),
                         "source_records": record["source_records"],
                         "source_sparse_sha256": record["sparse_sha256"],
                         "literal_pair_hist_terms": record.get("literal_pair_hist_terms"),
                         "nonzero_coefficients": len(row)})
    nonzeros = sum(map(len, rows))
    write("inputs.json", {"sha256": hashes, "point_sha256": point_hash,
                          "base_column_metadata_sha256": metadata_hash,
                          "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                          "baseline_rows": base_m, "original_columns": base_n,
                          "auxiliary_columns": n-base_n,
                          "cut_records": len(imported), "new_distinct_cuts": len(rows)-base_m,
                          "source_orbit_records": cuts["record_count"],
                          "source_zero_self_records": cuts["zero_self_records"],
                          "zero_self_records": sum(record["zero_self_row"] for record in imported),
                          "nonzero_duplicate_records": sum(not record["added"] and not record["zero_self_row"] for record in imported),
                          "rows": len(rows), "columns": n, "nonzeros": nonzeros,
                          "scope": "fixed16hist necessary relaxation only"})
    write("cut_records.json", imported)
    shutil.copyfile(structure_path, HERE / "epigraph_structure.json")
    cut_slacks = [F(record["baseline_slack"]) for record in imported]
    write("old_point_audit.json", {"W": point["W"], "input": str(point_path), "sha256": point_hash,
                                  "baseline_verified_rows": base_m, "baseline_minimum_slack": str(min(old_slacks)),
                                  "new_cut_negative_records": sum(v < 0 for v in cut_slacks),
                                  "new_cut_minimum_slack": str(min(cut_slacks)),
                                  "new_cut_slacks": [{"name": record["name"], "slack": record["baseline_slack"]} for record in imported]})
    encoded = {"columns": columns, "row_names": names,
               "rows": [[[j, str(v)] for j, v in sorted(row.items())] for row in rows],
               "objective": list(map(str, obj)), "normalization": list(map(str, norm)),
               "original_rows": 5692, "appended_unique_rows": len(rows)-5692,
               "baseline_rows": base_m, "this_round_added": len(rows)-base_m,
               "original_columns": base_n, "auxiliary_columns": n-base_n}
    payload = json.dumps(encoded, ensure_ascii=False, separators=(",", ":")).encode()
    with (HERE / "exact_matrix.json.gz").open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            stream.write(payload)
    del encoded, payload, matrix, cuts, seen
    ridx, cidx, data = [], [], []
    scales = np.ones(len(rows))
    for i, row in enumerate(rows):
        scales[i] = max([float(abs(v)) for v in row.values()] + [1e-50])
        for j, value in row.items():
            ridx.append(i)
            cidx.append(j)
            data.append(-float(value)/scales[i])
    sparse = coo_matrix((data, (ridx, cidx)), shape=(len(rows), n)).tocsr()
    log("matrix_ready", rows=len(rows), columns=n, nonzeros=nonzeros,
        new_distinct_cuts=len(rows)-base_m, negative_input_cut_records=sum(v < 0 for v in cut_slacks))
    solver_started = time.time()
    sol = linprog([float(v) for v in obj], A_ub=sparse, b_ub=np.zeros(len(rows)),
                  A_eq=coo_matrix(np.asarray([[float(v) for v in norm]])).tocsr(), b_eq=[1],
                  bounds=(0, None), method="highs", options={"primal_feasibility_tolerance": 1e-9,
                                                            "dual_feasibility_tolerance": 1e-9})
    status = {"success": bool(sol.success), "status_code": int(sol.status), "status": sol.message,
              "solver_seconds": time.time()-solver_started, "solver_iterations": sol.nit,
              "W_float": None if sol.fun is None else float(sol.fun), "rows": len(rows), "columns": n,
              "exact_verified": False, "scope": "fixed16hist necessary relaxation only; not SPE or universal half bound"}
    write("status.json", status)
    if not sol.success:
        log("solver_failed", **status)
        return
    canonical = sol.x.copy()
    for j, i in thresholds.items():
        canonical[j] = max(0.0, -sum(float(v)*canonical[k] for k, v in rows[i].items() if k < base_n))
    status.update({"positive_original_columns": int(np.count_nonzero(sol.x[:base_n] > 1e-9)),
                   "positive_solver_columns": int(np.count_nonzero(sol.x > 1e-9)),
                   "positive_canonical_columns": int(np.count_nonzero(canonical > 1e-9)),
                   "minimum_scaled_solver_slack": float(np.min(-sparse @ sol.x)),
                   "minimum_scaled_canonical_slack": float(np.min(-sparse @ canonical)),
                   "maximum_auxiliary_decrease_to_canonical": float(np.max(sol.x[base_n:]-canonical[base_n:]))})
    write("status.json", status)
    write("augmented_lp_float.json", {**status, "O": "1", "W": str(sol.fun),
                                      "completion": "canonical positive-part auxiliaries; floating only",
                                      "columns": [{**col, "weight": str(v)} for col, v in zip(columns, canonical)]})
    np.savez_compressed(HERE / "floating_solver_arrays.npz", primal=sol.x, canonical=canonical,
                        inequality_marginals=sol.ineqlin.marginals,
                        equality_marginals=sol.eqlin.marginals,
                        lower_marginals=sol.lower.marginals, scales=scales)
    log("float_candidate_saved", **status)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        write("assembly_or_float_failure.json", {"traceback": traceback.format_exc()})
        raise
