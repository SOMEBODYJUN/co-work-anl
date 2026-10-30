#!/usr/bin/env python3
"""Inspect saved executions and exact source identity; never execute an audit.

The six successful runs predate this cleanup batch. This tool verifies and copies
their original records, outputs and frozen comparisons without manufacturing a
new run. It uses only JSON/bytes/hash inspection. Run from any working directory.
"""
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CACHE = REPO.parent / 'boss4-next-cache'
EVIDENCE = HERE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def copy_checked(src, dst, expected):
    assert sha(src) == expected, str(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        assert dst.read_bytes() == src.read_bytes(), str(dst)
    else:
        shutil.copyfile(src, dst)
    assert sha(dst) == expected


def diff(a, b, path='$'):
    if type(a) is not type(b):
        return [{'path': path, 'frozen': a, 'reused': b}]
    if isinstance(a, dict):
        result = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                result.append({'path': path + '.' + key,
                               'frozen': a.get(key), 'reused': b.get(key),
                               'missing_side': 'frozen' if key not in a else 'reused'})
            else:
                result.extend(diff(a[key], b[key], path + '.' + key))
        return result
    if isinstance(a, list):
        if len(a) != len(b):
            return [{'path': path, 'frozen': a, 'reused': b}]
        return [item for i, (x, y) in enumerate(zip(a, b))
                for item in diff(x, y, path + '[' + str(i) + ']')]
    return [] if a == b else [{'path': path, 'frozen': a, 'reused': b}]


def main():
    assigned = json.loads((CACHE / 'clock-executable-residual-candidate.json').read_text())
    clock = json.loads((EVIDENCE / 'clock/replay-manifest.json').read_text())
    linear = json.loads((EVIDENCE / 'linear-degree-audits/run-index.json').read_text())
    comparisons = json.loads((EVIDENCE / 'clock/replay-comparison.json').read_text())['cases']
    old_prov = json.loads((EVIDENCE / 'clock/provenance.json').read_text())['sources']
    old_prov += json.loads((EVIDENCE / 'linear-degree-audits/provenance.json').read_text())
    # Reports were comparison dependencies in the earlier clock batch, not
    # owned sources in that manifest; recover their exact frozen metadata from
    # inventory rather than inventing an ID from a local file.
    inventory = [json.loads(line) for line in (REPO / 'cleanup/inventory.jsonl').read_text().splitlines()]
    provenance = []
    records = []
    comparison_records = []
    for src in assigned:
        stem = Path(src['path']).stem
        assembly = stem == 'independent_multiclass_assembly'
        home = EVIDENCE / ('linear-degree-audits' if assembly else 'clock')
        old_code = home / 'original' / src['path']
        assert len((CACHE / src['path']).read_bytes()) == src['size']
        assert sha(old_code) == src['sha256']
        copy_checked(CACHE / src['path'], HERE / 'original' / src['path'], src['sha256'])
        if assembly:
            runs = [r for r in linear['attempts'] if r['script'] == src['path']]
            assert len(runs) == 1
            run = runs[0]
            frozen_path = home / 'original/evidence/runs/weighted_congestion/cyclic_clone/linear_degree_multiclass_assembly.json'
        else:
            runs = [r for r in clock['programs']
                    if any(str(a).endswith('/' + stem + '.py') for a in r['command_argv'])]
            assert len(runs) == 1
            run = runs[0]
            comp = next(c for c in comparisons if c['program'] == stem)
            frozen_path = REPO / comp['frozen_report']
        assert run['exit_code'] == 0
        assert run['source_sha256'] == src['sha256']
        output_path = Path(run['output'])
        if not output_path.is_absolute():
            output_path = REPO / output_path
        assert sha(output_path) == run['output_sha256']
        copied_output = HERE / 'reused-output' / (stem + '.json')
        copy_checked(output_path, copied_output, run['output_sha256'])
        rel_frozen = frozen_path.relative_to(home / 'original').as_posix()
        frozen_meta = next(x for x in inventory if x['path'] == rel_frozen)
        copy_checked(frozen_path, HERE / 'original' / rel_frozen, frozen_meta['sha256'])
        frozen = json.loads(frozen_path.read_text())
        # Two historical reports wrap stdout in an execution envelope. Retain
        # full envelope bytes; compare its result, exactly as original replay.
        unwrapped = (isinstance(frozen.get('result'), dict)
                     and 'source_sha256' in frozen)
        if unwrapped:
            assert frozen['source_sha256'] == src['sha256']
            frozen = frozen['result']
        reused = json.loads(output_path.read_text())
        differences = diff(frozen, reused)
        assert all(d['path'] == '$.command' for d in differences), differences
        assert bool(differences) == (stem in {
            'independent_actual_clock_geometry', 'verify_clock_margin_padding',
            'independent_multiclass_assembly'})
        comparison_records.append({
            'id': src['id'], 'program': stem,
            'frozen_report': ('original/' + rel_frozen),
            'frozen_sha256': frozen_meta['sha256'],
            'historical_execution_envelope_unwrapped_for_comparison': unwrapped,
            'reused_output': copied_output.relative_to(HERE).as_posix(),
            'all_differences': differences, 'mathematical_differences': [],
            'math_exactly_equal': True})
        provenance.append({**src, 'role': 'assigned-source',
                           'saved_as': 'original/' + src['path'],
                           'cache_hash_checked': True, 'prior_execution_source_hash_checked': True})
        provenance.append({**frozen_meta, 'role': 'frozen-report-comparison-only',
                           'saved_as': 'original/' + rel_frozen})
        records.append({'id': src['id'], 'program': stem,
                        'reuse_of_prior_execution': True,
                        'new_original_program_execution_in_this_batch': False,
                        'prior_manifest': str((home / ('run-index.json' if assembly else 'replay-manifest.json')).relative_to(REPO)),
                        'prior_record': run,
                        'current_source_cache_and_archived_code_hash': src['sha256'],
                        'reused_output': copied_output.relative_to(HERE).as_posix(),
                        'recomputed_output_sha256': sha(copied_output)})
    deps = [
        ('clock', 'examples/weighted_congestion/anchored_actual_clock_degree43.json'),
        ('linear-degree-audits', 'research/current/weighted_congestion/linear_degree_allstate_lower_bound.md')]
    for home, path in deps:
        meta = next(x for x in old_prov if x['path'] == path)
        copy_checked(EVIDENCE / home / 'original' / path, HERE / 'original' / path, meta['sha256'])
        provenance.append({**meta, 'role': 'input-or-proof-binding-dependency-only',
                           'saved_as': 'original/' + path})
    save('provenance.json', {
        'claim_commit': '1f45864cf2ba71ce392adba52bada8e83a3ea09c',
        'assigned_source_count': 6, 'dependency_or_frozen_report_count': 8,
        'sources': provenance})
    save('reused-run-manifest.json', {
        'policy': 'Reuse six already successful exact same-hash original executions. This inspection invokes no original audit.',
        'new_original_program_executions': 0, 'reused_successful_executions': 6,
        'prior_python': clock['python'], 'records': records})
    save('reused-comparison.json', {
        'policy': 'Recompute every JSON leaf difference. Only command differs in three cases; all source, proof, input, arithmetic, mathematical and count fields are compared without exclusions.',
        'cases': comparison_records})
    print(json.dumps({'assigned_source_hashes_checked_in_three_locations': 6,
                      'frozen_and_dependency_hashes_checked': 8,
                      'existing_output_hashes_checked': 6,
                      'reused_exit_zero_executions': 6,
                      'new_original_executions': 0,
                      'command_differences': sum(len(x['all_differences']) for x in comparison_records),
                      'mathematical_differences': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
