#!/usr/bin/env python3
"""鲁棒循环批量修复：精确菜单提取、缩放编译及有限交叉核验。

None denotes infinity. Every numerical input is int or Fraction, never float.
This is a local optimizer, not a better-than-two approximation algorithm.
Run from the repository root; stdout is new evidence, never overwritten here.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from collections import deque
from itertools import product, permutations
from pathlib import Path
from random import Random
import hashlib
import json
import platform


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)) or x < 0:
        raise ValueError("expected a nonnegative exact rational")
    return F(x)


def validate(p, sigma):
    if not isinstance(p, (list, tuple)) or not p:
        raise ValueError("at least one machine is required")
    n = len(p[0])
    if any(len(row) != n for row in p) or len(sigma) != n:
        raise ValueError("inconsistent dimensions")
    p = [[None if x is None else rational(x) for x in row] for row in p]
    for j, i in enumerate(sigma):
        if isinstance(i, bool) or not isinstance(i, int) or not 0 <= i < len(p):
            raise ValueError("invalid machine index")
        if p[i][j] is None:
            raise ValueError("unavailable assignment")
    return p, tuple(sigma)


def loads(p, sigma):
    result = [F(0)] * len(p)
    for j, i in enumerate(sigma):
        result[i] += p[i][j]
    return tuple(result)


@dataclass(frozen=True)
class Arc:
    source: int
    target: int
    jobs: tuple[int, ...]
    removal: F
    arrival: F


def cycle_good(menu, cycle, margin=F(0)):
    if not cycle:
        return False
    strict = False
    for i, x in enumerate(cycle):
        a, b = menu[x], menu[cycle[(i+1) % len(cycle)]]
        if a.target != b.source or a.arrival > b.removal-margin:
            return False
        strict |= a.arrival < b.removal
    return strict


def extract_cycle(menu, margin=F(0)):
    """Exact polynomial oracle for an explicit menu; returns distinct sources.

    It finds turns arrival <= next removal-margin and at least one strict
    decrease. A zero-margin cycle of equalities is deliberately not accepted.
    """
    margin = rational(margin)
    size = len(menu)
    adjacency, reverse = [[] for _ in menu], [[] for _ in menu]
    for x, a in enumerate(menu):
        if a.source == a.target or a.removal < 0 or a.arrival < 0:
            raise ValueError("invalid arc")
        for y, b in enumerate(menu):
            if a.target == b.source and a.arrival <= b.removal-margin:
                adjacency[x].append(y)
                reverse[y].append(x)
    seen, order = set(), []
    for start in range(size):
        if start in seen:
            continue
        seen.add(start)
        stack = [(start, 0)]
        while stack:
            v, index = stack[-1]
            if index == len(adjacency[v]):
                stack.pop()
                order.append(v)
            else:
                w = adjacency[v][index]
                stack[-1] = v, index+1
                if w not in seen:
                    seen.add(w)
                    stack.append((w, 0))
    component = [-1] * size
    for start in reversed(order):
        if component[start] >= 0:
            continue
        component[start] = start
        stack = [start]
        while stack:
            v = stack.pop()
            for w in reverse[v]:
                if component[w] < 0:
                    component[w] = start
                    stack.append(w)
    witness = next(((x, y) for x in range(size) for y in adjacency[x]
                    if component[x] == component[y]
                    and menu[x].arrival < menu[y].removal), None)
    if witness is None:
        return None
    x, y = witness
    predecessor, queue = {y: None}, deque([y])
    while queue and x not in predecessor:
        v = queue.popleft()
        for w in adjacency[v]:
            if component[w] == component[x] and w not in predecessor:
                predecessor[w] = v
                queue.append(w)
    path, v = [], x
    while v is not None:
        path.append(v)
        v = predecessor[v]
    path.reverse()
    cycle = [x] + path[:-1]
    assert cycle_good(menu, cycle, margin)
    # Scalar removal order guarantees at least one branch remains admissible.
    # Checking the two branches also handles equalities and strictness exactly.
    while len({menu[x].source for x in cycle}) < len(cycle):
        first = {}
        for j, x in enumerate(cycle):
            u = menu[x].source
            if u in first:
                i = first[u]
                branches = [cycle[i:j], cycle[j:]+cycle[:i]]
                valid = [b for b in branches if cycle_good(menu, b, margin)]
                assert valid
                cycle = min(valid, key=lambda b: (len(b), tuple(b)))
                break
            first[u] = j
    return tuple(cycle)


def rounded_menu(p, sigma, target, eta):
    """Minimum-arrival representatives at every exact rounded-removal state."""
    n, m = len(sigma), len(p)
    if not n:
        return []
    h = eta*target/(2*n)
    bound = (4*n/eta).__floor__()
    menu = []
    for u in range(m):
        for v in range(m):
            if u == v:
                continue
            items = [j for j in range(n) if sigma[j] == u
                     and p[v][j] is not None and p[v][j] <= target]
            if not items:
                continue
            dp = [None]*(bound+1)
            dp[0] = F(0), None
            for j in items:
                z = (p[u][j]/h).__floor__()
                if z == 0:
                    continue  # Nonnegative arrival cost cannot help this state.
                nxt = list(dp)
                for q, state in enumerate(dp):
                    if state is None or q+z > bound:
                        continue
                    cost, node = state
                    cost += p[v][j]
                    if nxt[q+z] is None or cost < nxt[q+z][0]:
                        nxt[q+z] = cost, (j, node)
                dp = nxt
            for q, state in enumerate(dp[1:], 1):
                if state is None:
                    continue
                cost, node = state
                chosen = []
                while node is not None:
                    j, node = node
                    chosen.append(j)
                chosen = tuple(sorted(chosen))
                removal = sum((p[u][j] for j in chosen), F(0))
                assert removal >= q*h
                menu.append(Arc(u, v, chosen, removal, cost))
    return menu


def apply_cycle(p, sigma, menu, cycle, margin=F(0)):
    assert cycle_good(menu, cycle, margin)
    assert len({menu[x].source for x in cycle}) == len(cycle)
    result = list(sigma)
    for x in cycle:
        a = menu[x]
        assert all(sigma[j] == a.source for j in a.jobs)
        assert a.removal == sum((p[a.source][j] for j in a.jobs), F(0))
        assert a.arrival == sum((p[a.target][j] for j in a.jobs), F(0))
        for j in a.jobs:
            result[j] = a.target
    before, after = loads(p, sigma), loads(p, result)
    assert all(a <= b for a, b in zip(after, before))
    assert sum(after) < sum(before)
    for x in cycle:
        i = menu[x].source
        assert after[i] <= before[i]-margin
    return tuple(result)


def optimize(p, sigma, target, eta):
    """Terminates at no eta*T-robust cyclic-batch exchange on pruned edges.

    Fixed eta: deterministic polynomial in binary input length. Variable eta:
    polynomial in 1/eta, NOT in log(1/eta). No approximation ratio is asserted.
    """
    p, sigma = validate(p, sigma)
    target, eta = rational(target), rational(eta)
    if not 0 < eta < 1:
        raise ValueError("eta must be in (0,1)")
    if max(loads(p, sigma)) > 2*target:
        raise ValueError("starting schedule must have makespan <= 2T")
    if any(p[i][j] > target for j, i in enumerate(sigma)):
        raise ValueError("starting schedule must use pruned edges")
    if target == 0 or not sigma:
        return sigma, {"iterations": 0, "robust_claim_applicable": target > 0}
    margin, rounds = eta*target/2, 0
    initial = loads(p, sigma)
    while True:
        menu = rounded_menu(p, sigma, target, eta)
        cycle = extract_cycle(menu, margin)
        if cycle is None:
            break
        sigma = apply_cycle(p, sigma, menu, cycle, margin)
        rounds += 1
        assert rounds <= (4*len(p)/eta).__floor__()
    assert all(x <= y for x, y in zip(loads(p, sigma), initial))
    return sigma, {"iterations": rounds, "robust_claim_applicable": True,
                   "terminal_menu_arcs": len(menu)}


def all_bundles(p, sigma, target):
    menu = []
    for u in range(len(p)):
        for v in range(len(p)):
            if u == v:
                continue
            eligible = [j for j, i in enumerate(sigma) if i == u
                        and p[v][j] is not None and p[v][j] <= target]
            for mask in range(1, 1 << len(eligible)):
                jobs = tuple(j for a, j in enumerate(eligible) if mask >> a & 1)
                menu.append(Arc(u, v, jobs,
                                sum((p[u][j] for j in jobs), F(0)),
                                sum((p[v][j] for j in jobs), F(0))))
    return menu


def direct_cycle(menu, m, margin):
    """Independent exponential machine-order / option enumeration, audit only."""
    by_pair = {}
    for a in menu:
        by_pair.setdefault((a.source, a.target), []).append(a)
    for length in range(2, m+1):
        for order in permutations(range(m), length):
            if order[0] != min(order):
                continue
            options = [by_pair.get((order[i], order[(i+1) % length]), [])
                       for i in range(length)]
            for chosen in product(*options):
                if all(chosen[i].arrival <= chosen[(i+1) % length].removal-margin
                       for i in range(length)) and any(
                           chosen[i].arrival < chosen[(i+1) % length].removal
                           for i in range(length)):
                    return chosen
    return None


def audit():
    rng, menu_cases, optimizer_cases = Random(613513), 0, 0
    for m in range(2, 5):
        for _ in range(120):
            menu = [Arc(u, v, (), F(rng.randrange(9), 4), F(rng.randrange(9), 4))
                    for u in range(m) for v in range(m) if u != v
                    for _ in range(rng.randrange(3))]
            for margin in (F(0), F(1, 4)):
                exact = direct_cycle(menu, m, margin)
                found = extract_cycle(menu, margin)
                assert (exact is None) == (found is None)
                if found:
                    assert cycle_good(menu, found, margin)
                    assert len({menu[x].source for x in found}) == len(found)
                menu_cases += 1
    iterations = []
    for _ in range(100):
        m, n, target, eta = rng.randrange(2, 5), rng.randrange(1, 8), F(1), F(1, 3)
        p = [[None if rng.randrange(5) == 0 else F(rng.randrange(5), 4)
              for _ in range(n)] for _ in range(m)]
        sigma = []
        for j in range(n):
            possible = [i for i in range(m) if p[i][j] is not None]
            if not possible:
                p[0][j] = F(0)
                possible = [0]
            sigma.append(rng.choice(possible))
        if max(loads(p, sigma)) > 2:
            continue
        true_menu = all_bundles(p, sigma, target)
        compiled = rounded_menu(p, sigma, target, eta)
        # Enumerate every real subset and check its actual DP representative.
        h = eta*target/(2*n)
        for a in true_menu:
            q = sum((p[a.source][j]/h).__floor__() for j in a.jobs)
            if q:
                witnesses = [b for b in compiled if b.source == a.source
                             and b.target == a.target and
                             sum((p[b.source][j]/h).__floor__() for j in b.jobs) == q]
                assert any(b.arrival <= a.arrival and
                           b.removal >= a.removal-eta*target/2 for b in witnesses)
        if direct_cycle(true_menu, m, eta*target):
            assert extract_cycle(compiled, eta*target/2) is not None
        result, info = optimize(p, sigma, target, eta)
        assert direct_cycle(all_bundles(p, result, target), m, eta*target) is None
        assert all(a <= b for a, b in zip(loads(p, result), loads(p, sigma)))
        optimizer_cases += 1
        iterations.append(info['iterations'])
    # Both orthogonal elementary traps are handled when their needed bundles
    # are present; these checks are actual optimization runs, not formulas.
    fanout = []
    for k in (1, 2, 3, 7, 31):
        p = [[F(1), F(1)]+[F(1, 4*k)]*(4*k),
             [F(1), None]+[F(1, k)]*(2*k)+[None]*(2*k),
             [None, F(1)]+[None]*(2*k)+[F(1, k)]*(2*k)]
        start = (0, 0)+(1,)*(2*k)+(2,)*(2*k)
        result, info = optimize(p, start, F(1), F(1, 4))
        # Local robustness is not global optimality: a leaf can remain above 1
        # while further improvement would increase the already-light center.
        assert max(loads(p, result)) < 2
        fanout.append({"k": k, "final_loads": list(map(str, loads(p, result))), **info})
    ring = []
    for m in (2, 3, 5, 9):
        p = [[None]*(2*m) for _ in range(m)]
        for u in range(m):
            for j in (2*u, 2*u+1):
                p[u][j], p[(u+1) % m][j] = F(1), F(1, 2)
        start = tuple(j//2 for j in range(2*m))
        result, info = optimize(p, start, F(1), F(1, 4))
        assert max(loads(p, result)) == 1
        ring.append({"m": m, "final_makespan": "1", **info})
    fork = []
    for k in (2, 3, 7, 31, 2**80+1):
        eta, a = F(1, k), 1-F(1, 2*k)
        p = [[a, a, F(1), None, None, None],
             [eta/4, None, a, eta/4, a, None],
             [None, eta/2, None, a, None, a]]
        start = (0, 0, 1, 2, 1, 2)
        assert extract_cycle(all_bundles(p, start, F(1))) is None
        result, info = optimize(p, start, F(1), F(1, 4))
        assert result == start
        fork.append({"parameter": str(eta), "initial_makespan": str(2-eta), **info})
    fixture_path = Path(__file__).resolve().parents[3]/'examples/unrelated_machines/padded_fork_k2.json'
    fixture = json.loads(fixture_path.read_text())
    m = len(fixture['machine_labels'])
    data = fixture['finite_processing_matrix']
    p = [[F(row[str(i)]) if str(i) in row else None for row in data] for i in range(m)]
    start = tuple(fixture['initial_assignment'])
    result, padded_info = optimize(p, start, F(1), F(1, 4))
    assert result == start and padded_info['iterations'] == 0
    padded_info['input_sha256'] = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    boundaries = [([[F(0)]], (0,), F(0), F(1, 4)),
                  ([[], []], (), F(1), F(1, 4)),
                  ([[F(1, 2**80+1)], [F(0)]], (0,), F(1), F(1, 4))]
    for args in boundaries:
        result, _ = optimize(*args)
        assert max(loads(args[0], result)) <= max(loads(args[0], args[1]))
    invalid = [([], (), F(1), F(1, 4)), ([[1.0]], (0,), F(1), F(1, 4)),
               ([[None]], (0,), F(1), F(1, 4)), ([[1]], (False,), F(1), F(1, 4)),
               ([[1]], (0,), F(1), F(0)), ([[1]], (0,), F(0), F(1, 4))]
    for args in invalid:
        try:
            optimize(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input accepted")
    return {"status": "passed", "python": platform.python_version(),
            "arithmetic": "fractions.Fraction", "seed": 613513,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "explicit_menu_comparisons": menu_cases,
            "random_optimizer_cases": optimizer_cases,
            "successful_iteration_counts": iterations,
            "fanout_optimization": fanout, "ring_optimization": ring,
            "actual_padded_fork_optimizer": padded_info,
            "fork_stagnation": fork, "boundary_cases": len(boundaries),
            "invalid_cases": len(invalid),
            "limitations": ["Finite exact tests are not the general proof.",
                            "No universal approximation ratio is asserted.",
                            "No generic LP solver or LP-initialization theorem is implemented."]}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
