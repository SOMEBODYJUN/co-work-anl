#!/usr/bin/env python3
"""Independent finite actual-schedule oracle for a three-host interpolation.

The independent optimum core never imports a proof implementation or a
Santa Claus/configuration core.  audit() separately imports the normative
constructor AS THE OBJECT UNDER TEST and directly checks its actual sigma.
Rows below are ORIGINAL finite-eligibility job matrices.  The three host IDs
can be arbitrary.  A profile adds three actual fixed pin jobs (0 at free
hosts, T elsewhere).  Exact enumeration is a finite audit, not the algorithm.
"""
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import sys


def all_actual_schedules(machines, jobs):
    """Enumerate all original eligible assignments and independently sum load."""
    assert machines >= 3
    assert all(row and all(0 <= i < machines and p >= 0 for i, p in row.items())
               for row in jobs)
    for sigma in product(*(tuple(sorted(row)) for row in jobs)):
        loads = [0] * machines
        for row, owner in zip(jobs, sigma):
            loads[owner] += row[owner]
        yield sigma, tuple(loads)


def profile_preloads(machines, T, profile, hosts=None):
    a, b, c = hosts if hosts is not None else range(machines - 3, machines)
    assert len({a, b, c}) == 3 and all(0 <= i < machines for i in (a, b, c))
    free = {'a': {a}, 'bc': {b, c}, 'b': {b}, 'c': {c}}[profile]
    return tuple(T if i in (a, b, c) and i not in free else 0 for i in range(machines))


def classify(machines, jobs, T, hosts=None):
    """Find exact four-profile OPTs and two actual YES witnesses, if present."""
    preloads = {s: profile_preloads(machines, T, s, hosts) for s in ('a', 'bc', 'b', 'c')}
    optima = {s: None for s in preloads}
    first_yes = {'a': None, 'bc': None}
    last_yes = dict(first_yes)
    count = 0
    for sigma, base in all_actual_schedules(machines, jobs):
        count += 1
        for profile, pins in preloads.items():
            value = max(x + y for x, y in zip(base, pins))
            if optima[profile] is None or value < optima[profile]:
                optima[profile] = value
            if profile in first_yes and value <= T:
                if first_yes[profile] is None:
                    first_yes[profile] = sigma
                last_yes[profile] = sigma
    return {'optima': optima, 'first_yes': first_yes,
            'last_yes': last_yes, 'complete_assignments': count}


def verify_actual_output(machines, jobs, T, out, hosts=None):
    """Check a proposed full schedule against ORIGINAL jobs and actual pin jobs."""
    hosts = tuple(hosts if hosts is not None else range(machines - 3, machines))
    a, b, c = hosts
    assert out['free_host'] in (b, c)
    profile = 'b' if out['free_host'] == b else 'c'
    base_sigma = tuple(out['sigma'])
    assert len(base_sigma) == len(jobs)
    pins = hosts
    # The normative object outputs sigma of all original base jobs and the
    # profile.  Complete it with three explicit, singleton-eligible pin jobs.
    full_assignment = base_sigma + pins
    assert len(full_assignment) == len(jobs) + 3
    loads = [Fraction(0)] * machines
    for row, owner in zip(jobs, base_sigma):
        assert type(owner) is int and 0 <= owner < machines
        assert owner in row
        loads[owner] += row[owner]
    pin_values = [0 if owner == out['free_host'] else T for owner in pins]
    for owner, value in zip(pins, pin_values):
        loads[owner] += value
    assert max(loads) <= Fraction(3, 2) * T
    assert [Fraction(v) for v in out['loads']] == loads
    assert [Fraction(v) for v in out['preloads']] == list(profile_preloads(machines, T, profile, hosts))
    original_task_loads = [Fraction(0)] * machines
    for row, owner in zip(jobs, base_sigma):
        original_task_loads[owner] += row[owner]
    assert original_task_loads == [Fraction(v) for v in out['task_loads']]
    return loads


def audit():
    # Import is only the constructor being tested.  None of the independent
    # enumeration, objective, witness search or load checks use its helpers.
    normative_path = Path(__file__).with_name('three_host_majority_selector.py')
    name = 'independent_optimum_normative_object_under_test'
    spec = importlib.util.spec_from_file_location(name, normative_path)
    normative = importlib.util.module_from_spec(spec)
    sys.modules[name] = normative
    spec.loader.exec_module(normative)

    def solver(machines, jobs, T, yes_a, yes_bc, hosts=None):
        a, b, c = hosts if hosts is not None else range(machines - 3, machines)
        p = [[row.get(i) for row in jobs] for i in range(machines)]
        return normative.construct_three_host_selector(p, list(yes_a), list(yes_bc), T, a, b, c)

    counts = {'exhaustive_original_matrices': 0,
              'exhaustive_complete_assignments': 0,
              'exhaustive_two_yes': 0,
              'exhaustive_sharp': 0,
              'random_original_matrices': 0,
              'random_complete_assignments': 0,
              'random_two_yes': 0,
              'random_nonstandard_host_inputs': 0,
              'random_nonstandard_host_two_yes': 0,
              'normative_actual_outputs_checked': 0,
              'boundary_cases': 0}
    boundary_certificates = []

    def record_boundary(machines, jobs, T, yes_a, yes_bc, hosts=None, sharp=False):
        hosts = tuple(hosts if hosts is not None else range(machines - 3, machines))
        result = classify(machines, jobs, T, hosts)
        out = solver(machines, jobs, T, yes_a, yes_bc, hosts)
        loads = verify_actual_output(machines, jobs, T, out, hosts)
        counts['boundary_cases'] += 1
        counts['normative_actual_outputs_checked'] += 1
        assert min(result['optima']['b'], result['optima']['c']) <= Fraction(3, 2) * T
        if sharp:
            assert result['optima']['b'] == result['optima']['c'] == Fraction(3, 2) * T
        boundary_certificates.append({
            'machines': machines, 'hosts': hosts, 'T': T, 'original_jobs': jobs,
            'actual_yes_a': yes_a, 'actual_yes_bc': yes_bc,
            'free_host': out['free_host'], 'full_assignment': list(out['sigma']) + list(hosts),
            'pin_jobs': [{i: 0 if i == out['free_host'] else T} for i in hosts],
            'actual_full_loads': loads,
            'exact_bad_profile_optima': {s: result['optima'][s] for s in ('b', 'c')},
            'eligible_base_assignments': result['complete_assignments'],
            'is_sharp': sharp})
    # Units T=2 permit integer exact arithmetic and nontrivial zero edges.
    # None is unavailable.  Job order is canonical; all 0..3 job multisets
    # cover every original 3-machine shape up to permuting job identities.
    rows = [dict((i, p) for i, p in enumerate(row) if p is not None)
            for row in product((None, 0, 1, 2), repeat=3) if any(p is not None for p in row)]
    for n in range(4):
        for indices in combinations_with_replacement(range(len(rows)), n):
            jobs = [rows[j] for j in indices]
            result = classify(3, jobs, 2)
            counts['exhaustive_original_matrices'] += 1
            counts['exhaustive_complete_assignments'] += result['complete_assignments']
            yes = result['first_yes']
            if yes['a'] is None or yes['bc'] is None:
                continue
            counts['exhaustive_two_yes'] += 1
            value = min(result['optima']['b'], result['optima']['c'])
            assert value <= 3
            counts['exhaustive_sharp'] += value == 3
            out = solver(3, jobs, 2, yes['a'], yes['bc'])
            verify_actual_output(3, jobs, 2, out)
            counts['normative_actual_outputs_checked'] += 1
    rng = random.Random(2026101841)
    for _ in range(1200):
        machines = rng.randrange(3, 7)
        n = rng.randrange(7)
        hosts = tuple(rng.sample(range(machines), 3))
        counts['random_nonstandard_host_inputs'] += hosts != tuple(range(machines - 3, machines))
        T = rng.choice([Fraction(0), Fraction(1), Fraction(7, 11), Fraction(3, 2)])
        jobs = []
        for j in range(n):
            eligible = [i for i in range(machines) if rng.randrange(3)]
            if not eligible:
                eligible = [rng.randrange(machines)]
            jobs.append({i: Fraction(rng.randrange(5), rng.randrange(1, 5)) * T
                         for i in eligible})
        result = classify(machines, jobs, T, hosts)
        counts['random_original_matrices'] += 1
        counts['random_complete_assignments'] += result['complete_assignments']
        yes = result['first_yes']
        if yes['a'] is None or yes['bc'] is None:
            continue
        counts['random_two_yes'] += 1
        counts['random_nonstandard_host_two_yes'] += hosts != tuple(range(machines - 3, machines))
        assert min(result['optima']['b'], result['optima']['c']) <= Fraction(3, 2) * T
        for witnesses in (result['first_yes'], result['last_yes']):
            out = solver(machines, jobs, T, witnesses['a'], witnesses['bc'], hosts)
            verify_actual_output(machines, jobs, T, out, hosts)
            counts['normative_actual_outputs_checked'] += 1
    for T in (Fraction(1), Fraction(7, 11), Fraction(1, 2**127 - 1)):
        jobs = [{0: T / 2, 1: T}, {0: T / 2, 2: T}]
        result = classify(3, jobs, T)
        assert result['optima']['a'] == result['optima']['bc'] == T
        assert result['optima']['b'] == result['optima']['c'] == Fraction(3, 2) * T
        record_boundary(3, jobs, T, (0, 0), (1, 2), sharp=True)
    record_boundary(3, [], Fraction(1), (), ())
    record_boundary(3, [], Fraction(0), (), ())
    record_boundary(4, [{0: Fraction(1)}], Fraction(1), (0,), (0,), hosts=(3, 1, 2))
    record_boundary(4, [{0: Fraction(3, 7)}, {1: Fraction(0)}],
                    Fraction(1), (0, 1), (0, 1), hosts=(3, 1, 2))
    record_boundary(3, [{0: Fraction(0)}, {2: Fraction(0)}],
                    Fraction(0), (0, 2), (0, 2))
    record_boundary(4, [{0: Fraction(0), 1: Fraction(3, 2), 3: Fraction(5)}],
                    Fraction(0), (0,), (0,), hosts=(1, 2, 3))
    return {'status': 'pass', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'counts': counts,
            'normative_source_sha256': hashlib.sha256(normative_path.read_bytes()).hexdigest(),
            'boundary_certificates': boundary_certificates,
            'scope': 'finite exact ORIGINAL full matrices plus actual fixed pin jobs; normative imported only as object under test; independent OPT core has no normative helper calls; exhaustive jobs up to identity permutation',
            'seed': 2026101841}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True, default=str))
