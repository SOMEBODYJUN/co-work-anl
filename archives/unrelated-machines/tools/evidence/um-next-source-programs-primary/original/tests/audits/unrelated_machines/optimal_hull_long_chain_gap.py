#!/usr/bin/env python3
"""真实最优凸包槽初始化的长链修复证书；精确算术，重跑输出到 stdout。"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform


def instance(k: int, d: int):
    if type(k) is not int or type(d) is not int or k < 3 or d < 1:
        raise ValueError("integer k>=3,d>=1 required")
    a, delta = 1 - F(1, 2*k), F(1, k)
    long = d + 2*k - 1
    names = ["root"]
    chains = []
    for c in range(k+1):
        length = long if c == 0 else d
        row = list(range(len(names), len(names)+length+1))
        names.extend([f"chain{c}.home{r}" for r in range(length)] + [f"chain{c}.sink"])
        chains.append(row)
    jobs = []
    # Each entry gives (home, alternate, home time, alternate time).
    for c in range(k+1):
        jobs.append((0, chains[c][0], F(1) if c == 0 else delta, F(1)))
    local = []
    for c, row in enumerate(chains):
        block = []
        for h, nxt in zip(row, row[1:]):
            block.append(len(jobs))
            jobs.append((h, nxt, a, F(1)))
        local.append(block)
    m, n = len(names), len(jobs)
    p = [[None]*n for _ in range(m)]
    home = []
    for j, (h, nxt, s, t) in enumerate(jobs):
        p[h][j], p[nxt][j] = s, t
        home.append(h)
    s0, s1 = home[:], home[:]
    for c in range(1, k+1):
        s0[c] = chains[c][0]
        for j in local[c]:
            s0[j] = jobs[j][1]
    s1[0] = chains[0][0]
    for j in local[0]:
        s1[j] = jobs[j][1]
    x = [[delta*(s0[j] == i)+(1-delta)*(s1[j] == i)
          for j in range(n)] for i in range(m)]
    bad = home[:]
    bad[1] = chains[1][0]
    for j in local[1]:
        bad[j] = jobs[j][1]
    repair = bad[:]
    repair[2] = chains[2][0]
    for j in local[2]:
        repair[j] = jobs[j][1]
    return dict(k=k, d=d, a=a, delta=delta, long=long, p=p, x=x,
                jobs=jobs, chains=chains, local=local, names=names,
                home=home, s0=s0, s1=s1, bad=bad, repair=repair)


def loads(p, assignment):
    result = [F(0)]*len(p)
    for j, i in enumerate(assignment):
        if p[i][j] is None:
            raise AssertionError("ineligible assignment")
        result[i] += p[i][j]
    return result


def slots(p, x):
    edges = [[] for _ in x[0]]
    slot_ids = {}
    for i, row in enumerate(p):
        prefix = F(0)
        for j in sorted((j for j in range(len(row)) if x[i][j]),
                        key=lambda j: (-row[j], j)):
            end = prefix + x[i][j]
            q = prefix.numerator // prefix.denominator
            while F(q) < end:
                if min(end, q+1) > max(prefix, q):
                    slot_ids.setdefault((i, q), len(slot_ids))
                    edges[j].append((i, q))
                q += 1
            prefix = end
    return edges, slot_ids


def slot_injection(p, x, assignment):
    edges, _ = slots(p, x)
    occupied = {}
    selected = {}
    # Exact augmenting paths; this does not use the explicit injection formula.
    for start in range(len(assignment)):
        queue, seen_j, seen_s, parent = [start], {start}, set(), {}
        free = None
        for j in queue:
            for s in edges[j]:
                if s[0] != assignment[j] or s in seen_s:
                    continue
                seen_s.add(s)
                parent[s] = j
                if s not in occupied:
                    free = s
                    break
                nxt = occupied[s]
                if nxt not in seen_j:
                    queue.append(nxt)
                    seen_j.add(nxt)
            if free is not None:
                break
        if free is None:
            return None
        while True:
            j = parent[free]
            old = selected.get(j)
            selected[j] = free
            occupied[free] = j
            if old is None:
                break
            del occupied[old]
            free = old
    return [selected[j] for j in range(len(assignment))]


def minimum_slot_cost(p, x):
    """Exact residual shortest augmenting paths, independent of family formula."""
    edges, slot_ids = slots(p, x)
    n, ns = len(edges), len(slot_ids)
    source, sink = n+ns, n+ns+1
    graph = [[] for _ in range(sink+1)]

    def add(u, v, cost):
        graph[u].append([v, len(graph[v]), 1, cost])
        graph[v].append([u, len(graph[u])-1, 0, -cost])

    refs = []
    for j in range(n):
        add(source, j, F(0))
        for s in edges[j]:
            idx = len(graph[j])
            add(j, n+slot_ids[s], p[s[0]][j])
            refs.append((j, idx, s[0]))
    for z in range(ns):
        add(n+z, sink, F(0))
    total = F(0)
    for _ in range(n):
        dist = [None]*len(graph)
        parent = [None]*len(graph)
        dist[source] = F(0)
        for _ in range(len(graph)-1):
            changed = False
            for u, row in enumerate(graph):
                if dist[u] is None:
                    continue
                for t, (v, rev, cap, cost) in enumerate(row):
                    if cap and (dist[v] is None or dist[v] > dist[u]+cost):
                        dist[v], parent[v] = dist[u]+cost, (u, t)
                        changed = True
            if not changed:
                break
        if dist[sink] is None:
            raise AssertionError("no cover matching")
        total += dist[sink]
        v = sink
        while v != source:
            u, t = parent[v]
            edge = graph[u][t]
            edge[2] -= 1
            graph[v][edge[1]][2] += 1
            v = u
    assignment = [-1]*n
    for j, idx, i in refs:
        if graph[j][idx][2] == 0:
            assert assignment[j] == -1
            assignment[j] = i
    assert -1 not in assignment
    assert total == sum(loads(p, assignment))
    return total, assignment


def verify(k, d, optimize=True):
    z = instance(k, d)
    p, x = z['p'], z['x']
    m, n = len(p), len(p[0])
    assert m == k*d+k+z['long']+2 and n == m-1
    assert all(sum(x[i][j] for i in range(m)) == 1 for j in range(n))
    assert all(max(loads(p, z[s])) == 1 for s in ('s0', 's1'))
    assert all(sum(p[i][j]*x[i][j] for j in range(n) if p[i][j] is not None) <= 1
               for i in range(m))
    assert slot_injection(p, x, z['bad']) is not None
    assert max(loads(p, z['bad'])) == 2-F(1,k)
    badload, newload = loads(p, z['bad']), loads(p, z['repair'])
    assert max(newload) == max(F(1), 2-F(2,k)) < max(badload)
    changed = [j for j in range(n) if z['bad'][j] != z['repair'][j]]
    touched = {v for j in changed for v in (z['bad'][j], z['repair'][j])}
    assert len(changed) == d+1 and len(touched) == d+2
    assert max(sum(z['bad'][j] == i for j in changed) for i in range(m)) == 1
    ct = 1-z['delta']+d*(1-z['a'])
    cb = z['long']*(1-z['a'])
    assert cb-ct == F(1,2*k)
    expected = sum(loads(p, z['home']))+ct
    assert sum(badload) == expected
    if optimize:
        cost, assignment = minimum_slot_cost(p, x)
        assert cost == expected and assignment == z['bad']
    # A weak-makespan-monotone single-task implementation, not a lex descent.
    state = z['bad'][:]
    previous = max(badload)
    for j in reversed(z['local'][2]):
        state[j] = z['jobs'][j][1]
        current = max(loads(p, state))
        assert current <= previous
        previous = current
    state[2] = z['chains'][2][0]
    assert state == z['repair']
    return dict(k=k,d=d,machines=m,jobs=n,bad=str(max(badload)),
                repaired=str(max(newload)),changed_jobs=len(changed),
                participating_machines=len(touched),minimum_slot_cost=str(expected),
                cost_margin=str(cb-ct),mincost_optimized=optimize)


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def audit():
    cases = [verify(k,d) for k in range(3,9) for d in range(1,5)]
    boundaries = [verify(3,20,False), verify(16,1,False), verify(32,2,False)]
    rejected = 0
    for args in [(2,1),(3,0),(True,1),(3,False),(3.0,1)]:
        try:
            instance(*args)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid parameters accepted")
    return dict(title="真实最优凸包槽初始化的长链修复精确审计",
                claim="UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1",
                python=platform.python_version(),arithmetic="fractions.Fraction; exact",
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                cases=cases,boundaries=boundaries,invalid_rejections=rejected,
                limitations=["Finite implementation checks, not the universal proof.",
                             "Exact mincost flow checks cost and one optimizer; all-minimizer identity is proved in the account.",
                             "No general scheduling approximation algorithm or complexity lower bound."])


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2, default=encode))
