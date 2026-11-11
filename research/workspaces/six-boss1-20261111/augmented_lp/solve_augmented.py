"""Optimize the archived fixed-16hist 5692-row necessary LP plus 24 cuts.

The original builder is used unchanged. Coefficients are independently checked
against the archived literal reconstruction. Floating candidates are saved
before exact recovery. Every exact claim is checked using Fraction arithmetic.
The finite relaxation is neither a game nor an SPE certificate.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from datetime import datetime, timezone
from collections import Counter
import copy
import gzip
import importlib.util
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
REPO = HERE.parents[3]
RUNTIME = HERE / "runtime"
R2 = RUNTIME / "research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2"
PACK = REPO / "archives/customer-attraction/tools/evidence/requery-capacity-cut-packs-boss3"
OLD = REPO / "archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json"
CUTS = PACK / "runs/all-sparse-row-coefficients.json"
START = time.time()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def log(event, **fields):
    value = {"event": event, "elapsed_seconds": time.time() - START, **fields}
    print(json.dumps(value, ensure_ascii=False), flush=True)
    with (HERE / "progress.jsonl").open("a") as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + "\n")


def dot(row, values):
    return sum((v * values[j] for j, v in row.items() if values[j]), F())


def recover_primal(rows, norm, solution, exact_solve):
    keep = [j for j, value in enumerate(solution) if value > 1e-9]
    vals = solution[keep]
    equations = []
    selected = []
    for i, row in enumerate(rows):
        restricted = [row.get(j, F()) for j in keep]
        scale = max([float(abs(x)) for x in restricted] + [1e-50])
        if any(restricted) and abs(np.dot(np.asarray([float(x) for x in restricted]), vals)) < 1e-10 * scale:
            equations.append(restricted + [F()])
            selected.append(i)
    equations.append([norm[j] for j in keep] + [F(1)])
    log("exact_primal_recovery_started", positive_columns=len(keep), nontrivial_active_rows=len(selected))
    recovered = exact_solve(equations, len(keep))
    full = [F()] * len(solution)
    for j, value in zip(keep, recovered):
        full[j] = value
    assert min(full) >= 0
    assert sum((a * b for a, b in zip(norm, full)), F()) == 1
    slacks = [dot(row, full) for row in rows]
    assert min(slacks) >= 0, (slacks.index(min(slacks)), str(min(slacks)))
    return full, slacks, {"method": "archived exact_solve; original exact_point support/active thresholds; zero equations omitted",
                          "support": keep, "active_rows_used": selected}


def recover_dual(rows, norm, obj, solution, scales, primal, exact_solve):
    multipliers = -solution.ineqlin.marginals / scales
    keep = [i for i, value in enumerate(multipliers) if value > 1e-9]
    columns = [j for j, value in enumerate(primal) if value > 0]
    equations = [[rows[i].get(j, F()) for i in keep] + [norm[j], obj[j]] for j in columns]
    log("exact_dual_recovery_started", positive_row_multipliers=len(keep), equations=len(equations))
    weights = exact_solve(equations, len(keep) + 1)
    lam, lower = weights[:-1], weights[-1]
    assert min(lam) >= 0
    residual = [obj[j] - lower * norm[j] for j in range(len(obj))]
    for i, weight in zip(keep, lam):
        for j, value in rows[i].items():
            residual[j] -= weight * value
    assert min(residual) >= 0, (residual.index(min(residual)), str(min(residual)))
    primal_W = sum((v * w for v, w in zip(obj, primal)), F())
    assert lower == primal_W, (str(lower), str(primal_W))
    return {"verified": True, "normalization_multiplier": str(lower),
            "row_multipliers": [[i, str(value)] for i, value in zip(keep, lam) if value],
            "minimum_coefficient_residual": str(min(residual)),
            "residuals": [str(value) for value in residual],
            "equality_to_primal": True,
            "identity": "obj = lower * norm + sum_i lambda_i * row_i + nonnegative residual; lambda >= 0"}


def main():
    log("start", started_utc=datetime.now(timezone.utc).isoformat())
    input_hashes = {str(path.relative_to(REPO)): sha256(path.read_bytes()).hexdigest()
                    for path in (OLD, CUTS, PACK / "audit_cut_packs.py", Path(__file__), HERE / "materialization.json")}
    write("inputs.json", {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                          "sha256": input_hashes, "scope": "fixed 16hist necessary relaxation only"})
    sys.path.insert(0, str(R2))
    import B_menu_prices_master as builder
    cols, names, dense, obj, norm = builder.build(all_families=True)
    assert (len(dense), len(cols)) == (5692, 4849)
    old = json.loads(OLD.read_text())
    assert len(cols) == len(old["columns"])
    strip = lambda col: {k: v for k, v in col.items() if k != "weight"}
    assert all(strip(a) == strip(b) for a, b in zip(cols, old["columns"]))
    cols = [strip(c) for c in cols]
    rows = [{j: F(value) for j, value in enumerate(row) if value} for row in dense]
    del dense
    obj, norm = list(map(F, obj)), list(map(F, norm))
    log("base_built", rows=len(rows), columns=len(cols), nonzeros=sum(map(len, rows)))

    spec = importlib.util.spec_from_file_location("independent_archived_cut_audit", PACK / "audit_cut_packs.py")
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    records = json.loads(CUTS.read_text())
    seen = {}
    cut_records = []
    for record in records:
        row = {j: F(v) for j, v in record["nonzero"]}
        assert all(j < 1905 for j in row)
        original_pack = json.loads((audit.R3 / record["pack"]).read_text())
        cut = original_pack[record["field"]][record["number"]-1]["cut"]
        kind = "requery" if "requery" in record["pack"] or record["field"] == "requery" else "portfolio"
        rebuilt = audit.independent_row(cols, kind, cut)
        assert row == {j: value for j, value in enumerate(rebuilt) if value}
        fingerprint = sha256(json.dumps([[j, str(value)] for j, value in sorted(row.items())], separators=(",", ":")).encode()).hexdigest()
        if fingerprint not in seen:
            seen[fingerprint] = len(rows)
            rows.append(row)
            names.append("cut-pack:" + record["pack"] + ":" + record["field"] + ":" + str(record["number"]))
        cut_records.append({**record, "augmented_row": seen[fingerprint], "common_sparse_sha256": fingerprint})
    assert len(records) == 27 and len(seen) == 24 and len(rows) == 5716
    write("cut_records.json", cut_records)
    old_values = [F(c["weight"]) for c in old["columns"]]
    old_slacks = [dot(row, old_values) for row in rows]
    assert min(old_slacks[:5692]) >= 0
    assert sum((x * y for x, y in zip(norm, old_values)), F()) == 1
    old_W = sum((x * y for x, y in zip(obj, old_values)), F())
    assert old_W == F(old["W"])
    write("old_point_audit.json", {"W": str(old_W), "rows": len(rows), "original_minimum_slack": str(min(old_slacks[:5692])),
                                  "new_row_slacks": [[i, names[i], str(old_slacks[i])] for i in range(5692, len(rows))],
                                  "new_negative_rows": sum(value < 0 for value in old_slacks[5692:])})
    encoded = {"columns": cols, "row_names": names, "rows": [[[j, str(value)] for j, value in row.items()] for row in rows],
               "objective": list(map(str, obj)), "normalization": list(map(str, norm)), "original_rows": 5692, "appended_unique_rows": 24}
    with gzip.open(HERE / "exact_matrix.json.gz", "wt", encoding="utf-8") as stream:
        json.dump(encoded, stream, separators=(",", ":"))
    del encoded
    ridx, cidx, data = [], [], []
    scales = np.ones(len(rows))
    for i, row in enumerate(rows):
        scales[i] = max([float(abs(v)) for v in row.values()] + [1e-50])
        for j, value in row.items():
            ridx.append(i); cidx.append(j); data.append(-float(value) / scales[i])
    matrix = coo_matrix((data, (ridx, cidx)), shape=(len(rows), len(cols))).tocsr()
    log("augmented_matrix_ready", rows=len(rows), columns=len(cols), unique_cuts=len(seen), independent_cut_records_checked=len(records),
        old_point_negative_new_rows=sum(value < 0 for value in old_slacks[5692:]))
    sol = linprog([float(v) for v in obj], A_ub=matrix, b_ub=np.zeros(len(rows)),
                  A_eq=[[float(v) for v in norm]], b_eq=[1], bounds=(0, None), method="highs",
                  options={"primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9})
    summary = {"success": bool(sol.success), "status": sol.message, "W_float": None if sol.fun is None else float(sol.fun),
               "rows": len(rows), "columns": len(cols), "seconds_to_float": time.time()-START,
               "exact_verified": False, "scope": "fixed16hist necessary relaxation, not an SPE or universal bound"}
    write("status.json", summary)
    if not sol.success:
        log("solver_failed", **summary)
        return
    floating = {**summary, "O": "1", "W": str(sol.fun), "columns": [{**col, "weight": str(value)} for col, value in zip(cols, sol.x)]}
    write("augmented_lp_float.json", floating)
    np.savez_compressed(HERE / "floating_solver_arrays.npz", primal=sol.x, inequality_marginals=sol.ineqlin.marginals,
                        equality_marginals=sol.eqlin.marginals, lower_marginals=sol.lower.marginals, scales=scales)
    log("float_candidate_saved", **summary)
    exact_solve = builder.minimal.base.cl.exact_solve
    try:
        full, slacks, recovery = recover_primal(rows, norm, sol.x, exact_solve)
        W = sum((x*y for x,y in zip(obj, full)), F())
        exact = {"scope": "exact feasible fixed16hist necessary-condition point; not an SPE, not a game, not a universal bound",
                 "O": "1", "W": str(W), "strict_half_gap": str(1-2*W), "verified_rows": len(rows),
                 "minimum_slack": str(min(slacks)), "positive_columns": sum(value > 0 for value in full),
                 "exact_verified": True, "original_rows": 5692, "appended_distinct_rows": 24,
                 "columns": [{**col, "weight": str(value)} for col, value in zip(cols, full)]}
        write("augmented_lp_exact.json", exact)
        write("primal_exact_audit.json", {"recovery": recovery, "nonnegative": True, "normalization": "1", "W": str(W),
                                         "W_float": float(W), "old_W": str(old_W), "point_W_difference": str(W-old_W),
                                         "minimum_slack": str(min(slacks)), "row_slacks": list(map(str, slacks)),
                                         "new_row_slacks": [[i, names[i], str(slacks[i])] for i in range(5692, len(rows))]})
        summary.update({"exact_verified": True, "W_exact": str(W), "W_exact_float": float(W),
                        "below_half": W < F(1,2), "exact_point_difference_from_old": str(W-old_W)})
        write("status.json", summary)
        log("exact_primal_saved", W=str(W), W_float=float(W), strict_half_gap=str(1-2*W),
            point_W_difference_from_old=str(W-old_W), positive_columns=sum(v > 0 for v in full))
    except Exception:
        summary["exact_primal_failure"] = traceback.format_exc()
        write("status.json", summary)
        log("exact_primal_failed", detail=summary["exact_primal_failure"])
        return
    try:
        dual = recover_dual(rows, norm, obj, sol, scales, full, exact_solve)
        write("exact_dual_certificate.json", dual)
        summary.update({"exact_optimum_verified": True, "strictly_above_old_W": F(dual["normalization_multiplier"]) > old_W,
                        "seconds": time.time()-START})
        write("status.json", summary)
        log("exact_optimum_verified", W=dual["normalization_multiplier"], strictly_above_old_W=summary["strictly_above_old_W"])
    except Exception:
        summary.update({"exact_optimum_verified": False, "exact_dual_failure": traceback.format_exc(), "seconds": time.time()-START})
        write("status.json", summary)
        log("exact_dual_failed", detail=summary["exact_dual_failure"])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        write("unhandled_failure.json", {"traceback": traceback.format_exc(), "seconds": time.time()-START})
        raise
