#!/usr/bin/env python3
"""逐行精确负载/全局基数探针；精确有限审计，不是通用调度算法。"""
from fractions import Fraction as F
from itertools import product
from collections import deque
from pathlib import Path
import hashlib
import json
import platform


def domains(p, target):
    if isinstance(target, bool) or not isinstance(target, (int, F)) or target < 0 or not p:
        raise ValueError("nonnegative exact target and at least one machine required")
    n = len(p[0])
    if any(len(row) != n for row in p):
        raise ValueError("ragged matrix")
    for row in p:
        for a in row:
            if a is not None and (isinstance(a, bool) or not isinstance(a, (int, F)) or a < 0):
                raise ValueError("nonnegative exact times or None required")
    if any(all(row[j] is None for row in p) for j in range(n)):
        raise ValueError("unavailable job")
    return [{i for i, row in enumerate(p) if row[j] is not None and row[j] <= target}
            for j in range(n)]


def row_caps(p, target, d):
    n = len(d)
    out = []
    for i in range(len(p)):
        times = [F(p[i][j]) for j in range(n) if i in d[j]]
        low = min(times) if times else None
        out.append(0 if low is None else n if low == 0 else min(n, int(target // low)))
    return out


def query(p, target, d, v, forced):
    """Minimum exact v-load with other machines constrained only by row caps.

    The returned assignment is a relaxed witness: its other true loads can exceed
    target.  A missing witness safely rules out the forced edge at target.
    """
    if v not in d[forced]:
        raise ValueError("forced edge outside current domain")
    n = len(d)
    caps = row_caps(p, target, d)
    slots = [(i, t) for i, cap in enumerate(caps) if i != v for t in range(cap)]
    neighbors = {j: [s for s, (i, _) in enumerate(slots) if i in d[j]]
                 for j in range(n) if j != forced}
    match_slot = {}
    match_job = {}

    def augment(start):
        todo = deque([start])
        seen = {start}
        previous = {}
        while todo:
            j = todo.popleft()
            for s in neighbors[j]:
                if s in previous:
                    continue
                previous[s] = j
                if s not in match_slot:
                    while True:
                        a = previous[s]
                        old = match_job.get(a)
                        match_slot[s] = a
                        match_job[a] = s
                        if old is None:
                            return True
                        s = old
                a = match_slot[s]
                if a not in seen:
                    seen.add(a)
                    todo.append(a)
        return False

    required = [j for j in range(n) if j != forced and v not in d[j]]
    for j in required:
        if not augment(j):
            return None
    optional = sorted((j for j in range(n) if j != forced and v in d[j]),
                      key=lambda j: (-F(p[v][j]), j))
    for j in optional:
        augment(j)
    sigma = [v] * n
    for j, s in match_job.items():
        sigma[j] = slots[s][0]
    load = sum((F(p[v][j]) for j in range(n) if sigma[j] == v), F(0))
    return load, sigma


def filter_domains(p, target):
    d = domains(p, target)
    if any(not a for a in d):
        return d, False
    while True:
        deleted = []
        for j, a in enumerate(d):
            for v in sorted(a):
                result = query(p, target, d, v, j)
                if result is None or result[0] > target:
                    deleted.append((j, v))
        if not deleted:
            return d, True
        for j, v in deleted:
            d[j].remove(v)
        if any(not a for a in d):
            return d, False


def relaxed_oracle(p, target, d, v, forced):
    """Independent full assignment enumeration, only used for tiny instances."""
    caps = row_caps(p, target, d)
    best = None
    for sigma in product(*(sorted(a) for a in d)):
        if sigma[forced] != v:
            continue
        if any(sum(a == i for a in sigma) > caps[i] for i in range(len(p)) if i != v):
            continue
        value = sum((F(p[v][j]) for j, a in enumerate(sigma) if a == v), F(0))
        if best is None or value < best:
            best = value
    return best


def audit():
    cases = queries = schedules = 0
    for m, n, alphabet in [(2, 3, (None, 0, F(1, 2), 1)),
                            (3, 2, (None, 0, F(1, 2), 1))]:
        for flat in product(alphabet, repeat=m*n):
            p = [list(flat[i*n:(i+1)*n]) for i in range(m)]
            if any(all(p[i][j] is None for i in range(m)) for j in range(n)):
                continue
            cases += 1
            d = domains(p, F(1))
            for j in range(n):
                for v in sorted(d[j]):
                    got = query(p, F(1), d, v, j)
                    want = relaxed_oracle(p, F(1), d, v, j)
                    assert (None if got is None else got[0]) == want
                    queries += 1
            final, accepted = filter_domains(p, F(1))
            for sigma in product(*(sorted(a) for a in d)):
                loads = [sum((F(p[i][j]) for j, a in enumerate(sigma) if a == i), F(0))
                         for i in range(m)]
                if max(loads) <= 1:
                    assert accepted and all(a in final[j] for j, a in enumerate(sigma))
                    schedules += 1
    fixtures = [([[]], F(0)), ([[0, 0], [0, 0]], F(0)),
                ([[F(1, 10**50 + 151)], [None]], F(1, 10**50 + 151)),
                ([[2]], F(1)), ([[0, None], [None, 1]], F(1))]
    for p, target in fixtures:
        d, accepted = filter_domains(p, target)
        assert accepted == all(a for a in domains(p, target))
    invalid = [([], 1), ([[0], []], 1), ([[None]], 1), ([[True]], 1),
               ([[0.5]], 1), ([[-1]], 1), ([[0]], -1), ([[0]], True)]
    for args in invalid:
        try:
            filter_domains(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input accepted")
    return {"title": "逐行精确负载与全局基数探针的有限审计",
            "arithmetic": "Fraction/integer; no tolerance", "python": platform.python_version(),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "legal_matrices": cases, "full_assignment_oracle_queries": queries,
            "target_feasible_assignments_preserved": schedules,
            "edge_cases": len(fixtures), "invalid_cases": len(invalid),
            "scope": "all stated 2x3/3x2 matrices at T=1; not a universal proof or scheduling solver"}


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
