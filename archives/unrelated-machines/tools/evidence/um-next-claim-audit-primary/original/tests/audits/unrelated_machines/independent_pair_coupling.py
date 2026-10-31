"""Independent exact checks for subdivision and pair-config coupling.

Scratch audit: this is finite evidence, not a proof of universal assertions.
No repository import, random data, LP solver, floating-point arithmetic, or Git IO.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
import json


def optimum(machine_count, jobs):
    """jobs[e] is ((machine, rational_processing_time), ...)."""
    best = None
    for assignment in product(*(range(len(job)) for job in jobs)):
        loads = [Q(0) for _ in range(machine_count)]
        for job, choice in zip(jobs, assignment):
            i, p = job[choice]
            loads[i] += p
        value = max(loads, default=Q(0))
        if best is None or value < best:
            best = value
    return best


def subdivide(machine_count, jobs, H):
    assert H > 0
    new_jobs = []
    midpoint = machine_count
    for job in jobs:
        assert len(job) in (1, 2)
        if len(job) == 1:
            new_jobs.append(job)
        else:
            (u, a), (v, b) = job
            assert u != v
            new_jobs += [((u, a), (midpoint, H)),
                         ((v, b), (midpoint, H))]
            midpoint += 1
    return midpoint, new_jobs


def pair_coupling(mu, nu, shared):
    """mu/nu: dict[frozenset(job labels), positive rational mass]."""
    assert sum(mu.values()) == sum(nu.values()) == 1
    p = sum(w for S, w in mu.items() if shared in S)
    q = sum(w for S, w in nu.items() if shared in S)
    assert p + q == 1
    coupling = {}
    for S, a in mu.items():
        for R, b in nu.items():
            if (shared in S) == (shared in R):
                continue
            d = p if shared in S else 1-p
            assert d > 0
            coupling[S, R] = a*b/d
    assert sum(coupling.values()) == 1
    assert {S: sum(w for (A, B), w in coupling.items() if A == S)
            for S in mu} == mu
    assert {R: sum(w for (A, B), w in coupling.items() if B == R)
            for R in nu} == nu
    return coupling


def check_local_moment_cut(k):
    theta = Q(2*k-1, k)
    T0 = Q(k+1, k)
    # Terminal local distribution and old parent local distribution.
    mu = {(False, (1 << k)-1): 1-Q(1, k-1)}
    mu.update({(True, 1 << i): Q(1, k*(k-1)) for i in range(k)})
    nu = {1 << i: Q(1, k) for i in range(k)}
    assert sum(mu.values()) == sum(nu.values()) == 1
    for i in range(k):
        assert sum(w for (_, S), w in mu.items() if S >> i & 1) + sum(
            w for S, w in nu.items() if S >> i & 1) == 1
    old_residual = sum(w*comb(k-S.bit_count(), 2) for (_, S), w in mu.items())
    assert old_residual == Q(k-2, 2)
    assert sum(w*comb(S.bit_count(), 2) for S, w in nu.items()) == 0
    # Feasible local families change only at a + s/k (parent) or integer (leaf).
    breaks = sorted({Q(a)+Q(s, k) for a in (0, 1) for s in range(k+1)})
    tests = set(breaks)
    tests.update((a+b)/2 for a, b in zip(breaks, breaks[1:]))
    tested = 0
    for T in sorted(t for t in tests if 0 <= t < theta):
        for S in range(1 << k):
            if S.bit_count() <= T:
                assert comb(S.bit_count(), 2) == 0
            for incoming in (False, True):
                if Q(int(incoming))+Q(S.bit_count(), k) <= T:
                    if comb(k-S.bit_count(), 2) == 0:
                        assert not incoming
        tested += 1
    assert 1+Q(k-1, k) == theta
    assert T0 < theta
    return {'k': k, 'integer_threshold': str(theta),
            'old_T': str(T0), 'old_aggregate_residual': str(old_residual),
            'breakpoints_and_interiors_checked': tested}


def main():
    # Distinct nonnegative times, including zeros; these are exact assignments.
    inputs = []
    values = [Q(0), Q(1, 3), Q(1), Q(5, 3)]
    for a, b in product(values, repeat=2):
        for c, d in product(values, repeat=2):
            inputs.append((3, [((0, a), (1, b)), ((1, c), (2, d))]))
    inputs += [(2, [((0, Q(0)), (1, Q(7)))]),
               (2, [((0, Q(1, 97)), (1, Q(13, 101)))]),
               (3, [((0, Q(1)),), ((1, Q(1, 3)), (2, Q(4, 3)))]),
               (1, [])]
    H = Q(1)
    equality_cases = 0
    for m, jobs in inputs:
        old = optimum(m, jobs)
        new_m, new_jobs = subdivide(m, jobs, H)
        new = optimum(new_m, new_jobs)
        assert min(old, 2*H) <= new <= max(old, H)
        if H <= old <= 2*H:
            assert old == new
            equality_cases += 1
    # Boundary showing that original OPT < H does not imply equality.
    assert optimum(2, [((0, Q(0)), (1, Q(7)))]) == 0
    bad_m, bad_jobs = subdivide(2, [((0, Q(0)), (1, Q(7)))], H)
    assert optimum(bad_m, bad_jobs) == 1
    # Arbitrary singleton probabilities, including denominator and zero edges.
    shared = 'j'
    coupling_cases = 0
    for p in [Q(0), Q(1), Q(1, 97), Q(13, 101), Q(1, 2)]:
        mu = {}
        nu = {}
        for flag, event in [(True, p), (False, 1-p)]:
            if event:
                mu[frozenset(([shared] if flag else [])+['a'])] = event/3
                mu[frozenset(([shared] if flag else [])+['b'])] = 2*event/3
                nu[frozenset(([shared] if not flag else [])+['c'])] = event/5
                nu[frozenset(([shared] if not flag else [])+['d'])] = 4*event/5
        pair_coupling(mu, nu, shared)
        coupling_cases += 1
    print(json.dumps({'status': 'passed', 'arithmetic': 'fractions.Fraction',
                      'subdivision_instances_exhaustively_solved': len(inputs),
                      'equality_instances_H_le_OPT_le_2H': equality_cases,
                      'pair_coupling_cases': coupling_cases,
                      'local_moment_cut': [check_local_moment_cut(k)
                                           for k in range(4, 13)]}, indent=2))


if __name__ == '__main__':
    main()
