"""Independent exact audit of repeated minimal-overload contraction.

No import of the proposed implementation; sampled matrices are checked with
complete schedule enumeration. This is finite evidence, not a general proof.
"""
from fractions import Fraction as Q
from itertools import product
from random import Random
import hashlib
import json
import platform
from pathlib import Path


def all_assignments(machines, jobs, times):
    options = [[i for i in machines if (i, j) in times] for j in jobs]
    for owners in product(*options):
        assignment = dict(zip(jobs, owners))
        loads = {i: Q(0) for i in machines}
        for j, i in assignment.items():
            loads[i] += times[i, j]
        yield assignment, max(loads.values(), default=Q(0))


def reduce_all(m, n, times, T):
    machines, jobs = list(range(m)), list(range(n))
    times = {edge: p for edge, p in times.items() if p <= T}
    records = []
    if any(not any((i, j) in times for i in machines) for j in jobs):
        return None, records, 'initial_empty_domain'
    while True:
        chosen = None
        for v in machines:
            F = [j for j in jobs if (v, j) in times]
            S = sum((times[v, j] for j in F), Q(0))
            if S > T and all(S-times[v, j] <= T for j in F):
                chosen = v, F
                break
        if chosen is None:
            return (machines, jobs, times), records, 'fixed_point'
        v, F = chosen
        assert len(F) >= 2 and all(times[v, j] > 0 for j in F)
        e = n + len(records)
        remaining = [i for i in machines if i != v]
        witnesses = {}
        new_times = {(i, j): p for (i, j), p in times.items()
                     if i != v and j not in F}
        for i in remaining:
            candidates = [j for j in F if (i, j) in times]
            if candidates:
                a = min(candidates, key=lambda j: (times[i, j], j))
                witnesses[i] = a
                new_times[i, e] = times[i, a]
        records.append((v, tuple(F), e, witnesses))
        if not witnesses:
            return None, records, 'contracted_empty_domain'
        machines = remaining
        jobs = [j for j in jobs if j not in F] + [e]
        times = new_times
        assert len(records) <= m


def lift(assignment, records):
    assignment = dict(assignment)
    for v, children, e, witnesses in reversed(records):
        i = assignment.pop(e)
        a = witnesses[i]
        assignment.update({j: (i if j == a else v) for j in children})
    return assignment


def main():
    rng = Random(918273)
    values = [None, Q(0), Q(1, 97), Q(1, 3), Q(2, 3), Q(1), Q(4, 3)]
    fixtures = []
    for _ in range(1200):
        m, n = rng.randrange(1, 5), rng.randrange(6)
        T = rng.choice([Q(0), Q(1, 2), Q(1), Q(7, 6)])
        times = {}
        for i in range(m):
            for j in range(n):
                p = rng.choice(values)
                if p is not None:
                    times[i, j] = p
        # Include only legal input matrices.
        if all(any((i, j) in times for i in range(m)) for j in range(n)):
            fixtures.append((m, n, times, T))
    # A forced nested replacement: after deleting machine 0, its representative
    # plus job 2 form a minimal overload on machine 1, then both are restored.
    fixtures.append((3, 3, {(0, 0): Q(2, 3), (0, 1): Q(2, 3),
                           (1, 0): Q(2, 3), (1, 1): Q(2, 3),
                           (1, 2): Q(2, 3), (2, 0): Q(1),
                           (2, 1): Q(1), (2, 2): Q(1)}, Q(1)))
    lifts = contractions = rejected = nested = nested_lifts = 0
    for m, n, original, T in fixtures:
        feasible = any(B <= T for _, B in all_assignments(range(m), range(n), original))
        residual, records, status = reduce_all(m, n, original, T)
        contractions += len(records)
        if residual is None:
            assert not feasible
            rejected += 1
            continue
        machines, jobs, times = residual
        schedules = list(all_assignments(machines, jobs, times))
        assert feasible == any(B <= T for _, B in schedules)
        is_nested = any(any(j >= n for j in children)
                        for _, children, _, _ in records)
        nested += is_nested
        for assignment, B in schedules:
            restored = lift(assignment, records)
            assert set(restored) == set(range(n))
            loads = [Q(0) for _ in range(m)]
            for j, i in restored.items():
                assert (i, j) in original
                loads[i] += original[i, j]
            assert max(loads) <= max(B, T)
            lifts += 1
            nested_lifts += is_nested
    assert nested > 0 and nested_lifts > 0
    print(json.dumps({'status': 'passed', 'python': platform.python_version(),
                      'arithmetic': 'fractions.Fraction; exact',
                      'seed': 918273, 'legal_fixtures': len(fixtures),
                      'contractions': contractions, 'rejected_fixtures': rejected,
                      'residual_schedules_lifted': lifts,
                      'nested_residual_fixtures': nested,
                      'nested_schedules_lifted': nested_lifts,
                      'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'limits': 'finite sampled legal matrices, every schedule per fixture; not proof'},
                     indent=2))


if __name__ == '__main__':
    main()
