#!/usr/bin/env python3
"""Prepare 1050 unscaled raw rows; no optimizer or source-code imports."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = WS.parents[2]
STATUS = "PREPARED_NO_OPTIMIZER"
EXPECTED = {
    "visible_maximum_joint_v2/exact_input.json": "0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4",
    "visible_maximum_joint_v2/numerical_scaling.json": "db5f70c7e531fc9feafc66806523713d917838f614eb35a7a5b096fa2b88293e",
    "visible_maximum_joint_v2/freeze_manifest.json": "61428a95a0798e755694e659eba215f3910ad6e698f8d2a8ed26d5d398a376fd",
    "source2_joint_internal_safe/sixteen_reweighted_vertex_family.json": "a38144bb000e8585d520a731ed4159269a7245e0616d020ca12550d55df3719e",
    "source2_joint_internal_safe/proof.md": "e4ba6dd0e4cde35a9c899d35e85c53a98a042b257e6bb14a01078726138210e4",
    "source2_joint_internal_safe/freeze_manifest.json": "ec51f3eff143d0f555d2601deb1954a06f249aecbd4eabcfab3398d2c45d7b25",
    "all_source_nested_safe_family/exact_family.json": "340267bbe7148107a685eb260ffc24029de1a93f77f4a4fd3f201cc109e5aa8b",
    "all_source_nested_safe_family/proof.md": "80a6ce05d8fc236298ff2e6b9fe0cc47073b5cbd7afbb155b560cce1ec95e212",
    "all_source_nested_safe_family/freeze_manifest.json": "47969518d4514e96fcd938bf42cd0c114c4a6ed657bb0f996cbe3724d372a43b",
    "visible_maximum_joint_v2_solve/exact_certificate.json": "b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea",
}
COORDINATE_FIELDS = ["variables", "bit_order", "atom_columns", "K_column", "nonnegative_columns", "objective", "equalities", "equality_count", "inequality_convention"]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def vector(row):
    return tuple(F(row["a"].get(str(j), "0")) for j in range(513))


def encode(v):
    return {str(j): str(a) for j, a in enumerate(v)}


def dot(v, point):
    return sum((a * b for a, b in zip(v, point) if a and b), F(0))


def pin_sources():
    pins = {}

    def add(path, expected):
        path = path.resolve()
        name = str(path.relative_to(ROOT))
        if name in pins:
            assert pins[name] == expected, ("conflicting frozen source", name)
        assert sha(path) == expected, ("source byte mismatch", name)
        pins[name] = expected

    for rel, expected in EXPECTED.items():
        add(WS / rel, expected)
    for package in ["visible_maximum_joint_v2", "source2_joint_internal_safe", "all_source_nested_safe_family"]:
        directory = WS / package
        manifest = read(directory / "freeze_manifest.json")
        for name, info in manifest["artifacts"].items():
            path = ROOT / name if name.startswith("research/") or name.startswith("archives/") else directory / name
            add(path, info["sha256"] if isinstance(info, dict) else info)
        for field in ("source_sha256", "prior_frozen_artifact_sha256"):
            for name, expected in manifest.get(field, {}).items():
                add(ROOT / name, expected)
        source_path = directory / "source_pins.json"
        if source_path.exists():
            for name, expected in read(source_path)["sources"].items():
                add(ROOT / name, expected)
    save("source_pins.json", {"status": STATUS, "sources": pins,
         "pinned_by_assignment": {str((WS / r).relative_to(ROOT)): h for r, h in EXPECTED.items()},
         "source_packages": ["visible_maximum_joint_v2", "source2_joint_internal_safe", "all_source_nested_safe_family"]})
    return pins


def main():
    assert not (HERE / "freeze_manifest.json").exists(), "Frozen preparation must not be rebuilt."
    pins = pin_sources()
    base = read(WS / "visible_maximum_joint_v2/exact_input.json")
    old_scales = read(WS / "visible_maximum_joint_v2/numerical_scaling.json")
    endpoints = read(WS / "source2_joint_internal_safe/sixteen_reweighted_vertex_family.json")
    source_family = read(WS / "all_source_nested_safe_family/exact_family.json")
    assert len(base["raw_rows"]) == base["raw_inequality_count"] == 1003
    assert base["variables"] == 513 and base["K_column"] == 512 and len(base["equalities"]) == 2
    assert isinstance(endpoints, list) and len(endpoints) == 16
    assert len(source_family["rows"]) == 36
    selected = []
    excluded = []
    old_by_name = {r["name"]: r for r in base["raw_rows"]}
    EC = vector(next(e for e in base["equalities"] if e["name"] == "C_maximum_size"))
    source_comparisons = read(WS / "all_source_nested_safe_family/old_P25_comparisons.json")
    comparisons = {r["new_row"]: r for r in source_comparisons["row_comparisons"]}
    for source_index, row in enumerate(source_family["rows"]):
        if row["T"] == "outerOmean":
            old_name = f"PORTFOLIO25_i{row['source']}_T8_Q8"
            difference = tuple(a - b for a, b in zip(vector(row), vector(old_by_name[old_name])))
            assert all(v >= 0 for v in difference)
            assert encode(difference) == comparisons[row["name"]]["difference_a"]
            excluded.append({"source_family_index": source_index, "name": row["name"], "source_row": deepcopy(row),
                "reason": "dominated_by_existing_30_distinct_index_P25", "old_dominating_row": old_name,
                "identity": "excluded_row = old_dominating_row + sum(o*delta_i(p)*z)",
                "nonnegative_difference_a": encode(difference), "rhs_difference": "0"})
        elif row["source"] == 2 and row["T"] == "C":
            name = "SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE"
            residual = tuple(a - 12 * b - 29 * c for a, b, c in zip(vector(old_by_name[name]), vector(row), EC))
            assert not any(residual)
            excluded.append({"source_family_index": source_index, "name": row["name"], "source_row": deepcopy(row),
                "reason": "equivalent_to_existing_NS5_modulo_C_equality", "existing_row": name,
                "identity": "existing_NS5 = 12*excluded_row + 29*C_maximum_size_equality",
                "positive_row_scale": "12", "free_equality_multiplier": "29", "all_513_column_residuals": encode(residual)})
        else:
            assert row["T"] in [f"A{i}" for i in range(1, 7)] + ["X", "C"]
            selected.append((source_index, deepcopy(row)))
    assert len(selected) == 31 and len(excluded) == 5
    assert all(F(r["numerical_divisor"]) == 25 for r in endpoints)
    assert all(F(r["numerical_divisor"]) == 25 for _, r in selected)
    rows = deepcopy(base["raw_rows"]) + deepcopy(endpoints) + [r for _, r in selected]
    assert len(rows) == 1050 and len({r["name"] for r in rows}) == 1050
    assert rows[:1003] == base["raw_rows"] and rows[1003:1019] == endpoints
    current = {k: deepcopy(base[k]) for k in COORDINATE_FIELDS}
    current.update({"schema": "visible_maximum_joint_v3_exact_v1", "status": STATUS, "optimizer_calls": 0,
        "scope": "Full 512 actual/X/OPT-union/C types plus independent K; unchanged 1003 raw rows plus16 reweighted source2 endpoints and31 pure-role all-source nested-SAFE rows.",
        "raw_inequality_count": 1050, "raw_rows": rows,
        "raw_row_policy": "All old 1003 raw dictionaries literal; retain every zero, duplicate and redundant legal row; no pruning or numeric scaling of exact input.",
        "baseline_metadata": {k: deepcopy(v) for k, v in base.items() if k != "raw_rows"},
        "source_bindings": {r: h for r, h in EXPECTED.items()},
        "source_pins_sha256": sha(HERE / "source_pins.json"),
        "source_review_sha256": sha(HERE / "source_review.md"),
        "append_contract": {"baseline_raw_count": 1003, "source2_endpoint_count": 16,
             "all_source_pure_count": 31, "endpoint_raw_indices": [1003, 1018],
             "all_source_raw_indices": [1019, 1049], "excluded_from_new_source_family_only": [r["name"] for r in excluded]},
        "preparation_only": {"optimization_authorized": False, "point_conditioned": False,
             "K_fixed": False, "support_restricted": False, "SPE_sufficiency_claimed": False,
             "half_status": "OPEN", "future_release_owner": "Main"}})
    save("exact_input.json", current)
    save("excluded_rows.json", {"status": STATUS, "source_family_sha256": EXPECTED["all_source_nested_safe_family/exact_family.json"],
         "old_rows_removed": 0, "source_candidates_excluded": 5, "rows": excluded,
         "evidence_source_C": "all_source_nested_safe_family/C_equality_comparisons.json",
         "evidence_source_dominance": "all_source_nested_safe_family/old_P25_comparisons.json"})

    catalog = deepcopy(read(WS / "visible_maximum_joint_v2/row_catalog.json"))
    assert isinstance(catalog, list) and len(catalog) == 1003
    for offset, row in enumerate(endpoints):
        catalog.append({"raw_index": 1003 + offset, "name": row["name"], "family": row["family"], "rhs": row["rhs"],
            "stored_coefficient_entries": len(row["a"]), "numerical_divisor": row["numerical_divisor"],
            "source": "source2_joint_internal_safe/sixteen_reweighted_vertex_family.json", "source_row_index": offset,
            "actual_source": 2, "theta3_theta4_theta5": row["theta3_theta4_theta5"], "s": row["s"],
            "actual_source2_IC_weight": row["actual_source2_IC_weight"]})
    for offset, (source_index, row) in enumerate(selected):
        catalog.append({"raw_index": 1019 + offset, "name": row["name"], "family": row["family"], "rhs": row["rhs"],
            "stored_coefficient_entries": len(row["a"]), "numerical_divisor": row["numerical_divisor"],
            "source": "all_source_nested_safe_family/exact_family.json", "source_row_index": source_index,
            "actual_source": row["source"], "T": row["T"], "theta": row["theta"]})
    assert len(catalog) == 1050
    save("row_catalog.json", catalog)
    with (HERE / "row_catalog.tsv").open("w") as f:
        f.write("raw_index\tname\tfamily\trhs\tnumerical_divisor\tsource\tsource_row_index\tactual_source\tT\n")
        for r in catalog:
            f.write("\t".join(str(r.get(k, "")) for k in ["raw_index", "name", "family", "rhs", "numerical_divisor", "source", "source_row_index", "actual_source", "T"]) + "\n")
    for name in ["column_routing.json", "column_routing.tsv"]:
        (HERE / name).write_bytes((WS / "visible_maximum_joint_v2" / name).read_bytes())
    scales = {"status": STATUS, "raw_order": deepcopy(old_scales["raw_order"]),
              "raw_scales": deepcopy(old_scales["raw_scales"]),
              "baseline_scaling_metadata": {k: deepcopy(v) for k, v in old_scales.items() if k not in ["raw_scales", "raw_order"]}}
    scales["scope"] = "All 1003 old raw positive divisor strings unchanged;47 appended rows retain source divisor25. Exact input remains unscaled; no optimizer authorized."
    scales["raw_order"] += [r["name"] for r in rows[1003:]]
    for r in rows[1003:]:
        assert r["name"] not in scales["raw_scales"]
        scales["raw_scales"][r["name"]] = r["numerical_divisor"]
    scales["v3_append"] = {"endpoint_rows": 16, "pure_all_source_rows": 31, "new_divisor": "25"}
    assert len(scales["raw_order"]) == len(scales["raw_scales"]) == 1050
    for name, value in old_scales["raw_scales"].items():
        assert scales["raw_scales"][name] == value
    assert all(F(v) > 0 for v in scales["raw_scales"].values())
    save("numerical_scaling.json", scales)

    seen, zero, duplicates, identities = {}, [], [], []
    for index, row in enumerate(rows):
        v = vector(row);key = v, F(row["rhs"])
        if not any(v) and key[1] == 0:
            zero.append({"raw_index": index, "name": row["name"]})
        elif key in seen:
            duplicates.append({"raw_index": index, "name": row["name"], "first_raw_index": seen[key]})
        else:
            seen[key] = index
        identities.append({"raw_index": index, "name": row["name"], "retained": True})
    save("raw_identity_diagnostics.json", {"status": STATUS, "pruning_performed": False,
         "zero_rows": zero, "exact_duplicate_rows": duplicates, "distinct_nonzero_affine_rows": len(seen), "rows": identities})

    cert = read(WS / "visible_maximum_joint_v2_solve/exact_certificate.json")
    assert cert["input_sha256"] == EXPECTED["visible_maximum_joint_v2/exact_input.json"]
    point = tuple(map(F, cert["primal"]))
    assert len(point) == 513 and all(x >= 0 for x in point)
    for r in base["raw_rows"]:
        assert dot(vector(r), point) >= F(r["rhs"])
    for e in base["equalities"]:
        assert dot(vector(e), point) == F(e["rhs"])
    diagnostics = []
    for index in range(1003, 1050):
        row = rows[index];value = dot(vector(row), point) - F(row["rhs"])
        diagnostics.append({"raw_index": index, "name": row["name"], "family": row["family"],
                            "exact_slack": str(value), "negative": value < 0})
    negative = [r for r in diagnostics if r["negative"]]
    save("frozen_1003_point_diagnostics.json", {"status": "PASS_DIAGNOSTIC_ONLY", "optimizer_calls": 0,
         "baseline_input_sha256": EXPECTED["visible_maximum_joint_v2/exact_input.json"],
         "baseline_certificate_sha256": EXPECTED["visible_maximum_joint_v2_solve/exact_certificate.json"],
         "old_raw_rows_checked": 1003, "old_equalities_checked": 2, "old_nonnegative_columns_checked": 513,
         "appended_row_values": diagnostics, "negative_appended_rows": negative,
         "negative_count": len(negative), "new_input_has_no_point_constraints": True,
         "new_system_feasibility_or_optimality_claimed": False})
    for name, expected in pins.items():
        assert sha(ROOT / name) == expected, name
    result = {"status": STATUS, "optimizer_calls": 0, "input_sha256": sha(HERE / "exact_input.json"),
        "raw_rows": 1050, "columns": 513, "atom_types": 512, "equalities": 2,
        "old_raw_dictionaries_literal": 1003, "new_endpoint_rows": 16, "new_cross_source_pure_rows": 31,
        "excluded_source_candidates": 5, "old_raw_rows_removed": 0,
        "old_scale_strings_literal": 1003, "new_rows_divisor": "25",
        "zero_rows_retained": zero, "duplicate_rows_retained": len(duplicates),
        "distinct_nonzero_affine_rows": len(seen), "source_files_unchanged": len(pins),
        "old_point_negative_appended_rows": len(negative), "independent_literal_check_required": True}
    save("build_result.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
