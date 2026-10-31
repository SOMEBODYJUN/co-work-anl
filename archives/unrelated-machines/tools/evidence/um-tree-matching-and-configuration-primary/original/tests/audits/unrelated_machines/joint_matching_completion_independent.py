#!/usr/bin/env python3
"""独立核验唯一小端选择归约与条件块割。

This finite audit is not a general NP-hardness proof or a universal scheduling
algorithm.  Source instances and actual scheduling states are enumerated by
separate methods.  Arithmetic is integer/Fraction only, no LP package.
"""
from fractions import Fraction as F
from itertools import combinations, product
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import platform


def triple_reduction(q, triples):
    """No-pin reduction; times are in units 1/3 (small=1,big=3)."""
    assert q >= 0
    assert all(len(set(t)) == 3 and all(0 <= e < 3*q for e in t)
               for t in triples)
    source = 0
    set_machines = list(range(1, len(triples)+1))
    element_base = len(triples)+1
    jobs = [{source: 1, **{i: 3 for i in set_machines}}
            for _ in range(q+3)]
    for i, triple in zip(set_machines, triples):
        jobs.extend({i: 1, element_base+e: 3} for e in triple)
    assert all(sum(p == 1 for p in times.values()) == 1 for times in jobs)
    return jobs, 1+len(triples)+3*q


def source_exact_cover(q, triples):
    for chosen in combinations(triples, q):
        flat = [e for triple in chosen for e in triple]
        if len(flat) == len(set(flat)) == 3*q:
            return True
    return False


def scheduling_oracle(jobs, m, capacity=F(3)):
    """Exhaustive memoized assignment search at exact target 3 units.

    It knows only jobs, machine choices and residual capacities; no exact-cover
    or triggered-set deductions are used. Sorting selectors first yields memo
    reuse because they have identical processing vectors.
    """
    tasks = tuple(tuple(sorted(times.items())) for times in jobs)
    visited = 0

    @lru_cache(None)
    def possible(index, remaining):
        nonlocal visited
        visited += 1
        if index == len(tasks):
            return True
        for i, p in tasks[index]:
            if remaining[i] >= p:
                residual = list(remaining)
                residual[i] -= p
                if possible(index+1, tuple(residual)):
                    return True
        return False

    return possible(0, (capacity,)*m), lambda: visited


def audit_reduction():
    counts = []
    for q in (0, 1, 2):
        triples = list(product(range(q), repeat=3))
        # Tag the three source coordinates so every triple has distinct items.
        universe_triples = [(a, q+b, 2*q+c) for a, b, c in triples]
        checked = yes = search_states = delta_checks = 0
        for mask in range(1 << len(universe_triples)):
            family = [t for i, t in enumerate(universe_triples) if mask & (1 << i)]
            source = source_exact_cover(q, family)
            jobs, m = triple_reduction(q, family)
            target, states = scheduling_oracle(jobs, m)
            assert source == target, (q, family, source, target)
            checked += 1
            yes += source
            search_states += states()
            for delta in (F(1, 6), F(1, 3)-F(1, 10**60+7)):
                relaxed, extra_states = scheduling_oracle(jobs, m, 3*(1+delta))
                assert relaxed == source
                delta_checks += 1
        counts.append(dict(q=q, all_tripartite_triples=len(universe_triples),
                           family_instances=checked, yes_instances=yes,
                           positive_delta_queries=delta_checks,
                           independent_schedule_search_states=search_states))
    # Boundary delta=1/3 is outside the reduction's range.
    jobs, m = triple_reduction(1, [])
    assert not source_exact_cover(1, [])
    boundary, _ = scheduling_oracle(jobs, m, F(4))
    assert boundary
    return counts


def audit_given_witness_rounding(production):
    checked = []
    for T in (F(1), F(1, 2**257+1), F(0)):
        delta = F(1, 8)
        if T:
            p = [[3*T/4]+[T/2]*3, [None]+[T/2]*3]
            H = {0: 0}
            x = [[F(0)]+[F(1, 4)]*3, [F(0)]+[F(3, 4)]*3]
        else:
            p = [[F(0)]*3, [F(0)]*3]
            H = {}
            x = [[F(1, 4)]*3, [F(3, 4)]*3]
        assignment, returned_loads = production.round_interface(p, T, H, x, delta)
        n = len(p[0])
        assert len(assignment) == n and all(assignment[j] == i for j, i in H.items())
        actual = [sum((p[i][j] for j in range(n) if assignment[j] == i), F(0))
                  for i in range(len(p))]
        assert actual == returned_loads
        assert all(value <= (F(3, 2)+delta)*T for value in actual)
        checked.append(dict(T=str(T), delta=str(delta), loads=list(map(str, actual))))
    assignment, loads = production.round_interface([[]], F(0), {}, [[]], F(1, 3))
    assert assignment == [] and loads == [F(0)]
    return dict(exact_fractional_cases=checked, empty_task_case=True)


def path_terminal_oracle(k, star_occupied, escaped_reserves):
    """Actual orientation enumeration for the nonescaped reserve path."""
    remaining = [e for e in range(k-1) if e not in escaped_reserves]
    for directions in product((0, 1), repeat=len(remaining)):
        load = [int(i in star_occupied) for i in range(k)]
        for edge, direction in zip(remaining, directions):
            load[edge+direction] += 1
        if max(load, default=0) <= 1:
            return True
    return False


def audit_conditional_cuts():
    expanded = []
    for k in range(2, 7):
        cases = 0
        for occupied_mask in range(1 << k):
            occupied = {i for i in range(k) if occupied_mask & (1 << i)}
            minimum = None
            for escape_mask in range(1 << (k-1)):
                escaped = {i for i in range(k-1) if escape_mask & (1 << i)}
                feasible = path_terminal_oracle(k, occupied, escaped)
                if feasible:
                    minimum = len(escaped) if minimum is None else min(minimum, len(escaped))
                    assert len(escaped) >= max(len(occupied)-1, 0)
                cases += 1
            assert minimum == max(len(occupied)-1, 0)
        expanded.append(dict(k=k, star_escape_patterns=cases))
    algebra = []
    for k in (4, 5, 8, 16, 32, 64):
        h, alpha = 1, F(1, k-1)
        while alpha < F(1, 2):
            h += 1
            alpha *= F(k, k-1)
        theta = 2-F(1, k)
        checked = 0
        # Each floor-constant interval, both its left boundary and midpoint.
        # These cover all possible r_B values below theta, not all rationals.
        for a in range(k-1):
            for B in (1+F(a, k), 1+F(2*a+1, 2*k)):
                assert 1 <= B < theta
                r = k-(k*(B-1)).numerator//(k*(B-1)).denominator
                assert 2 <= r <= k
                # Verify the local configuration row for all actual subsets,
                # compressed only by their number of small jobs.
                for incoming in (0, 1):
                    for kept in range(k+1):
                        if incoming+F(kept, k) <= B:
                            assert kept <= k-r*incoming
                            if incoming:
                                assert k-kept >= r
                bottom_mass = r**(h-1)
                lower_z = F((r-1)*bottom_mass, 2)
                assert lower_z >= 2 > B
                checked += 1
        # At theta the relevant coefficient becomes zero. The stronger T0
        # coefficient must not be frozen and incorrectly reused at theta.
        rtheta = k-(k*(theta-1)).numerator//(k*(theta-1)).denominator
        assert rtheta == 1
        algebra.append(dict(k=k, height=h, threshold=str(theta),
                            floor_interval_samples=checked,
                            r_at_threshold=rtheta))
    return dict(path_orientation_enumeration=expanded, exact_interval_checks=algebra)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', type=Path,
                        default=Path(__file__).with_name('joint_matching_completion.py'))
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('joint_completion_production', args.module)
    production = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(production)
    print(json.dumps(dict(python=platform.python_version(),
                          arithmetic='integer units / fractions.Fraction',
                          source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          tested_rounding_sha256=hashlib.sha256(args.module.read_bytes()).hexdigest(),
                          reduction=audit_reduction(),
                          conditional_rounding=audit_given_witness_rounding(production),
                          block_cuts=audit_conditional_cuts(),
                          limits=['Finite reduction tests do not prove NP-completeness.',
                                  'Path orientation tests are local, not general scheduling enumeration.',
                                  'Interval algebra is specific to the recognized shared-z family.']), indent=2))


if __name__ == '__main__':
    main()
