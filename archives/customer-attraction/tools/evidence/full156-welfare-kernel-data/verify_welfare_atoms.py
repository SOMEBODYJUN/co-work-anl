#!/usr/bin/env python3
"""Independently realize the threshold catalogue as integer customer types.

This code does not import/run the historical generator, canonicalize pairs, or
use its moment/intersection routines.  It enumerates full six-index word
assignments and slab subintervals, then counts uncovered customers directly.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from math import factorial, lcm, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / "full156-tail-parent-report/original/research_5"
PATHS = {
    "welfare": SHARED / "full156_tail2_welfare_10344.json",
    "kernel": SHARED / "full156_tail2_kernel_10344.json",
    "point": SHARED / "combined_branch_master_exact.json",
    "pair": HERE.parent / "full156-pair-master-point/original/pair_master_exact.json",
}
HASHES = {
    "welfare": "fe8fb09f7527f8f4cd26ad67f6e43be5bc84cb5d9c47fea39fd0661bab0e5256",
    "kernel": "876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4",
    "point": "d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8",
    "pair": "090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2",
}


def load(role):
    data = PATHS[role].read_bytes()
    assert sha256(data).hexdigest() == HASHES[role], role
    return json.loads(data)


def group(g):
    assert len(g) == 4 and g[0] in (0, 1) and g[1] in (0, 1)
    assert all(len(w) == 3 and set(w) <= {0, 1} for w in g[2:])
    return g[0], g[1], tuple(g[2]), tuple(g[3])


def label(a):
    if len(a) == 2:
        return a[0] + str(a[1] + 1)
    return f"{a[0]}_{a[1]}_{a[2]+1}_{a[3]+1}"


def main():
    if not __debug__:
        raise RuntimeError("Assertions must remain enabled; do not use -O")
    welfare, kernel, point, pair = [load(role) for role in PATHS]
    assert set(welfare) == {"scope", "kernel_source", "kernel_sha256", "topics", "aliases",
                            "unit_customer_scale", "actual_pair", "welfare_numerators", "source_W"}
    assert welfare["scope"] == "exact full-catalogue r2 final welfare after fixed A1..A4; no inherited SPE"
    assert welfare["kernel_source"] == PATHS["kernel"].name
    assert welfare["kernel_sha256"] == HASHES["kernel"]
    assert kernel["source_sha256"] == HASHES["point"]
    assert kernel["pair_source_sha256"] == HASHES["pair"]
    scale = int(welfare["unit_customer_scale"])
    assert kernel["unit_customer_scale"] == str(scale)
    assert int(kernel["payoff_denominator_for_normalized_point"]) == 60 * scale
    patterns = tuple(product((0, 1), repeat=3))
    histograms = {i: c for i, c in enumerate(point["columns"]) if c["kind"] == "hist"}
    raw = defaultdict(dict)
    radii = defaultdict(dict)
    slabs = defaultdict(lambda: defaultdict(dict))
    denominators, old_to_current = [], {}
    for i, h in histograms.items():
        assert len(h["actual_bits"]) == 6 and set(h["actual_bits"]) <= {"0", "1"}
        assert len(h["hist"]) == 8 and sum(h["hist"]) == 6
        assert all(isinstance(c, int) and c >= 0 for c in h["hist"])
        assert sum(c * pat[0] for c, pat in zip(h["hist"], patterns)) == h["d"] == 1
        denominators.append(F(h["weight"]).denominator)
    current, stale_pointer_count = None, 0
    for j, c in enumerate(point["columns"]):
        assert F(c["weight"]) >= 0
        if c["kind"] == "hist":
            current = j
        elif c["kind"] == "joint-reply":
            # The old pointer is a legacy index; the current histogram block
            # owns the rows.  Check the complete legacy-to-current mapping.
            old = c["hist_column_old"]
            assert old not in old_to_current or old_to_current[old] == current
            old_to_current[old] = current
            stale_pointer_count += old != current
            g, state = group(c["group"]), tuple(c["state"])
            assert state not in raw[current].setdefault(g, {})
            raw[current][g][state] = F(c["weight"])
        elif c["kind"] == "overlap":
            assert c["hist_column"] in histograms and len(c["groups"]) == 2
            for g in c["groups"]:
                group(g)
        else:
            assert c["kind"] == "K"
    for i, groups in raw.items():
        for g, values in groups.items():
            assert set(values) == {(0, 1), (1, 0), (1, 1)}
            assert sum(values.values()) <= F(histograms[i]["weight"])
            radii[i][g] = values[1, 0] + values[1, 1]
            denominators.append(radii[i][g].denominator)
    for v in pair["variables"]:
        i, left, right = v["hist_column"], F(v["left"]), F(v["right"])
        g, y = group(v["group"]), F(v["weight"])
        assert 0 <= y <= right - left and v["r"] in (0, 1)
        assert v["r"] == int(right <= radii[i][g])
        assert right <= radii[i][g] or left >= radii[i][g]
        assert g not in slabs[i][left, right]
        slabs[i][left, right][g] = v["r"], y
        denominators.append(y.denominator)
    assert scale == 720 * lcm(*denominators)
    assert set(slabs) == {i for i, h in histograms.items() if F(h["weight"])}
    actions = ([('A', i) for i in range(6)]
               + [(f, i) for f in ('T', 'B', 'C') for i in range(6)]
               + [(f, k, i, j) for f in ('R', 'Z')
                  for k, i, j in product(range(2), range(6), range(6)) if k or i != j])
    labels = list(map(label, actions))
    assert len(actions) == 156 and welfare["topics"] == kernel["topics"] == labels
    assert welfare["aliases"] == kernel["aliases"] == list(range(156))
    assert welfare["actual_pair"] == kernel["actual_last_pair"] == [4, 5]
    assert kernel["fixed_prefix"] == [0, 1, 2, 3] and kernel["players"] == 6
    atoms, per_histogram = Counter(), []
    raw_records = 0
    for i, h in histograms.items():
        mass = F(h["weight"])
        if not mass:
            continue
        words = [pat for pat, c in zip(patterns, h["hist"]) for _ in range(c)]
        assignments = sorted(set(permutations(words)))
        size = len(assignments)
        assert size == factorial(6) // prod(factorial(c) for c in h["hist"])
        intervals = slabs[i]
        bounds = sorted(intervals)
        assert bounds[0][0] == 0 and bounds[-1][1] == mass
        assert all(bounds[k][1] == bounds[k+1][0] for k in range(len(bounds)-1))
        count, total = 0, 0
        for ws in assignments:
            old_bits = [int(h["actual_bits"][a[1]]) if a[0] == 'A'
                        else ws[a[1]][('T', 'B', 'C').index(a[0])] for a in actions[:24]]
            for (left, right), values in intervals.items():
                assert set(values) == set(radii[i])
                cuts = sorted({F(0), right-left} | {y for _, y in values.values()})
                for lo, hi in zip(cuts, cuts[1:]):
                    units = (hi-lo) * scale / size
                    assert units.denominator == 1 and units > 0
                    mask = sum(bit << j for j, bit in enumerate(old_bits))
                    for j, (family, k, ai, aj) in enumerate(actions[24:], 24):
                        rbit, y = values[k, int(ai == aj), ws[ai], ws[aj]]
                        mask |= (rbit if family == 'R' else int(hi <= y)) << j
                    atoms[mask] += int(units)
                    total += int(units)
                    count += 1
        assert total == mass * scale
        per_histogram.append({"current_column": i, "actual_bits": h["actual_bits"],
                              "word_assignments": size, "slabs": len(intervals), "atom_records": count})
        raw_records += count
    assert sum(atoms.values()) == scale
    coverage_columns = [tuple(mask for mask in atoms if mask >> i & 1) for i in range(156)]
    assert len(set(coverage_columns)) == 156
    assert all(mask & sum(1 << i for i in range(6, 12)) for mask in atoms)
    prefix = sum(mass for mask, mass in atoms.items() if mask & 15)
    uncovered = [[0] * 156 for _ in range(156)]
    for mask, mass in atoms.items():
        if mask & 15:
            continue
        absent = [i for i in range(156) if not (mask >> i & 1)]
        for i in absent:
            for j in absent:
                uncovered[i][j] += mass
    rebuilt = [[scale-uncovered[i][j] for j in range(156)] for i in range(156)]
    source_matrix = welfare["welfare_numerators"]
    assert len(source_matrix) == 156 and all(len(row) == 156 for row in source_matrix)
    checked = 0
    for i, row in enumerate(source_matrix):
        for j, value in enumerate(row):
            assert isinstance(value, str) and str(int(value)) == value
            assert int(value) == rebuilt[i][j], (i, j)
            assert rebuilt[i][j] == rebuilt[j][i] and 0 <= rebuilt[i][j] <= scale
            checked += 1
    old_W = F(rebuilt[4][5], scale)
    assert old_W == F(welfare["source_W"]) == F(kernel["source_W"]) == F(point["W"]) == F(pair["W"])
    assert old_W == sum(F(h["weight"]) for h in histograms.values() if int(h["actual_bits"], 2))
    # This check separates final welfare from remaining-player profit directly
    # on customer types, without taking the old payoff matrix as an oracle.
    actual_payoffs = [F(0) for _ in range(6)]
    for mask, mass in atoms.items():
        a = [int(bool(mask & (1 << j))) for j in range(6)]
        cover_count = sum(a)
        if cover_count:
            for j in range(6):
                actual_payoffs[j] += F(mass * a[j], cover_count * scale)
    assert sum(actual_payoffs) == old_W
    flat = [v for row in rebuilt for v in row]
    low, high = min(flat), max(flat)
    row_groups = defaultdict(list)
    for name, row in zip(labels, rebuilt):
        row_groups[tuple(row)].append(name)
    atom_json = json.dumps([[hex(mask), str(n)] for mask, n in sorted(atoms.items())], separators=(',', ':')).encode()
    atom_lines = ''.join(f'{mask}:{atoms[mask]}\n' for mask in sorted(atoms)).encode()
    report = {
        "status": "all_24336_welfare_cells_independently_rebuilt",
        "method": "full six-index multiset assignments and second-threshold subinterval atoms; integer uncovered-pair counting; no historical generator import or entry run",
        "input_sha256": HASHES, "primary_size": PATHS['welfare'].stat().st_size,
        "primary_all_nine_fields": list(welfare),
        "raw_point_columns": dict(Counter(c['kind'] for c in point['columns'])),
        "legacy_histogram_mapping": [[old, cur] for old, cur in old_to_current.items()],
        "legacy_pointer_values_different_from_current": stale_pointer_count,
        "raw_pair_variables": len(pair['variables']), "per_histogram": per_histogram,
        "positive_histograms": len(per_histogram), "raw_atom_records": raw_records,
        "distinct_integer_customer_types": len(atoms), "unit_customer_scale_and_total": str(scale),
        "atom_json_hex_sha256": sha256(atom_json).hexdigest(), "atom_colon_lines_sha256": sha256(atom_lines).hexdigest(),
        "all_156_coverages_distinct": True, "checked_welfare_cells": checked,
        "normalized_OPT6_from_all_T_coverage": "1", "normalized_prefix_coverage": str(F(prefix, scale)),
        "minimum_normalized_welfare": str(F(low, scale)), "maximum_normalized_welfare": str(F(high, scale)),
        "minimum_pairs": [[labels[i], labels[j]] for i in range(156) for j in range(156) if rebuilt[i][j] == low],
        "maximum_pairs": [[labels[i], labels[j]] for i in range(156) for j in range(156) if rebuilt[i][j] == high],
        "pairs_below_half": sum(2*v < scale for v in flat), "pairs_equal_half": sum(2*v == scale for v in flat),
        "pairs_above_half": sum(2*v > scale for v in flat), "distinct_welfare_values": len(set(flat)),
        "distinct_welfare_rows": len(row_groups), "equal_welfare_row_groups": [v for v in row_groups.values() if len(v)>1],
        "actual_pair": welfare['actual_pair'], "actual_normalized_W": str(old_W),
        "actual_six_normalized_payoffs_from_atoms": list(map(str, actual_payoffs)),
        "actual_tail_profit": str(sum(actual_payoffs[4:])), "actual_prefix_players_profit": str(sum(actual_payoffs[:4])),
        "row_verification": [{"topic": labels[i], "cells": 156, "minimum_integer_welfare": str(min(row)),
                              "maximum_integer_welfare": str(max(row)), "below_half": sum(2*v<scale for v in row),
                              "sha256_comma_decimal_integers": sha256(','.join(map(str,row)).encode()).hexdigest()}
                             for i,row in enumerate(rebuilt)],
        "not_rechecked": "point's 5108 necessary rows, pair's 10344 necessary rows, any full six-player SPE, or new tail equilibrium enumeration",
        "source_reading_correction": "An initial read-only trial treated hist_column_old as a current index and stopped at KeyError 21; the final reconstruction validates all 16 legacy-to-current mappings and uses the current histogram block.",
    }
    (HERE / 'welfare-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('row_verification','per_histogram','legacy_histogram_mapping','minimum_pairs','maximum_pairs')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
