#!/usr/bin/env python3
"""Prepare one genuine finite catalog from exact actual/OPT marginals.

This performs only static input construction and arithmetic.  It does not run
an equilibrium oracle, LP, MILP, random search, or any frozen original main.
The source's B/C/R/Z and auxiliary variables are not interpreted as themes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction as F
from functools import reduce
from math import comb, gcd, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
POINT = HERE / "complete_zz_5799_v1_original4849_exact.json"
POINT_SHA = "1af6fd35f9cf1a51220072e627df042b450a52a7c6ecac388a98247ecac043d2"
VISIBLE = HERE / "complete_zz_5799_v1_visible.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def construct():
    assert sha(POINT) == POINT_SHA
    point = json.loads(POINT.read_text())
    visible = json.loads(VISIBLE.read_text())
    assert visible["point_sha256"] == POINT_SHA
    assert len(point["columns"]) == 4849 and F(point["O"]) == 1
    hist = []
    masses = defaultdict(F)
    contributors = defaultdict(list)
    for j, column in enumerate(point["columns"]):
        if column["kind"] != "hist":
            continue
        bits, mass = column["actual_bits"], F(column["weight"])
        assert len(bits) == 6 and set(bits) <= {"0", "1"}
        assert column["d"] == 1 and mass >= 0
        hist.append({"column_index": j, "actual_bits": bits,
                     "d": 1, "hist": column["hist"], "weight": str(mass)})
        if mass == 0:
            continue
        actual_mask = sum((int(bit) << a) for a, bit in enumerate(bits))
        for t in range(6):
            mask = actual_mask | (1 << (6 + t))
            masses[mask] += mass / 6
            contributors[mask].append({"hist_column": j, "mass": str(mass / 6)})
    assert len(hist) == 16 and sum(map(lambda h: F(h["weight"]), hist)) == 1
    assert sum(masses.values()) == 1
    denominator = lcm(*(v.denominator for v in masses.values()))
    raw_counts = {mask: int(value * denominator) for mask, value in masses.items()}
    divisor = reduce(gcd, raw_counts.values())
    counts = {mask: count // divisor for mask, count in raw_counts.items()}
    total = sum(counts.values())
    assert all(F(count, total) == masses[mask] for mask, count in counts.items())
    labels = [f"A{i}" for i in range(1, 7)] + [f"T{i}" for i in range(1, 7)]
    actual = (1 << 6) - 1
    for mask in counts:
        assert ((mask >> 6) & actual).bit_count() == 1
    welfare = sum(count for mask, count in counts.items() if mask & actual)
    utilities = [sum((F(count, (mask & actual).bit_count())
                      for mask, count in counts.items() if mask & (1 << a)), F())
                 for a in range(6)]
    assert F(welfare, total) == F(point["W"])
    assert [str(u / total) for u in utilities] == visible["actual_utilities"]
    topic_sizes = [sum(count for mask, count in counts.items() if mask & (1 << a))
                   for a in range(12)]
    assert topic_sizes[6:] == [total // 6] * 6 and total % 6 == 0
    supports = [{mask for mask in counts if mask & (1 << a)} for a in range(12)]
    maximal = [a for a in range(12) if not any(supports[a] < s for s in supports)]
    return {
        "schema": "one-fixed-full-history-catalog-candidate-v1",
        "status": "prepared_and_statically_verified; equilibrium_not_solved",
        "players": 6,
        "labels": labels,
        "mask_convention": "Bit j corresponds to labels[j]; source actual_bits position 0 is A1.",
        "model": "Each integer clone denotes a distinct unit customer. All 12 labels, repetitions and weak ties remain available at every ordered history.",
        "scope": "Only actual A1..A6 and comparison T1..T6 marginals are realized. No B/C/R/Z or old auxiliary variable is asserted to be a true continuation theme. Failure in this catalog does not exclude larger catalogs.",
        "source": {
            "point_path": str(POINT.relative_to(ROOT)), "point_sha256": POINT_SHA,
            "full_point_sha256": point["parent_full_point_sha256"],
            "full_matrix_sha256": point["parent_full_matrix_sha256"],
            "visible_path": str(VISIBLE.relative_to(ROOT)), "visible_sha256": sha(VISIBLE),
            "preparation_script_sha256": sha(Path(__file__)),
        },
        "source_hist_columns": hist,
        "construction": "For each source hist h and each t=1..6 create mass m_h/6 on actual_bits(h) union {T_t}; merge identical masks; clear denominators and divide the common integer gcd.",
        "rational_denominator_before_gcd": str(denominator),
        "integer_common_gcd_removed": str(divisor),
        "unit_customers": str(total),
        "nonzero_customer_types": [
            {"mask": mask, "members": [labels[a] for a in range(12) if mask & (1 << a)],
             "integer_clones": str(counts[mask]), "normalized_mass": str(masses[mask]),
             "source_contributions": contributors[mask]}
            for mask in sorted(counts)
        ],
        "target_terminal_counts": [1] * 6 + [0] * 6,
        "specified_actual_order": labels[:6],
        "static_verification": {
            "source_hist_count": len(hist),
            "source_positive_hist_count": sum(F(h["weight"]) > 0 for h in hist),
            "positive_actual_bit_patterns": len({h["actual_bits"] for h in hist if F(h["weight"]) > 0}),
            "nonzero_types": len(counts),
            "distinct_coverages": len({frozenset(s) for s in supports}),
            "maximal_label_indices": maximal,
            "empty_label_indices": [a for a, s in enumerate(supports) if not s],
            "topic_unit_customers": [str(v) for v in topic_sizes],
            "T_partition_covers_every_customer_exactly_once": True,
            "OPT6": str(total),
            "OPT6_proof": "The six T labels partition all customers, so a legal six-topic cover attains the total population, the universal coverage upper bound.",
            "target_W": str(welfare),
            "target_W_over_OPT6": str(F(welfare, total)),
            "target_O_minus_2W_normalized": str(F(total - 2 * welfare, total)),
            "target_actual_utilities": [str(u) for u in utilities],
            "target_normalized_actual_utilities": [str(u / total) for u in utilities],
            "integer_population_bit_length": total.bit_length(),
            "terminal_count_states": comb(17, 6),
            "all_count_states": comb(18, 6),
            "all_count_terminal_containment_pairs_upper_bound": comb(29, 6),
            "all_action_child_terminal_pairs_upper_bound": 12 * comb(28, 5),
            "literal_ordered_decision_histories": sum(12**d for d in range(6)),
            "literal_nonself_comparisons": 11 * sum(12**d for d in range(6)),
        },
        "oracle_calls": 0,
        "optimizer_calls": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = construct()
    with args.output.open("x") as stream:
        stream.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "sha256": sha(args.output),
                      "static_verification": data["static_verification"]}, indent=2))


if __name__ == "__main__":
    main()
