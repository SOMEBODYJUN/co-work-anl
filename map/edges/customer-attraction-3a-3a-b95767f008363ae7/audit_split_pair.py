"""Audit the fixed split PAIR point from saved data and true-row formulas."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, pairwise, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "archives/customer-attraction/tools/evidence"
PAIR = EVIDENCE / "pair-split-cross-points-boss3"
REPLAY = PAIR / "replay/split"
INPUT = EVIDENCE / "split-basic-graph-program/related/split_basic_exact.json"
ZZ_POINT = EVIDENCE / "zz-threshold-closure-program/related/zz_split_exact.json"
POINT = PAIR / "original/pair_closure_exact.json"
TASK = ROOT / "research/operations/map-v2/tasks/customer-attraction-3a-3a-b95767f008363ae7.json"


def load(path):
    return json.loads(path.read_bytes())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def share(numerator, denominator):
    return F(numerator, denominator) if numerator else F()


def group(record):
    family, diagonal, word_i, word_j = record
    return family, diagonal, tuple(word_i), tuple(word_j)


def partition(indices):
    blocks = {}
    return tuple(blocks.setdefault(index, len(blocks)) for index in indices)


def signs(values):
    result = Counter("positive" if value > 0 else "negative" if value < 0 else "zero" for value in values)
    return {name: result[name] for name in ("positive", "zero", "negative")}


def source_structure(columns):
    histograms, state_columns = {}, {}
    for index, column in enumerate(columns):
        if column["kind"] == "hist":
            hist_index = index
            histograms[index] = column
            state_columns[index] = {}
        if column["kind"] == "joint-reply":
            states = state_columns[hist_index].setdefault(group(column["group"]), {})
            state = tuple(column["state"])
            assert state not in states
            states[state] = index
    weights = [F(column["weight"]) for column in columns]
    for hist_index, groups in state_columns.items():
        for states in groups.values():
            assert set(states) == {(0, 1), (1, 0), (1, 1)}
            assert sum(weights[index] for index in states.values()) <= weights[hist_index]
    marginals = {
        (index, member): weights[states[1, 0]] + weights[states[1, 1]]
        for index, groups in state_columns.items() for member, states in groups.items()
    }
    return histograms, state_columns, weights, marginals


def bound_slabs(variables, state_columns, weights, marginals):
    slabs = {}
    variable_index = 0
    for hist_index, groups in state_columns.items():
        mass = weights[hist_index]
        endpoints = sorted({F(), mass, *(marginals[hist_index, member] for member in groups)})
        assert endpoints[0] == 0 and endpoints[-1] == mass
        for left, right in pairwise(endpoints):
            entries = {}
            for member in groups:
                variable = variables[variable_index]
                assert set(variable) == {"hist_column", "left", "right", "group", "r", "weight"}
                assert (variable["hist_column"], F(variable["left"]), F(variable["right"])) == (hist_index, left, right)
                assert group(variable["group"]) == member
                assert variable["r"] == int(right <= marginals[hist_index, member])
                assert 0 <= F(variable["weight"]) <= right - left
                entries[member] = variable_index
                variable_index += 1
            slabs[hist_index, left, right] = entries
    assert variable_index == len(variables)
    return slabs


def membership(slabs, variables, columns, histograms, state_columns, old_weights, marginals):
    zero = F()
    mapped = [old_weights[i] if col["kind"] in {"K", "hist"} else zero for i, col in enumerate(columns)]
    atoms, upper_rows = [], {}
    sizes = defaultdict(F)
    overlap_index = len(variables)
    words = tuple(product(range(2), repeat=3))
    edges = tuple((f, i, j) for f, i, j in product(range(2), range(6), range(6)) if f or i != j)
    orbit_sizes = Counter((f, int(i == j)) for f, i, j in edges)
    for (hist_index, left, right), entries in slabs.items():
        layer_mass = right - left
        local_ids = tuple(entries.values())
        local_weights = {i: F(variables[i]["weight"]) for i in local_ids}
        r_ids = {i for i in local_ids if variables[i]["r"]}
        integrated_z = dict.fromkeys(local_ids, zero)
        integrated_pairs = dict.fromkeys(combinations(local_ids, 2), zero)
        for start, end in pairwise(sorted({zero, layer_mass, *local_weights.values()})):
            z_ids = {i for i in local_ids if end <= local_weights[i]}
            atoms.append({
                "hist_column": hist_index, "R_slab_left": str(left), "R_slab_right": str(right),
                "local_left": str(start), "local_right": str(end), "mass": str(end - start),
                "R_one_variables": sorted(r_ids), "Z_one_variables": sorted(z_ids),
            })
            for index in z_ids:
                integrated_z[index] += end - start
            for pair in combinations(sorted(z_ids), 2):
                integrated_pairs[pair] += end - start
        assert integrated_z == local_weights
        for (i, j), intersection in integrated_pairs.items():
            assert intersection == min(local_weights[i], local_weights[j])
            for index in (i, j):
                upper_rows[f"ZZ-overlap-upper:{overlap_index}:{index}"] = local_weights[index] - intersection
            overlap_index += 1
        hist = histograms[hist_index]
        bits = tuple(map(int, hist["actual_bits"]))
        for index, bit in enumerate(bits, 1):
            sizes[f"actual-{index}"] += bit * layer_mass
        named_words = tuple(word for word, count in zip(words, hist["hist"]) for _ in range(count))
        for index, family in enumerate("TBC"):
            sizes[f"{family}-average"] += layer_mass * F(sum(word[index] for word in named_words), 6)
        for f, i, j in edges:
            diagonal = int(i == j)
            member = f, diagonal, named_words[i], named_words[j]
            index = entries[member]
            orbit_count = orbit_sizes[f, diagonal]
            sizes[f"R-{f}-{diagonal}"] += (layer_mass if index in r_ids else zero) / orbit_count
            sizes[f"Z-{f}-{diagonal}"] += local_weights[index] / orbit_count
        for member, index in entries.items():
            states = state_columns[hist_index][member]
            r = int(index in r_ids)
            mapped[states[r, 1]] += local_weights[index]
            if r:
                mapped[states[1, 0]] += layer_mass - local_weights[index]
    for index, col in enumerate(columns):
        if col["kind"] == "overlap":
            member, other = map(group, col["groups"])
            hist_index = col["hist_column"]
            mapped[index] = min(marginals[hist_index, member], marginals[hist_index, other])
    for hist_index, groups in state_columns.items():
        for member, states in groups.items():
            assert mapped[states[1, 0]] + mapped[states[1, 1]] == marginals[hist_index, member]
            assert sum(mapped[index] for index in states.values()) <= old_weights[hist_index]
    return atoms, mapped, upper_rows, dict(sizes)


def true_rows(slabs, histograms, variables):
    """Expand true index edges and aggregate exact customer formulas."""
    words = tuple(product(range(2), repeat=3))
    patterns = sorted({partition(index) for index in product(range(4), repeat=4)})
    edges = [(f, i, j) for f, i, j in product(range(2), range(6), range(6)) if f or i != j]
    comparison_types = list(product(range(2), range(2), patterns))
    totals = {kind: dict.fromkeys(comparison_types, F()) for kind in ("Z-Z", "RZ", "ZZ")}
    for (hist_index, left, right), entries in slabs.items():
        hist = histograms[hist_index]
        named_words = [word for word, count in zip(words, hist["hist"]) for _ in range(count)]
        assert len(named_words) == 6
        bits = tuple(map(int, hist["actual_bits"]))
        p = sum(bits[:4])
        c, d = bits[4:]
        mass = right - left
        h = share(c, p + c + d) + share(d, p + c + d) + F(c, (p + 1) * (p + 2))
        by_class = Counter(
            ((f, g, partition((i, j, k, l))),
             entries[f, int(i == j), named_words[i], named_words[j]],
             entries[g, int(k == l), named_words[k], named_words[l]])
            for (f, i, j), (g, k, l) in product(edges, repeat=2)
        )
        for (key, i, j), multiplicity in by_class.items():
            r = variables[i]["r"]
            y, z = F(variables[i]["weight"]), F(variables[j]["weight"])
            totals["Z-Z"][key] += multiplicity * (y - z) / (p + 1 + r)
            totals["RZ"][key] += multiplicity * (
                mass * h - (mass * r + z) / (p + 1) + r * z / ((p + 1) * (p + 2))
            )
            totals["ZZ"][key] += multiplicity * (
                mass * h - (y + z) / (p + 1) + min(y, z) / ((p + 1) * (p + 2))
            )
    return {
        "Z_to_Z": {f"Z-Z:{key}": value for key, value in totals["Z-Z"].items()},
        "PAIR_RZ": {str(("RZ", *key)): value for key, value in totals["RZ"].items()},
        "PAIR_ZZ": {str(("ZZ", *key)): value for key, value in totals["ZZ"].items()},
    }


def split_rows(histograms, state_columns, mapped):
    """Evaluate the 16 R and 12 Z budgets separately for the two C-family classes."""
    words = tuple(product(range(2), repeat=3))
    totals = defaultdict(F)
    for index, hist in histograms.items():
        mass = mapped[index]
        named_words = [word for word, count in zip(words, hist["hist"]) for _ in range(count)]
        bits = tuple(map(int, hist["actual_bits"]))
        prefix, p, ell, whole = map(sum, (bits[:3], bits[:4], bits[:5], bits))
        h = share(bits[4] + bits[5], whole) + F(bits[4], (p + 1) * (p + 2))
        n_b, n_c = (F(sum(word[i] for word in named_words), 6) for i in (1, 2))
        for i, j in product(range(6), repeat=2):
            own_word = named_words[i]
            t, b, c = own_word
            chosen = named_words[j][2]
            diag = int(i == j)
            states = state_columns[index][1, diag, own_word, named_words[j]]
            beta, gamma = (share(n, prefix + t + b + c) for n in (b, c))
            denominator = prefix + t + chosen + 1
            measures = {state: mapped[col] for state, col in states.items()}
            measures[0, 0] = mass - sum(measures.values())
            for (r, z), value in measures.items():
                r_rows = {
                    "source": beta - share(chosen, prefix + t + chosen + r),
                    "reverse_terminal": gamma - F(r, prefix + t + b + 1),
                    "price": share(bits[5], whole) - F(r, ell + 1),
                    "capacity": -r,
                }
                query = {
                    "own_B": b, "own_C": c, "own_T": t, "opt_average": F(hist["d"], 6),
                    **{f"actual_{k}": bit for k, bit in enumerate(bits, 1)},
                    "B_average": n_b, "C_average": n_c,
                }
                r_rows.update({f"terminal_{key}": (r - q) / F(denominator) for key, q in query.items()})
                v = share(z, p + r + z)
                z_rows = {
                    "source": share(bits[4], whole) - share(r, p + r + z),
                    "pair": h - F(r + z, p + 1) + F(r * z, (p + 1) * (p + 2)),
                    "price": share(bits[5], whole) - F(z, ell + 1),
                    "capacity": -z,
                    **{f"actual{k}": v - F(bit, p + r + 1) for k, bit in enumerate(bits)},
                    "ownR": v - F(r, p + r + 1),
                    "reverseR": F(r - z, denominator),
                }
                for name, family in (("R", r_rows), ("Z", z_rows)):
                    for key, coefficient in family.items():
                        totals[str((name, diag, key))] += value * coefficient
    for name, diag in product(("R", "Z"), range(2)):
        totals[str((name, diag, "capacity"))] += (6 if diag else 30) * mapped[0]
    return dict(totals)


def prices(histograms, capacity):
    words = tuple(product(range(2), repeat=3))
    actual = [F()] * 6
    each = {(index, family): F() for index, family in product(range(6), (1, 2))}
    family_mass = dict.fromkeys((1, 2), F())
    total_mass, welfare, optimum = F(), F(), F()
    for hist in histograms.values():
        mass = F(hist["weight"])
        bits = tuple(map(int, hist["actual_bits"]))
        menu_counts = tuple(sum(count * word[i] for count, word in zip(hist["hist"], words)) for i in range(3))
        assert sum(hist["hist"]) == 6 and menu_counts[0] == hist["d"] == 1
        total_mass += mass
        welfare += bool(sum(bits)) * mass
        optimum += bool(menu_counts[0]) * mass
        for i, bit in enumerate(bits):
            actual[i] += mass * share(bit, sum(bits))
            for family in (1, 2):
                each[i, family] += mass * F(menu_counts[family], sum(bits[:i]) + 6 - i)
        for family in (1, 2):
            family_mass[family] += mass * menu_counts[family]
    assert sum(actual) == welfare
    rows = {f"actual-floor:{(i, family)}": 6 * actual[i] - quote for (i, family), quote in each.items()}
    rows.update({f"old-capacity:{f}": 6 * capacity - mass for f, mass in family_mass.items()})
    return rows, actual, total_mass, welfare, optimum


def main():
    task = load(TASK)["definition"]
    refs = []
    for ref in task["context_plan"]["reading_refs"]:
        path = ROOT / ref["path"]
        data = path.read_bytes()
        assert digest(path) == ref["sha256"]
        refs.append({**ref, "bytes": len(data), "lines": len(data.splitlines())})

    point, source, zz = map(load, (POINT, INPUT, ZZ_POINT))
    assert set(point) == {"scope", "W", "O", "rows", "original_Z_variables", "overlap_variables",
                          "minimum_slack", "free_vertex_variables", "variables"}
    assert (source["verified_rows"], len(source["columns"]), zz["rows"], point["rows"]) == (3945, 1905, 4005, 7931)
    assert digest(INPUT) == zz["source_sha256"]
    variables = point["variables"]
    zz_variables = zz["variables"]
    assert len(variables) == len(zz_variables) == point["original_Z_variables"] == 275
    for one, other in zip(variables, zz_variables):
        assert {k: v for k, v in one.items() if k != "weight"} == {k: v for k, v in other.items() if k != "weight"}
    changed = [i for i, (one, other) in enumerate(zip(variables, zz_variables))
               if F(one["weight"]) != F(other["weight"])]
    assert len(changed) == 103

    histograms, state_columns, old_weights, marginals = source_structure(source["columns"])
    assert Counter(column["kind"] for column in source["columns"]) == {
        "K": 1, "hist": 16, "joint-reply": 582, "overlap": 1306
    }
    assert len(marginals) == 194 and sum(bool(old_weights[i]) for i in histograms) == 10
    slabs = bound_slabs(variables, state_columns, old_weights, marginals)
    assert slabs == bound_slabs(zz_variables, state_columns, old_weights, marginals)
    assert len(slabs) == 22
    boundary = Counter(
        "zero" if not F(var["weight"]) else "upper" if F(var["weight"]) == F(var["right"]) - F(var["left"]) else "interior"
        for var in variables
    )
    assert boundary == {"zero": 124, "upper": 91, "interior": 60}
    assert boundary["interior"] == point["free_vertex_variables"]

    atoms, mapped, upper_rows, sizes = membership(
        slabs, variables, source["columns"], histograms, state_columns, old_weights, marginals
    )
    recipe = load(REPLAY / "common-cube-atom-recipe.json")
    assert atoms == recipe["atoms"] and len(atoms) == 33
    assert sum(F(atom["mass"]) for atom in atoms) == F(recipe["total_mass"]) == 1
    assert recipe["all_Z_integrals_checked"] == len(variables)
    assert len(upper_rows) == 2 * recipe["all_ZZ_min_intersections_checked"] == 2 * point["overlap_variables"]
    mapped_file = load(REPLAY / "mapped-1905-weights.json")
    assert mapped_file["fixed_source_sha256"] == digest(INPUT)
    assert mapped == list(map(F, mapped_file["weights"]))
    changes = Counter(column["kind"] for column, old, new in zip(source["columns"], old_weights, mapped) if old != new)
    assert changes == {"joint-reply": 116, "overlap": 193}
    frechet_failures = []
    for i, col in enumerate(source["columns"]):
        if col["kind"] == "overlap":
            index = col["hist_column"]
            first, second = (marginals[index, group(value)] for value in col["groups"])
            lower = max(F(), first + second - old_weights[index])
            assert lower <= mapped[i] == min(first, second)
            if old_weights[i] < lower:
                frechet_failures.append(i)
    assert len(frechet_failures) == 189 and 992 in frechet_failures
    assert max(sizes.values()) == old_weights[0]
    assert {name for name, value in sizes.items() if value == old_weights[0]} == {"R-1-0", "R-1-1"}

    price_rows, actual, mass, welfare, optimum = prices(histograms, old_weights[0])
    assert mass == optimum == F(point["O"]) == F(zz["O"]) == F(source["O"]) == 1
    assert welfare == F(point["W"]) == F(zz["W"]) == F(source["W"]) < F(1, 2)
    price_audit = load(EVIDENCE / "cross-source-graph-program/added-row-slacks.json")["split_point"]
    assert price_rows == {row["name"]: F(row["slack"]) for row in price_audit}
    history = load(PAIR / "replay/preserved-margins-and-history.json")
    for row in history["point_comparisons"]["split"]["old_14_values"]:
        assert price_rows[row["name"]] == F(row["new_slack"]) == F(row["old_saved_slack"])
    historical = history["historical_7931_report"]
    historical_path = ROOT / historical["file"]
    historic_data = load(historical_path)
    assert digest(historical_path) == historical["sha256"]
    assert digest(POINT) == historic_data["point_sha256"]
    assert historic_data["source_sha256"] == historical["historical_code_sha256"] != historical["current_code_sha256"]
    assert (historic_data["rows"], F(historic_data["W"]), F(historic_data["minimum_slack"])) == (7931, welfare, F())

    rows = load(REPLAY / "all-row-slacks.json")
    assert len(rows) == point["rows"]
    assert all(set(row) == {"row", "name", "slack"} and row["row"] == i for i, row in enumerate(rows))
    assert len({row["name"] for row in rows}) == len(rows)
    row_parts = {
        name: {row["name"]: F(row["slack"]) for row in rows[start:end]}
        for name, start, end in [
            ("old_affine", 0, 3945), ("Z_to_Z", 3945, 4005), ("PAIR_RZ", 4005, 4065),
            ("PAIR_ZZ", 4065, 4125), ("overlap_upper", 4125, 7931)
        ]
    }
    split_values = split_rows(histograms, state_columns, mapped)
    assert split_values == {row["name"]: F(row["slack"]) for row in rows[3889:3945]}
    new_rows = true_rows(slabs, histograms, variables)
    zz_rows = true_rows(slabs, histograms, zz_variables)
    assert all(row_parts[name] == values for name, values in new_rows.items())
    assert row_parts["overlap_upper"] == upper_rows
    stats = {name: signs(part.values()) for name, part in row_parts.items()}
    assert sum(part["positive"] for part in stats.values()) == 1756
    assert sum(part["zero"] for part in stats.values()) == 6175
    assert not any(part["negative"] for part in stats.values())
    execution = load(REPLAY / "execution-record.json")
    assert (execution["mode"], execution["exit_code"], execution["original_build_calls"]) == ("split", 0, 1)
    assert execution["original_CLI_called"] is execution["optimizer_called"] is False
    saved = load(REPLAY / "semantic-and-full-matrix-report.json")
    assert saved["point_sha256"] == digest(POINT) and saved["fixed_source_sha256"] == digest(INPUT)
    assert saved["program_sha256"] == historical["current_code_sha256"]
    assert {key: F(value) for key, value in saved["orbit_theme_sizes"].items()} == sizes
    assert saved["effective_argv"][1:] == ["--split"]

    zz_rerun = EVIDENCE / "zz-split-exact-point/rerun"
    zz_execution = load(zz_rerun / "execution.json")
    zz_stdout = load(zz_rerun / "stdout.txt")
    zz_dependencies = {Path(row["original_path"]).name: row["sha256"]
                       for row in load(zz_rerun / "runtime-manifest.json")}
    assert zz_execution["argv"][-2:] == ["--split", "--verify"]
    assert zz_execution["exit_code"] == 0 and zz_execution["LP_calls"] == 0
    assert zz_execution["assertions_enabled"] and zz_execution["original_functions_modified"] is False
    assert digest(zz_rerun / "stdout.txt") == zz_execution["stdout_sha256"]
    assert (zz_stdout["verified_rows"], zz_stdout["variables"], F(zz_stdout["minimum_slack"]), F(zz_stdout["W"])) == (
        4005, 275, F(), welfare
    )
    assert zz_dependencies["zz_threshold_closure.py"] == saved["zz_program_sha256"]
    assert zz_dependencies["zz_split_exact.json"] == digest(ZZ_POINT)
    assert zz_dependencies["split_basic_exact.json"] == digest(INPUT)
    zz_atoms, zz_mapped, zz_bounds, zz_sizes = membership(
        slabs, zz_variables, source["columns"], histograms, state_columns, old_weights, marginals
    )
    assert len(zz_atoms) == 43 and len(zz_bounds) == 3806
    assert all(value >= 0 for value in zz_bounds.values())
    assert all(value >= 0 for part in zz_rows.values() for value in part.values())

    result = {
        "declared_reads": refs,
        "fixed_input_sha256": digest(INPUT), "pair_point_sha256": digest(POINT), "zz_4005_point_sha256": digest(ZZ_POINT),
        "fixed_histograms": 16, "positive_histograms": 10, "fixed_R_groups": len(marginals), "R_slabs": len(slabs),
        "Z_variable_bounds": dict(boundary), "simultaneously_realized_ZZ_minima": len(upper_rows) // 2,
        "representative_atoms": len(atoms), "remapped_coordinate_changes": dict(changes),
        "fixed_input_original_RR_lower_bound_failures": len(frechet_failures),
        "first_short_example_old_RR_col_992": {"old": str(old_weights[992]), "new": str(mapped[992])},
        "actual_profits": [str(value) for value in actual],
        "mass_and_optimum": str(optimum), "W": str(welfare), "K": str(old_weights[0]),
        "catalogue_orbit_theme_sizes": {key: str(value) for key, value in sizes.items()},
        "pricing_and_capacity_rows": {key: str(value) for key, value in price_rows.items()},
        "saved_7931_row_signs": stats,
        "split_rows_on_7931_point": signs(split_values.values()),
        "zz_4005_comparison": {
            "identical_descriptors": True, "same_fixed_input": True, "same_W": True,
            "changed_Z_indices": changed,
            "independent_row_signs_at_4005_point": {name: signs(part.values()) for name, part in zz_rows.items()},
            "exact_PAIR_rows_at_4005_point_using_its_own_ZZ_minima": {
                row: str(value) for name in ("PAIR_RZ", "PAIR_ZZ") for row, value in zz_rows[name].items()
            },
            "minimum_PAIR_slack_over_nonempty_classes": {
                name: str(min(value for value in zz_rows[name].values() if value)) for name in ("PAIR_RZ", "PAIR_ZZ")
            },
            "same_frozen_ZZ_coefficient_builder": saved["zz_program_sha256"],
            "independent_overlap_upper_signs": signs(zz_bounds.values()),
            "positive_representative_atoms": len(zz_atoms),
            "changed_remapped_coordinates_vs_7931_point": sum(x != y for x, y in zip(zz_mapped, mapped)),
            "maximum_theme_size_after_index_averaging": str(max(zz_sizes.values())),

        },
        "historical_report": historical,
        "verification_boundary": (
            "Independently reconstructed all split variable metadata, atoms, 1905 weights, 180 indexed true rows, "
            "3806 overlap bounds, all 56 inherited split budgets, and 14 omitted price/capacity diagnostics; read all 7931 saved exact slacks. "
            "The other 3889 inherited affine rows rely on the completed original build and replay. No optimizer or whole-matrix builder ran in this audit."
        ),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
