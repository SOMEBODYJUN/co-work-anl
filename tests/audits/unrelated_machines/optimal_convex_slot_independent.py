#!/usr/bin/env python3
"""全局最优凸组合仍可使固定单位槽图接近二倍：独立精确审计。

Scratch reviewer artifact; standard-library only.  General proof is the slot
cardinality count, not the finite checks.  Two finite routes deliberately use
different edge-generation and enumeration methods.
"""

from fractions import Fraction
from itertools import permutations, product
from math import factorial
import json
import platform
import random


def times(m):
    return [Fraction(1)] + [Fraction(1, m + 1)] * (m * m - 1)


def schedules(m):
    # Base: big job at 0; m-1 groups of m+1 small jobs at 1,...,m-1.
    base = [0] + [1 + (j // (m + 1)) for j in range(m * m - 1)]
    return [[(i + shift) % m for i in base] for shift in range(m)]


def load(m, sigma):
    result = [Fraction(0) for _ in range(m)]
    for j, i in enumerate(sigma):
        result[i] += times(m)[j]
    return result


def interval_graph(m, orders):
    """Route A: implement positive interval intersection from first principles."""
    n = m * m
    neighbors = [set() for _ in range(n)]
    slot_mass = [Fraction(0) for _ in range(n)]
    job_mass = [Fraction(0) for _ in range(n)]
    for i, order in enumerate(orders):
        assert sorted(order) == list(range(n)) and order[0] == 0
        cursor = Fraction(0)
        for j in order:
            end = cursor + Fraction(1, m)
            for k in range(m):
                intersection = min(end, Fraction(k + 1)) - max(cursor, Fraction(k))
                if intersection > 0:
                    s = i * m + k
                    neighbors[j].add(s)
                    slot_mass[s] += intersection
                    job_mass[j] += intersection
            cursor = end
        assert cursor == m
    # Exact fractional perfect matching supplies the Hall certificate.
    assert all(value == 1 for value in job_mass)
    assert all(value == 1 for value in slot_mass)
    return neighbors


def one_perfect_matching(graph):
    """Unweighted augmenting path oracle on the interval-built support graph."""
    slot_to_job = {}

    def augment(j, seen):
        for s in sorted(graph[j]):
            if s in seen:
                continue
            seen.add(s)
            if s not in slot_to_job or augment(slot_to_job[s], seen):
                slot_to_job[s] = j
                return True
        return False

    for j in range(len(graph)):
        assert augment(j, set())
    return {j: s for s, j in slot_to_job.items()}


def exact_components_check(m):
    components = schedules(m)
    assert len(components) == m
    for sigma in components:
        assert load(m, sigma) == [Fraction(1)] * m
    for j in range(m * m):
        assert sorted(sigma[j] for sigma in components) == list(range(m))
    # One big job gives OPT >= 1, the actual components give OPT <= 1.
    expected = Fraction(2 * m, m + 1)
    assert expected == 2 - Fraction(2, m + 1)
    assert (m * m - 1) * Fraction(1, m + 1) == m - 1
    return expected


def route_a_m2():
    m = 2
    graph = interval_graph(m, [list(range(m * m)) for _ in range(m)])
    accepted = []
    # Every possible labeled job->slot bijection, no assignment shortcut.
    for image in permutations(range(m * m)):
        if all(image[j] in graph[j] for j in range(m * m)):
            sigma = tuple(s // m for s in image)
            assert max(load(m, sigma)) == Fraction(4, 3)
            assert [sigma.count(i) for i in range(m)] == [m] * m
            accepted.append({"slots": image, "assignment": sigma})
    assert len(accepted) == factorial(m) ** m == 4
    return {"m": m, "bijections_examined": factorial(m * m), "perfect_matchings": accepted,
            "all_makespans": "4/3"}


def route_b_m3():
    # Independently derive each chosen job's slot by rank // m, then locally
    # enumerate slot injections rather than invoking Route A's graph or oracle.
    m = 3
    n = 9
    opt = None
    expandable = 0
    cardinality_balanced = 0
    makespans = set()
    for sigma in product(range(m), repeat=n):
        C = max(load(m, sigma))
        opt = C if opt is None else min(opt, C)
        chosen = [[j for j, i in enumerate(sigma) if i == machine]
                  for machine in range(m)]
        if all(len(js) == m for js in chosen):
            cardinality_balanced += 1
        can_expand = True
        for js in chosen:
            if len(js) > m:
                can_expand = False
                break
            # Direct local enumeration of all injections into machine slots.
            if not any(all(j // m == k for j, k in zip(js, injection))
                       for injection in permutations(range(m), len(js))):
                can_expand = False
                break
        if can_expand:
            expandable += 1
            makespans.add(str(C))
            assert C == Fraction(3, 2)
            assert all(len(js) == m for js in chosen)
    assert opt == 1 and expandable == factorial(m) ** m == 216
    assert cardinality_balanced == factorial(n) // (factorial(m) ** m) == 1680
    return {"m": m, "assignments_examined": 3 ** 9,
            "OPT_by_all_assignments": str(opt),
            "cardinality_balanced": cardinality_balanced,
            "slot_expandable": expandable, "expandable_makespans": sorted(makespans)}


def tie_and_hall_checks():
    # For all orders, exact per-job and per-slot mass 1 proves Hall symbolically.
    # Below are reproducibility checks, not an enumeration of all tie orders.
    rng = random.Random(704091)
    records = []
    for m in [1, 2, 3, 4, 5, 8, 12]:
        target = exact_components_check(m)
        n = m * m
        for trial in range(3):
            orders = []
            for i in range(m):
                small = list(range(1, n))
                if trial == 1:
                    small.reverse()
                elif trial == 2:
                    rng.shuffle(small)
                orders.append([0] + small)
            graph = interval_graph(m, orders)
            matching = one_perfect_matching(graph)
            sigma = [matching[j] // m for j in range(n)]
            assert [sigma.count(i) for i in range(m)] == [m] * m
            assert max(load(m, sigma)) == target
            source=sigma[0]
            co_small=[j for j in range(1,n) if sigma[j]==source]
            dests=[i for i in range(m) if i!=source]
            assert len(co_small)==len(dests)==m-1
            repair=sigma.copy()
            for j,i in zip(co_small,dests):repair[j]=i
            assert load(m,repair)==[Fraction(1)]*m
            assert sum(x!=y for x,y in zip(sigma,repair))==m-1
            if m <= 4:
                # Explicit every-subset Hall audit; larger m uses mass certificate.
                for mask in range(1 << n):
                    U = [j for j in range(n) if mask & (1 << j)]
                    adjacent = set().union(*(graph[j] for j in U)) if U else set()
                    assert len(adjacent) >= len(U)
        records.append({"m": m, "n": n, "optimal_components": m,
                        "per_job_and_slot_mass": "1", "makespan": str(target),
                        "tie_orders_checked": 3,
                        "all_Hall_subsets_checked": m <= 4})
    return records


if __name__ == "__main__":
    result = {
        "title": "真实最优调度凸组合的固定槽图近二倍障碍：独立审计",
        "python": platform.python_version(), "arithmetic": "fractions.Fraction",
        "seed": 704091,
        "family": "m machines, m^2 jobs: one size 1, m^2-1 size 1/(m+1)",
        "route_A": route_a_m2(), "route_B": route_b_m3(),
        "component_and_tie_checks": tie_and_hall_checks(),
        "scope": "Finite exact evidence; general claim needs the elementary cardinality and convex-decomposition proof.",
        "limitations": "Does not obstruct using a supplied optimal convex-combination component directly; does not prove algorithmic hardness or UM-TARGET-v1.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
