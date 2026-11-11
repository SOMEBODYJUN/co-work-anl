#!/usr/bin/env python3
"""Independent literal arithmetic implementation; no builder import.

Reconstruct the negative of the actual weighted budget columns, enumerate
their full hidden minima, and obtain every candidate coefficient from those
minima. This is an internal independent implementation, not a blind external
mathematical review. No numerical optimizer is imported or called.
"""
from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

P = Path(__file__).resolve().parent
W = P.parent
REPO = W.parents[2]
THETA = Q(5, 12)
TYPES = tuple(product((0, 1), repeat=9))
PURE = tuple(f"A{j}" for j in range(1, 7)) + ("X", "C")
ALL_ROLES = PURE + ("outerOmean",)
SOURCE_HASHES = {
    "main_all_source25_family/proof.md": "abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0",
    "main_source2_maximum_nested_safe/proof.md": "1264073e7d41a827f91031fe07d5b3138245d5590b57b3c393d06326c2986067",
    "main_source2_maximum_nested_safe/build_exact.py": "40f78ff920fdf590363c168a3afbfdd40220c0b0f3f8f36c20afaf99a5bf2dcf",
    "main_source2_maximum_nested_safe/exact_certificate.json": "97694ec0496d52b428fe6a9cfee7030944312709a11de8a67b201bd724e751ac",
    "main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json": "a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba",
    "visible_maximum_joint/exact_input.json": "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33",
    "visible_maximum_joint_solve/exact_certificate.json": "8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347",
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def payoff(bit, total):
    assert total > 0 or bit == 0
    return Q(bit, total) if total else Q(0)


def direct_cost(i, p, t, tail, menu, theta=THETA):
    """Negative of the sum of actual IC/CAP/BR/SAFE customer columns."""
    assert len(tail) == 6 - i and len(menu) == 6
    slots = {j: tail[j - i - 1] for j in range(i + 1, 7)}
    total = p + t + sum(slots.values())
    prefix5 = p + t + sum(slots[j] for j in range(i + 1, 5))
    prefix6 = prefix5 + slots[5]
    budget = -25 * payoff(t, total)
    for j in range(i + 1, 6):
        budget -= Q(slots[j], 2)
    budget -= slots[6]
    # Each index is literally queried at each true node.
    budget += sum((payoff(slots[6], total) - Q(menu[j], prefix6 + 1)
                   for j in range(6)), Q(0)) / 6
    budget += theta * sum((payoff(slots[5], total) - Q(menu[j], prefix5 + 2)
                           for j in range(6)), Q(0)) / 6
    return -budget


def literal_minimum_formula(i, p, t, o):
    n, D = 6 - i, p + 7 - i
    if t == 0:
        return Q(o, 6 * (p + 1)) + Q(5 * o, 72 * (p + 2))
    # Independently evaluate the proved attaining physical tail; do not
    # copy the builder's m_i expression to generate the matrix.
    z = int(p + n < 5)
    L = p + n + z
    return Q(25 - z, L) - THETA / L + Q(n - 1, 2) + z + (1 + THETA) * Q(o, 6 * D)


def dense(row):
    assert set(row["a"]) <= {str(j) for j in range(513)}
    return tuple(Q(row["a"].get(str(j), "0")) for j in range(513))


def membership(bits, role):
    if role in PURE[:6]:
        return bits[PURE.index(role)]
    assert role in ("X", "C")
    return bits[6] if role == "X" else bits[8]


def exact_dot(row, point):
    return sum((a * b for a, b in zip(row, point) if a and b), Q(0))


def read_jsonlines(name):
    with gzip.open(P / name, "rt", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def exhausted(iterator):
    try:
        next(iterator)
    except StopIteration:
        return
    raise AssertionError("Unexpected extra literal record")


def main():
    for name, expected in SOURCE_HASHES.items():
        assert sha(W / name) == expected, name
    pins = read(P / "source_pins.json")
    for name, expected in pins["sources"].items():
        assert sha(REPO / name) == expected, name
    assert sha(REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md") == "cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88"
    assert pins["excluded_unfrozen_1003"] is True

    state_rows = read(P / "hidden_state_checks.json")["states"]
    minimum_rows = read(P / "minimum_table.json")["minima"]
    assert len(state_rows) == 416 and len(minimum_rows) == 40
    k, mpos = 0, 0
    minima, minima0, minimizing_tails = {}, {}, {}
    for i in range(1, 5):
        for p, t, o in product(range(i), (0, 1), (0, 1)):
            menu = (o, 0, 0, 0, 0, 0)
            costs, base_costs, tails_list = [], [], []
            for tail in product((0, 1), repeat=6 - i):
                base = direct_cost(i, p, t, tail, menu, Q(0))
                value = direct_cost(i, p, t, tail, menu)
                slope = (value - base) / THETA
                record = state_rows[k]
                assert (record["source"], record["p"], record["t"], record["o"], tuple(record["tail"])) == (i, p, t, o, tail)
                assert record["tail_slots"] == list(range(i + 1, 7))
                assert Q(record["base_P25_cost"]) == base
                assert Q(record["internal5_increment"]) == slope
                assert Q(record["cost"]) == value
                target = literal_minimum_formula(i, p, t, o)
                assert Q(record["minimum"]) == target
                assert Q(record["residual"]) == value - target >= 0
                costs.append(value);base_costs.append(base);tails_list.append(tail)
                k += 1
            key = i, p, t, o
            minima[key], minima0[key] = min(costs), min(base_costs)
            assert minima[key] == literal_minimum_formula(i, p, t, o)
            minimizing_tails[key] = [list(tail) for tail, v in zip(tails_list, costs) if v == minima[key]]
            record = minimum_rows[mpos]
            assert (record["source"], record["p"], record["t"], record["o"]) == key
            assert Q(record["minimum"]) == minima[key]
            assert Q(record["base_minimum"]) == minima0[key]
            assert Q(record["theta_slope"]) == (minima[key] - minima0[key]) / THETA
            assert record["minimizing_tails"] == minimizing_tails[key]
            mpos += 1
    assert (k, mpos) == (416, 40)

    ep = read(P / "affine_endpoint_checks.json")
    assert ep["valid_theta_interval"] == ["0", "5/12"]
    for r in ep["critical_witnesses"]:
        i, p, t, o, tail = r["source"], r["p"], r["t"], r["o"], r["tail"]
        assert (p, t, o) == (0, 0, 1)
        assert tail[-2:] == [1, 0] and all(x == 0 for x in tail[:-2])
        assert Q(r["ceiling"]) == THETA
        too_large = Q(1, 2)
        value = direct_cost(i, p, t, tail, (1, 0, 0, 0, 0, 0), too_large)
        wrong_affine = minima0[i, p, t, o] + too_large * (minima[i, p, t, o] - minima0[i, p, t, o]) / THETA
        assert value - wrong_affine == -Q(1, 12)
    assert len(ep["critical_witnesses"]) == 4
    for r in ep["wrong_unclamped_H_failures"]:
        i, p, o, tail = r["source"], r["p"], r["o"], r["tail"]
        assert p == i - 1 and tail[-1] == 0 and all(v == 1 for v in tail[:-1])
        actual = direct_cost(i, p, 1, tail, (o, 0, 0, 0, 0, 0))
        assert Q(r["actual"]) == actual
        assert actual - Q(r["wrong_H_equals_t_over_D_minimum"]) == Q(r["negative_residual"]) == -Q(1, 72)
    assert len(ep["wrong_unclamped_H_failures"]) == 8

    inner_stream = iter(read_jsonlines("literal_inner_six_index.jsonl.gz"))
    inner_checks = 0
    for i in range(1, 5):
        for p, t in product(range(i), (0, 1)):
            for tail in product((0, 1), repeat=6 - i):
                for menu in product((0, 1), repeat=6):
                    r = next(inner_stream)
                    d, o = sum(menu), int(any(menu))
                    assert (r["source"], r["p"], r["t"], tuple(r["tail"]), tuple(r["menu"])) == (i, p, t, tail, menu)
                    exact = direct_cost(i, p, t, tail, menu)
                    projected = direct_cost(i, p, t, tail, (o, 0, 0, 0, 0, 0))
                    assert (r["d"], r["o"]) == (d, o)
                    assert Q(r["literal"]) == exact
                    assert Q(r["union_projected"]) == projected
                    assert Q(r["residual"]) == exact - projected >= 0
                    inner_checks += 1
    exhausted(inner_stream)
    assert inner_checks == 13312

    outer_stream = iter(read_jsonlines("literal_outer_same_six_index.jsonl.gz"))
    av = read(P / "outer_average_checks.json")
    outer_checks, avg_checks, observed_slopes = 0, 0, []
    for i in range(1, 5):
        for p in range(i):
            for o in (0, 1):
                difference = minima[i, p, 1, o] - minima[i, p, 0, o]
                observed_slopes.append(difference)
                assert difference >= Q(743, 144) > 0
            for menu in product((0, 1), repeat=6):
                d, o = sum(menu), int(any(menu))
                lower = [minima[i, p, menu[k], o] for k in range(6)]
                average = sum(lower, Q(0)) / 6
                m0, m1 = minima[i, p, 0, o], minima[i, p, 1, o]
                weak = m0 + Q(o, 6) * (m1 - m0)
                r = av["averages"][avg_checks]
                assert (r["source"], r["p"], tuple(r["menu"])) == (i, p, menu)
                assert list(map(Q, r["six_lower_costs"])) == lower
                assert Q(r["exact_outer_average"]) == average == m0 + Q(d, 6) * (m1 - m0)
                assert Q(r["union_outer_cost"]) == weak
                assert Q(r["residual"]) == average - weak >= 0
                if o == 0:
                    assert lower == [Q(0)] * 6
                for k in range(6):
                    for tail in product((0, 1), repeat=6 - i):
                        r = next(outer_stream)
                        assert (r["source"], r["p"], tuple(r["menu"]), r["outer_index"], tuple(r["tail"])) == (i, p, menu, k, tail)
                        assert r["t"] == menu[k] and r["o"] == o
                        value = direct_cost(i, p, menu[k], tail, menu)
                        assert Q(r["literal_inner_average"]) == value
                        assert Q(r["one_outer_index_lower_cost"]) == lower[k]
                        assert Q(r["residual"]) == value - lower[k] >= 0
                        outer_checks += 1
                avg_checks += 1
    exhausted(outer_stream)
    assert (outer_checks, avg_checks) == (39936, 640)
    assert min(observed_slopes) == Q(av["minimum_m1_minus_m0"]) == Q(2333, 432)
    assert len(av["averages"]) == 640 and len(av["positive_slope_cases"]) == 20

    fam = read(P / "exact_family.json")
    base = read(W / "visible_maximum_joint/exact_input.json")
    assert fam["status"] == "PREPARED_NO_OPTIMIZER" and fam["optimizer_calls"] == 0
    assert fam["variables"] == 513 and fam["K_column"] == 512
    assert fam["atom_columns"] == base["atom_columns"]
    assert fam["bit_order"] == [f"a{j}" for j in range(1, 7)] + ["x", "o", "c"]
    assert fam["nonnegative_columns"] == list(range(513))
    assert fam["normalization_required"] is False and fam["requires_OPT_union"] is False
    assert fam["added_to_any_LP"] is False and fam["not_a_solver_input"] is True
    assert fam["proof_sha256"] == sha(P / "proof.md")
    assert fam["source_review_sha256"] == sha(P / "source_review.md")
    assert fam["source_pins_sha256"] == sha(P / "source_pins.json")
    assert len(fam["rows"]) == fam["row_count"] == 36
    reconstructed, by_name = {}, {r["name"]: r for r in fam["rows"]}
    for index, (i, role) in enumerate(product(range(1, 5), ALL_ROLES)):
        row = fam["rows"][index]
        assert (row["name"], row["source"], row["T"]) == (f"NESTED_SAFE5_i{i}_T{role}", i, role)
        assert Q(row["theta"]) == THETA and Q(row["rhs"]) == 0 and Q(row["numerical_divisor"]) == 25
        values = []
        for bits in TYPES:
            p, o = sum(bits[:i - 1]), bits[7]
            if role == "outerOmean":
                # Literal six outer indices at the union-floor vector.
                bound = sum((minima[i, p, q, o] for q in (o, 0, 0, 0, 0, 0)), Q(0)) / 6
            else:
                bound = minima[i, p, membership(bits, role), o]
            values.append(25 * payoff(bits[i - 1], sum(bits[:6])) - bound)
        values.append(sum([Q(1, 2)] * (5 - i), Q(1)))
        expected = tuple(values)
        assert dense(row) == expected, row["name"]
        assert set(row["a"]) == {str(j) for j in range(513)}
        reconstructed[row["name"]] = expected
    assert len(reconstructed) == 36

    EC = tuple(Q(bits[8]) for bits in TYPES) + (Q(-1),)
    ccheck = read(P / "C_equality_comparisons.json")
    assert dense(ccheck["C_equality"]) == EC
    for r in ccheck["specializations"]:
        i = r["source"];mult = Q(7 - i, 2)
        assert Q(r["free_equality_multiplier"]) == mult
        expected = tuple(a + mult * b for a, b in zip(reconstructed[r["raw_row"]], EC))
        assert dense(r) == expected and expected[-1] == 0
    mainrow = read(W / "main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json")
    assert dense(mainrow) == tuple(12 * a + 29 * b for a, b in zip(reconstructed["NESTED_SAFE5_i2_TC"], EC))
    assert all(Q(v) == 0 for v in ccheck["Main_NS5_all_513_column_residuals"].values())

    old_rows = {r["name"]: r for r in base["raw_rows"]}
    catalog = read(P / "row_catalog.json")
    comparisons = read(P / "old_P25_comparisons.json")
    expected_deltas = {1: [Q(1, 162)], 2: [Q(7, 1440), Q(5, 2592)],
                       3: [Q(11, 1728), Q(1, 1620), Q(11, 5184)],
                       4: [Q(23, 2592), Q(11, 5184), Q(7, 8640), Q(7, 2592)]}
    for r in comparisons["outer_delta_table"]:
        assert Q(r["delta"]) == expected_deltas[r["source"]][r["p"]] > 0
    assert len(catalog["rows"]) == len(comparisons["row_comparisons"]) == 36
    for index, (record, comp) in enumerate(zip(catalog["rows"], comparisons["row_comparisons"])):
        i, role = record["source"], record["T"]
        assert record["row_index"] == index and record["name"] == fam["rows"][index]["name"]
        assert record["dominated_by_old_P25_30"] == (role == "outerOmean")
        assert record["equivalent_to_Main_NS5_modulo_C_equality"] == (i == 2 and role == "C")
        assert record["strict_increment_or_cone_independence_claimed"] is False
        new, old = reconstructed[record["name"]], dense(old_rows[record["old_P25_comparison_row"]])
        difference = tuple(a - b for a, b in zip(new, old))
        assert tuple(Q(comp["difference_a"][str(j)]) for j in range(513)) == difference
        for j, bits in enumerate(TYPES):
            p, o = sum(bits[:i - 1]), bits[7]
            if role == "outerOmean":
                expected = o * expected_deltas[i][p]
            else:
                t, D = membership(bits, role), p + 7 - i
                expected = THETA * (Q(t, min(D, 5)) - Q(o, 6 * (p + (5 - i) * t + 2)))
            assert difference[j] == expected
        assert difference[-1] == 0

    point_cert = read(W / "visible_maximum_joint_solve/exact_certificate.json")
    point = tuple(map(Q, point_cert["primal"]))
    assert len(point) == 513 and all(v >= 0 for v in point)
    for r in base["raw_rows"]:
        assert exact_dot(dense(r), point) >= Q(r["rhs"])
    for r in base["equalities"]:
        assert exact_dot(dense(r), point) == Q(r["rhs"])
    diag = read(P / "frozen_1002_point_diagnostics.json")
    negatives = []
    for r in diag["all_new_slacks"]:
        value = exact_dot(reconstructed[r["row"]], point)
        assert Q(r["exact_slack"]) == value
        assert r["negative"] == (value < 0)
        old_value = exact_dot(dense(old_rows[r["old_P25_row"]]), point)
        assert Q(r["old_P25_exact_slack"]) == old_value
        assert Q(r["new_minus_old_slack"]) == value - old_value
        if value < 0:
            negatives.append(r)
    assert {(r["source"], r["T"]) for r in negatives} == {(2, "A4"), (2, "C")}
    assert diag["negative_count"] == 2
    assert exact_dot(dense(mainrow), point) == 12 * exact_dot(reconstructed["NESTED_SAFE5_i2_TC"], point)
    for name, expected in pins["sources"].items():
        assert sha(REPO / name) == expected, name

    result = {"status": "PREPARED_NO_OPTIMIZER", "result": "PASS_INTERNAL_INDEPENDENT_LITERAL_CHECK",
              "family_sha256": sha(P / "exact_family.json"), "proof_sha256": sha(P / "proof.md"),
              "checker_sha256": sha(Path(__file__)), "optimizer_calls": 0, "builder_imported": False,
              "external_blind_review_claimed": False, "candidate_rows": 36, "columns": 513,
              "matrix_coefficients_checked": 18468, "literal_hidden_states": 416, "exact_minimum_types": 40,
              "literal_inner_menu_states": inner_checks, "literal_same_list_outer_states": outer_checks,
              "outer_average_cases": avg_checks, "outer_delta_cases": 10, "outer_rows_dominated": 4,
              "C_specialization_columns": 2052, "Main_NS5_identity_columns": 513,
              "old_P25_comparison_columns": 18468, "baseline_point_rows_verified": 1002,
              "baseline_point_equalities_verified": 2, "negative_old_point_rows": negatives,
              "minimum_outer_m1_minus_m0": "2333/432", "theta_endpoint": "5/12",
              "wrong_unclamped_H_counterexamples": 8, "source_files_unchanged": len(pins["sources"]),
              "added_to_any_LP": False, "half_status": "OPEN"}
    (P / "literal_check_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
