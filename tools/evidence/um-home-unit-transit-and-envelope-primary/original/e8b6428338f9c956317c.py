#!/usr/bin/env python3
"""Exact home/unit normalizations, directed token bridge, and finite audits.

Only Python's standard library is used.  All processing times use Fraction.
The assignment and rooted-tree oracles enumerate their own search spaces;
neither calls the normalization or token decoder to determine its optimum.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


@dataclass(frozen=True)
class HomeUnit:
    m: int
    home: tuple[int, ...]
    a: tuple[F, ...]
    alternatives: tuple[tuple[int, ...], ...]
    unit_eligible: tuple[tuple[int, ...], ...] = ()

    def __post_init__(self):
        if self.m < 1 or len(self.home) != len(self.a) or len(self.home) != len(self.alternatives):
            raise ValueError("invalid dimensions")
        for h, a, alternatives in zip(self.home, self.a, self.alternatives):
            if not isinstance(a, (int, F)) or not 0 <= a <= 1 or not 0 <= h < self.m:
                raise ValueError("invalid exact home time or home")
            if len(set(alternatives)) != len(alternatives) or h in alternatives:
                raise ValueError("duplicate or home alternative")
            if any(not 0 <= i < self.m for i in alternatives):
                raise ValueError("invalid alternative")
        for eligible in self.unit_eligible:
            if not eligible or len(set(eligible)) != len(eligible) or any(not 0 <= i < self.m for i in eligible):
                raise ValueError("invalid unit eligibility")

    @property
    def nj(self):
        return len(self.home)

    @property
    def n(self):
        return self.nj + len(self.unit_eligible)

    def choices(self, j):
        if j < self.nj:
            return (self.home[j],) + self.alternatives[j]
        return self.unit_eligible[j - self.nj]

    def time(self, j, i):
        if i not in self.choices(j):
            raise ValueError("unavailable assignment")
        return F(self.a[j]) if j < self.nj and i == self.home[j] else F(1)

    def loads(self, sigma):
        if len(sigma) != self.n:
            raise ValueError("incomplete assignment")
        load = [F(0) for _ in range(self.m)]
        for j, i in enumerate(sigma):
            load[i] += self.time(j, i)
        return tuple(load)

    def baseline(self):
        b = [F(0) for _ in range(self.m)]
        for h, a in zip(self.home, self.a):
            b[h] += a
        return tuple(b)


def _adjacency(p, sigma):
    adjacency = [[] for _ in range(p.m)]
    for j, h in enumerate(p.home):
        if sigma[j] != h:
            adjacency[h].append((sigma[j], j))
    return adjacency


def _simple_cycle(p, sigma):
    """Deterministic iterative DFS; return original job labels on one cycle."""
    adjacency = _adjacency(p, sigma)
    color = [0] * p.m
    parent_job = [-1] * p.m
    parent_vertex = [-1] * p.m
    for start in range(p.m):
        if color[start]:
            continue
        color[start] = 1
        stack = [(start, 0)]
        while stack:
            v, index = stack[-1]
            if index == len(adjacency[v]):
                color[v] = 2
                stack.pop()
                continue
            stack[-1] = (v, index + 1)
            w, job = adjacency[v][index]
            if color[w] == 0:
                color[w] = 1
                parent_job[w], parent_vertex[w] = job, v
                stack.append((w, 0))
            elif color[w] == 1:
                cycle = [job]
                x = v
                while x != w:
                    cycle.append(parent_job[x])
                    x = parent_vertex[x]
                return tuple(cycle)
    return ()


def cancel_cycles(p: HomeUnit, sigma):
    """Return final complete schedule and a replayable list of cycle batches."""
    p.loads(sigma)
    tau = list(sigma)
    trace = []
    while True:
        cycle = _simple_cycle(p, tau)
        if not cycle:
            return tuple(tau), tuple(trace)
        for j in cycle:
            tau[j] = p.home[j]
        trace.append(cycle)


def normalize_unit_roots(p: HomeUnit, sigma):
    """Require actual makespan <2; no baseline budget is required to run."""
    if max(p.loads(sigma)) >= 2:
        raise ValueError("actual makespan must be strictly below 2")
    adjacency = _adjacency(p, sigma)
    roots = tuple(sigma[p.nj:])
    reachable = set(roots)
    stack = list(roots)
    while stack:
        v = stack.pop()
        for w, _ in adjacency[v]:
            if w not in reachable:
                reachable.add(w)
                stack.append(w)
    tau = tuple(sigma[j] if h in reachable else h for j, h in enumerate(p.home)) + tuple(roots)
    return tau, frozenset(reachable), roots


@dataclass(frozen=True)
class Token:
    instance: HomeUnit
    edges: tuple[tuple[int, int], ...]
    demand: tuple[int, ...]
    root: int
    child_jobs: tuple[tuple[int, ...], ...]


def build_token(n, edges, demand, root):
    edges = tuple(sorted(edges))
    demand = tuple(demand)
    if n < 1 or len(demand) != n or not 0 <= root < n or any(k < 0 or not isinstance(k, int) for k in demand):
        raise ValueError("invalid directed token input")
    if len(set(edges)) != len(edges) or any(not (0 <= v < n and 0 <= w < n) or v == w for v, w in edges):
        raise ValueError("graph must be simple and loopless")
    children = [tuple(w for v, w in edges if v == i) for i in range(n)]
    if any(demand[v] == 0 and children[v] for v in range(n)):
        raise ValueError("zero-demand vertex must be a sink")
    home, a, alternatives = [], [], []
    child_jobs = []
    for v, k in enumerate(demand):
        ids = []
        if k:
            q = min(k, len(children[v]))
            for _ in range(q):
                ids.append(len(home))
                home.append(v)
                a.append(F(1, k))
                alternatives.append(children[v])
            if q < k:
                home.append(v)
                a.append(F(k - q, k))
                alternatives.append(())
        child_jobs.append(tuple(ids))
    instance = HomeUnit(n, tuple(home), tuple(a), tuple(alternatives), ((root,),))
    return Token(instance, edges, demand, root, tuple(child_jobs))


def _tree_data(n, edges, root):
    """Validate a claimed root tree, including the singleton root."""
    indegree = [0] * n
    children = [[] for _ in range(n)]
    vertices = {root}
    for v, w in edges:
        children[v].append(w)
        indegree[w] += 1
        vertices.update((v, w))
    if indegree[root] or any(indegree[v] != 1 for v in vertices if v != root):
        raise ValueError("not a rooted tree")
    seen, stack = {root}, [root]
    while stack:
        v = stack.pop()
        for w in children[v]:
            if w in seen:
                raise ValueError("cycle or duplicate tree edge")
            seen.add(w)
            stack.append(w)
    if seen != vertices:
        raise ValueError("tree is not root-reachable")
    return seen, children


def tree_score(token, tree):
    tree = tuple(tree)
    if not set(tree) <= set(token.edges):
        raise ValueError("edge outside original graph")
    vertices, children = _tree_data(token.instance.m, tree, token.root)
    return min([F(1)] + [F(len(children[v]), token.demand[v]) for v in vertices if token.demand[v]])


def decode_token(token, sigma):
    p = token.instance
    if max(p.loads(sigma)) >= 2:
        raise ValueError("decoder requires actual makespan <2")
    _, reachable, _ = normalize_unit_roots(p, sigma)
    tree = tuple((p.home[j], sigma[j]) for j in range(p.nj) if p.home[j] in reachable and sigma[j] != p.home[j])
    tree_score(token, tree)
    return tree


def schedule_tree(token, tree):
    """Prune excessive tree children, then assign every original token job."""
    tree_score(token, tree)
    p = token.instance
    _, children = _tree_data(p.m, tree, token.root)
    tau = list(p.home) + [token.root]
    stack = [token.root]
    while stack:
        v = stack.pop()
        kept = sorted(children[v])[:token.demand[v]]
        for job, w in zip(token.child_jobs[v], kept):
            tau[job] = w
        stack.extend(kept)
    return tuple(tau)


def _audit_acyclic(p, sigma):
    """Independent topological deletion, not the construction's DFS."""
    degree = [0] * p.m
    outgoing = [[] for _ in range(p.m)]
    for j, h in enumerate(p.home):
        if sigma[j] != h:
            degree[sigma[j]] += 1
            outgoing[h].append(sigma[j])
    queue = [i for i in range(p.m) if degree[i] == 0]
    count = 0
    while queue:
        v = queue.pop()
        count += 1
        for w in outgoing[v]:
            degree[w] -= 1
            if degree[w] == 0:
                queue.append(w)
    return count == p.m


def _check_normalizations(p, sigma, counts):
    before = p.loads(sigma)
    tau, trace = cancel_cycles(p, sigma)
    after = p.loads(tau)
    assert tau[p.nj:] == tuple(sigma[p.nj:])
    assert all(tau[j] in (sigma[j], p.home[j]) for j in range(p.nj))
    assert all(x <= y for x, y in zip(after, before))
    assert _audit_acyclic(p, tau)
    replay = list(sigma)
    for cycle in trace:
        old = p.loads(replay)
        sources = [p.home[j] for j in cycle]
        targets = [replay[j] for j in cycle]
        assert len(set(sources)) == len(cycle) and set(sources) == set(targets)
        for j in cycle:
            replay[j] = p.home[j]
        new = p.loads(replay)
        change = {p.home[j]: p.a[j] - 1 for j in cycle}
        assert all(new[i] - old[i] == change.get(i, 0) for i in range(p.m))
    assert tuple(replay) == tau
    counts["normalization_schedules"] += 1
    counts["schedules_with_cycles"] += bool(trace)
    if max(before) < 2:
        normalized, reachable, roots = normalize_unit_roots(p, sigma)
        load = p.loads(normalized)
        b = p.baseline()
        assert normalized[p.nj:] == tuple(sigma[p.nj:])
        assert len(roots) == len(set(roots))
        assert all(load[i] == (before[i] if i in reachable else b[i]) for i in range(p.m))
        assert _audit_acyclic(p, normalized)
        in_edges = [0] * p.m
        out_edges = [[] for _ in range(p.m)]
        for j, h in enumerate(p.home):
            if normalized[j] != h:
                assert h in reachable and normalized[j] in reachable
                in_edges[normalized[j]] += 1
                out_edges[h].append(normalized[j])
        assert all(in_edges[i] == (0 if i in roots or i not in reachable else 1) for i in range(p.m))
        # Each component is checked from its own U identity, not only by counts.
        claimed = set()
        for root in roots:
            seen, stack = {root}, [root]
            while stack:
                v = stack.pop()
                for w in out_edges[v]:
                    assert w not in seen
                    seen.add(w)
                    stack.append(w)
            assert not claimed.intersection(seen)
            claimed.update(seen)
        assert claimed == set(reachable)
        if all(b[i] <= max(before) for i in range(p.m) if i not in reachable):
            assert max(load) <= max(before)
        counts["subtwo_normalizations"] += 1


def audit_normalizations():
    counts = {"normalization_schedules": 0, "schedules_with_cycles": 0, "subtwo_normalizations": 0}
    for times in product((F(0), F(1, 2), F(1)), repeat=3):
        for nu in range(3):
            p = HomeUnit(3, (0, 1, 2), times, ((1, 2), (0, 2), (0, 1)), ((0, 1, 2),) * nu)
            for sigma in product(*(p.choices(j) for j in range(p.n))):
                _check_normalizations(p, sigma, counts)
    # Outdegree-two / overlapping-cycle support, including general loads >=2.
    for nu in range(2):
        p = HomeUnit(3, (0, 0, 1, 2), (F(1),) * 4, ((1, 2), (1, 2), (0, 2), (0, 1)), ((0, 1, 2),) * nu)
        for sigma in product(*(p.choices(j) for j in range(p.n))):
            _check_normalizations(p, sigma, counts)
    # U has arbitrary finite unit endpoints; an unreachable two-cycle is erased.
    p = HomeUnit(3, (1, 2), (F(0), F(1)), ((2,), (1,)), ((0, 1, 2),))
    _check_normalizations(p, (2, 1, 0), counts)
    normalized, reachable, roots = normalize_unit_roots(p, (2, 1, 0))
    assert normalized == (1, 2, 0) and reachable == {0} and roots == (0,)
    # Empty jobs and exact zero, and no home-budget guarantee outside the scope.
    _check_normalizations(HomeUnit(1, (), (), ()), (), counts)
    p = HomeUnit(3, (0, 0), (F(1), F(1)), ((1,), (2,)))
    normalized, _, _ = normalize_unit_roots(p, (1, 2))
    assert p.loads(normalized) == (2, 0, 0)
    counts["boundary_fixtures"] = 3
    return counts


def _oracle_trees(n, edges, root):
    """Enumerate edge subsets independently of the token matrix/decoder."""
    trees = []
    for mask in range(1 << len(edges)):
        chosen = tuple(e for index, e in enumerate(edges) if mask & (1 << index))
        # Direct reachability and indegree checks, not _tree_data.
        vertices = {root}
        incoming = {v: 0 for v in range(n)}
        for v, w in chosen:
            vertices.update((v, w))
            incoming[w] += 1
        if incoming[root] or any(incoming[v] != 1 for v in vertices if v != root):
            continue
        seen = {root}
        changed = True
        while changed:
            changed = False
            for v, w in chosen:
                if v in seen and w not in seen:
                    seen.add(w)
                    changed = True
        if seen == vertices:
            trees.append((chosen, vertices, tuple(sum(v == i for v, _ in chosen) for i in range(n))))
    return trees


def audit_directed_token():
    n = 3
    possible = tuple((v, w) for v in range(n) for w in range(n) if v != w)
    huge = (1 << 80) + 7
    counts = {"digraphs": 0, "token_instances": 0, "complete_assignments": 0, "subtwo_decodings": 0, "tree_schedules": 0}
    for mask in range(1 << len(possible)):
        edges = tuple(e for index, e in enumerate(possible) if mask & (1 << index))
        counts["digraphs"] += 1
        outdegree = tuple(sum(v == i for v, _ in edges) for i in range(n))
        choices = [(0, 1, 2, huge) if outdegree[v] == 0 else (1, 2, huge) for v in range(n)]
        for root in range(n):
            trees = _oracle_trees(n, edges, root)
            for demand in product(*choices):
                token = build_token(n, edges, demand, root)
                p = token.instance
                assert p.n <= 1 + len(edges) + n
                assert all(b <= 1 for b in p.baseline())
                # Independent all-tree optimum: no schedule or decoder calls.
                best_tree = max(min([F(1)] + [F(degree[v], demand[v]) for v in vertices if demand[v]]) for _, vertices, degree in trees)
                best_actual = None
                for sigma in product(*(p.choices(j) for j in range(p.n))):
                    load = p.loads(sigma)
                    value = max(load)
                    best_actual = value if best_actual is None else min(best_actual, value)
                    counts["complete_assignments"] += 1
                    if value < 2:
                        tree = decode_token(token, sigma)
                        assert tree_score(token, tree) >= 2 - value
                        normalized, reachable, _ = normalize_unit_roots(p, sigma)
                        newload = p.loads(normalized)
                        b = p.baseline()
                        assert all(newload[i] == (load[i] if i in reachable else b[i]) for i in range(n))
                        assert max(newload) <= value
                        counts["subtwo_decodings"] += 1
                assert best_actual == 2 - best_tree, (edges, demand, root, best_actual, best_tree)
                for tree, vertices, degree in trees:
                    score = min([F(1)] + [F(degree[v], demand[v]) for v in vertices if demand[v]])
                    sigma = schedule_tree(token, tree)
                    assert max(p.loads(sigma)) <= 2 - score
                    counts["tree_schedules"] += 1
                counts["token_instances"] += 1
    counts["huge_demand"] = str(huge)
    counts["scope"] = "all 64 loopless simple 3-vertex digraphs, every root, all legal demand vectors from {0,1,2,2**80+7}, every complete token assignment and every root-tree edge subset"
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", choices=("all", "normalizations", "token"), default="all")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"arithmetic": "fractions.Fraction", "status": "passed"}
    if args.audit in ("all", "normalizations"):
        result["normalizations"] = audit_normalizations()
    if args.audit in ("all", "token"):
        result["directed_token"] = audit_directed_token()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
