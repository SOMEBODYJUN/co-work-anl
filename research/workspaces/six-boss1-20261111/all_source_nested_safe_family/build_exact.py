#!/usr/bin/env python3
"""Exact all-source P25 + internal-fifth SAFE family, zero optimization.

Only this new package is written. All source packages and the frozen 1002
point are read-only; no 1003 artifact is read or bound.
"""
from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = WS.parents[2]
THETA = F(5, 12)
STATUS = "PREPARED_NO_OPTIMIZER"
ATOMS = tuple(product((0, 1), repeat=9))
PURE = tuple(f"A{i}" for i in range(1, 7)) + ("X", "C")
ROLES = PURE + ("outerOmean",)
EXPECTED = {
    "main_all_source25_family/proof.md": "abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0",
    "main_source2_maximum_nested_safe/proof.md": "1264073e7d41a827f91031fe07d5b3138245d5590b57b3c393d06326c2986067",
    "main_source2_maximum_nested_safe/build_exact.py": "40f78ff920fdf590363c168a3afbfdd40220c0b0f3f8f36c20afaf99a5bf2dcf",
    "main_source2_maximum_nested_safe/exact_certificate.json": "97694ec0496d52b428fe6a9cfee7030944312709a11de8a67b201bd724e751ac",
    "main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json": "a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba",
    "visible_maximum_joint/exact_input.json": "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33",
    "visible_maximum_joint_solve/exact_certificate.json": "8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347",
}
MODEL = "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md"
MODEL_SHA = "cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88"


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(name, value):
    path = HERE / name
    assert path.parent == HERE
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def share(bit, load_value):
    assert load_value or not bit
    return F(bit, load_value) if load_value else F(0)


def minimum(source, prefix, t, o, theta=THETA):
    n = 6 - source
    D = prefix + n + 1
    return (F(n + 1, 2) * t + F(24 * t, D)
            + F(o, 6 * (prefix + 1 + n * t))
            + theta * (F(o, 6 * (prefix + (5 - source) * t + 2))
                       - F(t, min(D, 5))))


def hidden_cost(source, prefix, t, o, tails):
    """Assemble the separate true-budget shares, not only a closed numerator."""
    assert len(tails) == 6 - source
    L = prefix + t + sum(tails)
    vi, v5, v6 = share(t, L), share(tails[-2], L), share(tails[-1], L)
    D6 = prefix + t + sum(tails[:-1]) + 1
    D5 = prefix + t + sum(tails[:-2]) + 2
    sizes = F(sum(tails[:-1]), 2) + tails[-1]
    base = 25 * vi - v6 + sizes + F(o, 6 * D6)
    fifth = F(o, 6 * D5) - v5
    return base, fifth, base + THETA * fifth


def literal_menu_cost(source, prefix, t, menu, tails):
    L = prefix + t + sum(tails)
    D6 = prefix + t + sum(tails[:-1]) + 1
    D5 = prefix + t + sum(tails[:-2]) + 2
    literal = 25 * share(t, L) - share(tails[-1], L)
    literal -= THETA * share(tails[-2], L)
    literal += F(sum(tails[:-1]), 2) + tails[-1]
    literal += sum((F(q, D6) for q in menu), F(0)) / 6
    literal += THETA * sum((F(q, D5) for q in menu), F(0)) / 6
    return literal


def member(bits, role):
    if role.startswith("A"):
        return bits[int(role[1:]) - 1]
    if role == "X":
        return bits[6]
    if role == "C":
        return bits[8]
    raise ValueError("An outer mean is six actual legal indices, not a membership bit")


def cost_for_role(bits, source, role):
    p, o = sum(bits[:source - 1]), bits[7]
    if role != "outerOmean":
        return minimum(source, p, member(bits, role), o)
    m0, m1 = minimum(source, p, 0, o), minimum(source, p, 1, o)
    return m0 + F(o, 6) * (m1 - m0)


def dense(row):
    return [F(row["a"].get(str(j), "0")) for j in range(513)]


def encode(vec):
    return {str(j): str(v) for j, v in enumerate(vec)}


def dot(vec, point):
    return sum((a * b for a, b in zip(vec, point) if a and b), F(0))


def jsonl_record(out, record):
    out.write((json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n").encode())


def main():
    assert not (HERE / "freeze_manifest.json").exists(), "Preserve the frozen symbolic package."
    pins = {}
    for relative, expected in EXPECTED.items():
        assert sha(WS / relative) == expected, relative
        pins[str((WS / relative).relative_to(ROOT))] = expected
    assert sha(ROOT / MODEL) == MODEL_SHA
    pins[MODEL] = MODEL_SHA
    save("source_pins.json", {"status": STATUS, "sources": pins, "excluded_unfrozen_1003": True})

    states, minima, thresholds, unclamped_failures = [], [], [], []
    for i in range(1, 5):
        n = 6 - i
        for p, t, o in product(range(i), (0, 1), (0, 1)):
            expected, base_expected = minimum(i, p, t, o), minimum(i, p, t, o, F(0))
            expected_slope = (expected - base_expected) / THETA
            values, zeros = [], []
            for tails in product((0, 1), repeat=n):
                base, fifth, value = hidden_cost(i, p, t, o, tails)
                assert base >= base_expected and value >= expected
                residual = value - expected
                states.append({"source": i, "p": p, "t": t, "o": o,
                               "tail_slots": list(range(i + 1, 7)), "tail": list(tails),
                               "base_P25_cost": str(base), "internal5_increment": str(fifth),
                               "cost": str(value), "minimum": str(expected), "residual": str(residual)})
                values.append(value)
                if residual == 0:
                    zeros.append(list(tails))
                if fifth < expected_slope:
                    ceiling = (base - base_expected) / (expected_slope - fifth)
                    assert ceiling >= THETA
                    thresholds.append({"source": i, "p": p, "t": t, "o": o, "tail": list(tails), "ceiling": str(ceiling)})
            assert min(values) == expected
            minima.append({"source": i, "p": p, "t": t, "o": o,
                           "minimum": str(expected), "base_minimum": str(base_expected),
                           "theta_slope": str(expected_slope), "minimizing_tails": zeros})
        for o in (0, 1):
            p, t, tails = i - 1, 1, (1,) * (n - 1) + (0,)
            correct = minimum(i, p, t, o)
            wrong = correct + THETA * (F(1, 5) - F(1, 6))
            actual = hidden_cost(i, p, t, o, tails)[2]
            assert actual == correct and actual - wrong == -F(1, 72)
            unclamped_failures.append({"source": i, "p": p, "t": t, "o": o,
                                       "tail": list(tails), "actual": str(actual),
                                       "wrong_H_equals_t_over_D_minimum": str(wrong),
                                       "negative_residual": str(actual - wrong)})
    assert len(states) == 416 and len(minima) == 40
    assert min(F(r["ceiling"]) for r in thresholds) == THETA
    critical = [r for r in thresholds if F(r["ceiling"]) == THETA]
    assert len(critical) == 4
    save("hidden_state_checks.json", {"status": "PASS", "count": len(states), "states": states})
    save("minimum_table.json", {"status": "PASS", "count": len(minima), "minima": minima})
    save("affine_endpoint_checks.json", {"status": "PASS", "valid_theta_interval": ["0", str(THETA)],
         "critical_witnesses": critical, "full_upper_bound_ratios": thresholds,
         "wrong_unclamped_H_failures": unclamped_failures,
         "interpretation": "Exact endpoint for this fixed affine formula only; not an optimization of all real budgets."})

    inner_count, outer_local_count, outer_averages, slope_values = 0, 0, [], []
    with (HERE / "literal_inner_six_index.jsonl.gz").open("wb") as handle:
        with gzip.GzipFile(filename="", mode="wb", fileobj=handle, mtime=0) as out:
            for i in range(1, 5):
                for p, t in product(range(i), (0, 1)):
                    for tails in product((0, 1), repeat=6 - i):
                        D6, D5 = p + t + sum(tails[:-1]) + 1, p + t + sum(tails[:-2]) + 2
                        for menu in product((0, 1), repeat=6):
                            d, o = sum(menu), int(any(menu))
                            actual = literal_menu_cost(i, p, t, menu, tails)
                            projected = hidden_cost(i, p, t, o, tails)[2]
                            difference = F(d - o, 6) * (F(1, D6) + THETA * F(1, D5))
                            assert actual - projected == difference >= 0
                            jsonl_record(out, {"source": i, "p": p, "t": t, "tail": list(tails),
                                "menu": list(menu), "d": d, "o": o, "literal": str(actual),
                                "union_projected": str(projected), "residual": str(difference)})
                            inner_count += 1
    with (HERE / "literal_outer_same_six_index.jsonl.gz").open("wb") as handle:
        with gzip.GzipFile(filename="", mode="wb", fileobj=handle, mtime=0) as out:
            for i in range(1, 5):
                for p in range(i):
                    for o in (0, 1):
                        diff = minimum(i, p, 1, o) - minimum(i, p, 0, o)
                        assert diff >= F(743, 144) > 0
                        slope_values.append({"source": i, "p": p, "o": o, "m1_minus_m0": str(diff)})
                    for menu in product((0, 1), repeat=6):
                        d, o = sum(menu), int(any(menu))
                        m0, m1 = minimum(i, p, 0, o), minimum(i, p, 1, o)
                        min_by_index = [minimum(i, p, menu[k], o) for k in range(6)]
                        exact = sum(min_by_index, F(0)) / 6
                        weak = m0 + F(o, 6) * (m1 - m0)
                        assert exact == m0 + F(d, 6) * (m1 - m0)
                        assert exact - weak == F(d - o, 6) * (m1 - m0) >= 0
                        if o == 0:
                            assert menu == (0,) * 6 and exact == weak == m0 == 0
                        outer_averages.append({"source": i, "p": p, "menu": list(menu), "d": d,
                            "o": o, "six_lower_costs": list(map(str, min_by_index)),
                            "exact_outer_average": str(exact), "union_outer_cost": str(weak),
                            "residual": str(exact - weak)})
                        for k in range(6):
                            for tails in product((0, 1), repeat=6 - i):
                                actual = literal_menu_cost(i, p, menu[k], menu, tails)
                                target = min_by_index[k]
                                assert actual >= target
                                jsonl_record(out, {"source": i, "p": p, "menu": list(menu), "outer_index": k,
                                    "t": menu[k], "o": o, "tail": list(tails), "literal_inner_average": str(actual),
                                    "one_outer_index_lower_cost": str(target), "residual": str(actual - target)})
                                outer_local_count += 1
    assert inner_count == 13312 and outer_local_count == 39936 and len(outer_averages) == 640
    smallest = min(F(r["m1_minus_m0"]) for r in slope_values)
    assert smallest == F(2333, 432)
    save("outer_average_checks.json", {"status": "PASS", "same_six_query_list": True,
         "positive_slope_cases": slope_values, "minimum_m1_minus_m0": str(smallest),
         "outer_average_count": len(outer_averages), "averages": outer_averages,
         "inner_literal_count": inner_count, "outer_local_literal_count": outer_local_count})

    baseline = load(WS / "visible_maximum_joint/exact_input.json")
    old_rows = {r["name"]: r for r in baseline["raw_rows"]}
    assert baseline["variables"] == 513 and len(baseline["raw_rows"]) == 1002
    assert len(baseline["atom_columns"]) == 512
    for j, bits in enumerate(ATOMS):
        a = baseline["atom_columns"][j]
        assert tuple(a["a"]) + (a["x"], a["o"], a["c"]) == bits
    family, catalog = [], []
    for i in range(1, 5):
        for role in ROLES:
            vals = [25 * share(t[i - 1], sum(t[:6])) - cost_for_role(t, i, role) for t in ATOMS]
            vals.append(F(7 - i, 2))
            name = f"NESTED_SAFE5_i{i}_T{role}"
            row = {"name": name, "family": "ALL_SOURCE_NESTED_SAFE5", "source": i,
                   "T": role, "theta": str(THETA), "a": encode(vals), "rhs": "0", "numerical_divisor": "25"}
            family.append(row)
            old_name = (f"PORTFOLIO25_i{i}_T8_Q8" if role == "outerOmean" else
                        f"PORTFOLIO25_i{i}_TC_QOmean" if role == "C" else
                        f"PORTFOLIO25_i{i}_T{7 if role == 'X' else int(role[1:])}_Q8")
            assert old_name in old_rows
            catalog.append({"row_index": len(family) - 1, "name": name, "source": i, "T": role,
                "old_P25_comparison_row": old_name,
                "dominated_by_old_P25_30": role == "outerOmean",
                "equivalent_to_Main_NS5_modulo_C_equality": i == 2 and role == "C",
                "strict_increment_or_cone_independence_claimed": False,
                "numerical_divisor": "25"})
    assert len(family) == 36 and all(len(r["a"]) == 513 for r in family)
    save("exact_family.json", {"schema": "all_source_nested_safe5_exact_family_v1", "status": STATUS,
         "theorem_status": "PROVED_NECESSARY_FAMILY", "optimizer_calls": 0,
         "scope": "Actual sources 1..4, any legal forced T, same-branch true internal source5 SAFE; any six legal query union.",
         "theta": str(THETA), "variables": 513, "K_column": 512,
         "bit_order": baseline["bit_order"], "atom_columns": baseline["atom_columns"],
         "nonnegative_columns": list(range(513)), "inequality_convention": "a dot z >= rhs",
         "row_count": 36, "rows": family, "not_a_solver_input": True,
         "normalization_required": False, "requires_OPT_union": False,
         "proof_sha256": sha(HERE / "proof.md"), "source_review_sha256": sha(HERE / "source_review.md"),
         "source_pins_sha256": sha(HERE / "source_pins.json"),
         "added_to_any_LP": False, "half_status": "OPEN"})
    save("row_catalog.json", {"status": STATUS, "rows": catalog, "raw_count": 36,
         "pure_role_rows": 32, "outer_mean_dominated_rows": 4,
         "already_proved_C2_equivalent_rows": 1, "new_cone_independence_claimed": False})

    by_name = {r["name"]: r for r in family}
    EC = [F(t[8]) for t in ATOMS] + [F(-1)]
    specialized = []
    for i in range(1, 5):
        raw = dense(by_name[f"NESTED_SAFE5_i{i}_TC"])
        ci = F(7 - i, 2)
        simplified = [r + ci * e for r, e in zip(raw, EC)]
        direct = []
        for t in ATOMS:
            p, c, o, n = sum(t[:i - 1]), t[8], t[7], 6 - i
            D = p + n + 1
            B, M, N, H = F(c, D), F(o, 6 * (p + 1 + n * c)), F(o, 6 * (p + (5 - i) * c + 2)), F(c, min(D, 5))
            direct.append(25 * share(t[i - 1], sum(t[:6])) - 24 * B - M - THETA * N + THETA * H)
        direct.append(F(0))
        assert simplified == direct
        specialized.append({"source": i, "raw_row": f"NESTED_SAFE5_i{i}_TC",
                            "free_equality_multiplier": str(ci), "a": encode(simplified), "rhs": "0"})
    main_NS = load(WS / "main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json")
    raw2 = dense(by_name["NESTED_SAFE5_i2_TC"])
    main_residuals = [v - 12 * r - 29 * e for v, r, e in zip(dense(main_NS), raw2, EC)]
    assert all(v == 0 for v in main_residuals)
    save("C_equality_comparisons.json", {"status": "PASS", "C_equality": {"a": encode(EC), "rhs": "0"},
         "specializations": specialized, "Main_NS5_identity": "Main_NS5 = 12*R_i2_C + 29*(sum(c*z)-K)",
         "Main_NS5_row_sha256": EXPECTED["main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json"],
         "Main_NS5_all_513_column_residuals": encode(main_residuals),
         "specialized_rows_are_comparisons_only_not_extra_family_rows": True})

    comparisons, deltas = [], []
    for i in range(1, 5):
        for p in range(i):
            n, D = 6 - i, p + 7 - i
            delta = F(n, 36 * (p + 1) * D) - THETA * (F(5, 36 * (p + 2)) + F(1, 36 * D) - F(1, 6 * min(D, 5)))
            assert delta > 0
            deltas.append({"source": i, "p": p, "delta": str(delta)})
    for rec in catalog:
        new = dense(by_name[rec["name"]]);old = dense(old_rows[rec["old_P25_comparison_row"]])
        i, role = rec["source"], rec["T"]
        diff, expected = [a - b for a, b in zip(new, old)], []
        for t in ATOMS:
            p, o, n = sum(t[:i - 1]), t[7], 6 - i
            D = p + n + 1
            if role == "outerOmean":
                delta = next(F(d["delta"]) for d in deltas if d["source"] == i and d["p"] == p)
                expected.append(o * delta)
            else:
                bit = member(t, role)
                expected.append(THETA * (F(bit, min(D, 5)) - F(o, 6 * (p + (5 - i) * bit + 2))))
        expected.append(F(0))
        assert diff == expected
        comparisons.append({"new_row": rec["name"], "old_row": rec["old_P25_comparison_row"],
            "difference_a": encode(diff), "all_difference_coefficients_nonnegative": all(v >= 0 for v in diff),
            "outermean_strictly_dominated_on_O_positive": role == "outerOmean"})
    save("old_P25_comparisons.json", {"status": "PASS", "all_36_times_513_columns_checked": 18468,
         "outer_delta_table": deltas, "row_comparisons": comparisons,
         "pure_rows_cone_independence_claimed": False})

    cert = load(WS / "visible_maximum_joint_solve/exact_certificate.json")
    assert cert["input_sha256"] == EXPECTED["visible_maximum_joint/exact_input.json"]
    point = list(map(F, cert["primal"]))
    assert len(point) == 513 and all(x >= 0 for x in point)
    for row in baseline["raw_rows"]:
        assert dot(dense(row), point) - F(row["rhs"]) >= 0
    for eq in baseline["equalities"]:
        assert dot(dense(eq), point) == F(eq["rhs"])
    objective = [F(baseline["objective"].get(str(j), "0")) for j in range(513)]
    assert dot(objective, point) == F(cert["objective"])
    diagnostics = []
    for rec in catalog:
        row, old = by_name[rec["name"]], old_rows[rec["old_P25_comparison_row"]]
        slack = dot(dense(row), point)
        old_slack = dot(dense(old), point) - F(old["rhs"])
        diagnostics.append({"row": row["name"], "source": row["source"], "T": row["T"],
            "exact_slack": str(slack), "negative": slack < 0, "old_P25_row": old["name"],
            "old_P25_exact_slack": str(old_slack), "new_minus_old_slack": str(slack - old_slack)})
    negative = [r for r in diagnostics if r["negative"]]
    assert {(r["source"], r["T"]) for r in negative} == {(2, "C"), (2, "A4")}
    main_slack = dot(dense(main_NS), point)
    c2_slack = next(F(r["exact_slack"]) for r in diagnostics if r["source"] == 2 and r["T"] == "C")
    assert main_slack == 12 * c2_slack and dot(EC, point) == 0
    save("frozen_1002_point_diagnostics.json", {"status": "PASS_ZERO_OPTIMIZATION_DIAGNOSTIC", "optimizer_calls": 0,
         "input_sha256": EXPECTED["visible_maximum_joint/exact_input.json"],
         "certificate_sha256": EXPECTED["visible_maximum_joint_solve/exact_certificate.json"],
         "baseline_nonnegative_columns_verified": 513, "baseline_raw_rows_verified": 1002,
         "baseline_equalities_verified": 2, "all_new_slacks": diagnostics,
         "negative_count": len(negative), "negative_rows": negative, "Main_NS5_slack": str(main_slack),
         "C2_raw_slack_times_12_equals_Main_NS5": True,
         "not_claimed": ["SPE existence or counterexample", "new cone optimum", "A4 independence after NS5", "any 1003-point result"]})
    for relative, expected in pins.items():
        assert sha(ROOT / relative) == expected, relative
    result = {"status": STATUS, "optimizer_calls": 0, "family_sha256": sha(HERE / "exact_family.json"),
        "candidate_rows": 36, "pure_role_rows": 32, "outermean_dominated_rows": 4, "columns": 513,
        "matrix_coefficients": 18468, "hidden_states": 416, "minimum_types": 40,
        "literal_inner_six_index_states": inner_count, "literal_outer_same_six_index_states": outer_local_count,
        "literal_outer_average_cases": 640, "minimum_outer_m1_minus_m0": str(smallest),
        "theta_affine_endpoint": str(THETA), "Main_NS5_identity_columns_checked": 513,
        "C_equality_specialization_columns_checked": 4 * 513,
        "old_P25_comparison_columns_checked": 36 * 513, "frozen_1002_negative_rows": negative,
        "source_files_unchanged": len(pins), "added_to_any_LP": False,
        "strict_newness_of_each_pure_row_claimed": False, "half_status": "OPEN"}
    save("build_result.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
