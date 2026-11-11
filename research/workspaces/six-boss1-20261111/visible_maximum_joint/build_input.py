#!/usr/bin/env python3
"""Prepare all 512 visible-C atom types using exact arithmetic only.

This file has no optimizer, point completion, or model-realizability routine.
Every write is confined to its own visible_maximum_joint directory.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = WS.parents[2]
STATUS = "PREPARED_NO_OPTIMIZER"
ATOM_COUNT, KCOL, NCOLS = 512, 512, 513
BITS = [f"a{i}" for i in range(1, 7)] + ["x", "o", "c"]
PURE_OLD = [f"A{i}" for i in range(1, 7)] + ["X"]
WALLET_ROLES = PURE_OLD + ["Omean", "C"]
P25_ROLES = PURE_OLD + ["C", "Omean"]

EXPECTED = {
    "universal_union_wallet_v6/exact_input.json": "49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936",
    "universal_union_wallet_v6/exact_certificate.json": "98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d",
    "universal_union_wallet_v6/numerical_scaling.json": "6e6fe99114b864e98f92a99a7583caa9391ddd5538dca7ed591e2ae49b72e965",
    "main_root30_cap4_strict_bound/ROOT30_B2_B4_CAPACITY_FEEDBACK.json": "8459c0a86264e02efae76f16a060f1af0d0941c190863c7344b25481bc42fdc8",
    "maximal_root_tail_wallet_v3/exact_certificate.json": "b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925",
    "maximal_root_tail_wallet_v3/exact_input.json": "01c57b65a82b682d222cb449407416c4db0de60961c90d6eaafd35d15b1f79d0",
    "maximal_root_tail_wallet_v3/proof.md": "f5d47adde14fd247eeb55a4d1afa282400030ff361966e47c62deeabd1810851",
    "main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json": "d4ee988b28e897bcb836811c45e1c27a9728c64e352d2e30c79c93fded71a834",
    "main_all_source25_family/proof.md": "abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0",
    "main_all_source25_family/exact_family.json": "8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0",
}

OTHER_SOURCES = [
    ROOT / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    ROOT / "archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md",
    ROOT / "archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md",
    WS / "universal_union_wallet_lp/source_derivations.md",
    WS / "universal_union_wallet_lp/build_and_solve.py",
    WS / "universal_union_wallet_lp/check_certificate.py",
    WS / "universal_union_wallet_v6/ingest_rows.py",
    WS / "universal_union_wallet_v6/check_source_and_certificate.py",
    WS / "universal_union_wallet_v6/source_review.md",
    WS / "main_root30_cap4_strict_bound/proof.md",
]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(name, value):
    path = HERE / name
    assert path.parent == HERE
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def lift(coefficients):
    """Keep every explicitly stored zero and every coefficient string verbatim."""
    result = {}
    for key, value in coefficients.items():
        old = int(key)
        assert 0 <= old <= 256
        targets = (512,) if old == 256 else (2 * old, 2 * old + 1)
        for target in targets:
            result[str(target)] = value
    return result


def share(numerator, denominator):
    assert denominator or not numerator
    return F(numerator, denominator) if denominator else F(0)


def utility(bits, index):
    return share(bits[index], sum(bits[:6]))


def role_bit(bits, role):
    if role.startswith("A"):
        return bits[int(role[1:]) - 1]
    if role == "X":
        return bits[6]
    if role == "C":
        return bits[8]
    raise ValueError("Omean has six real query indices; it is not a pure membership bit")


def raw_divisor(row):
    if "numerical_divisor" in row:
        return F(row["numerical_divisor"])
    return max([F(1), abs(F(row["rhs"]))] + [abs(F(v)) for v in row["a"].values()])


def pure_cost25(p, n, t, q):
    assert t in (0, 1) and q in (0, 1)
    return F(n + 1, 2) * t + F(24 * t, p + n + 1) + F(q, p + 1 + n * t)


def new_cost25(bits, i, T, Q):
    """Only a pure/pure or single-six-index-average query is used here."""
    assert T == "C" or Q == "C"
    p, n, o = sum(bits[: i - 1]), 6 - i, bits[7]
    if T != "Omean" and Q != "Omean":
        return pure_cost25(p, n, role_bit(bits, T), role_bit(bits, Q))
    if Q == "Omean":
        t = role_bit(bits, T)
        return F(n + 1, 2) * t + F(24 * t, p + n + 1) + F(o, 6 * (p + 1 + n * t))
    q = role_bit(bits, Q)
    return F(q, p + 1) + F(o, 6) * (
        F(n + 1, 2) + F(24, p + n + 1) - F(n * q, (p + 1) * (p + n + 1))
    )


def pair_cost(bits, other):
    D, c, o = sum(bits[:4]) + 1, bits[8], bits[7]
    if other == "Omean":
        return F(c, D) + F(o, 6 * D) - F(c * o, 6 * D * (D + 1))
    r = role_bit(bits, other)
    return F(c + r, D) - F(c * r, D * (D + 1))


def literal_audit():
    """Finite exact identities for the analytical source, not numerical solving."""
    tails, minima, wallet_means, p25_means = [], [], [], []
    for i in range(1, 6):
        n = 6 - i
        for p in range(i):
            for t, q in product((0, 1), repeat=2):
                exact_values = []
                target = pure_cost25(p, n, t, q)
                for tail in product((0, 1), repeat=n):
                    s, z = sum(tail[:-1]), tail[-1]
                    phi = share(25 * t - z, p + t + s + z) + F(s, 2) + z + F(q, p + t + s + 1)
                    assert phi >= target
                    exact_values.append(phi)
                    tails.append({"i": i, "p": p, "t": t, "q": q, "tail": list(tail), "phi": str(phi), "minimum": str(target), "residual": str(phi - target)})
                assert min(exact_values) == target
                minima.append({"i": i, "p": p, "t": t, "q": q, "minimum": str(target)})
            for menu in product((0, 1), repeat=6):
                d, o = sum(menu), int(any(menu))
                A, B, E = F(n + 1, 2) + F(24, p + n + 1), F(1, p + 1), F(n, (p + 1) * (p + n + 1))
                for c in (0, 1):
                    exact_c_mean = sum((pure_cost25(p, n, c, q) for q in menu), F(0)) / 6
                    exact_mean_c = sum((pure_cost25(p, n, t, c) for t in menu), F(0)) / 6
                    weak_c_mean = A * c + F(o, 6) * (B - E * c)
                    weak_mean_c = B * c + F(o, 6) * (A - E * c)
                    assert exact_c_mean - weak_c_mean == F(d - o, 6) * (B - E * c) >= 0
                    assert exact_mean_c - weak_mean_c == F(d - o, 6) * (A - E * c) >= 0
                    for direction, exact, weak in [("C_Omean", exact_c_mean, weak_c_mean), ("Omean_C", exact_mean_c, weak_mean_c)]:
                        p25_means.append({"i": i, "p": p, "c": c, "menu": list(menu), "direction": direction, "exact_six_index_average": str(exact), "weak_union_cost": str(weak), "residual": str(exact - weak)})
    for D in range(1, 6):
        for c in (0, 1):
            for menu in product((0, 1), repeat=6):
                d, o = sum(menu), int(any(menu))
                exact = sum((F(c + q, D) - F(c * q, D * (D + 1)) for q in menu), F(0)) / 6
                weak = F(c, D) + F(o, 6 * D) - F(c * o, 6 * D * (D + 1))
                assert exact - weak == F((d - o) * (D + 1 - c), 6 * D * (D + 1)) >= 0
                wallet_means.append({"D": D, "c": c, "menu": list(menu), "exact_six_index_average": str(exact), "weak_union_cost": str(weak), "residual": str(exact - weak)})
    assert (len(tails), len(minima), len(wallet_means), len(p25_means)) == (456, 60, 640, 3840)
    return {"status": "PASS", "optimizer_calls": 0, "P25_hidden_states": tails, "P25_minima": minima, "RC_PAIR_C_mean_states": wallet_means, "P25_C_mixed_states": p25_means}


def main():
    assert HERE.name == "visible_maximum_joint"
    assert not (HERE / "freeze_manifest.json").exists(), "Prepared input is frozen; do not regenerate."
    before = {str((WS / rel).relative_to(ROOT)): digest(WS / rel) for rel in EXPECTED}
    for rel, expected in EXPECTED.items():
        assert digest(WS / rel) == expected, rel
    for source in OTHER_SOURCES:
        before[str(source.relative_to(ROOT))] = digest(source)
    save("source_pins.json", {"status": STATUS, "sources": before, "pinned_by_assignment": {str((WS / p).relative_to(ROOT)): h for p, h in EXPECTED.items()}})

    old = read(WS / "universal_union_wallet_v6/exact_input.json")
    oldscales = read(WS / "universal_union_wallet_v6/numerical_scaling.json")["scales"]
    cap4 = read(WS / "main_root30_cap4_strict_bound/ROOT30_B2_B4_CAPACITY_FEEDBACK.json")
    root270 = read(WS / "maximal_root_tail_wallet_v3/exact_certificate.json")
    root270_row = read(WS / "main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json")
    assert old["variables"] == 257 and len(old["raw_rows"]) == 867
    assert old["K_column"] == 256 and old["nonnegative_columns"] == list(range(257))
    assert old["atom_columns"] == [{"index": j, "a": list(bits[:6]), "x": bits[6], "o": bits[7]} for j, bits in enumerate(product((0, 1), repeat=8))]
    atoms = list(product((0, 1), repeat=9))
    atom_columns = [{"index": j, "old_index": j // 2, "a": list(t[:6]), "x": t[6], "o": t[7], "c": t[8]} for j, t in enumerate(atoms)]
    rows, catalog = [], []

    def append(row, origin, old_raw_index=None, **metadata):
        j = len(rows)
        rows.append(row)
        entry = {"raw_index": j, "name": row["name"], "family": row["family"], "origin": origin, "rhs": row["rhs"], "numerical_divisor": str(raw_divisor(row)), "old_raw_index": old_raw_index}
        entry.update(metadata)
        catalog.append(entry)

    for j, source in enumerate(old["raw_rows"]):
        row = deepcopy(source)
        row["a"] = lift(source["a"])
        append(row, "v6_pullback", old_raw_index=j)
        if row["name"] in oldscales:
            assert raw_divisor(row) == F(oldscales[row["name"]]), row["name"]
    assert len(oldscales) == 798 and all(name in {r["name"] for r in old["raw_rows"]} for name in oldscales)

    rootrow = deepcopy(cap4)
    rootrow["a"] = lift(cap4["a"])
    append(rootrow, "root_cap4_pullback", root_u_coefficient="1")
    a4, b4 = F(117135582158121, 1145925867755340), F(23074097917720, 1145925867755340)
    assert [F(rootrow["a"].get(str(j), "0")) for j in range(NCOLS)] == [utility(t, 0) - b4 * t[7] for t in atoms] + [-a4]
    line = root270["universal_root_line"]
    assert line["integer_line"] == {"u": "16877573861922720", "K": "1767904008200582", "O": "337340181272013"}
    assert line["any_six_legal_query_union"] and line["requires_OPT6"] is False
    a270, b270 = F(line["a"]), F(line["b"])
    assert a270 == F(1767904008200582, 16877573861922720) and b270 == F(337340181272013, 16877573861922720)

    def newrow(name, family, fn, K=F(0), rhs=F(0), divisor=F(1), origin="visible_C", **metadata):
        coeffs = [F(fn(t)) for t in atoms] + [F(K)]
        row = {"name": name, "family": family, "a": {str(j): str(v) for j, v in enumerate(coeffs)}, "rhs": str(rhs), "numerical_divisor": str(divisor)}
        row.update(metadata)
        append(row, origin, **metadata)

    lifted270 = deepcopy(root270_row)
    lifted270["a"] = lift(root270_row["a"])
    append(lifted270, "root270_pullback", root_u_coefficient="1")
    assert [F(lifted270["a"].get(str(j), "0")) for j in range(NCOLS)] == [utility(t, 0) - b270 * t[7] for t in atoms] + [-a270]
    for i in range(1, 7):
        newrow(f"SAFE_{i}_C", "VISIBLE_C_SAFE", lambda t, i=i: utility(t, i - 1) - F(t[8], sum(t[: i - 1]) + 7 - i), source=i, Q="C")
    newrow("FMAX_C", "VISIBLE_C_FMAX", lambda t: F(t[6] - t[8], sum(t[:4]) + 1), Q="C")
    newrow("MX_C", "VISIBLE_C_MX", lambda t: utility(t, 4) - F(t[8], sum(t[:4]) + 1 + t[6]), source=5, Q="C")
    for other in WALLET_ROLES:
        newrow(f"RC_C_{other}", "VISIBLE_C_RC", lambda t, other=other: utility(t, 4) + F(t[6], sum(t[:4]) + 1) - pair_cost(t, other), left="C", right=other)
    for other in WALLET_ROLES:
        newrow(f"PAIR_C_{other}", "VISIBLE_C_PAIR", lambda t, other=other: utility(t, 4) + utility(t, 5) + F(t[4], (sum(t[:4]) + 1) * (sum(t[:4]) + 2)) - pair_cost(t, other), left="C", right=other)
    for i, T, Q in product(range(1, 6), P25_ROLES, P25_ROLES):
        if T != "C" and Q != "C":
            continue
        newrow(f"PORTFOLIO25_i{i}_T{T}_Q{Q}", "VISIBLE_C_PORTFOLIO25", lambda t, i=i, T=T, Q=Q: 25 * utility(t, i - 1) - new_cost25(t, i, T, Q), K=F(7 - i, 2), divisor=F(25), source=i, T=T, Q=Q)
    for five in combinations(PURE_OLD, 5):
        newrow("OPT6_C_" + "_".join(five), "VISIBLE_C_OPT6", lambda t, five=five: -F(bool(t[8] or any(role_bit(t, role) for role in five))), rhs=F(-1), labels=list(five) + ["C"])
    newrow("MENU_MAX_SIZE_LOWER_BOUND", "MENU_MAX_SIZE", lambda t: -F(t[7], 6), K=F(1), origin="six_query_max_size")

    assert len(rows) == len(catalog) == 1002
    assert len({r["name"] for r in rows}) == 1002
    assert [r["name"] for r in rows[:867]] == [r["name"] for r in old["raw_rows"]]
    assert Counter(r["family"] for r in rows[869:1001]) == {"VISIBLE_C_SAFE": 6, "VISIBLE_C_FMAX": 1, "VISIBLE_C_MX": 1, "VISIBLE_C_RC": 9, "VISIBLE_C_PAIR": 9, "VISIBLE_C_PORTFOLIO25": 85, "VISIBLE_C_OPT6": 21}
    eq_o = deepcopy(old["equality"])
    eq_o["a"] = lift(eq_o["a"])
    eq_c = {"name": "C_maximum_size", "a": {**{str(j): "1" for j, t in enumerate(atoms) if t[8]}, "512": "-1"}, "rhs": "0"}
    source_bindings = {"baseline_input": EXPECTED["universal_union_wallet_v6/exact_input.json"], "baseline_certificate": EXPECTED["universal_union_wallet_v6/exact_certificate.json"], "CAP4_row": EXPECTED["main_root30_cap4_strict_bound/ROOT30_B2_B4_CAPACITY_FEEDBACK.json"], "ROOT270_certificate": EXPECTED["maximal_root_tail_wallet_v3/exact_certificate.json"], "ROOT270_input": EXPECTED["maximal_root_tail_wallet_v3/exact_input.json"], "ROOT270_proof": EXPECTED["maximal_root_tail_wallet_v3/proof.md"], "ROOT270_standard_row": EXPECTED["main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json"], "P25_family": EXPECTED["main_all_source25_family/exact_family.json"], "P25_proof": EXPECTED["main_all_source25_family/proof.md"]}
    inp = {
        "schema": "visible_maximum_joint_exact_v1",
        "status": STATUS,
        "optimizer_calls": 0,
        "scope": "All 512 actual-A1..A6 / common-actual-P-maximizer X / OPT6-union o / true-global-size-maximizer C types, independent K; complete necessary projection only.",
        "variables": NCOLS,
        "bit_order": BITS,
        "atom_columns": atom_columns,
        "K_column": KCOL,
        "nonnegative_columns": list(range(NCOLS)),
        "objective": lift(old["objective"]),
        "equalities": [eq_o, eq_c],
        "equality_count": 2,
        "inequality_convention": old["inequality_convention"],
        "raw_inequality_count": 1002,
        "raw_row_policy": "Retain all old and new raw rows in declared order, including zero and exactly duplicate affine rows; no pruning and no numerical scaling of this input.",
        "raw_rows": rows,
        "source_bindings": source_bindings,
        "source_pins_sha256": digest(HERE / "source_pins.json"),
        "source_review_sha256": digest(HERE / "source_review.md"),
        "Main_pre_freeze_increment": {"original_planned_raw_count": 1001, "final_raw_count": 1002, "added_row": "MENU_MAX_SIZE_LOWER_BOUND", "meaning": "K-O/6>=0 from six actual legal query size caps and union-count weakening", "standard_ROOT270_row_sha256": EXPECTED["main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json"]},
        "preparation_only": {"optimization_authorized": False, "point_completion_performed": False, "SPE_sufficiency_claimed": False, "half_status": "OPEN", "future_release_owner": "Main"},
    }
    save("exact_input.json", inp)

    routing = {"status": STATUS, "bit_order": BITS, "rule": "new_atom=2*old_atom+c; old K256 maps to K512", "old_to_new": [{"old_index": j, "new_c0": 2 * j, "new_c1": 2 * j + 1} for j in range(256)], "K": {"old_index": 256, "new_index": 512}, "columns": atom_columns + [{"index": 512, "kind": "K"}]}
    save("column_routing.json", routing)
    with (HERE / "column_routing.tsv").open("w", encoding="utf-8") as f:
        f.write("new_column\told_column\ta1a2a3a4a5a6xoc\tc\tkind\n")
        for j, t in enumerate(atoms):
            f.write(f"{j}\t{j//2}\t{''.join(map(str,t))}\t{t[8]}\tatom\n")
        f.write("512\t256\t\t\tK\n")

    save("row_catalog.json", {"status": STATUS, "raw_rows": 1002, "columns": 513, "equalities": 2, "index_convention": "zero-based raw_index", "rows": catalog})
    with (HERE / "row_catalog.tsv").open("w", encoding="utf-8") as f:
        f.write("raw_index\tname\tfamily\torigin\trhs\tnumerical_divisor\told_raw_index\tsource\tT\tQ\tleft\tright\tlabels\n")
        for r in catalog:
            fields = [r.get(k, "") for k in ("raw_index", "name", "family", "origin", "rhs", "numerical_divisor", "old_raw_index", "source", "T", "Q", "left", "right")]
            f.write("\t".join("" if x is None else str(x) for x in fields) + "\t" + ",".join(r.get("labels", [])) + "\n")
    scales = {r["name"]: str(raw_divisor(r)) for r in rows}
    assert all(F(v) > 0 for v in scales.values())
    save("numerical_scaling.json", {"status": STATUS, "scope": "Unscaled exact input. Future numeric consumers may divide complete rows and rhs only by these positive values after Main release.", "raw_order": [r["name"] for r in rows], "raw_scales": scales, "baseline_rule": "explicit numerical_divisor else max(1,abs(rhs),max_abs_coefficient); all 798 baseline stored unique scales checked", "new_P25_divisor": "25", "other_new_divisor": "1"})

    seen, diagnostics, zeros, duplicate_count = {}, [], [], 0
    for index, row in enumerate(rows):
        coeffs = tuple(F(row["a"].get(str(j), "0")) for j in range(NCOLS))
        key = coeffs, F(row["rhs"])
        is_zero = not any(coeffs) and key[1] == 0
        first = seen.get(key)
        diagnostics.append({"raw_index": index, "name": row["name"], "zero": is_zero, "identical_to_raw_index": first, "retained": True})
        if is_zero:
            zeros.append(row["name"])
        if first is not None:
            duplicate_count += 1
        else:
            seen[key] = index
    save("raw_identity_diagnostics.json", {"status": STATUS, "pruning_performed": False, "zero_rows": zeros, "exact_duplicate_raw_rows": duplicate_count, "distinct_affine_rows_including_zero": len(seen), "rows": diagnostics})

    literal = literal_audit()
    save("literal_query_checks.json", literal)
    for path, expected in before.items():
        assert digest(ROOT / path) == expected, ("read-only source changed", path)
    report = {"status": STATUS, "optimizer_calls": 0, "input_sha256": digest(HERE / "exact_input.json"), "raw_rows": len(rows), "columns": NCOLS, "atom_types": ATOM_COUNT, "equalities": 2, "inherited_raw_rows": 867, "new_root_rows": 2, "new_visible_C_rows": 132, "new_menu_K_lower_bound_rows": 1, "new_family_counts": dict(Counter(r["family"] for r in rows[869:])), "all_old_stored_unique_scaling_values_checked": len(oldscales), "old_raw_positive_divisors_recorded": 867, "all_zero_and_duplicate_raw_rows_retained": True, "zero_raw_rows": zeros, "distinct_affine_rows_including_zero": len(seen), "exact_duplicate_raw_rows": duplicate_count, "source_files_unchanged": len(before), "P25_hidden_states": 456, "P25_minima": 60, "six_index_wallet_mixed_states": 640, "six_index_P25_mixed_states": 3840, "independent_precheck_required": True, "future_optimizer_release_required_from_Main": True}
    save("build_result.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
