#!/usr/bin/env python3
"""Exact audit of the compact true-optimal-hull weighted-excess pivot trap."""

from fractions import Fraction as F
import hashlib
import platform
import json
from pathlib import Path


def rank(matrix):
    if not matrix:
        return 0
    mat = [[F(v) for v in row] for row in matrix]
    row = 0
    for col in range(len(mat[0])):
        pivot = next((r for r in range(row, len(mat)) if mat[r][col]), None)
        if pivot is None:
            continue
        mat[row], mat[pivot] = mat[pivot], mat[row]
        scale = mat[row][col]
        mat[row] = [v / scale for v in mat[row]]
        for r in range(len(mat)):
            if r != row and mat[r][col]:
                scale = mat[r][col]
                mat[r] = [a - scale * b for a, b in zip(mat[r], mat[row])]
        row += 1
        if row == len(mat):
            break
    return row


def audit(eps, m):
    assert 0 < eps < 1 and m >= 3 and F(m) > 1 / eps
    q = 1 - F(1, m)
    beta = (1 - eps) / 4
    homes = [f"H{i}" for i in range(m)]
    outside = [f"Z{i}" for i in range(m)]
    jobs = ["B"] + [f"{kind}{i}" for i in range(m) for kind in ("A", "F")]
    p = {(home, "B"): F(1) for home in homes}
    for i in range(m):
        p[homes[i], f"A{i}"] = q
        p[homes[i], f"F{i}"] = F(1, m)
        p[outside[i], f"A{i}"] = beta
        p[outside[i], f"F{i}"] = beta
    assert len(p) == 5 * m
    assert all(0 < value <= 1 for value in p.values())

    witnesses = []
    x = {edge: F(0) for edge in p}
    for h in range(m):
        sigma = {"B": homes[h]}
        for i in range(m):
            for kind in ("A", "F"):
                sigma[f"{kind}{i}"] = outside[i] if i == h else homes[i]
        loads = {machine: F(0) for machine in homes + outside}
        for job, machine in sigma.items():
            assert (machine, job) in p
            loads[machine] += p[machine, job]
            x[machine, job] += F(1, m)
        assert max(loads.values()) == 1
        witnesses.append(sigma)
    for i in range(m):
        assert x[homes[i], "B"] == F(1, m)
        for kind in ("A", "F"):
            assert x[homes[i], f"{kind}{i}"] == q
            assert x[outside[i], f"{kind}{i}"] == F(1, m)

    fixed = {}
    protected = set(homes)

    def inspect(t):
        alive_jobs = [job for job in jobs if job not in fixed]
        variables = [edge for edge in p if edge[1] in alive_jobs and 0 < x[edge] < 1]
        assert all(sum(x.get((machine, job), 0) for machine in homes + outside) == 1
                   for job in jobs)
        excess = {machine: sum((p[edge] * (1 - x[edge]) for edge in variables
                                if edge[0] == machine), F(0))
                  for machine in homes + outside}
        fixed_load = {machine: sum((p[machine, job] for job, selected in fixed.items()
                                    if selected == machine), F(0))
                      for machine in homes + outside}
        for i, home in enumerate(homes):
            fractional_load = sum((p[edge] * x[edge] for edge in variables
                                   if edge[0] == home), F(0))
            assert fixed_load[home] + fractional_load == 1
            assert excess[home] == (q if i < t else 1)
            assert excess[home] > 1 - eps
        if t == 0:
            for sink in outside:
                assert excess[sink] == 2 * beta * q
                assert excess[sink] < 1 - eps
        matrix = []
        for job in alive_jobs:
            matrix.append([F(edge[1] == job) for edge in variables])
        for home in homes:
            matrix.append([p[edge] if edge[0] == home else F(0) for edge in variables])
        actual_rank = rank(matrix)
        a = m - t
        assert len(variables) == m + 4 * a
        assert len(alive_jobs) == 2 * a + 1
        assert len(protected) == m
        if a:
            assert actual_rank == len(alive_jobs) + m
            assert len(variables) - actual_rank == 2 * a - 1
        else:
            assert actual_rank == m == len(variables)
        return variables, excess, fixed_load, {
            "t": t, "N": len(variables), "J": len(alive_jobs), "P": m,
            "rank": actual_rank, "nullity": len(variables) - actual_rank,
            "count_slack": len(variables) - len(alive_jobs) - m,
        }

    states = []
    for i in range(m):
        variables, excess, fixed_load, state = inspect(i)
        states.append(state)
        direction = {
            (homes[i], f"A{i}"): F(1),
            (outside[i], f"A{i}"): F(-1),
            (homes[i], f"F{i}"): F(-(m - 1)),
            (outside[i], f"F{i}"): F(m - 1),
        }
        assert all(edge in variables for edge in direction)
        for job in jobs:
            assert sum((d for edge, d in direction.items() if edge[1] == job), F(0)) == 0
        for home in homes:
            assert sum((p[edge] * d for edge, d in direction.items()
                        if edge[0] == home), F(0)) == 0
        bounds = [(1 - x[edge]) / d if d > 0 else x[edge] / (-d)
                  for edge, d in direction.items()]
        theta = min(bounds)
        assert all(bound == F(1, m) for bound in bounds)
        assert theta == F(1, m)
        assert x[homes[i], "B"] + x[homes[i], f"A{i}"] == 1
        assert (x[homes[i], "B"] + x[homes[i], f"A{i}"]
                + theta * direction[homes[i], f"A{i}"]) > 1
        for edge, d in direction.items():
            x[edge] += theta * d
            assert x[edge] in (0, 1)
        fixed[f"A{i}"] = homes[i]
        fixed[f"F{i}"] = outside[i]
    variables, excess, fixed_load, state = inspect(m)
    states.append(state)
    assert set(job for _, job in variables) == {"B"}
    deficit = sum(((1 - p[edge]) * (1 - x[edge]) for edge in variables), F(0))
    assert deficit == 0 < eps * (len(variables) - 1)
    completions = []
    for home in homes:
        loads = dict(fixed_load)
        loads[home] += 1
        makespan = max(loads.values())
        assert makespan == 2 - F(1, m) > 2 - eps
        completions.append(str(makespan))
    return {
        "epsilon": str(eps), "m": m, "q": str(q), "beta": str(beta),
        "machines": 2 * m, "jobs": 2 * m + 1, "finite_edges": len(p),
        "optimal_witnesses_checked": len(witnesses), "OPT": "1",
        "maximal_pivots": m,
        "terminal_makespan_all_completions": completions[0],
        "terminal_anchor_completions_checked": len(completions),
        "terminal_D": str(deficit), "states": states,
    }


if __name__ == "__main__":
    cases = [(F(1, 2), 3), (F(1, 2), 5), (F(1, 3), 4),
             (F(1, 4), 5), (F(1, 5), 6), (F(1, 10), 11),
             (F(2, 3), 3), (F(3, 4), 4)]
    results = [audit(eps, m) for eps, m in cases]
    payload = {
        "status": "all Fraction checks passed", "case_count": len(results),
        "python_version": platform.python_version(), "arithmetic": "fractions.Fraction; deterministic",
        "command": "python3 tests/audits/unrelated_machines/weighted_excess_zero_defect_trap.py",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cases": results,
        "scope": "Specified legal history only; preserves task equalities and protected loads, not CONFIG/big-count inequalities.",
    }
    print(json.dumps(payload, indent=2))
