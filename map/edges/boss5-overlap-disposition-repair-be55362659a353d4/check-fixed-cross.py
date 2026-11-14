"""Reconstruct the fixed cross common-membership witness with exact arithmetic."""

import ast
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import lcm
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "archives/customer-attraction/tools/evidence"
CROSS = "zz-cross-exact-point"
STATES = {(0, 1), (1, 0), (1, 1)}
FLAGS = ["--cross", "--priced", "--optimum", "--verify"]
SOURCE_SHA = "955c456ad3381a8cdc72139ba9ccc73dfe70297183e72727ae6ad165dc80e947"
POINT_SHA = "239ab62a100cd77f12cc9b8d131048e87babccb2103c781953af33909c364111"


def load(relative):
    path = EVIDENCE / relative
    raw = path.read_bytes()
    return json.loads(raw), sha256(raw).hexdigest()


def group_key(description):
    family, diagonal, first, second = description
    return family, diagonal, tuple(first), tuple(second)


def partition(indices):
    classes = {}
    return tuple(classes.setdefault(i, len(classes)) for i in indices)


def exact_atoms(mass, weights):
    possible = []
    for weight in weights:
        assert 0 <= weight <= mass
        choices = [(0, mass - weight), (1, weight)]
        possible.append([(bit, value / mass) for bit, value in choices if value])
    atoms = {}
    for outcome in product(*possible):
        weight = mass
        bits = []
        for bit, probability in outcome:
            weight *= probability
            bits.append(str(bit))
        atoms["".join(bits)] = weight
    return atoms


def sign_counts(values):
    counts = Counter("positive" if x > 0 else "negative" if x < 0 else "zero" for x in values)
    return {key: counts[key] for key in ("positive", "zero", "negative")}


def main():
    old, old_sha = load("cross-source-graph-program/related/cross_source_priced_optimum_exact.json")
    point, point_sha = load("zz-threshold-closure-program/related/zz_cross_exact.json")
    saved_cube, cube_sha = load(f"{CROSS}/conditional-cube-atoms.json")
    saved_lift, lift_sha = load(f"{CROSS}/rerun/affine-lifted-weights.json")
    rows, rows_sha = load(f"{CROSS}/rerun/all-row-slacks.json")
    run, run_sha = load(f"{CROSS}/rerun/execution.json")
    assert old_sha == SOURCE_SHA == point["source_sha256"]
    assert point_sha == POINT_SHA
    assert run["effective_argv"] == FLAGS and run["all_saved_descriptors_match_generated_order"]
    assert run["input_hashes_before_and_after"]["zz_cross_exact.json"] == point_sha
    assert run["input_hashes_before_and_after"]["cross_source_priced_optimum_exact.json"] == old_sha
    assert run["artifacts"]["affine-lifted-weights.json"]["sha256"] == lift_sha
    assert run["artifacts"]["all-row-slacks.json"]["sha256"] == rows_sha
    assert run["original_main_calls"] == 1 and run["linprog_calls"] == 0

    columns = old["columns"]
    old_weights = [Fraction(col["weight"]) for col in columns]
    histograms = {}
    overlaps = defaultdict(list)
    for index, column in enumerate(columns):
        if column["kind"] == "hist":
            histogram = index
            histograms[histogram] = {}
        elif column["kind"] == "joint-reply":
            groups = histograms[histogram]
            key = group_key(column["group"])
            state = tuple(column["state"])
            assert state not in groups.setdefault(key, {})
            groups[key][state] = index
        elif column["kind"] == "overlap":
            overlaps[column["hist_column"]].append(index)
        else:
            assert index == 0 and column["kind"] == "K"

    all_words = list(product(range(2), repeat=3))
    edges = [(family, i, j) for family, i, j in product(range(2), range(6), range(6)) if family or i != j]
    assert len(edges) == 66
    lift = [Fraction()] * len(columns)
    lift[0] = old_weights[0]
    cube = []
    free_counts = Counter()
    zz = defaultdict(Fraction)
    positive = interior = 0
    cursor = 0
    welfare = profit = query = Fraction()
    for histogram, groups in histograms.items():
        h = columns[histogram]
        mass = old_weights[histogram]
        lift[histogram] = mass
        a = tuple(map(int, h["actual_bits"]))
        if any(a):
            welfare += mass
        if a[2]:
            profit += mass / sum(a)
        words = [w for w, count in zip(all_words, h["hist"], strict=True) for _ in range(count)]
        assert len(words) == 6 and sum(w[0] for w in words) == h["d"] == 1
        q = {}
        for g, states in groups.items():
            assert set(states) == STATES
            values = {state: old_weights[index] for state, index in states.items()}
            assert min(values.values()) >= 0 and sum(values.values()) <= mass
            q[g] = values[1, 0] + values[1, 1]

        ordered_groups = tuple(groups)
        positions = {g: local for local, g in enumerate(ordered_groups)}
        edge_positions = [positions[family, int(i == j), words[i], words[j]] for family, i, j in edges]
        for (family, _, _), local in zip(edges, edge_positions, strict=True):
            if family == 0:
                query += q[ordered_groups[local]] / (sum(a[:2]) + 4)

        endpoints = sorted({Fraction(), mass, *q.values()})
        for left, right in zip(endpoints, endpoints[1:]):
            size = right - left
            start = cursor
            r = [int(right <= q[g]) for g in groups]
            weights = []
            for (g, bit) in zip(groups, r, strict=True):
                record = point["variables"][cursor]
                assert (record["hist_column"], Fraction(record["left"]), Fraction(record["right"]),
                        group_key(record["group"]), record["r"]) == (histogram, left, right, g, bit)
                weights.append(Fraction(record["weight"]))
                cursor += 1

            atoms = exact_atoms(size, weights)
            interior_count = sum(0 < value < size for value in weights)
            assert len(atoms) == 2 ** interior_count and sum(atoms.values()) == size
            free_counts[interior_count] += 1
            interior += interior_count
            positive += sum(value > 0 for value in weights)
            recorded = saved_cube["slabs"][len(cube)]
            assert (recorded["hist_column"], Fraction(recorded["left"]), Fraction(recorded["right"])) == (histogram, left, right)
            assert recorded["variable_indices"] == list(range(start, cursor))
            assert recorded["R_bits"] == "".join(map(str, r)) and recorded["free_Z_count"] == interior_count
            assert len(recorded["atoms"]) == len(atoms)
            assert {item["Z_bits"]: Fraction(item["mass"]) for item in recorded["atoms"]} == atoms
            cube.append(atoms)

            z = [
                sum((weight for bits, weight in atoms.items() if bits[local] == "1"), Fraction())
                for local in range(len(groups))
            ]
            assert z == weights
            for bits, weight in atoms.items():
                for local, states in enumerate(groups.values()):
                    state = (r[local], int(bits[local]))
                    if state in STATES:
                        lift[states[state]] += weight
            for index in overlaps[histogram]:
                g1, g2 = map(group_key, columns[index]["groups"])
                if r[positions[g1]] and r[positions[g2]]:
                    lift[index] += size

            actual_prefix = sum(a[:4])
            for (f, i, j), e in zip(edges, edge_positions, strict=True):
                denominator = actual_prefix + 1 + r[e]
                for (g, k, ell), other in zip(edges, edge_positions, strict=True):
                    zz[f, g, partition((i, j, k, ell))] += (z[e] - z[other]) / denominator

        for g, states in groups.items():
            assert lift[states[1, 0]] + lift[states[1, 1]] == q[g]
        for index in overlaps[histogram]:
            g1, g2 = map(group_key, columns[index]["groups"])
            assert lift[index] == min(q[g1], q[g2])

    assert cursor == point["variables_count"] == len(point["variables"]) == 302
    assert len(cube) == len(saved_cube["slabs"]) == 24
    assert sum(map(len, cube)) == 227
    assert positive == point["positive_variables"] == 119 and interior == 28
    assert free_counts == {0: 13, 1: 5, 2: 3, 5: 2, 7: 1}
    assert lift == list(map(Fraction, saved_lift)) and len(lift) == 1905
    changes = Counter(c["kind"] for c, before, after in zip(columns, old_weights, lift, strict=True) if before != after)
    assert changes == {"joint-reply": 88, "overlap": 180}
    r_group_count = sum(map(len, histograms.values()))
    z_changes = sum(
        old_weights[states[0, 1]] + old_weights[states[1, 1]] != lift[states[0, 1]] + lift[states[1, 1]]
        for groups in histograms.values() for states in groups.values()
    )
    assert r_group_count == 194 and z_changes == 62
    assert welfare == Fraction(old["W"]) == Fraction(point["W"]) < Fraction(1, 2)
    assert sum(lift[h] for h in histograms) == Fraction(point["O"]) == 1
    scale = 720 * lcm(*(weight.denominator for atoms in cube for weight in atoms.values()))
    assert str(scale) == saved_cube["unit_customer_scale_after_720_permutations"]
    assert all((weight * scale / 720).denominator == 1 for atoms in cube for weight in atoms.values())

    assert len(rows) == run["total_rows"] == point["rows"] == 4987
    assert [row["index"] for row in rows] == list(range(4987))
    exact_slacks = [Fraction(row["slack"]) for row in rows]
    assert min(exact_slacks) == 0
    assert all(not row["name"].startswith("Z-Z:") for row in rows[:4927])
    keys = set()
    for row, slack in zip(rows[4927:], exact_slacks[4927:], strict=True):
        assert row["name"].startswith("Z-Z:")
        key = ast.literal_eval(row["name"][4:])
        assert key not in keys and slack == zz.get(key, 0)
        keys.add(key)
    assert len(keys) == 60 and len(zz) == 42 and zz.keys() <= keys
    assert sign_counts(exact_slacks[:4927]) == {"positive": 2427, "zero": 2500, "negative": 0}
    assert sign_counts(exact_slacks[4927:]) == {"positive": 19, "zero": 41, "negative": 0}
    floor = 30 * profit - query
    assert floor == Fraction(-4749850661723892253166888285611, 107365313311072858536618851786648)
    result = {
        "scope": "Exact direct threshold reconstruction, common-membership atomization, ZZ aggregates and one omitted R FLOOR. The old 4927 coefficients come from the frozen verifier event.",
        "source_sha256": old_sha,
        "point_sha256": point_sha,
        "original_event_sha256": run_sha,
        "original_event_flags": FLAGS,
        "saved_rows_sha256": rows_sha,
        "saved_lift_sha256": lift_sha,
        "saved_atoms_sha256": cube_sha,
        "histograms": len(histograms),
        "positive_histograms": sum(old_weights[h] > 0 for h in histograms),
        "slabs": len(cube),
        "all_source_variable_descriptors_and_z_marginals_matched": cursor,
        "z_weight_counts": {"zero": cursor - positive, "upper": positive - interior, "interior": interior},
        "free_z_histogram": dict(sorted(free_counts.items())),
        "all_saved_atom_assignments_and_masses_matched": sum(map(len, cube)),
        "all_original_lift_coordinates_matched": len(lift),
        "unchanged_r_marginals": r_group_count,
        "changed_z_marginals": z_changes,
        "changed_original_coordinates": dict(changes),
        "saved_old_cross_row_sign_counts": sign_counts(exact_slacks[:4927]),
        "independently_evaluated_zz_row_sign_counts": sign_counts(exact_slacks[4927:]),
        "zz_structurally_empty_rows": len(keys) - len(zz),
        "all_rows_sign_counts": sign_counts(exact_slacks),
        "unit_scale_decimal_digits_after_720_permutations": len(str(scale)),
        "normalized_membership_catalog_opt_6": "1",
        "normalized_specified_path_welfare": str(welfare),
        "actual_third_profit": str(profit),
        "family_0_off_diagonal_r_query_sum": str(query),
        "omitted_actual_third_r_floor": str(floor),
        "original_verifier_runs_in_this_review": 0,
        "lp_runs_in_this_review": 0,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
