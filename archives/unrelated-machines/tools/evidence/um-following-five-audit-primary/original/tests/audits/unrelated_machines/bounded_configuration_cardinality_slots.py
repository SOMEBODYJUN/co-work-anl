#!/usr/bin/env python3
"""Exact finite certificates for bounded-cardinality configuration slot envelopes."""
from fractions import Fraction as Q
import json
import hashlib
import platform
from pathlib import Path


def make_case(K):
    eta = Q(1, 100)
    p = {'B': Q(1)}
    if K == 2:
        p.update({f'A{j}': Q(1, 2) for j in range(2)})
        configs = [(('A0', 'A1'), Q(1))]
    elif K == 3:
        p.update({f'A{j}': Q(1, 2) for j in range(2)})
        p.update({f'C{j}': Q(1, 3) for j in range(3)})
        configs = [(('A0', 'A1'), Q(2, 3)),
                   (('C0', 'C1', 'C2'), Q(1, 3))]
    elif K == 4:
        p.update({f'A{j}': Q(3, 8) for j in range(2)})
        p.update({f'C{j}': Q(1, 3) for j in range(3)})
        p.update({f'D{j}': Q(1, 4) for j in range(4)})
        configs = [(('A0', 'A1', 'D0'), Q(5, 9)),
                   (('C0', 'C1', 'C2'), Q(1, 3)),
                   (('D0', 'D1', 'D2', 'D3'), Q(1, 9))]
    else:
        raise ValueError(K)
    configs = [(('B',), eta)] + [(s, w * (1 - eta)) for s, w in configs]
    assert sum(w for _, w in configs) == 1
    assert all(len(s) <= K and sum(p[j] for j in s) <= 1 for s, _ in configs)
    x = {j: sum(w for s, w in configs if j in s) for j in p}
    assert all(0 < v < 1 for v in x.values())
    order = sorted(p, key=lambda j: (-p[j], j))
    pos = Q(0)
    intervals = {}
    for j in order:
        intervals[j] = (pos, pos + x[j])
        pos += x[j]
    slots = (pos.numerator + pos.denominator - 1) // pos.denominator
    maxima, selected = [], []
    for s in range(slots):
        adj = [j for j in order if max(Q(s), intervals[j][0]) <
               min(Q(s + 1), intervals[j][1])]
        assert adj
        j = max(adj, key=lambda j: p[j])
        maxima.append(p[j])
        selected.append(j)
    assert len(set(selected)) == slots
    # Every other job uses its own private machine, where it has size 1.
    # Its fractional mass is 1-x[j], leaving one available private slot.
    matching = {j: ('central', selected.index(j)) if j in selected
                else (f'private_{j}', 0) for j in p}
    assert len(set(matching.values())) == len(p)
    for j, (m, s) in matching.items():
        if m == 'central':
            assert max(Q(s), intervals[j][0]) < min(Q(s + 1), intervals[j][1])
        else:
            assert 1 - x[j] > 0
    rowload = sum(p[j] for j in selected)
    envelope = sum(maxima)
    assert rowload == envelope
    expected = {2: Q(3, 2), 3: Q(11, 6), 4: Q(47, 24)}[K]
    assert envelope == expected
    # All-private is a schedule of makespan 1. B has size 1 everywhere eligible.
    opt = Q(1)
    assert rowload > opt
    return {'K': K, 'T': '1', 'OPT': str(opt),
            'central_slot_maxima': [str(t) for t in maxima],
            'central_envelope': str(envelope), 'actual_matching_load': str(rowload),
            'central_selected_jobs': selected,
            'total_jobs': len(p), 'total_machines': len(p) + 1,
            'central_configs': [{'jobs': list(s), 'weight': str(w)} for s, w in configs],
            'central_marginals': {j: str(x[j]) for j in p},
            'coverage_equal_one': True, 'matching_verified': True}


if __name__ == '__main__':
    print(json.dumps({'arithmetic': 'fractions.Fraction; no sampling', 'python_version': platform.python_version(), 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'command': 'python3 tests/audits/unrelated_machines/bounded_configuration_cardinality_slots.py', 'cases': [make_case(k) for k in (2, 3, 4)], 'limit': 'Only explicit low-K full instances and matching certificates; no generic LP implementation or sharp K4 claim.'}, indent=2))
