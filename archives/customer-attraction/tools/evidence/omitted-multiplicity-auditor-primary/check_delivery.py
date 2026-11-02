"""Packaging checks only: never executes or imports the mathematical audit."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BODY = ROOT / 'archives/customer-attraction/state/程序/遗漏比较重数的逐客户与乘积精确审计器--程序.md'
SID = 'de59eb19dab1f01a5554'


def digest(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    assert manifest['primary_source_id'] == SID
    source = HERE / 'original/verify_omitted_optimal_multiplicity.py'
    record = digest(source)
    assert record['bytes'] == 2767
    assert record['sha256'] == '4778b8d18bb842882c352ab7dcd7e098f8eb3466828bbfb8bfe3af4d6767816d'
    assert manifest['preserved_primary']['sha256'] == record['sha256']
    expected = {
        'status': 'passed',
        'scope': 'exact coefficient and recurrence audit, not a search over games',
        'recurrence_cases': 36,
        'six_player_integer_column_checks': 2304,
        'six_player_fractional_column_checks': 2688,
        'F6_6': '2352949/6718464',
        'beta6': '6718464/2352949',
        'all_omissions_at_least_two_bound': '9071413/4705898',
        'strict_counterexample_unique_optimal_occurrence_floor': '340383/2352949',
    }
    assert json.loads((HERE / 'rerun/original_stdout.json').read_text()) == expected
    assert len((HERE / 'rerun/original_stdout.json').read_bytes()) == 413
    assert not (HERE / 'rerun/original_stderr.txt').read_bytes()
    metadata = json.loads((HERE / 'rerun/metadata.json').read_text())
    assert metadata['returncode'] == 0 and metadata['assertions_enabled']
    assert metadata['isolated_interpreter'] and metadata['source_unchanged_after_run']
    assert metadata['original_entry_invocations_this_task'] == 1
    body = BODY.read_text()
    assert body.startswith('---\n')
    front, remainder = body[4:].split('\n---\n', 1)
    assert 'id: "customer-attraction/omitted-comparator-multiplicity-exact-auditor"' in front
    assert 'kind: "program"' in front and 'type_tag: "程序"' in front
    assert SID in front and 'source_refs:' in front and remainder.strip()
    # This checker works both inside a stage tree and after repository integration.
    comparisons = json.loads((HERE / 'comparison.json').read_text())
    fallback = Path(comparisons['repository_read_root'])
    links = []
    for path in (BODY, HERE / 'README.md'):
        for raw in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in raw or raw.startswith('#'):
                continue
            target = (path.parent / raw.split('#')[0]).resolve()
            exists = target.is_file()
            if not exists and target.is_relative_to(ROOT):
                exists = (fallback / target.relative_to(ROOT)).is_file()
            links.append({'from': str(path.relative_to(ROOT)), 'target': raw, 'exists': exists})
    assert all(row['exists'] for row in links), links
    json_files = []
    for path in sorted(HERE.rglob('*.json')):
        json.loads(path.read_text())
        json_files.append(str(path.relative_to(ROOT)))
    report = {'status': 'passed', 'scope': 'Packaging only; no mathematical audit executed or imported.',
              'primary': record, 'nine_output_fields_equal_expected': True,
              'source_entry_invocations_by_this_checker': 0,
              'body': digest(BODY), 'json_files_parsed': json_files, 'links': links}
    (HERE / 'self-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'links': len(links), 'output_fields': len(expected),
                      'original_entry_runs_by_checker': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
