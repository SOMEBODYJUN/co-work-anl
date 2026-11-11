"""Append certified row files to a cached finite matrix and resolve exactly.

Usage: refine_cached.py BASE_DIRECTORY OUTPUT_DIRECTORY EXTRA_JSON [...]
Supported extras are cross-branch selected_rows, cross-branch rows with negative
saved slack, or transport families[*].certificate.sparse_original_row.
Input hashes and exact slacks bind every imported row to the baseline point.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import gzip
import json
import sys
import time
import traceback

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

import solve_augmented as common
import recover_dual_free as dual_recovery


def main():
    base, output, *extras = map(lambda value: Path(value).resolve(), sys.argv[1:])
    output.mkdir(parents=True, exist_ok=False)
    common.HERE = output
    common.START = time.time()
    write, log = common.write, common.log
    point_path = base / "augmented_lp_exact.json"
    point_raw = point_path.read_bytes()
    point = json.loads(point_raw)
    point_hash = sha256(point_raw).hexdigest()
    baseline_W = F(point["W"])
    values = [F(col["weight"]) for col in point["columns"]]
    with gzip.open(base / "exact_matrix.json.gz", "rt") as stream:
        matrix = json.load(stream)
    cols, names = matrix["columns"], matrix["row_names"]
    rows = [{j: F(value) for j,value in row} for row in matrix["rows"]]
    original_count = len(rows)
    norm, obj = list(map(F, matrix["normalization"])), list(map(F, matrix["objective"]))
    signature = lambda row: tuple((j, str(value)) for j,value in sorted(row.items()) if value)
    seen = {signature(row): i for i,row in enumerate(rows)}
    imported = []
    input_hashes = {str(point_path): point_hash,
                    str(base / "exact_matrix.json.gz"): sha256((base / "exact_matrix.json.gz").read_bytes()).hexdigest()}
    for extra in extras:
        raw = extra.read_bytes()
        input_hashes[str(extra)] = sha256(raw).hexdigest()
        report = json.loads(raw)
        source_hash = report.get("source_sha256", report.get("input_sha256"))
        assert source_hash == point_hash, (str(extra), source_hash, point_hash)
        if "families" in report:
            records = [{"name": "transport:" + family["family"],
                        "coefficients": family["certificate"]["sparse_original_row"],
                        "slack": family["certificate"]["exact_slack"]} for family in report["families"]]
        elif "selected_rows" in report:
            records = report["selected_rows"]
        else:
            records = [record for record in report["rows"] if F(record["slack"]) < 0]
        for record in records:
            row = {j: F(value) for j,value in record["coefficients"] if F(value)}
            assert all(0 <= j < len(cols) for j in row)
            slack = common.dot(row, values)
            assert slack == F(record["slack"]) < 0
            key = signature(row)
            if key not in seen:
                seen[key] = len(rows)
                rows.append(row)
                names.append(extra.stem + ":" + record["name"])
            imported.append({"source": str(extra), "name": record["name"], "row": seen[key], "baseline_slack": str(slack)})
    write("inputs.json", {"sha256": input_hashes, "baseline_rows": original_count, "baseline_W": str(baseline_W),
                          "new_records": len(imported), "new_distinct_rows": len(rows)-original_count,
                          "scope": "fixed16hist necessary relaxation; imported cuts certified in named agent files"})
    write("cut_records.json", imported)
    write("old_point_audit.json", {"W": str(baseline_W), "input": str(point_path), "sha256": point_hash})
    encoded = {"columns": cols, "row_names": names,
               "rows": [[[j,str(value)] for j,value in row.items()] for row in rows],
               "objective": list(map(str,obj)), "normalization": list(map(str,norm)),
               "original_rows": 5692, "appended_unique_rows": len(rows)-5692,
               "baseline_rows": original_count, "this_round_added": len(rows)-original_count}
    with gzip.open(output / "exact_matrix.json.gz", "wt") as stream:
        json.dump(encoded,stream,separators=(",", ":"))
    ridx,cidx,data=[],[],[]
    scales=np.ones(len(rows))
    for i,row in enumerate(rows):
        scales[i]=max([float(abs(value)) for value in row.values()]+[1e-50])
        for j,value in row.items():
            ridx.append(i);cidx.append(j);data.append(-float(value)/scales[i])
    sparse=coo_matrix((data,(ridx,cidx)),shape=(len(rows),len(cols))).tocsr()
    log("refined_matrix_ready", rows=len(rows), columns=len(cols), records=len(imported), distinct_added=len(rows)-original_count)
    sol=linprog([float(v) for v in obj],A_ub=sparse,b_ub=np.zeros(len(rows)),
                A_eq=[[float(v) for v in norm]],b_eq=[1],bounds=(0,None),method="highs",
                options={"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9})
    status={"success":bool(sol.success),"status":sol.message,"W_float":None if sol.fun is None else float(sol.fun),
            "rows":len(rows),"columns":len(cols),"exact_verified":False,
            "scope":"fixed16hist necessary relaxation only; not SPE or universal half bound"}
    write("status.json",status)
    if not sol.success:
        log("solver_failed",**status)
        return
    write("augmented_lp_float.json",{**status,"O":"1","W":str(sol.fun),
                                    "columns":[{**col,"weight":str(value)} for col,value in zip(cols,sol.x)]})
    np.savez_compressed(output/"floating_solver_arrays.npz",primal=sol.x,inequality_marginals=sol.ineqlin.marginals,
                        equality_marginals=sol.eqlin.marginals,lower_marginals=sol.lower.marginals,scales=scales)
    log("float_candidate_saved",**status)
    keep=[j for j,value in enumerate(sol.x) if value>1e-9]
    solve=lambda equations,n: dual_recovery.affine_solve(equations,n,[sol.x[j] for j in keep])[0]
    try:
        full,slacks,recovery=common.recover_primal(rows,norm,sol.x,solve)
        recovery["method"]="sparse exact echelon elimination on active equations; full Fraction verification"
        W=sum((a*b for a,b in zip(obj,full)),F())
        exact={"scope":"exact feasible fixed16hist necessary relaxation; not SPE or game",
               "O":"1","W":str(W),"strict_half_gap":str(1-2*W),"verified_rows":len(rows),
               "minimum_slack":str(min(slacks)),"positive_columns":sum(v>0 for v in full),"exact_verified":True,
               "columns":[{**col,"weight":str(value)} for col,value in zip(cols,full)]}
        write("augmented_lp_exact.json",exact)
        write("primal_exact_audit.json",{"W":str(W),"W_float":float(W),"minimum_slack":str(min(slacks)),
                                         "row_slacks":list(map(str,slacks)),"recovery":recovery})
        status.update({"exact_verified":True,"W_exact":str(W),"below_half":W<F(1,2),"exact_point_difference_from_baseline":str(W-baseline_W)})
        write("status.json",status)
        log("exact_primal_saved",W=str(W),W_float=float(W),below_half=W<F(1,2),positive_columns=sum(v>0 for v in full))
    except Exception:
        status["exact_primal_failure"]=traceback.format_exc();write("status.json",status)
        log("exact_primal_failed",detail=status["exact_primal_failure"])
        return
    dual_recovery.HERE=output
    try:
        dual_recovery.main()
        log("exact_optimum_verified",W=str(W),W_float=float(W),below_half=W<F(1,2))
    except Exception:
        status=json.loads((output/"status.json").read_text());status["exact_dual_failure"]=traceback.format_exc()
        write("status.json",status);log("exact_dual_failed",detail=status["exact_dual_failure"])


if __name__=="__main__":
    main()
