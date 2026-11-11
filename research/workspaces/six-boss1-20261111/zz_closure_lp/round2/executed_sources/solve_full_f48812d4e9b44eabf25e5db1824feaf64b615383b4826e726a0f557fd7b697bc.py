"""Full old-Z/old-Z Frechet minimum envelopes plus approved new early cuts.

Every row is row*x >= 0. The original 4849 columns and all 7954 earlier
positive-part auxiliaries are unchanged. New upper-envelope variables k are
bounded by q_source and v_query; every orbit budget uses them with positive
coefficients, so canonical k=min(q_source,v_query) is an exact existential
representation of the whole minimum envelope, not a physical joint coupling.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
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
BASE = HERE.parent
RUN = BASE.parent
CUTS = RUN / "new_point_separation" / "priority_six_cuts_13931.json"
START = time.time()


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
    return sum((coefficient*values[j] for j, coefficient in row.items() if values[j]), F())


def add(row, j, value):
    if value:
        value += row.get(j, F())
        if value:
            row[j] = value
        else:
            row.pop(j, None)


def signature(row):
    return tuple((j, str(v)) for j, v in sorted(row.items()) if v)


def parse_row(encoded):
    row = {}
    for j, value in encoded:
        assert isinstance(j, int) and j not in row
        value = F(value)
        if value:
            row[j] = value
    return row


def group_key(raw):
    return raw[0], raw[1], tuple(raw[2]), tuple(raw[3])


def partition(xs):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in xs)


def main():
    log("start", scope="full ZZ Frechet minimum envelopes within the fixed16hist necessary LP only")
    point_path = BASE / "augmented_lp_exact.json"
    matrix_path = BASE / "exact_matrix.json.gz"
    source_audit_path = BASE / "zz-at-certified-point.json"
    epi_path = BASE / "epigraph_structure.json"
    input_paths = [point_path, matrix_path, source_audit_path, epi_path, CUTS, Path(__file__)]
    hashes = {str(path.relative_to(RUN)): sha256(path.read_bytes()).hexdigest() for path in input_paths}
    point_hash = sha256(point_path.read_bytes()).hexdigest()
    assert point_hash == "3ba6eb84ca024a6e7bf2816eea010f8bfaf6de610a7a93229711af4bd26a671b"
    assert sha256(matrix_path.read_bytes()).hexdigest() == "aecc64e6e068a33ee119d67ad25a116de5aef431b1fcc004f1799a55562b07c5"
    point = json.loads(point_path.read_text())
    with gzip.open(matrix_path, "rt", encoding="utf-8") as stream:
        matrix = json.load(stream)
    source_audit = json.loads(source_audit_path.read_text())
    cuts = json.loads(CUTS.read_text())
    assert source_audit["input_sha256"] == point_hash
    assert source_audit["matrix_sha256"] == sha256(matrix_path.read_bytes()).hexdigest()
    assert cuts.get("input_sha256", cuts.get("source_sha256")) == point_hash
    assert cuts["matrix_sha256"] == sha256(matrix_path.read_bytes()).hexdigest()
    assert sha256(CUTS.read_bytes()).hexdigest() == "243343cc3076fb1c607397256f60653d7b033a92cc0f3c61b42e9c27bca68409"
    strip = lambda col: {k: v for k, v in col.items() if k != "weight"}
    columns = [strip(col) for col in point["columns"]]
    assert columns == matrix["columns"]
    original_n, prior_n = 4849, len(columns)
    rows = [parse_row(row) for row in matrix["rows"]]
    names = list(matrix["row_names"])
    prior_m = len(rows)
    assert (prior_m, prior_n) == (13931, 12803)
    obj, norm = list(map(F, matrix["objective"])), list(map(F, matrix["normalization"]))
    old_values = [F(col["weight"]) for col in point["columns"]]
    assert min(old_values) >= 0 and min(dot(row, old_values) for row in rows) >= 0
    assert sum((a*b for a, b in zip(norm, old_values)), F()) == 1
    assert sum((a*b for a, b in zip(obj, old_values)), F()) == F(point["W"])
    metadata_hash = sha256(json.dumps(columns[:original_n], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    assert metadata_hash == source_audit["original_columns_sha256"]
    epi = json.loads(epi_path.read_text())
    assert epi["original_columns"] == original_n
    max_thresholds = dict(epi["thresholds"])
    assert set(max_thresholds) == set(range(original_n, prior_n))
    for j, i in max_thresholds.items():
        assert old_values[j] == max(F(), -dot({k: v for k, v in rows[i].items() if k < original_n}, old_values))

    hist = {}
    groups = defaultdict(dict)
    old_to_current = {}
    current_hist = None
    for j, col in enumerate(columns[:original_n]):
        if col["kind"] == "hist":
            current_hist = j
            hist[j] = col
        elif col["kind"] == "joint-reply":
            old = col["hist_column_old"]
            assert old_to_current.setdefault(old, current_hist) == current_hist
            groups[current_hist].setdefault(group_key(col["group"]), {})[tuple(col["state"])] = j
    assert len(hist) == 16 and sum(map(len, groups.values())) == 194
    for gs in groups.values():
        for ids in gs.values():
            assert set(ids) == {(0, 1), (1, 0), (1, 1)}
    edges = [e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2]]
    assert len(edges) == 66
    aux_records = []
    budgets = defaultdict(dict)
    orbit_counts = Counter()
    group_counts = []
    for hi, col in hist.items():
        words = [word for word, count in zip(product(range(2), repeat=3), col["hist"]) for _ in range(count)]
        assert len(words) == 6
        gs = {e: (e[0], int(e[1] == e[2]), words[e[1]], words[e[2]]) for e in edges}
        pairs = sorted({(gs[e], gs[f]) for e in edges for f in edges if e != f})
        group_counts.append([hi, len(set(gs.values())), len(pairs)])
        pair_columns = {}
        for source, query in pairs:
            j = len(columns)
            pair_columns[source, query] = j
            columns.append({"kind": "ZZ-frechet-envelope-upper", "hist_column": hi,
                            "source_group": source, "query_group": query,
                            "semantics": "virtual common upper envelope, not a physical cross intersection"})
            qids, vids = groups[hi][source], groups[hi][query]
            q = {qids[1, 0]: F(1), qids[1, 1]: F(1)}
            v = {vids[0, 1]: F(1), vids[1, 1]: F(1)}
            upper_rows = []
            for tag, bound in (("q", q), ("v", v)):
                upper_rows.append(len(rows))
                rows.append({**bound, j: F(-1)})
                names.append(f"ZZ-upper:{j}:{tag}")
            aux_records.append({"column": j, "hist_column": hi, "source_group": source, "query_group": query,
                                "q_upper_row": upper_rows[0], "v_upper_row": upper_rows[1]})
            old_values.append(min(dot(q, old_values), dot(v, old_values)))
        P = sum(map(int, col["actual_bits"][:4]))
        D = (P+1)*(P+2)
        for e in edges:
            ie = groups[hi][gs[e]]
            for f in edges:
                if e == f:
                    continue
                name = (e[0], f[0], partition((e[1], e[2], f[1], f[2])))
                orbit_counts[name] += 1
                row = budgets[name]
                jf = groups[hi][gs[f]]
                for state in ((0, 1), (1, 1)):
                    add(row, ie[state], F(1, P+1))
                    add(row, jf[state], -F(1, P+1))
                add(row, ie[1, 1], -F(1, D))
                add(row, pair_columns[gs[e], gs[f]], F(1, D))
    assert len(aux_records) == 2790 and len(budgets) == 39
    assert len({signature(row) for row in budgets.values()}) == 39
    expected_values = {(record["name"][0], record["name"][1], tuple(record["name"][2])): F(record["value"])
                       for record in source_audit["known_ZZ_frechet_bounds_at_this_point"]}
    budget_records = []
    for name, row in sorted(budgets.items()):
        index = len(rows)
        rows.append(row)
        names.append("ZZ-full-min:"+json.dumps(name, separators=(",", ":")))
        slack = dot(row, old_values)
        assert slack == expected_values[name]
        assert all(value > 0 for j, value in row.items() if j >= prior_n)
        budget_records.append({"row": index, "orbit": name, "literal_pair_hist_terms": orbit_counts[name],
                               "input_slack": str(slack)})
    assert len(rows) == 19550 and len(columns) == 15593
    assert sum(F(record["input_slack"]) < 0 for record in budget_records) == 12
    n = len(columns)
    obj += [F()]*(n-prior_n)
    norm += [F()]*(n-prior_n)
    before_early = len(rows)
    seen = {signature(row): i for i, row in enumerate(rows)}
    early_records = []
    selected = cuts.get("selected_rows", cuts.get("rows", cuts.get("cuts")))
    assert isinstance(selected, list) and len(selected) == 6
    for record in selected:
        row = parse_row(record.get("coefficients", record.get("row")))
        assert row and all(0 <= j < original_n for j in row)
        slack = dot(row, old_values)
        assert slack == F(record.get("slack", record.get("value"))) < 0
        assert sha256(json.dumps(record["coefficients"], separators=(",", ":")).encode()).hexdigest() == record["sparse_sha256"]
        name = record["name"]
        key = signature(row)
        added = key not in seen
        if added:
            seen[key] = len(rows)
            rows.append(row)
            names.append("new-early-at13931:"+str(name))
        early_records.append({"name": name, "row": seen[key], "added": added, "input_slack": str(slack),
                              "mechanism": record.get("mechanism")})
    nonzeros = sum(map(len, rows))
    structure = {"scope": "exact shared-upper-variable formulation of all 39 nonself ZZ minimum envelopes",
                 "original_columns": original_n, "prior_columns": prior_n, "prior_rows": prior_m,
                 "group_counts": group_counts, "all_ordered_group_pairs": 2806,
                 "unused_self_only_group_pairs_omitted": 16,
                 "auxiliaries": aux_records, "budget_records": budget_records,
                 "budget_rows": [record["row"] for record in budget_records],
                 "upper_rows": [i for record in aux_records for i in (record["q_upper_row"], record["v_upper_row"])],
                 "literal_nonself_hist_terms": sum(orbit_counts.values())}
    write("zz_envelope_structure.json", structure)
    shutil.copyfile(epi_path, HERE / "epigraph_structure.json")
    write("early_cut_records.json", early_records)
    write("inputs.json", {"sha256": hashes, "point_sha256": point_hash,
                          "base_column_metadata_sha256": metadata_hash,
                          "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                          "baseline_rows": prior_m, "baseline_columns": prior_n, "original_columns": original_n,
                          "old_max_auxiliaries": prior_n-original_n, "new_min_auxiliaries": n-prior_n,
                          "new_upper_rows": len(structure["upper_rows"]), "new_orbit_budgets": len(budget_records),
                          "early_cut_records": len(early_records), "new_distinct_early_cuts": len(rows)-before_early,
                          "duplicate_early_cuts": sum(not record["added"] for record in early_records),
                          "rows": len(rows), "columns": n, "nonzeros": nonzeros,
                          "scope": "fixed16hist necessary relaxation only"})
    write("old_point_audit.json", {"W": point["W"], "input": str(point_path), "sha256": point_hash,
                                  "canonical_ZZ_negative_budgets": 12, "canonical_ZZ_budgets": budget_records,
                                  "negative_early_cut_records": len(early_records)})
    encoded = {"columns": columns, "row_names": names,
               "rows": [[[j, str(v)] for j, v in sorted(row.items())] for row in rows],
               "objective": list(map(str, obj)), "normalization": list(map(str, norm)),
               "original_rows": 5692, "appended_unique_rows": len(rows)-5692,
               "baseline_rows": prior_m, "this_round_added": len(rows)-prior_m,
               "original_columns": original_n, "auxiliary_columns": n-original_n,
               "canonical_max_auxiliaries": prior_n-original_n, "canonical_min_auxiliaries": n-prior_n}
    with (HERE / "exact_matrix.json.gz").open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as stream:
            stream.write(json.dumps(encoded, ensure_ascii=False, separators=(",", ":")).encode())
    del encoded, matrix, cuts, source_audit, seen, budgets
    ridx, cidx, data = [], [], []
    scales = np.ones(len(rows))
    for i, row in enumerate(rows):
        scales[i] = max([float(abs(v)) for v in row.values()]+[1e-50])
        for j, value in row.items():
            ridx.append(i); cidx.append(j); data.append(-float(value)/scales[i])
    sparse = coo_matrix((data, (ridx, cidx)), shape=(len(rows), n)).tocsr()
    log("matrix_ready", rows=len(rows), columns=n, nonzeros=nonzeros,
        min_auxiliaries=len(aux_records), min_upper_rows=len(structure["upper_rows"]),
        ZZ_orbit_budgets=len(budget_records), new_distinct_early_cuts=len(rows)-before_early)
    solver_start = time.time()
    solution = linprog(list(map(float, obj)), A_ub=sparse, b_ub=np.zeros(len(rows)),
                       A_eq=coo_matrix(np.asarray([list(map(float, norm))])).tocsr(), b_eq=[1],
                       bounds=(0, None), method="highs", options={"primal_feasibility_tolerance": 1e-9,
                                                                 "dual_feasibility_tolerance": 1e-9})
    status = {"success": bool(solution.success), "status_code": int(solution.status), "status": solution.message,
              "solver_seconds": time.time()-solver_start, "solver_iterations": solution.nit,
              "W_float": None if solution.fun is None else float(solution.fun), "rows": len(rows), "columns": n,
              "exact_verified": False, "scope": "fixed16hist necessary relaxation only; not SPE or universal half bound"}
    write("status.json", status)
    if not solution.success:
        log("solver_failed", **status)
        return
    canonical = solution.x.copy()
    for j, i in max_thresholds.items():
        canonical[j] = max(0.0, -sum(float(v)*canonical[k] for k, v in rows[i].items() if k < original_n))
    for record in aux_records:
        j = record["column"]
        bounds = [sum(float(v)*canonical[k] for k, v in rows[i].items() if k < original_n)
                  for i in (record["q_upper_row"], record["v_upper_row"])]
        canonical[j] = max(0.0, min(bounds))
    status.update({"positive_original_columns": int(np.count_nonzero(solution.x[:original_n] > 1e-9)),
                   "positive_old_max_auxiliaries": int(np.count_nonzero(canonical[original_n:prior_n] > 1e-9)),
                   "positive_new_min_auxiliaries": int(np.count_nonzero(canonical[prior_n:] > 1e-9)),
                   "positive_solver_columns": int(np.count_nonzero(solution.x > 1e-9)),
                   "positive_canonical_columns": int(np.count_nonzero(canonical > 1e-9)),
                   "minimum_scaled_solver_slack": float(np.min(-sparse@solution.x)),
                   "minimum_scaled_canonical_slack": float(np.min(-sparse@canonical))})
    write("status.json", status)
    write("augmented_lp_float.json", {**status, "O": "1", "W": str(solution.fun),
                                      "completion": "old auxiliaries canonical max, new upper envelopes canonical min; floating only",
                                      "columns": [{**col, "weight": str(value)} for col, value in zip(columns, canonical)]})
    np.savez_compressed(HERE / "floating_solver_arrays.npz", primal=solution.x, canonical=canonical,
                        inequality_marginals=solution.ineqlin.marginals, equality_marginals=solution.eqlin.marginals,
                        lower_marginals=solution.lower.marginals, scales=scales)
    log("float_candidate_saved", **status)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        write("assembly_or_float_failure.json", {"traceback": traceback.format_exc()})
        raise
