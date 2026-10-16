#!/usr/bin/env python3
"""Exact finite audit of pair-configuration coupling and edge subdivision.

Not a configuration LP solver and not a new approximation algorithm.  The
explicit VW generator is deliberately limited to k <= 4.  All checks use
Fraction; exhaustive oracles are used only for the documented small cases.
The command writes JSON to stdout and never overwrites frozen evidence.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform

import rounding_and_gap as baseline


def endpoints(p, j):
    result = [i for i, row in enumerate(p) if row[j] is not None]
    if len(result) != 2:
        raise ValueError("Exactly two distinct eligible machines required")
    return result


def certificate(p, configs, target):
    p = baseline.matrix(p)
    target = baseline.rational(target)
    if target < 0 or len(configs) != len(p):
        raise ValueError("Invalid configuration dimensions or target")
    marginals = [[F(0) for _ in p[0]] for _ in p]
    for i, choices in enumerate(configs):
        if sum(w for w, _ in choices) != 1:
            raise ValueError("Machine mass not one")
        for w, jobs in choices:
            if w < 0 or len(set(jobs)) != len(jobs):
                raise ValueError("Invalid weight or repeated job")
            if any(p[i][j] is None for j in jobs):
                raise ValueError("Unavailable processing time")
            if sum(p[i][j] for j in jobs) > target:
                raise ValueError("Overloaded configuration")
            for j in jobs:
                marginals[i][j] += w
    if any(sum(row[j] for row in marginals) != 1 for j in range(len(p[0]))):
        raise ValueError("Job marginal not one")
    return marginals


def subdivide(p, configs, target, middle_time=1):
    """Replace every job by two jobs, adding one capacity-one middle machine."""
    p = baseline.matrix(p)
    h = baseline.rational(middle_time)
    if h <= 0 or h > target:
        raise ValueError("Require 0 < middle_time <= target")
    x = certificate(p, configs, target)
    m, n = len(p), len(p[0])
    out = [[None] * (2*n) for _ in range(m+n)]
    mapped = [{} for _ in p]
    new_configs = [[] for _ in range(m+n)]
    for j in range(n):
        u, v = endpoints(p, j)
        out[u][2*j], out[v][2*j+1] = p[u][j], p[v][j]
        out[m+j][2*j] = out[m+j][2*j+1] = h
        mapped[u][j], mapped[v][j] = 2*j, 2*j+1
        # The outer-u marginal of its own job is x[u,j]. Its middle marginal
        # is therefore x[v,j], and conversely for the other new job.
        new_configs[m+j] = [(x[v][j], (2*j,)), (x[u][j], (2*j+1,))]
    for i, choices in enumerate(configs):
        new_configs[i] = [(w, tuple(mapped[i][j] for j in jobs))
                          for w, jobs in choices]
    certificate(out, new_configs, target)
    return out, new_configs


def lift_assignment(p, assignment):
    """Keep the chosen endpoint's subjob outside and the other subjob inside."""
    baseline.loads(p, assignment)
    m = len(p)
    result = []
    for j, i in enumerate(assignment):
        u, v = endpoints(p, j)
        result.extend((u, m+j) if i == u else (m+j, v))
    return result


def compress_assignment(p, expanded, assignment, middle_time=1):
    """For schedules below 2H, choose an outside subjob for each original job."""
    actual = baseline.loads(expanded, assignment)
    h = baseline.rational(middle_time)
    if max(actual) >= 2*h:
        raise ValueError("Compression contract requires makespan < 2H")
    m = len(p)
    result = []
    for j in range(len(p[0])):
        u, v = endpoints(p, j)
        if assignment[2*j] == u:
            result.append(u)
        elif assignment[2*j+1] == v:
            result.append(v)
        else:
            raise AssertionError("Both subjobs at the middle machine")
    old_loads = baseline.loads(p, result)
    assert all(a <= b for a, b in zip(old_loads, actual[:m]))
    return result


def pair_distribution(left, right, shared):
    """Couple configurations with complementary indicators of <=1 common job."""
    if len(shared) > 1:
        raise ValueError("This lemma only applies to a simple machine graph")
    result = []
    if not shared:
        return [(a, b, w*z) for a, (w, _) in enumerate(left)
                for b, (z, _) in enumerate(right) if w*z]
    j = next(iter(shared))
    a = sum(w for w, jobs in left if j in jobs)
    b = sum(w for w, jobs in right if j in jobs)
    if a+b != 1:
        raise ValueError("Complementary job marginals required")
    for s, (w, first) in enumerate(left):
        for t, (z, second) in enumerate(right):
            if (j in first) == (j in second):
                continue
            denominator = a if j in first else 1-a
            if w*z:
                assert denominator > 0
                result.append((s, t, w*z/denominator))
    return result


def check_all_pairs(p, configs):
    count, entries = 0, 0
    for u, v in combinations(range(len(p)), 2):
        shared = {j for j in range(len(p[0]))
                  if p[u][j] is not None and p[v][j] is not None}
        assert len(shared) <= 1
        joint = pair_distribution(configs[u], configs[v], shared)
        assert sum(z for _, _, z in joint) == 1
        for s, (w, _) in enumerate(configs[u]):
            assert sum(z for a, _, z in joint if a == s) == w
        for t, (w, _) in enumerate(configs[v]):
            assert sum(z for _, b, z in joint if b == t) == w
        for s, t, z in joint:
            assert z >= 0
            assert all((j in configs[u][s][1]) + (j in configs[v][t][1]) == 1
                       for j in shared)
        count += 1
        entries += len(joint)
    return count, entries


def expanded_exhaustive(p, expanded):
    """Independent load enumeration; additionally check every legal compression."""
    options = [[i for i, row in enumerate(expanded) if row[j] is not None]
               for j in range(len(expanded[0]))]
    best, number, compressed = None, 0, 0
    for assignment in product(*options):
        number += 1
        ls = [F(0) for _ in expanded]
        for j, i in enumerate(assignment):
            ls[i] += expanded[i][j]
        value = max(ls)
        best = value if best is None else min(best, value)
        if value < 2:
            old = compress_assignment(p, expanded, assignment)
            independent = [sum(p[i][j] for j, v in enumerate(old) if v == i)
                           for i in range(len(p))]
            assert max(independent) <= value
            compressed += 1
    return best, number, compressed


def audit():
    rows = []
    for k in (2, 3, 4):
        p, y, t = baseline.gap_instance(k)
        new_p, new_y = subdivide(p, y, t)
        pairs, joint_entries = check_all_pairs(new_p, new_y)
        theta = F(2*k-1, k)
        assert theta/t == 2-F(3, k+1)
        assert (2-F(3, k+1))*t == theta
        row = {"k": k, "old_m": len(p), "old_n": len(p[0]),
               "new_m": len(new_p), "new_n": len(new_p[0]),
               "target": str(t), "proved_optimum": str(theta),
               "certified_ratio": str(theta/t), "all_pair_couplings": pairs,
               "positive_joint_entries": joint_entries,
               "configuration_certificate": "exactly verified"}
        if k <= 3:
            opt, sigma, original_count = baseline.exhaustive_optimum(p)
            assert opt == theta
            lifted = lift_assignment(p, sigma)
            assert max(baseline.loads(new_p, lifted)) == theta
            independent, number, compressed = expanded_exhaustive(p, new_p)
            assert independent == theta
            row.update(original_assignments=original_count,
                       expanded_assignments=number,
                       expanded_below_two_compressed=compressed,
                       exhaustive_optimum=str(independent))
        rows.append(row)
    # Zero/one marginals: all jobs forced by the chosen integral certificate;
    # empty jobs, zero processing and a denominator much larger than bit budgets
    # in tiny integer tests. These are finite boundary checks, not bit proofs.
    edge_cases = [([[0], [0]], [[(F(1), (0,))], [(F(1), ())]], 1),
                  ([[], []], [[(F(1), ())], [(F(1), ())]], 1),
                  ([[F(1, 2**257+93)], [1]],
                   [[(F(1), (0,))], [(F(1), ())]], 1)]
    for p, y, t in edge_cases:
        new_p, new_y = subdivide(p, y, t)
        check_all_pairs(new_p, new_y)
    # The claimed old-VW moment obstruction is checked from its actual leaf
    # configurations, not inferred from a numeric LP solution.
    residuals = []
    for k in (3, 4):
        p, y, t = baseline.gap_instance(k)
        found = 0
        for u, v in combinations(range(len(p)), 2):
            bundle = [j for j in range(len(p[0]))
                      if p[u][j] is not None and p[v][j] is not None]
            if len(bundle) != k:
                continue
            if all(p[u][j] == 1 for j in bundle):
                u, v = v, u
            for j, ell in combinations(bundle, 2):
                parent_miss = sum(w for w, s in y[u] if j not in s and ell not in s)
                terminal_pair = sum(w for w, s in y[v] if j in s and ell in s)
                assert parent_miss == F(k-2, k*(k-1)) > 0
                assert terminal_pair == 0
                found += 1
        residuals.append({"k": k, "pair_obstructions_checked": found,
                          "per_pair_residual": str(F(k-2, k*(k-1)))})
    return {"schema_version": 1, "python_version": platform.python_version(),
            "arithmetic": "exact fractions.Fraction; deterministic; no seed",
            "command": "python3 tests/audits/unrelated_machines/pair_coupling_subdivision.py",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "baseline_sha256": hashlib.sha256(Path(baseline.__file__).read_bytes()).hexdigest(),
            "subdivision": rows, "moment_residuals": residuals,
            "boundary_fixtures": len(edge_cases),
            "limitations": ["Expanded VW families only k=2,3,4; no k>4 graph materialization",
                            "Integer exhaustive checks only k=2,3; general proof is separate",
                            "No generic configuration solver, SA solver or approximation breakthrough",
                            "Novelty and external peer review not certified"]}


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
