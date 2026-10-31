#!/usr/bin/env python3
"""余横截配置锐化障碍：D=3,4 的显式 Fraction 证书和 Hall 审计。

This finite audit checks full configuration certificates, complete original
schedules, explicit mandatory matching witnesses, and all two-port-per-player
Hall obstructions up to state-label symmetry.  It does not enumerate all full
UM schedules and does not infer a general proof from finite tests.
"""
from collections import Counter, deque
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json


def pid(u, a):
    return f'P:{u}:{a}'


def gid(u, a, j):
    return f'g:{u}:{a}:{j}'


def aid(u, a):
    return f'A:{u}:{a}'


def bid(j):
    return f'B:{j}'


def lid(u, a, j):
    return f'L:{u}:{a}:{j}'


def jid(u, a, j):
    return f'J:{u}:{a}:{j}'


def xid(u):
    return f'X:{u}'


def build(D):
    if type(D) is not int or D < 3:
        raise ValueError('integer D >= 3 required')
    m = D + 1
    ground = [gid(u, a, j) for u in range(m) for a in range(D) for j in range(D)]
    ground += [aid(u, a) for u in range(m) for a in range(D)]
    ground += [bid(j) for j in range(D)]
    parents = [pid(u, a) for u in range(m) for a in range(D)]
    machines = parents + ground
    jobs, mandatory, configurations = {}, {}, []
    for u in range(m):
        jobs[xid(u)] = {pid(u, a): F(1) for a in range(D)}
        for a in range(D):
            ports = []
            for j in range(D):
                ports.append(jid(u, a, j))
                jobs[jid(u, a, j)] = {pid(u, a): F(1, D), gid(u, a, j): F(1)}
                neighborhood = [gid(u, a, j), aid(u, a), bid(j)]
                mandatory[lid(u, a, j)] = neighborhood
                jobs[lid(u, a, j)] = {v: F(1) for v in neighborhood}
                configurations += [
                    {'machine': gid(u, a, j), 'jobs': [jid(u, a, j)], 'weight': F(1, D)},
                    {'machine': gid(u, a, j), 'jobs': [lid(u, a, j)], 'weight': F(D - 1, D)},
                    {'machine': aid(u, a), 'jobs': [lid(u, a, j)], 'weight': F(1, D)},
                ]
            configurations += [
                {'machine': pid(u, a), 'jobs': [xid(u)], 'weight': F(1, D)},
                {'machine': pid(u, a), 'jobs': ports, 'weight': F(D - 1, D)},
            ]
    configurations += [{'machine': bid(j), 'jobs': [], 'weight': F(1)} for j in range(D)]
    return {'D': D, 'm': m, 'ground': ground, 'machines': machines,
            'jobs': jobs, 'mandatory': mandatory, 'configurations': configurations}


def check_lp(I):
    rows = {v: F(0) for v in I['machines']}
    coverage = {job: F(0) for job in I['jobs']}
    for c in I['configurations']:
        v, jobs, weight = c['machine'], c['jobs'], c['weight']
        assert weight >= 0 and len(set(jobs)) == len(jobs)
        load = F(0)
        for job in jobs:
            assert v in I['jobs'][job]
            load += I['jobs'][job][v]
            coverage[job] += weight
        assert load <= 1
        rows[v] += weight
    assert set(rows.values()) == {F(1)}
    assert set(coverage.values()) == {F(1)}
    return {'row_count': len(rows), 'job_count': len(coverage),
            'configuration_count': len(I['configurations']),
            'all_row_sums': F(1), 'all_job_coverages': F(1)}


def check_matching(I, removed, matching):
    assert set(matching) == set(I['mandatory'])
    assert len(set(matching.values())) == len(matching)
    removed = set(removed)
    for job, v in matching.items():
        assert v in I['mandatory'][job] and v not in removed


def own_matching(I):
    D, m = I['D'], I['m']
    return {lid(u, a, j): gid(u, a, j)
            for u in range(m) for a in range(D) for j in range(D)}


def matroid_certificates(I):
    D, m = I['D'], I['m']
    singleton_configs = []
    for u in range(m):
        for a in range(D):
            C = [gid(u, a, j) for j in range(D)]
            matching = own_matching(I)
            for j in range(D):
                matching[lid(u, a, j)] = aid(u, a) if j == 0 else bid(j)
            check_matching(I, C, matching)
            singleton_configs.append({'u': u, 'a': a, 'removed': C,
                                      'mandatory_matching': matching})
    mixture = []
    marginal = {v: F(0) for v in I['ground']}
    for t in range(D):
        T = [gid(u, a, t) for u in range(m) for a in range(D)]
        matching = own_matching(I)
        for u in range(m):
            for a in range(D):
                matching[lid(u, a, t)] = aid(u, a)
        check_matching(I, T, matching)
        for v in T:
            marginal[v] += F(1, D)
        mixture.append({'weight': F(1, D), 'removed': T,
                        'mandatory_matching': matching})
    assert all(marginal[v] == (F(1, D) if v.startswith('g:') else F(0))
               for v in I['ground'])
    # Independent union attaining exactly one retained element per player.
    selected = [gid(u, 0, 0) for u in range(m)]
    matching = own_matching(I)
    for u in range(m):
        matching[lid(u, 0, 0)] = aid(u, 0)
    check_matching(I, selected, matching)
    return {'all_individual_configuration_witnesses': singleton_configs,
            'explicit_marginal_convex_combination': mixture,
            'marginal': marginal,
            'one_per_player_witness': {'removed': selected, 'mandatory_matching': matching}}


def maximum_matching(neighbors):
    """Independent direct augmenting paths for the affected jobs only."""
    owner = {}
    assigned = {}
    for start in neighbors:
        previous, queue, seen = {start: None}, deque([start]), set()
        last = None
        while queue and last is None:
            job = queue.popleft()
            for v in neighbors[job]:
                if v in seen:
                    continue
                seen.add(v)
                if v not in owner:
                    last = job, v
                    break
                if owner[v] not in previous:
                    previous[owner[v]] = job, v
                    queue.append(owner[v])
        if last is None:
            continue
        job, v = last
        while True:
            assigned[job] = v
            owner[v] = job
            if previous[job] is None:
                break
            job, v = previous[job]
    assert len(set(assigned.values())) == len(assigned)
    return assigned


def exhaustive_two_per_player_hall(I):
    D, m = I['D'], I['m']
    # All state choices are isomorphic via a private permutation of a for
    # each u; enumerate every pair pattern at canonical a_u=0, not all jobs.
    pairs = list(combinations(range(D), 2))
    checked, hist, max_neighbors, representative = 0, Counter(), 0, None
    for selected_pairs in product(pairs, repeat=m):
        removed = {gid(u, 0, j) for u in range(m) for j in selected_pairs[u]}
        affected = [lid(u, 0, j) for u in range(m) for j in selected_pairs[u]]
        neighbors = {job: [v for v in I['mandatory'][job] if v not in removed]
                     for job in affected}
        union = {v for vv in neighbors.values() for v in vv}
        assert len(affected) == 2 * m
        assert len(union) <= m + D < len(affected)
        matching = maximum_matching(neighbors)
        assert len(matching) <= len(union) < len(affected)
        hist[len(matching)] += 1
        max_neighbors = max(max_neighbors, len(union))
        checked += 1
        if len(union) == m + D and representative is None:
            representative = {'removed': sorted(removed), 'affected_jobs': affected,
                              'actual_neighbors': sorted(union),
                              'partial_matching': matching}
    assert representative is not None
    return {'canonical_state': 0, 'state_symmetry_used': True,
            'all_pair_patterns': checked, 'affected_job_count': 2 * m,
            'largest_actual_neighborhood': max_neighbors,
            'strict_capacity_bound': m + D,
            'maximum_matching_size_histogram': dict(sorted(hist.items())),
            'representative_Hall_deficit': representative}


def actual_schedule(I):
    D, m = I['D'], I['m']
    sigma = {}
    for u in range(m):
        sigma[xid(u)] = pid(u, 0)
        for a in range(D):
            for j in range(D):
                active = a == 0 and j == 0
                sigma[jid(u, a, j)] = gid(u, a, j) if active else pid(u, a)
                sigma[lid(u, a, j)] = aid(u, a) if active else gid(u, a, j)
    assert set(sigma) == set(I['jobs'])
    loads = {v: F(0) for v in I['machines']}
    for job, v in sigma.items():
        assert v in I['jobs'][job]
        loads[v] += I['jobs'][job][v]
    expected = F(2) - F(1, D)
    assert max(loads.values()) == expected
    for u in range(m):
        assert loads[pid(u, 0)] == expected
    # Exact numerical branch used in the universal lower-bound argument.
    assert F(1) + F(D - 1, D) == expected < 2
    assert 2 * m > m + D
    return {'sigma': sigma, 'loads': loads, 'actual_makespan': max(loads.values()),
            'claimed_exact_OPT': expected,
            'lower_bound_numeric_identity': {'two_ports_per_player': 2 * m,
                                             'accessible_unit_machines': m + D,
                                             'selector_plus_D_minus_1_ports': expected}}


def jsonable(x):
    if isinstance(x, F):
        return str(x)
    if type(x) is dict:
        return {str(k): jsonable(v) for k, v in x.items()}
    if type(x) in (list, tuple):
        return [jsonable(v) for v in x]
    return x


def audit():
    results = []
    for D in (3, 4):
        I = build(D)
        results.append({'D': D, 'm': I['m'],
                        'ground_count': len(I['ground']),
                        'machine_count': len(I['machines']),
                        'mandatory_job_count': len(I['mandatory']),
                        'total_original_job_count': len(I['jobs']),
                        'input': I,
                        'configuration_certificate_check': check_lp(I),
                        'matroid_matching_certificates': matroid_certificates(I),
                        'two_per_player_Hall_check': exhaustive_two_per_player_hall(I),
                        'complete_original_schedule': actual_schedule(I)})
    return {'title': '显式余横截拟阵锐化间隙的 Fraction 与 Hall 有限核验',
            'scope': 'D=3,4 exact finite checks; general proof is separate; not NP-hardness',
            'source_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'cases': results}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    with args.output.open('x') as f:
        json.dump(jsonable(audit()), f, ensure_ascii=False, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
