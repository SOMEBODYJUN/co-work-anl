#!/usr/bin/env python3
"""Actual open-two-tree module YES states and a unit-slot source-NO escape.

Default finite certificate uses original two-tree k=4,height=3.  Every
tree job is parent1/k, child1.  Terminal parallel bundles are OPENED into
individual real leaf-port jobs.  No LP information enters any assignment.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


def original_height(k):
    h = 1; alpha = F(1, k - 1)
    while alpha < F(1, 2):
        alpha *= F(k, k - 1); h += 1
    return h, alpha


def words(k, length):
    return list(product(range(k), repeat=length))


def active(word, k):
    return all(digit < k // 2 for digit in word)


def tree_core(k, h, variables):
    machines = []; ids = {}; jobs = []
    for v in range(variables):
        for sign in (0, 1):
            for length in range(h):
                for word in words(k, length):
                    ids[v, sign, word] = len(machines)
                    machines.append({'kind': 'internal', 'variable': v, 'sign': sign, 'word': word})
    for v in range(variables):
        jobs.append({'kind': 'selector', 'variable': v,
                     'eligible': {ids[v, 0, ()]: F(1), ids[v, 1, ()]: F(1)}})
        for sign in (0, 1):
            for length in range(1, h):
                for word in words(k, length):
                    jobs.append({'kind': 'tree_edge', 'variable': v, 'sign': sign, 'word': word,
                                 'eligible': {ids[v, sign, word[:-1]]: F(1, k), ids[v, sign, word]: F(1)}})
            for word in words(k, h):
                jobs.append({'kind': 'leaf_port', 'variable': v, 'sign': sign, 'word': word,
                             'eligible': {ids[v, sign, word[:-1]]: F(1, k)}})
    return machines, ids, jobs


def exact_loads(jobs, sigma, machines):
    assert len(jobs) == len(sigma)
    loads = [F(0)] * machines
    for job, owner in zip(jobs, sigma):
        assert type(owner) is int and owner in job['eligible']
        assert all(value >= 0 for value in job['eligible'].values())
        loads[owner] += job['eligible'][owner]
    return loads


def private_module(k=4, h=3):
    machines, ids, jobs = tree_core(k, h, 1)
    for job in jobs:
        if job['kind'] == 'leaf_port':
            host = len(machines)
            machines.append({'kind': 'private_host', 'sign': job['sign'], 'word': job['word']})
            job['private_host'] = host; job['eligible'][host] = F(1)
    profiles = []
    for name, sign, prune in (('all_positive_open_T_YES', 0, False),
                              ('all_negative_open_T_YES', 1, False),
                              ('only_pruned_negative_open_weak', 1, True)):
        sigma = []; open_hosts = []
        for job in jobs:
            v = job['variable']
            if job['kind'] == 'selector':
                owner = ids[v, sign, ()]
            elif job['kind'] == 'tree_edge':
                down = job['sign'] == sign and (not prune or active(job['word'], k))
                owner = ids[v, job['sign'], job['word'] if down else job['word'][:-1]]
            else:
                out = job['sign'] == sign and (not prune or active(job['word'], k))
                owner = job['private_host'] if out else ids[v, job['sign'], job['word'][:-1]]
                if out:
                    open_hosts.append(owner)
            sigma.append(owner)
        open_set = set(open_hosts)
        pins = [{'kind': 'actual_fixed_preload', 'eligible': {i: F(0 if i in open_set else 1)}}
                for i, machine in enumerate(machines) if machine['kind'] == 'private_host']
        sigma += [next(iter(pin['eligible'])) for pin in pins]
        full_jobs = jobs + pins
        loads = exact_loads(full_jobs, sigma, len(machines))
        assert max(loads) == (F(3, 2) if prune else F(1))
        profiles.append({'name': name, 'open_hosts': open_hosts, 'original_jobs': full_jobs,
                         'sigma': sigma, 'actual_machine_loads': loads, 'actual_makespan': max(loads)})
    return {'k': k, 'height': h, 'machines': machines, 'profiles': profiles}


def graft(k=4, h=3, source_kind='fullcube', external_mode='unit_slots'):
    exponent = k.bit_length() - 1
    assert k == 1 << exponent and exponent % 2 == 0 and k >= 4
    d = 1 + exponent * h; A = (d + 1) // 2
    assert d == 2 * A - 1
    count = 1 << d; occurrences = k**h
    assert occurrences == 1 << (d - 1)
    masks = list(range(count)) if source_kind == 'fullcube' else [0] * occurrences + [count - 1] * occurrences
    machines, ids, jobs = tree_core(k, h, d)
    internal_count = len(machines)
    slots = A if external_mode == 'unit_slots' else 1
    for clause in range(count):
        for slot in range(slots):
            machines.append({'kind': 'clause_slot', 'clause': clause, 'sign_mask': masks[clause], 'slot': slot})
    leaf_words = words(k, h)
    active_words = [word for word in leaf_words if active(word, k)]
    leaf_to_clause = {}
    for v in range(d):
        for sign in (0, 1):
            all_clauses = [clause for clause, mask in enumerate(masks) if ((mask >> v) & 1) == sign]
            assert len(all_clauses) == occurrences
            if source_kind == 'fullcube' and sign == 1:
                good = [clause for clause in all_clauses if masks[clause].bit_count() <= A]
                assert len(good) >= len(active_words)
                chosen = good[:len(active_words)]
                selected = set(chosen)
                remainder = [clause for clause in all_clauses if clause not in selected]
                mapping = dict(zip(active_words, chosen))
                mapping.update(zip((word for word in leaf_words if not active(word, k)), remainder))
            else:
                mapping = dict(zip(leaf_words, all_clauses))
            assert len(mapping) == occurrences and set(mapping.values()) == set(all_clauses)
            for word, clause in mapping.items():
                leaf_to_clause[v, sign, word] = clause
    for job in jobs:
        if job['kind'] == 'leaf_port':
            clause = leaf_to_clause[job['variable'], job['sign'], job['word']]
            job['clause'] = clause
            for slot in range(slots):
                job['eligible'][internal_count + clause * slots + slot] = F(1) if slots == A else F(1, A)
    source_assignment = None if source_kind == 'fullcube' else sum(1 << v for v in range(A - 1))
    selected_ports = [[] for _ in range(count)]
    sigma = []
    for index, job in enumerate(jobs):
        v = job['variable']
        selected_sign = 1 if source_assignment is None else (0 if (source_assignment >> v) & 1 else 1)
        prune = source_assignment is None
        if job['kind'] == 'selector':
            owner = ids[v, selected_sign, ()]
        elif job['kind'] == 'tree_edge':
            down = job['sign'] == selected_sign and (not prune or active(job['word'], k))
            owner = ids[v, job['sign'], job['word'] if down else job['word'][:-1]]
        else:
            out = job['sign'] == selected_sign and (not prune or active(job['word'], k))
            owner = None if out else ids[v, job['sign'], job['word'][:-1]]
            if out:
                selected_ports[job['clause']].append(index)
        sigma.append(owner)
    counts = [len(row) for row in selected_ports]
    assert max(counts) <= A
    for clause, row in enumerate(selected_ports):
        for rank, job_index in enumerate(row):
            sigma[job_index] = internal_count + clause * slots + (rank if slots == A else 0)
    loads = exact_loads(jobs, sigma, len(machines))
    assert max(loads) == (F(3, 2) if source_assignment is None else F(1))
    no_witnesses = []
    if source_assignment is None:
        for assignment in range(count):
            clause = assignment ^ (count - 1)
            assert (assignment ^ masks[clause]).bit_count() == d
            no_witnesses.append({'source_assignment': assignment, 'all_true_clause': clause})
    else:
        assert max((source_assignment ^ mask).bit_count() for mask in masks) <= A
    return {'k': k, 'height': h, 'd': d, 'A': A, 'occurrences_per_sign': occurrences,
            'source_kind': source_kind, 'external_mode': external_mode, 'source_clause_masks': masks,
            'source_assignment_T_YES': source_assignment, 'source_NO_all_assignments': no_witnesses,
            'machines': machines, 'original_jobs': jobs, 'sigma': sigma,
            'actual_machine_loads': loads, 'actual_makespan': max(loads),
            'actual_external_ports_per_clause': counts,
            'selected_leaf_ports': sum(counts), 'maximum_external_ports_per_clause': max(counts),
            'internal_machine_count': internal_count, 'clause_slots': count * slots}


def audit():
    k = 4; h, alpha = original_height(k)
    assert h == 3
    examples = {'private_module': private_module(k, h),
                'unit_slot_source_NO_escape': graft(k, h, 'fullcube', 'unit_slots'),
                'single_endpoint_source_NO_escape': graft(k, h, 'fullcube', 'scaled_single'),
                'unit_slot_balanced_source_T_YES': graft(k, h, 'paired_clauses', 'unit_slots')}
    return {'status': 'pass', 'k': k, 'original_height': h, 'original_root_alpha': alpha,
            'sealed_original_tree_exact_OPT_by_known_proof': F(2) - F(1, k),
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': 'explicit opened-bottom wiring only; module complete YES states, source NO physical escapes, one balanced source YES; not every designer wiring or general hardness',
            'examples': examples}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True, default=str))
