#!/usr/bin/env python3
"""Independent generic-matrix checks, including noncanonical actual assignments.

Written after the independent proof freeze. No author code is imported.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import hashlib
import json


def build(labels, edges, d):
    machines, jobs = set(), {}
    def add(j, opts):
        assert j not in jobs
        jobs[j] = dict(opts)
        assert len(jobs[j]) == len(opts)
        machines.update(jobs[j])
    for e, (u, v, pi) in enumerate(edges):
        add(("s", e), [(("R", e, a), F(1)) for a in labels[u]])
        for a in labels[u]:
            add(("xu", e, a), [(("R", e, a), F(1, 2)), (("H", e, u, a), F(1))])
            add(("xv", e, a), [(("R", e, a), F(1, 2)), (("H", e, v, pi[a]), F(1))])
        for w in (u, v):
            for b in labels[w]:
                add(("z", e, w, b), [(("H", e, w, b), F(3, 4)), (("A", w, b), F(1, d))])
    for v, domain in labels.items():
        for b in domain:
            add(("w", v, b), [(("A", v, b), F(1)), (("B", v, b), F(1))])
            for r in range(d):
                add(("f", v, b, r), [(("B", v, b), F(1, d)), (("C", v, r), F(1))])
    if not machines:
        machines.add(("idle",))
    return machines, jobs


def counts(labels, edges, chosen):
    t = {v: Counter() for v in labels}
    for e, ((u, v, pi), a) in enumerate(zip(edges, chosen)):
        t[u][a] += 1
        t[v][pi[a]] += 1
    return t


def second(t):
    return max((sorted(c.values(), reverse=True) + [0, 0])[1] for c in t.values()) if t else 0


def schedule(labels, edges, d, chosen, exact_second=False):
    t = counts(labels, edges, chosen)
    touched = set()
    out = {}
    for e, ((u, v, pi), a0) in enumerate(zip(edges, chosen)):
        out[("s", e)] = ("R", e, a0)
        for a in labels[u]:
            out[("xu", e, a)] = ("H", e, u, a) if a == a0 else ("R", e, a)
            out[("xv", e, a)] = ("H", e, v, pi[a]) if a == a0 else ("R", e, a)
        touched.update([(e, u, a0), (e, v, pi[a0])])
        for w in (u, v):
            for b in labels[w]:
                out[("z", e, w, b)] = ("A", w, b) if (e, w, b) in touched else ("H", e, w, b)
    for v, domain in labels.items():
        if exact_second:
            opened = max(domain, key=lambda b: t[v][b])
        else:
            opened_set = [b for b in domain if t[v][b] > d//2]
            assert len(opened_set) <= 1
            opened = opened_set[0] if opened_set else None
        for b in domain:
            active = b == opened
            out[("w", v, b)] = ("B" if active else "A", v, b)
            for r in range(d):
                exported = active and (exact_second or r < d-d//2)
                out[("f", v, b, r)] = ("C", v, r) if exported else ("B", v, b)
    return out


def verify(labels, edges, d, chosen):
    machines, jobs = build(labels, edges, d)
    peaks = []
    for exact in (False, True):
        out = schedule(labels, edges, d, chosen, exact)
        assert set(out) == set(jobs)
        loads = {m: F(0) for m in machines}
        for j, m in out.items():
            assert m in jobs[j]
            loads[m] += jobs[j][m]
        peak = max(loads.values())
        assert peak <= 1 + F(d//2, d)
        assert all(loads[m] <= 1 for m in machines if m[0] == "C")
        for e, ((u, v, pi), a0) in enumerate(zip(edges, chosen)):
            assert out[("s", e)] == ("R", e, a0)
            assert out[("xu", e, a0)] == ("H", e, u, a0)
            assert out[("xv", e, a0)] == ("H", e, v, pi[a0])
            for a in labels[u]:
                if a != a0:
                    assert out[("xu", e, a)] == out[("xv", e, a)] == ("R", e, a)
        if exact:
            assert peak == (1 + F(second(counts(labels, edges, chosen)), d) if labels else 0)
        peaks.append(str(peak))
    return peaks


def exact_opt_by_all_assignment_search(labels, edges, d):
    """Integer-scaled DFS over every actual job option, with sound peak pruning."""
    machines, jobs = build(labels, edges, d)
    if not jobs:
        return {"opt": "0", "visited_nodes": 1, "complete_better_assignments": 1}
    scale = lcm(4, d)
    mids = {m: i for i, m in enumerate(sorted(machines, key=str))}
    opts = [[(mids[m], int(p*scale)) for m, p in o.items()] for o in jobs.values()]
    # Large jobs first to expose physical capacity contradictions early.
    opts.sort(key=lambda o: (-min(p for _, p in o), len(o)))
    loads = [0]*len(mids)
    bound = int((1+F(d//2, d))*scale)
    best = bound
    visited = leaves = 0
    def search(i):
        nonlocal best, visited, leaves
        visited += 1
        if i == len(opts):
            leaves += 1
            best = min(best, max(loads))
            return
        for host, p in opts[i]:
            # Search only for strict improvement over the independently supplied upper.
            if loads[host]+p >= best:
                continue
            loads[host] += p
            search(i+1)
            loads[host] -= p
    search(0)
    return {"opt": str(F(best, scale)), "visited_nodes": visited,
            "complete_better_assignments": leaves}


if __name__ == "__main__":
    cases = [
        ("empty_full_vertex_set", {}, [], 2, True),
        ("left_isolated_right_side_empty", {"u": [0]}, [], 2, True),
        ("two_isolates", {"u": [0], "v": [0]}, [], 3, True),
        ("noninjective_single_edge", {"u": [0, 1], "v": [0]}, [("u", "v", {0: 0, 1: 0})], 2, True),
        ("D2_unsat_equal_boundary", {"u": [0], "v": [0, 1]},
         [("u", "v", {0: 0}), ("u", "v", {0: 1})], 2, True),
        ("D3_unsat_strict_small_threshold", {"u": [0], "v": [0, 1]},
         [("u", "v", {0: 0}), ("u", "v", {0: 1})], 3, True),
        ("noninjective_three_parallel", {"u": [0, 1], "v": [0, 1]},
         [("u", "v", {0: 0, 1: 0}), ("u", "v", {0: 1, 1: 1}),
          ("u", "v", {0: 0, 1: 0})], 3, False),
    ]
    records = []
    for name, labels, edges, d, enumerate_actual in cases:
        machines, jobs = build(labels, edges, d)
        chosen_family = list(product(*(labels[u] for u, v, pi in edges)))
        peaks = [verify(labels, edges, d, chosen) for chosen in chosen_family]
        mu = min(second(counts(labels, edges, chosen)) for chosen in chosen_family)
        predicted = 1+F(mu, d) if labels else F(0)
        record = {"case": name, "D": d, "machines": len(machines), "jobs": len(jobs),
                  "finite_entries": sum(len(o) for o in jobs.values()),
                  "all_edge_state_choices_checked": len(chosen_family),
                  "universal_and_second_count_schedule_peaks": peaks,
                  "predicted_exact_opt": str(predicted)}
        if enumerate_actual:
            record["all_actual_assignment_search"] = exact_opt_by_all_assignment_search(labels, edges, d)
            assert record["all_actual_assignment_search"]["opt"] == str(predicted)
        records.append(record)
    data = {"scope": "finite audit only; no author code imported",
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "cases": records}
    print(json.dumps(data, indent=2))
