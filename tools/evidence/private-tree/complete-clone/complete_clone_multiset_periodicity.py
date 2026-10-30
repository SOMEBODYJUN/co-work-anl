#!/usr/bin/env python3
"""Finite exact checks for complete machine/job cloning, not a polynomial solver.

Two independent oracles: labeled assignments and type-count dynamic programming.
All costs and comparisons use Fraction; None denotes an unavailable edge.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import random


def dimensions(p):
    assert p and all(len(row) == len(p[0]) for row in p)
    m, n = len(p), len(p[0])
    assert all(x is None or isinstance(x, F) and x >= 0 for row in p for x in row)
    assert all(any(p[i][j] is not None for i in range(m)) for j in range(n))
    return m, n


def labeled_oracle(p, q):
    """Explicit finite-edge assignment enumeration with exact load pruning."""
    m, n = dimensions(p)
    assert isinstance(q, int) and q > 0
    jobs = [(j, r) for j in range(n) for r in range(q)]
    jobs.sort(key=lambda jr: (sum(p[i][jr[0]] is not None for i in range(m)), jr))
    loads = [F(0)] * (m * q)
    upper = sum((min(p[i][j] for i in range(m) if p[i][j] is not None)
                 for j in range(n)), F(0))
    best = upper
    visited = 0

    def visit(k):
        nonlocal best, visited
        visited += 1
        if k == len(jobs):
            best = min(best, max(loads, default=F(0)))
            return
        j, _ = jobs[k]
        for i in range(m):
            if p[i][j] is None:
                continue
            # Equal-load clones of one machine type are exactly symmetric.
            seen = set()
            for s in range(q):
                ix = i * q + s
                if loads[ix] in seen:
                    continue
                seen.add(loads[ix])
                new = loads[ix] + p[i][j]
                if new >= best:
                    continue
                old = loads[ix]
                loads[ix] = new
                visit(k + 1)
                loads[ix] = old

    visit(0)
    return best, visited


def count_oracle(p, q):
    """Minimize a bottleneck over type counts; does not call labeled_oracle."""
    m, n = dimensions(p)
    assert q > 0
    counts = list(product(range(q + 1), repeat=n))
    target = (q,) * n
    dp = {(0,) * n: F(0)}
    for i in range(m):
        patterns = []
        for a in counts:
            if any(a[j] and p[i][j] is None for j in range(n)):
                continue
            load = sum((a[j] * p[i][j] for j in range(n) if a[j]), F(0))
            patterns.append((a, load))
        for _ in range(q):
            nxt = {}
            for done, old in dp.items():
                for a, load in patterns:
                    total = tuple(done[j] + a[j] for j in range(n))
                    if any(x > q for x in total):
                        continue
                    candidate = max(old, load)
                    if total not in nxt or candidate < nxt[total]:
                        nxt[total] = candidate
            dp = nxt
    return dp[target]


def parity_schedule(q):
    """Actual labeled allocation for the parity example, q >= 1."""
    p = [[F(2), F(1), None], [F(2), None, F(1)]]
    sigma = {}
    if q % 2:
        for r in range(q):
            sigma[0, r] = (0, r)
            sigma[1, r] = (0, r)
            sigma[2, r] = (1, r)
    else:
        h = q // 2
        for r in range(q):
            sigma[0, r] = (r // h, r % h)
            sigma[1, r] = (0, h + r // 2)
            sigma[2, r] = (1, h + r // 2)
    loads = {(i, s): F(0) for i in range(2) for s in range(q)}
    assert len(sigma) == 3 * q
    for (j, r), dest in sigma.items():
        assert 0 <= r < q and p[dest[0]][j] is not None
        loads[dest] += p[dest[0]][j]
    return max(loads.values()), {f"{i}:{s}": str(v) for (i, s), v in loads.items()}


def arbitrary_period_schedule(m, q):
    """All labeled jobs for the arbitrary-period seed; integer units are 1/m."""
    rem = q % m
    d = 0 if rem == 0 else (m - rem + q - 1) // q
    cap = q * (d + 1) // m
    big_per_row, left = [], q
    for _ in range(m):
        take = min(cap, left)
        big_per_row.append(take)
        left -= take
    assert left == 0 and all(b <= q for b in big_per_row)
    loads = [[0] * q for _ in range(m)]
    sigma = {}
    big_label = 0
    for i, b in enumerate(big_per_row):
        for s in range(b):
            sigma[0, big_label] = (i, s)
            big_label += 1
            loads[i][s] += m
        capacities = [d if s < b else m + d for s in range(q)]
        cursor = 0
        for kind in range(m - 1):
            j = 1 + i * (m - 1) + kind
            for r in range(q):
                while cursor < q and capacities[cursor] == 0:
                    cursor += 1
                assert cursor < q
                sigma[j, r] = (i, cursor)
                capacities[cursor] -= 1
                loads[i][cursor] += 1
    assert len(sigma) == q * (1 + m * (m - 1)) and big_label == q
    for (j, r), (i, s) in sigma.items():
        assert 0 <= r < q and 0 <= s < q
        assert j == 0 or (j - 1) // (m - 1) == i
    value = F(max(max(row) for row in loads), m)
    assert value == 1 + F(d, m)
    # Independent minimization of the exact row-capacity inequalities.
    ds = [t for t in range(m) if m * (q * (t + 1) // m) >= q]
    assert min(ds) == d
    assert (value == 1) == (q % m == 0)
    return value


def run():
    rng = random.Random(24019)
    cases = [
        [[F(0)]], [[F(0), None], [None, F(1)]], [[], []],
        [[F(1, 10**40 + 7), None], [F(2, 3), F(1, 7)]],
        [[F(2), F(1), None], [F(2), None, F(1)]],
        [[F(1)] * 3, [F(1)] * 3],
    ]
    alphabet = [F(0), F(1, 3), F(1), F(2), None]
    for _ in range(80):
        m, n = rng.choice([1, 2]), rng.randrange(4)
        p = [[rng.choice(alphabet) for _ in range(n)] for _ in range(m)]
        for j in range(n):
            if all(p[i][j] is None for i in range(m)):
                p[rng.randrange(m)][j] = F(1, 3)
        cases.append(p)
    checks, visited = 0, 0
    for p in cases:
        values = {}
        for q in (1, 2):
            a, nodes = labeled_oracle(p, q)
            b = count_oracle(p, q)
            assert a == b, (p, q, a, b)
            values[q] = a
            checks += 1
            visited += nodes
        assert values[2] <= values[1]  # divisibility monotonicity only
    parity = []
    p = [[F(2), F(1), None], [F(2), None, F(1)]]
    for q in range(1, 6):
        expected = F(2 if q % 2 == 0 else 3)
        a, nodes = labeled_oracle(p, q)
        assert a == count_oracle(p, q) == expected
        visited += nodes
        parity.append({"q": q, "opt": str(a)})
    actual = []
    for q in range(1, 25):
        value, loads = parity_schedule(q)
        assert value == (2 if q % 2 == 0 else 3)
        actual.append({"q": q, "makespan": str(value), "loads": loads})
    # Explicit multiset witness at T=2: each row half big, half two private.
    for i in range(2):
        big = [1, 0, 0]
        private = [0, 2 if i == 0 else 0, 2 if i == 1 else 0]
        assert sum((big[j] * p[i][j] for j in range(3) if big[j]), F(0)) == 2
        assert sum((private[j] * p[i][j] for j in range(3) if private[j]), F(0)) == 2
    coverage = [F(0)] * 3
    for a in [(1, 0, 0), (0, 2, 0), (1, 0, 0), (0, 0, 2)]:
        coverage = [coverage[j] + F(a[j], 2) for j in range(3)]
    assert coverage == [1, 1, 1]
    # Arithmetic in the proof: private capacities force 2*x=q at T<3.
    for q in range(1, 51):
        feasible = [x for x in range(q + 1) if 2 * (q - x) >= q and 2 * x >= q]
        assert feasible == ([q // 2] if q % 2 == 0 else [])
    family = []
    for m in range(1, 10):
        for q in range(1, 41):
            value = arbitrary_period_schedule(m, q)
            if q >= m - 1:
                assert value == (1 if q % m == 0 else 1 + F(1, m))
            family.append((m, q, str(value)))
    sylvester = []
    prod, denominators = 1, []
    for k in range(1, 6):
        denominators.append(prod + 1)
        prod *= denominators[-1]
        ds = denominators + [prod]
        assert sum((F(1, d) for d in ds), F(0)) == 1
        for q in range(1, 101):
            feasible = sum((q + d - 1) // d for d in ds) <= q
            assert feasible == (q % prod == 0)
        if k <= 3:
            q = prod
            loads = [[F(0)] * q for _ in ds]
            sigma, big = {}, 0
            for i, d in enumerate(ds):
                for r in range(q):
                    sigma[k + i, r] = (i, r // d)
                    loads[i][r // d] += F(1, d)
                for s in range(q // d, q):
                    sigma[big // q, big % q] = (i, s)
                    big += 1
                    loads[i][s] += 1
            assert big == k * q and len(sigma) == (2 * k + 1) * q
            assert all(x == 1 for row in loads for x in row)
        sylvester.append({"k": k, "denominators": ds, "first_optimal_q": prod})
    return {
        "claim": "UM-COMPLETE-CLONE-MULTISET-PERIODICITY-v1",
        "python": platform.python_version(), "arithmetic": "fractions.Fraction; exact integer counts",
        "seed": 24019, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "case_count": len(cases), "cross_oracle_checks": checks,
        "labeled_search_nodes": visited, "parity_two_oracle_values": parity,
        "actual_allocations": actual, "capacity_integer_checks": 50,
        "arbitrary_period_family": {"m_range": [1, 9], "q_range": [1, 40],
                                    "actual_assignment_and_capacity_checks": len(family),
                                    "cases_sha256": hashlib.sha256(json.dumps(family).encode()).hexdigest()},
        "exponential_first_attainment": {"families": sylvester,
                                         "capacity_checks": 500,
                                         "actual_labeled_constructions_k": [1, 2, 3]},
        "limits": ["Finite exact oracle comparisons do not prove the general theorem.",
                   "No generic multiset-LP solver, eventual-period computation, or polynomial-time scheduling backend is implemented.",
                   "The deterministic random sample is not exhaustive over all input matrices."]
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
