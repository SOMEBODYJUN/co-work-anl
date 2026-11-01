#!/usr/bin/env python3
"""Exact finite audit of the independently reconstructed single-threshold profile lemma.

This is a scratch audit, not a generic SC solver or a proof of the universal lemma.
Small cases enumerate all locally emitted profiles two different ways and search all
partial allocations directly. Larger local count cases exercise nontrivial block cuts.
"""

from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import ceil, comb
from pathlib import Path
import hashlib
import json
import random


@lru_cache(None)
def parameters(n, epsilon):
    assert n > 0 and epsilon > 0
    delta = epsilon / (4 * (1 + epsilon))
    cutoff = delta / n
    values = [F(1)]
    while values[-1] > cutoff:
        values.append(values[-1] / (1 + delta))
    types = len(values)
    blocks = tuple(max(1, (delta / (types * a)).numerator //
                       (delta / (types * a)).denominator) for a in values)
    bound = ceil(4 * types / delta)
    assert values[-1] <= cutoff < (1 + delta) * values[-1]
    assert all(b * a >= delta / (2 * types)
               for b, a in zip(blocks, values))
    return delta, cutoff, tuple(values), blocks, bound


def round_entry(value, cutoff, values):
    capped = min(value, F(1))
    if capped < cutoff:
        return None
    # Binary search in the strictly descending palette; no logarithms or floats.
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] <= capped:
            hi = mid
        else:
            lo = mid + 1
    assert values[lo] <= capped
    assert lo == 0 or values[lo - 1] > capped
    return lo


def rounded_matrix(matrix, epsilon):
    m = len(matrix)
    n = len(matrix[0]) if m else 0
    assert m >= 1 and all(len(row) == n for row in matrix)
    if n == 0:
        return (), (), 0, tuple(() for _ in matrix)
    delta, cutoff, values, blocks, bound = parameters(n, epsilon)
    kinds = tuple(tuple(round_entry(v, cutoff, values) for v in row)
                  for row in matrix)
    for row, tags in zip(matrix, kinds):
        for v, tag in zip(row, tags):
            rounded = F(0) if tag is None else values[tag]
            assert 0 <= rounded <= min(v, F(1))
            if tag is not None:
                assert rounded >= min(v, F(1)) / (1 + delta)
    return values, blocks, bound, kinds


def profiles_by_blocks(tags, values, blocks, bound, gamma):
    availability = Counter(k for k in tags if k is not None)
    active = sorted(k for k in availability if availability[k] >= blocks[k])
    emitted = set()

    def visit(pos, remaining_h, remaining_items, partial, value):
        if pos == len(active):
            if value >= gamma:
                emitted.add(tuple(partial))
            return
        k = active[pos]
        b = blocks[k]
        top = min(remaining_h, remaining_items // b, availability[k] // b)
        for h in range(top + 1):
            count = b * h
            if count:
                partial.append((k, count))
            visit(pos + 1, remaining_h - h, remaining_items - count,
                  partial, value + values[k] * count)
            if count:
                partial.pop()

    visit(0, bound, len(tags), [], F(0))
    return emitted


def profiles_by_all_counts(tags, values, blocks, bound, gamma):
    """Independent local oracle: enumerate every attainable count vector first."""
    availability = Counter(k for k in tags if k is not None)
    active = sorted(availability)
    emitted = set()
    for counts in product(*(range(availability[k] + 1) for k in active)):
        if sum(counts) > len(tags):
            continue
        if any(c % blocks[k] for k, c in zip(active, counts)):
            continue
        if sum(c // blocks[k] for k, c in zip(active, counts)) > bound:
            continue
        if sum((values[k] * c for k, c in zip(active, counts)), F(0)) < gamma:
            continue
        emitted.add(tuple((k, c) for k, c in zip(active, counts) if c))
    return emitted


def exact_original_optimum(matrix):
    m, n = len(matrix), len(matrix[0])
    best = F(0)
    # Nonnegative SC values let the optimum assign every item, for this oracle only.
    for allocation in product(range(m), repeat=n):
        loads = [F(0)] * m
        for j, i in enumerate(allocation):
            loads[i] += matrix[i][j]
        best = max(best, min(loads))
    return best


def direct_profile_feasibility(kinds, profile_sets):
    """Search actual disjoint partial allocations, without using the proof's subsets."""
    m, n = len(kinds), len(kinds[0])
    if any(not family for family in profile_sets):
        return None
    for allocation in product(range(m + 1), repeat=n):
        counts = [Counter() for _ in range(m)]
        valid = True
        for j, owner in enumerate(allocation):
            if owner == m:
                continue
            tag = kinds[owner][j]
            if tag is None:
                valid = False
                break
            counts[owner][tag] += 1
        if valid and all(tuple(sorted(row.items())) in family
                         for row, family in zip(counts, profile_sets)):
            return allocation
    return None


def audit_matrix(matrix, epsilon):
    m, n = len(matrix), len(matrix[0])
    gamma = 1 / (1 + epsilon)
    opt = exact_original_optimum(matrix)
    if n == 0:
        values, blocks, bound, kinds = rounded_matrix(matrix, epsilon)
        assert not values and not blocks and bound == 0 and opt == 0
        return {"yes": False, "profiles": 0, "types": 0, "local_yes_subsets": 0}
    values, blocks, bound, kinds = rounded_matrix(matrix, epsilon)
    families = []
    local_yes_subsets = 0
    for tags in kinds:
        actual = profiles_by_blocks(tags, values, blocks, bound, gamma)
        independent = profiles_by_all_counts(tags, values, blocks, bound, gamma)
        assert actual == independent
        for profile in actual:
            assert sum(count for _, count in profile) <= n
            assert sum((values[k] * count for k, count in profile), F(0)) >= gamma
        families.append(actual)
        # The final Exact strengthens completeness to every individual resource subset.
        row = matrix[len(families) - 1]
        for mask in range(1 << n):
            if sum((row[j] for j in range(n) if mask & (1 << j)), F(0)) < 1:
                continue
            local_yes_subsets += 1
            subset_counts = Counter(tags[j] for j in range(n)
                                    if mask & (1 << j) and tags[j] is not None)
            assert any(all(c <= subset_counts[k] for k, c in profile)
                       for profile in actual)
    witness = direct_profile_feasibility(kinds, families)
    if opt >= 1:
        assert witness is not None, (matrix, epsilon, opt)
    return {"yes": opt >= 1, "profiles": sum(map(len, families)),
            "types": len(values), "local_yes_subsets": local_yes_subsets}


def audit_local_counts(n, epsilon):
    delta, cutoff, values, blocks, bound = parameters(n, epsilon)
    types = len(values)
    # A capped configuration with one unit item plus tails immediately below a block.
    counts = [max(0, b - 1) if b >= 2 else 0 for b in blocks]
    counts[0] = 1
    assert sum(counts) <= n
    before = sum((a * c for a, c in zip(values, counts)), F(0))
    assert 1 <= before < 2
    kept = [b * (c // b) for b, c in zip(blocks, counts)]
    after = sum((a * c for a, c in zip(values, kept)), F(0))
    loss = before - after
    assert 0 <= loss <= delta
    assert sum(c // b for c, b in zip(kept, blocks)) <= bound
    assert after == 1
    assert after >= 1 / (1 + epsilon)
    assert any(b >= 2 for b in blocks), (n, epsilon, types)
    assert loss > 0
    return {"n": n, "epsilon": str(epsilon), "types": types,
            "nontrivial_blocks": sum(b >= 2 for b in blocks),
            "discarded_value": str(loss), "count_sum": sum(counts),
            "record_bound": bound,
            "unfiltered_record_count_bits": comb(bound + types, types).bit_length(),
            "max_grid_numerator_bits": max(a.numerator.bit_length() for a in values),
            "max_grid_denominator_bits": max(a.denominator.bit_length() for a in values)}


def main():
    rng = random.Random(824731)
    epsilons = [F(1, 8), F(1, 2), F(2), F(7)]
    matrices = [
        [[F(0)] * 0],
        [[F(0)] * 0 for _ in range(3)],
        [[F(0)]],
        [[F(1)]],
        [[F(2)]],
        [[F(1)], [F(1)]],
        [[F(1), F(0)], [F(0), F(1)]],
        [[F(1, 2)] * 4, [F(1, 2)] * 4],
        [[F(1, 3)] * 6, [F(1, 3)] * 6],
        [[F(1), F(1, 2), F(1, 4)], [F(1, 4), F(1, 2), F(1)]],
        [[F(1, 2**73 + 17), F(1), F(0)],
         [F(1), F(1, 2**71 + 33), F(1)]],
    ]
    choices = [F(0), F(1, 64), F(1, 8), F(1, 3), F(1, 2), F(3, 4), F(1), F(2)]
    for _ in range(70):
        m, n = rng.randint(1, 3), rng.randint(0, 6)
        matrices.append([[rng.choice(choices) for _ in range(n)] for _ in range(m)])
    for _ in range(25):
        m, n = rng.randint(1, 3), 6
        matrix = [[rng.choice(choices) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            matrix[i][i] = F(1)
        matrices.append(matrix)

    report = {"seed": 824731, "small_matrix_checks": 0, "small_yes_checks": 0,
              "total_emitted_profiles_checked": 0, "max_types": 0,
              "local_yes_subsets_checked": 0,
              "boundary_checks": 0, "local_count_checks": []}
    for epsilon in epsilons:
        for matrix in matrices:
            result = audit_matrix(matrix, epsilon)
            report["small_matrix_checks"] += 1
            report["small_yes_checks"] += int(result["yes"])
            report["total_emitted_profiles_checked"] += result["profiles"]
            report["max_types"] = max(report["max_types"], result["types"])
            report["local_yes_subsets_checked"] += result["local_yes_subsets"]
        # Exact cutoff retained, just below cutoff dropped; grid bottom can be lower.
        delta = epsilon / (4 * (1 + epsilon))
        cutoff = delta / 4
        values, blocks, bound, kinds = rounded_matrix(
            [[F(1), cutoff, cutoff - F(1, 2**109), F(0)]], epsilon)
        assert kinds[0][1] is not None
        assert kinds[0][2] is None and kinds[0][3] is None
        assert values[kinds[0][1]] <= cutoff
        audit_matrix([[F(1), cutoff, cutoff - F(1, 2**109), F(0)]], epsilon)
        report["boundary_checks"] += 1
        for n in (1024, 4096):
            report["local_count_checks"].append(audit_local_counts(n, epsilon))

    # Literal old-cutoff factor claim fails already for one player, ten resources.
    old_eta = F(1, 10)
    old_values = [F(9, 100)] * 9 + [F(19, 100)]
    old_cutoff = 1 / ((1 + old_eta) * len(old_values))
    assert sum(old_values) == 1
    old_retained = sum(v for v in old_values if v >= old_cutoff)
    assert old_retained == F(19, 100) < 1 / (1 + old_eta)
    report["literal_old_cutoff_counterexample"] = {
        "eta": str(old_eta), "n": 10, "input_values": list(map(str, old_values)),
        "old_cutoff": str(old_cutoff), "original_total": "1",
        "retained_before_geometric_rounding": str(old_retained),
        "claimed_lower_bound": str(1 / (1 + old_eta))}
    report["scope"] = [
        "Small exact local-profile enumeration compared block recursion to independent all-count enumeration.",
        "All actual partial allocations were searched on small matrices to verify the YES implication.",
        "Every original row subset of value at least one was separately checked for local profile containment.",
        "Larger local count vectors exercise b>=2 and count rounding loss, without full global allocation search.",
        "This finite audit does not prove the general statement or solve common profile selection."]
    source = Path(__file__).resolve()
    root = source.parents[3]
    note = root / "research/current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md"
    report["code_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    report["note_sha256"] = hashlib.sha256(note.read_bytes()).hexdigest()
    print(json.dumps(report, indent=2))



if __name__ == "__main__":
    main()
