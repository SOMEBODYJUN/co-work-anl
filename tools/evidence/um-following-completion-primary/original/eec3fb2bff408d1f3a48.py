#!/usr/bin/env python3
"""Exact finite audit; standard Python, no external solver, no general proof claim."""
from fractions import Fraction as F
from itertools import product
from random import Random
import json
import platform


def schedules(matrix):
    m = len(matrix)
    n = len(matrix[0]) if m else 0
    choices = [[i for i in range(m) if matrix[i][j] is not None]
               for j in range(n)]
    for assignment in product(*choices):
        loads = [F(0) for _ in range(m)]
        for j, i in enumerate(assignment):
            loads[i] += matrix[i][j]
        yield assignment, max(loads, default=F(0))


def contract(matrix, vertex, target):
    m, n = len(matrix), len(matrix[0])
    cover = [j for j in range(n) if matrix[vertex][j] is not None]
    total = sum((matrix[vertex][j] for j in cover), F(0))
    assert cover and total > target
    assert all(total - matrix[vertex][j] <= target for j in cover)
    keep = [j for j in range(n) if j not in cover]
    other = [i for i in range(m) if i != vertex]
    reduced = []
    for i in other:
        finite = [matrix[i][j] for j in cover if matrix[i][j] is not None]
        reduced.append([matrix[i][j] for j in keep]
                       + [min(finite) if finite else None])
    return reduced, cover, keep, other


def lift_once(frame, assignment):
    matrix, vertex, target, cover, keep, other = frame
    original = [None] * len(matrix[0])
    for index, j in enumerate(keep):
        original[j] = other[assignment[index]]
    chosen_machine = other[assignment[-1]]
    witness = min((j for j in cover if matrix[chosen_machine][j] is not None),
                  key=lambda j: matrix[chosen_machine][j])
    original[witness] = chosen_machine
    for j in cover:
        if j != witness:
            original[j] = vertex
    return tuple(original)


def makespan(matrix, assignment):
    loads = [F(0)] * len(matrix)
    assert len(assignment) == len(matrix[0])
    for j, i in enumerate(assignment):
        assert matrix[i][j] is not None
        loads[i] += matrix[i][j]
    return max(loads, default=F(0))


def chain_audit():
    """Enumerate final schedules then undo every nested contraction in reverse."""
    rng = Random(903629)
    counts = {"sampled_matrices": 5000, "initially_legal_pruned_matrices": 0,
              "chains_with_two_or_more_steps": 0, "nested_steps": 0,
              "reject_certificates_checked": 0, "fully_lifted_schedules": 0,
              "maximum_steps_seen": 0}
    mandatory = [
        [[F(1), F(1), None], [F(2, 3), F(1, 3), F(1)],
         [F(1, 2), None, F(1)]],
        [[F(1), F(1), None], [F(2, 3), F(1, 3), F(1)],
         [F(1, 2), None, F(1, 6)]]]
    matrices = [(matrix, F(1)) for matrix in mandatory]
    for _ in range(counts["sampled_matrices"]):
        m, n = rng.choice([1, 2, 3, 4]), rng.choice([2, 3, 4, 5])
        target = rng.choice([F(0), F(1, 2), F(1), F(7, 6)])
        matrix = [[rng.choice([None, F(0), F(1, 6), F(1, 2), F(2, 3),
                               F(1), F(7, 6)]) for _ in range(n)]
                  for _ in range(m)]
        matrices.append((matrix, target))
    for raw, target in matrices:
        matrix = [[p if p is None or p <= target else None for p in row]
                  for row in raw]
        if any(all(matrix[i][j] is None for i in range(len(matrix)))
               for j in range(len(matrix[0]))):
            continue
        counts["initially_legal_pruned_matrices"] += 1
        original = matrix
        current = matrix
        leafsets = [frozenset([j]) for j in range(len(matrix[0]))]
        frames = []
        rejected = False
        while True:
            selected = None
            for vertex in range(len(current)):
                cover = [j for j in range(len(current[0]))
                         if current[vertex][j] is not None]
                total = sum((current[vertex][j] for j in cover), F(0))
                if (cover and total > target
                        and all(total - current[vertex][j] <= target for j in cover)):
                    selected = vertex
                    break
            if selected is None:
                break
            reduced, cover, keep, other = contract(current, selected, target)
            counts["nested_steps"] += any(len(leafsets[j]) > 1 for j in cover)
            new_leafset = frozenset().union(*(leafsets[j] for j in cover))
            assert sum(len(leafsets[j]) for j in cover) == len(new_leafset)
            leafsets = [leafsets[j] for j in keep] + [new_leafset]
            assert sum(map(len, leafsets)) == len(original[0])
            assert len(frozenset().union(*leafsets)) == len(original[0])
            frames.append((current, selected, target, cover, keep, other))
            if not reduced or all(row[-1] is None for row in reduced):
                rejected = True
                break
            current = reduced
        counts["maximum_steps_seen"] = max(counts["maximum_steps_seen"], len(frames))
        counts["chains_with_two_or_more_steps"] += len(frames) >= 2
        if rejected:
            assert not any(bound <= target for _, bound in schedules(original))
            counts["reject_certificates_checked"] += 1
            continue
        reduced_schedules = list(schedules(current))
        assert (any(bound <= target for _, bound in schedules(original))
                == any(bound <= target for _, bound in reduced_schedules))
        for assignment, bound in reduced_schedules:
            lifted = assignment
            for frame in reversed(frames):
                old_bound = makespan(frame[0], lift_once(frame, lifted))
                assert old_bound <= max(bound, target)
                lifted = lift_once(frame, lifted)
            assert makespan(original, lifted) <= max(bound, target)
            counts["fully_lifted_schedules"] += 1
    return counts


def main():
    rng = Random(837210)
    count = lifted = unequal = zero_cases = 0
    for _ in range(4000):
        m, n = rng.choice([2, 3, 4]), rng.choice([2, 3, 4, 5])
        target = rng.choice([F(0), F(1, 2), F(1), F(7, 6)])
        matrix = [[rng.choice([None, F(0), F(1, 6), F(1, 2), F(2, 3),
                               F(1), F(7, 6)]) for _ in range(n)]
                  for _ in range(m)]
        matrix = [[p if p is None or p <= target else None for p in row]
                  for row in matrix]
        if any(all(matrix[i][j] is None for i in range(m)) for j in range(n)):
            continue
        for vertex in range(m):
            cover = [j for j in range(n) if matrix[vertex][j] is not None]
            total = sum((matrix[vertex][j] for j in cover), F(0))
            if not cover or total <= target:
                continue
            if any(total - matrix[vertex][j] > target for j in cover):
                continue
            reduced, cover, keep, other = contract(matrix, vertex, target)
            original_schedules = list(schedules(matrix))
            reduced_schedules = list(schedules(reduced))
            assert (any(b <= target for _, b in original_schedules)
                    == any(b <= target for _, b in reduced_schedules))
            for assignment, bound in reduced_schedules:
                original = [None] * n
                for index, j in enumerate(keep):
                    original[j] = other[assignment[index]]
                chosen_machine = other[assignment[-1]]
                witness = min((j for j in cover
                               if matrix[chosen_machine][j] is not None),
                              key=lambda j: matrix[chosen_machine][j])
                original[witness] = chosen_machine
                for j in cover:
                    if j != witness:
                        original[j] = vertex
                loads = [F(0) for _ in range(m)]
                for j, i in enumerate(original):
                    loads[i] += matrix[i][j]
                assert max(loads) <= max(bound, target)
                lifted += 1
            count += 1
            unequal += len(set(matrix[vertex][j] for j in cover)) > 1
            zero_cases += any(p == 0 for row in matrix for p in row if p is not None)
    gap_checks = []
    for k in range(2, 13):
        assert F(1, k) + F(k - 1, k) == 1
        assert F(1, k) + (k - 1) * F(1, k) == 1
        assert F(k - 1, k) + (k + 1) * F(1, k * (k + 1)) == 1
        assert (k + 1) * F(1, k + 1) == 1
        assert k * F(1, k + 1) + k * F(1, k * (k + 1)) == 1
        optimum = F(2 * k - 1, k)
        assert optimum == 1 + (k - 1) * F(1, k)
        gap_checks.append({"k": k, "machines": k * k + 3 * k - 1,
                           "jobs": 2 * k * k + k, "config_target": 1,
                           "proved_optimum": str(optimum),
                           "minimal_star_irreducible": k >= 3})
    # Independent full schedule enumeration of the smallest star-gap instance.
    k = 2
    centers = [("V", a) for a in range(k)]
    globals_ = [("G", g) for g in range(k - 1)]
    locals_ = [("R", a, ell) for a in range(k) for ell in range(k + 1)]
    machines = centers + globals_ + locals_
    machine_index = {v: i for i, v in enumerate(machines)}
    options = []
    for a in range(k):
        options.append([(machine_index[("V", a)], k)]
                       + [(machine_index[g], k) for g in globals_])
    for a in range(k):
        for _ in range(k):
            options.append([(machine_index[("R", a, ell)], k)
                            for ell in range(k + 1)])
    for a in range(k):
        for _ in range(k):
            options.append([(machine_index[("V", a)], 1)]
                           + [(machine_index[("R", a, ell)], k)
                              for ell in range(k + 1)])
    optimum = None
    assignments_checked = 0
    for assignment in product(*options):
        loads = [0] * len(machines)
        for i, p in assignment:
            loads[i] += p
        makespan = max(loads)
        if optimum is None or makespan < optimum:
            optimum = makespan
        assignments_checked += 1
    assert assignments_checked == 2 ** 2 * 3 ** 4 * 4 ** 4 == 82944
    assert optimum == 3
    print(json.dumps({"python_version": platform.python_version(),
                      "arithmetic": "fractions.Fraction; no tolerance",
                      "seed": 837210, "sampled_matrices": 4000,
                      "applicable_contractions": count,
                      "lifts_checked": lifted, "unequal_star_cases": unequal,
                      "zero_entry_cases": zero_cases,
                      "gap_marginal_checks": gap_checks,
                      "star_gap_k2_independent_full_enumeration": {
                          "integer_scale": 2,
                          "assignments_checked": assignments_checked,
                          "integer_optimum": optimum,
                          "exact_optimum": "3/2"},
                      "nested_contraction_audit": chain_audit(),
                      "status": "all exact finite assertions passed",
                      "limitation": "sampling and finite enumeration, not a general proof"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
