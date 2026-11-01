#!/usr/bin/env python3
"""Static packaging checks only: never import or run any mathematical source."""
import ast
import gzip
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BODY = ROOT / 'archives/customer-attraction/state/程序/固定背景收益切片的有理秩与核基审计程序--程序.md'
RECEIPT = ROOT / 'cleanup/workspaces/Boss7/receipts-round17/6b6d01e6c77956272308.json'
R = HERE / 'replay'


def read(path):
    return json.loads(path.read_text())


def verify(path, item):
    b = path.read_bytes()
    assert len(b) == item.get('bytes', item.get('size')), str(path)
    assert hashlib.sha256(b).hexdigest() == item['sha256'], str(path)


def main():
    own = read(HERE / 'artifact-manifest.json')['files']
    for item in own:
        verify(ROOT / item['path'], item)
    sources = read(HERE / 'source-manifest.json')['sources']
    for item in sources:
        verify(ROOT / item['preserved_path'], item)
        assert item['full_file_reviewed'] is True
    assert [x['id'] for x in sources if x['role'] == 'primary'] == ['6b6d01e6c77956272308']
    comparisons = read(HERE / 'comparison-manifest.json')['files']
    for item in comparisons:
        verify(ROOT / item['path'], item)
    json_files = sorted(x for x in HERE.rglob('*.json') if x.name != 'self-check.json')
    for path in json_files:
        read(path)
    py_files = sorted(HERE.rglob('*.py'))
    for path in py_files:
        ast.parse(path.read_text(), filename=str(path))
    body = BODY.read_text()
    header = body.split('---', 2)[1]
    for name in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']:
        assert re.search(r'^' + name + ':', header, re.M), name
    links = []
    for document in [BODY, HERE / 'README.md']:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            target = target.strip('<>').split('#', 1)[0]
            if not target or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target):
                continue
            assert (document.parent / target).resolve().exists(), (str(document), target)
            links.append({'document': str(document.relative_to(ROOT)), 'target': target})
    event = read(R / 'execution.json')
    assert event['source_before'] == event['source_after']
    verify(HERE / 'original/audit_fixed_background.py', event['source_before'])
    for name, item in event['files'].items():
        verify(R / name, item)
    assert event['assertions_enabled'] is True
    assert event['original_function_call_events'] == {
        '<genexpr>': 811694, '<module>': 1, 'aggregate_coefficients': 546,
        'aggregate_rows': 77, 'main': 1, 'payoff': 135296, 'rank': 525,
        'residue_vector': 343, 'rows_from_customers': 187, 'verify_aggregate': 77,
        'verify_all_unit': 14, 'verify_case': 96, 'verify_four': 165, 'verify_six': 8}
    for key in ['helper_replacements', 'additional_original_helper_calls', 'optimization_calls',
                'SPE_solver_calls', 'new_independent_mathematical_audits']:
        assert event[key] == 0
    process = read(R / 'process-capture.json')
    assert process['returncode'] == 0
    for name, item in process['outputs'].items():
        verify(R / ('stderr.txt' if '.stderr.' in name else 'stdout.txt'), item)
    assert (R / 'stderr.txt').stat().st_size == 0
    assert (R / 'fixed_background_audit.json').read_bytes() == (HERE / 'related/fixed_background_audit.json').read_bytes()
    report = read(R / 'fixed_background_audit.json')
    assert report['status'] == 'passed'
    arrays = ['cases', 'aggregate_cases', 'all_unit_cases']
    assert read(R / 'stdout.txt') == {k: v for k, v in report.items() if k not in arrays}
    raw = gzip.decompress((R / 'original-observations.json.gz').read_bytes())
    assert len(raw) == event['observation_payload_uncompressed_bytes'] == 842445
    observed = json.loads(raw)
    summary = read(R / 'observation-summary.json')
    expected = {'base': [96, 18144, 265, 3514], 'four': [165, 14880, 0, 0],
                'aggregate': [77, 27776, 546, 11031], 'all_unit': [14, 55296, 0, 0],
                'six': [8, 0, 0, 0]}
    assert set(observed) == set(summary) == set(expected)
    syntax_strings = 0
    for family, records in observed.items():
        entries = sum(sum(len(row) for row in item.get('rows', [])) for item in records)
        vectors = sum(len(item.get('circuits', [])) for item in records)
        coefficients = sum(sum(len(row) for row in item.get('circuits', [])) for item in records)
        assert [len(records), entries, vectors, coefficients] == expected[family]
        assert summary[family] == {
            'calls': len(records), 'matrix_entries_serialized': entries,
            'basis_vectors_serialized': vectors, 'basis_coefficients_serialized': coefficients,
            'returned_records': [x['returned'] for x in records]}
        for item in records:
            if family == 'six':
                assert item['returned'] == 1 and 'rows' not in item and 'circuits' not in item
                continue
            M = item['M']
            rows = item['rows']
            expected_rows = {'base': 2*M, 'four': 4, 'aggregate': 3*M+1,
                             'all_unit': 2*M + item.get('k', 0)*(M+1)}[family]
            assert len(rows) == expected_rows
            columns = item['patterns']
            assert len(columns) == 1 << (2 + len(item['bg']))
            assert len({tuple(x) for x in columns}) == len(columns)
            assert all(len(x) == 2+len(item['bg']) and all(v in [0, 1] for v in x) for x in columns)
            assert all(len(row) == len(columns) for row in rows)
            assert all(len(vector) == len(rows) for vector in item.get('circuits', []))
            for row in rows + item.get('circuits', []):
                for value in row:
                    assert isinstance(value, str) and str(Fraction(value)) == value
                    syntax_strings += 1
            if family == 'four':
                assert item['returned'] == 1
            else:
                assert item['actual'] == item['returned']['rank']
    assert syntax_strings == 130641
    assert [x['returned'] for x in observed['base']] == report['cases']
    assert [x['returned'] for x in observed['aggregate']] == report['aggregate_cases']
    assert [x['returned'] for x in observed['all_unit']] == report['all_unit_cases']
    assert [x['k'] for x in observed['six']] == list(range(1, 9))
    assert report['case_count'] == 96 and report['four_slot_cases'] == 165
    assert report['aggregate_case_count'] == 77 and report['all_unit_case_count'] == 14
    assert report['circuit_vectors_checked'] == 265 and report['aggregate_circuit_vectors_checked'] == 546
    assert report['six_row_parameter_cases'] == 8
    scope = read(HERE / 'execution-scope.json')
    assert scope['original_main_runs'] == 1
    assert scope['old_root_review_runs'] == scope['new_independent_rank_or_nullspace_runs'] == 0
    assert scope['original_function_call_events'] == event['original_function_call_events']
    receipt = read(RECEIPT)
    assert receipt['id'] == '6b6d01e6c77956272308' and receipt['disposition'] == 'integrated'
    for key in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
        assert receipt[key] is True
    for target in receipt['targets']:
        assert (ROOT / target).exists(), target
    result = {'status': 'PASS', 'scope': 'Static fingerprints, source/event identity, captured array shapes/counts, canonical Fraction strings, links and receipt. No source import, rank, inner product, payoff, optimizer or SPE execution.',
              'own_fingerprints': len(own), 'source_bindings': len(sources), 'comparison_bindings': len(comparisons),
              'JSON_files': len(json_files), 'Python_AST_files': len(py_files),
              'local_links': len(links), 'receipt_targets': len(receipt['targets']),
              'old_new_report_bytes_equal': True, 'observed_matrix_entries': 116096,
              'observed_basis_vectors': 811, 'observed_basis_coefficients': 14545,
              'Fraction_syntax_strings': syntax_strings, 'original_function_call_events': event['original_function_call_events'],
              'links': links}
    (HERE / 'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'links'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
