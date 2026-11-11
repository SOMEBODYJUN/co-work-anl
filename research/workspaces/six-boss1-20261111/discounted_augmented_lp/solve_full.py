"""Append the 22 frozen named discounted rows to the certified ZZ19556 LP.

All inherited columns, rows, objective and normalization are kept unchanged.
The 7954 positive-part and 2790 minimum auxiliaries keep their old semantics.
This finite necessary-condition LP alone is optimized; no SPE claim is made.
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
import time
import traceback

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
BASE = RUN / "zz_closure_lp" / "round2"
CUTS = RUN / "shared_source_deepening" / "selected_all_named_19556.json"
START = time.time()
EXPECTED_POINT = "bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3"
EXPECTED_MATRIX = "353b1978b6c2ad46d28dc33a03b5ff8c3f71f273d9bf4d71cc15f5a9cf223f0c"
EXPECTED_CUTS = "3b373504be8593d6737433ea8341aac5eba67a153243392d173631e05f02e130"


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")


def log(event, **fields):
    record = {"event": event, "utc": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": time.time()-START, **fields}
    line = json.dumps(record, ensure_ascii=False)
    print(line, flush=True)
    with (HERE / "progress.jsonl").open("a") as stream:
        stream.write(line+"\n")


def dot(row, values):
    return sum((v*values[j] for j, v in row.items() if values[j]), F())


def parse_row(encoded, n):
    row = {}
    for j, value in encoded:
        assert isinstance(j, int) and 0 <= j < n and j not in row
        value = F(value)
        assert value
        row[j] = value
    return row


def signature(row):
    return tuple(sorted(row.items()))


def main():
    log("start", scope="ZZ19556 plus 22 named discounted rows; finite necessary LP only")
    point_path, matrix_path = BASE/"augmented_lp_exact.json", BASE/"exact_matrix.json.gz"
    for path, digest in ((point_path, EXPECTED_POINT), (matrix_path, EXPECTED_MATRIX), (CUTS, EXPECTED_CUTS)):
        assert sha256(path.read_bytes()).hexdigest() == digest, str(path)
    point = json.loads(point_path.read_text())
    with gzip.open(matrix_path, "rt", encoding="utf-8") as stream:
        matrix = json.load(stream)
    cuts = json.loads(CUTS.read_text())
    assert cuts["source_sha256"] == EXPECTED_POINT and cuts["matrix_sha256"] == EXPECTED_MATRIX
    assert (cuts["baseline_rows"], cuts["columns"], cuts["original_columns"]) == (19556, 15593, 4849)
    columns = matrix["columns"]
    n, original_n, prior_m = len(columns), 4849, len(matrix["rows"])
    assert (prior_m, n) == (19556, 15593)
    assert [{k:v for k,v in c.items() if k != "weight"} for c in point["columns"]] == columns
    rows = [parse_row(row, n) for row in matrix["rows"]]
    names = list(matrix["row_names"])
    obj, norm = list(map(F, matrix["objective"])), list(map(F, matrix["normalization"]))
    old_values = [F(c["weight"]) for c in point["columns"]]
    assert min(old_values) >= 0
    assert min(dot(row, old_values) for row in rows) >= 0
    assert sum((a*b for a,b in zip(norm,old_values)), F()) == 1
    assert sum((a*b for a,b in zip(obj,old_values)), F()) == F(point["W"])
    epi = json.loads((HERE/"epigraph_structure.json").read_text())
    zz = json.loads((HERE/"zz_envelope_structure.json").read_text())
    for name in ("epigraph_structure.json", "zz_envelope_structure.json"):
        assert (HERE/name).read_bytes() == (BASE/name).read_bytes()
    thresholds = dict(epi["thresholds"])
    assert len(thresholds) == 7954 and len(zz["auxiliaries"]) == 2790
    assert set(thresholds) == set(range(original_n,12803))
    for j,i in thresholds.items():
        assert old_values[j] == max(F(),-dot({k:v for k,v in rows[i].items() if k < original_n},old_values))
    for record in zz["auxiliaries"]:
        assert old_values[record["column"]] == min(dot({k:v for k,v in rows[i].items() if k < original_n},old_values)
                                                    for i in (record["q_upper_row"], record["v_upper_row"]))
    seen = {signature(row):i for i,row in enumerate(rows)}
    records = []
    selected = cuts["selected_rows"]
    assert len(selected) == 22
    assert Counter((r["state_count"],r["theta"]) for r in selected) == {(2,"0"):11,(2,"1/4"):10,(4,"1/4"):1}
    for r in selected:
        row = parse_row(r["coefficients"],n)
        assert all(j < original_n for j in row)
        digest = sha256(json.dumps(r["coefficients"],separators=(",",":")).encode()).hexdigest()
        assert digest == r["vector_sha256"]
        value = dot(row, old_values)
        assert value == F(r["slack"]) == F(r["exact_slack"]) < 0
        key = signature(row)
        assert key not in seen, (r["name"],seen.get(key))
        index = len(rows)
        seen[key] = index
        rows.append(row)
        names.append("named-at19556:"+r["name"])
        records.append({"row":index,"name":r["name"],"vector_sha256":digest,"input_slack":str(value),
                        "family":r["family"],"actual_source_zero_based":r["actual_source_zero_based"],
                        "forced":r["forced"],"theta":r["theta"],"state_count":r["state_count"],
                        "nonzero_original_coordinates":len(row),"auxiliary_coefficients_all_zero":True})
    assert len(rows) == 19578
    write("cut_records.json", records)
    write("old_point_audit.json", {"input":str(point_path),"sha256":EXPECTED_POINT,"W":point["W"],
          "verified_baseline_rows":prior_m,"nonnegative_columns":n,"new_negative_rows":len(records),
          "new_row_slacks":[[r["row"],r["name"],r["input_slack"]] for r in records]})
    input_paths = [point_path,matrix_path,CUTS,Path(__file__),HERE/"recover_full.py",HERE/"verify_certificates.py",
                   BASE/"epigraph_structure.json",BASE/"zz_envelope_structure.json",BASE/"exact_dual_certificate.json"]
    write("inputs.json", {"sha256":{str(p.relative_to(RUN)):sha256(p.read_bytes()).hexdigest() for p in input_paths},
          "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
          "baseline_rows":prior_m,"baseline_columns":n,"original_columns":original_n,
          "new_distinct_rows":22,"duplicate_rows":0,"rows":len(rows),"columns":n,
          "max_auxiliaries":len(thresholds),"min_auxiliaries":len(zz["auxiliaries"]),
          "scope":"finite fixed16hist necessary LP only; no SPE or universal lower bound claim"})
    encoded = {**matrix,"row_names":names,"rows":[[[j,str(v)] for j,v in sorted(row.items())] for row in rows],
               "appended_unique_rows":len(rows)-matrix["original_rows"],"baseline_rows":prior_m,
               "this_round_added":22,"new_row_package_sha256":EXPECTED_CUTS}
    with (HERE/"exact_matrix.json.gz").open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as stream:
            stream.write(json.dumps(encoded,ensure_ascii=False,separators=(",",":")).encode())
    nonzeros = sum(map(len,rows))
    del encoded,matrix,cuts,seen,old_values
    ridx,cidx,data = [],[],[]
    scales = np.ones(len(rows))
    for i,row in enumerate(rows):
        scales[i] = max([float(abs(v)) for v in row.values()]+[1e-50])
        for j,value in row.items():
            ridx.append(i);cidx.append(j);data.append(-float(value)/scales[i])
    sparse = coo_matrix((data,(ridx,cidx)),shape=(len(rows),n)).tocsr()
    log("matrix_ready",rows=len(rows),columns=n,nonzeros=nonzeros,new_rows=22)
    solver_start=time.time()
    options={"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9}
    solution=linprog(list(map(float,obj)),A_ub=sparse,b_ub=np.zeros(len(rows)),
                     A_eq=coo_matrix(np.asarray([list(map(float,norm))])).tocsr(),b_eq=[1],
                     bounds=(0,None),method="highs",options=options)
    status={"success":bool(solution.success),"status_code":int(solution.status),"status":solution.message,
            "solver_seconds":time.time()-solver_start,"solver_iterations":solution.nit,"solver_options":options,
            "W_float":None if solution.fun is None else float(solution.fun),"rows":len(rows),"columns":n,
            "exact_verified":False,"scope":"finite fixed16hist necessary relaxation only; not SPE or universal half bound"}
    write("status.json",status)
    assert solution.success, solution.message
    canonical=solution.x.copy()
    for j,i in thresholds.items():
        canonical[j]=max(0.0,-sum(float(v)*canonical[k] for k,v in rows[i].items() if k < original_n))
    for r in zz["auxiliaries"]:
        canonical[r["column"]]=max(0.0,min(sum(float(v)*canonical[k] for k,v in rows[i].items() if k < original_n)
                                                 for i in (r["q_upper_row"],r["v_upper_row"])))
    status.update({"positive_original_columns":int(np.count_nonzero(canonical[:original_n]>1e-9)),
                   "positive_old_max_auxiliaries":int(np.count_nonzero(canonical[original_n:12803]>1e-9)),
                   "positive_min_auxiliaries":int(np.count_nonzero(canonical[12803:]>1e-9)),
                   "minimum_scaled_solver_slack":float(np.min(-sparse@solution.x)),
                   "minimum_scaled_canonical_slack":float(np.min(-sparse@canonical))})
    write("status.json",status)
    write("augmented_lp_float.json",{**status,"O":"1","W":str(solution.fun),
          "completion":"unchanged canonical max and min auxiliaries; floating only",
          "columns":[{**col,"weight":str(v)} for col,v in zip(columns,canonical)]})
    np.savez_compressed(HERE/"floating_solver_arrays.npz",primal=solution.x,canonical=canonical,
          inequality_marginals=solution.ineqlin.marginals,equality_marginals=solution.eqlin.marginals,
          lower_marginals=solution.lower.marginals,scales=scales)
    log("float_candidate_saved",**status)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        write("assembly_or_float_failure.json",{"traceback":traceback.format_exc()})
        raise
