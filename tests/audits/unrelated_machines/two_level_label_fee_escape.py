#!/usr/bin/env python3
"""Finite Fraction audit of complete, original two-level label-fee schedules.

No LP, external scheduler, or source satisfiability oracle is used to construct
the schedules. Tiny state/list enumerations check separate finite identities.
The general claims and arbitrary-schedule lower bound are proved in the account.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


def build(labels, edges, degree_bound):
    """edges = (left vertex, right vertex, full projection dictionary)."""
    assert degree_bound >= 2
    assert all(labels[v] and len(labels[v]) == len(set(labels[v])) for v in labels)
    deg = Counter(x for u, v, _ in edges for x in (u, v))
    assert not ({u for u, _, _ in edges} & {v for _, v, _ in edges})
    assert max(deg.values(), default=0) <= degree_bound
    machines, jobs = set(), {}

    def add(job, ends):
        assert job not in jobs
        jobs[job] = dict(ends)
        assert len(jobs[job]) == len(ends) and ends
        machines.update(jobs[job])

    for e, (u, v, pi) in enumerate(edges):
        assert u != v and set(pi) == set(labels[u])
        assert set(pi.values()) <= set(labels[v])
        add(('s', e), [(('R', e, a), F(1)) for a in labels[u]])
        for a in labels[u]:
            add(('xu', e, a), [(('R', e, a), F(1, 2)), (('H', e, u, a), F(1))])
            add(('xv', e, a), [(('R', e, a), F(1, 2)), (('H', e, v, pi[a]), F(1))])
        for endpoint in (u, v):
            for a in labels[endpoint]:
                add(('z', e, endpoint, a), [(('H', e, endpoint, a), F(3, 4)),
                                          (('A', endpoint, a), F(1, degree_bound))])
    for v in labels:
        for a in labels[v]:
            add(('w', v, a), [(('A', v, a), F(1)), (('B', v, a), F(1))])
            for r in range(degree_bound):
                add(('f', v, a, r), [(('B', v, a), F(1, degree_bound)),
                                       (('C', v, r), F(1))])
    if not machines:
        machines.add(('empty',))
    return machines, jobs


def construct(labels, edges, degree_bound, chosen, mode='half'):
    assert len(chosen) == len(edges) and mode in ('half', 'max', 'none')
    out, requested, counts = {}, set(), Counter()
    for e, ((u, v, pi), selected) in enumerate(zip(edges, chosen)):
        assert selected in labels[u]
        out['s', e] = ('R', e, selected)
        for a in labels[u]:
            out['xu', e, a] = ('H', e, u, a) if a == selected else ('R', e, a)
            out['xv', e, a] = ('H', e, v, pi[a]) if a == selected else ('R', e, a)
        for endpoint, a in ((u, selected), (v, pi[selected])):
            requested.add((e, endpoint, a))
            counts[endpoint, a] += 1
        for endpoint in (u, v):
            for a in labels[endpoint]:
                out['z', e, endpoint, a] = (('A', endpoint, a)
                    if (e, endpoint, a) in requested else ('H', e, endpoint, a))
    for v, alphabet in labels.items():
        largest = max(alphabet, key=lambda a: counts[v, a])
        for a in alphabet:
            opened = ((counts[v, a] > degree_bound // 2) if mode == 'half'
                      else (a == largest) if mode == 'max' else False)
            out['w', v, a] = ('B' if opened else 'A', v, a)
            for r in range(degree_bound):
                out['f', v, a, r] = ('C', v, r) if opened else ('B', v, a)
    return out, counts


def verify(labels, edges, degree_bound, chosen, mode='half'):
    machines, jobs = build(labels, edges, degree_bound)
    out, counts = construct(labels, edges, degree_bound, chosen, mode)
    assert set(out) == set(jobs)
    load = dict.fromkeys(machines, F(0))
    for j, dest in out.items():
        assert dest in jobs[j]
        load[dest] += jobs[j][dest]
    peak = max(load.values())
    second = max((sorted((counts[v, a] for a in alphabet), reverse=True) + [0, 0])[1]
                 for v, alphabet in labels.items()) if labels else 0
    assert all(load[m] <= 1 for m in machines if m[0] == 'C')
    if mode == 'half':
        assert peak <= 1 + F(degree_bound // 2, degree_bound)
    elif mode == 'max':
        assert peak == (1 + F(second, degree_bound) if labels else F(0))
    return dict(machines=len(machines), jobs=len(jobs),
                finite_entries=sum(map(len, jobs.values())), peak=str(peak),
                second=second, all_jobs_once=True, pool_load_at_most_one=True)


def shift(q):
    labels = {0: list(range(q)), 1: list(range(q))}
    edges = [(0, 1, {a: (a+t) % q for a in range(q)}) for t in range(q)]
    report = verify(labels, edges, q, list(range(q)), 'none')
    assert F(report['peak']) == 1 + F(1, q)
    assert report['machines'] == 3*q*q + 6*q
    assert report['jobs'] == 6*q*q + 3*q
    assert report['finite_entries'] == 13*q*q + 4*q
    for choice in ([0]*q, list(range(q)), [e % 2 for e in range(q)]):
        verify(labels, edges, q, choice, 'half')
        verify(labels, edges, q, choice, 'max')
    return dict(q=q, **report)


def tiny_sources():
    # All these data are listed: no random generator or hidden parameter seed.
    cases = [({}, [], 2), ({0: [0]}, [], 2),
             ({0: [0, 1], 1: [0]}, [(0, 1, {0: 0, 1: 0})], 2),
             ({0: [0], 1: [0, 1]}, [(0, 1, {0: 0}), (0, 1, {0: 1})], 2),
             ({0: [0, 1], 1: [0, 1], 2: [0]},
              [(0, 1, {0: 0, 1: 1}), (0, 1, {0: 1, 1: 0})], 2),
             ({0: [0, 1, 2], 1: [0, 1], 2: [0, 1]},
              [(0, 1, {0: 0, 1: 0, 2: 1}), (0, 2, {0: 0, 1: 1, 2: 1})], 3)]
    records = []
    for labels, edges, D in cases:
        outputs = []
        satisfied = False
        for assignments in product(*(labels[v] for v in labels)):
            labelling = dict(zip(labels, assignments))
            satisfied |= all(pi[labelling[u]] == labelling[v] for u, v, pi in edges)
        for choice in product(*(labels[u] for u, _, _ in edges)):
            verify(labels, edges, D, choice, 'half')
            outputs.append(verify(labels, edges, D, choice, 'max'))
        mu = min(o['second'] for o in outputs)
        assert (mu == 0) == satisfied
        records.append(dict(labels=labels, edges=[(u, v, pi) for u, v, pi in edges],
                            D=D, all_state_choices=len(outputs), mu=mu,
                            source_singleton_satisfiable=satisfied,
                            best_constructed_peak=str(min(F(o['peak']) for o in outputs))))
    return records


def list_counts(q):
    checked = 0
    for mask_a, mask_b in product(range(1 << q), repeat=2):
        a = [i for i in range(q) if mask_a >> i & 1]
        b = [i for i in range(q) if mask_b >> i & 1]
        covered = len({(y-x) % q for x in a for y in b})
        assert covered <= len(a)*len(b)
        assert 4*covered <= (len(a)+len(b))**2
        checked += 1
    return dict(q=q, list_pairs=checked)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[3]
    account = root / 'research/current/unrelated_machines/two_level_label_fee_escape.md'
    report = dict(command='python3 tests/audits/unrelated_machines/two_level_label_fee_escape.py',
                  arithmetic='fractions.Fraction; integers', seed='none; explicit inputs',
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  account_sha256=hashlib.sha256(account.read_bytes()).hexdigest(),
                  shift=[shift(q) for q in (3, 5, 7, 11, 25)],
                  tiny_sources=tiny_sources(), list_counts=[list_counts(q) for q in (3, 5, 7)],
                  unchecked='No enumeration of all actual schedules, arbitrary sources, or general approximation algorithms. The OPT lower identity uses the separate mathematical proof.')
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
