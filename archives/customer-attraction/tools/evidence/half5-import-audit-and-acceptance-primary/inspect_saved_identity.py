"""Read frozen provenance and compare saved records; never run proof code."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def differences(a, b):
    return {k: [a.get(k), b.get(k)] for k in sorted(a.keys() | b.keys())
            if k not in a or k not in b or a[k] != b[k]}


def main():
    manifest = read(HERE / 'source-manifest.json')
    files = {Path(r['path']).name: ROOT / r['evidence_path'] for r in manifest}
    byte_checks = []
    for r in manifest:
        p = ROOT / r['evidence_path']
        ok = p.stat().st_size == r['size'] and sha(p) == r['sha256']
        assert ok, r['id']
        byte_checks.append({'id': r['id'], 'path': r['evidence_path'],
                            'bytes': r['size'], 'sha256': r['sha256'], 'equal': ok})
    original = read(files['original_global_replay.json'])
    parent = read(files['parent_main_replay.json'])
    local = read(files['parent_local_replay.json'])
    canonical = ROOT / 'archives/customer-attraction/tools/half5-exact'
    replay = ROOT / 'archives/customer-attraction/evidence/half5-exact/replay'
    code_bindings = []
    for report, code in [('metadata_and_K_check.json', 'check_metadata.py'),
                         ('old_engine_crosscheck.json', 'crosscheck_old_engine.py')]:
        expected = read(files[report])['code_sha256']
        actual = sha(files[code])
        assert expected == actual
        code_bindings.append({'report': report, 'code': code,
                              'reported': expected, 'current_bytes_sha256': actual})
    input_bindings = []
    for name, item in parent['source_lemmas'].items():
        p = canonical / item['path']
        actual = sha(p)
        assert actual == item['sha256']
        input_bindings.append({'family': name, 'path': str(p.relative_to(ROOT)),
                               'reported': item['sha256'], 'current_sha256': actual})
    rows = [files['original_global_replay_row_manifest.json'],
            files['parent_main_replay_row_manifest.json'], canonical / 'row_manifest.json']
    row_hashes = [sha(p) for p in rows]
    assert len(set(row_hashes)) == 1
    comparisons = {
        'original_vs_parent_main': differences(original, parent),
        'original_vs_mature_main': differences(original, read(replay / 'global.json')),
        'parent_vs_mature_main': differences(parent, read(replay / 'global.json')),
        'parent_vs_mature_local': differences(local, read(replay / 'local.json')),
    }
    assert all(set(v) == {'seconds'} for k, v in comparisons.items() if k.endswith('main'))
    assert set(comparisons['parent_vs_mature_local']) == {'elapsed_seconds'}
    result = {
        'scope': 'static source-byte and saved-record identity comparison only',
        'primary_count': len(manifest), 'primary_bytes': sum(r['size'] for r in manifest),
        'source_byte_checks': byte_checks, 'report_to_code_bindings': code_bindings,
        'main_input_bindings': input_bindings,
        'row_manifests': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p)} for p in rows],
        'saved_record_differing_top_level_fields': comparisons,
        'original_math_program_runs': 0, 'new_mathematical_domain_checks': 0,
        'historical_zip_read_or_certified': False,
        'transitive_old_engine_run_hashes_not_inferred': True,
    }
    (HERE / 'binding-review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'primary_count': len(manifest), 'primary_bytes': result['primary_bytes'],
                      'row_manifest_equal': True, 'code_bindings': len(code_bindings),
                      'main_inputs': len(input_bindings),
                      'report_differences': comparisons}, ensure_ascii=False))


if __name__ == '__main__':
    main()
