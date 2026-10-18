"""Audit-only explicit ordinary-UM checks for Cartesian tensor Exact v1.

No author Proof is imported.  All times/starts/loads are integer units of 1/D,
D=2**t.  The only exhaustive optimization is the full t=1 matrix (1024 choices).
t=2,3,4 use the supplied cyclic-state witness and finite intersection checks.

Requires a fresh --output-dir; neither directories nor files are overwritten.
Runtime/output are charged to the explicit matrix, never claimed polynomial in t.
"""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path


EXACT_SHA256 = '60299e46c9677b6fbfc94ac866bfe317151c83154c1fe7c14510eedc84050bac'


def binary_vectors(t):
    return list(product((0, 1), repeat=t))


def valid_incidence(g, ell, u):
    return all(((symbol % 2) ^ (slope & (symbol // 2))) == target
               for slope, target, symbol in zip(g, ell, u))


def construct_matrix(t):
    if not isinstance(t, int) or isinstance(t, bool) or t < 1:
        raise ValueError('Exact object requires integer t>=1')
    D = 2 ** t
    bits = binary_vectors(t)
    resources = list(product(range(4), repeat=t))
    machines = []
    resource_id = {}
    private_id = {}
    for u in resources:
        i = len(machines)
        resource_id[u] = i
        machines.append({'id': i, 'kind': 'resource', 'u': list(u)})
    for g in bits:
        for ell in bits:
            i = len(machines)
            private_id[(g, ell)] = i
            machines.append({'id': i, 'kind': 'private', 'g': list(g), 'ell': list(ell)})
    # Construct supports by scanning actual resource identities, not by the witness.
    supports = {(g, ell): [u for u in resources if valid_incidence(g, ell, u)]
                for g in bits for ell in bits}
    jobs = []
    for g in bits:
        jobs.append({'id': len(jobs), 'kind': 'selector', 'g': list(g),
                     'finite': [{'machine': private_id[(g, ell)], 'time_units': D}
                                for ell in bits]})
    for g in bits:
        for ell in bits:
            for u in supports[(g, ell)]:
                jobs.append({'id': len(jobs), 'kind': 'incidence', 'g': list(g),
                             'ell': list(ell), 'u': list(u),
                             'finite': [{'machine': private_id[(g, ell)], 'time_units': 1},
                                        {'machine': resource_id[u], 'time_units': D}]})
    return {'scope': 'audit_only: normalized flat Cartesian tensor Exact v1',
            't': t, 'time_denominator': D, 'unlisted_processing_times': 'infinity',
            'machines': machines, 'jobs': jobs,
            'states': [{'g': list(g), 'ell': list(ell),
                        'private_machine': private_id[(g, ell)],
                        'resource_machines': [resource_id[u] for u in supports[(g, ell)]]}
                       for g in bits for ell in bits]}


def check_matrix(P):
    """Read the actual sparse finite table, including all original state jobs."""
    t, D = P['t'], P['time_denominator']
    assert t >= 1 and D == 2 ** t
    bits = set(binary_vectors(t))
    universe = set(product(range(4), repeat=t))
    machine_by_id = {x['id']: x for x in P['machines']}
    assert len(machine_by_id) == len(P['machines']) == 2 * D ** 2
    assert set(machine_by_id) == set(range(len(machine_by_id)))
    resource_id, private_id = {}, {}
    for machine in P['machines']:
        if machine['kind'] == 'resource':
            u = tuple(machine['u'])
            assert u in universe and u not in resource_id
            resource_id[u] = machine['id']
        else:
            assert machine['kind'] == 'private'
            key = (tuple(machine['g']), tuple(machine['ell']))
            assert key[0] in bits and key[1] in bits and key not in private_id
            private_id[key] = machine['id']
    assert set(resource_id) == universe
    assert set(private_id) == set(product(bits, bits))
    selectors, incidences = {}, set()
    supports = {key: set() for key in private_id}
    finite_count = 0
    assert len(P['jobs']) == D ** 3 + D
    assert {j['id'] for j in P['jobs']} == set(range(len(P['jobs'])))
    for job in P['jobs']:
        g = tuple(job['g'])
        assert g in bits
        row = {e['machine']: e['time_units'] for e in job['finite']}
        assert len(row) == len(job['finite']) and set(row) <= set(machine_by_id)
        assert all(type(v) is int and v > 0 for v in row.values())
        finite_count += len(row)
        if job['kind'] == 'selector':
            assert g not in selectors
            selectors[g] = job['id']
            assert row == {private_id[(g, ell)]: D for ell in bits}
        else:
            assert job['kind'] == 'incidence'
            ell, u = tuple(job['ell']), tuple(job['u'])
            assert ell in bits and u in universe
            # Direct coordinate membership from actual base-symbol labels.
            assert all(((u[i] % 2) + g[i] * (u[i] // 2)) % 2 == ell[i]
                       for i in range(t))
            identity = (g, ell, u)
            assert identity not in incidences
            incidences.add(identity)
            supports[(g, ell)].add(u)
            assert row == {private_id[(g, ell)]: 1, resource_id[u]: D}
    assert set(selectors) == bits and len(incidences) == D ** 3
    for (g, ell), actual in supports.items():
        expected = {u for u in universe if all(
            ((u[i] % 2) + g[i] * (u[i] // 2)) % 2 == ell[i] for i in range(t))}
        assert actual == expected and len(actual) == D
    assert finite_count == 2 * D ** 3 + D ** 2
    state_rows = {(tuple(s['g']), tuple(s['ell'])): s for s in P['states']}
    assert len(state_rows) == len(P['states']) == D ** 2
    for key, actual in supports.items():
        row = state_rows[key]
        assert row['private_machine'] == private_id[key]
        assert len(row['resource_machines']) == D
        assert set(row['resource_machines']) == {resource_id[u] for u in actual}
    if t == 1:
        assert supports == {((0,), (0,)): {(0,), (2,)},
                            ((0,), (1,)): {(1,), (3,)},
                            ((1,), (0,)): {(0,), (3,)},
                            ((1,), (1,)): {(1,), (2,)}}
    return resource_id, private_id, supports, finite_count


def cyclic_state(g):
    return g[1:] + g[:1]


def construct_assignment(P, resource_id, private_id):
    D = P['time_denominator']
    load = [0] * len(P['machines'])
    records = []
    for job in P['jobs']:
        g = tuple(job['g'])
        selected = cyclic_state(g)
        if job['kind'] == 'selector':
            destination = private_id[(g, selected)]
        else:
            ell, u = tuple(job['ell']), tuple(job['u'])
            a = tuple(symbol // 2 for symbol in u)
            export = ell == selected and a != (1,) * P['t']
            destination = resource_id[u] if export else private_id[(g, ell)]
        row = {e['machine']: e['time_units'] for e in job['finite']}
        processing = row[destination]
        start = load[destination]
        load[destination] += processing
        records.append({'job': job['id'], 'machine': destination,
                        'time_units': processing, 'start_units': start,
                        'finish_units': load[destination]})
    return {'t': P['t'], 'time_denominator': D,
            'witness': 'ell_i(g)=g_(i+1) cyclic; export selected incidences iff a!=allones',
            'selected_states': [{'g': list(g), 'ell': list(cyclic_state(g))}
                                for g in binary_vectors(P['t'])],
            'assignment': records,
            'machine_load_units': [{'machine': i, 'load_units': value}
                                   for i, value in enumerate(load)],
            'makespan_units': max(load),
            'makespan_rational': {'numerator': max(load), 'denominator': D}}


def check_assignment(P, sigma, resource_id, private_id):
    D, t = P['time_denominator'], P['t']
    jobs = {j['id']: j for j in P['jobs']}
    seen = set()
    load = [0] * len(P['machines'])
    intervals = [[] for _ in P['machines']]
    exports = Counter()
    resource_units = Counter()
    last_finish = 0
    for record in sigma['assignment']:
        j, machine = record['job'], record['machine']
        assert j in jobs and j not in seen
        seen.add(j)
        job = jobs[j]
        row = {e['machine']: e['time_units'] for e in job['finite']}
        assert machine in row
        p = row[machine]
        assert record['time_units'] == p
        start, finish = record['start_units'], record['finish_units']
        assert type(start) is int and type(finish) is int and start >= 0 and finish == start + p
        load[machine] += p
        intervals[machine].append((start, finish))
        last_finish = max(last_finish, finish)
        g = tuple(job['g'])
        selected = cyclic_state(g)
        if job['kind'] == 'selector':
            assert machine == private_id[(g, selected)]
        else:
            ell, u = tuple(job['ell']), tuple(job['u'])
            expected_export = ell == selected and any(symbol // 2 == 0 for symbol in u)
            if expected_export:
                assert machine == resource_id[u]
                exports[g] += 1
                resource_units[machine] += 1
            else:
                assert machine == private_id[(g, ell)]
    assert seen == set(jobs) and len(sigma['assignment']) == len(jobs)
    for x in intervals:
        x.sort()
        assert all(a[1] <= b[0] for a, b in zip(x, x[1:]))
    declared = {x['machine']: x['load_units'] for x in sigma['machine_load_units']}
    assert declared == dict(enumerate(load))
    assert max(load) == last_finish == sigma['makespan_units'] == D + 1
    assert sigma['makespan_rational'] == {'numerator': D + 1, 'denominator': D}
    assert sigma['time_denominator'] == D and sigma['t'] == t
    assert sigma['selected_states'] == [
        {'g': list(g), 'ell': list(cyclic_state(g))} for g in binary_vectors(t)]
    for g in binary_vectors(t):
        assert exports[g] == D - 1
    for (g, ell), i in private_id.items():
        assert load[i] == (D + 1 if ell == cyclic_state(g) else D)
    for i in resource_id.values():
        assert load[i] in (0, D) and resource_units[i] <= 1
    assert len(resource_units) == D * (D - 1)
    return {'all_original_jobs_assigned_once': len(seen),
            'eligible_assignments_checked': len(seen),
            'exported_selected_incidence_jobs': sum(exports.values()),
            'exports_per_group': D - 1,
            'used_resource_machines': len(resource_units),
            'unused_resource_machines': D ** 2 - len(resource_units),
            'makespan_units': D + 1, 'time_denominator': D,
            'no_overlap': True}


def complementary_intersections(P, supports, resource_id):
    """Every ORDERED complementary group pair and every indexed-state pair."""
    t, D = P['t'], P['time_denominator']
    bits = binary_vectors(t)
    certificates = []
    for g in bits:
        h = tuple(1 - x for x in g)
        for ell in bits:
            for other_ell in bits:
                intersection = supports[(g, ell)] & supports[(h, other_ell)]
                assert len(intersection) == 1
                actual = next(iter(intersection))
                # Independent closed coordinate solution, compared to actual P supports.
                a = tuple(x ^ y for x, y in zip(ell, other_ell))
                b = tuple(ell[i] ^ (g[i] & a[i]) for i in range(t))
                calculated = tuple(2 * a[i] + b[i] for i in range(t))
                assert actual == calculated
                certificates.append({'g': list(g), 'complement_g': list(h),
                                     'ell': list(ell), 'complement_ell': list(other_ell),
                                     'unique_resource': list(actual),
                                     'resource_machine': resource_id[actual]})
    assert len(certificates) == D ** 3
    return {'t': t, 'ordered_pairs_checked': len(certificates),
            'unordered_pairs_represented': len(certificates) // 2,
            'intersection_size_for_every_pair': 1, 'certificates': certificates}


def exhaustive_t1_actual_opt(P):
    if P['t'] != 1:
        raise ValueError('full assignment enumeration is permitted ONLY for t=1')
    best = None
    best_assignment = None
    histogram = Counter()
    count = 0
    choices = [job['finite'] for job in P['jobs']]
    for assignment in product(*choices):
        count += 1
        loads = [0] * len(P['machines'])
        for edge in assignment:
            loads[edge['machine']] += edge['time_units']
        peak = max(loads)
        histogram[peak] += 1
        if best is None or peak < best:
            best = peak
            best_assignment = [{'job': job['id'], 'machine': edge['machine']}
                               for job, edge in zip(P['jobs'], assignment)]
    assert count == 1024 and best == 3 and P['time_denominator'] == 2
    return {'t': 1, 'complete_assignments_enumerated': count,
            'exact_OPT_units': best, 'time_denominator': 2,
            'exact_OPT_rational': {'numerator': 3, 'denominator': 2},
            'peak_units_histogram': dict(sorted(histogram.items())),
            'one_optimal_original_assignment': best_assignment}


def write_new_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def reject_float(value):
    if isinstance(value, float):
        raise AssertionError('floating-point value entered exact audit output')
    if isinstance(value, dict):
        for k, v in value.items():
            reject_float(k)
            reject_float(v)
    elif isinstance(value, (tuple, list)):
        for v in value:
            reject_float(v)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    root = Path(args.output_dir)
    root.mkdir(exist_ok=False)
    summary = {'implementation': 'audit_only', 'source_exact_sha256': EXACT_SHA256,
               'no_general_theorem_certification': True,
               'brute_scope': 'only t=1 complete ordinary P; never t>=2', 'cases': []}
    for t in range(1, 5):
        P = construct_matrix(t)
        resource_id, private_id, supports, finite_count = check_matrix(P)
        sigma = construct_assignment(P, resource_id, private_id)
        actual = check_assignment(P, sigma, resource_id, private_id)
        intersections = complementary_intersections(P, supports, resource_id)
        D = 2 ** t
        counts = {'groups': D, 'indexed_states': D ** 2,
                  'private_machines': D ** 2, 'resource_machines': D ** 2,
                  'machines': 2 * D ** 2, 'incidence_jobs': D ** 3,
                  'selector_jobs': D, 'jobs': len(P['jobs']),
                  'sparse_finite_processing_entries': finite_count,
                  'dense_processing_entries_if_materialized': len(P['jobs']) * len(P['machines'])}
        row = {'t': t, 'counts': counts, 'actual_assignment_check': actual,
               'ordered_complementary_group_state_pairs_checked': intersections['ordered_pairs_checked'],
               'minimum_witness_export_mass': {'numerator': D - 1, 'denominator': D},
               'optimization_enumerated': t == 1}
        if t == 1:
            brute = exhaustive_t1_actual_opt(P)
            reject_float(brute)
            write_new_json(root / 't1_full_original_opt_enumeration.json', brute)
            row['complete_original_assignments_enumerated'] = brute['complete_assignments_enumerated']
        for value in (P, sigma, intersections, row):
            reject_float(value)
        write_new_json(root / ('t%d_sparse_P.json' % t), P)
        write_new_json(root / ('t%d_all_original_job_schedule.json' % t), sigma)
        write_new_json(root / ('t%d_all_complementary_intersections.json' % t), intersections)
        summary['cases'].append(row)
    reject_float(summary)
    write_new_json(root / 'summary.json', summary)
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(root.iterdir()) if p.is_file()}
    manifest = {'audit_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'source_exact_sha256': EXACT_SHA256, 'files': files}
    write_new_json(root / 'manifest.json', manifest)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
