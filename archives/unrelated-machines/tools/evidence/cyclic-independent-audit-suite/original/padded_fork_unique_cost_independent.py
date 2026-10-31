#!/usr/bin/env python3
"""Exact padded fork with unique minimum-cost LST output; no repo imports."""
from fractions import Fraction as F
from math import ceil
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


def case(theta):
    T, C, a = F(1), 2 - theta, 1 - theta / 2
    N = ceil(8 / theta)
    m, n = N + 3, N + 6
    # A=0,B=1,E=2, H_s=s+3. First six jobs are original fork.
    P = [{0: a, 1: theta / 4}, {0: a, 2: theta / 2},
         {1: a, 0: F(1)}, {2: a, 1: theta / 4},
         {1: a}, {2: a}]
    for j in range(4):
        for i in range(3, m):
            P[j][i] = F(1)
    P.extend({i: a} for i in range(3, m))
    initial = (0, 0, 1, 2, 1, 2) + tuple(range(3, m))
    optimum = (1, 2, 0, 1, 1, 2) + tuple(range(3, m))
    t = (a + 1) / (4 * a)
    beta = theta / (4 * a)
    x = [{} for _ in range(n)]
    for j in (0, 1):
        x[j][0] = t
        for i in range(3, m):
            x[j][i] = (1 - t) / N
    for j, i in ((2, 1), (3, 2)):
        x[j][i] = beta
        for h in range(3, m):
            x[j][h] = (1 - beta) / N
    for j in range(4, n):
        x[j][initial[j]] = F(1)
    assert all(sum(row.values(), F(0)) == 1 for row in x)
    assert all(initial[j] in x[j] and x[j][initial[j]] > 0 for j in range(n))
    assert all(0 < z <= 1 and 0 < P[j][i] <= 1 for j, row in enumerate(x)
               for i, z in row.items())
    frac_load = [sum((P[j][i] * x[j].get(i, 0) for j in range(n)
                      if i in P[j]), F(0)) for i in range(m)]
    assert all(z <= T for z in frac_load)
    F_out = 4 - 2 * t - 2 * beta
    assert frac_load[0] == (a + 1) / 2
    assert frac_load[0] == frac_load[1] == frac_load[2] == 1 - theta / 4
    assert all(z == a + F_out / N for z in frac_load[3:])
    def loads(s):
        return [sum((P[j][i] for j in range(n) if s[j] == i), F(0))
                for i in range(m)]
    assert loads(initial) == [C] * 3 + [a] * N
    assert max(loads(optimum)) == 1
    # Makespan<1 cannot keep b together with its fixed resident job at B;
    # every other b destination requires time1. Thus OPT>=1.
    assert P[2][1] + P[4][1] == C > 1
    assert all(p == 1 for i, p in P[2].items() if i != 1)
    assert sum(loads(initial)) <= m
    assert sum(loads(initial)) <= sum(frac_load)
    assert 1 + a > C
    # Any changed core job at a pad exceeds C, independent of other core moves.
    # Thus <=C schedules reduce exactly to the original 16-way enumeration.
    core_schedules = list(product((0, 1), (0, 2), (1, 0), (2, 1)))
    monotone = []
    for s4 in core_schedules:
        s = s4 + initial[4:]
        if s != initial and max(loads(s)) <= C:
            monotone.append(s)
    assert monotone == [optimum]
    # Build the genuine ordered unit-slot support graph using the explicit x.
    graph = [set() for _ in range(n)]
    for i in range(m):
        jobs = [j for j in range(n) if x[j].get(i, 0) > 0]
        jobs.sort(key=lambda j: (-P[j][i], j))
        pos = F(0)
        for j in jobs:
            end = pos + x[j][i]
            while pos < end:
                slot = pos.numerator // pos.denominator
                nxt = min(end, F(slot + 1))
                assert nxt > pos
                graph[j].add((i, slot))
                pos = nxt
    # An explicit injection; no matching or cost optimizer is called.
    job_to_slot = [(0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (2, 1)]
    job_to_slot.extend((i, 1) for i in range(3, m))
    assert len(job_to_slot) == n
    assert len(set(job_to_slot)) == n
    assert all(slot in graph[j] and slot[0] == initial[j]
               for j, slot in enumerate(job_to_slot))
    # Per-job support cost lower bound: current allocation is a minimum-cost
    # matching, not merely a matching with cost <= the fractional objective.
    assert all(P[j][initial[j]] == min(P[j][i] for i in x[j]) for j in range(n))
    assert all(all(P[j][initial[j]] < P[j][i] for i in x[j]
                   if i != initial[j]) for j in range(4))
    result = {"theta": str(theta), "pads": N, "machines": m, "jobs": n,
            "OPT": "1", "initial_makespan": str(C),
            "initial_total_work": str(sum(loads(initial))),
            "fractional_total_work": str(sum(frac_load)),
            "max_fractional_load": str(max(frac_load)),
            "padding_arrival_excess_above_C": str(1 + a - C),
            "slot_matching_covers_all_jobs": True,
            "initial_is_min_cost_support_slot_matching": True,
            "initial_is_unique_min_cost_support_slot_assignment": True,
            "one_destination_makespan_nonincreasing_repairs": 0,
            "explicit_job_to_slot_injection": [[j, i, s] for j, (i, s)
                                               in enumerate(job_to_slot)]}
    if theta == F(1, 2):
        result["concrete_instance"] = {
            "T": "1", "C": str(C), "a": str(a), "t": str(t),
            "beta": str(beta), "F_out": str(F_out),
            "machine_labels": ["A", "B", "E"] + ["H_" + str(i) for i in range(N)],
            "job_labels": ["X", "Y", "b", "c", "f_B", "f_E"] +
                          ["h_" + str(i) for i in range(N)],
            "finite_processing_matrix": [{str(i): str(p) for i, p in row.items()}
                                         for row in P],
            "unlisted_processing_entries": "infinity",
            "fractional_assignment": [{str(i): str(z) for i, z in row.items()}
                                      for row in x],
            "unlisted_fractional_entries": "0",
            "initial_assignment": list(initial),
            "optimum_assignment": list(optimum),
            "initial_loads": [str(z) for z in loads(initial)],
            "optimum_loads": [str(z) for z in loads(optimum)],
            "fractional_loads": [str(z) for z in frac_load],
            "slot_indexing": "zero-based; each [job,machine,slot] injection is above"}
    return result


def main():
    rows = [case(F(1, k)) for k in range(2, 65)]
    print(json.dumps({"status": "passed", "python": sys.version.split()[0],
                      "arithmetic": "fractions.Fraction", "k_range": [2, 64],
                      "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "cases": rows,
                      "limitations": ["Finite audit is not the general proof.",
                                      "The explicitly supplied fractional point is not asserted basic.",
                                      "The output need not be selected by every LST implementation.",
                                      "No algorithmic approximation hardness is asserted."]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
