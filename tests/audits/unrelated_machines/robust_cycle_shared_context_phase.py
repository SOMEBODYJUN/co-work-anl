#!/usr/bin/env python3
"""Small exact boundary audit for robust cycles with a shared fixed context.

This enumerates only explicitly small instances. It is not an UM solver,
hardness reduction, or proof of the general theorem. All output is stdout JSON.
"""
from fractions import Fraction as Q
from itertools import product
import json


def core(name, home, successor):
    a, b = tuple(map(Q, home)), tuple(map(Q, successor))
    if len(a) < 2 or len(a) != len(b):
        raise ValueError('a core needs at least two machines and jobs')
    return {'name': name, 'machines': tuple(f'{name}{i}' for i in range(len(a))),
            'a': a, 'b': b}


def validate(c, T, B):
    if not 0 < T <= B < 2*T:
        raise ValueError('require 0 < T <= B < 2T')
    if any(not 0 <= w <= T for w in c['a'] + c['b']):
        raise ValueError('core times must lie in [0,T]')


def options(c):
    m = c['machines']
    return {f"{c['name']}j{i}": {m[i]: a, m[(i+1) % len(m)]: b}
            for i, (a, b) in enumerate(zip(c['a'], c['b']))}


def schedule(c, bits):
    m = c['machines']
    if len(bits) != len(m) or any(x not in (0, 1) for x in bits):
        raise ValueError('invalid orientation')
    return {f"{c['name']}j{i}": m[(i+x) % len(m)]
            for i, x in enumerate(bits)}


def loads(machines, jobs, assignment):
    if set(assignment) != set(jobs):
        raise ValueError('every original job must be assigned exactly once')
    out = dict.fromkeys(machines, Q(0))
    for j, destination in assignment.items():
        if destination not in out or destination not in jobs[j]:
            raise ValueError('assignment uses an unavailable original endpoint')
        time = jobs[j][destination]
        if time < 0:
            raise ValueError('negative original processing time')
        out[destination] += time
    return out


def peak(L):
    return max(L.values(), default=Q(0))


def encoded(L):
    return {str(i): str(w) for i, w in sorted(L.items())}


def audit_core(c, T, B):
    validate(c, T, B)
    n = len(c['machines'])
    collisions = [c['a'][i] + c['b'][i-1] for i in range(n)]
    predicted = all(w > B for w in collisions)
    feasible = []
    for bits in product((0, 1), repeat=n):
        L = loads(c['machines'], options(c), schedule(c, bits))
        if peak(L) <= B:
            feasible.append(bits)
    actual = set(feasible) == {(0,)*n, (1,)*n}
    assert actual == predicted
    witness = None
    if predicted:
        assert all(w > B-T for w in c['a'] + c['b'])
        assert all(abs(c['a'][i]-c['b'][i-1]) < 2*T-B for i in range(n))
    else:
        i = next(i for i, w in enumerate(collisions) if w <= B)
        bits = [0]*n
        bits[i-1] = 1
        L = loads(c['machines'], options(c), schedule(c, bits))
        assert len(set(bits)) == 2 and peak(L) <= B
        witness = {'bits': bits, 'loads': encoded(L)}
    return {'name': c['name'], 'T': str(T), 'B': str(B),
            'orientation_count': 2**n, 'weak_feasible_count': len(feasible),
            'collisions': list(map(str, collisions)), 'robust': predicted,
            'nonrobust_single_flip': witness}


def audit_shared_context():
    T, B = Q(1), Q(3, 2)
    ca = core('A', [1, Q(3, 5)], [1, Q(3, 5)])
    cb = core('B', [Q(3, 5), Q(9, 10), Q(4, 5)],
              [Q(4, 5), Q(4, 5), 1])
    cores = (ca, cb)
    for c in cores:
        assert audit_core(c, T, B)['robust']
    machines = ca['machines'] + cb['machines'] + ('X',)
    assert len(machines) == len(set(machines))
    context = {
        'c0': {'A0': Q(1, 4), 'B0': Q(3, 8), 'X': Q(7, 3)},
        'c1': {'B0': Q(1, 3), 'A0': Q(1, 5), 'X': Q(0)},
        'c2': {'B1': Q(1, 10), 'A1': Q(1, 11)},
        'c3': {'B2': Q(1, 5), 'A0': Q(1, 7)},
        'c4': {'X': Q(1), 'A0': Q(2, 5), 'B0': Q(1, 4)},
        'c5': {'A1': Q(0), 'B2': Q(0)},
    }
    fixed = {'c0': 'A0', 'c1': 'B0', 'c2': 'B1',
             'c3': 'B2', 'c4': 'X', 'c5': 'A1'}
    jobs = {**options(ca), **options(cb), **context}
    sigma = {**schedule(ca, (1, 1)), **schedule(cb, (0, 0, 0)), **fixed}
    initial = loads(machines, jobs, sigma)
    assert peak(initial) <= T
    targets = []
    for theta in product((0, 1), repeat=2):
        tau = {**schedule(ca, (theta[0],)*2),
               **schedule(cb, (theta[1],)*3), **fixed}
        L = loads(machines, jobs, tau)
        assert all(tau[j] == sigma[j] for j in context)
        assert L['X'] == initial['X']
        assert peak(L) < 3*T-B <= B
        targets.append({'theta': list(theta), 'loads': encoded(L)})
    weak_patterns = []
    for bits in product((0, 1), repeat=5):
        tau = {**schedule(ca, bits[:2]), **schedule(cb, bits[2:]), **fixed}
        if peak(loads(machines, jobs, tau)) <= B:
            assert len(set(bits[:2])) == len(set(bits[2:])) == 1
            weak_patterns.append(list(bits))
    assert len(weak_patterns) == 4
    return {'T': str(T), 'B': str(B), 'original_job_count': len(jobs),
            'machine_count': len(machines), 'initial_loads': encoded(initial),
            'all_core_orientations_checked': 32,
            'weak_core_patterns': weak_patterns, 'targets': targets}


def audit_two_machine_family(T, B, d):
    c = core('S', [T, d], [T, d])
    check = audit_core(c, T, B)
    assert check['robust']
    jobs = {**options(c), 'f': {'S0': T-d}}
    strict = {**schedule(c, (1, 1)), 'f': 'S0'}
    other = {**schedule(c, (0, 0)), 'f': 'S0'}
    initial = loads(c['machines'], jobs, strict)
    target = loads(c['machines'], jobs, other)
    assert peak(initial) == T
    assert peak(target) == 2*T-d < 3*T-B
    # Check all four original-job orientations with this fixed real context.
    fixed_context_profiles = []
    for bits in product((0, 1), repeat=2):
        L = loads(c['machines'], jobs, {**schedule(c, bits), 'f': 'S0'})
        fixed_context_profiles.append({'bits': list(bits), 'peak': str(peak(L))})
    return {'T': str(T), 'B': str(B), 'd': str(d),
            'initial_loads': encoded(initial), 'target_loads': encoded(target),
            'strict_envelope': str(3*T-B),
            'fixed_context_all_orientations': fixed_context_profiles}


def audit_overlap_outside_domain():
    T, B = Q(1), Q(6, 5)
    # The two cores intentionally reuse M; this is outside the theorem domain.
    c1 = {'name': 'O1', 'machines': ('M', 'N1'),
          'a': (Q(3, 10), Q(9, 10)), 'b': (Q(9, 10), Q(19, 20))}
    c2 = {'name': 'O2', 'machines': ('M', 'N2'),
          'a': (Q(3, 10), Q(9, 10)), 'b': (Q(9, 10), Q(19, 20))}
    assert audit_core(c1, T, B)['robust']
    assert audit_core(c2, T, B)['robust']
    jobs = {**options(c1), **options(c2), 'f': {'M': Q(2, 5)}}
    sigma = {**schedule(c1, (0, 0)), **schedule(c2, (0, 0)), 'f': 'M'}
    tau = {**schedule(c1, (1, 1)), **schedule(c2, (1, 1)), 'f': 'M'}
    old = loads(('M', 'N1', 'N2'), jobs, sigma)
    new = loads(('M', 'N1', 'N2'), jobs, tau)
    assert peak(old) == 1 and peak(new) == Q(23, 10) > 3*T-B
    return {'outside_domain': 'core machines overlap',
            'initial_loads': encoded(old), 'target_loads': encoded(new),
            'inapplicable_envelope': str(3*T-B)}


def main():
    D = 2**62
    cases = [
        (core('lower_boundary', [1, Q(1, 2)], [1, Q(1, 2)]), Q(1), Q(1)),
        (core('one_equality_collision', [Q(3, 4), 1, 1], [1, 1, Q(3, 4)]),
         Q(1), Q(3, 2)),
        (core('above_equality', [Q(19, 25)]*3, [Q(19, 25)]*3), Q(1), Q(3, 2)),
        (core('four_cycle', [1, Q(7, 8), Q(15, 16), 1], [1]*4), Q(1), Q(7, 4)),
        (core('zero_time_nonrobust', [0, 1], [1, 1]), Q(1), Q(1)),
        (core('scaled_rational', [Q(3, 7)]*2, [Q(3, 7)]*2), Q(3, 7), Q(11, 14)),
        (core('large_denominator', [Q(1)]*2, [Q(D-2, D)]*2), Q(1), Q(2*D-4, D)),
    ]
    local = [audit_core(*case) for case in cases]
    sharp = []
    for T in (Q(1), Q(3, 7)):
        for factor in (Q(1), Q(4, 3), Q(149, 100)):
            B = factor*T
            row = audit_two_machine_family(T, B, T/2)
            assert Q(3, 2)*T > B
            assert max(map(Q, row['target_loads'].values())) == Q(3, 2)*T
            sharp.append(row)
    envelope = []
    for T in (Q(1), Q(3, 7)):
        for factor in (Q(1), Q(3, 2), Q(7, 4), Q(2)-Q(1, 2**20)):
            B = factor*T
            e = (2*T-B)/3
            d = B-T+e
            row = audit_two_machine_family(T, B, d)
            row['e'] = str(e)
            assert max(map(Q, row['target_loads'].values())) == 3*T-B-e
            envelope.append(row)
    # At B=3T/2 the sharp-C core itself is no longer robust: equality matters.
    equality = audit_core(core('sharp_threshold_equality', [1, Q(1, 2)],
                               [1, Q(1, 2)]), Q(1), Q(3, 2))
    assert not equality['robust']
    print(json.dumps({
        'claim_id': 'UM-ROBUST-CYCLE-SHARED-CONTEXT-PHASE-v1',
        'scope': 'finite exact audit; not a general UM solver or hardness proof',
        'arithmetic': 'fractions.Fraction; no floating point',
        'local_orientation_cases': local,
        'shared_context': audit_shared_context(),
        'three_halves_sharp_cases': sharp,
        'strict_envelope_cases': envelope,
        'threshold_equality': equality,
        'machine_overlap_domain_counterexample': audit_overlap_outside_domain(),
        'all_assertions_passed': True,
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
