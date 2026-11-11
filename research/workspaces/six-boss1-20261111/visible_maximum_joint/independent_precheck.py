#!/usr/bin/env python3
"""Independent exact preparation audit; no builder import or optimizer.

The old 867 rows are checked by literal pullback.  The new C rows are rebuilt
from actual customer shares and the formal SAFE/RC/PAIR/P25 statements.
Menu averages enumerate all 64 memberships of six actual legal query indices;
neither disjointness nor independence of labels is assumed.
Only independent_precheck_result.json is written by this program.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = HERE.parents[3]
ATOMS = tuple(product((0, 1), repeat=9))
PURE_OLD = tuple(f"A{i}" for i in range(1, 7)) + ("X",)
QUERY_ROLES = PURE_OLD + ("C", "Omean")
PAIR_ROLES = PURE_OLD + ("Omean", "C")
EXPECTED_HASHES = {
    "universal_union_wallet_v6/exact_input.json":
        "49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936",
    "universal_union_wallet_v6/exact_certificate.json":
        "98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d",
    "main_root30_cap4_strict_bound/ROOT30_B2_B4_CAPACITY_FEEDBACK.json":
        "8459c0a86264e02efae76f16a060f1af0d0941c190863c7344b25481bc42fdc8",
    "main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json":
        "d4ee988b28e897bcb836811c45e1c27a9728c64e352d2e30c79c93fded71a834",
    "maximal_root_tail_wallet_v3/exact_certificate.json":
        "b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925",
    "maximal_root_tail_wallet_v3/exact_input.json":
        "01c57b65a82b682d222cb449407416c4db0de60961c90d6eaafd35d15b1f79d0",
    "maximal_root_tail_wallet_v3/proof.md":
        "f5d47adde14fd247eeb55a4d1afa282400030ff361966e47c62deeabd1810851",
    "main_all_source25_family/proof.md":
        "abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0",
    "main_all_source25_family/exact_family.json":
        "8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0",
}
FORMAL_SOURCES = (
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    "archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md",
    "archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md",
    "research/workspaces/six-boss1-20261111/universal_union_wallet_lp/source_derivations.md",
    "research/workspaces/six-boss1-20261111/universal_union_wallet_lp/build_and_solve.py",
    "research/workspaces/six-boss1-20261111/universal_union_wallet_lp/check_certificate.py",
    "research/workspaces/six-boss1-20261111/universal_union_wallet_v6/ingest_rows.py",
)


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def pullback(coeffs):
    """Preserve even explicit zero values and each source rational string."""
    out = {}
    for old_j, value in coeffs.items():
        old_j = int(old_j)
        assert 0 <= old_j <= 256
        if old_j == 256:
            out["512"] = value
        else:
            out[str(2 * old_j)] = value
            out[str(2 * old_j + 1)] = value
    return out


def dense(row):
    assert all(str(int(j)) == j and 0 <= int(j) < 513 for j in row["a"])
    return tuple(F(row["a"].get(str(j), "0")) for j in range(513))


def effective_old_divisor(row):
    if "numerical_divisor" in row:
        return F(row["numerical_divisor"])
    return max([F(1), abs(F(row["rhs"]))]
               + [abs(F(value)) for value in row["a"].values()])


def share(t, i):
    load = sum(t[:6])
    return F(t[i], load) if load else F(0)


def member(t, role):
    if role.startswith("A"):
        return F(t[int(role[1:]) - 1])
    return F(t[6]) if role == "X" else F(t[8]) if role == "C" else F(t[7], 6)


def legal_pair_rhs(background, left_bit, right_bit):
    """One genuine legal pair, retaining its exact shared customer bit."""
    D = background + 1
    return F(left_bit + right_bit, D) - F(left_bit * right_bit, D * (D + 1))


def direct_p25_cost(source, p, t, q):
    n = 6 - source
    c0 = F(n + 1, 2)
    return c0 * t + F(24 * t, p + n + 1) + F(q, p + 1 + n * t)


def visible_p25_cost(atom, source, T, Q):
    """Rebuild both mean orientations from their six-index expansions."""
    p = sum(atom[:source - 1])
    if T == "Omean":
        assert Q == "C"
        # A six-query membership vector with exactly o memberships realizes
        # the weakened d=o expression; monotonic weakening is checked below.
        return sum(direct_p25_cost(source, p, bit, atom[8])
                   for bit in (atom[7], 0, 0, 0, 0, 0)) / 6
    if Q == "Omean":
        assert T == "C"
        return sum(direct_p25_cost(source, p, atom[8], bit)
                   for bit in (atom[7], 0, 0, 0, 0, 0)) / 6
    return direct_p25_cost(source, p, int(member(atom, T)), int(member(atom, Q)))


def independently_rebuild_C_rows():
    expected = {}

    def add(name, family, values, K=F(0), rhs=F(0), divisor=F(1)):
        assert name not in expected
        expected[name] = {
            "family": family,
            "a": tuple(F(value) for value in values) + (F(K),),
            "rhs": F(rhs), "divisor": F(divisor),
        }

    for source in range(1, 7):
        add(f"SAFE_{source}_C", "SAFE",
            (share(t, source - 1) - F(t[8], sum(t[:source - 1]) + 7 - source)
             for t in ATOMS))
    add("FMAX_C", "FMAX", (F(t[6] - t[8], sum(t[:4]) + 1) for t in ATOMS))
    add("MX_C", "MX", (share(t, 4) - F(t[8], sum(t[:4]) + 1 + t[6])
                        for t in ATOMS))
    for role in PAIR_ROLES:
        rhs_by_atom = []
        for t in ATOMS:
            P = sum(t[:4])
            if role == "Omean":
                rhs_by_atom.append(sum(legal_pair_rhs(P, t[8], bit)
                                       for bit in (t[7], 0, 0, 0, 0, 0)) / 6)
            else:
                rhs_by_atom.append(legal_pair_rhs(P, t[8], int(member(t, role))))
        add(f"RC_C_{role}", "RC",
            (share(t, 4) + F(t[6], sum(t[:4]) + 1) - rhs
             for t, rhs in zip(ATOMS, rhs_by_atom)))
        add(f"PAIR_C_{role}", "PAIR",
            (share(t, 4) + share(t, 5)
             + F(t[4], (sum(t[:4]) + 1) * (sum(t[:4]) + 2)) - rhs
             for t, rhs in zip(ATOMS, rhs_by_atom)))
    for source in range(1, 6):
        for T in QUERY_ROLES:
            for Q in QUERY_ROLES:
                if "C" not in (T, Q):
                    continue
                add(f"PORTFOLIO25_i{source}_T{T}_Q{Q}", "P25",
                    (25 * share(t, source - 1) - visible_p25_cost(t, source, T, Q)
                     for t in ATOMS), K=F(7 - source, 2), divisor=F(25))
    for selected in combinations(PURE_OLD, 5):
        add("OPT6_C_" + "_".join(selected), "OPT6",
            (-int(t[8] or any(member(t, role) for role in selected)) for t in ATOMS),
            rhs=-1)
    assert len(expected) == 132
    assert Counter(row["family"] for row in expected.values()) == {
        "SAFE": 6, "FMAX": 1, "MX": 1, "RC": 9, "PAIR": 9, "P25": 85, "OPT6": 21}
    return expected


def check_p25_payment_envelope():
    states = minima = 0
    for source in range(1, 6):
        n = 6 - source
        for p, t, q in product(range(source), (0, 1), (0, 1)):
            values = []
            for tail in product((0, 1), repeat=n):
                s, z = sum(tail[:-1]), tail[-1]
                load = p + t + s + z
                phi = (F(25 * t - z, load) if load else F(0))
                phi += F(s, 2) + z + F(q, p + t + s + 1)
                target = direct_p25_cost(source, p, t, q)
                assert phi >= target, (source, p, t, q, tail, phi, target)
                values.append(phi)
                states += 1
            assert min(values) == direct_p25_cost(source, p, t, q)
            minima += 1
    assert states == 456 and minima == 60
    return {"hidden_state_checks": states, "exact_minima_checks": minima}


def check_six_index_mean_expansions():
    """Actual 6-label vectors, including aliases and all overlap degrees."""
    pair_checks = p25_checks = old_pair_self = old_p25_self = 0
    for P, c, memberships in product(range(5), (0, 1), product((0, 1), repeat=6)):
        D = P + 1
        d, o = sum(memberships), int(any(memberships))
        exact = sum(legal_pair_rhs(P, c, bit) for bit in memberships) / 6
        weak = F(c, D) + F(o, 6 * D) - F(c * o, 6 * D * (D + 1))
        assert exact - weak == F((d - o) * (D + 1 - c), 6 * D * (D + 1)) >= 0
        pair_checks += 1
    for source in range(1, 6):
        n = 6 - source
        for p, c, memberships in product(range(source), (0, 1), product((0, 1), repeat=6)):
            d, o = sum(memberships), int(any(memberships))
            cap = p + n + 1
            A = F(n + 1, 2) + F(24, cap)
            B = F(1, p + 1)
            E = F(n, (p + 1) * cap)
            exact_C_mean = sum(direct_p25_cost(source, p, c, bit) for bit in memberships) / 6
            weak_C_mean = A * c + F(o, 6) * (B - E * c)
            assert exact_C_mean - weak_C_mean == F(d - o, 6) * (B - E * c) >= 0
            exact_mean_C = sum(direct_p25_cost(source, p, bit, c) for bit in memberships) / 6
            weak_mean_C = B * c + F(o, 6) * (A - E * c)
            assert exact_mean_C - weak_mean_C == F(d - o, 6) * (A - E * c) >= 0
            p25_checks += 2
    # These old rows are pulled back without change.  Their distinct averaging
    # contracts are checked here to guard against an accidental common rule.
    for P, memberships in product(range(5), product((0, 1), repeat=6)):
        D = P + 1
        d, o = sum(memberships), int(any(memberships))
        exact = sum(legal_pair_rhs(P, memberships[j], memberships[k])
                    for j in range(6) for k in range(6)) / 36
        weak = F(o, 3 * D) - F(o, 36 * D * (D + 1))
        assert exact >= weak
        assert exact == F(d, 3 * D) - F(d * d, 36 * D * (D + 1))
        old_pair_self += 1
    for source in range(1, 6):
        n = 6 - source
        for p, memberships in product(range(source), product((0, 1), repeat=6)):
            d, o = sum(memberships), int(any(memberships))
            exact = sum(direct_p25_cost(source, p, memberships[j], memberships[k])
                        for j in range(6) for k in range(6) if j != k) / 30
            cap = p + n + 1
            A = F(n + 1, 2) + F(24, cap)
            B = F(1, p + 1)
            E = F(n, (p + 1) * cap)
            assert exact == F(d, 6) * (A + B) - F(d * (d - 1), 30) * E
            assert exact >= F(o, 6) * (A + B)
            old_p25_self += 1
    assert (pair_checks, p25_checks, old_pair_self, old_p25_self) == (640, 3840, 320, 960)
    for memberships in product((0, 1), repeat=6):
        assert sum(memberships) - int(any(memberships)) >= 0
    return {
        "membership_vectors_per_case": 64,
        "new_C_pair_one_mean_checks": pair_checks,
        "new_C_p25_both_orientations_checks": p25_checks,
        "inherited_pair_36_ordered_index_average_checks": old_pair_self,
        "inherited_p25_30_distinct_ordered_index_average_checks": old_p25_self,
        "menu_union_maximum_size_membership_checks": 64,
        "partition_assumed": False, "query_independence_assumed": False,
    }


def main():
    hashes = {}
    for name, expected in EXPECTED_HASHES.items():
        hashes[name] = digest(WS / name)
        assert hashes[name] == expected, name
    formal_hashes = {name: digest(ROOT / name) for name in FORMAL_SOURCES}
    base = read(WS / "universal_union_wallet_v6/exact_input.json")
    inp = read(HERE / "exact_input.json")
    assert len(base["raw_rows"]) == 867
    assert inp["status"] == "PREPARED_NO_OPTIMIZER"
    assert inp["variables"] == 513
    assert inp["K_column"] == 512
    assert inp["nonnegative_columns"] == list(range(513))
    assert len(inp["atom_columns"]) == 512
    for j, (record, bits) in enumerate(zip(inp["atom_columns"], ATOMS)):
        assert record["index"] == j
        assert tuple(record["a"]) + (record["x"], record["o"], record["c"]) == bits
        assert j == 2 * (j // 2) + bits[-1]
    assert inp["objective"] == pullback(base["objective"])
    eqs = inp["equalities"]
    assert len(eqs) == 2
    assert eqs[0] == {**base["equality"], "a": pullback(base["equality"]["a"])}
    assert eqs[1]["name"] == "C_maximum_size" and F(eqs[1]["rhs"]) == 0
    assert dense(eqs[1]) == tuple(F(t[8]) for t in ATOMS) + (F(-1),)
    assert inp["inequality_convention"] == base["inequality_convention"] == "a dot z >= rhs"
    rows = inp["raw_rows"]
    assert len(rows) == inp["raw_inequality_count"] == 1002
    assert len({r["name"] for r in rows}) == 1002
    by_name = {r["name"]: r for r in rows}
    for k, old in enumerate(base["raw_rows"]):
        expected = {**old, "a": pullback(old["a"])}
        assert rows[k] == expected, ("inherited raw metadata or literal coefficient mismatch", k)
    # Old zero/duplicate rows remain in their original raw slots, even where
    # their counterpart is absent from the old numerical unique representation.
    zero_old = [j for j, r in enumerate(base["raw_rows"])
                if not any(F(v) for v in r["a"].values()) and F(r["rhs"]) == 0]
    assert all(not any(dense(rows[j])) for j in zero_old)

    root4 = read(WS / "main_root30_cap4_strict_bound/ROOT30_B2_B4_CAPACITY_FEEDBACK.json")
    assert rows[867] == {**root4, "a": pullback(root4["a"])}
    root270_row = read(WS / "main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json")
    assert rows[868] == {**root270_row, "a": pullback(root270_row["a"])}
    assert rows[868]["name"] == "ROOT270_TRUE_BRANCH_P25"
    root270 = read(WS / "maximal_root_tail_wallet_v3/exact_certificate.json")
    line = root270["universal_root_line"]
    a, b = F(line["a"]), F(line["b"])
    assert line["integer_line"] == {"u": "16877573861922720", "K": "1767904008200582", "O": "337340181272013"}
    assert a == F(1767904008200582, 16877573861922720)
    assert b == F(337340181272013, 16877573861922720)
    assert line["any_six_legal_query_union"] and not line["requires_OPT6"]
    assert F(root270["branch_union_OPT_weight"]) == 0
    assert all(F(v) > 0 for v in root270["dual"]["original_unscaled_row_weights"].values())
    assert dense(rows[868]) == tuple(share(t, 0) - b * t[7] for t in ATOMS) + (-a,)
    assert F(rows[868]["rhs"]) == 0 and F(rows[868]["numerical_divisor"]) == 1

    new_expected = independently_rebuild_C_rows()
    assert set(r["name"] for r in rows[869:1001]) == set(new_expected)
    for name, expected in new_expected.items():
        actual = by_name[name]
        assert dense(actual) == expected["a"], ("new-C-coefficient", name)
        assert F(actual["rhs"]) == expected["rhs"], name
        assert F(actual["numerical_divisor"]) == expected["divisor"], name
    menu_size = rows[1001]
    assert menu_size["name"] == "MENU_MAX_SIZE_LOWER_BOUND"
    assert menu_size["family"] == "MENU_MAX_SIZE"
    assert dense(menu_size) == tuple(-F(t[7], 6) for t in ATOMS) + (F(1),)
    assert F(menu_size["rhs"]) == 0 and F(menu_size["numerical_divisor"]) == 1

    old_scales = read(WS / "universal_union_wallet_v6/numerical_scaling.json")["scales"]
    assert len(old_scales) == 798
    for row in base["unique_rows"]:
        assert F(old_scales[row["name"]]) == effective_old_divisor(row) > 0
    # The independent expected raw scales are also returned in a compact hash.
    expected_raw_scales = {
        r["name"]: str(effective_old_divisor(r)) for r in base["raw_rows"]}
    expected_raw_scales.update({rows[867]["name"]: "1", rows[868]["name"]: "1"})
    expected_raw_scales.update({name: str(r["divisor"]) for name, r in new_expected.items()})
    expected_raw_scales[menu_size["name"]] = "1"
    scale_data = read(HERE / "numerical_scaling.json")
    actual_raw_scales = scale_data["raw_scales"]
    assert isinstance(actual_raw_scales, dict)
    assert set(actual_raw_scales) == set(expected_raw_scales)
    assert scale_data["raw_order"] == [r["name"] for r in rows]
    for name, expected in expected_raw_scales.items():
        assert F(actual_raw_scales[name]) == F(expected) > 0, ("divisor", name)

    routing = read(HERE / "column_routing.json")
    assert routing["bit_order"] == [f"a{i}" for i in range(1, 7)] + ["x", "o", "c"]
    assert routing["old_to_new"] == [
        {"old_index": j, "new_c0": 2 * j, "new_c1": 2 * j + 1}
        for j in range(256)]
    assert routing["K"] == {"old_index": 256, "new_index": 512}
    assert routing["columns"] == inp["atom_columns"] + [{"index": 512, "kind": "K"}]
    for j, record in enumerate(inp["atom_columns"]):
        assert record["old_index"] == j // 2
    catalog = read(HERE / "row_catalog.json")["rows"]
    assert len(catalog) == 1002
    for k, (record, row) in enumerate(zip(catalog, rows)):
        assert record["raw_index"] == k
        assert record["name"] == row["name"] and record["family"] == row["family"]
        assert F(record["rhs"]) == F(row["rhs"])
        assert F(record["numerical_divisor"]) == F(expected_raw_scales[row["name"]])
        if k < 867:
            assert record["origin"] == "v6_pullback" and record["old_raw_index"] == k
        elif k == 867:
            assert record["origin"] == "root_cap4_pullback"
        elif k == 868:
            assert record["origin"] == "root270_pullback"
        elif k < 1001:
            assert record["origin"] == "visible_C"
            if row["name"].startswith("PORTFOLIO25_"):
                assert record["T"] in QUERY_ROLES and record["Q"] in QUERY_ROLES
                assert "C" in (record["T"], record["Q"])
                assert row["name"] == f'PORTFOLIO25_i{record["source"]}_T{record["T"]}_Q{record["Q"]}'
            elif row["name"].startswith(("RC_C_", "PAIR_C_")):
                assert record["left"] == "C" and record["right"] in PAIR_ROLES
                assert row["name"].endswith("_C_" + record["right"])
            elif row["name"].startswith("OPT6_C_"):
                assert len(record["labels"]) == 6 and len(set(record["labels"])) == 6
                assert "C" in record["labels"] and set(record["labels"]) <= set(PURE_OLD + ("C",))
                assert set(record["labels"]) == set(row["name"][5:].split("_"))
        else:
            assert record["origin"] == "six_query_max_size"

    seen, zeros, duplicates = {}, [], []
    for k, row in enumerate(rows):
        key = (dense(row), F(row["rhs"]))
        if not any(key[0]) and key[1] == 0:
            zeros.append({"raw_index": k, "name": row["name"]})
        elif key in seen:
            duplicates.append({"raw_index": k, "name": row["name"], "first_raw_index": seen[key]})
        else:
            seen[key] = k
    result = {
        "status": "PREPARED_NO_OPTIMIZER",
        "result": "PASS: independent literal lift and exact source-formula precheck",
        "input_sha256": digest(HERE / "exact_input.json"),
        "checker_sha256": digest(Path(__file__)),
        "optimizer_calls": 0, "builder_imported": False,
        "old_primal_point_used": False, "SPE_existence_claimed": False,
        "raw_inequalities": 1002, "variables": 513, "atom_columns": 512,
        "equalities": 2, "old_raw_rows_preserved": 867,
        "old_literal_lift_coefficient_checks": 867 * 513,
        "new_root_coefficient_checks": 2 * 513,
        "new_C_coefficient_checks": 132 * 513,
        "new_menu_maximum_size_coefficient_checks": 513,
        "new_C_families": dict(Counter(r["family"] for r in new_expected.values())),
        "old_unique_numerical_divisors_verified": len(old_scales),
        "all_raw_numerical_divisors_verified": len(expected_raw_scales),
        "row_catalog_records_verified": len(catalog),
        "column_routing_records_verified": 513,
        "raw_scales_canonical_sha256": sha256(json.dumps(expected_raw_scales, sort_keys=True).encode()).hexdigest(),
        "raw_zero_rows_retained": zeros, "exact_duplicate_rows_retained": duplicates,
        "distinct_nonzero_affine_rows": len(seen),
        "p25_real_payment_envelope": check_p25_payment_envelope(),
        "menu_index_checks": check_six_index_mean_expansions(),
        "source_sha256_verified": hashes,
        "formal_sources_read_sha256": formal_hashes,
        "scope": "Necessary full-domain projection only; no LP, point completion, or half claim.",
    }
    (HERE / "independent_precheck_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "result", "input_sha256", "optimizer_calls", "raw_inequalities",
        "variables", "equalities", "new_C_families", "distinct_nonzero_affine_rows",
        "p25_real_payment_envelope", "menu_index_checks")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
