#!/usr/bin/env python3
"""剪枝调度首步临时容量：实际步选择、锐环族和独立有限 oracle。

All arithmetic is exact. None denotes an unavailable edge. The one-step
routine does not find an optimal schedule or promise any eventual progress.
Run from the repository root; stdout only, never overwrite frozen evidence.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise ValueError("only exact int/Fraction input is accepted")
    value = F(value)
    if value < 0:
        raise ValueError("negative time or bound")
    return value


def checked(p, sigma):
    if not p:
        raise ValueError("at least one machine is required")
    n = len(sigma)
    if any(len(row) != n for row in p):
        raise ValueError("matrix/assignment dimensions differ")
    p = [[None if a is None else rational(a) for a in row] for row in p]
    if any(isinstance(i, bool) or not isinstance(i, int)
           or i < 0 or i >= len(p) or p[i][j] is None
           for j, i in enumerate(sigma)):
        raise ValueError("illegal assignment")
    if any(all(row[j] is None for row in p) for j in range(n)):
        raise ValueError("unavailable job")
    return p


def loads(p, sigma):
    return [sum((p[i][j] for j in range(len(sigma)) if sigma[j] == i), F(0))
            for i in range(len(p))]


def bound(t, c):
    t, c = rational(t), rational(c)
    if not t <= c <= 2*t:
        raise ValueError("require T <= C <= 2T")
    return max(2*t, c+t/2)


def first_step(p, sigma, t, c):
    """DONE, MOVE, or certified NO_T_SCHEDULE; never claims improvement.

    Preconditions: sigma is legal, every used edge is <=T, loads <= C,
    and T<=C<=2T. All original finite destination edges <=T are reopened.
    NO_T_SCHEDULE follows from the proved first-step lemma, not an LP.
    """
    p = checked(p, sigma)
    t, c = rational(t), rational(c)
    u = bound(t, c)
    old = loads(p, sigma)
    if max(old) > c or any(p[i][j] > t for j, i in enumerate(sigma)):
        raise ValueError("initial schedule is outside the pruned load contract")
    if max(old) <= t:
        return {"status": "DONE", "assignment": list(sigma), "loads": old}
    best = None
    for j, src in enumerate(sigma):
        for dst in range(len(p)):
            if dst == src or p[dst][j] is None or p[dst][j] > t:
                continue
            new = old.copy()
            new[src] -= p[src][j]
            new[dst] += p[dst][j]
            key = (max(new), j, dst)
            if best is None or key < best[0]:
                best = (key, new)
    if best is not None and best[0][0] <= u:
        (_, j, dst), new = best
        out = list(sigma)
        out[j] = dst
        return {"status": "MOVE", "job": j, "destination": dst,
                "assignment": out, "loads": new}
    return {"status": "NO_T_SCHEDULE"}


def sharp_cycle(k, t, c):
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    t, c = rational(t), rational(c)
    bound(t, c)
    if t == 0:
        raise ValueError("the nondegenerate sharp family requires T>0")
    m = k+1
    p, sigma, tau, order = [[] for _ in range(m)], [], [], []

    def add(src, dst, a, b):
        j = len(sigma)
        for i in range(m):
            p[i].append(a if i == src else b if i == dst else None)
        sigma.append(src)
        tau.append(dst)
        return j

    if 2*c <= 3*t:
        for i in range(m):
            add(i, i, c-t, c-t)
        for i in range(m):
            order.append(add(i, (i+1) % m, t, 2*t-c))
    else:
        rings = [[], []]
        for i in range(m):
            for r in range(2):
                rings[r].append(add(i, (i+1) % m, c/2, t/2))
        order = rings[0]+rings[1]
    return p, sigma, tau, order


def enumeration_oracle(p, sigma, tau, k):
    """Enumerate all actual assignments, and the entire bounded-batch graph.

    Independent of the displayed migration order and first_step chooser.
    Only used for small fixtures; its exponential cost is not the algorithm.
    """
    options = [tuple(i for i, row in enumerate(p) if row[j] is not None)
               for j in range(len(sigma))]
    states = list(product(*options))
    costs = []
    for state in states:
        accum = [F(0)]*len(p)
        for j, i in enumerate(state):
            accum[i] += p[i][j]
        costs.append(max(accum))
    start, goal = states.index(tuple(sigma)), states.index(tuple(tau))
    first = min(costs[i] for i, state in enumerate(states)
                if 1 <= sum(x != y for x, y in zip(state, sigma)) <= k)
    # Minimax Dijkstra permits reversals, repeated moves and arbitrary k-batches.
    distance = [None]*len(states)
    distance[start] = costs[start]
    remaining = set(range(len(states)))
    while remaining:
        possible = [i for i in remaining if distance[i] is not None]
        if not possible:
            break
        v = min(possible, key=lambda i: (distance[i], i))
        remaining.remove(v)
        if v == goal:
            break
        for w in remaining:
            if 1 <= sum(x != y for x, y in zip(states[v], states[w])) <= k:
                candidate = max(distance[v], costs[w])
                if distance[w] is None or candidate < distance[w]:
                    distance[w] = candidate
    return min(costs), first, distance[goal], len(states)


def audit():
    # Exhaust all endpoint jobs on the half-unit grid for two machines, and
    # all fixed loads on that grid. Every nonfixed job has distinct owners.
    endpoint_cases = 0
    for n in range(1, 5):
        for jobs in product(tuple(product(range(2), range(3), range(3))), repeat=n):
            source, target = [0, 0], [0, 0]
            for i, a, b in jobs:
                source[i] += a
                target[1-i] += b
            for fixed in product(range(3), repeat=2):
                old = [source[i]+fixed[i] for i in range(2)]
                end = [target[i]+fixed[i] for i in range(2)]
                if max(old) > 4 or max(end) > 2:
                    continue
                c = max(2, max(old))
                u = max(F(4), F(c)+1)
                values = []
                for i, a, b in jobs:
                    moved = old.copy()
                    moved[i] -= a
                    moved[1-i] += b
                    values.append(max(moved))
                assert min(values) <= u
                endpoint_cases += 1
    fixtures, state_count = [], 0
    for k in (1, 2, 3):
        for t in (F(1), F(2, 7)):
            for ratio in (F(1), F(5, 4), F(3, 2), F(7, 4), F(2)):
                c = ratio*t
                p, sigma, tau, order = sharp_cycle(k, t, c)
                u = bound(t, c)
                assert max(loads(p, sigma)) == c
                assert max(loads(p, tau)) == t
                assert all(x is None or 0 <= x <= t for row in p for x in row)
                state, peak = sigma.copy(), c
                for j in order:
                    state[j] = tau[j]
                    peak = max(peak, max(loads(p, state)))
                assert state == tau and peak == u
                opt, first, optimal_peak, count = enumeration_oracle(p, sigma, tau, k)
                assert opt == t and first == optimal_peak == u
                state_count += count
                out = first_step(p, sigma, t, c)
                assert out["status"] == ("DONE" if c == t else "MOVE")
                fixtures.append({"k": k, "T": str(t), "C": str(c),
                                 "U": str(u), "states": count})
    # Zero target/empty/one machine; huge denominators; reliable NO branch.
    assert first_step([[]], [], 0, 0)["status"] == "DONE"
    assert first_step([[0]], [0], 0, 0)["status"] == "DONE"
    assert first_step([[F(1), F(1)]], [0, 0], 1, 2)["status"] == "NO_T_SCHEDULE"
    denominator = 2**127+1
    p, sigma, _, _ = sharp_cycle(2, F(1, denominator), F(7, 4*denominator))
    assert first_step(p, sigma, F(1, denominator), F(7, 4*denominator))["status"] == "MOVE"
    invalid = [([], [], 1, 1), ([[1.0]], [0], 1, 1),
               ([[True]], [0], 1, 1), ([[None]], [0], 1, 1),
               ([[1]], [0], 0, 0), ([[1]], [0], 1, F(5, 2))]
    for args in invalid:
        try:
            first_step(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input accepted")
    return {"python": platform.python_version(), "arithmetic": "Fraction/integer",
            "seed": None, "two_machine_endpoint_cases": endpoint_cases,
            "endpoint_grid": "T=2; a,b,f in {0,1,2}; 1<=different-owner jobs<=4",
            "sharp_fixtures": fixtures, "enumerated_states": state_count,
            "boundary_cases": 4, "invalid_cases": len(invalid),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "limits": "Finite audits only. No general full-path U bound, target finder, or sub-2 approximation."}


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
