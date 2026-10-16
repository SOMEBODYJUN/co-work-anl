#!/usr/bin/env python3
"""对称共同条件矩的单机确定性疏散：精确 2T 阈值审计。

Reproducible exact audit; writes a fresh JSON result only to stdout.

For q >= 2 there are m=2q identical machines and n=mq identical jobs,
each of size 1/q.  D is uniform over assignments with q jobs per machine.
Delete machine 0, fix a chosen c-job package there, and redirect only the
old machine-0 choice of every retained job to one deterministic fallback.
All other choices stay fixed.  Push forward the same pair matrix by RYR^t.

The negative result concerns that specified matrix, not its first moment.
For a q-job deleted package and q jobs in each fallback group, the SAME
first moment has a different, genuinely optimal second-moment certificate.
We construct it by exact regular bipartite multigraph decomposition.

On this uniform instance, P0(1) (LST plus all prefix cardinalities) is
exactly the one-hot assignment system with row count <= q.  The program
checks both true and false conditional capacity rows, not just base rows.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
import platform
import sys


def dimensions(q):
    assert q >= 2
    return 2 * q, 2 * q * q


def old_moment(q, left, right):
    m, n = dimensions(q)
    i, a = left
    k, b = right
    if a == b:
        return F(1, m) if i == k else F()
    return F(q - 1 if i == k else q, m * (n - 1))


def balanced_groups(total, count):
    a, b = divmod(total, count)
    return [a + (i < b) for i in range(count)]


def make_map(q, c, group_sizes):
    m, n = dimensions(q)
    assert len(group_sizes) == m - 1
    assert sum(group_sizes) == n - c
    jobs = tuple(range(c, n))
    fallback = {}
    pos = 0
    for k, size in enumerate(group_sizes, 1):
        for a in jobs[pos : pos + size]:
            fallback[a] = k
        pos += size
    edges = tuple((k, a) for k in range(1, m) for a in jobs)
    preimages = {
        (k, a): ((k, a), (0, a)) if fallback[a] == k else ((k, a),)
        for k, a in edges
    }
    return jobs, fallback, edges, preimages


def check_matrix(q, c, group_sizes):
    """Explicit pair-matrix pushforward, independent of conditional formulas."""
    m, n = dimensions(q)
    jobs, fallback, edges, preimages = make_map(q, c, group_sizes)
    x = {e: F(len(preimages[e]), m) for e in edges}
    y = {
        (e, f): sum((old_moment(q, a, b) for a in preimages[e] for b in preimages[f]), F())
        for e in edges
        for f in edges
    }
    violations = check_certificate(q, x, y, jobs, edges)
    return {"q": q, "c": c, "groups": group_sizes, "passes": not violations,
            "first_violation": violations[:1]}, (x, y, jobs, fallback, edges)


def check_certificate(q, x, y, jobs, edges):
    m, _ = dimensions(q)
    assert all(y[e, e] == x[e] for e in edges)
    assert all(y[e, f] == y[f, e] for e in edges for f in edges)
    assert all(sum((x[k, a] for k in range(1, m)), F()) == 1 for a in jobs)
    for e in edges:
        for a in jobs:
            assert sum((y[e, (k, a)] for k in range(1, m)), F()) == x[e]
    violations = []
    for k in range(1, m):
        mean = sum((x[k, a] for a in jobs), F())
        if mean > q:
            violations.append(("base", k, str(mean - q)))
        for e in edges:
            true_mass = sum((y[(k, a), e] for a in jobs), F())
            if true_mass > q * x[e]:
                violations.append(("true", k, e, str(true_mass - q * x[e])))
            false_mass = mean - true_mass
            if false_mass > q * (1 - x[e]):
                violations.append(("false", k, e, str(false_mass - q * (1 - x[e]))))
    return violations


def perfect_matching(jobs, weights, neighbors):
    """One support perfect matching, using iterative alternating-path BFS."""
    from collections import deque
    match_job, match_slot = {}, {}
    for start in jobs:
        pending = deque([start])
        seen_jobs = {start}
        previous_slot = {}
        free_slot = None
        while pending and free_slot is None:
            a = pending.popleft()
            for slot in neighbors[a]:
                if weights[a, slot] == 0 or slot in previous_slot:
                    continue
                previous_slot[slot] = a
                if slot not in match_slot:
                    free_slot = slot
                    break
                old_job = match_slot[slot]
                if old_job not in seen_jobs:
                    seen_jobs.add(old_job)
                    pending.append(old_job)
        assert free_slot is not None, "regular bipartite support must have a perfect matching"
        slot = free_slot
        while True:
            a = previous_slot[slot]
            old_slot = match_job.get(a)
            match_job[a] = slot
            match_slot[slot] = a
            if a == start:
                break
            assert old_slot is not None
            slot = old_slot
    assert len(match_job) == len(jobs)
    return match_job


def rebuild_same_base(q, build_pair_matrix):
    """Keep x'=Rx for c=q, f_k=q, and rebuild a true optimal pair matrix."""
    m, _ = dimensions(q)
    c = q
    groups = [q] * (m - 1)
    jobs, fallback, edges, preimages = make_map(q, c, groups)
    x = {e: F(len(preimages[e]), m) for e in edges}
    assert all(sum((x[k, a] for a in jobs), F()) == q for k in range(1, m))
    weights = Counter()
    for k in range(1, m):
        local_slot = 0
        capacity_left = m
        for a in jobs:
            amount = x[k, a] * m
            assert amount.denominator == 1
            amount = amount.numerator
            while amount:
                take = min(amount, capacity_left)
                slot = (k - 1) * q + local_slot
                weights[a, slot] += take
                amount -= take
                capacity_left -= take
                if capacity_left == 0:
                    local_slot += 1
                    capacity_left = m
        assert local_slot == q and capacity_left == m
    neighbors = {a: tuple(sorted(slot for b, slot in weights if b == a)) for a in jobs}
    assert all(sum(weights[a, slot] for slot in neighbors[a]) == m for a in jobs)
    assert all(sum(weights[a, slot] for a in jobs) == m for slot in range(len(jobs)))
    schedules = []
    for _ in range(m):
        matching = perfect_matching(jobs, weights, neighbors)
        schedule = {a: 1 + matching[a] // q for a in jobs}
        assert all(sum(schedule[a] == k for a in jobs) == q for k in range(1, m))
        schedules.append(schedule)
        for a, slot in matching.items():
            assert weights[a, slot] > 0
            weights[a, slot] -= 1
    assert all(value == 0 for value in weights.values())
    marginal_counts = Counter((schedule[a], a) for schedule in schedules for a in jobs)
    assert all(F(marginal_counts[e], m) == x[e] for e in edges)
    result = {"q": q, "deleted_package_load": str(F(c, q)),
              "schedule_count": m, "same_base_preserved": True,
              "each_schedule_makespan": "1", "explicit_pair_matrix_checked": build_pair_matrix}
    if build_pair_matrix:
        pair_counts = Counter()
        for schedule in schedules:
            literals = tuple((schedule[a], a) for a in jobs)
            for e, f in product(literals, repeat=2):
                pair_counts[e, f] += 1
        rebuilt = {(e, f): F(pair_counts[e, f], m) for e in edges for f in edges}
        assert not check_certificate(q, x, rebuilt, jobs, edges)
        pushed = {
            (e, f): sum((old_moment(q, a, b) for a in preimages[e] for b in preimages[f]), F())
            for e in edges for f in edges
        }
        difference = next((e, f, str(pushed[e, f]), str(rebuilt[e, f]))
                          for e in edges for f in edges if pushed[e, f] != rebuilt[e, f])
        result["different_second_moment_entry"] = difference
    return result


def conditional_count(q, c, f, kind):
    _, n = dimensions(q)
    retained = n - c
    if kind == "merged_same":
        return 1 + F((2 * q - 1) * (retained + f - 2), 2 * (n - 1))
    if kind == "merged_other":
        return F(2 * q * (retained - 1) + (2 * q - 1) * f, 2 * (n - 1))
    if kind == "unmerged_same":
        return 1 + F((q - 1) * (retained - 1) + q * f, n - 1)
    if kind == "unmerged_fallback":
        return F(q * (retained + f - 2), n - 1)
    if kind == "unmerged_other":
        return F(q * (retained + f - 1), n - 1)
    raise ValueError(kind)


def all_balanced_assignments(q):
    m, n = dimensions(q)
    state = [-1] * n

    def rec(machine, remaining):
        if machine == m - 1:
            assert len(remaining) == q
            for a in remaining:
                state[a] = machine
            yield tuple(state)
            return
        for chosen in combinations(remaining, q):
            chosen_set = set(chosen)
            for a in chosen:
                state[a] = machine
            yield from rec(machine + 1, tuple(a for a in remaining if a not in chosen_set))

    yield from rec(0, tuple(range(n)))


def enumerate_q2():
    q = 2
    m, n = dimensions(q)
    states = tuple(all_balanced_assignments(q))
    assert len(states) == factorial(n) // factorial(q) ** m
    counts = Counter()
    for state in states:
        literals = tuple((state[a], a) for a in range(n))
        for e, f in product(literals, repeat=2):
            counts[e, f] += 1
    for e, f in product(product(range(m), range(n)), repeat=2):
        assert F(counts[e, f], len(states)) == old_moment(q, e, f)
    cases = []
    for c in [0, 1, 2, 3, 4]:
        sizes = balanced_groups(n - c, m - 1)
        result, data = check_matrix(q, c, sizes)
        x, y, jobs, fallback, edges = data
        mapped_counts = Counter()
        for state in states:
            literals = tuple((fallback[a] if state[a] == 0 else state[a], a) for a in jobs)
            for e, f in product(literals, repeat=2):
                mapped_counts[e, f] += 1
        assert all(F(mapped_counts[e, f], len(states)) == y[e, f] for e in edges for f in edges)
        assert result["passes"] == (c == 4)
        cases.append(result)
    return {"full_balanced_assignments": len(states), "cases": cases}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-q", type=int, default=32)
    args = parser.parse_args()
    assert args.max_q >= 4
    negative_checks = 0
    positive_formula_checks = 0
    for q in range(2, args.max_q + 1):
        m, n = dimensions(q)
        for c in range(2 * q):
            f = (n - c + m - 2) // (m - 1)
            assert f >= q
            over = conditional_count(q, c, f, "merged_same") - q
            bound = F(q - 1, 2 * (n - 1))
            assert over >= bound > 0
            assert over == F((2 * q - 1) * (f - c) + n - 2 * q, 2 * (n - 1))
            negative_checks += 1
        c = 2 * q
        sizes = [q - 1] * q + [q] * (q - 1)
        assert len(sizes) == m - 1 and sum(sizes) == n - c
        for f in set(sizes):
            for kind in ["merged_same", "merged_other", "unmerged_same",
                         "unmerged_fallback", "unmerged_other"]:
                value = conditional_count(q, c, f, kind)
                multiplicity = 2 if kind.startswith("merged") else 1
                assert 0 <= value <= q
                assert multiplicity * (q - value) <= c - f
                positive_formula_checks += 1
    matrices = []
    for q in range(2, 5):
        m, n = dimensions(q)
        for c in [q, 2 * q - 1, 2 * q]:
            sizes = balanced_groups(n - c, m - 1)
            result, _ = check_matrix(q, c, sizes)
            assert result["passes"] == (c == 2 * q)
            matrices.append(result)
    import json
    print(json.dumps({
        "title": "对称共同条件矩的单机确定性疏散精确阈值",
        "status": "finite audit; theorem requires general proof",
        "python": sys.version,
        "platform": platform.platform(),
        "arithmetic": "fractions.Fraction; no floating point; exhaustive q=2 balanced assignments",
        "q_range": [2, args.max_q],
        "negative_parameter_checks": negative_checks,
        "positive_conditional_formula_checks": positive_formula_checks,
        "explicit_matrix_checks": matrices,
        "independent_full_distribution": enumerate_q2(),
        "honest_positive_same_base_reconstruction": [
            rebuild_same_base(q, q <= 4) for q in range(2, 9)
        ],
        "scope": "same pair matrix pushforward; only old deleted-machine choices redirect; other choices fixed",
        "not_claimed": "no general N(P0) gap, no obstruction to re-solving moments, multi-machine transport, or UM-TARGET-v1; the same base at c=q has an explicit valid rebuilt certificate",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
