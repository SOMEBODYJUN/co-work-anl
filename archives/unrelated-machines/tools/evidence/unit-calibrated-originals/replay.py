#!/usr/bin/env python3
"""One replay of three frozen audits and four CLIs, with literal rechecks.

No imports of the constructors or their model kernel. Production scripts run
from byte-identical external snapshots so concurrent repository sync is safe.
The only new exhaustive search is the three small original counterexamples.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def literal_model(data):
    k, h = int(data['k']), int(data['h'])
    capacity = list(map(int, data['clause_capacities']))
    nodes, trees, roots, degree = {}, [], [], Counter()
    for v, variable in enumerate(data['variables']):
        pair = []
        for s, sign in enumerate(('positive', 'negative')):
            leaves = {tuple(row['path']): row['clause'] for row in variable[sign]}
            assert len(leaves) == len(variable[sign]) == k ** h
            prefixes = sorted({p[:d] for p in leaves for d in range(h)}, key=lambda p: (len(p), p))
            for p in prefixes:
                nodes[v, s, p] = len(nodes)
            degree.update(leaves.values())
            trees.append((v, s, leaves, prefixes))
            pair.append(nodes[v, s, ()])
        roots.append(pair)
    internal = len(nodes)
    starts, cursor = [], internal
    for a in capacity:
        starts.append(cursor)
        cursor += a
    jobs = []
    for v, pair in enumerate(roots):
        jobs.append({'kind': 'selector', 'variable': v, 'edges': [(u, F(1)) for u in pair]})
    for v, s, leaves, prefixes in trees:
        for parent in prefixes:
            for digit in range(k):
                path = parent + (digit,)
                u = nodes[v, s, parent]
                row = {'kind': 'port' if len(path) == h else 'edge', 'variable': v,
                       'sign': s, 'path': list(path), 'parent': u, 'edges': [(u, F(1, k))]}
                if len(path) == h:
                    c = leaves[path]
                    row.update(clause=c, external={'start': starts[c], 'count': capacity[c], 'time': F(1)})
                    row['edges'] += [(starts[c] + j, F(1)) for j in range(min(capacity[c], degree[c]))]
                else:
                    child = nodes[v, s, path]
                    row.update(child=child)
                    row['edges'].append((child, F(1)))
                jobs.append(row)
    listed = set(range(internal))
    for c, a in enumerate(capacity):
        listed.update(range(starts[c], starts[c] + min(a, degree[c])))
    if not cursor:
        listed.add(0)
    return jobs, roots, listed, max(cursor, 1), internal


def assigned_loads(jobs, sigma, full_m):
    assert len(jobs) == len(sigma)
    load = Counter()
    for row, u in zip(jobs, sigma):
        assert type(u) is int and 0 <= u < full_m
        edges = dict(row['edges'])
        if u in edges:
            p = edges[u]
        else:
            ext = row['external']
            assert ext['start'] <= u < ext['start'] + ext['count']
            p = F(1)
        load[u] += p
    return load


def recheck(data, result, counts):
    jobs, roots, listed, full_m, internal = literal_model(data)
    assert len(jobs) == len(result['jobs'])
    assert roots == result['roots'] and full_m == result['full_machine_count']
    for j, (expected, actual) in enumerate(zip(jobs, result['jobs'])):
        assert actual['job'] == j
        for key, value in expected.items():
            if key == 'edges':
                assert [(u, F(p)) for u, p in actual[key]] == value
            elif key == 'external':
                assert {**actual[key], 'time': F(actual[key]['time'])} == value
            else:
                assert actual[key] == value
    load = assigned_loads(jobs, result['sigma'], full_m)
    assert max(load.values(), default=F(0)) == F(result['makespan']) <= F(result['bound'])
    assert {r['machine'] for r in result['listed_loads']} == listed
    for row in result['listed_loads']:
        assert load[row['machine']] == F(row['load'])
    assert all(u in listed or value == 0 for u, value in load.items())
    assert all(value <= 1 for u, value in load.items() if u >= internal)
    assert F(result['omitted_unit_machine_load']) == 0
    counts['literal_complete_output_records'] += 1
    counts['literal_original_job_assignments'] += len(jobs)
    counts['literal_listed_machine_loads'] += len(listed)
    return jobs, full_m


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-dir', required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    run = Path(args.run_dir).resolve()
    run.mkdir(parents=True, exist_ok=False)
    source = run / 'source'
    shutil.copytree(base / 'original', source, ignore=shutil.ignore_patterns('__pycache__'))
    commands, counts = [], Counter()

    def command(name, script, arguments):
        argv = [sys.executable, str(source / script), *arguments]
        process = subprocess.run(argv, capture_output=True, text=True)
        (run / (name + '.stdout')).write_text(process.stdout)
        (run / (name + '.stderr')).write_text(process.stderr)
        commands.append({'name': name, 'argv': argv, 'cwd': str(Path.cwd()),
                         'exit_code': process.returncode, 'stdout': name + '.stdout', 'stderr': name + '.stderr'})
        dump(run / 'commands.json', commands)
        assert process.returncode == 0, name
        return json.loads((run / (name + '.json')).read_text())

    core = command('cardinality-audit', 'unit_readout_calibrated_cardinality.py', ['--output', str(run / 'cardinality-audit.json')])
    independent = command('independent-audit', 'unit_readout_calibrated_independent.py', ['--output', str(run / 'independent-audit.json')])
    literal = command('literal-audit', 'unit_readout_literal_gap.py', ['--output', str(run / 'literal-audit.json')])
    assert core['status'] == literal['status'] == 'passed'
    for case in core['actual_original_matrix_boundary_certificates']:
        recheck(case['input'], case['certificate'], counts)
    for case in literal['full_original_boundary_certificates']:
        recheck(case['instance'], case['result'], counts)

    examples = json.loads((source / 'unit_readout_calibrated_counterexamples.json').read_text())
    finite = []
    assert examples['code_sha256'] == sha256((source / 'unit_readout_calibrated_cardinality.py').read_bytes()).hexdigest()
    for case in examples['examples']:
        jobs, full_m = recheck(case['input'], case['certificate'], counts)
        assert all(not ('external' in row) or row['external']['count'] <= 2 for row in jobs)
        choices = [sorted(dict(row['edges'])) for row in jobs]
        best, enumerated = None, 0
        for sigma in product(*choices):
            load = assigned_loads(jobs, sigma, full_m)
            value = max(load.values(), default=F(0))
            best = value if best is None else min(best, value)
            enumerated += 1
        assert best == F(case['optimum']) and enumerated == case['assignments_enumerated']
        counts['counterexample_all_legal_assignments_enumerated'] += enumerated
        finite.append({'name': case['name'], 'original_jobs': len(jobs), 'optimum': str(best), 'all_legal_assignments': enumerated})

    # The three distinct production modes are exercised without rerunning audits.
    first = examples['examples'][0]['input']
    dump(run / 'calibrated-input.json', first)
    result = command('calibrated-cli', 'unit_readout_calibrated_cardinality.py', ['--input', str(run / 'calibrated-input.json'), '--mode', 'calibrated', '--r', '1', '--output', str(run / 'calibrated-cli.json')])
    recheck(first, result, counts)
    last = examples['examples'][2]['input']
    dump(run / 'bounded-input.json', last)
    result = command('bounded-cli', 'unit_readout_calibrated_cardinality.py', ['--input', str(run / 'bounded-input.json'), '--mode', 'bounded', '--D', '8', '--output', str(run / 'bounded-cli.json')])
    recheck(last, result, counts)
    unary = {'k': 1, 'h': 1, 'variables': [{'id': 0, 'positive': [{'path': [0], 'clause': 0}], 'negative': [{'path': [0], 'clause': 0}]}], 'clause_capacities': [1]}
    denominator = 10 ** 5000 + 151
    z = F(1, denominator)
    witness = [str(z), str(z), str(1-z)]
    dump(run / 'witness-input.json', unary)
    dump(run / 'witness-t.json', witness)
    result = command('witness-cli', 'unit_readout_calibrated_cardinality.py', ['--input', str(run / 'witness-input.json'), '--mode', 'witness', '--r', '1', '--t-file', str(run / 'witness-t.json'), '--output', str(run / 'witness-cli.json')])
    recheck(unary, result, counts)
    literal_input = {'instance': first, 'literal_weights': [['1/2', '1/2']]}
    dump(run / 'literal-input.json', literal_input)
    result = command('literal-cli', 'unit_readout_literal_gap.py', ['--input', str(run / 'literal-input.json'), '--output', str(run / 'literal-cli.json')])
    recheck(first, result, counts)

    report = {'status': 'passed', 'python': platform.python_version(), 'counts': dict(counts),
              'cardinality_counts': core['counts'], 'independent_counts': independent['counts'],
              'independent_giant_denominator_bit_length': independent['giant_denominator_bit_length'],
              'literal_counts': literal['counts'], 'counterexamples': finite,
              'commands': commands, 'source_sha256': {p.name: sha256(p.read_bytes()).hexdigest() for p in sorted(source.iterdir()) if p.is_file()},
              'scope': 'Three original finite audits and four distinct CLIs replayed once. New independent literal recheck covers only the saved explicit boundary/CLI/counterexample records. New exhaustive enumeration is only the three original small examples, 1698 schedules. No exact LP, infeasibility oracle, or generic OPT backend was implemented.'}
    dump(run / 'verification.json', report)
    print(json.dumps({'status': 'passed', 'counts': report['counts']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
