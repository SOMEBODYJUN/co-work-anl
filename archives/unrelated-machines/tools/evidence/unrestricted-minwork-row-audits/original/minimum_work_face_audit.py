#!/usr/bin/env python3
"""Exact audit: minimum-total-work assignment-LP face loses near-optimal schedules.

All arithmetic is integer/Fraction. Small complete assignment enumeration is
performed through count matrices: tasks from one home are indistinguishable for
processing times, but no schedules are removed from the objective oracle.
No numerical LP solver and no imported scheduling audit is used.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import hashlib
import json
from pathlib import Path
import platform


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def matrix_rank(a):
    a = [list(map(F, row)) for row in a]
    rank = 0
    for col in range(len(a[0]) if a else 0):
        pivot = next((r for r in range(rank, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        divisor = a[rank][col]
        a[rank] = [v / divisor for v in a[rank]]
        for row in range(rank + 1, len(a)):
            multiplier = a[row][col]
            if multiplier:
                a[row] = [x - multiplier * y for x, y in zip(a[row], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def family(m):
    assert m >= 2
    d = F(1, m)
    jobs = [None] + [h for h in range(m) for _ in range(m - 1)]
    p = [[F(m) if h is None else (F(1) if i == h else 1 + d)
          for h in jobs] for i in range(m)]
    x = [[F(0) for _ in jobs] for _ in range(m)]
    for i in range(m):
        x[i][0] = F(m + 1, m * m) if i < m - 1 else F(1, m * m)
    for j, h in enumerate(jobs[1:], 1):
        x[h][j] = F(1)
    return p, x, jobs, F(m) + d


def slot_matching(p, x):
    m, n = len(p), len(p[0])
    adjacency = [[] for _ in range(n)]
    slot_machine = []
    for i in range(m):
        total = sum(x[i])
        slot_count = (total.numerator + total.denominator - 1) // total.denominator
        offset = len(slot_machine)
        slot_machine.extend([i] * slot_count)
        cursor = F(0)
        for j in sorted(range(n), key=lambda j: (-p[i][j], j)):
            width = x[i][j]
            if not width:
                continue
            end = cursor + width
            for k in range(cursor.numerator // cursor.denominator,
                           (end.numerator + end.denominator - 1) // end.denominator):
                if max(cursor, F(k)) < min(end, F(k + 1)):
                    adjacency[j].append(offset + k)
            cursor = end
    owner = {}
    def augment(j, seen):
        for s in adjacency[j]:
            if s in seen:
                continue
            seen.add(s)
            if s not in owner or augment(owner[s], seen):
                owner[s] = j
                return True
        return False
    for j in range(n):
        assert augment(j, set())
    assignment = [None] * n
    for s, j in owner.items():
        assignment[j] = slot_machine[s]
    loads = [sum(p[i][j] for j in range(n) if assignment[j] == i) for i in range(m)]
    assert all(assignment[j] == h for j, h in enumerate([None] + [a for a in range(m) for _ in range(m - 1)]) if j)
    return loads, len(slot_machine), sum(map(len, adjacency))


def rank_audit(m):
    p, x, jobs, target = family(m)
    positive = [(i, j) for i in range(m) for j in range(len(jobs)) if x[i][j]]
    rows = [[F(j == job) for i, j in positive] for job in range(len(jobs))]
    rows.extend([[p[i][j] if i == machine else F(0) for i, j in positive]
                 for machine in range(m - 1)])
    rank = matrix_rank(rows)
    assert rank == len(positive) == m * m
    for j in range(len(jobs)):
        assert sum(x[i][j] for i in range(m)) == 1
    loads = [sum(p[i][j] * x[i][j] for j in range(len(jobs))) for i in range(m)]
    assert all(load <= target for load in loads)
    assert all(load == target for load in loads[:-1])
    assert loads[-1] == F(m - 1) + F(1, m)
    assert sum(loads) == m * m
    assert all(p[i][j] <= target for i in range(m) for j in range(len(jobs)))
    return {"m": m, "positive_variables": len(positive), "active_support_rank": rank,
            "target": str(target), "fractional_loads": list(map(str, loads)),
            "fractional_total_work": str(sum(loads))}


def complete_count_oracle(m):
    """Exhaust all count matrices and B positions, using times scaled by m."""
    choices = list(compositions(m - 1, m))
    best_by_offhome = {}
    checked = 0
    for counts in product(choices, repeat=m):
        offhome = sum(sum(row) - row[h] for h, row in enumerate(counts))
        small_loads = [sum(counts[h][i] * (m if h == i else m + 1)
                           for h in range(m)) for i in range(m)]
        for b in range(m):
            checked += 1
            makespan = max(load + (m * m if i == b else 0)
                           for i, load in enumerate(small_loads))
            best_by_offhome[offhome] = min(best_by_offhome.get(offhome, makespan), makespan)
    optimum = min(best_by_offhome.values())
    assert optimum == m * m + 1
    staircase = []
    for q in range(m * (m - 1) + 1):
        oracle = min(value for offhome, value in best_by_offhome.items() if offhome <= q)
        prediction = max(m * (2 * m - 1 - min(q, m - 1)), m * m + 1)
        assert oracle == prediction, (m, q, oracle, prediction)
        staircase.append({"offhome_budget": q, "minimum_makespan": str(F(oracle, m))})
    assert checked == m * comb(2 * m - 2, m - 1) ** m
    return {"m": m, "count_matrix_and_big_position_states": checked,
            "covers_all_labeled_assignments_up_to_home_type_symmetry": True,
            "number_of_labeled_assignments_covered": m ** (m * (m - 1) + 1),
            "optimum": str(F(optimum, m)), "pareto_staircase": staircase}


def asymptotic_audit(m):
    p, x, jobs, target = family(m)
    loads, slots, edges = slot_matching(p, x)
    assert max(loads) == 2 * m - 1
    ratio = F(2 * m - 1) / target
    assert 2 - ratio == F(m + 2, m * m + 1)
    # Explicit optimal schedule: B on last home and its tasks one per other home.
    assignment = [m - 1]
    seen_last = 0
    for h in jobs[1:]:
        if h == m - 1:
            assignment.append(seen_last)
            seen_last += 1
        else:
            assignment.append(h)
    optimal_loads = [sum(p[i][j] for j in range(len(jobs)) if assignment[j] == i)
                     for i in range(m)]
    assert max(optimal_loads) == target
    assert sum(optimal_loads) == m * m + F(m - 1, m)
    # True LST threshold is m: B has no edge below m; uniform B and home-small
    # form an exact feasible point at m. All original edges survive at m.
    assert all(p[i][j] <= m for i in range(m) for j in range(len(jobs)))
    uniform_loads = [sum(p[i][j] * (F(1, m) if j == 0 else F(jobs[j] == i))
                         for j in range(len(jobs))) for i in range(m)]
    assert uniform_loads == [F(m)] * m
    assert target / m == 1 + F(1, m * m)
    return {"m": m, "slot_matching_makespan": str(max(loads)),
            "target_and_true_optimum": str(target), "ratio": str(ratio),
            "two_minus_ratio": str(2 - ratio), "slots": slots,
            "slot_edges": edges, "explicit_optimal_loads": list(map(str, optimal_loads)),
            "true_lst_threshold": str(m), "optimum_to_lst_ratio": str(target / m)}


def boundary_oracle(m, delta):
    """Independent labeled assignment oracle for delta=0 and delta=1 only."""
    assert delta in (0, 1)
    homes = [h for h in range(m) for _ in range(m - 1)]
    n = len(homes) + 1
    optimum = None
    min_work = None
    face_makespans = set()
    for assignment in product(range(m), repeat=n):
        loads = [0] * m
        loads[assignment[0]] = m
        for j, h in enumerate(homes, 1):
            loads[assignment[j]] += 1 + delta * (assignment[j] != h)
        work = sum(loads)
        value = max(loads)
        optimum = value if optimum is None else min(optimum, value)
        if min_work is None or work < min_work:
            min_work = work
            face_makespans = {value}
        elif work == min_work:
            face_makespans.add(value)
    assert optimum == m + delta
    assert min_work == m * m
    if delta == 1:
        assert face_makespans == {2 * m - 1}
    else:
        # Degenerate delta=0: the all-minimizer-face assertion is false, since
        # the true optimum itself has minimum total work.
        assert m in face_makespans
    return {"m": m, "delta": delta, "labeled_assignments": m ** n,
            "true_optimum": optimum, "minimum_integer_total_work": min_work,
            "makespans_at_minimum_work": sorted(face_makespans),
            "delta_zero_does_not_preserve_whole_face_scope": delta == 0}


def main():
    output = {
        "title": "最小总处理量面、basic顶点与支撑舍入的精确核验",
        "arithmetic": "Python arbitrary precision integers and fractions.Fraction",
        "python": platform.python_version(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "rank_checks": [rank_audit(m) for m in range(2, 9)],
        "complete_oracles": [complete_count_oracle(m) for m in range(2, 5)],
        "independent_degenerate_and_endpoint_oracles": [boundary_oracle(m, delta)
                for m in (2, 3) for delta in (0, 1)],
        "slot_and_optimal_schedule_checks": [asymptotic_audit(m) for m in [2, 3, 4, 8, 16, 32, 64]],
        "limits": [
            "This finite audit is not the general proof.",
            "No solver for the general scheduling problem is implemented.",
            "The point is an assignment-LP basic point, not in the optimal scheduling convex hull.",
            "The minimum-work face is not asserted feasible for the configuration LP.",
            "The obstruction requires support restriction, integral freezing, or exact total-work nonincrease.",
            "Changing the objective, reopening zero edges, or allowing positive work increase is not ruled out."
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
