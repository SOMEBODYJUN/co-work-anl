#!/usr/bin/env python3
"""Exact count-state audit; no repository imports and no floating arithmetic.

Machines are identical. A macro has Q unit ticks and a tiny has one tick.
Every count-state is a complete labeled-machine scheduling orbit.
"""
from __future__ import annotations

import json
from itertools import product


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def loads(Q, macros, tinies):
    return tuple(Q * u + t for u, t in zip(macros, tinies))


def majorized(new, old):
    a, b = sorted(new, reverse=True), sorted(old, reverse=True)
    return sum(a) == sum(b) and all(
        sum(a[:r]) <= sum(b[:r]) for r in range(1, len(a))
    )


def repair(Q, initial_u, initial_t):
    u, t = list(initial_u), list(initial_t)
    m, k, N = len(u), sum(u), sum(t)
    M = max(((k + m - 1) // m) * Q, (k * Q + N + m - 1) // m)
    history = []
    while max(u) - min(u) >= 2:
        s = min(i for i in range(m) if u[i] == max(u))
        v = min(i for i in range(m) if u[i] == min(u))
        old_loads = loads(Q, u, t)
        old_psi = sum(z * z for z in u)
        D = old_loads[s] - old_loads[v]
        r = max(0, Q - D)
        assert 0 <= r <= t[v]
        u[s] -= 1
        u[v] += 1
        t[v] -= r
        t[s] += r
        new_loads = loads(Q, u, t)
        assert majorized(new_loads, old_loads)
        assert sum(z * z for z in u) < old_psi
        assert (D >= Q) or sorted(new_loads) == sorted(old_loads)
        history.append(("macro", r + 1, old_loads, new_loads))
    while max(loads(Q, u, t)) > M:
        old_loads = loads(Q, u, t)
        s = min(i for i in range(m) if old_loads[i] == max(old_loads))
        v = min(i for i in range(m) if old_loads[i] == min(old_loads))
        assert t[s] > 0
        assert old_loads[s] >= M + 1 and old_loads[v] <= M - 1
        t[s] -= 1
        t[v] += 1
        new_loads = loads(Q, u, t)
        assert majorized(new_loads, old_loads)
        assert sorted(new_loads) != sorted(old_loads)
        history.append(("tiny", 1, old_loads, new_loads))
    macro_steps = sum(h[0] == "macro" for h in history)
    tiny_steps = sum(h[0] == "tiny" for h in history)
    assert 2 * macro_steps <= sum(z * z for z in initial_u)
    assert tiny_steps <= N
    assert max(loads(Q, u, t)) == M
    return M, history


def audit_all_count_states():
    parameters = states = macro_steps = tiny_steps = 0
    max_support = 0
    for m, Q, k, N in product((2, 3), range(1, 6), range(6), range(9)):
        us, ts = list(compositions(k, m)), list(compositions(N, m))
        # Independent exhaustive optimum over all count-states, not M's formula.
        brute_opt = min(max(loads(Q, u, t)) for u in us for t in ts)
        parameters += 1
        for u in us:
            for t in ts:
                M, path = repair(Q, u, t)
                assert M == brute_opt
                states += 1
                macro_steps += sum(h[0] == "macro" for h in path)
                tiny_steps += sum(h[0] == "tiny" for h in path)
                max_support = max(max_support, *(h[1] for h in path), 0)
    return dict(parameters=parameters, all_count_states=states,
                macro_steps_checked=macro_steps, tiny_steps_checked=tiny_steps,
                largest_atomic_support=max_support)


def audit_repaired_barrier_families():
    repaired, original = [], []
    for m in range(2, 31):
        Q = m * m
        for r in range(1, m):
            u = (2,) + (0,) * (m - 1)
            t = (0,) + (Q + r,) * (m - 1)
            M, path = repair(Q, u, t)
            assert M == Q + m + r
            assert path[0][0:2] == ("macro", r + 1)
            assert sorted(path[0][2]) == sorted(path[0][3])
            assert sum(h[0] == "macro" for h in path) == 1
            assert sum(h[0] == "tiny" for h in path) == Q - m - r
            repaired.append((m, r, M, len(path)))
    for m in range(3, 101):
        Q, r = m, 1
        M, path = repair(Q, (2,) + (0,) * (m - 1),
                         (0,) + (Q + r,) * (m - 1))
        assert M == m + 2
        assert path[0][0:2] == ("macro", 2)
        assert sum(h[0] == "tiny" for h in path) == m - 2
        original.append((m, M, len(path)))
    return dict(repaired_Q_equals_m_squared_instances=len(repaired),
                original_Q_equals_m_instances=len(original),
                repaired_last=repaired[-1], original_last=original[-1])


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "exact_integer_ticks": True,
                      "exhaustive": audit_all_count_states(),
                      "families": audit_repaired_barrier_families()},
                     indent=2))
