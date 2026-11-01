"""Independent integer-customer realization of all frozen F/G/U entries.

Enumerates full six-index multiset arrangements and actual threshold atoms.
Does not import or run the author's canonical/moment generator, an LP, or a
game solver.  Only standard-library exact arithmetic is used.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / "full156-tail-parent-report/original/research_5"
EXPECTED = {
    "kernel": "876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4",
    "point": "d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8",
    "pair": "090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2",
}


def read_exact(path, identity):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED[identity]
    return json.loads(raw), {"sha256": digest, "bytes": len(raw)}


def group_key(raw):
    family, diagonal, left, right = raw
    return family, diagonal, tuple(left), tuple(right)


def label(action):
    if len(action) == 2:
        return action[0] + str(action[1] + 1)
    return f"{action[0]}_{action[1]}_{action[2] + 1}_{action[3] + 1}"


def orbit_key(actions):
    seen, out = {}, []
    def index(i):
        if i not in seen:
            seen[i] = len(seen)
        return seen[i]
    for action in actions:
        if action[0] == "A":
            out.append(action)
        elif len(action) == 2:
            out.append((action[0], index(action[1])))
        else:
            out.append((action[0], action[1], index(action[2]), index(action[3])))
    return tuple(out), len(seen)


def main():
    if not __debug__:
        raise RuntimeError("Assertions must remain enabled; do not use -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", type=Path, default=HERE.parent / "full156-pair-master-point/original/pair_master_exact.json")
    args = parser.parse_args()
    kernel, kernel_meta = read_exact(SHARED / "full156_tail2_kernel_10344.json", "kernel")
    point, point_meta = read_exact(SHARED / "combined_branch_master_exact.json", "point")
    pair, pair_meta = read_exact(args.pair, "pair")
    assert set(kernel) == {
        "scope", "source_sha256", "pair_source_sha256", "original_labels",
        "original_descriptors", "aliases", "topics", "players", "fixed_prefix",
        "actual_last_pair", "unit_customer_scale", "payoff_denominator_for_normalized_point",
        "F_numerators", "G_numerators", "payoff_numerators", "actual_payoff_numerators",
        "source_W", "kernel_classes", "seconds",
    }
    assert kernel["source_sha256"] == point_meta["sha256"]
    assert kernel["pair_source_sha256"] == pair_meta["sha256"]

    # A joint-reply block follows its current hist column.  Its old index is
    # retained only as a consistent legacy label, not used as a current offset.
    hist, current, denominators = {}, None, []
    legacy_mismatches = 0
    for position, column in enumerate(point["columns"]):
        value = F(column["weight"])
        assert value >= 0
        if column["kind"] == "hist":
            current = position
            actual = tuple(map(int, column["actual_bits"]))
            counts = tuple(column["hist"])
            assert len(actual) == 6 and set(actual) <= {0, 1}
            assert len(counts) == 8 and sum(counts) == 6 and min(counts) >= 0
            hist[position] = {"actual": actual, "counts": counts, "mass": value,
                              "raw": {}, "slabs": {}, "legacy": set()}
            denominators.append(value.denominator)
        elif column["kind"] == "joint-reply":
            key, state = group_key(column["group"]), tuple(column["state"])
            states = hist[current]["raw"].setdefault(key, {})
            assert state not in states
            states[state] = value
            hist[current]["legacy"].add(column["hist_column_old"])
            legacy_mismatches += column["hist_column_old"] != current
        else:
            assert column["kind"] in ("K", "overlap")
    assert len(hist) == 16
    for data in hist.values():
        assert len(data["legacy"]) == 1
        data["radius"] = {}
        for key, states in data["raw"].items():
            assert set(states) == {(0, 1), (1, 0), (1, 1)}
            assert sum(states.values()) <= data["mass"]  # omitted 00 mass
            radius = states[1, 0] + states[1, 1]
            data["radius"][key] = radius
            denominators.append(radius.denominator)
    assert len({next(iter(data["legacy"])) for data in hist.values()}) == 16
    for variable in pair["variables"]:
        data = hist[variable["hist_column"]]
        left, right = F(variable["left"]), F(variable["right"])
        key = group_key(variable["group"])
        bit, weight = variable["r"], F(variable["weight"])
        assert bit in (0, 1) and 0 <= weight <= right - left
        slab = data["slabs"].setdefault((left, right), {})
        assert key not in slab
        slab[key] = bit, weight
        denominators.append(weight.denominator)

    scale = 720 * lcm(*denominators)
    denominator = 60 * scale
    assert scale == int(kernel["unit_customer_scale"])
    assert denominator == int(kernel["payoff_denominator_for_normalized_point"])
    assert kernel["players"] == 6 and kernel["fixed_prefix"] == [0, 1, 2, 3]
    assert kernel["actual_last_pair"] == [4, 5]
    assert point["O"] == pair["O"] == "1"
    assert F(point["W"]) == F(pair["W"]) == F(kernel["source_W"])

    actions = [("A", i) for i in range(6)]
    actions += [(family, i) for family in ("T", "B", "C") for i in range(6)]
    actions += [(family, k, i, j) for family in ("R", "Z")
                for k, i, j in product(range(2), range(6), range(6)) if k or i != j]
    assert len(actions) == 156
    labels = [label(action) for action in actions]
    assert kernel["original_descriptors"] == list(map(list, actions))
    assert kernel["original_labels"] == kernel["topics"] == labels
    assert kernel["aliases"] == list(range(156))

    # Full named-index realization, without canonicalization or falling-factorial
    # moments: every distinct arrangement of each six-word multiset is present.
    patterns = list(product((0, 1), repeat=3))
    atoms, atom_records, details = defaultdict(int), 0, []
    for hist_index, data in hist.items():
        if not data["mass"]:
            assert not data["slabs"]
            continue
        words = [patterns[j] for j, count in enumerate(data["counts"]) for _ in range(count)]
        arrangements = sorted(set(permutations(words)))
        count = len(arrangements)
        assert 720 % count == 0
        assert all(sum(word[0] for word in row) == 1 for row in arrangements)
        previous, subslabs, hist_atoms = F(0), 0, 0
        for (left, right), slab in sorted(data["slabs"].items()):
            assert left == previous and right > left
            previous = right
            assert set(slab) == set(data["radius"])
            for key, (bit, weight) in slab.items():
                radius = data["radius"][key]
                assert (bit == 1 and radius >= right) or (bit == 0 and radius <= left)
            cuts = sorted({F(0), right - left, *[weight for bit, weight in slab.values()]})
            subslabs += len(cuts) - 1
            for low, high in zip(cuts, cuts[1:]):
                mass = scale * (high - low) / count
                assert mass.denominator == 1 and mass > 0
                midpoint = (low + high) / 2
                for row in arrangements:
                    mask = 0
                    for i, action in enumerate(actions):
                        if action[0] == "A":
                            covered = data["actual"][action[1]]
                        elif action[0] in ("T", "B", "C"):
                            covered = row[action[1]][("T", "B", "C").index(action[0])]
                        else:
                            key = action[1], int(action[2] == action[3]), row[action[2]], row[action[3]]
                            bit, weight = slab[key]
                            covered = bit if action[0] == "R" else midpoint < weight
                        if covered:
                            mask |= 1 << i
                    assert mask > 0 and ((mask >> 6) & 63).bit_count() == 1
                    atoms[mask] += int(mass)
                    atom_records += 1
                    hist_atoms += 1
        assert previous == data["mass"]
        details.append({"hist_column": hist_index, "mass": str(data["mass"]),
                        "named_arrangements": count, "R_slabs": len(data["slabs"]),
                        "Z_subslabs": subslabs, "atom_records": hist_atoms})
    assert len(details) == 10 and atom_records == len(atoms) == 1590
    assert sum(atoms.values()) == scale

    # One unit customer with fixed prefix load p contributes 60/(p+1)
    # to F and 60/((p+1)(p+2)) to G.  All such factors are integers.
    first, overlap = [0] * 156, [[0] * 156 for _ in range(156)]
    actual_payoff = [0] * 6
    actual_coverage = 0
    for mask, count in atoms.items():
        prefix_load = (mask & 15).bit_count()
        assert 60 % (prefix_load + 1) == 0
        assert 60 % ((prefix_load + 1) * (prefix_load + 2)) == 0
        first_amount = count * (60 // (prefix_load + 1))
        overlap_amount = count * (60 // ((prefix_load + 1) * (prefix_load + 2)))
        members = [i for i in range(156) if (mask >> i) & 1]
        for i in members:
            first[i] += first_amount
            for j in members:
                overlap[i][j] += overlap_amount
        actual_load = (mask & 63).bit_count()
        if actual_load:
            actual_coverage += count
            for i in range(6):
                if mask & (1 << i):
                    actual_payoff[i] += count * (60 // actual_load)
    payoffs = [[first[i] - overlap[i][j] for j in range(156)] for i in range(156)]
    assert len(kernel["F_numerators"]) == 156
    assert all(len(row) == 156 for row in kernel["G_numerators"] + kernel["payoff_numerators"])
    assert len(kernel["G_numerators"]) == len(kernel["payoff_numerators"]) == 156
    for field in (kernel["F_numerators"], *kernel["G_numerators"], *kernel["payoff_numerators"]):
        assert all(isinstance(v, str) and v.isdigit() for v in field)
    assert first == list(map(int, kernel["F_numerators"]))
    assert overlap == [list(map(int, row)) for row in kernel["G_numerators"]]
    assert payoffs == [list(map(int, row)) for row in kernel["payoff_numerators"]]
    assert all(overlap[i][j] == overlap[j][i] for i in range(156) for j in range(156))
    assert all(overlap[i][i] + overlap[j][j] - 2 * overlap[i][j] > 0
               for i in range(156) for j in range(i))
    assert min(v for row in payoffs for v in row) > 0
    assert actual_payoff[4:] == [payoffs[4][5], payoffs[5][4]] == list(map(int, kernel["actual_payoff_numerators"]))
    assert sum(actual_payoff) == 60 * actual_coverage
    assert F(actual_coverage, scale) == F(kernel["source_W"])

    # This reproduces only the reported cache-key count, independently of the
    # atom-based matrix computation above; it is not a count of customer types.
    unary = {orbit_key([action]) for action in actions}
    pairs = {min(orbit_key([left, right]), orbit_key([right, left]))
             for i, left in enumerate(actions) for right in actions[i:]}
    assert len(unary) == 15 and len(pairs) == 231
    assert len(unary | pairs) == kernel["kernel_classes"] == 246
    canonical_atoms = [[hex(mask), str(count)] for mask, count in sorted(atoms.items())]
    atom_bytes = json.dumps(canonical_atoms, separators=(",", ":")).encode()
    atom_digest = hashlib.sha256(atom_bytes).hexdigest()
    assert atom_digest == "87d207363bf7e9401b47c7a8be10cb8e7b23227fcd0a8cfbd2198893c21abccd"
    (HERE / "unit-customer-types.json").write_text(json.dumps({
        "scope": "new independent exact finite unit-customer realization; not a complete SPE",
        "labels": labels, "total_customers": str(scale), "types": canonical_atoms,
        "canonical_type_list_sha256": atom_digest,
    }, indent=2) + "\n")
    report = {
        "status": "all 48828 frozen F/G/U integers equal independent unit-customer reconstruction",
        "kernel": kernel_meta, "point": point_meta, "pair": pair_meta,
        "kernel_fields": list(kernel),
        "source_scope": kernel["scope"], "source_seconds_preserved_not_reproduced": kernel["seconds"],
        "point_column_kinds": dict(Counter(c["kind"] for c in point["columns"])),
        "point_verified_rows_metadata_only": point["verified_rows"],
        "pair_rows_metadata_only": pair["rows"], "pair_variables_read": len(pair["variables"]),
        "raw_reply_groups_with_nonnegative_00": sum(len(h["raw"]) for h in hist.values()),
        "legacy_hist_index_mismatches_not_used_as_offsets": legacy_mismatches,
        "legacy_to_current_hist": [[next(iter(h["legacy"])), i] for i, h in hist.items()],
        "positive_hist_details": details,
        "raw_atom_records": atom_records, "distinct_customer_types": len(atoms),
        "unit_customers": str(scale), "normalized_payoff_denominator": str(denominator),
        "canonical_type_list_sha256": atom_digest,
        "six_T_topics_partition_all_customers": True, "normalized_OPT6": "1",
        "aliases_identity_and_all_coverages_distinct": True,
        "F_entries_checked": 156, "G_entries_checked": 24336, "U_entries_checked": 24336,
        "F_distinct_values": len(set(first)),
        "G_distinct_values": len({v for row in overlap for v in row}),
        "U_distinct_values": len({v for row in payoffs for v in row}),
        "G_zero_entries": sum(v == 0 for row in overlap for v in row),
        "U_zero_entries": sum(v == 0 for row in payoffs for v in row),
        "actual_normalized_payoffs": [str(F(v, denominator)) for v in actual_payoff],
        "actual_normalized_W": str(F(actual_coverage, scale)),
        "unary_cache_classes": len(unary), "pair_cache_classes": len(pairs),
        "pair_classes_by_named_index_count": {str(i): sum(key[1] == i for key in pairs) for i in range(5)},
        "limits": "Certifies this finite catalogue and fixed-prefix kernel. No 5108/10344 necessary-row revalidation, original generator run, tail strategy enumeration, or full six-player SPE certification.",
    }
    (HERE / "independent-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "raw_atom_records", "distinct_customer_types", "unit_customers", "canonical_type_list_sha256")}, indent=2))


if __name__ == "__main__":
    main()
