#!/usr/bin/env python3
"""Exact finite audits of the top-two matching bound and SAT sharpness.

All processing times in this audit are integers representing half time units.
This is an audit implementation; it accepts exact Fraction inputs as well.
"""

import argparse
from collections import deque
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import shlex
import sys


def matching_assignment(rows, target):
    """Return None only if the heavy-job matching fails; job-major rows."""
    if any(not any(p is not None for p in row) for row in rows):
        return None
    minima = [min(p for p in row if p is not None) for row in rows]
    heavy = [j for j, q in enumerate(minima) if 2 * q > target]
    owner = {}
    assigned_machine = {}

    def augment(root):
        queue = deque([root])
        seen_jobs = {root}
        parent_machine = {}
        while queue:
            j = queue.popleft()
            for i, p in enumerate(rows[j]):
                if p is None or p > target or i in parent_machine:
                    continue
                parent_machine[i] = j
                if i not in owner:
                    # Flip the alternating path, with no recursion limit.
                    current = i
                    while True:
                        path_job = parent_machine[current]
                        previous = assigned_machine.get(path_job)
                        owner[current] = path_job
                        assigned_machine[path_job] = current
                        if previous is None:
                            return True
                        current = previous
                next_job = owner[i]
                if next_job not in seen_jobs:
                    seen_jobs.add(next_job)
                    queue.append(next_job)
        return False

    for j in heavy:
        if not augment(j):
            return None
    result = [None] * len(rows)
    for i, j in owner.items():
        result[j] = i
    for j, q in enumerate(minima):
        if result[j] is None:
            result[j] = rows[j].index(q)
    return tuple(result)


def objective(rows, assignment):
    if assignment is None:
        return None
    by_machine = {}
    for row, i in zip(rows, assignment):
        p = row[i]
        assert p is not None
        by_machine.setdefault(i, []).append(p)
    return max((sum(sorted(a, reverse=True)[:2]) for a in by_machine.values()), default=0)


def exact_top_two(rows):
    domains = [tuple(i for i, p in enumerate(row) if p is not None) for row in rows]
    if any(not domain for domain in domains):
        return None
    return min((objective(rows, a) for a in product(*domains)), default=0)


def optimized_matching(rows):
    if any(not any(p is not None for p in row) for row in rows):
        return None, None
    breakpoints = {0}
    for row in rows:
        breakpoints.update(p for p in row if p is not None)
        breakpoints.add(2 * min(p for p in row if p is not None))
    for target in sorted(breakpoints):
        assignment = matching_assignment(rows, target)
        if assignment is not None:
            return target, assignment
    raise AssertionError("A finite instance must eventually have no heavy jobs")


def matrix_audit(machines, jobs, values):
    count = feasible = zero = tight = 0
    for entries in product(values, repeat=machines * jobs):
        rows = [entries[j * machines:(j + 1) * machines] for j in range(jobs)]
        opt = exact_top_two(rows)
        target, assignment = optimized_matching(rows)
        count += 1
        if opt is None:
            assert target is None and assignment is None
            continue
        feasible += 1
        bound = objective(rows, assignment)
        assert target <= opt
        assert 2 * bound <= 3 * target
        assert 2 * bound <= 3 * opt
        if opt == 0:
            zero += 1
            assert bound == target == 0
        elif 2 * bound == 3 * opt:
            tight += 1
        # Verify that success is monotone at every actual breakpoint.
        candidates = sorted({0} | {p for row in rows for p in row if p is not None}
                            | {2 * min(p for p in row if p is not None) for row in rows})
        outcomes = [matching_assignment(rows, t) is not None for t in candidates]
        assert outcomes == sorted(outcomes)
    return {"machines": machines, "jobs": jobs, "matrices": count,
            "finite_feasible": feasible, "zero_optimum": zero,
            "invalid_job_without_finite_incidence": count - feasible,
            "algorithm_ratio_exactly_3_over_2": tight}


def split_sat_instance(clauses):
    """Uniform occurrence-copy cycle construction; literals are signed ints."""
    occurrences = {}
    copied_clauses = []
    copy_count = 0
    for clause in clauses:
        copied = []
        for literal in clause:
            copy_count += 1
            occurrences.setdefault(abs(literal), []).append(copy_count)
            copied.append(copy_count if literal > 0 else -copy_count)
        copied_clauses.append(tuple(copied))
    implications = []
    for cycle in occurrences.values():
        implications.extend((-copy, cycle[(index + 1) % len(cycle)])
                            for index, copy in enumerate(cycle))
    machine_count = 2 * copy_count
    rows = []
    for copy in range(1, copy_count + 1):
        row = [None] * machine_count
        row[2 * copy - 2] = row[2 * copy - 1] = 2
        rows.append(tuple(row))
    for clause in copied_clauses + implications:
        row = [None] * machine_count
        for literal in clause:
            machine = 2 * abs(literal) - 2 + (literal < 0)
            row[machine] = 1
        rows.append(tuple(row))
    return rows, copy_count


def sat(clauses):
    variables = sorted({abs(lit) for clause in clauses for lit in clause})
    for bits in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, bits))
        if all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in clauses):
            return True
    return False


def sharpness_audit():
    # Exhaust all subsets of the four unit and four distinct binary clauses
    # over two variables. Enumerate every possible unit-job placement.
    atoms = ((1,), (-1,), (2,), (-2,),
             (1, 2), (1, -2), (-1, 2), (-1, -2))
    formulas = satisfiable = unit_placements = 0
    unsat_pair_witnesses = 0
    for mask in range(1 << len(atoms)):
        clauses = [atoms[i] for i in range(len(atoms)) if mask & (1 << i)]
        expected = sat(clauses)
        rows, heavy_count = split_sat_instance(clauses)
        assert all(sum(p is not None for p in row) <= 3 for row in rows)
        assert all(sum(row[i] is not None for row in rows) <= 3
                   for i in range(2 * heavy_count))
        pair_safe_exists = False
        for bits in product((0, 1), repeat=heavy_count):
            unit_placements += 1
            blocked = {2 * copy + bit for copy, bit in enumerate(bits)}
            assignment = [2 * copy + bit for copy, bit in enumerate(bits)]
            possible = True
            for row in rows[heavy_count:]:
                choices = [i for i, p in enumerate(row) if p is not None and i not in blocked]
                if not choices:
                    possible = False
                    break
                assignment.append(choices[0])
            if possible:
                # Free literal machines have at most two half-jobs.
                assert objective(rows, assignment) <= 2
                pair_safe_exists = True
            elif not expected:
                unsat_pair_witnesses += 1
        assert pair_safe_exists == expected
        # Every assignment has top-two <=3 regardless of small job placement:
        # each machine has <=one unit job and <=two half jobs.
        assert all(sum(p == 2 for p in (row[i] for row in rows)) <= 1
                   for i in range(2 * heavy_count))
        formulas += 1
        satisfiable += expected
    return {"formulas": formulas, "satisfiable": satisfiable,
            "unsatisfiable": formulas - satisfiable,
            "unit_job_placements_exhausted": unit_placements,
            "unsat_placements_with_unavoidable_unit_plus_half_pair": unsat_pair_witnesses}


def degeneracy_audit():
    assert optimized_matching([]) == (0, ())
    assert optimized_matching([()]) == (None, None)
    assert optimized_matching([(None, None)]) == (None, None)
    assert optimized_matching([(0, None), (0, None)]) == (0, (0, 0))
    tiny = Fraction(1, 10**100)
    rows = [(tiny, None), (None, 1), (tiny, 1)]
    target, assignment = optimized_matching(rows)
    assert objective(rows, assignment) <= Fraction(3, 2) * exact_top_two(rows)
    assert target <= exact_top_two(rows)
    return {"empty_jobs": "pass", "zero_machines_nonempty_jobs": "pass",
            "job_with_no_finite_incidence": "pass", "zero_optimum": "pass",
            "100_digit_denominator": "pass"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path,
                        help="New JSON output path; existing files are never overwritten")
    parser.add_argument("--base-commit", default=None,
                        help="Optional parent-supplied git commit; this script never invokes git")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error(f"Refusing to overwrite existing output: {output}")
    source = Path(__file__).resolve()
    results = {
        "provenance": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "base_commit": args.base_commit,
            "base_commit_note": "Parent-supplied only; git was not accessed",
            "source_path": str(source),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "seed": None,
            "randomness": "none; all reported families are exhaustive",
            "parameters": {
                "processing_time_scale": "2 integer units = one physical time unit",
                "matrix_families": [
                    {"machines": 2, "jobs": 4, "values": [None, 0, 1, 2]},
                    {"machines": 3, "jobs": 3, "values": [None, 1, 2]},
                ],
                "sharpness_atoms": [[1], [-1], [2], [-2], [1, 2], [1, -2], [-1, 2], [-1, -2]],
            },
            "limits": [
                "Finite audits do not replace the proof for arbitrary matrix dimensions",
                "SAT audit exhausts two-variable unit/binary-clause subsets, not all 3CNF inputs",
                "Cases with a job lacking a finite incidence are separately counted as invalid",
                "The rational bit-length audit includes one 100-digit denominator, not all bit lengths",
            ],
            "replay": " ".join(shlex.quote(part) for part in
                               [sys.executable, str(source), "--output", "<fresh-output-path>.json"]),
        },
        "arithmetic": "integer half-units, with a separate exact Fraction bit-length case",
        "matrix_audits": [matrix_audit(2, 4, (None, 0, 1, 2)),
                          matrix_audit(3, 3, (None, 1, 2))],
        "sharpness_audit": sharpness_audit(),
        "degeneracies": degeneracy_audit(),
        "errors": 0,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x") as stream:
        stream.write(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
