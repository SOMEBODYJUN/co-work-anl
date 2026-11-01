#!/usr/bin/env python3
"""Static delivery checks only: no source imports, BI, LP or Fraction audit."""
import ast
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BODY = ROOT / 'archives/customer-attraction/state/程序/静态安全值的有限搜索程序--程序.md'
RECEIPT = ROOT / 'cleanup/workspaces/Boss7/receipts-round15/99f46e401eb918a3f747.json'


def read(path):
    return json.loads(path.read_text())


def verify(path, item):
    raw = path.read_bytes()
    assert len(raw) == item.get('bytes', item.get('size')), str(path)
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], str(path)


def main():
    manifest = read(HERE / 'artifact-manifest.json')
    for item in manifest['files']:
        verify(ROOT / item['path'], item)
    source = read(HERE / 'source-manifest.json')
    for item in source['sources']:
        verify(HERE / item['preserved_path'], item['source'])
    assert source['runtime_local_imports'] == []
    comparisons = read(HERE / 'comparison-manifest.json')['formal_objects']
    for item in comparisons:
        verify(ROOT / item['path'], item)
    shared = read(HERE / 'shared-audit-binding.json')['files']
    for item in shared:
        verify(ROOT / item['path'], item)

    json_files = sorted(p for p in HERE.rglob('*.json') if p.name != 'self-check.json')
    for path in json_files:
        read(path)
    python_files = sorted(HERE.rglob('*.py'))
    for path in python_files:
        ast.parse(path.read_text(), filename=str(path))
    local_links = []
    for document in [BODY, HERE / 'README.md']:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            target = target.strip('<>').split('#', 1)[0]
            if not target or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target):
                continue
            resolved = (document.parent / target).resolve()
            assert resolved.exists(), (str(document), target)
            local_links.append({'document': str(document.relative_to(ROOT)), 'target': target})

    event = read(HERE / 'replay/execution.json')
    assert event['inputs_before'] == event['inputs_after']
    for item in event['inputs_before']:
        # Recorded original absolute invocation paths are historical metadata.
        rel = 'original/search_security.py' if item['path'].endswith('/search_security.py') else 'related/random_best.json'
        verify(HERE / rel, item)
    for name, item in event['files'].items():
        verify(HERE / 'replay' / name, item)
    for key in ['original_Probe_initializations', 'original_solve_calls', 'original_integer_BI_calls', 'original_security_LP_calls']:
        assert event[key] == 1
    assert event['original_main_runs'] == event['random_candidates_regenerated'] == 0
    assert event['full_ordered_policy_certificate_generated'] is False
    assert event['independent_fraction_audit_run_here'] is False
    process = read(HERE / 'replay/process-capture.json')
    assert process['returncode'] == process['original_random_main_runs'] == 0
    for name, item in process['output_files'].items():
        verify(HERE / 'replay' / name, item)
    assert (HERE / 'replay/stderr.txt').read_bytes() == b''

    saved = read(HERE / 'related/random_best.json')
    result = read(HERE / 'replay/original-return.json')
    for field in ['ratio_W_over_nv', 'v_screen', 'query_screen', 'target']:
        assert result[field] == saved[field]
        assert result['matches_saved_fields'][field] is True
    assert result['weights'] == saved['weights']
    assert (result['n'], result['k'], result['scale']) == (5, 7, 60)
    assert (result['state_count'], result['terminal_count'], result['background_count']) == (792, 462, 210)
    assert result['target_welfare'] == 29
    assert result['target'] == [0, 0, 0, 0, 0, 5, 0]
    assert result['root_outcome_indices'] == [5]
    assert result['state_outcome_sizes'] == [1]
    assert result['ranges']['coefficient_max'] == 60
    assert result['ranges']['weighted_pay_max'] == 1596
    assert result['ranges']['integer_dot_product_upper_bound'] == 2040
    states = read(HERE / 'replay/outcome-sets.json')['states']
    terminal = read(HERE / 'replay/terminal-payments.json')
    assert len(states) == len({tuple(x['prefix_counts']) for x in states}) == 792
    assert len(terminal['terminal_counts']) == len(terminal['scaled_pay']) == 462
    assert terminal['scale'] == 60
    for counts, pay in zip(terminal['terminal_counts'], terminal['scaled_pay']):
        assert len(counts) == len(pay) == 7 and sum(counts) == 5
    for item in states:
        assert len(item['prefix_counts']) == 7 and 0 <= sum(item['prefix_counts']) <= 5
        assert len(item['terminal_indices']) == len(item['terminal_counts']) == 1
        index = item['terminal_indices'][0]
        assert 0 <= index < 462
        assert item['terminal_counts'][0] == terminal['terminal_counts'][index]

    sibling = HERE.parent / 'static-security-search-data'
    assert (HERE / 'related/random_best.json').read_bytes() == (sibling / 'original/random_best.json').read_bytes()
    point = read(sibling / 'point-audit.json')
    assert point['exact_point']['W'] == 29
    assert point['exact_point']['v_5'] == '29/5'
    assert point['exact_point']['W_over_5v'] == '1'
    assert point['scope']['BI'] == point['scope']['LP'] == 0
    assert point['unique_strategy']['ordered_tree_separately_enumerated'] is False
    scope = read(HERE / 'execution-scope.json')
    assert scope['original_random_main'] == scope['RNG_calls'] == 0
    assert scope['original_solve_calls'] == scope['original_integer_BI'] == scope['original_security_LP'] == 1
    receipt = read(RECEIPT)
    assert receipt['id'] == '99f46e401eb918a3f747'
    assert receipt['disposition'] == 'integrated'
    for key in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for']:
        assert receipt[key] is True
    for target in receipt['targets']:
        assert (ROOT / target).exists(), target

    report = {
        'status': 'PASS',
        'scope': 'static byte/structure/link/receipt checks only; no original imports, BI, LP, RNG or independent mathematical rerun',
        'own_artifact_fingerprints': len(manifest['files']),
        'original_source_bindings': len(source['sources']),
        'comparison_fingerprints': len(comparisons),
        'shared_audit_fingerprints': len(shared),
        'json_syntax_files': len(json_files),
        'python_AST_files': len(python_files),
        'local_links_checked': len(local_links),
        'receipt_targets': len(receipt['targets']),
        'serialized_count_states_checked': len(states),
        'serialized_terminal_rows_checked': len(terminal['terminal_counts']),
        'four_saved_result_fields_match': True,
        'source_and_input_unchanged': True,
        'links': local_links,
    }
    (HERE / 'self-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'links'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
