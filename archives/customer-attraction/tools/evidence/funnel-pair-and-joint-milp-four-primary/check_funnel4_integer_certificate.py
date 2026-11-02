"""Exact independent integer-polynomial verification of the recovered n=4 certificate.

Reads the frozen floating support only; recovers each near-one multiplier as the
new exact integer 1. Does not import or execute the LP/MILP discovery programs.
"""
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
from itertools import product
import json
from pathlib import Path

SOURCE_SHA256 = '2729877b4f297c44861960412ee16973ee7b6c9642392c508058d6160b864193'
N, K = 4, 8


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return N if h[0] < N else 0
    group = range(N) if h[1] < N else range(N, K)
    return next(a for a in group if a not in h)


def finish(h):
    while len(h) < N:
        h += (action(h),)
    return h


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    obj = json.loads(raw, parse_float=Decimal)
    assert obj['players'] == N and obj['labels'] == K and obj['symbolic_background'] is True
    assert obj['kind'] == 'floating discovery only' and obj['general_half_proof'] is False
    root, bg_b, bg_c = finish(()), tuple(range(N-1)), (0,) + tuple(range(2, N))
    assert list(root) == obj['root'] == [0, 4, 5, 6]
    assert list(bg_b) == obj['B'] == [0, 1, 2]
    assert list(bg_c) == obj['C'] == [0, 2, 3]
    # Check that the rule is total on the full ordered decision tree; it remains
    # a formal policy until a customer instance supplies all of its SPE rows.
    policy = []
    for depth in range(N):
        for h in product(range(K), repeat=depth):
            a = action(h)
            assert 0 <= a < K and len(finish(h)) == N
            policy.append({'h': list(h), 'a': a})
    assert len(policy) == 585
    numerators = {0: [0]*N}
    for load in range(1, N+1):
        polynomial = [1]
        for j in range(1, N+1):
            if j != load:
                polynomial = multiply(polynomial, [j, 1])
        assert len(polynomial) == N
        numerators[load] = polynomial
    denominator = [1]
    for j in range(1, N+1):
        denominator = multiply(denominator, [j, 1])

    def row(topic, leaf, mask):
        assert topic in leaf
        if not (mask >> topic & 1):
            return [0]*N
        load = sum(mask >> a & 1 for a in leaf)
        assert 1 <= load <= N
        return numerators[load]

    def add(target, source, sign):
        return [x + sign*y for x, y in zip(target, source)]

    def gamma(h, alternative, mask):
        return add(row(action(h), finish(h), mask),
                   row(alternative, finish(h + (alternative,)), mask), -1)

    assert [q['a'] for q in obj['queries']] == list(range(K))
    query_results, recovered, distinct = [], [], set()
    coefficient_checks = 0
    largest_rounding_difference = Decimal(0)
    for query in obj['queries']:
        a = query['a']
        assert query['status'] == 0
        terms = []
        for entry in query['lambdas']:
            h, b = tuple(entry['h']), entry['a']
            assert len(h) in (0, 1, N-1)
            assert not h if len(h) == 0 else True
            assert h == (0,) if len(h) == 1 else True
            assert all(0 <= x < K for x in h) and 0 <= b < K and b != action(h)
            distance = abs(Decimal(entry['value']) - 1)
            assert distance < Decimal('1e-10')
            largest_rounding_difference = max(largest_rounding_difference, distance)
            terms.append((h, b))
            distinct.add((h, b))
        assert len(set(terms)) == len(terms)
        recovered.append({'query': a, 'terms': [{'h': list(h), 'a': b, 'coefficient': 1} for h,b in terms]})
        polynomials = []
        nonzero = []
        minimum = None
        for mask in range(1 << K):
            target = add(row(root[0], root, mask), row(root[1], root, mask), 1)
            target = add(target, row(a, bg_b+(a,), mask), -1)
            target = add(target, row(a, bg_c+(a,), mask), -1)
            remainder = target
            for h, b in terms:
                remainder = add(remainder, gamma(h, b, mask), -1)
            assert all(isinstance(x, int) and x >= 0 for x in remainder), (a, mask, remainder)
            coefficient_checks += N
            minimum = min(remainder) if minimum is None else min(minimum, *remainder)
            polynomials.append(remainder)
            if any(remainder):
                nonzero.append({'mask': mask, 'ascending_coefficients': remainder})
        assert polynomials[0] == [0]*N
        query_results.append({'query': a, 'multiplier_count': len(terms),
                              'interest_masks_including_empty': 256,
                              'zero_remainder_masks_including_empty': 256-len(nonzero),
                              'minimum_coefficient': minimum,
                              'nonzero_remainder_polynomials': nonzero})
    assert sum(x['multiplier_count'] for x in query_results) == 26
    assert coefficient_checks == 8192
    report = {
        'status': 'EXACT_RECOVERED_INTEGER_CERTIFICATE_PASSED',
        'source_sha256': SOURCE_SHA256,
        'recovery': 'All 26 recorded near-one values replaced by a NEW exact integer-one certificate; original floating values are not declared exact.',
        'largest_recorded_distance_from_one': str(largest_rounding_difference),
        'players': N, 'labels': K, 'root': root,
        'static_backgrounds': [bg_b, bg_c], 'static_probabilities': ['1/2', '1/2'],
        'formal_ordered_policy_histories': len(policy),
        'all_spe_incentives_with_self': len(policy)*K,
        'discovery_selected_incentive_rows': (1+1+K**(N-1))*(K-1),
        'recovered_multiplier_count': 26, 'distinct_incentive_rows_used': len(distinct),
        'coefficient_checks_including_empty_type': coefficient_checks,
        'coefficient_checks_nonempty_types': K*((1 << K)-1)*N,
        'denominator_ascending_coefficients': denominator,
        'numerator_ascending_coefficients': numerators,
        'minimum_remainder_coefficient': min(q['minimum_coefficient'] for q in query_results),
        'certificate': recovered, 'queries': query_results,
        'zero_remainders_not_listed': True,
        'scope': 'Fixed four-player/eight-label funnel policy, every query, arbitrary per-customer nonnegative background; proves v4(background) <= (u1+u2)/2 when that fixed complete policy is SPE. No universal policy/n-player/half conclusion.',
        'discovery_program_runs': 0, 'LP_or_MILP_runs': 0,
    }
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('certificate','queries','numerator_ascending_coefficients')}, indent=2))


if __name__ == '__main__':
    main()
