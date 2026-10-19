#!/usr/bin/env python3
"""Exact audit-only constructions for bounded multiplicity clone wiring.

No imports from the research repository and no floating-point arithmetic.
This is not a generic MC_c solver or an algorithm for general UM.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json
import platform


def verify_schedule(machines, jobs, assignment):
    assert set(assignment) == set(jobs)
    loads = {i: F(0) for i in machines}
    for j, i in assignment.items():
        assert i in jobs[j], (j, i)
        loads[i] += jobs[j][i]
    return loads


def brute_opt(machines, jobs):
    """Enumerate every actual assignment; used on tiny complete inputs only."""
    labels = list(jobs)
    best, count = None, 0
    for dests in product(*(list(jobs[j]) for j in labels)):
        count += 1
        loads = verify_schedule(machines, jobs, dict(zip(labels, dests)))
        value = max(loads.values(), default=F(0))
        if best is None or value < best:
            best = value
    assert best is not None
    return best, count


def near_two_seed(m):
    assert m >= 2
    machines = list(range(m))
    jobs = {("B",): {i: F(1) for i in machines}}
    for i in machines:
        for t in range(1, m):
            jobs[("U", i, t)] = {i: F(1, m)}
    return machines, jobs


def clone_matrix(machines, jobs, q, perm_families):
    """Expand every original job, machine and finite incidence in full."""
    copies = [(i, s) for i in machines for s in range(q)]
    clone_jobs = {}
    for j, ends in jobs.items():
        for r in range(q):
            edges = {}
            for i, p in ends.items():
                family = perm_families[i, j]
                assert family
                for pi in family:
                    assert sorted(pi) == list(range(q))
                    edges[i, pi[r]] = p
            clone_jobs[j, r] = edges
    assert set(perm_families) == {(i, j) for j in jobs for i in jobs[j]}
    return copies, clone_jobs


def common_cycle(m):
    machines, jobs = near_two_seed(m)
    ident = tuple(range(m))
    shift = tuple((x + 1) % m for x in range(m))
    wiring = {(i, j): [ident, shift] for j in jobs for i in jobs[j]}
    clone_machines, clone_jobs = clone_matrix(machines, jobs, m, wiring)
    actual = {}
    for (j, x) in clone_jobs:
        if j == ("B",):
            actual[j, x] = (x, x)
        else:
            _, i, t = j
            d = (x - i) % m
            actual[j, x] = (i, (x + int(d < t)) % m)
    loads = verify_schedule(clone_machines, clone_jobs, actual)
    assert set(loads.values()) == {F(1)}
    assert len(clone_machines) == m * m
    assert len(clone_jobs) == m + m * m * (m - 1)
    edge_count = sum(map(len, clone_jobs.values()))
    assert edge_count == 2 * m**3

    # Verify the per-original-private-type occupancy independently from loads.
    for i in machines:
        for t in range(1, m):
            multiplicity = Counter(actual[("U", i, t), x][1] for x in range(m))
            assert multiplicity[i] == 0
            assert multiplicity[(i + t) % m] == 2
            assert all(multiplicity[s] == 1 for s in range(m)
                       if s not in {i, (i + t) % m})

    # Each individual original incidence has precisely one 2m-cycle.
    graph = defaultdict(set)
    for x in range(m):
        for s in {x, (x + 1) % m}:
            graph["j", x].add(("i", s))
            graph["i", s].add(("j", x))
    assert len(graph) == 2 * m
    assert all(len(ns) == 2 for ns in graph.values())
    seen, queue = set(), [("j", 0)]
    while queue:
        v = queue.pop()
        if v not in seen:
            seen.add(v)
            queue.extend(graph[v] - seen)
    assert len(seen) == 2 * m
    return clone_machines, clone_jobs, actual, {
        "m": m, "original_jobs": len(jobs), "original_opt": str(F(2) - F(1, m)),
        "clone_copies": m, "clone_machines": len(clone_machines),
        "clone_jobs": len(clone_jobs), "finite_edges": edge_count,
        "all_machine_loads": "1", "individual_incidence_cycle_length": 2 * m,
    }


def lift_certificate(machines, jobs, c, threshold, certificate):
    """General rational MC_c point -> c permutations + all actual job copies.

    Certificate maps each machine to [(multiplicity dict, rational weight)].
    Coloring is by the target's occurrence number, then each partial matching
    is extended to a full permutation, including arbitrary unused incidences.
    """
    assert c >= 1 and threshold >= 0
    q, coverage = 1, {j: F(0) for j in jobs}
    for i in machines:
        assert sum((w for _, w in certificate[i]), F(0)) == 1
        for a, w in certificate[i]:
            assert isinstance(w, F) and w >= 0
            q = lcm(q, w.denominator)
            assert all(isinstance(v, int) and 0 <= v <= c for v in a.values())
            assert all(j in jobs and i in jobs[j] for j in a if a[j])
            assert sum((jobs[j][i] * v for j, v in a.items() if v), F(0)) <= threshold
            for j, v in a.items():
                coverage[j] += w * v
    assert all(v == 1 for v in coverage.values())

    desired = {}
    sockets = defaultdict(list)
    for i in machines:
        s = 0
        for a, w in certificate[i]:
            repeats = q * w
            assert repeats.denominator == 1
            for _ in range(repeats.numerator):
                desired[i, s] = {j: v for j, v in a.items() if v}
                for j, v in a.items():
                    sockets[j].extend([(i, s)] * v)
                s += 1
        assert s == q

    actual = {}
    used = defaultdict(list)
    for j in jobs:
        assert len(sockets[j]) == q
        for r, (i, s) in enumerate(sockets[j]):
            actual[j, r] = (i, s)
            used[i, j].append((r, s))

    wiring = {}
    for j, ends in jobs.items():
        for i in ends:
            partials = [{} for _ in range(c)]
            target_next_color = Counter()
            for r, s in used[i, j]:
                h = target_next_color[s]
                target_next_color[s] += 1
                assert h < c
                assert r not in partials[h] and s not in partials[h].values()
                partials[h][r] = s
            family = []
            for partial in partials:
                unused_left = [r for r in range(q) if r not in partial]
                used_right = set(partial.values())
                unused_right = [s for s in range(q) if s not in used_right]
                full = dict(partial)
                full.update(zip(unused_left, unused_right))
                pi = tuple(full[r] for r in range(q))
                assert sorted(pi) == list(range(q))
                family.append(pi)
            wiring[i, j] = family

    clone_machines, clone_jobs = clone_matrix(machines, jobs, q, wiring)
    loads = verify_schedule(clone_machines, clone_jobs, actual)
    assert max(loads.values(), default=F(0)) <= threshold
    observed = {i: Counter() for i in clone_machines}
    for (j, _), i in actual.items():
        observed[i][j] += 1
    assert all(dict(observed[i]) == desired[i] for i in clone_machines)
    return {
        "cap": c, "threshold": str(threshold), "denominator_q": q,
        "machines": len(clone_machines), "jobs": len(clone_jobs),
        "finite_edges": sum(map(len, clone_jobs.values())),
        "actual_peak": str(max(loads.values(), default=F(0))),
    }


def strict_hierarchy(c):
    machines = list(range(c + 1))
    jobs = {("B", b): {i: F(1) for i in machines} for b in range(c)}
    for i in machines:
        jobs["U", i] = {i: F(1, c + 1)}
    cert = {}
    for i in machines:
        cert[i] = [({("U", i): c + 1}, F(1, c + 1))]
        cert[i] += [({("B", b): 1}, F(1, c + 1)) for b in range(c)]
    result = lift_certificate(machines, jobs, c + 1, F(1), cert)
    # Enumerate all one-row multiplicity vectors at thresholds in [1,next).
    # Unit configurations hold a single unit; private-only configs hold <=c.
    feasible_at_one = []
    sizes = [F(1)] * c + [F(1, c + 1)]
    for a in product(range(c + 1), repeat=c + 1):
        if sum((x * p for x, p in zip(a, sizes)), F(0)) <= 1:
            feasible_at_one.append(a)
            if any(a[:c]):
                assert sum(a[:c]) == 1 and a[-1] == 0
    assert max(a[-1] for a in feasible_at_one) == c
    result.update({"lower_cap": c, "lower_cap_threshold": str(F(1) + F(1, c + 1)),
                   "number_local_lower_cap_configs_at_one": len(feasible_at_one)})
    return result


def exhaust_all_two_label_wirings():
    machines, jobs = near_two_seed(2)
    q = 2
    ident, swap = (0, 1), (1, 0)
    incidences = [(i, j) for j in jobs for i in jobs[j]]
    one, two = Counter(), Counter()
    counts = Counter()
    # These are precisely all unions of <=2 permutations on two labels.
    choices = [[ident], [swap], [ident, swap]]
    for selected in product(range(3), repeat=len(incidences)):
        wiring = {e: choices[s] for e, s in zip(incidences, selected)}
        cm, cj = clone_matrix(machines, jobs, q, wiring)
        opt, checked = brute_opt(cm, cj)
        assert F(1) <= opt <= F(3, 2)
        two[str(opt)] += 1
        counts["all_assignments"] += checked
        if all(s < 2 for s in selected):
            assert opt == F(3, 2)
            one[str(opt)] += 1
            counts["one_wiring_assignments"] += checked
    assert sum(two.values()) == 81 and sum(one.values()) == 16
    return {"m": 2, "q": 2, "c1_wiring_graphs": sum(one.values()),
            "c1_opt_histogram": dict(one), "c2_wiring_graphs": sum(two.values()),
            "c2_opt_histogram": dict(two), **counts}


def exhaust_denominator_two_certificates():
    """All 2-copy row-config arrays for this heterogeneous positive matrix."""
    machines = [0, 1]
    jobs = {"a": {0: F(1, 2), 1: F(1)},
            "b": {0: F(1), 1: F(1, 2)}}
    configs = {}
    for i in machines:
        configs[i] = [dict(zip(jobs, a)) for a in product(range(3), repeat=2)
                      if sum((jobs[j][i] * v for j, v in zip(jobs, a)), F(0)) <= 1]
    array_count = 0
    unique = set()
    for a0, a1, b0, b1 in product(configs[0], configs[0], configs[1], configs[1]):
        if any(sum(a[j] for a in (a0, a1, b0, b1)) != 2 for j in jobs):
            continue
        array_count += 1
        cert = {0: [(a0, F(1, 2)), (a1, F(1, 2))],
                1: [(b0, F(1, 2)), (b1, F(1, 2))]}
        result = lift_certificate(machines, jobs, 2, F(1), cert)
        assert result["denominator_q"] == 2
        unique.add(tuple(tuple(sorted((tuple(a.items()) for a in (x0, x1))))
                         for x0, x1 in ((a0, a1), (b0, b1))))
    assert array_count
    return {"ordered_configuration_arrays": array_count,
            "distinct_configuration_laws": len(unique), "cap": 2, "q": 2,
            "matrix": [["1/2", "1"], ["1", "1/2"]]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), "Refuse to overwrite an existing report"
    report = {"status": "audit_only", "python": platform.python_version(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    report["common_cycle"] = [common_cycle(m)[3] for m in range(2, 18)]
    report["all_two_label_wirings"] = exhaust_all_two_label_wirings()
    report["all_denominator_two_certificates"] = exhaust_denominator_two_certificates()
    # The local strict-cap Cartesian enumeration is limited to c<=4.
    report["strict_cap_hierarchy"] = [strict_hierarchy(c) for c in range(1, 5)]
    report["zero_boundary"] = lift_certificate(
        [0], {"z": {0: F(0)}}, 2, F(0),
        {0: [({"z": 2}, F(1, 2)), ({}, F(1, 2))]})
    report["empty_boundary"] = lift_certificate(
        [0, 1], {}, 2, F(0), {0: [({}, F(1))], 1: [({}, F(1))]})
    report["explicit_zero_on_unavailable_boundary"] = lift_certificate(
        [0, 1], {"a": {0: F(1)}, "b": {1: F(1)}}, 2, F(1),
        {0: [({"a": 1, "b": 0}, F(1))],
         1: [({"a": 0, "b": 1}, F(1))]})
    cm, cj, _actual, _stats = common_cycle(2)
    opt, checked = brute_opt(cm, cj)
    report["common_cycle_full_assignment_exhaustion"] = {
        "m": 2, "opt": str(opt), "assignments": checked}
    assert opt == 1
    report["not_implemented"] = [
        "generic MC_c optimization", "large-instance exhaustive optimum",
        "NP-hard source reduction", "near-two hardness or a UM approximation algorithm"]
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
