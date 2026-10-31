#!/usr/bin/env python3
"""紧凑逃逸族：完整单机配置强制后的全配置LP证书。仅作精确审计。"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import compact_count_escape as family


def unit_pack(rows, demand, cfg, forced=None):
    """Pack rational job masses into unit singleton-configuration rows."""
    demand = dict(demand)
    available = list(rows)
    if forced is not None:
        row, chosen = forced
        assert row in available and len(chosen) <= 1
        available.remove(row)
        cfg[row] = [(frozenset(chosen), F(1))]
        for job in chosen:
            assert demand[job] == 1
            demand[job] -= 1
    jobs = iter(sorted(demand))
    job = next(jobs, None)
    for row in available:
        left = F(1)
        out = []
        while left and job is not None:
            mass = min(left, demand[job])
            if mass:
                out.append((frozenset([job]), mass))
                demand[job] -= mass
                left -= mass
            if demand[job] == 0:
                job = next(jobs, None)
        if left:
            out.append((frozenset(), left))
        cfg[row] = out
    assert all(v == 0 for v in demand.values()), demand


def extend(k, machine, chosen):
    """Return an actual full y certificate with y[machine,chosen]=1."""
    machines, times, _ = family.build(k)
    chosen = frozenset(chosen)
    if machine not in times or not chosen <= times[machine].keys():
        raise ValueError('unavailable machine/job')
    if sum((times[machine][j] for j in chosen), F(0)) > 1:
        raise ValueError('configuration exceeds target')
    n = 2*k*k
    a = [F(1, k)]*n
    escape = set()
    center_override = {}
    tag = machine[0]
    if tag == 'V':
        block = machine[1]
        if ('X', block) in chosen:
            a = [F(2*k-1, n-1)]*n
            a[block] = F(1)
            escape.update(('Y', block, s) for s in range(k-1))
        else:
            a[block] = F(0)
            other = (block+1) % n
            a[other] = F(2, k)
            escape.add(('Y', other, 0))
            escape.update(('Y', block, s) for s in range(max(0, k-len(chosen)-1)))
        center_override[block] = chosen
    elif tag == 'G':
        if chosen:
            block = next(iter(chosen))[1]
            a[block] = F(0)
            other = (block+1) % n
            a[other] = F(2, k)
            escape.add(('Y', other, 0))
        else:
            for block in range(k):
                a[block] = F(2, k)
                escape.add(('Y', block, 0))
    elif tag == 'R':
        block = machine[1]
        a[block] = F(0)
        other = (block+1) % n
        a[other] = F(2, k)
        escape.add(('Y', other, 0))
        if chosen and next(iter(chosen))[0] == 'Z':
            center_override[block] = frozenset(('Z', block, s) for s in range(k)) - chosen
    elif tag == 'E':
        escape = set(chosen)
    else:
        raise ValueError('unknown machine type')
    assert len(escape) <= k
    cfg = {}
    zmass = {}
    for block in range(n):
        zset = frozenset(('Z', block, s) for s in range(k))
        if block in center_override:
            c = center_override[block]
            cfg['V', block] = [(c, F(1))]
            for z in zset:
                zmass[z] = F(z not in c)
        else:
            cfg['V', block] = [(frozenset([('X', block)]), a[block]),
                               (zset, 1-a[block])]
            zmass.update((z, a[block]) for z in zset)
    globals_ = [('G', g) for g in range(n-2*k)]
    unit_pack(globals_, {('X', block): 1-a[block] for block in range(n)}, cfg,
              (machine, chosen) if tag == 'G' else None)
    for block in range(n):
        demand = {('Y', block, s): F(('Y', block, s) not in escape) for s in range(k)}
        demand.update((('Z', block, s), zmass['Z', block, s]) for s in range(k))
        rows = [('R', block, r) for r in range(k+1)]
        unit_pack(rows, demand, cfg, (machine, chosen) if tag == 'R' and machine[1] == block else None)
    cfg['E',] = [(frozenset(escape), F(1))]
    return machines, times, cfg


def validate(machines, times, cfg, machine=None, chosen=None):
    """Recompute every configuration, machine normalization and job cover."""
    cover = defaultdict(F)
    assert set(cfg) == set(machines)
    count = 0
    for i in machines:
        assert sum((w for _, w in cfg[i]), F(0)) == 1
        for c, weight in cfg[i]:
            assert weight >= 0 and c <= times[i].keys()
            assert sum((times[i][j] for j in c), F(0)) <= 1
            for j in c:
                cover[j] += weight
            count += 1
    jobs = set().union(*(set(row) for row in times.values()))
    assert set(cover) == jobs and all(v == 1 for v in cover.values())
    if machine is not None:
        chosen = frozenset(chosen)
        assert sum((w for c, w in cfg[machine] if c == chosen), F(0)) == 1
    return count


def all_configs(row):
    jobs = sorted(row)
    # The only many-job row is z; all finite times in this family are positive.
    cap = min(len(jobs), int(1/min(row.values())))
    for size in range(cap+1):
        for c in combinations(jobs, size):
            if sum((row[j] for j in c), F(0)) <= 1:
                yield frozenset(c)


def audit(k, full=False):
    machines, times, _ = family.build(k)
    queries = entries = 0
    kinds = defaultdict(int)
    digest = hashlib.sha256()
    for i in machines:
        if i[0] == 'E' and not full:
            jobs = sorted(times[i])
            cases = [frozenset()] + [frozenset([j]) for j in jobs]
            cases += [frozenset(jobs[:k]), frozenset(('Y', a, 0) for a in range(k))]
        else:
            cases = all_configs(times[i])
        for c in cases:
            mm, tt, yy = extend(k, i, c)
            entries += validate(mm, tt, yy, i, c)
            serial = [(row, [(sorted(cc), str(w)) for cc, w in yy[row]]) for row in sorted(yy)]
            digest.update(json.dumps([i, sorted(c), serial], separators=(',', ':')).encode())
            queries += 1
            kinds[i[0]] += 1
    return {'k': k, 'machines': len(machines), 'jobs': len(set().union(*(set(r) for r in times.values()))),
            'full_all_machine_configurations': full, 'queries': queries,
            'by_machine_type': dict(kinds), 'actual_configuration_entries_checked': entries,
            'certificate_stream_sha256': digest.hexdigest()}


if __name__ == '__main__':
    results = [audit(2, True), audit(3), audit(4)]
    bad = 0
    for i, c in [(('V', 0), [('X', 0), ('Z', 0, 0)]),
                 (('R', 0, 0), [('Y', 0, 0), ('Y', 0, 1)]),
                 (('E',), [('Y', 0, 0), ('Y', 0, 1), ('Y', 1, 0)])]:
        try:
            extend(2, i, c)
        except ValueError:
            bad += 1
        else:
            raise AssertionError('invalid config accepted')
    root = Path(__file__).resolve().parent
    print(json.dumps({'title': '完整单机配置强制的紧凑共享逃逸证书',
                      'python': platform.python_version(), 'arithmetic': 'Fraction, exact, no tolerance',
                      'command': 'python3 tests/audits/unrelated_machines/compact_config_probe.py',
                      'sources': {f: hashlib.sha256((root/f).read_bytes()).hexdigest()
                                  for f in ['compact_config_probe.py', 'compact_count_escape.py']},
                      'checks': results, 'invalid_configurations_rejected': bad,
                      'limits': 'k2 all configurations; k3/4 all non-z configurations plus stated z cases; no full schedule enumeration; not a hierarchy gap'},
                     ensure_ascii=False, indent=2))
