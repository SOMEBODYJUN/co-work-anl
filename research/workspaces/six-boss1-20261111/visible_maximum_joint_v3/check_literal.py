#!/usr/bin/env python3
"""Independent literal preparation checker; no builder/solver imports.

Reconstruct new rows from the actual weighted IC/CAP/BR/SAFE budgets, retaining
all hidden types and actual query indices. Old rows are checked literally.
This is an internal independent implementation, not an external blind review.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = WS.parents[2]
ATOMS = tuple(product((0, 1), repeat=9))
PURE = tuple(f"A{i}" for i in range(1, 7)) + ("X", "C")
FIVE = F(5, 12)


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def dense(row):
    assert all(str(int(k)) == k and 0 <= int(k) < 513 for k in row["a"])
    return tuple(F(row["a"].get(str(j), "0")) for j in range(513))


def share(bit, load):
    assert load or bit == 0
    return F(bit, load) if load else F(0)


def cost(i, p, t, tails, queries, alpha, internal):
    """Negative of the literal sum of original weighted customer budgets."""
    assert len(tails) == 6 - i and len(queries) == 6
    slot = {j: tails[j - i - 1] for j in range(i + 1, 7)}
    load = p + t + sum(tails)
    budget = -alpha * share(t, load)
    for j in range(i + 1, 6):
        budget -= F(slot[j], 2)
    budget -= slot[6]
    terminal_prefix = p + t + sum(slot[j] for j in range(i + 1, 6))
    budget += sum((share(slot[6], load) - F(q, terminal_prefix + 1) for q in queries), F(0)) / 6
    for j, theta in internal.items():
        assert i < j < 6 and theta >= 0
        prefix = p + t + sum(slot[k] for k in range(i + 1, j))
        budget += theta * sum((share(slot[j], load) - F(q, prefix + 7 - j) for q in queries), F(0)) / 6
    return -budget


def member(bits, role):
    if role in PURE[:6]:
        return bits[PURE.index(role)]
    assert role in ("X", "C")
    return bits[6] if role == "X" else bits[8]


def dot(v, point):
    return sum((a * b for a, b in zip(v, point) if a and b), F(0))


def main():
    assert sha(WS / "visible_maximum_joint_v2/exact_input.json") == "0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4"
    assert sha(WS / "source2_joint_internal_safe/sixteen_reweighted_vertex_family.json") == "a38144bb000e8585d520a731ed4159269a7245e0616d020ca12550d55df3719e"
    assert sha(WS / "all_source_nested_safe_family/exact_family.json") == "340267bbe7148107a685eb260ffc24029de1a93f77f4a4fd3f201cc109e5aa8b"
    pins = read(HERE / "source_pins.json")
    for name, expected in pins["sources"].items():
        assert sha(ROOT / name) == expected, name
    base = read(WS / "visible_maximum_joint_v2/exact_input.json")
    inp = read(HERE / "exact_input.json")
    vertex_rows = read(WS / "source2_joint_internal_safe/sixteen_reweighted_vertex_family.json")
    cross = read(WS / "all_source_nested_safe_family/exact_family.json")
    assert inp["status"] == "PREPARED_NO_OPTIMIZER" and inp["optimizer_calls"] == 0
    assert inp["variables"] == 513 and inp["K_column"] == 512
    for field in ["variables", "bit_order", "atom_columns", "K_column", "nonnegative_columns", "objective", "equalities", "equality_count", "inequality_convention"]:
        assert inp[field] == base[field], field
    assert inp["baseline_metadata"] == {k: v for k, v in base.items() if k != "raw_rows"}
    assert inp["source_pins_sha256"] == sha(HERE / "source_pins.json")
    assert inp["source_review_sha256"] == sha(HERE / "source_review.md")
    assert inp["nonnegative_columns"] == list(range(513))
    assert len(inp["equalities"]) == inp["equality_count"] == 2
    assert len(inp["atom_columns"]) == 512
    for j, (record, t) in enumerate(zip(inp["atom_columns"], ATOMS)):
        assert record == {"index": j, "old_index": j // 2, "a": list(t[:6]), "x": t[6], "o": t[7], "c": t[8]}
    assert inp["objective"] == {str(j): "1" for j, t in enumerate(ATOMS) if sum(t[:6]) > 0}
    assert dense(inp["equalities"][0]) == tuple(F(t[7]) for t in ATOMS) + (F(0),)
    assert F(inp["equalities"][0]["rhs"]) == 1
    EC = tuple(F(t[8]) for t in ATOMS) + (F(-1),)
    assert dense(inp["equalities"][1]) == EC and F(inp["equalities"][1]["rhs"]) == 0

    rows = inp["raw_rows"]
    assert len(rows) == inp["raw_inequality_count"] == 1050
    assert rows[:1003] == base["raw_rows"]
    assert rows[1003:1019] == vertex_rows
    selected = [(k, r) for k, r in enumerate(cross["rows"]) if r["T"] in PURE and not (r["source"] == 2 and r["T"] == "C")]
    assert len(selected) == 31 and rows[1019:] == [r for _, r in selected]
    assert len({r["name"] for r in rows}) == 1050

    expected_new, hidden, cross_hidden = {}, [], []
    vertex_menu_checks = 0
    for idx, row in enumerate(vertex_rows):
        which, s_bit = divmod(idx, 2)
        code = tuple((which >> j) & 1 for j in (2, 1, 0))
        theta5 = FIVE * code[2]
        theta4 = (FIVE - theta5 / 36) * code[1]
        theta3 = (FIVE - theta4 / 72 - theta5 / 36) * code[0]
        thetas, s = (theta3, theta4, theta5), F(9 * s_bit)
        alpha = 25 + sum(thetas, F(0)) - s
        assert alpha >= 16
        assert row["name"] == "SOURCE2_MAXIMUM_C_REWEIGHTED_INTERNAL_SAFE_V" + "".join(map(str, code)) + f"_S{int(s)}"
        assert tuple(map(F, row["theta3_theta4_theta5"])) == thetas
        assert F(row["s"]) == s and F(row["actual_source2_IC_weight"]) == alpha
        assert F(row["rhs"]) == 0 and row["numerical_divisor"] == "25"
        internal = dict(zip((3, 4, 5), thetas))
        minima = {}
        for p, c, o in product((0, 1), repeat=3):
            values = []
            target = F(5 * c, 2) + F(24 * c, p + 5) + F(o, 6 * (p + 4 * c + 1)) - s * c / 5
            target += sum((theta * F(o, 6 * (p + (j - 2) * c + 7 - j)) for j, theta in internal.items()), F(0))
            for tail in product((0, 1), repeat=4):
                value = cost(2, p, c, tail, (o, 0, 0, 0, 0, 0), alpha, internal)
                assert value >= target
                values.append(value)
                hidden.append({"endpoint_index": idx, "p": p, "c": c, "o": o, "tail": list(tail),
                    "literal_cost": str(value), "closed_minimum": str(target), "residual": str(value - target)})
            assert min(values) == target
            minima[p, c, o] = min(values)
        for p, c in product((0, 1), repeat=2):
            for tail in product((0, 1), repeat=4):
                prefix6 = p + c + sum(tail[:3])
                for menu in product((0, 1), repeat=6):
                    d, o = sum(menu), int(any(menu))
                    literal = cost(2, p, c, tail, menu, alpha, internal)
                    projected = cost(2, p, c, tail, (o, 0, 0, 0, 0, 0), alpha, internal)
                    slope = F(1, prefix6 + 1)
                    for j, theta in internal.items():
                        prefixj = p + c + sum(tail[:j - 3])
                        slope += theta / (prefixj + 7 - j)
                    assert literal - projected == F(d - o, 6) * slope >= 0
                    vertex_menu_checks += 1
        # Add the exact free C mass equality only after actual budgets.
        eq_multiplier = F(5, 2) - s / 5
        coefficients = tuple(alpha * share(t[1], sum(t[:6])) - minima[t[0], t[8], t[7]] + eq_multiplier * t[8] for t in ATOMS) + (F(5, 2) - eq_multiplier,)
        assert dense(row) == coefficients
        assert coefficients[-1] == s / 5
        expected_new[row["name"]] = coefficients
    assert len(hidden) == 2048 and vertex_menu_checks == 65536

    cross_min = {}
    cross_menu_checks = 0
    for i in range(1, 5):
        n = 6 - i
        for p, t, o in product(range(i), (0, 1), (0, 1)):
            target = F(n + 1, 2) * t + F(24 * t, p + n + 1) + F(o, 6 * (p + 1 + n * t))
            target += FIVE * (F(o, 6 * (p + (5 - i) * t + 2)) - F(t, min(p + n + 1, 5)))
            values = []
            for tail in product((0, 1), repeat=n):
                value = cost(i, p, t, tail, (o, 0, 0, 0, 0, 0), F(25), {5: FIVE})
                assert value >= target
                values.append(value)
                cross_hidden.append({"source": i, "p": p, "t": t, "o": o, "tail": list(tail),
                    "literal_cost": str(value), "closed_minimum": str(target), "residual": str(value - target)})
            assert min(values) == target
            cross_min[i, p, t, o] = min(values)
        for p, t in product(range(i), (0, 1)):
            for tail in product((0, 1), repeat=n):
                D6 = p + t + sum(tail[:-1]) + 1
                D5 = p + t + sum(tail[:-2]) + 2
                for menu in product((0, 1), repeat=6):
                    d, o = sum(menu), int(any(menu))
                    exact = cost(i, p, t, tail, menu, F(25), {5: FIVE})
                    weak = cost(i, p, t, tail, (o, 0, 0, 0, 0, 0), F(25), {5: FIVE})
                    assert exact - weak == F(d - o, 6) * (F(1, D6) + FIVE / D5) >= 0
                    cross_menu_checks += 1
    assert len(cross_hidden) == 416 and len(cross_min) == 40 and cross_menu_checks == 13312
    all_cross_vectors = {}
    for row in cross["rows"]:
        i, role = row["source"], row["T"]
        values = []
        for t in ATOMS:
            p, o = sum(t[:i - 1]), t[7]
            if role == "outerOmean":
                value = sum((cross_min[i, p, q, o] for q in (o, 0, 0, 0, 0, 0)), F(0)) / 6
            else:
                value = cross_min[i, p, member(t, role), o]
            values.append(25 * share(t[i - 1], sum(t[:6])) - value)
        values.append(F(7 - i, 2))
        assert dense(row) == tuple(values)
        all_cross_vectors[row["name"]] = tuple(values)
    for _, row in selected:
        expected_new[row["name"]] = all_cross_vectors[row["name"]]
    assert len(expected_new) == 47
    with (HERE / "appended_column_checks.tsv").open("w") as out:
        out.write("raw_index\trow_name\tcolumn\tstored\tliteral_expected\tresidual\n")
        for idx in range(1003, 1050):
            row = rows[idx];wanted = expected_new[row["name"]]
            for j, stored in enumerate(dense(row)):
                assert stored == wanted[j]
                out.write(f"{idx}\t{row['name']}\t{j}\t{stored}\t{wanted[j]}\t0\n")

    old_by_name = {r["name"]: r for r in base["raw_rows"]}
    exclusions = read(HERE / "excluded_rows.json")
    assert exclusions["old_rows_removed"] == 0 and len(exclusions["rows"]) == 5
    excluded_names = set()
    for e in exclusions["rows"]:
        source = cross["rows"][e["source_family_index"]]
        assert e["source_row"] == source and e["name"] == source["name"]
        assert e["name"] not in {r["name"] for r in rows[1019:]}
        excluded_names.add(e["name"])
        if source["T"] == "outerOmean":
            old = old_by_name[e["old_dominating_row"]]
            diff = tuple(a - b for a, b in zip(all_cross_vectors[e["name"]], dense(old)))
            assert tuple(F(e["nonnegative_difference_a"][str(j)]) for j in range(513)) == diff
            assert all(v >= 0 for v in diff)
            assert all(diff[j] > 0 for j, t in enumerate(ATOMS) if t[7])
        else:
            assert source["source"] == 2 and source["T"] == "C"
            assert dense(old_by_name[e["existing_row"]]) == tuple(12 * a + 29 * b for a, b in zip(all_cross_vectors[e["name"]], EC))
            assert all(F(v) == 0 for v in e["all_513_column_residuals"].values())
    assert excluded_names == {"NESTED_SAFE5_i2_TC"} | {f"NESTED_SAFE5_i{i}_TouterOmean" for i in range(1, 5)}

    scaling = read(HERE / "numerical_scaling.json")
    old_scaling = read(WS / "visible_maximum_joint_v2/numerical_scaling.json")
    assert scaling["raw_order"] == [r["name"] for r in rows]
    assert scaling["raw_order"][:1003] == old_scaling["raw_order"]
    for name, scale in old_scaling["raw_scales"].items():
        assert scaling["raw_scales"][name] == scale and F(scale) > 0
    for row in rows[1003:]:
        assert row["numerical_divisor"] == scaling["raw_scales"][row["name"]] == "25"
    assert len(scaling["raw_scales"]) == 1050
    catalog = read(HERE / "row_catalog.json")
    assert catalog[:1003] == read(WS / "visible_maximum_joint_v2/row_catalog.json")
    assert len(catalog) == 1050
    for k, (r, c) in enumerate(zip(rows, catalog)):
        assert c["raw_index"] == k and c["name"] == r["name"] and c["family"] == r["family"]
        assert c["rhs"] == r["rhs"] and c["numerical_divisor"] == scaling["raw_scales"][r["name"]]
    assert (HERE / "column_routing.json").read_bytes() == (WS / "visible_maximum_joint_v2/column_routing.json").read_bytes()
    assert (HERE / "column_routing.tsv").read_bytes() == (WS / "visible_maximum_joint_v2/column_routing.tsv").read_bytes()
    route = read(HERE / "column_routing.json")
    assert route["columns"] == inp["atom_columns"] + [{"index": 512, "kind": "K"}]

    zero, duplicates, seen = [], [], {}
    for k, row in enumerate(rows):
        v = dense(row);key = v, F(row["rhs"])
        if not any(v) and key[1] == 0:
            zero.append({"raw_index": k, "name": row["name"]})
        elif key in seen:
            duplicates.append({"raw_index": k, "name": row["name"], "first_raw_index": seen[key]})
        else:
            seen[key] = k
    diagnostic = read(HERE / "raw_identity_diagnostics.json")
    assert diagnostic["zero_rows"] == zero and diagnostic["exact_duplicate_rows"] == duplicates
    assert len(seen) == diagnostic["distinct_nonzero_affine_rows"] == 980
    assert len(zero) == 1 and len(duplicates) == 69 and diagnostic["pruning_performed"] is False

    assert sha(WS / "visible_maximum_joint_v2_solve/exact_certificate.json") == "b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea"
    cert = read(WS / "visible_maximum_joint_v2_solve/exact_certificate.json")
    point = tuple(map(F, cert["primal"]))
    assert len(point) == 513 and all(x >= 0 for x in point)
    for row in base["raw_rows"]:
        assert dot(dense(row), point) >= F(row["rhs"])
    for eq in base["equalities"]:
        assert dot(dense(eq), point) == F(eq["rhs"])
    pd = read(HERE / "frozen_1003_point_diagnostics.json")
    negatives = []
    for d in pd["appended_row_values"]:
        row = rows[d["raw_index"]]
        assert d["name"] == row["name"]
        slack = dot(dense(row), point) - F(row["rhs"])
        assert F(d["exact_slack"]) == slack and d["negative"] == (slack < 0)
        if slack < 0:
            negatives.append(d)
    assert len(pd["appended_row_values"]) == 47 and negatives == pd["negative_appended_rows"]
    assert len(negatives) == 8
    assert [r["name"] for r in negatives if r["raw_index"] >= 1019] == ["NESTED_SAFE5_i2_TA4"]
    assert all(inp["preparation_only"][k] is False for k in ["optimization_authorized", "point_conditioned", "K_fixed", "support_restricted", "SPE_sufficiency_claimed"])
    for name, expected in pins["sources"].items():
        assert sha(ROOT / name) == expected, name

    state_result = {"status": "PASS", "endpoint_hidden_states": hidden, "cross_source_hidden_states": cross_hidden,
                    "endpoint_literal_six_index_cases": vertex_menu_checks, "cross_source_literal_six_index_cases": cross_menu_checks}
    (HERE / "literal_source_checks.json").write_text(json.dumps(state_result, ensure_ascii=False, indent=2) + "\n")
    result = {"status": "PREPARED_NO_OPTIMIZER", "result": "PASS_INDEPENDENT_LITERAL_PREPARATION_CHECK",
        "input_sha256": sha(HERE / "exact_input.json"), "checker_sha256": sha(Path(__file__)),
        "optimizer_calls": 0, "builder_or_source_code_imported": False, "external_blind_review_claimed": False,
        "raw_rows": 1050, "columns": 513, "equalities": 2,
        "old_raw_dictionaries_literal": 1003, "old_coefficient_entries_checked": 1003 * 513,
        "new_endpoint_rows": 16, "new_pure_cross_source_rows": 31, "appended_column_checks": 47 * 513,
        "excluded_source_rows": 5, "exclusion_column_checks": 5 * 513,
        "endpoint_hidden_states": len(hidden), "endpoint_minimum_types": 16 * 8,
        "cross_source_hidden_states": len(cross_hidden), "cross_source_minimum_types": 40,
        "endpoint_literal_six_query_checks": vertex_menu_checks, "cross_source_literal_six_query_checks": cross_menu_checks,
        "old_positive_scale_strings_preserved": 1003, "new_positive_scales_checked": 47,
        "raw_zero_rows_retained": zero, "raw_duplicate_rows_retained": len(duplicates),
        "distinct_nonzero_affine_rows": 980, "source_files_unchanged": len(pins["sources"]),
        "frozen_1003_negative_appended_rows": negatives,
        "new_system_feasibility_or_optimality_claimed": False, "half_status": "OPEN"}
    (HERE / "literal_check_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
