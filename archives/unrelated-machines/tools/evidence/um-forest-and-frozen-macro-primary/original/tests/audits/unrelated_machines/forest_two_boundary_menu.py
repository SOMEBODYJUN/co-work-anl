"""双边界森林的一端精确、另一端乘性保零菜单。

Normalized sparse-input oracle. Every menu item stores a real assignment with
original task identities. Fraction/integer arithmetic only; no repository writes.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from random import Random
import json
import platform


def ceil(x):
    return -((-x.numerator) // x.denominator)


def loads(jobs, assignment, vertices):
    out = dict.fromkeys(vertices, F(0))
    for job, vertex in zip(jobs, assignment):
        out[vertex] += job[vertex]
    return out


@dataclass(frozen=True)
class MenuItem:
    a_load: F
    b_load: F
    assignment: tuple
    budget: F


def topology(jobs, a, b):
    if a == b:
        raise ValueError("two distinct boundaries required")
    vertices = sorted({a, b}.union(*(set(job) for job in jobs)))
    dsu = {v: v for v in vertices}
    adjacency = {v: [] for v in vertices}
    fixed = {v: [] for v in vertices}
    bundles = {}

    def find(v):
        while dsu[v] != v:
            dsu[v] = dsu[dsu[v]]
            v = dsu[v]
        return v

    for j, job in enumerate(jobs):
        if not 1 <= len(job) <= 2 or any(p < 0 for p in job.values()):
            raise ValueError("jobs need one or two nonnegative finite times")
        endpoints = tuple(sorted(job))
        if len(endpoints) == 1:
            fixed[endpoints[0]].append(j)
        else:
            if endpoints not in bundles:
                u, v = endpoints
                ru, rv = find(u), find(v)
                if ru == rv:
                    raise ValueError("simple machine support is not a forest")
                dsu[ru] = rv
                adjacency[u].append(v)
                adjacency[v].append(u)
                bundles[endpoints] = []
            bundles[endpoints].append(j)

    parent = {}
    children = {v: [] for v in vertices}
    order = []
    for start in [a] + [v for v in vertices if v != a]:
        if start in parent:
            continue
        parent[start] = None
        stack = [start]
        while stack:
            v = stack.pop()
            order.append(v)
            for w in adjacency[v]:
                if w != parent[v]:
                    parent[w] = v
                    children[v].append(w)
                    stack.append(w)
    return vertices, fixed, bundles, children, order


def grid_optimum(jobs, a, q, caps, graph):
    """Exact optimum at a, integer weights and capacities everywhere else.

    Returns None iff the rounded model is infeasible. The other connected
    components are feasibility problems, with no hidden objective constraints.
    """
    vertices, fixed, bundles, children, order = graph
    residual = {}
    assignments = {}
    minimum = {}

    def weight(j, v):
        return jobs[j][v] if v == a else q[j][v]

    for v in reversed(order):
        value = sum((weight(j, v) for j in fixed[v]), F(0) if v == a else 0)
        for w in children[v]:
            cap = residual[w]
            js = bundles[tuple(sorted((v, w)))]
            dp = [None] * (cap + 1)
            dp[0] = F(0) if v == a else 0
            layers = []
            for j in js:
                ndp = [None] * (cap + 1)
                back = [None] * (cap + 1)
                for used, current in enumerate(dp):
                    if current is None:
                        continue
                    parent_value = current + weight(j, v)
                    if ndp[used] is None or parent_value < ndp[used]:
                        ndp[used] = parent_value
                        back[used] = (used, v)
                    child_used = used + q[j][w]
                    if child_used <= cap:
                        if ndp[child_used] is None or current < ndp[child_used]:
                            ndp[child_used] = current
                            back[child_used] = (used, w)
                dp = ndp
                layers.append(back)
            candidates = [(cost, used) for used, cost in enumerate(dp) if cost is not None]
            if not candidates:
                return None
            burden, used = min(candidates)
            value += burden
            for j, back in reversed(list(zip(js, layers))):
                previous, vertex = back[used]
                assignments[j] = vertex
                used = previous
        minimum[v] = value
        for j in fixed[v]:
            assignments[j] = v
        if v != a:
            if value > caps[v]:
                return None
            residual[v] = caps[v] - value
    witness = tuple(assignments[j] for j in range(len(jobs)))
    return minimum[a], witness


def boundary_menu(jobs, a, b, target, eta, verify=False):
    """Return menu and metadata; an empty menu certifies no original T schedule.

    For every legal rho with b and all internal loads <= T (a is unbounded),
    there is a returned tau with
        L_a(tau) <= L_a(rho), L_b(tau) <= (1+eta)L_b(rho),
        L_v(tau) <= (1+eta)T for every internal machine v.
    In particular, zero original b load is preserved exactly.

    There is no T feasibility iff success promise. Menu entries are correlated
    alternatives, not independent ordinary summary jobs.
    """
    jobs = [{v: F(p) for v, p in job.items()} for job in jobs]
    target, eta = F(target), F(eta)
    if target < 0 or eta <= 0:
        raise ValueError("target >= 0 and eta > 0 required")
    graph = topology(jobs, a, b)
    vertices = graph[0]
    n = len(jobs)
    if target == 0 or n == 0:
        assignment = []
        for job in jobs:
            zero_non_a = [v for v in sorted(job) if v != a and job[v] == 0]
            if zero_non_a:
                assignment.append(zero_non_a[0])
            elif a in job:
                assignment.append(a)
            else:
                return [], {"K": 0, "budgets": [F(0)], "epsilon": F(0), "vertices": vertices}
        actual = loads(jobs, assignment, vertices)
        return [MenuItem(actual[a], F(0), tuple(assignment), F(0))], {"K": 0, "budgets": [F(0)], "epsilon": F(0), "vertices": vertices}

    epsilon = min(eta / 3, F(1, 3))
    K = n + (F(n) / epsilon).__floor__()
    delta_internal = epsilon * target / n
    budgets = [F(0)]
    positive_b_times = [job[b] for job in jobs if b in job and job[b] > 0]
    if positive_b_times:
        budget = min(positive_b_times)
        if budget <= target:
            while True:
                budgets.append(budget)
                if budget >= target:
                    break
                budget *= 1 + epsilon

    menu = []
    seen = set()
    for budget in budgets:
        q = []
        for job in jobs:
            row = {}
            for v, p in job.items():
                if v == a:
                    continue
                if v == b:
                    row[v] = int(p > 0) if budget == 0 else ceil(p * n / (epsilon * budget))
                else:
                    row[v] = ceil(p / delta_internal)
            q.append(row)
        caps = {v: K for v in vertices if v != a}
        if budget == 0:
            caps[b] = 0
        result = grid_optimum(jobs, a, q, caps, graph)
        if verify:
            grid_best = None
            for candidate in product(*(tuple(sorted(job)) for job in jobs)):
                ok = all(sum((q[j].get(v, 0) for j, w in enumerate(candidate) if w == v), 0) <= caps[v] for v in caps)
                if ok:
                    candidate_value = sum((jobs[j][a] for j, w in enumerate(candidate) if w == a), F(0))
                    grid_best = candidate_value if grid_best is None else min(grid_best, candidate_value)
            assert (grid_best is None) == (result is None)
            if result is not None:
                assert grid_best == result[0]
        if result is None:
            continue
        value, assignment = result
        if assignment in seen:
            continue
        seen.add(assignment)
        actual = loads(jobs, assignment, vertices)
        assert value == actual[a]
        assert all(actual[v] <= (1 + epsilon) * target for v in vertices if v not in (a, b))
        assert actual[b] == 0 if budget == 0 else actual[b] <= (1 + epsilon) * budget
        menu.append(MenuItem(actual[a], actual[b], assignment, budget))
    return menu, {"K": K, "budgets": budgets, "epsilon": epsilon, "vertices": vertices}


def audit():
    rng = Random(16102026)
    cases, feasible_cases, certificates, checked_schedules, zero_schedules = 0, 0, 0, 0, 0
    max_menu, max_guesses = 0, 0
    for m in range(2, 7):
        for _ in range(100):
            edges = [(v, rng.randrange(v)) for v in range(1, m) if rng.randrange(4)]
            n = rng.randrange(9)
            jobs = []
            for _ in range(n):
                if edges and rng.randrange(4):
                    u, v = rng.choice(edges)
                    jobs.append({u: F(rng.randrange(8), rng.randrange(1, 7)), v: F(rng.randrange(8), rng.randrange(1, 7))})
                else:
                    v = rng.randrange(m)
                    jobs.append({v: F(rng.randrange(8), rng.randrange(1, 7))})
            a, b = rng.sample(range(m), 2)
            target = F(rng.randrange(8), rng.randrange(1, 7))
            eta = rng.choice([F(1, 2), F(1, 3), F(1, 5), F(2)])
            menu, meta = boundary_menu(jobs, a, b, target, eta, verify=True)
            original_feasible = []
            for rho in product(*(tuple(sorted(job)) for job in jobs)):
                load = loads(jobs, rho, range(m))
                if all(load[v] <= target for v in range(m) if v != a):
                    original_feasible.append((rho, load))
            for rho, load in original_feasible:
                assert any(item.a_load <= load[a] and item.b_load <= (1 + eta) * load[b] for item in menu)
                checked_schedules += 1
                zero_schedules += int(load[b] == 0)
            if original_feasible:
                feasible_cases += 1
            if not menu:
                assert not original_feasible
                certificates += 1
            max_menu = max(max_menu, len(menu))
            max_guesses = max(max_guesses, len(meta["budgets"]))
            cases += 1

    # One bundle is already a nontrivial Pareto tradeoff; all menu witnesses retain IDs.
    denominator = 2**1000 + 937
    jobs = [{0: F(j + 1, 17), 1: F(j + 1, denominator)} for j in range(7)]
    menu, meta = boundary_menu(jobs, 0, 1, F(28, denominator), F(1, 5), verify=True)
    assert menu
    assert any(item.b_load == 0 for item in menu)
    # Very large labels must not allocate arrays indexed by numerical machine count.
    huge = 2**1000
    sparse, _ = boundary_menu([{huge: F(0), huge + 1: F(1)}, {huge + 2: F(0)}], huge, huge + 1, F(0), F(1, 5))
    assert len(sparse) == 1 and sparse[0].assignment == (huge, huge + 2)
    unbounded_a, _ = boundary_menu([{0: F(7)}, {0: F(4), 1: F(0)}, {0: F(0), 2: F(8)}], 0, 1, F(0), F(1, 5))
    assert len(unbounded_a) == 1 and unbounded_a[0].a_load == 7 and unbounded_a[0].b_load == 0
    # Deep forests use an explicit stack; no recursive call-depth hypothesis.
    deep_jobs = [{v: F(1), v + 1: F(1)} for v in range(1001)]
    deep, deep_meta = boundary_menu(deep_jobs, 0, 1001, F(1), F(1))
    assert deep and all(item.a_load <= 1 for item in deep)
    # A genuine simple cycle is outside the contract, bundles themselves are fine.
    try:
        boundary_menu([{0: F(1), 1: F(1)}, {1: F(1), 2: F(1)}, {2: F(1), 0: F(1)}], 0, 1, F(1), F(1))
        raise AssertionError("cycle accepted")
    except ValueError as error:
        assert "forest" in str(error)

    # Disjoint gadgets sharing b: multiplicative errors sum with no count factor.
    # Use original schedules assigning the first task in every gadget to b.
    shared_original = F(0)
    shared_output = F(0)
    for g in range(1, 31):
        a = g + 1
        original_b = F(g, 1000)
        jobs = [{a: F(1, 3), 0: original_b}, {a: F(1, 3), 0: F(g + 1, 1000)}]
        menu, _ = boundary_menu(jobs, a, 0, F(1), F(1, 5))
        matches = [item for item in menu if item.a_load <= F(1, 3) and item.b_load <= F(6, 5) * original_b]
        assert matches
        chosen = min(matches, key=lambda item: item.b_load)
        shared_original += original_b
        shared_output += chosen.b_load
    assert shared_output <= F(6, 5) * shared_original
    return {
        "claim": "UM-FOREST-TWO-BOUNDARY-MENU-v1",
        "seed": 16102026,
        "random_cases": cases,
        "original_feasible_cases": feasible_cases,
        "empty_menu_certificates": certificates,
        "covered_original_schedules": checked_schedules,
        "zero_b_original_schedules": zero_schedules,
        "max_menu_items": max_menu,
        "max_geometric_guesses": max_guesses,
        "large_denominator_bits": denominator.bit_length(),
        "deep_path_edges": len(deep_jobs),
        "deep_menu_items": len(deep),
        "deep_K": deep_meta["K"],
        "shared_boundary_gadgets": 30,
        "shared_boundary_original": str(shared_original),
        "shared_boundary_output": str(shared_output),
        "python": platform.python_version(),
        "arithmetic": "Fraction/integer only",
        "limits": "finite audit, no general R||Cmax result; correlated menus require a core selection algorithm",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
