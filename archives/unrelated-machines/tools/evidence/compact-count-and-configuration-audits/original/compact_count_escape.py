#!/usr/bin/env python3
"""紧凑共享逃逸族的配置、全部pair和单行探针证书核验。"""
from collections import defaultdict, Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import capacity_one_star_pair as old_pair
import row_count_probe as probe


def build(k):
    if isinstance(k, bool) or not isinstance(k, int) or not 2 <= k <= 8:
        raise ValueError("explicit audit builder accepts 2<=k<=8")
    nblocks = 2*k*k
    ng = nblocks-2*k
    machines = ([('V', a) for a in range(nblocks)] + [('G', g) for g in range(ng)]
                + [('R', a, r) for a in range(nblocks) for r in range(k+1)] + [('E',)])
    times = {i: {} for i in machines}
    cfg = {i: [] for i in machines}
    for a in range(nblocks):
        x = ('X', a)
        times['V', a][x] = F(1)
        cfg['V', a] = [(frozenset([x]), F(1, k)),
                       (frozenset(('Z', a, s) for s in range(k)), F(k-1, k))]
        for g in range(ng):
            times['G', g][x] = F(1)
            cfg['G', g].append((frozenset([x]), F(1, nblocks)))
        for s in range(k):
            y, z = ('Y', a, s), ('Z', a, s)
            times['E',][y] = F(1, k)
            times['V', a][z] = F(1, k)
            for r in range(k+1):
                times['R', a, r][y] = F(1)
                times['R', a, r][z] = F(1)
        for r in range(k+1):
            cfg['R', a, r] = ([(frozenset([('Y', a, s)]), F(1, k+1)) for s in range(k)]
                              + [(frozenset([('Z', a, s)]), F(1, k*(k+1))) for s in range(k)])
    cfg['E',] = [(frozenset(), F(1))]
    return machines, times, cfg


def pair(k, left, right):
    nblocks = 2*k*k
    if left[0] == right[0] == 'G':
        return [(a, (a+1) % nblocks, F(1, nblocks)) for a in range(nblocks)]
    if left[0] != 'V' and right[0] == 'V':
        answer = pair(k, right, left)
        return None if answer is None else [(j, i, w) for i, j, w in answer]
    if left[0] == 'V' and right[0] == 'G':
        a = left[1]
        return ([(0, b, F(1, k*(nblocks-1))) for b in range(nblocks) if b != a]
                + [(1, a, F(1, nblocks))]
                + [(1, b, F(1, nblocks)-F(1, k*(nblocks-1)))
                   for b in range(nblocks) if b != a])
    return old_pair.explicit_pair(k, left, right)


def audit(k):
    machines, times, cfg = build(k)
    jobs = sorted(set().union(*(set(row) for row in times.values())))
    expected_m = 2*k**3+6*k*k-2*k+1
    expected_n = 4*k**3+2*k*k
    assert len(machines) == expected_m and len(jobs) == expected_n
    coverage = defaultdict(F)
    unions = {}
    for i in machines:
        unions[i] = frozenset().union(*(s for s, _ in cfg[i]))
        assert sum((w for _, w in cfg[i]), F(0)) == 1
        for s, w in cfg[i]:
            assert w >= 0 and sum((times[i][j] for j in s), F(0)) <= 1
            for j in s:
                coverage[j] += w
        total = sum(times[i].values(), F(0))
        assert total <= 1 or any(total-p > 1 for p in times[i].values())
    assert set(coverage) == set(jobs) and all(w == 1 for w in coverage.values())
    assert min(sum(j in times[i] for i in machines) for j in jobs) >= 4
    explicit = factorized = entries = 0
    for left, right in combinations(machines, 2):
        joint = pair(k, left, right)
        if joint is None:
            assert unions[left].isdisjoint(unions[right])
            factorized += 1
            continue
        lm, rm = defaultdict(F), defaultdict(F)
        for a, b, w in joint:
            assert w >= 0
            if w:
                assert cfg[left][a][0].isdisjoint(cfg[right][b][0])
            lm[a] += w
            rm[b] += w
            entries += 1
        assert all(lm[a] == w for a, (_, w) in enumerate(cfg[left]))
        assert all(rm[b] == w for b, (_, w) in enumerate(cfg[right]))
        explicit += 1
    p = [[times[i].get(j) for j in jobs] for i in machines]
    d = probe.domains(p, F(1))
    caps = probe.row_caps(p, F(1), d)
    assert all(c == (k if machines[i][0] in ('V', 'E') else 1) for i, c in enumerate(caps))
    # Run the actual optimizer on every forced edge for the smallest member.
    queries = 0
    if k == 2:
        for j in range(len(jobs)):
            for v in sorted(d[j]):
                result = probe.query(p, F(1), d, v, j)
                assert result is not None and result[0] == p[v][j]
                counts = Counter(result[1])
                assert all(counts[i] <= caps[i] for i in range(len(p)) if i != v)
                assert result[1][j] == v
                assert all(a in d[b] for b, a in enumerate(result[1]))
                queries += 1
    return {'k': k, 'machines': expected_m, 'jobs': expected_n,
            'all_machine_pairs': explicit+factorized, 'explicit_pairs': explicit,
            'factorized_disjoint_support_pairs': factorized, 'explicit_pair_entries': entries,
            'actual_global_forced_edge_optimizer_queries': queries,
            'config_target': '1', 'symbolic_optimum': str(F(2*k-1, k))}


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    print(json.dumps({'title': '紧凑共享逃逸与全局基数探针的精确证书',
                      'python': platform.python_version(), 'arithmetic': 'Fraction/integer',
                      'sources': {n: hashlib.sha256((root/n).read_bytes()).hexdigest()
                                  for n in ('compact_count_escape.py', 'row_count_probe.py',
                                            'capacity_one_star_pair.py')},
                      'checks': [audit(k) for k in range(2, 6)],
                      'limits': 'finite certificates; no full schedule enumeration; optimizer queries only k=2'},
                     ensure_ascii=False, indent=2))
