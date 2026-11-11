"""Append the pinned complete 81 separate-query epigraph without optimization.

Only this directory is written.  All old row and column objects are retained.
The source extension's full structural domain is copied before point weights
are inspected.  Canonical values at the certified complete624 opt_v2 point are
diagnostics, not a feasible extended point or a shared-transport certificate.
Main must independently audit every new coefficient before any solve.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = RUN.parents[2]
STEM = "complete624_single81_v1"
SEMANTIC = 4849
BASE_N = 12631
BASE_M = 12666
NEW_N = 7954
NEW_M = 8035
FAMILIES = ("B2", "B3", "B4", "Mroot")
METADATA_SHA = "afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460"

SOURCES = {
    "input_contract": (
        "research/workspaces/six-boss2-20261111-cross/joint_requery/boss1_81_extension_input_contract_v1.md",
        "920af1fc69141562a70ab6a763af1f761f211d34cac2220fcb4fe67f5797b2de",
    ),
    "domain_bridge": (
        "research/workspaces/six-boss2-20261111-cross/joint_requery/boss1_transport_domain_bridge_v1.md",
        "f0929b2c569fc8468cf3c35f91a9b0540801e086f706b8e7c10132a9eac662dc",
    ),
    "mother_matrix": (
        "research/workspaces/six-boss2-20261111-cross/joint_requery/complete624_actual4_R00_v1_matrix.json.gz",
        "556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a",
    ),
    "mother_point": (
        "research/workspaces/six-boss2-20261111-cross/master_cuts/complete624_actual4_R00_opt_v2_exact.json",
        "02bcb92f33f7e7e4fac00a4c64fd39b0a4f0c68a736559c300bbfba255168817",
    ),
    "semantic_projection": (
        "research/workspaces/six-boss2-20261111-cross/master_cuts/complete624_actual4_R00_opt_v2_original4849_exact.json",
        "75cf981c8e9a6554b796735b3e96c7e1145f420addec0ba045b25a293139803c",
    ),
    "extension": (
        "research/workspaces/six-boss1-20261111/tail_constraints/single-query-epigraph.json",
        "964ef22c37f9338a5e29423ff6009611256f5720b5f0b7016bb55940e570a94c",
    ),
    "extension_builder": (
        "research/workspaces/six-boss1-20261111/tail_constraints/build_single_query_epigraph.py",
        "3aacc1edd5b6cf7357e1f2dbce15b1c459620abbce7b3dfb9f79a1169551703f",
    ),
    "semantic_decoder": (
        "research/workspaces/six-boss1-20261111/tail_constraints/transport_separator.py",
        "182f48cb2005b78f9a3de2847df333f9365f2d29e867f43b354b9e13515bda29",
    ),
    "frozen_93_diagnostic": (
        "research/workspaces/six-boss2-20261111-cross/joint_requery/boss1_transport_93_at624_v2.json",
        "3305ffd8de3c1c19061cfc4c23cc05a4ca446f351618ead1ce32804ec95fa8c7",
    ),
    "main_mother_verification": (
        "research/workspaces/six-boss2-20261111-cross/main_verify_complete624_opt_v2.json",
        "8a8668e4ed5348a25ce8d1ee7c35adc2f475704c4c85c84947a9d459af1c9a93",
    ),
    "main_projection_verification": (
        "research/workspaces/six-boss2-20261111-cross/main_verify_624_projection_v1.json",
        "dbbb6a48ece28cd587f818f153d176096f5f4f5edf9aebd927ba14067b1a7f1d",
    ),
}


def sha_file(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_sha(value):
    h = hashlib.sha256()
    encoder = json.JSONEncoder(ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    for block in encoder.iterencode(value):
        h.update(block.encode("utf-8"))
    return h.hexdigest()


def load_source(name):
    path = ROOT / SOURCES[name][0]
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def source_manifest():
    result = {}
    for name, (relative, expected) in SOURCES.items():
        path = ROOT / relative
        actual = sha_file(path)
        assert actual == expected, (name, actual, expected)
        result[name] = {"path": relative, "sha256": actual, "bytes": path.stat().st_size}
    return result


def save_json(path, value):
    assert path.parent == HERE and not path.exists(), path
    temporary = path.with_name(path.name + ".tmp")
    assert not temporary.exists(), temporary
    with temporary.open("xb") as binary:
        if path.suffix == ".gz":
            with gzip.GzipFile(filename="", fileobj=binary, mode="wb", mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as text:
                    json.dump(value, text, ensure_ascii=False, separators=(",", ":"))
                    text.write("\n")
        else:
            with io.TextIOWrapper(binary, encoding="utf-8", newline="\n") as text:
                json.dump(value, text, ensure_ascii=False, indent=2)
                text.write("\n")
    temporary.rename(path)
    return {"path": str(path.relative_to(ROOT)), "sha256": sha_file(path), "bytes": path.stat().st_size}


@lru_cache(maxsize=None)
def rational(value):
    return F(value)


def check_sparse(entries, width):
    previous = -1
    for j, value in entries:
        assert isinstance(j, int) and previous < j < width
        assert isinstance(value, str) and value == str(rational(value)) and rational(value)
        previous = j


def dot(entries, values):
    return sum((rational(value) * values[j] for j, value in entries if values[j]), F())


def remap(j):
    assert 0 <= j < SEMANTIC + NEW_N
    return j if j < SEMANTIC else BASE_N + j - SEMANTIC


def freeze(value):
    return tuple(freeze(x) for x in value) if isinstance(value, (list, tuple)) else value


def budget_identity(name, labels):
    kind, family, orbit_text, label = name.split(":")
    orbit = [int(x) for x in orbit_text.strip("()").split(",")]
    if kind == "tail-budget":
        query = [f"new-to-{label}"]
    else:
        assert kind == "Z-budget"
        query = ["Z-to-new", labels[family].index(label), label]
    return {"family": family, "orbit": orbit, "query": query}


def diagnostic_key(record):
    return record["family"], tuple(record["orbit"]), tuple(record["query"])


def main():
    outputs = {
        "matrix": HERE / f"{STEM}_matrix.json.gz",
        "mapping": HERE / f"{STEM}_mapping.json.gz",
        "canonical": HERE / f"{STEM}_canonical_at624_v2.json.gz",
        "structure": HERE / f"{STEM}_structure.json",
    }
    assert all(not path.exists() for path in outputs.values()), "Refuse to overwrite a frozen output"
    sources = source_manifest()
    mother = load_source("mother_matrix")
    extension = load_source("extension")
    assert mother["row_count"] == len(mother["rows"]) == BASE_M
    assert mother["column_count"] == len(mother["columns"]) == BASE_N
    assert mother["nonnegative_columns"] == "all"
    assert extension["base_column_metadata_sha256"] == METADATA_SHA
    assert canonical_sha(mother["columns"][:SEMANTIC]) == METADATA_SHA
    assert len(extension["new_columns"]) == NEW_N
    assert len(extension["rows"]) == NEW_M
    assert extension["stats"]["base_columns"] == SEMANTIC
    assert extension["stats"]["added_columns"] == NEW_N
    assert extension["stats"]["added_rows"] == NEW_M
    assert extension["stats"]["threshold_rows"] == NEW_N
    assert extension["stats"]["budget_rows"] == 81
    parent_column_hash = canonical_sha(mother["columns"])
    parent_row_hash = canonical_sha(mother["rows"])
    mother_nonzeros = sum(len(row["nonzero"]) for row in mother["rows"])
    source_nonzeros = sum(len(row["coefficients"]) for row in extension["rows"])
    assert mother_nonzeros == 2704303 and source_nonzeros == 340092

    # Construct the whole matrix before consulting any diagnostic point mass.
    columns = mother["columns"] + extension["new_columns"]
    rows = list(mother["rows"])
    occurrences = defaultdict(list)
    row_map = []
    kinds = Counter()
    for i, old_row in enumerate(mother["rows"]):
        assert old_row["index"] == i
        check_sparse(old_row["nonzero"], BASE_N)
        assert canonical_sha(old_row["nonzero"]) == old_row["sparse_sha256"]
    for k, source_row in enumerate(extension["rows"]):
        check_sparse(source_row["coefficients"], SEMANTIC + NEW_N)
        entries = [[remap(j), value] for j, value in source_row["coefficients"]]
        check_sparse(entries, BASE_N + NEW_N)
        assert all(j < SEMANTIC or j >= BASE_N for j, _ in entries)
        assert all(j != 0 for j, _ in entries)
        target = BASE_M + k
        row = {
            "index": target,
            "name": "single81:" + source_row["name"],
            "sparse_sha256": canonical_sha(entries),
            "nonzero": entries,
            "new_row_kind": source_row["kind"],
            "source_row_index": k,
            "source_row_name": source_row["name"],
        }
        aux = [(j, value) for j, value in entries if j >= BASE_N]
        if source_row["kind"].endswith("threshold"):
            assert len(aux) == 1 and aux[0][1] == "1"
            row["auxiliary_column"] = aux[0][0]
        else:
            assert source_row["kind"].endswith("budget") and aux
            assert all(rational(value) < 0 for _, value in aux)
        for j, value in aux:
            occurrences[j].append((target, source_row["kind"], value))
        rows.append(row)
        kinds[source_row["kind"]] += 1
        row_map.append({
            "source_index": k,
            "target_index": target,
            "source_name": source_row["name"],
            "target_name": row["name"],
            "kind": source_row["kind"],
            "source_object_sha256": canonical_sha(source_row),
            "source_sparse_sha256": canonical_sha(source_row["coefficients"]),
            "target_sparse_sha256": row["sparse_sha256"],
        })
    assert dict(kinds) == {"tail-threshold": 4268, "Z-threshold": 3686, "tail-budget": 24, "Z-budget": 57}
    assert len(columns) == 20585 and len(rows) == 20701
    assert len({row["name"] for row in rows}) == len(rows)
    assert set(occurrences) == set(range(BASE_N, BASE_N + NEW_N))

    column_map = []
    for t, descriptor in enumerate(extension["new_columns"]):
        j = BASE_N + t
        hits = occurrences[j]
        threshold = [hit for hit in hits if hit[1].endswith("threshold")]
        budget = [hit for hit in hits if hit[1].endswith("budget")]
        assert len(hits) == 2 and len(threshold) == len(budget) == 1
        assert threshold[0][2] == "1" and rational(budget[0][2]) < 0
        column_map.append({
            "source_index": SEMANTIC + t,
            "source_new_columns_index": t,
            "target_index": j,
            "descriptor": descriptor,
            "descriptor_sha256": canonical_sha(descriptor),
            "threshold_row": threshold[0][0],
            "budget_row": budget[0][0],
            "budget_coefficient": budget[0][2],
            "canonical_rule": "max(0, -sum(threshold_old_coefficient * old_variable))",
        })
    family_ranges = {}
    for family in FAMILIES:
        cj = [BASE_N + t for t, d in enumerate(extension["new_columns"]) if d["family"] == family]
        ri = [BASE_M + k for k, r in enumerate(extension["rows"]) if r["name"].split(":")[1] == family]
        assert cj == list(range(min(cj), max(cj) + 1))
        assert ri == list(range(min(ri), max(ri) + 1))
        family_ranges[family] = {
            "column_range_inclusive": [min(cj), max(cj)],
            "row_range_inclusive": [min(ri), max(ri)],
            "columns": len(cj),
            "rows": len(ri),
            "source_structure": extension["stats"]["families"][family],
        }
    assert [family_ranges[f]["column_range_inclusive"] for f in FAMILIES] == [[12631, 14764], [14765, 16316], [16317, 17286], [17287, 20584]]
    assert [family_ranges[f]["row_range_inclusive"] for f in FAMILIES] == [[12666, 14820], [14821, 16390], [16391, 17375], [17376, 20700]]

    # Numerical values start here. The pinned decoder retains zero-mass states.
    point_json = load_source("mother_point")
    projection_json = load_source("semantic_projection")
    assert [{k: v for k, v in c.items() if k != "weight"} for c in point_json["columns"]] == mother["columns"]
    assert projection_json["columns"] == point_json["columns"][:SEMANTIC]
    assert projection_json["parent_full_point_sha256"] == sources["mother_point"]["sha256"]
    assert point_json["matrix_sha256"] == sources["mother_matrix"]["sha256"]
    sys.path.insert(0, str((ROOT / SOURCES["semantic_decoder"][0]).parent))
    from transport_separator import Point, ORBITS, STATES, budgets, single_row_lower_cost
    point = Point(ROOT / SOURCES["semantic_projection"][0])
    assert len(point.columns) == SEMANTIC
    assert len(point.hist) == 16 and sum(map(len, point.groups.values())) == 194
    groups = {(hi, freeze(group.key)): group for hi, gs in point.groups.items() for group in gs}
    full_domain = []
    for family in FAMILIES:
        for hi, hist in point.hist.items():
            states = point.family_states[family][hi]
            lo = min(s.terminal_denom - 1 for s in states)
            high = max(s.terminal_denom - 1 for s in states)
            assert [lo, high] == extension["stats"]["families"][family]["load_ranges"][str(hi)]
            for group in point.groups[hi]:
                for member in ("R", "Z"):
                    for threshold in range(lo + 1, high + 1):
                        full_domain.append({"kind": "terminal-query-positive-part", "family": family,
                                            "hist_column": hi, "group": group.key,
                                            "member": member, "threshold": threshold})
                for label in point.labels[family]:
                    full_domain.append({"kind": "reverse-Z-query-positive-part", "family": family,
                                        "hist_column": hi, "group": group.key, "theme": label})
    assert canonical_sha(full_domain) == canonical_sha(extension["new_columns"])

    old_values = [F(c["weight"]) for c in point_json["columns"]]
    assert min(old_values) >= 0
    new_values = []
    auxiliary_diagnostics = []
    for t, descriptor in enumerate(extension["new_columns"]):
        hi = descriptor["hist_column"]
        family = descriptor["family"]
        states = point.family_states[family][hi]
        group = groups[hi, freeze(descriptor["group"])]
        if descriptor["kind"] == "terminal-query-positive-part":
            member = 0 if descriptor["member"] == "R" else 1
            q = sum((mass * state[member] for state, mass in zip(STATES, group.rho)), F())
            high_mass = sum((state.mass for state in states if state.terminal_denom > descriptor["threshold"]), F())
            argument = q - high_mass
            components = {"member_mass": str(q), "high_load_mass": str(high_mass)}
        else:
            assert descriptor["kind"] == "reverse-Z-query-positive-part"
            xi = point.labels[family].index(descriptor["theme"])
            y = sum((state.mass * state.members[xi] for state in states), F())
            q = group.rho[2] + group.rho[3]
            argument = y - q
            components = {"theme_mass": str(y), "R_mass": str(q)}
        value = max(F(), argument)
        mapping = column_map[t]
        threshold_row = rows[mapping["threshold_row"]]
        old_part = [[j, v] for j, v in threshold_row["nonzero"] if j < SEMANTIC]
        assert dot(old_part, old_values) == -argument
        new_values.append(value)
        auxiliary_diagnostics.append({
            "column": BASE_N + t, "threshold_row": mapping["threshold_row"],
            "budget_row": mapping["budget_row"], "argument": str(argument),
            "value": str(value), "threshold_slack": str(value - argument), **components,
        })
    extended_values = old_values + new_values
    mother_slacks = [dot(row["nonzero"], old_values) for row in mother["rows"]]
    assert min(mother_slacks) >= 0
    frozen = load_source("frozen_93_diagnostic")
    assert frozen["full_point_sha256"] == sources["mother_point"]["sha256"]
    assert frozen["input_sha256"] == sources["semantic_projection"]["sha256"]
    frozen_singles = {diagnostic_key(r): r for r in frozen["records"] if r["query"][0] != "new-to-RZ-equal"}
    assert len(frozen_singles) == 81
    budget_values = []
    threshold_slacks = []
    seen_queries = set()
    for k, source_row in enumerate(extension["rows"]):
        row = rows[BASE_M + k]
        value = dot(row["nonzero"], extended_values)
        if source_row["kind"].endswith("threshold"):
            assert value >= 0
            threshold_slacks.append(value)
            continue
        identity = budget_identity(source_row["name"], point.labels)
        row["query_identity"] = identity
        row_map[k]["query_identity"] = identity
        key = diagnostic_key(identity)
        assert key not in seen_queries
        seen_queries.add(key)
        family, orbit, query = key
        spec = (query[0], orbit, *query[1:])
        semantic_budget = budgets(point, family, [spec])[0]
        semantic_cost = single_row_lower_cost(point, family, spec)
        saved = frozen_singles[key]
        assert value == semantic_budget - semantic_cost == F(saved["slack"])
        assert semantic_budget == F(saved["budget"])
        assert semantic_cost == F(saved["minimum_cost"])
        budget_values.append({
            "row_index": row["index"], "row_name": row["name"],
            "source_row_index": k, **identity,
            "budget": str(semantic_budget), "minimum_cost": str(semantic_cost),
            "slack": str(value), "negative": value < 0,
            "matches_frozen_93_single": True,
        })
    assert len(threshold_slacks) == NEW_N and len(budget_values) == 81
    assert seen_queries == set(frozen_singles)
    assert sum(record["negative"] for record in budget_values) == 9 == frozen["single_negative"]
    minimum_budget = min(F(record["slack"]) for record in budget_values)
    assert minimum_budget == F(frozen["minimum_single"])
    assert len(mother["objective"]) == len(mother["normalization"]) == BASE_N
    objective = mother["objective"] + ["0"] * NEW_N
    normalization = mother["normalization"] + ["0"] * NEW_N
    old_W = sum((rational(c) * old_values[j] for j, c in enumerate(mother["objective"]) if c != "0"), F())
    old_O = sum((rational(c) * old_values[j] for j, c in enumerate(mother["normalization"]) if c != "0"), F())
    assert old_W == F(point_json["W"]) and old_O == F(point_json["O"]) == 1
    assert canonical_sha(columns[:BASE_N]) == parent_column_hash
    assert canonical_sha(rows[:BASE_M]) == parent_row_hash
    assert columns[BASE_N:] == extension["new_columns"]
    assert sum(len(row["nonzero"]) for row in rows) == 3044395
    assert source_manifest() == sources
    for check in ("main_mother_verification", "main_projection_verification"):
        assert load_source(check)["status"] == "PASS"

    structure_scope = (
        "Prepared exact extension for the 81 separate single-query minima on the fixed complete state domain. "
        "No optimization; no 12 equal-pair constraints; no common transport, full SPE, or universal welfare assertion. "
        "Main independent coefficient audit is still required."
    )
    matrix = {k: v for k, v in mother.items() if k not in ("columns", "rows", "objective", "normalization")}
    matrix.update({
        "scope": structure_scope,
        "columns": columns, "rows": rows, "row_count": len(rows), "column_count": len(columns),
        "base_row_count": BASE_M, "added_row_count": NEW_M,
        "base_column_count": BASE_N, "added_column_count": NEW_N,
        "objective": objective, "normalization": normalization,
        "mother_metadata": {k: v for k, v in mother.items() if k not in ("columns", "rows", "objective", "normalization")},
        "mother_matrix_path": sources["mother_matrix"]["path"],
        "mother_matrix_sha256": sources["mother_matrix"]["sha256"],
        "single81_structure": {"semantic_prefix_columns": SEMANTIC, "row_kinds": dict(kinds), "families": family_ranges},
        "source_extension_path": sources["extension"]["path"],
        "source_extension_sha256": sources["extension"]["sha256"],
    })
    matrix_info = save_json(outputs["matrix"], matrix)
    # Decode the saved file and compare the full serialized matrix, not just counts.
    with gzip.open(outputs["matrix"], "rt", encoding="utf-8") as handle:
        roundtrip = json.load(handle)
    assert roundtrip == matrix
    del roundtrip

    mapping = {
        "scope": structure_scope,
        "matrix": matrix_info,
        "sources": sources,
        "indexing": "zero based; omitted sparse coefficients are zero; every column is nonnegative",
        "source_column_to_matrix_column": [remap(j) for j in range(SEMANTIC + NEW_N)],
        "mother_columns": [{"source_index": j, "target_index": j, "descriptor_sha256": canonical_sha(c)}
                           for j, c in enumerate(mother["columns"])],
        "mother_rows": [{"source_index": i, "target_index": i, "name": r["name"],
                         "sparse_sha256": r["sparse_sha256"], "object_sha256": canonical_sha(r)}
                        for i, r in enumerate(mother["rows"])],
        "new_columns": column_map,
        "extension_rows": row_map,
        "family_ranges": family_ranges,
        "zero_blocks": {"mother_rows_new_columns": [0, BASE_M, BASE_N, BASE_N + NEW_N],
                        "new_rows_mother_auxiliaries": [BASE_M, BASE_M + NEW_M, SEMANTIC, BASE_N]},
        "elimination": {
            "rule": "Each new variable is max(0, minus its threshold row's old-column linear part).",
            "justification": "It has coefficient +1 in exactly one threshold and a strictly negative coefficient in exactly one budget; objective and normalization are zero.",
            "scope": "Existence of new auxiliary values iff these 81 separate minimum budgets hold, on the inherited legal mass domain.",
        },
        "inherited_full_vector_hash_note": "Legacy full_vector_sha256 fields in preserved mother row objects retain their original provenance. Current whole-width row identity is given by exact sparse entries and sparse_sha256.",
    }
    mapping_info = save_json(outputs["mapping"], mapping)
    changed = sum(value != F(old) for value, old in zip(new_values, extension["canonical_extension_at_input"]["new_weights"]))
    assert changed > 0
    canonical = {
        "scope": "Canonical auxiliary evaluation of the frozen mother opt_v2 point; this extended vector violates 9 budgets and is not feasible.",
        "matrix": matrix_info, "mapping": mapping_info,
        "mother_point": sources["mother_point"], "semantic_projection": sources["semantic_projection"],
        "frozen_93_diagnostic": sources["frozen_93_diagnostic"],
        "exact_feasible": False, "optimizer_calls": 0,
        "new_weight_start_column": BASE_N,
        "new_weights": [str(x) for x in new_values],
        "extended_weights": [str(x) for x in extended_values],
        "auxiliaries": auxiliary_diagnostics,
        "budget_rows": budget_values,
        "threshold_rows_checked": len(threshold_slacks),
        "minimum_threshold_slack": str(min(threshold_slacks)),
        "mother_rows_checked": len(mother_slacks),
        "minimum_mother_slack": str(min(mother_slacks)),
        "negative_budget_rows": 9,
        "minimum_budget_slack": str(minimum_budget),
        "new_positive_columns": sum(x > 0 for x in new_values),
        "new_zero_columns": sum(x == 0 for x in new_values),
        "canonical_values_changed_from_source_old_point": changed,
        "O": str(old_O), "W": str(old_W),
        "old_W_is_not_an_extended_feasible_value": True,
    }
    canonical_info = save_json(outputs["canonical"], canonical)
    structure = {
        "status": "PASS_CONSTRUCTION_CHECKS_PENDING_MAIN_COEFFICIENT_AUDIT",
        "scope": structure_scope,
        "sources": sources,
        "outputs": {"matrix": matrix_info, "mapping": mapping_info, "canonical": canonical_info},
        "script_sha256": sha_file(Path(__file__)),
        "rows": len(rows), "columns": len(columns), "nonzeros": 3044395,
        "mother_rows": BASE_M, "mother_columns": BASE_N, "mother_nonzeros": mother_nonzeros,
        "new_rows": NEW_M, "new_columns": NEW_N, "new_nonzeros": source_nonzeros,
        "new_row_kinds": dict(kinds), "family_ranges": family_ranges,
        "semantic_prefix_sha256": METADATA_SHA,
        "mother_column_objects_sha256": parent_column_hash,
        "mother_row_objects_sha256": parent_row_hash,
        "all_column_descriptors_sha256": canonical_sha(columns),
        "all_row_objects_sha256": canonical_sha(rows),
        "all_sparse_row_hashes_sha256": canonical_sha([row["sparse_sha256"] for row in rows]),
        "mother_rows_and_columns_preserved_exactly": True,
        "projection_equals_full_mother_prefix_including_weights": True,
        "all_new_coefficients_equal_pinned_source_under_index_map": True,
        "all_threshold_and_budget_domains_generated_from_full_descriptors": True,
        "all_threshold_ranges_equal_full_state_load_ranges": True,
        "all_new_column_descriptors_equal_full_domain_in_order": True,
        "objective_and_normalization_zero_extended": True,
        "old_rows_zero_on_new_columns": True,
        "new_rows_zero_on_mother_auxiliary_columns_4849_through_12630": True,
        "new_rows_zero_on_K": True,
        "each_new_column_has_exactly_one_unit_threshold_and_one_negative_budget_coefficient": True,
        "all_sparse_entries_sorted_unique_nonzero_reduced_rational": True,
        "all_row_names_unique": True,
        "saved_matrix_roundtrip_equal_to_constructed_matrix": True,
        "all_frozen_source_hashes_rechecked_unchanged": True,
        "exact_canonical_thresholds_checked": NEW_N,
        "exact_canonical_semantic_budgets_checked": 81,
        "all_81_canonical_budgets_match_frozen_93_singles_exactly": True,
        "negative_canonical_budget_rows": 9,
        "minimum_canonical_budget_slack": str(minimum_budget),
        "mother_rows_rechecked_at_frozen_point": len(mother_slacks),
        "minimum_mother_slack": str(min(mother_slacks)),
        "zero_mass_histograms_retained": sum(point.mass[hi] == 0 for hi in point.hist),
        "zero_mass_family_states_retained": sum(s.mass == 0 for f in point.family_states.values() for states in f.values() for s in states),
        "new_columns_on_zero_mass_histograms_retained": sum(point.mass[d["hist_column"]] == 0 for d in extension["new_columns"]),
        "new_canonical_positive_columns": sum(x > 0 for x in new_values),
        "new_canonical_zero_columns": sum(x == 0 for x in new_values),
        "canonical_values_changed_from_source_old_point": changed,
        "optimizer_calls": 0, "mathematical_float_operations": 0,
        "independent_semantic_coefficient_audit_done_by_this_builder": False,
        "shared_transport_feasibility_claim": False,
        "equal_pair_queries_added": 0,
        "original_six_player_full_domain_half_welfare_question": "OPEN",
    }
    structure_info = save_json(outputs["structure"], structure)
    print(json.dumps({"status": structure["status"], "outputs": {**structure["outputs"], "structure": structure_info},
                      "rows": len(rows), "columns": len(columns), "nonzeros": 3044395,
                      "negative_canonical_budgets": 9}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
