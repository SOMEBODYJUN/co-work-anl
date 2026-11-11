"""Independent standard-library Fraction verification of the full peer union extension.

Imports no assembly, recovery, numerical-solver, or cut-discovery module.
Reconstructs frozen new full vectors, checks unchanged old rows/descriptors,
every primal row, every dual column, and all canonical max/min auxiliaries.
It certifies this finite necessary system; source proofs supply row validity.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
BASE = RUN / "peer_augmented_lp"
EXPECTED_POINT = "d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f"
EXPECTED_MATRIX = "6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9"
EXPECTED_PEER_MATRIX = "0b4bd0a81097b022a638fdc44324c731768255579a5bf07618e12c35c9342bec"
EXPECTED_PEER_POINT = "63edbafd53493a20ec64ced5f09a694ead3f894bfb6419cde425de0b3a1710c1"
EXPECTED_PEER_DUAL = "2787510b002b927357b49a0a09a64b928ae808fcf8674b1bc41f87e824c75a50"
EXPECTED_PEER_W = Fraction("121493068957403865211086566942389521730338522914685389129175912565358962386745/246609158228421583872999564263448718798282013890815209401160684000599193827791")


def read_matrix(path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def decode(encoded, n):
    result = {}
    for column, value in encoded:
        assert type(column) is int and 0 <= column < n and column not in result
        rational = Fraction(value)
        assert rational
        result[column] = rational
    return result


def dot(row, values):
    total = Fraction(0)
    for column, coefficient in row.items():
        total += coefficient*values[column]
    return total


def oriented_signature(row):
    """Independent canonicalization modulo positive scaling only."""
    if not row:
        return ()
    first = min(row)
    scale = abs(row[first])
    return tuple((j, coefficient/scale) for j, coefficient in sorted(row.items()))


def verify_whole_peer(plan, matrix, rows, values, W):
    paths = {key: RUN/plan["peer_reference"][key]["path"] for key in ("matrix", "point", "dual")}
    expected_hashes = {"matrix":EXPECTED_PEER_MATRIX, "point":EXPECTED_PEER_POINT, "dual":EXPECTED_PEER_DUAL}
    for key, path in paths.items():
        assert sha256(path.read_bytes()).hexdigest() == expected_hashes[key]
        assert plan["peer_reference"][key]["sha256"] == expected_hashes[key]
    peer = read_matrix(paths["matrix"])
    peer_point = json.loads(paths["point"].read_text())
    peer_dual = json.loads(paths["dual"].read_text())
    assert len(peer["columns"]) == peer["column_count"] == 4849
    assert len(peer["rows"]) == peer["row_count"] == 5799
    assert peer["columns"] == matrix["columns"][:4849]
    assert peer["objective"] == matrix["objective"][:4849]
    assert peer["normalization"] == matrix["normalization"][:4849]
    assert all(Fraction(v) == 0 for v in matrix["objective"][4849:] + matrix["normalization"][4849:])
    signatures = {}
    for i, row in enumerate(rows):
        signatures.setdefault(oriented_signature(row), i)
    peer_rows, coverage, missing_from_baseline = [], [], []
    for i, source in enumerate(peer["rows"]):
        assert source["index"] == i
        row = decode(source["nonzero"], 4849)
        signature = oriented_signature(row)
        assert signature in signatures, ("peer row absent from union", i, source["name"])
        target = signatures[signature]
        factor = row[min(row)]/rows[target][min(row)] if row else Fraction(1)
        assert factor > 0
        assert row == {j:factor*coefficient for j,coefficient in rows[target].items()}
        slack = dot(row, values)
        assert slack >= 0 and slack == factor*dot(rows[target], values)
        if target >= 19621:
            missing_from_baseline.append(i)
        peer_rows.append(row)
        coverage.append({"peer_row":i, "peer_name":source["name"], "union_row":target,
                         "peer_equals_union_times":str(factor), "union_point_peer_slack":str(slack)})
    assert len(missing_from_baseline) == 40
    assert all(record["union_row"] < 19621 for record in coverage[:5692])
    assert {record["union_row"] for record in coverage if record["union_row"] >= 19621} == set(range(19621,19661))
    assert len(rows) == 19662
    original_values = [Fraction(c["weight"]) for c in peer_point["columns"]]
    assert [{k:v for k,v in c.items() if k != "weight"} for c in peer_point["columns"]] == peer["columns"]
    assert len(original_values) == 4849 and min(original_values) >= 0
    peer_slacks = [dot(row, original_values) for row in peer_rows]
    assert min(peer_slacks) >= 0
    objective, normalization = list(map(Fraction, peer["objective"])), list(map(Fraction, peer["normalization"]))
    assert sum((a*b for a,b in zip(normalization, original_values)), Fraction(0)) == Fraction(peer_point["O"]) == 1
    peer_W = sum((a*b for a,b in zip(objective, original_values)), Fraction(0))
    assert peer_W == Fraction(peer_point["W"]) == EXPECTED_PEER_W
    assert peer_dual["matrix_sha256"] == EXPECTED_PEER_MATRIX
    assert peer_dual["point_sha256"] == EXPECTED_PEER_POINT
    assert Fraction(peer_dual["normalization_multiplier"]) == peer_W
    peer_residuals = [c-peer_W*a for c,a in zip(objective,normalization)]
    embedded_weights, seen = {}, set()
    for record in peer_dual["row_multipliers"]:
        i, weight = record["row_index"], Fraction(record["weight"])
        assert type(i) is int and 0 <= i < len(peer_rows) and i not in seen and weight > 0
        seen.add(i)
        assert record["row_name"] == peer["rows"][i]["name"]
        assert peer_slacks[i] == 0
        for j, coefficient in peer_rows[i].items():
            peer_residuals[j] -= weight*coefficient
        target, factor = coverage[i]["union_row"], Fraction(coverage[i]["peer_equals_union_times"])
        embedded_weights[target] = embedded_weights.get(target, Fraction(0)) + weight*factor
    assert min(peer_residuals) >= 0
    assert peer_residuals == list(map(Fraction, peer_dual["residuals"]))
    assert sum((a*b for a,b in zip(peer_residuals, original_values)), Fraction(0)) == 0
    union_residuals = [Fraction(c)-peer_W*Fraction(a) for c,a in zip(matrix["objective"], matrix["normalization"])]
    for i, weight in embedded_weights.items():
        for j, coefficient in rows[i].items():
            union_residuals[j] -= weight*coefficient
    assert union_residuals == peer_residuals + [Fraction(0)]*(len(values)-4849)
    assert min(union_residuals) >= 0 and W >= peer_W
    inherited = {"scope":"exact peer5799 dual embedded by positive row scaling into finite union LP",
                 "verified":True, "normalization_multiplier":str(peer_W),
                 "peer_matrix_sha256":EXPECTED_PEER_MATRIX, "peer_point_sha256":EXPECTED_PEER_POINT,
                 "peer_dual_sha256":EXPECTED_PEER_DUAL,
                 "row_multipliers":[[i,str(weight)] for i,weight in sorted(embedded_weights.items())],
                 "residuals":list(map(str,union_residuals)), "gap_to_union_optimum":str(W-peer_W)}
    (HERE/"inherited_peer_dual_lower_bound.json").write_text(json.dumps(inherited,ensure_ascii=False,indent=2)+"\n")
    (HERE/"whole_peer_coverage.json").write_text(json.dumps({"peer_rows":5799,"union_rows":len(rows),
          "missing_from_baseline_peer_indices":missing_from_baseline, "all_rows_covered_by_positive_scaling":True,
          "row_correspondences":coverage},ensure_ascii=False,indent=2)+"\n")
    return {"peer_rows_covered":5799, "peer_descriptors_matched":4849,
            "peer_rows_added":len(missing_from_baseline), "peer_first_5692_rows_in_baseline":True,
            "peer_primal_rows_reverified":5799, "peer_dual_columns_reverified":4849,
            "peer_dual_embedded_union_columns":len(values),
            "peer_exact_optimum":str(peer_W), "peer_optimum_float":float(peer_W),
            "union_at_least_peer_optimum":W >= peer_W, "union_strictly_above_peer_optimum":W > peer_W,
            "exact_difference_from_peer_optimum":str(W-peer_W), "difference_from_peer_optimum_float":float(W-peer_W),
            "whole_peer_coverage_sha256":sha256((HERE/"whole_peer_coverage.json").read_bytes()).hexdigest(),
            "embedded_peer_dual_sha256":sha256((HERE/"inherited_peer_dual_lower_bound.json").read_bytes()).hexdigest()}


def verify_reviewed_reverse(plan, rows, old_values):
    """Bind the added reverse624 row to Main's independently rebuilt source."""
    reference = plan["reverse624_reference"]
    source_path, audit_path, code_path = [RUN/reference[key]["path"] for key in ("source", "audit", "code")]
    for key, path in zip(("source", "audit", "code"), (source_path,audit_path,code_path)):
        assert sha256(path.read_bytes()).hexdigest() == reference[key]["sha256"]
    original = json.loads(source_path.read_text())
    audit = json.loads(audit_path.read_text())
    package = json.loads((RUN/plan["packages"][1]["path"]).read_text())
    assert len(package["selected_rows"]) == 1
    selected = package["selected_rows"][0]
    assert package["main_audit_sha256"] == reference["audit"]["sha256"]
    assert selected["source_package_sha256"] == reference["source"]["sha256"]
    assert audit["source_sha256"] == reference["code"]["sha256"]
    assert audit["package_sha256"] == reference["source"]["sha256"]
    assert audit["point_sha256"] == EXPECTED_POINT
    assert audit["original_columns_checked"] == 4849 and audit["zero_auxiliary_columns_checked"] == 10744
    assert audit["literal_hidden_evaluations"] == 4992 and audit["all_coefficients_equal"] is True
    source = original["cuts"][selected["source_cut_index"]]
    assert (source["i"], source["k"], source["member"], source["orb"]) == (3,3,0,[0,0])
    assert decode(source["sparse_row"],15593) == rows[19661]
    assert dot(rows[19661],old_values) == Fraction(audit["new_exact_slack"]) == Fraction(selected["slack"])
    assert Fraction(source["exact_slack"]) == Fraction(audit["old_exact_slack"]) == Fraction(selected["original_exact_slack"])
    return {"reviewed_reverse624_source_vector_verified":True, "reviewed_reverse624_row":19661,
            "reviewed_reverse624_main_literal_audit_bound":True}


def main():
    start = time.time()
    inputs = json.loads((HERE/"inputs.json").read_text())
    for relative, digest in inputs["sha256"].items():
        assert sha256((RUN/relative).read_bytes()).hexdigest() == digest, relative
    for record in json.loads((HERE/"source_snapshots.json").read_text()):
        assert sha256((RUN/record["source"]).read_bytes()).hexdigest() == record["sha256"]
        assert sha256((HERE/record["snapshot"]).read_bytes()).hexdigest() == record["sha256"]
    for record in json.loads((HERE/"executed_sources.json").read_text()):
        assert sha256((HERE/record["source"]).read_bytes()).hexdigest() == record["sha256"]
        assert sha256((HERE/record["snapshot"]).read_bytes()).hexdigest() == record["sha256"]
    recovery_inputs = json.loads((HERE/"recovery_inputs.json").read_text())
    for filename, digest in recovery_inputs["sha256"].items():
        assert sha256((HERE/filename).read_bytes()).hexdigest() == digest
    assert sha256((BASE/"augmented_lp_exact.json").read_bytes()).hexdigest() == EXPECTED_POINT
    assert sha256((BASE/"exact_matrix.json.gz").read_bytes()).hexdigest() == EXPECTED_MATRIX
    plan = json.loads((HERE/"append_plan.json").read_text())
    assert plan["baseline_point_sha256"] == EXPECTED_POINT
    assert plan["baseline_matrix_sha256"] == EXPECTED_MATRIX
    assert plan["main_whole_peer_scan"] != "awaiting Main confirmation before execution"
    matrix = read_matrix(HERE/"exact_matrix.json.gz")
    baseline = read_matrix(BASE/"exact_matrix.json.gz")
    point = json.loads((HERE/"augmented_lp_exact.json").read_text())
    original_n, n, prior_m = 4849, 15593, 19621
    assert len(baseline["rows"]) == prior_m and len(baseline["columns"]) == n
    assert matrix["columns"] == baseline["columns"]
    assert matrix["row_names"][:prior_m] == baseline["row_names"]
    assert matrix["objective"] == baseline["objective"]
    assert matrix["normalization"] == baseline["normalization"]
    assert matrix["rows"][:prior_m] == baseline["rows"]
    assert len(matrix["rows"]) == len(matrix["row_names"]) == plan["expected_total_rows"]
    assert len(matrix["rows"]) == matrix["original_rows"] + matrix["appended_unique_rows"]
    assert matrix["this_round_added"] == plan["expected_new_distinct_rows"]
    assert [{k:v for k,v in c.items() if k != "weight"} for c in point["columns"]] == matrix["columns"]
    rows = [decode(encoded, n) for encoded in matrix["rows"]]
    old_signatures = {oriented_signature(row) for row in rows[:prior_m]}
    new_signatures = set()
    records = json.loads((HERE/"cut_records.json").read_text())
    assert len(records) == plan["expected_new_distinct_rows"]
    input_point = json.loads((BASE/"augmented_lp_exact.json").read_text())
    old_values = [Fraction(c["weight"]) for c in input_point["columns"]]
    assert [{k:v for k,v in c.items() if k != "weight"} for c in input_point["columns"]] == baseline["columns"]
    assert min(old_values) >= 0 and min(dot(row, old_values) for row in rows[:prior_m]) >= 0
    offset = 0
    input_signs = Counter()
    for package in plan["packages"]:
        path = RUN/package["path"]
        assert sha256(path.read_bytes()).hexdigest() == package["sha256"]
        cuts = json.loads(path.read_text())
        assert cuts.get("point_sha256", cuts.get("source_sha256")) == EXPECTED_POINT
        assert cuts["matrix_sha256"] == EXPECTED_MATRIX
        assert (cuts["baseline_rows"], cuts["columns"], cuts["original_columns"]) == (prior_m, n, original_n)
        assert len(cuts["selected_rows"]) == package["expected_rows"]
        negative_count = 0
        for package_index, source in enumerate(cuts["selected_rows"]):
            record = records[offset]
            i = prior_m + offset
            expected = decode(source["coefficients"], n)
            assert rows[i] == expected and all(j < original_n for j in expected)
            assert record["row"] == i and record["name"] == source["name"]
            assert matrix["row_names"][i] == package["name_prefix"] + source["name"]
            assert record["matrix_row_name"] == matrix["row_names"][i]
            assert record["package"] == package["path"] and record["package_sha256"] == package["sha256"]
            assert record["package_selected_index"] == package_index
            digest = sha256(json.dumps(source["coefficients"], separators=(",", ":")).encode()).hexdigest()
            assert digest == source["vector_sha256"] == record["vector_sha256"]
            sig = oriented_signature(expected)
            assert sig not in old_signatures and sig not in new_signatures
            new_signatures.add(sig)
            value = dot(expected, old_values)
            assert value == Fraction(source["slack"]) == Fraction(record["input_slack"])
            if "exact_slack" in source:
                assert value == Fraction(source["exact_slack"])
            negative_count += value < 0
            input_signs["negative" if value < 0 else "zero" if value == 0 else "positive"] += 1
            offset += 1
        assert negative_count == package["expected_negative_rows"]
    assert offset == len(records) == len(new_signatures)
    values = [Fraction(c["weight"]) for c in point["columns"]]
    assert len(values) == n and min(values) >= 0
    assert point["positive_columns"] == sum(v > 0 for v in values)
    epi = json.loads((HERE/"epigraph_structure.json").read_text())
    zz = json.loads((HERE/"zz_envelope_structure.json").read_text())
    for name in ("epigraph_structure.json", "zz_envelope_structure.json"):
        assert (HERE/name).read_bytes() == (BASE/name).read_bytes()
    assert len(epi["thresholds"]) == 7954 and len(zz["auxiliaries"]) == 2790
    assert {j for j,i in epi["thresholds"]} == set(range(original_n, 12803))
    for j,i in epi["thresholds"]:
        assert rows[i][j] == 1 and all(k < original_n or k == j for k in rows[i])
        expression = sum((v*values[k] for k,v in rows[i].items() if k < original_n), Fraction(0))
        old_expression = sum((v*old_values[k] for k,v in rows[i].items() if k < original_n), Fraction(0))
        assert values[j] == max(Fraction(0), -expression)
        assert old_values[j] == max(Fraction(0), -old_expression)
    assert [r["column"] for r in zz["auxiliaries"]] == list(range(12803, n))
    for r in zz["auxiliaries"]:
        j = r["column"]
        upper, old_upper = [], []
        for i in (r["q_upper_row"], r["v_upper_row"]):
            assert rows[i][j] == -1 and all(k < original_n or k == j for k in rows[i])
            upper.append(sum((v*values[k] for k,v in rows[i].items() if k < original_n), Fraction(0)))
            old_upper.append(sum((v*old_values[k] for k,v in rows[i].items() if k < original_n), Fraction(0)))
        assert values[j] == min(upper)
        assert old_values[j] == min(old_upper)
    objective = list(map(Fraction, matrix["objective"]))
    normalization = list(map(Fraction, matrix["normalization"]))
    assert len(objective) == len(normalization) == n
    assert not any(objective[original_n:] + normalization[original_n:])
    O = sum((a*b for a,b in zip(normalization, values)), Fraction(0))
    W = sum((a*b for a,b in zip(objective, values)), Fraction(0))
    assert O == Fraction(point["O"]) == 1 and W == Fraction(point["W"])
    assert Fraction(point["strict_half_gap"]) == 1-2*W
    assert sum((a*b for a,b in zip(normalization, old_values)), Fraction(0)) == 1
    assert sum((a*b for a,b in zip(objective, old_values)), Fraction(0)) == Fraction(input_point["W"])
    slacks = [dot(row, values) for row in rows]
    assert min(slacks) >= 0 and str(min(slacks)) == point["minimum_slack"]
    assert point["verified_rows"] == len(rows)
    primal_audit = json.loads((HERE/"primal_exact_audit.json").read_text())
    assert slacks == list(map(Fraction, primal_audit["row_slacks"]))
    primal_recovery = primal_audit["recovery"]
    support = primal_recovery["support"]
    assert len(support) == len(set(support)) == primal_recovery["variables"]
    assert primal_recovery["rank"] + len(primal_recovery["free_variables"]) == len(support)
    assert {j for j in range(original_n) if values[j]} <= set(support)
    assert [j for j,v in primal_recovery["free_values"]] == primal_recovery["free_variables"]
    for j,v in primal_recovery["free_values"]:
        assert values[support[j]] == Fraction(v)
    dual = json.loads((HERE/"exact_dual_certificate.json").read_text())
    matrix_hash = sha256((HERE/"exact_matrix.json.gz").read_bytes()).hexdigest()
    assert matrix_hash == dual["matrix_sha256"]
    lower = Fraction(dual["normalization_multiplier"])
    residuals = [c-lower*a for c,a in zip(objective, normalization)]
    multipliers = {}
    complementarity = Fraction(0)
    for i, encoded in dual["row_multipliers"]:
        weight = Fraction(encoded)
        assert type(i) is int and 0 <= i < len(rows) and i not in multipliers and weight > 0
        multipliers[i] = weight
        for j, coefficient in rows[i].items():
            residuals[j] -= weight*coefficient
        complementarity += weight*slacks[i]
    assert min(residuals) >= 0 and residuals == list(map(Fraction, dual["residuals"]))
    assert lower == W and complementarity == 0
    assert sum((a*b for a,b in zip(residuals, values)), Fraction(0)) == 0
    dual_recovery = dual["recovery"]
    if "support_rows" in dual_recovery:
        dual_support = dual_recovery["support_rows"]
        assert len(dual_support) == len(set(dual_support))
        assert set(multipliers) <= set(dual_support)
        assert dual_recovery["variables"] == len(dual_support) + 1
        assert dual_recovery["rank"] + len(dual_recovery["free_variables"]) == dual_recovery["variables"]
        dual_values = [multipliers.get(i, Fraction(0)) for i in dual_support] + [lower]
        assert [j for j,v in dual_recovery["free_values"]] == dual_recovery["free_variables"]
        for j,v in dual_recovery["free_values"]:
            assert dual_values[j] == Fraction(v)
    inherited = json.loads((HERE/"inherited_dual_lower_bound.json").read_text())
    old_certificate = json.loads((BASE/"exact_dual_certificate.json").read_text())
    assert inherited["row_multipliers"] == old_certificate["row_multipliers"]
    assert inherited["source_sha256"] == sha256((BASE/"exact_dual_certificate.json").read_bytes()).hexdigest()
    inherited_lower = Fraction(inherited["normalization_multiplier"])
    inherited_residuals = [c-inherited_lower*a for c,a in zip(objective, normalization)]
    for i, encoded in inherited["row_multipliers"]:
        weight = Fraction(encoded)
        assert weight > 0 and i < prior_m
        for j, coefficient in rows[i].items():
            inherited_residuals[j] -= weight*coefficient
    assert min(inherited_residuals) >= 0
    assert inherited_residuals == list(map(Fraction, inherited["residuals"]))
    assert inherited_lower <= lower
    old_W = Fraction(input_point["W"])
    assert inherited_lower == old_W
    peer_report = verify_whole_peer(plan, matrix, rows, values, W)
    reverse_report = verify_reviewed_reverse(plan, rows, old_values)
    results = [{**record, "exact_slack":str(slacks[record["row"]]),
                "slack_float":float(slacks[record["row"]]),
                "dual_weight":str(multipliers.get(record["row"], Fraction(0))),
                "positive_dual_weight":multipliers.get(record["row"], Fraction(0)) > 0}
               for record in records]
    (HERE/"new_row_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    positive_dual_new_rows = [[r["row"], r["name"], r["dual_weight"]] for r in results if r["positive_dual_weight"]]
    report = {"scope":"independent standard-library all-row/all-column Fraction check of this finite necessary LP only; not SPE or universal bound",
              "rows":len(rows), "columns":n, "O":str(O), "W":str(W), "W_float":float(W),
              "below_half":W < Fraction(1,2), "strict_half_gap":str(1-2*W),
              "input_sha256_verified":True, "executed_source_snapshots_verified":True,
              "unchanged_baseline_rows":prior_m, "unchanged_baseline_columns":n,
              "appended_full_vectors_verified":len(records), "distinct_from_baseline_and_each_other":True,
              "old_point_new_row_signs":dict(input_signs),
              "canonical_max_auxiliaries_verified":7954, "canonical_min_auxiliaries_verified":2790,
              "exact_primal_verified":True, "primal_rows_checked":len(rows), "nonnegative_primal_columns_checked":n,
              "minimum_primal_slack":str(min(slacks)), "positive_original_columns":sum(v > 0 for v in values[:original_n]),
              "positive_max_auxiliaries":sum(v > 0 for v in values[original_n:12803]),
              "positive_min_auxiliaries":sum(v > 0 for v in values[12803:]),
              "primal_support_and_free_values_verified":True,
              "primal_recovery_rank":primal_recovery["rank"], "primal_free_variables":len(primal_recovery["free_variables"]),
              "exact_dual_verified":True, "dual_columns_checked":n, "exact_optimum":str(lower),
              "minimum_dual_residual":str(min(residuals)), "positive_dual_rows":len(multipliers),
              "positive_dual_new_rows":positive_dual_new_rows,
              "dual_support_and_free_values_verified":True,
              "dual_recovery_rank":dual_recovery.get("rank"), "dual_free_variables":len(dual_recovery.get("free_variables", [])),
              "inherited_dual_reverified":True, "exact_complementarity_verified":True,
              "strictly_above_old_W":W > old_W, "exact_optimum_increase":str(W-old_W), "optimum_increase_float":float(W-old_W),
              **peer_report,
              **reverse_report,
              "new_row_slacks":[[r["row"], r["name"], r["exact_slack"]] for r in results],
              "matrix_sha256":matrix_hash, "point_sha256":sha256((HERE/"augmented_lp_exact.json").read_bytes()).hexdigest(),
              "dual_sha256":sha256((HERE/"exact_dual_certificate.json").read_bytes()).hexdigest(),
              "new_row_results_sha256":sha256((HERE/"new_row_results.json").read_bytes()).hexdigest(),
              "verifier_sha256":sha256(Path(__file__).read_bytes()).hexdigest(), "seconds":time.time()-start}
    (HERE/"certificate_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("new_row_slacks", "positive_dual_new_rows")}, indent=2))


if __name__ == "__main__":
    main()
