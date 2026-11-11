"""Independent standard-library Fraction verification of the peer extension.

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
BASE = RUN / "discounted_augmented_lp"
EXPECTED_POINT = "a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505"
EXPECTED_MATRIX = "a95bd72e0fdc2b0b93af79b1a0e8b324b6bd1fc8f62abe8a3ce642be4bcc3936"


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
    assert plan["main_old_frozen_scan"] != "awaiting Main confirmation before execution"
    matrix = read_matrix(HERE/"exact_matrix.json.gz")
    baseline = read_matrix(BASE/"exact_matrix.json.gz")
    point = json.loads((HERE/"augmented_lp_exact.json").read_text())
    original_n, n, prior_m = 4849, 15593, 19578
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
    old_signatures = {tuple(sorted(row.items())) for row in rows[:prior_m]}
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
            sig = tuple(sorted(expected.items()))
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
              "new_row_slacks":[[r["row"], r["name"], r["exact_slack"]] for r in results],
              "matrix_sha256":matrix_hash, "point_sha256":sha256((HERE/"augmented_lp_exact.json").read_bytes()).hexdigest(),
              "dual_sha256":sha256((HERE/"exact_dual_certificate.json").read_bytes()).hexdigest(),
              "new_row_results_sha256":sha256((HERE/"new_row_results.json").read_bytes()).hexdigest(),
              "verifier_sha256":sha256(Path(__file__).read_bytes()).hexdigest(), "seconds":time.time()-start}
    (HERE/"certificate_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("new_row_slacks", "positive_dual_new_rows")}, indent=2))


if __name__ == "__main__":
    main()
