#!/usr/bin/env python3
"""两个固定原矩阵的精确证书审计；不是一般调度器或一般证明。

从正文常数定义重建全部finite entries，不调用证书生成器。
take/continue只核完整达界证书；sharp SAT例穷举全部5184合法分配。
输出必须是不存在的新文件，冻结证据不覆盖。
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def read(path):
    raw = path.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def actual_loads(jobs, assignment, machines):
    assert set(assignment) == set(jobs)
    loads = {m: F(0) for m in machines}
    for j, m in assignment.items():
        assert m in jobs[j] and m in loads, (j, m)
        loads[m] += F(jobs[j][m])
    return loads


def take_check(path):
    cert, sha = read(path)
    states, machines = {}, set()
    for a in range(1, 4):
        states[f'r_{a}'] = {'take1': {'u_1': '3/5', f'x_{a}': '2/5'}}
        states[f'm_{a}'] = {'off': {f'x_{a}': '1'},
                            'take2': {'u_2': '2/5', f'y_{a}': '3/5'}}
        states[f'l_{a}'] = {'off': {f'y_{a}': '1'},
                            'accept': {f'z_{a}': '1'}}
    jobs = {}
    for g, menu in states.items():
        jobs['J:' + g] = {'M:' + g + ':' + s: '1' for s in menu}
        for s, row in menu.items():
            private = 'M:' + g + ':' + s
            machines.add(private)
            for u, p in row.items():
                resource = 'R:' + u
                machines.add(resource)
                jobs[f'I:{g}:{s}:{u}'] = {private: p, resource: '1'}
    assert cert['states'] == states and cert['jobs'] == jobs
    assert len(cert['machines']) == len(set(cert['machines'])) == 26
    assert set(cert['machines']) == machines
    assert len(jobs) == cert['job_count'] == 30
    assert sum(map(len, jobs.values())) == cert['finite_entry_count'] == 57
    assert cert['selector_count'] == 9 and cert['incidence_count'] == 21
    loads = actual_loads(jobs, cert['assignment'], machines)
    assert loads == {m: F(v) for m, v in cert['loads'].items()}
    assert max(loads.values()) == F(cert['peak']) == F(8, 5)
    selected, bundles, seen, values = cert['selected_states'], cert['bundles'], set(), {}
    assert set(selected) == set(bundles) == set(states)
    for g, menu in states.items():
        row = menu[selected[g]]
        assert len(bundles[g]) == len(set(bundles[g]))
        assert set(bundles[g]) <= set(row) and not seen.intersection(bundles[g])
        seen.update(bundles[g])
        values[g] = sum((F(row[u]) for u in bundles[g]), F(0))
        assert cert['assignment']['J:' + g] == f'M:{g}:{selected[g]}'
        for u in bundles[g]:
            assert cert['assignment'][f'I:{g}:{selected[g]}:{u}'] == 'R:' + u
    assert values == {g: F(v) for g, v in cert['qualities'].items()}
    assert min(values.values()) == F(cert['partial_value']) == F(2, 5)
    return dict(sha256=sha, machines=26, jobs=30, finite_entries=57,
                exact_witness_peak='8/5', witness_partial_value='2/5',
                all_original_jobs_and_loads_checked=True,
                optimization_run=False,
                analytic_lower_bound='canonical proof, not inferred from this check')


def sharp_check(root_path, independent_path):
    root, root_sha = read(root_path)
    other, other_sha = read(independent_path)
    machines = [f'M{i}' for i in range(4)] + [f'C{i}' for i in range(4)]
    jobs = {}
    for i in range(4):
        jobs[f'q{i}'] = {f'M{i}': 8, f'M{(i + 1) % 4}': 10, f'C{i}': 5}
        pin = i if i < 2 else (i + 1) % 4
        jobs[f'b{i}'] = {f'M{pin}': 8, f'C{i}': 10}
    jobs.update({'u+': {'C0': 5, 'C1': 5}, 'u-': {'C2': 5, 'C3': 5}})
    assert root['machines'] == machines and root['jobs'] == jobs
    assert root['time_denominator'] == 10
    assert root['all_unlisted_times'] == 'infinity'
    rename_j = {f'q{i}': f'q_{i+1}' for i in range(4)}
    rename_j.update({f'b{i}': f'b_{i+1}' for i in range(4)})
    rename_j.update({'u+': 'u_1', 'u-': 'u_2'})
    rename_m = {f'{c}{i}': f'{c}_{i+1}' for c in 'MC' for i in range(4)}
    renamed = {rename_j[j]: {rename_m[m]: p for m, p in row.items()}
               for j, row in jobs.items()}
    assert other['jobs'] == renamed
    assert set(other['machines']) == set(rename_m.values())
    assert other['finite_entry_count'] == sum(map(len, jobs.values())) == 24
    assert other['unlisted_entries'] == 'infinite'
    hist = Counter()
    ordered = list(jobs)
    for destinations in product(*(list(jobs[j]) for j in ordered)):
        loads = dict.fromkeys(machines, 0)
        for j, m in zip(ordered, destinations):
            loads[m] += jobs[j][m]
        hist[max(loads.values())] += 1
    assert sum(hist.values()) == root['complete_assignments_enumerated'] == 5184
    assert min(hist) == root['exact_opt_units'] == other['minimum_peak_units'] == 15
    assert hist == Counter({int(k): v for k, v in root['peak_histogram_units'].items()})
    assert hist == Counter({int(k): v for k, v in other['peak_histogram'].items()})
    assert other['assignment_count'] == 5184 and other['below_15_assignments'] == 0
    assert max(actual_loads(jobs, root['one_optimal_assignment'], machines).values()) == 15
    assert max(actual_loads(renamed, other['one_optimal_assignment'], rename_m.values()).values()) == 15
    baseline = actual_loads(renamed, other['baseline_assignment'], rename_m.values())
    assert baseline == {m: F(v) for m, v in other['baseline_loads'].items()}
    assert max(baseline.values()) == 15
    return dict(root_sha256=root_sha, independent_sha256=other_sha,
                machines=8, jobs=10, finite_entries=24,
                complete_assignments=5184, exact_opt='3/2',
                peak_histogram_units=dict(sorted(hist.items())), denominator=10,
                scope='one explicit UNSAT source only; no general theorem from enumeration')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--take-certificate', type=Path, required=True)
    parser.add_argument('--sharp-certificate', type=Path, required=True)
    parser.add_argument('--independent-sharp-certificate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'frozen output already exists'
    result = {'scope': 'audit_only: two fixed explicit matrices, not a production solver',
              'take_continue': take_check(args.take_certificate),
              'sharp_three_halves': sharp_check(args.sharp_certificate,
                                                args.independent_sharp_certificate)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
