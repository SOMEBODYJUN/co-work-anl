#!/usr/bin/env python3
"""Tiny exact Fraction checks for the incidence cycle-rank asset.

The universal statement is proved by feedback-edge enumeration and leaf/cycle
reasoning in the corresponding Markdown asset; this script is finite only.
"""
from fractions import Fraction as F
from itertools import product


def brute(m, jobs, T):
    best = None
    best_s = None
    for s in product(range(m), repeat=len(jobs)):
        loads = [F(0) for _ in range(m)]
        ok = True
        for j, i in enumerate(s):
            p = jobs[j].get(i)
            if p is None:
                ok = False; break
            loads[i] += p
        if ok and max(loads, default=F(0)) <= T:
            return s, loads
    return None, None


def check_leaf_paths():
    # A machine-task path with a task of support three is still a forest.
    jobs = [
        {0: F(1), 1: F(2), 2: F(1)},
        {1: F(1), 3: F(3)},
        {2: F(1)},
    ]
    s, loads = brute(4, jobs, F(2))
    assert s is not None and max(loads) <= 2
    s2, _ = brute(4, jobs, F(1, 1))
    assert s2 is not None


def check_cycle_core():
    # A 4-cycle in the incidence graph; each task has support two.
    jobs = [{0: F(1), 1: F(2)}, {0: F(2), 1: F(1)}]
    s, loads = brute(2, jobs, F(1))
    assert s in [(0, 1), (1, 0)] and max(loads) <= 1
    s2, _ = brute(2, jobs, F(0))
    assert s2 is None


def check_zero_and_empty():
    assert brute(1, [], F(0)) == ((), [F(0)])
    jobs = [{0: F(0), 1: F(3)}, {1: F(0)}]
    s, loads = brute(2, jobs, F(0))
    assert s is not None and loads == [F(0), F(0)]


def check_fail_leaf():
    jobs = [{0: F(2)}, {0: F(2)}]
    s, _ = brute(2, jobs, F(2))
    assert s is None


def main():
    check_leaf_paths(); check_cycle_core(); check_zero_and_empty(); check_fail_leaf()
    print({"incidence_components_checked": 4, "status": "ok"})


if __name__ == "__main__":
    main()
