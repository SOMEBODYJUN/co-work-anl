#!/usr/bin/env python3
"""Run four new original entrypoints once and read every certificate record.

The semantic checker imports none of the generators or their independent reader.
The raw 1.76MB source is fully parsed; every job, eligible edge, owner and machine
load is checked, as are the source-assignment tables and all model metadata.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from importlib.metadata import version
from itertools import product
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def words(k, length):
    return list(product(range(k), repeat=length))


def certificates(data, source_hash):
    counts = Counter()
    assert set(data) == {'code_sha256', 'k', 'original_height', 'original_root_alpha', 'scope', 'sealed_original_tree_exact_OPT_by_known_proof', 'status', 'examples'}
    assert data['status'] == 'pass' and data['code_sha256'] == source_hash
    assert data['k'] == 4 and data['original_height'] == 3
    assert F(data['original_root_alpha']) == F(16, 27) and F(4, 9) < F(1, 2) <= F(16, 27)
    assert F(data['sealed_original_tree_exact_OPT_by_known_proof']) == F(7, 4)
    assert data['scope'] == 'explicit opened-bottom wiring only; module complete YES states, source NO physical escapes, one balanced source YES; not every designer wiring or general hardness'
    expected_names = {'private_module', 'unit_slot_source_NO_escape', 'single_endpoint_source_NO_escape', 'unit_slot_balanced_source_T_YES'}
    assert set(data['examples']) == expected_names

    def check(jobs, machines, sigma, loads, k, h, variables, slot_mode, masks=None, external=F(1), opens=None):
        internal = {(m['variable'], m['sign'], tuple(m['word'])): i for i, m in enumerate(machines) if m['kind'] == 'internal'}
        expected_nodes = {(v, s, p) for v in range(variables) for s in (0, 1) for depth in range(h) for p in words(k, depth)}
        assert set(internal) == expected_nodes
        assert len(internal) == sum(m['kind'] == 'internal' for m in machines)
        for m in machines:
            if m['kind'] == 'internal': assert set(m) == {'kind', 'variable', 'sign', 'word'}
            elif slot_mode:
                assert set(m) == {'kind', 'clause', 'sign_mask', 'slot'} and m['kind'] == 'clause_slot'
                assert m['sign_mask'] == masks[m['clause']]
            else:
                assert set(m) == {'kind', 'sign', 'word'} and m['kind'] == 'private_host'
        expected_jobs = {('selector', v) for v in range(variables)}
        expected_jobs |= {(kind, v, s, p) for v in range(variables) for s in (0, 1)
                          for length in range(1, h + 1) for p in words(k, length)
                          for kind in ('leaf_port' if length == h else 'tree_edge',)}
        seen, leaf_by_clause, actual_counts, per_variable = set(), {}, Counter(), Counter()
        pins, load = {}, [F(0)] * len(machines)
        assert len(jobs) == len(sigma) and len(loads) == len(machines)
        for row, u in zip(jobs, sigma):
            eligible = {int(i): F(z) for i, z in row['eligible'].items()}
            assert eligible and all(0 <= i < len(machines) and z >= 0 for i, z in eligible.items())
            assert type(u) is int and u in eligible
            counts['finite_eligible_entries'] += len(eligible)
            kind = row['kind']
            if kind == 'actual_fixed_preload':
                assert not slot_mode and set(row) == {'kind', 'eligible'} and len(eligible) == 1
                host, t = next(iter(eligible.items()))
                assert host not in pins and machines[host]['kind'] == 'private_host'
                assert t == (0 if host in opens else 1)
                pins[host] = t
            elif kind == 'selector':
                assert set(row) == {'kind', 'variable', 'eligible'}
                v = row['variable']; key = (kind, v)
                assert eligible == {internal[v, 0, ()]: F(1), internal[v, 1, ()]: F(1)}
                assert key not in seen; seen.add(key)
            else:
                v, s, p = row['variable'], row['sign'], tuple(row['word'])
                key = (kind, v, s, p)
                assert key in expected_jobs and key not in seen; seen.add(key)
                parent = internal[v, s, p[:-1]]
                if kind == 'tree_edge':
                    assert set(row) == {'kind', 'variable', 'sign', 'word', 'eligible'}
                    assert eligible == {parent: F(1, k), internal[v, s, p]: F(1)}
                elif slot_mode:
                    assert set(row) == {'kind', 'variable', 'sign', 'word', 'eligible', 'clause'}
                    c = row['clause']
                    slots = {i for i, m in enumerate(machines) if m['kind'] == 'clause_slot' and m['clause'] == c}
                    assert eligible == {parent: F(1, k), **{i: external for i in slots}}
                    assert s == ((masks[c] >> v) & 1)
                    leaf_by_clause.setdefault(c, []).append((v, s))
                    if u in slots:
                        actual_counts[c] += 1; per_variable[v] += 1
                else:
                    assert set(row) == {'kind', 'variable', 'sign', 'word', 'eligible', 'private_host'}
                    host = row['private_host']
                    assert machines[host] == {'kind': 'private_host', 'sign': s, 'word': list(p)}
                    assert eligible == {parent: F(1, k), host: F(1)}
                    if u == host: actual_counts[host] += 1
            load[u] += eligible[u]
        assert seen == expected_jobs
        assert load == list(map(F, loads))
        if slot_mode:
            assert not pins and set(leaf_by_clause) == set(range(len(masks)))
            for c, leaves in leaf_by_clause.items():
                assert len(leaves) == variables and {v for v, s in leaves} == set(range(variables))
        else:
            hosts = {i for i, m in enumerate(machines) if m['kind'] == 'private_host'}
            assert set(pins) == hosts and set(actual_counts) == opens
        counts['complete_certificates'] += 1
        counts['original_job_assignments'] += len(jobs)
        counts['all_machine_loads'] += len(machines)
        counts['fixed_preload_jobs'] += len(pins)
        return max(load, default=F(0)), [actual_counts[c] for c in range(len(masks))] if slot_mode else actual_counts, [per_variable[v] for v in range(variables)]

    private = data['examples']['private_module']
    assert set(private) == {'k', 'height', 'machines', 'profiles'} and private['k'] == 4 and private['height'] == 3
    assert len(private['machines']) == 170 and len(private['profiles']) == 3
    profile_names = ('all_positive_open_T_YES', 'all_negative_open_T_YES', 'only_pruned_negative_open_weak')
    for i, record in enumerate(private['profiles']):
        assert set(record) == {'name', 'open_hosts', 'original_jobs', 'sigma', 'actual_machine_loads', 'actual_makespan'}
        assert record['name'] == profile_names[i] and len(record['original_jobs']) == 297
        sign = int(i != 0)
        expected = {j for j, m in enumerate(private['machines']) if m['kind'] == 'private_host' and m['sign'] == sign and (i != 2 or all(z < 2 for z in m['word']))}
        assert len(record['open_hosts']) == len(expected) and set(record['open_hosts']) == expected
        maximum, _, _ = check(record['original_jobs'], private['machines'], record['sigma'], record['actual_machine_loads'], 4, 3, 1, False, opens=expected)
        assert maximum == F(record['actual_makespan']) == (F(3, 2) if i == 2 else F(1))
    summaries = []
    for name in sorted(expected_names - {'private_module'}):
        record = data['examples'][name]
        assert set(record) == {'A', 'actual_external_ports_per_clause', 'actual_machine_loads', 'actual_makespan', 'clause_slots', 'd', 'external_mode', 'height', 'internal_machine_count', 'k', 'machines', 'maximum_external_ports_per_clause', 'occurrences_per_sign', 'original_jobs', 'selected_leaf_ports', 'sigma', 'source_NO_all_assignments', 'source_assignment_T_YES', 'source_clause_masks', 'source_kind'}
        unit = record['external_mode'] == 'unit_slots'
        fullcube = record['source_kind'] == 'fullcube'
        assert record['k'] == 4 and record['height'] == 3 and record['A'] == 4 and record['d'] == 7
        assert record['occurrences_per_sign'] == 64 and record['internal_machine_count'] == 294
        assert record['clause_slots'] == (512 if unit else 128)
        assert len(record['machines']) == 294 + record['clause_slots'] and len(record['original_jobs']) == 1183
        masks = record['source_clause_masks']
        assert masks == (list(range(128)) if fullcube else [0] * 64 + [127] * 64)
        maximum, outgoing, per_variable = check(record['original_jobs'], record['machines'], record['sigma'], record['actual_machine_loads'], 4, 3, 7, True, masks, F(1) if unit else F(1, 4))
        assert outgoing == record['actual_external_ports_per_clause'] and max(outgoing) == record['maximum_external_ports_per_clause'] == 4
        assert sum(outgoing) == record['selected_leaf_ports'] == (56 if fullcube else 448)
        assert per_variable == ([8] * 7 if fullcube else [64] * 7)
        assert maximum == F(record['actual_makespan']) == (F(3, 2) if fullcube else F(1))
        if fullcube:
            assert record['source_assignment_T_YES'] is None
            table = record['source_NO_all_assignments']
            assert table == [{'source_assignment': x, 'all_true_clause': x ^ 127} for x in range(128)]
            for witness in table:
                assert (witness['source_assignment'] ^ masks[witness['all_true_clause']]).bit_count() == 7
                counts['source_NO_assignment_witnesses'] += 1
        else:
            assert record['source_assignment_T_YES'] == 7 and record['source_NO_all_assignments'] == []
            assert max((7 ^ mask).bit_count() for mask in masks) == 4
        summaries.append({'name': name, 'jobs': 1183, 'machines': len(record['machines']), 'makespan': str(maximum), 'ports_per_variable': per_variable})
    return dict(counts), summaries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-dir', required=True)
    args = parser.parse_args()
    base, run = Path(__file__).resolve().parent, Path(args.run_dir).resolve()
    run.mkdir(parents=True, exist_ok=False)
    repository = run / 'repository'
    audits, examples = repository / 'tests/audits/unrelated_machines', repository / 'examples/unrelated_machines'
    audits.mkdir(parents=True); examples.mkdir(parents=True)
    for p in (base / 'original').iterdir():
        if p.is_file(): shutil.copy2(p, (audits if p.suffix == '.py' else examples) / p.name)
    commands = []

    def command(name, filename, arguments=(), output=None):
        argv = [sys.executable, str(audits / filename), *map(str, arguments)]
        process = subprocess.run(argv, capture_output=True, text=True)
        (run / (name + '.stdout')).write_text(process.stdout)
        (run / (name + '.stderr')).write_text(process.stderr)
        commands.append({'name': name, 'argv': argv, 'cwd': str(Path.cwd()), 'exit_code': process.returncode, 'stdout': name + '.stdout', 'stderr': name + '.stderr'})
        dump(run / 'commands.json', commands)
        assert process.returncode == 0, name
        return json.loads(Path(output).read_text() if output else process.stdout)

    row_audit = command('row-audit', 'unit_readout_configuration_row_decomposition.py', ['--output', run / 'row-audit.json'], run / 'row-audit.json')
    row_input = {'k': 4, 's': 2, 'q': '1/3', 't': ['1'] * 4, 'c': ['2/3', '0', '0', '0']}
    dump(run / 'row-input.json', row_input)
    row_cli = command('row-cli', 'unit_readout_configuration_row_decomposition.py', ['--input', run / 'row-input.json', '--output', run / 'row-cli.json'], run / 'row-cli.json')
    assert row_cli['raw_lift'] == row_input['c'] and list(map(F, row_cli['cooccurrence_lift'])) == [0] * 4
    assert sum(F(c['weight']) for c in row_cli['configurations']) == 1
    assert sum(F(c['weight']) * c['incoming'] for c in row_cli['configurations']) == F(1, 3)
    assert all(not c['outgoing'] for c in row_cli['configurations'])
    generated = command('two-tree-generator', 'unit_readout_two_tree_certificates.py')
    frozen = examples / 'unit_readout_two_tree_actual_certificates.json'
    assert (run / 'two-tree-generator.stdout').read_bytes() == frozen.read_bytes()
    independent = command('two-tree-independent', 'unit_readout_two_tree_independent.py')
    tree_counts, tree_summaries = certificates(json.loads(frozen.read_text()), sha256((audits / 'unit_readout_two_tree_certificates.py').read_bytes()).hexdigest())
    example = json.loads((examples / 'unit_readout_configuration_threshold_examples.json').read_text())
    assert set(example) == {'scope', 'literal_gap_witness', 'closed_tree_parameters'}
    assert example['scope'] == 'Exact finite witnesses/parameters only; theorem proof is in the current account.'
    witness = example['literal_gap_witness']; instance = witness['instance']
    assert set(witness) == {'instance', 'literal_weights'} and instance['k'] == 3 and instance['h'] == 1
    assert instance['variables'] == [{'id': 0, 'positive': [{'path': [i], 'clause': 0} for i in range(3)], 'negative': [{'path': [i], 'clause': 1} for i in range(3)]}]
    assert instance['clause_capacities'] == [3, 1] and witness['literal_weights'] == [['3/4', '1/4']]
    assert [3*F(y) for y in witness['literal_weights'][0]] == [F(9, 4), F(3, 4)]
    parameters = []
    assert example['closed_tree_parameters'] == [[1,5],[2,3],[3,1],[4,1],[4,3],[5,7],[8,16],[12,32]]
    for k, h in example['closed_tree_parameters']:
        rhs = 2 * k ** (h-1)
        s = next(s for s in range(k) if (k-s) ** h <= rhs)
        threshold, optimum = F(1) + F(s,k), F(2) - F(1,k)
        parameters.append({'k': k, 'h': h, 's_min': s, 'feasible_lhs': (k-s)**h, 'rhs': rhs,
                           'previous_lhs': (k-s+1)**h if s else None, 'T_CONFIG': str(threshold),
                           'OPT_from_scoped_closed_tree_theorem': str(optimum), 'ratio': str(optimum/threshold)})
    report = {'status': 'passed', 'python': platform.python_version(), 'numpy': version('numpy'), 'scipy': version('scipy'),
              'row_counts': row_audit['counts'], 'row_max_support': row_audit['maximum_constructed_support_on_grid'],
              'tree_semantic_counts': tree_counts, 'tree_summaries': tree_summaries, 'original_independent_reader': independent,
              'generator_byte_equal_frozen': True, 'closed_tree_parameter_arithmetic': parameters,
              'literal_gap_witness': {'source_mass': ['9/4','3/4'], 'capacity': [3,1], 'given_algorithm_bound': '5/3',
                                      'actual_OPT1_reason': 'choose positive selector; send all three positive leaves to its three units; keep negative leaves at parent'},
              'commands': commands, 'source_sha256': {p.name: sha256(p.read_bytes()).hexdigest() for p in sorted((base / 'original').iterdir()) if p.is_file()},
              'scope': 'Exact finite single-row audit and one lift-clipping CLI; six full opened-tree certificates and all metadata/edges/owners/loads; eight arithmetic parameter checks. No general/global CONFIG solver, all-schedules OPT oracle, or sealed-tree matrix construction was run.'}
    dump(run / 'verification.json', report)
    print(json.dumps({'status': 'passed', 'row_counts': report['row_counts'], 'tree_counts': tree_counts}, ensure_ascii=False))


if __name__ == '__main__':
    main()
