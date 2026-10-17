#!/usr/bin/env python3
"""Explicit full-cube counterexamples to one balanced dual-rail block code.

This is a finite actual scheduling constructor, not a general hardness
reduction.  All original jobs have exactly two eligible machines.  Times
are exact nonnegative rationals.  Input A describes an EXPLICIT cube of
2**(2*A-1) constraints; complexity is polynomial in that expanded input.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


class IntegralFlow:
    def __init__(self, n):
        self.g = [[] for _ in range(n)]

    def edge(self, u, v, cap):
        first = len(self.g[u]); second = len(self.g[v])
        self.g[u].append([v, second, cap])
        self.g[v].append([u, first, 0])
        return u, first

    def flow(self, s, t):
        value = 0
        while True:
            predecessor = [None] * len(self.g)
            predecessor[s] = (s, -1)
            queue = [s]
            for u in queue:
                if predecessor[t] is not None:
                    break
                for index, (v, reverse, cap) in enumerate(self.g[u]):
                    if cap and predecessor[v] is None:
                        predecessor[v] = (u, index)
                        queue.append(v)
            if predecessor[t] is None:
                return value
            path = []; v = t
            while v != s:
                u, index = predecessor[v]
                path.append((u, index)); v = u
            amount = min(self.g[u][index][2] for u, index in path)
            assert amount >= 1
            for u, index in path:
                edge = self.g[u][index]
                edge[2] -= amount
                self.g[edge[0]][edge[1]][2] += amount
            value += amount


def instance(A):
    assert type(A) is int and A >= 1
    d = 2 * A - 1; k = 2**(d - 1); clauses = 2**d
    jobs = []
    for v in range(d):
        jobs.append({'kind': 'selector', 'variable': v,
                     'eligible': {2 * v: F(1), 2 * v + 1: F(1)}})
    for mask in range(clauses):
        for v in range(d):
            negative = (mask >> v) & 1
            jobs.append({'kind': 'port', 'variable': v, 'clause_mask': mask,
                         'negative': negative,
                         'eligible': {2 * v + negative: F(1, k), 2 * d + mask: F(1, A)}})
    return {'A': A, 'd': d, 'k': k, 'machines': 2 * d + clauses,
            'jobs': jobs, 'threshold': F(1)}


def exact_formula(A):
    d = 2 * A - 1; k = 2**(d - 1)
    options = []
    for B in range(A, d + 1):
        R = sum(max(mask.bit_count() - B, 0) for mask in range(2**d))
        r = (R + d - 1) // d
        options.append({'B': B, 'total_removed_ports': R, 'rail_capacity': r,
                        'value': max(F(B, A), 1 + F(r, k))})
    best = min(options, key=lambda x: (x['value'], x['B']))
    return best, options


def deletion_flow(d, B, rail_capacity):
    clauses = 2**d; source = 0; variable_offset = 1 + clauses
    sink = variable_offset + d
    graph = IntegralFlow(sink + 1); handles = {}; required = 0
    for mask in range(clauses):
        need = max(mask.bit_count() - B, 0)
        graph.edge(source, 1 + mask, need); required += need
        for v in range(d):
            if (mask >> v) & 1:
                handles[mask, v] = graph.edge(1 + mask, variable_offset + v, 1)
    for v in range(d):
        graph.edge(variable_offset + v, sink, rail_capacity)
    assert graph.flow(source, sink) == required
    removed = set()
    for pair, (u, index) in handles.items():
        if graph.g[u][index][2] == 0:
            removed.add(pair)
    assert len(removed) == required
    return removed


def physical_certificate(data, removed):
    A, d, k = data['A'], data['d'], data['k']
    sigma = []
    for job in data['jobs']:
        v = job['variable']
        if job['kind'] == 'selector':
            owner = 2 * v + 1
        elif not job['negative'] or (job['clause_mask'], v) in removed:
            owner = 2 * v + job['negative']
        else:
            owner = 2 * d + job['clause_mask']
        assert owner in job['eligible']
        sigma.append(owner)
    loads = [F(0)] * data['machines']
    for job, owner in zip(data['jobs'], sigma):
        loads[owner] += job['eligible'][owner]
    rail_removed = [sum((mask, v) in removed for mask in range(2**d)) for v in range(d)]
    return {'sigma': sigma, 'actual_machine_loads': loads, 'actual_makespan': max(loads),
            'negative_rail_internal_port_counts': rail_removed,
            'removed_ports': [{'clause_mask': mask, 'variable': v} for mask, v in sorted(removed)]}


def construct(A):
    data = instance(A)
    best, options = exact_formula(A)
    removed = deletion_flow(data['d'], best['B'], best['rail_capacity'])
    certificate = physical_certificate(data, removed)
    assert certificate['actual_makespan'] == best['value']
    # A=3 has a particularly transparent seven-port physical certificate.
    special = None
    if A == 3:
        full = (1 << data['d']) - 1
        hand = {(full ^ (1 << i), (i + 1) % 5) for i in range(5)}
        hand.update({(full, 0), (full, 1)})
        special = physical_certificate(data, hand)
        assert special['actual_makespan'] == F(9, 8)
        assert max(special['actual_machine_loads'][2 * data['d']:]) <= 1
    return {'status': 'constructed', 'instance': data, 'certificate': certificate,
            'exact_value_formula': best, 'formula_candidates': options,
            'A3_hand_certificate': special,
            'source_no_scope': 'A>=2: every source assignment has an all-true clause, so even weak threshold d-1 is impossible',
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': 'one balanced two-rail selector code on an explicit full signed cube; no claim against other block codes'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--A', type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(construct(args.A), indent=2, sort_keys=True, default=str))


if __name__ == '__main__':
    main()
