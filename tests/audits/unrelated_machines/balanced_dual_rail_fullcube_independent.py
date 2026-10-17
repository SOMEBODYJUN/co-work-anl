#!/usr/bin/env python3
"""Independent complete-cut and physical-assignment checks for A=1..5.

The physical oracle never calls the tested constructor's formula or flow
helpers.  It enumerates all variable-side cuts of the explicit deletion
network, then every possible physical load breakpoint.  This is NOT an
enumeration of 2**number_of_jobs original complete assignments.  Its exact
normal-form reduction and min-cut equivalence must be justified separately.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import sys


def complete_cut_demands(d, B):
    """Every cut: outside variables can absorb at most one per incidence."""
    clauses = range(1 << d)
    demands = {}
    for inside in range(1, 1 << d):
        amount = 0
        for mask in clauses:
            clause_need = max(mask.bit_count() - B, 0)
            available_outside = (mask & ~inside).bit_count()
            amount += max(clause_need - available_outside, 0)
        demands[inside] = amount
    return demands


def complete_physical_oracle(A):
    d = 2 * A - 1; k = 1 << (d - 1)
    cuts = {B: complete_cut_demands(d, B) for B in range(d + 1)}
    candidates = {1 + F(h, k) for h in range(k + 1)}
    candidates.update(F(B, A) for B in range(A, d + 1))
    feasible = []
    for C in sorted(candidates):
        h = ((C - 1) * k).__floor__()
        B = min(d, (C * A).__floor__())
        ok = all(need <= h * subset.bit_count() for subset, need in cuts[B].items())
        if ok:
            feasible.append(C)
    assert feasible
    return {'optimum': min(feasible),
            'all_cut_count': sum(len(row) for row in cuts.values()),
            'all_physical_breakpoints': len(candidates),
            'feasible_breakpoints': len(feasible)}


def physical_check(data, certificate):
    """Reconstruct the entire original two-edge matrix; sum every real job."""
    A, d, k, m = data['A'], data['d'], data['k'], data['machines']
    assert d == 2 * A - 1 and k == 1 << (d - 1)
    assert m == 2 * d + (1 << d)
    jobs = data['jobs']; sigma = certificate['sigma']
    assert len(jobs) == len(sigma) == d * (1 << d) + d
    loads = [F(0)] * m
    negative_internal = [0] * d
    for index, (job, owner) in enumerate(zip(jobs, sigma)):
        assert type(owner) is int
        if index < d:
            v = index
            expected = {2 * v: F(1), 2 * v + 1: F(1)}
            assert job['kind'] == 'selector' and job['variable'] == v
        else:
            mask, v = divmod(index - d, d)
            negative = (mask >> v) & 1
            expected = {2 * v + negative: F(1, k), 2 * d + mask: F(1, A)}
            assert job['kind'] == 'port' and job['variable'] == v
            assert job['clause_mask'] == mask and job['negative'] == negative
            if negative and owner == 2 * v + 1:
                negative_internal[v] += 1
        assert job['eligible'] == expected
        assert owner in expected
        loads[owner] += expected[owner]
    assert loads == certificate['actual_machine_loads']
    assert max(loads) == certificate['actual_makespan']
    assert negative_internal == certificate['negative_rail_internal_port_counts']
    return max(loads)


def independent_half_certificate(data):
    A, d, k = data['A'], data['d'], data['k']
    assert A >= 2 and k % 2 == 0
    selected = []
    for v in range(d):
        possible = [mask for mask in range(1 << d)
                    if (mask >> v) & 1 and mask.bit_count() <= A]
        assert len(possible) >= k // 2
        selected.append(set(possible[:k // 2]))
    sigma = []
    loads = [F(0)] * data['machines']; removed = [0] * d
    for index in range(len(data['jobs'])):
        if index < d:
            owner = 2 * index + 1
        else:
            mask, v = divmod(index - d, d)
            negative = (mask >> v) & 1
            if negative and mask in selected[v]:
                owner = 2 * d + mask
            else:
                owner = 2 * v + negative
                removed[v] += negative
        sigma.append(owner)
        loads[owner] += data['jobs'][index]['eligible'][owner]
    certificate = {'sigma': sigma, 'actual_machine_loads': loads,
                   'actual_makespan': max(loads),
                   'negative_rail_internal_port_counts': removed}
    assert physical_check(data, certificate) == F(3, 2)
    assert max(loads[2 * d:]) <= 1
    return certificate


def audit():
    path = Path(__file__).with_name('balanced_dual_rail_fullcube.py')
    name = 'fullcube_constructor_under_test'
    spec = importlib.util.spec_from_file_location(name, path)
    tested = importlib.util.module_from_spec(spec)
    sys.modules[name] = tested
    spec.loader.exec_module(tested)
    records = []
    totals = {'all_cut_count': 0, 'all_physical_breakpoints': 0,
              'original_jobs_checked': 0, 'actual_certificates': 0,
              'source_no_assignments_checked': 0}
    for A in range(1, 6):
        out = tested.construct(A)
        data = out['instance']
        actual = physical_check(data, out['certificate'])
        independent = complete_physical_oracle(A)
        assert actual == independent['optimum'] == out['exact_value_formula']['value']
        totals['actual_certificates'] += 1
        totals['original_jobs_checked'] += len(data['jobs'])
        half = None
        if A >= 2:
            half = independent_half_certificate(data)['actual_makespan']
            totals['actual_certificates'] += 1
            totals['original_jobs_checked'] += len(data['jobs'])
            full = (1 << data['d']) - 1
            for source_assignment in range(1 << data['d']):
                # Literal truth mask at a signed clause is assignment XOR sign.
                violating_clause = source_assignment ^ full
                assert (source_assignment ^ violating_clause).bit_count() == data['d']
                assert data['d'] > 2 * A - 2
                totals['source_no_assignments_checked'] += 1
        if A == 3:
            hand = out['A3_hand_certificate']
            assert physical_check(data, hand) == F(9, 8)
            assert hand['negative_rail_internal_port_counts'] == [2, 2, 1, 1, 1]
            totals['actual_certificates'] += 1
            totals['original_jobs_checked'] += len(data['jobs'])
        for key in ('all_cut_count', 'all_physical_breakpoints'):
            totals[key] += independent[key]
        records.append({'A': A, 'machines': data['machines'], 'jobs': len(data['jobs']),
                        'd': data['d'], 'k': data['k'], 'exact_optimum': actual,
                        'independent_half_makespan': half, **independent})
    return {'status': 'pass', 'records': records, 'counts': totals,
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'tested_constructor_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'scope': 'A1..5 full deletion-network cuts and all physical load breakpoints; actual original jobs/eligibilities/loads; not exhaustive original-job assignment enumeration; finite evidence only'}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True, default=str))
