"""Sparse assembly and HiGHS solve of the fixed-16hist sorting extension.

All rows have the form row*x >= 0 and all variables are nonnegative.
The original 4849-column prefix is preserved.  This is a necessary LP only.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json
import platform
import sys
import time
import traceback

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
BASE = RUN / "augmented_lp" / "round2"
EPIGRAPH = RUN / "tail_constraints" / "single-query-epigraph.json"
CUTS = RUN / "cross_branch_math" / "round3_candidate_cuts.json"
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
    log("start", scope="finite fixed16hist necessary relaxation; not SPE or universal welfare bound")
    point_path = BASE / "augmented_lp_exact.json"
    matrix_path = BASE / "exact_matrix.json.gz"
    inputs = [point_path, matrix_path, EPIGRAPH, CUTS, Path(__file__)]
    hashes = {str(path.relative_to(RUN)): sha256(path.read_bytes()).hexdigest() for path in inputs}
    point = json.loads(point_path.read_text())
    with gzip.open(matrix_path, "rt", encoding="utf-8") as stream:
        matrix = json.load(stream)
    epi = json.loads(EPIGRAPH.read_text())
    cuts = json.loads(CUTS.read_text())
    point_hash = sha256(point_path.read_bytes()).hexdigest()
    assert epi["input_sha256"] == cuts["source_sha256"] == point_hash
    strip = lambda col: {k: v for k, v in col.items() if k != "weight"}
    prefix = [strip(col) for col in point["columns"]]
    assert prefix == matrix["columns"]
    metadata_hash = sha256(json.dumps(prefix, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    assert epi["base_column_metadata_sha256"] == metadata_hash
    base_n = len(prefix)
    rows = [parse_row(row) for row in matrix["rows"]]
    names = list(matrix["row_names"])
    base_m = len(rows)
    assert (base_m, base_n) == (5764, 4849)
    assert all(0 <= j < base_n for row in rows for j in row)
    old_values = [F(col["weight"]) for col in point["columns"]]
    assert min(dot(row, old_values) for row in rows) >= 0
    columns = prefix + epi["new_columns"]
    n = len(columns)
    assert n == 12803 and len(epi["rows"]) == 8035
    obj = list(map(F, matrix["objective"])) + [F()] * (n - base_n)
    norm = list(map(F, matrix["normalization"])) + [F()] * (n - base_n)
    thresholds = {}
    budgets = []
    budget_owners = {}
    epi_records = []
    for record in epi["rows"]:
        row = parse_row(record["coefficients"])
        assert all(0 <= j < n for j in row)
        i = len(rows)
        rows.append(row)
        names.append("single-query:" + record["name"])
        epi_records.append({"row": i, "name": record["name"], "kind": record["kind"]})
        auxiliaries = [j for j in row if j >= base_n]
        if record["kind"].endswith("threshold"):
            assert len(auxiliaries) == 1
            j = auxiliaries[0]
            assert row[j] == 1 and j not in thresholds
            thresholds[j] = i
        else:
            assert record["kind"].endswith("budget")
            budgets.append(i)
            for j in auxiliaries:
                assert row[j] < 0 and j not in budget_owners
                budget_owners[j] = (i, row[j])
    assert set(thresholds) == set(budget_owners) == set(range(base_n, n))
    assert len(thresholds) == 7954 and len(budgets) == 81 and len(rows) == 13799
    baseline_extended = old_values + [F()] * (n - base_n)
    for j, i in thresholds.items():
        baseline_extended[j] = max(F(), -dot({k: v for k, v in rows[i].items() if k < base_n}, old_values))
    assert baseline_extended[base_n:] == list(map(F, epi["canonical_extension_at_input"]["new_weights"]))
    baseline_epi_slacks = [dot(row, baseline_extended) for row in rows[base_m:]]
    baseline_budget_slacks = [dot(rows[i], baseline_extended) for i in budgets]
    assert sum(v < 0 for v in baseline_budget_slacks) == 12
    seen = {signature(row): i for i, row in enumerate(rows)}
    imported = []
    pre_cuts = len(rows)
    for record in cuts["selected_rows"]:
        row = parse_row(record["coefficients"])
        assert all(0 <= j < base_n for j in row)
        slack = dot(row, old_values)
        assert slack == F(record["slack"]) < 0
        key = signature(row)
        added = key not in seen
        if added:
            seen[key] = len(rows)
            rows.append(row)
            names.append("round3:" + record["name"])
        imported.append({"name": record["name"], "row": seen[key], "added": added,
                         "baseline_slack": str(slack), "mechanism": record.get("mechanism")})
    nonzeros = sum(map(len, rows))
    write("inputs.json", {"sha256": hashes, "point_sha256": point_hash,
                          "base_column_metadata_sha256": metadata_hash,
                          "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                          "base_rows": base_m, "base_columns": base_n,
                          "epigraph_rows": pre_cuts-base_m, "epigraph_columns": n-base_n,
                          "selected_cut_records": len(imported), "new_distinct_cuts": len(rows)-pre_cuts,
                          "duplicate_cut_records": sum(not record["added"] for record in imported),
                          "rows": len(rows), "columns": n, "nonzeros": nonzeros,
                          "scope": "fixed16hist necessary relaxation only"})
    write("cut_records.json", imported)
    write("epigraph_structure.json", {"original_columns": base_n, "base_rows": base_m,
                                      "thresholds": [[j, i] for j, i in sorted(thresholds.items())],
                                      "budget_owners": [[j, i, str(v)] for j, (i, v) in sorted(budget_owners.items())],
                                      "budget_rows": budgets, "records": epi_records})
    write("old_point_audit.json", {"W": point["W"], "input": str(point_path), "sha256": point_hash,
                                  "canonical_budget_negative_count": 12,
                                  "canonical_budget_slacks": [[i, str(v)] for i, v in zip(budgets, baseline_budget_slacks)],
                                  "minimum_epigraph_slack": str(min(baseline_epi_slacks))})
    encoded = {"columns": columns, "row_names": names,
               "rows": [[[j, str(v)] for j, v in row.items()] for row in rows],
               "objective": list(map(str, obj)), "normalization": list(map(str, norm)),
               "original_rows": 5692, "appended_unique_rows": len(rows)-5692,
               "baseline_rows": base_m, "this_round_added": len(rows)-base_m,
               "original_columns": base_n, "auxiliary_columns": n-base_n}
    with gzip.open(HERE / "exact_matrix.json.gz", "wt", encoding="utf-8") as stream:
        json.dump(encoded, stream, ensure_ascii=False, separators=(",", ":"))
    del encoded, matrix, epi, cuts, seen
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
        new_distinct_cuts=len(rows)-pre_cuts, threshold_rows=len(thresholds), budget_rows=len(budgets))
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
