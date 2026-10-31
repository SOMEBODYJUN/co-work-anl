#!/usr/bin/env python3
"""Exact configurations and pairwise-compatible couplings, no global distribution claim."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
import platform


def build(k):
    assert k >= 2
    machines = ([('V', a) for a in range(k)]
                + [('G', g) for g in range(k - 1)]
                + [('R', a, ell) for a in range(k) for ell in range(k + 1)])
    times = {machine: {} for machine in machines}
    configs = {machine: [] for machine in machines}
    def config(machine, jobs, weight):
        configs[machine].append((frozenset(jobs), weight))
    for a in range(k):
        x = ('X', a)
        times['V', a][x] = F(1)
        for g in range(k - 1):
            times['G', g][x] = F(1)
        for h in range(k):
            y = ('Y', a, h)
            for ell in range(k + 1):
                times['R', a, ell][y] = F(1)
        for r in range(k):
            z = ('Z', a, r)
            times['V', a][z] = F(1, k)
            for ell in range(k + 1):
                times['R', a, ell][z] = F(1)
        config(('V', a), [x], F(1, k))
        config(('V', a), [('Z', a, r) for r in range(k)], F(k - 1, k))
    for g in range(k - 1):
        for a in range(k):
            config(('G', g), [('X', a)], F(1, k))
    for a in range(k):
        for ell in range(k + 1):
            for h in range(k):
                config(('R', a, ell), [('Y', a, h)], F(1, k + 1))
            for r in range(k):
                config(('R', a, ell), [('Z', a, r)], F(1, k * (k + 1)))
    return machines, times, configs


def explicit_pair(k, left, right):
    # Return (left-config index, right-config index, joint mass), or None for product.
    if left[0] == right[0] == 'G':
        return [(a, (a + 1) % k, F(1, k)) for a in range(k)]
    if left[0] == right[0] == 'R' and left[1] == right[1]:
        return ([(h, (h + 1) % k, F(1, k + 1)) for h in range(k)]
                + [(k + r, k + (r + 1) % k, F(1, k * (k + 1)))
                   for r in range(k)])
    if left[0] != 'V' and right[0] == 'V':
        reverse = explicit_pair(k, right, left)
        return None if reverse is None else [(j, i, weight) for i, j, weight in reverse]
    if left[0] == 'V' and right[0] == 'G':
        a = left[1]
        return ([(0, b, F(1, k * (k - 1))) for b in range(k) if b != a]
                + [(1, a, F(1, k))]
                + [(1, b, F(k - 2, k * (k - 1))) for b in range(k) if b != a])
    if left[0] == 'V' and right[0] == 'R' and left[1] == right[1]:
        return ([(0, k + r, F(1, k * (k + 1))) for r in range(k)]
                + [(0, h, F(1, k * k * (k + 1))) for h in range(k)]
                + [(1, h, F(k - 1, k * k)) for h in range(k)])
    return None


def audit(k):
    machines, times, configs = build(k)
    coverage = defaultdict(F)
    unions = {}
    config_count = 0
    eligibility = defaultdict(int)
    for machine in machines:
        for job in times[machine]:
            eligibility[job] += 1
        assert sum((weight for _, weight in configs[machine]), F(0)) == 1
        unions[machine] = frozenset().union(*(jobs for jobs, _ in configs[machine]))
        for jobs, weight in configs[machine]:
            assert weight >= 0
            assert sum((times[machine][job] for job in jobs), F(0)) <= 1
            for job in jobs:
                coverage[job] += weight
            config_count += 1
    assert all(weight == 1 for weight in coverage.values())
    assert set(coverage) == set(eligibility)
    assert len(machines) == k*k + 3*k - 1
    assert len(coverage) == 2*k*k + k
    explicit = product_count = checked_entries = implicit_entries = 0
    per_type = defaultdict(int)
    for left, right in combinations(machines, 2):
        joint = explicit_pair(k, left, right)
        if joint is None:
            # Product certificates are represented in factorized form. All support
            # configurations are pair-compatible because the support unions are disjoint.
            assert unions[left].isdisjoint(unions[right])
            lsum = sum((weight for _, weight in configs[left]), F(0))
            rsum = sum((weight for _, weight in configs[right]), F(0))
            assert lsum == rsum == 1
            for _, weight in configs[left]:
                assert weight * rsum == weight
            for _, weight in configs[right]:
                assert weight * lsum == weight
            product_count += 1
            implicit_entries += len(configs[left]) * len(configs[right])
            continue
        lm = defaultdict(F)
        rm = defaultdict(F)
        assert sum((weight for _, _, weight in joint), F(0)) == 1
        for i, j, weight in joint:
            assert weight >= 0
            if weight:
                assert configs[left][i][0].isdisjoint(configs[right][j][0])
            lm[i] += weight
            rm[j] += weight
            checked_entries += 1
        assert all(lm[i] == weight for i, (_, weight) in enumerate(configs[left]))
        assert all(rm[j] == weight for j, (_, weight) in enumerate(configs[right]))
        explicit += 1
        per_type[left[0] + '-' + right[0]] += 1
    assert explicit + product_count == len(machines)*(len(machines)-1)//2
    # No T=1 minimal-overload-star contraction is available for k>=3.
    irreducible = all(sum(times[machine].values(), F(0)) <= 1
                      or any(sum(times[machine].values(), F(0)) - value > 1
                             for value in times[machine].values())
                      for machine in machines)
    assert irreducible == (k >= 3)
    assert min(eligibility.values()) == k
    return {'k': k, 'machines': len(machines), 'jobs': len(coverage),
            'supported_configurations': config_count,
            'machine_pairs_checked': explicit + product_count,
            'explicit_compatible_pair_couplings': explicit,
            'explicit_joint_entries_checked': checked_entries,
            'factorized_product_pairs': product_count,
            'factorized_product_entries_represented': implicit_entries,
            'explicit_types': dict(per_type),
            'minimum_job_eligibility': min(eligibility.values()),
            'minimal_overload_star_irreducible': irreducible,
            'config_target': '1', 'proved_integer_optimum': str(F(2*k-1, k))}


if __name__ == '__main__':
    print(json.dumps({'python_version': platform.python_version(),
                      'arithmetic': 'fractions.Fraction; no tolerance',
                      'claim_scope': 'machine-wise configurations + all pairwise compatible couplings, no global joint distribution',
                      'source_of_coupling_formulas': 'boss2 root reconstruction; independent exact audit by frontier_algorithms',
                      'checks': [audit(k) for k in range(3, 13)],
                      'status': 'all exact assertions passed',
                      'limits': 'finite k=3..12 audit; general proof requires the displayed symbolic formulas'},
                     ensure_ascii=False, indent=2))
