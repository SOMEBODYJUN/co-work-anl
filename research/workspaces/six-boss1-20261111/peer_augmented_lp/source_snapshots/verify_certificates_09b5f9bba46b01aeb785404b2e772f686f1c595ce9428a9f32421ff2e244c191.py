"""Standard-library verification of saved full-min matrix and exact certificates.

No constructor or recovery module is imported. The upper-envelope extension is
rebuilt using orbit/group incidence counts; inherited rows are checked against
the frozen exact matrix, not independently rederived as mathematical statements.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
RUN = BASE.parent


def key(raw):
    return raw[0], raw[1], tuple(raw[2]), tuple(raw[3])


def partition(xs):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in xs)


def main():
    start = time.time()
    inputs = json.loads((HERE / "inputs.json").read_text())
    for relative, digest in inputs["sha256"].items():
        assert sha256((RUN / relative).read_bytes()).hexdigest() == digest, relative
    with gzip.open(HERE / "exact_matrix.json.gz", "rt") as stream:
        matrix = json.load(stream)
    with gzip.open(BASE / "exact_matrix.json.gz", "rt") as stream:
        baseline = json.load(stream)
    point = json.loads((HERE / "augmented_lp_exact.json").read_text())
    epi = json.loads((HERE / "epigraph_structure.json").read_text())
    zz = json.loads((HERE / "zz_envelope_structure.json").read_text())
    prior_m, prior_n, original_n = len(baseline["rows"]), len(baseline["columns"]), 4849
    assert matrix["columns"][:prior_n] == baseline["columns"]
    assert matrix["row_names"][:prior_m] == baseline["row_names"]
    assert matrix["objective"][:prior_n] == baseline["objective"]
    assert matrix["normalization"][:prior_n] == baseline["normalization"]
    assert all(F(v) == 0 for v in matrix["objective"][prior_n:]+matrix["normalization"][prior_n:])
    strip = lambda col: {k: v for k, v in col.items() if k != "weight"}
    assert [strip(col) for col in point["columns"]] == matrix["columns"]
    rows = [{j: F(v) for j, v in row} for row in matrix["rows"]]
    assert all(len(row) == len(encoded) for row, encoded in zip(rows, matrix["rows"]))
    assert len(rows) == len(matrix["row_names"]) == point["verified_rows"]
    assert len(rows) == matrix["original_rows"]+matrix["appended_unique_rows"]
    for row, expected in zip(rows, baseline["rows"]):
        assert row == {j: F(v) for j, v in expected}
    values = [F(col["weight"]) for col in point["columns"]]
    assert min(values) >= 0
    assert point["positive_columns"] == sum(value > 0 for value in values)
    n = len(values)
    assert n == len(matrix["columns"]) == 15593 and prior_n == 12803 and prior_m == 13931
    hist, groups = {}, defaultdict(dict)
    current_hist = None
    for j, col in enumerate(matrix["columns"][:original_n]):
        if col["kind"] == "hist":
            current_hist = j
            hist[j] = col
        elif col["kind"] == "joint-reply":
            groups[current_hist].setdefault(key(col["group"]), {})[tuple(col["state"])] = j
    assert sha256((HERE / "epigraph_structure.json").read_bytes()).hexdigest() == sha256((BASE / "epigraph_structure.json").read_bytes()).hexdigest()
    for j, i in epi["thresholds"]:
        assert rows[i][j] == 1
        expected = max(F(), -sum((v*values[k] for k, v in rows[i].items() if k < original_n), F()))
        assert values[j] == expected
    pair_columns = {}
    upper_rows = []
    assert [record["column"] for record in zz["auxiliaries"]] == list(range(prior_n, n))
    for offset, record in enumerate(zz["auxiliaries"]):
        j, hi = record["column"], record["hist_column"]
        source, query = key(record["source_group"]), key(record["query_group"])
        pair_columns[hi, source, query] = j
        col = matrix["columns"][j]
        assert col["kind"] == "ZZ-frechet-envelope-upper" and col["hist_column"] == hi
        assert key(col["source_group"]) == source and key(col["query_group"]) == query
        qids, vids = groups[hi][source], groups[hi][query]
        q = {qids[1, 0]: F(1), qids[1, 1]: F(1), j: F(-1)}
        v = {vids[0, 1]: F(1), vids[1, 1]: F(1), j: F(-1)}
        qi, vi = record["q_upper_row"], record["v_upper_row"]
        assert (qi, vi) == (prior_m+2*offset, prior_m+2*offset+1)
        assert rows[qi] == q and rows[vi] == v
        upper_rows.extend([qi, vi])
        assert values[j] == min(values[qids[1, 0]]+values[qids[1, 1]],
                                values[vids[0, 1]]+values[vids[1, 1]])
    assert upper_rows == zz["upper_rows"] and len(upper_rows) == 5580
    expected_budgets = defaultdict(lambda: defaultdict(F))
    incidence_totals = Counter()
    expected_pairs = set()
    edges = [e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2]]
    for hi, col in hist.items():
        words = [word for word, count in zip(product(range(2), repeat=3), col["hist"]) for _ in range(count)]
        group = {e: (e[0], int(e[1] == e[2]), words[e[1]], words[e[2]]) for e in edges}
        counts = Counter()
        for e in edges:
            for f in edges:
                if e == f:
                    continue
                orbit = (e[0], f[0], partition((e[1], e[2], f[1], f[2])))
                counts[orbit, group[e], group[f]] += 1
                expected_pairs.add((hi, group[e], group[f]))
        P = sum(map(int, col["actual_bits"][:4]))
        D = (P+1)*(P+2)
        for (orbit, source, query), count in counts.items():
            incidence_totals[orbit] += count
            qids, vids = groups[hi][source], groups[hi][query]
            row = expected_budgets[orbit]
            for state in ((0, 1), (1, 1)):
                row[qids[state]] += F(count, P+1)
                row[vids[state]] -= F(count, P+1)
            row[qids[1, 1]] -= F(count, D)
            row[pair_columns[hi, source, query]] += F(count, D)
    assert expected_pairs == set(pair_columns) and len(expected_pairs) == 2790
    assert len(expected_budgets) == 39 and sum(incidence_totals.values()) == 68640
    assert zz["budget_rows"] == list(range(prior_m+5580, prior_m+5580+39))
    verified_orbits = set()
    for record in zz["budget_records"]:
        name = record["orbit"]
        orbit = name[0], name[1], tuple(name[2])
        verified_orbits.add(orbit)
        expected = {j: v for j, v in expected_budgets[orbit].items() if v}
        assert rows[record["row"]] == expected
        assert record["literal_pair_hist_terms"] == incidence_totals[orbit]
        assert all(v > 0 for j, v in expected.items() if j >= prior_n)
    assert verified_orbits == set(expected_budgets)
    cut_package = json.loads((RUN / "new_point_separation" / "priority_six_cuts_13931.json").read_text())
    early_records = json.loads((HERE / "early_cut_records.json").read_text())
    sources = {record["name"]: record for record in cut_package["selected_rows"]}
    for record in early_records:
        assert rows[record["row"]] == {j: F(v) for j, v in sources[record["name"]]["coefficients"]}
    assert len(rows) == 19550+sum(record["added"] for record in early_records)
    obj, norm = list(map(F, matrix["objective"])), list(map(F, matrix["normalization"]))
    O = sum((a*b for a, b in zip(norm, values)), F())
    W = sum((a*b for a, b in zip(obj, values)), F())
    assert O == F(point["O"]) == 1 and W == F(point["W"])
    assert 1-2*W == F(point["strict_half_gap"])
    slacks = [sum((coefficient*values[j] for j, coefficient in row.items()), F()) for row in rows]
    assert min(slacks) >= 0 and str(min(slacks)) == point["minimum_slack"]
    dual = json.loads((HERE / "exact_dual_certificate.json").read_text())
    matrix_hash = sha256((HERE / "exact_matrix.json.gz").read_bytes()).hexdigest()
    assert dual["matrix_sha256"] == matrix_hash
    lower = F(dual["normalization_multiplier"])
    residuals = [c-lower*a for c, a in zip(obj, norm)]
    seen_dual_rows = set()
    for i, encoded in dual["row_multipliers"]:
        weight = F(encoded)
        assert weight >= 0 and 0 <= i < len(rows) and i not in seen_dual_rows
        seen_dual_rows.add(i)
        for j, coefficient in rows[i].items():
            residuals[j] -= weight*coefficient
    assert min(residuals) >= 0 and residuals == list(map(F, dual["residuals"]))
    assert lower == W
    old_W = F(json.loads((HERE / "old_point_audit.json").read_text())["W"])
    report = {"scope": "standard-library exact matrix/certificate check, plus independent group-incidence reconstruction of full ZZ extension; not SPE",
              "rows": len(rows), "columns": n, "O": str(O), "W": str(W), "W_float": float(W),
              "below_half": W < F(1, 2), "strict_half_gap": str(1-2*W),
              "input_sha256_verified": True, "unchanged_baseline_rows": prior_m, "unchanged_baseline_columns": prior_n,
              "canonical_max_auxiliaries_verified": len(epi["thresholds"]),
              "canonical_min_auxiliaries_verified": len(pair_columns), "upper_rows_rebuilt": len(upper_rows),
              "orbit_budgets_independently_rebuilt": len(expected_budgets), "early_cuts_verified": len(early_records),
              "exact_primal_verified": True, "minimum_slack": str(min(slacks)),
              "full_ZZ_min_envelope_negative_budgets": sum(slacks[i] < 0 for i in zz["budget_rows"]),
              "full_ZZ_min_envelope_minimum_slack": str(min(slacks[i] for i in zz["budget_rows"])),
              "positive_original_columns": sum(v > 0 for v in values[:original_n]),
              "positive_old_max_auxiliaries": sum(v > 0 for v in values[original_n:prior_n]),
              "positive_new_min_auxiliaries": sum(v > 0 for v in values[prior_n:]),
              "exact_dual_verified": True, "exact_optimum": str(lower),
              "minimum_dual_residual": str(min(residuals)), "positive_dual_rows": len(dual["row_multipliers"]),
              "strictly_above_old_W": lower > old_W, "exact_optimum_increase": str(lower-old_W),
              "matrix_sha256": matrix_hash,
              "point_sha256": sha256((HERE / "augmented_lp_exact.json").read_bytes()).hexdigest(),
              "dual_sha256": sha256((HERE / "exact_dual_certificate.json").read_bytes()).hexdigest(),
              "seconds": time.time()-start}
    (HERE / "certificate_verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
