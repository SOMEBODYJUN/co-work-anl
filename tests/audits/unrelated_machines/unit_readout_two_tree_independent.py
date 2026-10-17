#!/usr/bin/env python3
"""Read full actual matrices/certificates; never import their generator."""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import hashlib
import json

PATH = Path(__file__).resolve().parents[3] / 'examples/unrelated_machines/unit_readout_two_tree_actual_certificates.json'


def check(jobs, sigma, machines, expected):
    assert len(jobs) == len(sigma)
    loads = [F(0)] * len(machines)
    for job, owner in zip(jobs, sigma):
        eligible = {int(i): F(value) for i, value in job['eligible'].items()}
        assert eligible and all(0 <= i < len(machines) and time >= 0 for i, time in eligible.items())
        assert type(owner) is int and owner in eligible
        loads[owner] += eligible[owner]
    assert loads == [F(value) for value in expected]
    return loads


def validate_tree_edges(jobs, machines, k, h, variables, external_time, slot_mode):
    internal = {(m['variable'], m['sign'], tuple(m['word'])): i
                for i, m in enumerate(machines) if m['kind'] == 'internal'}
    assert len(internal) == variables * 2 * sum(k**level for level in range(h))
    seen = set(); leaves_by_clause = {}
    for job in jobs:
        kind = job['kind']
        if kind == 'actual_fixed_preload':
            continue
        v = job['variable']; eligible = {int(i): F(value) for i, value in job['eligible'].items()}
        assert 0 <= v < variables
        if kind == 'selector':
            key = (v, kind)
            assert eligible == {internal[v, 0, ()]: F(1), internal[v, 1, ()]: F(1)}
        else:
            word, sign = tuple(job['word']), job['sign']
            assert sign in (0, 1) and all(0 <= digit < k for digit in word)
            key = (v, sign, kind, word)
            parent = internal[v, sign, word[:-1]]
            assert eligible[parent] == F(1, k)
            if kind == 'tree_edge':
                assert 1 <= len(word) < h
                assert eligible == {parent: F(1, k), internal[v, sign, word]: F(1)}
            else:
                assert kind == 'leaf_port' and len(word) == h
                external = {i: time for i, time in eligible.items() if i != parent}
                assert external and all(time == external_time for time in external.values())
                if slot_mode:
                    clause = job['clause']
                    assert {machines[i]['clause'] for i in external} == {clause}
                    slots = {i for i, m in enumerate(machines) if m['kind'] == 'clause_slot' and m['clause'] == clause}
                    assert set(external) == slots
                    leaves_by_clause.setdefault(clause, []).append((v, sign))
                else:
                    assert set(external) == {job['private_host']}
        assert key not in seen
        seen.add(key)
    count = Counter(job['kind'] for job in jobs)
    assert count['selector'] == variables
    assert count['tree_edge'] == variables * 2 * (sum(k**level for level in range(h)) - 1)
    assert count['leaf_port'] == variables * 2 * k**h
    return leaves_by_clause


def audit():
    data = json.loads(PATH.read_text()); examples = data['examples']
    actual_jobs = actual_machines = certificates = source_assignments = 0
    private = examples['private_module']
    for record in private['profiles']:
        jobs, machines, sigma = record['original_jobs'], private['machines'], record['sigma']
        validate_tree_edges(jobs, machines, 4, 3, 1, F(1), False)
        opens = set(record['open_hosts'])
        pins = [job for job in jobs if job['kind'] == 'actual_fixed_preload']
        assert len(pins) == 128
        for pin in pins:
            assert len(pin['eligible']) == 1
            host = int(next(iter(pin['eligible'])))
            assert F(pin['eligible'][str(host)]) == (0 if host in opens else 1)
        loads = check(jobs, sigma, machines, record['actual_machine_loads'])
        assert max(loads) == F(record['actual_makespan'])
        assert max(loads) == (F(3, 2) if len(opens) == 8 else F(1))
        certificates += 1; actual_jobs += len(jobs); actual_machines += len(machines)
    records = []
    for name in ('unit_slot_source_NO_escape', 'single_endpoint_source_NO_escape', 'unit_slot_balanced_source_T_YES'):
        record = examples[name]
        jobs, sigma, machines = record['original_jobs'], record['sigma'], record['machines']
        unit = record['external_mode'] == 'unit_slots'
        leaves = validate_tree_edges(jobs, machines, 4, 3, 7, F(1) if unit else F(1, 4), True)
        masks = record['source_clause_masks']
        assert len(leaves) == len(masks) == 128
        for clause, ports in leaves.items():
            assert len(ports) == 7 and {v for v, sign in ports} == set(range(7))
            assert all(sign == ((masks[clause] >> v) & 1) for v, sign in ports)
        loads = check(jobs, sigma, machines, record['actual_machine_loads'])
        actual_counts = [0] * 128
        per_variable = [0] * 7
        for job, owner in zip(jobs, sigma):
            if job['kind'] == 'leaf_port' and machines[owner]['kind'] == 'clause_slot':
                actual_counts[job['clause']] += 1
                per_variable[job['variable']] += 1
        assert actual_counts == record['actual_external_ports_per_clause']
        assert max(actual_counts) <= 4
        assert max(loads) == F(record['actual_makespan'])
        if record['source_kind'] == 'fullcube':
            assert sorted(masks) == list(range(128))
            assert max(loads) == F(3, 2) and per_variable == [8] * 7
            for assignment in range(128):
                assert max((assignment ^ mask).bit_count() for mask in masks) == 7
                source_assignments += 1
        else:
            x = record['source_assignment_T_YES']
            assert max((x ^ mask).bit_count() for mask in masks) <= 4
            assert max(loads) == 1 and per_variable == [64] * 7
        certificates += 1; actual_jobs += len(jobs); actual_machines += len(machines)
        records.append({'name': name, 'jobs': len(jobs), 'machines': len(machines),
                        'actual_makespan': max(loads), 'ports_per_variable': per_variable,
                        'maximum_external_ports_per_clause': max(actual_counts)})
    return {'status': 'pass', 'counts': {'actual_full_certificates': certificates,
            'actual_jobs_checked': actual_jobs, 'actual_machine_loads_checked': actual_machines,
            'source_NO_assignments_checked': source_assignments}, 'records': records,
            'input_sha256': hashlib.sha256(PATH.read_bytes()).hexdigest(),
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': 'all original job eligibilities/times/owners and all loads in6 explicit certificates; no generator import, no LP, no general designer-wiring claim'}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True, default=str))
