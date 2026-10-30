#!/usr/bin/env python3
"""Exact finite audit for MULTICOLUMN-2 v1; not a universal proof.

No ratios are used for assertions.  Monotone samples extend to step functions
on [0,infinity), so every sampled instance is in the claimed input class.
"""

from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import json
import random


def balanced_counts(n, q, t):
    small, remainder = divmod(n - t, q - 1)
    return (t,) + (small,) * (q - 1 - remainder) + (small + 1,) * remainder


def arrays(n, q, w, f, low, middle, high):
    A = [f[1 + w * t] + (q - 1) * low for t in range(n + 1)]
    D = [f[w * t] + high + (q - 2) * low for t in range(n + 1)]
    F = [f[1 + w * t] + (n - t) * high + t * middle
         for t in range(n + 1)]
    return A, D, F


def light_ne(counts, A, D):
    for origin, count in enumerate(counts):
        if not count:
            continue
        current = A[count] if origin == 0 else D[count]
        for dest, target in enumerate(counts):
            if origin != dest:
                deviated = A[target + 1] if dest == 0 else D[target + 1]
                if current > deviated:
                    return False
    return True


def potential(counts, A, D):
    return sum(A[1:counts[0] + 1]) + sum(
        sum(D[1:count + 1]) for count in counts[1:])


def exhaustive_audit():
    scenarios = [(q, n, Fraction(1))
                 for q in (3, 4, 5) for n in (1, 3, 5, 7)]
    scenarios += [(3, n, w) for n in (1, 3, 5)
                  for w in (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3),
                            Fraction(2, 5), Fraction(3, 4))]
    totals = {"instances": 0, "balanced_light_ne": 0,
              "minimum_potential_states": 0, "zero_heavy_cost_states": 0,
              "exceptional_comparisons": 0, "max_heavy_ratio": "1"}
    maximum = Fraction(1)
    scenario_outputs = []
    for q, n, w in scenarios:
        loads = sorted({w * t for t in range(n + 1)} |
                       {1 + w * t for t in range(n + 1)})
        g_values = [triple for triple in combinations_with_replacement(range(4), 3)
                    if w != 1 or triple[0] == triple[1]]
        local = {"q": q, "n": n, "w": str(w), "instances": 0,
                 "balanced_light_ne": 0}
        counts_list = [balanced_counts(n, q, t) for t in range(n + 1)]
        for values in combinations_with_replacement(range(4), len(loads)):
            f = dict(zip(loads, values))
            for low, middle, high in g_values:
                A, D, F = arrays(n, q, w, f, low, middle, high)
                potentials = [potential(counts, A, D) for counts in counts_list]
                optimum = min(potentials)
                for counts, psi in zip(counts_list, potentials):
                    is_ne = light_ne(counts, A, D)
                    if psi == optimum:
                        assert is_ne, (q, n, w, f, (low, middle, high), counts)
                        totals["minimum_potential_states"] += 1
                    if not is_ne:
                        continue
                    local["balanced_light_ne"] += 1
                    totals["balanced_light_ne"] += 1
                    t = counts[0]
                    if F[t] == 0:
                        totals["zero_heavy_cost_states"] += 1
                    for u in counts[1:]:
                        assert F[t] <= 2 * F[u], (
                            q, n, w, f, (low, middle, high), counts, F)
                        if t == 0 and 2 * u == n + 1:
                            totals["exceptional_comparisons"] += 1
                        if F[u] != 0:
                            maximum = max(maximum, Fraction(F[t], F[u]))
                        else:
                            assert F[t] == 0
                local["instances"] += 1
                totals["instances"] += 1
        scenario_outputs.append(local)
    totals["max_heavy_ratio"] = str(maximum)
    return {"totals": totals, "scenarios": scenario_outputs}


def direct_costs(q, n, w, assignment, heavy, f, g):
    strategies = []
    strategies.append({(heavy, 0)} | {(heavy, i + 1) for i in range(n)})
    for i, chosen in enumerate(assignment):
        strategies.append({(chosen, 0)} |
                          {(col, i + 1) for col in range(q) if col != chosen})
    weights = [Fraction(1)] + [w] * n
    loads = {(col, i): Fraction(0) for col in range(q) for i in range(n + 1)}
    for strategy, weight in zip(strategies, weights):
        for resource in strategy:
            loads[resource] += weight
    costs = []
    for strategy in strategies:
        costs.append(sum(f(loads[resource]) if resource[1] == 0
                         else g(loads[resource]) for resource in strategy))
    return costs


def direct_formula_audit():
    checked = 0
    for q in (3, 4):
        for n in (1, 2, 3, 4):
            for w in (Fraction(1), Fraction(1, 2), Fraction(2, 3)):
                for assignment in product(range(q), repeat=n):
                    counts = [assignment.count(col) for col in range(q)]
                    for heavy in range(q):
                        f = lambda load: load ** 3 + 2 * load
                        g = lambda load: load ** 2
                        direct = direct_costs(q, n, w, assignment, heavy, f, g)
                        t = counts[heavy]
                        formula_heavy = f(1 + w * t) + (n - t) * g(1 + w) + t * g(1)
                        assert direct[0] == formula_heavy
                        for i, chosen in enumerate(assignment):
                            expected = f(w * counts[chosen] + (chosen == heavy))
                            expected += (q - 1) * g(w)
                            if chosen != heavy:
                                expected += g(1 + w) - g(w)
                            assert direct[i + 1] == expected
                        checked += 1
    return checked


def large_integer_audit():
    rng = random.Random(20261014)
    checked = 0
    for _ in range(3000):
        q = rng.randrange(3, 9)
        n = rng.randrange(1, 51)
        w = Fraction(rng.randrange(1, 13), 12)
        loads = sorted({w * t for t in range(n + 1)} |
                       {1 + w * t for t in range(n + 1)})
        increments = [rng.choice((0, 0, 1, 10, 1000)) for _ in loads]
        values = []
        running = 0
        for increment in increments:
            running += increment
            values.append(running)
        f = dict(zip(loads, values))
        low, middle, high = sorted(rng.randrange(2001) for _ in range(3))
        if w == 1:
            middle = low
        A, D, F = arrays(n, q, w, f, low, middle, high)
        counts_list = [balanced_counts(n, q, t) for t in range(n + 1)]
        psi = [potential(counts, A, D) for counts in counts_list]
        optimum = min(psi)
        for counts, value in zip(counts_list, psi):
            if value == optimum:
                assert light_ne(counts, A, D)
                assert all(F[counts[0]] <= 2 * F[u] for u in counts[1:])
        checked += 1
    return checked


def main():
    result = {"claim": "MULTICOLUMN-2 v1, independent R1 audit",
              "assertion_rule": "C <= 2D; zero costs checked without division",
              "exhaustive": exhaustive_audit(),
              "direct_resource_profiles_checked": direct_formula_audit(),
              "larger_exact_integer_instances_checked": large_integer_audit(),
              "status": "PASS"}
    destination = Path(__file__).with_name("exact_test_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["exhaustive"]["totals"], ensure_ascii=False))
    print(f"direct formula profiles: {result['direct_resource_profiles_checked']}")
    print(f"larger instances: {result['larger_exact_integer_instances_checked']}")
    print(f"PASS: {destination}")


if __name__ == "__main__":
    main()
