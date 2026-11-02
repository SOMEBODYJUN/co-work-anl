"""Verify preserved bytes, execution events and report arithmetic; no source import/BI."""
from argparse import ArgumentParser
from fractions import Fraction
from pathlib import Path
import ast
import hashlib
import json


def fingerprint(path):
    raw = path.read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def verify():
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / 'source-manifest.json').read_text())
    assert manifest['primary_count'] == 4
    assert manifest['primary_bytes'] == 15810
    assert sum(r['size'] for r in manifest['rows']) == 15810
    originals = {}
    for row in manifest['rows']:
        path = base / 'original' / row['path']
        assert fingerprint(path) == (row['size'], row['sha256'])
        assert row['full_file_read'] is True
        raw = path.read_bytes()
        git_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert git_blob == row['blob']
        originals[path.name] = path
        if path.suffix == '.py':
            ast.parse(path.read_text())  # Parse only; never execute a source node.
        else:
            json.loads(path.read_text())
    comparisons = json.loads((base / 'comparison-manifest.json').read_text())
    assert comparisons['comparison_count'] == len(comparisons['rows']) == 7
    for row in comparisons['rows']:
        assert fingerprint(base / row['path']) == (row['size'], row['sha256'])
    events = []
    for case, stem, output_size in [
        ('blind', 'insurer_blind_audit', 2532),
        ('sharp', 'insurer_three_sharp_audit', 5683),
    ]:
        directory = base / 'runs' / case
        event = json.loads((directory / 'event.json').read_text())
        assert event['case'] == case
        assert event['original_entry_invocations'] == 1
        assert event['returncode'] == 0
        assert event['PYTHONOPTIMIZE'] == '0'
        assert event['PYTHONDONTWRITEBYTECODE'] == '1'
        assert event['source_unchanged_after_run'] is True
        assert event['byte_identical_to_frozen_report'] is True
        assert event['structured_identical_to_frozen_report'] is True
        assert event['source_sha256'] == fingerprint(originals[stem + '.py'])[1]
        assert (directory / (stem + '.py')).read_bytes() == originals[stem + '.py'].read_bytes()
        assert (directory / (stem + '.json')).read_bytes() == originals[stem + '.json'].read_bytes()
        assert fingerprint(directory / (stem + '.json')) == (output_size, event['output_sha256'])
        assert event['frozen_report_sha256'] == event['output_sha256']
        assert (directory / 'stderr.txt').read_bytes() == b''
        assert event['additional_random_search_or_new_parameters'] == 0
        assert event['canonical_repository_solver_or_optimizer_calls'] == 0
        assert event['parent_seven_input_or_author_compiler_entries'] == 0
        events.append({'case': case, 'recorded_original_entry_invocations': 1,
                       'returncode': 0, 'output_bytes': output_size,
                       'wall_seconds_recorded': event['wall_seconds']})
    blind = json.loads(originals['insurer_blind_audit.json'].read_text())
    assert (base / 'runs/blind/stdout.txt').read_bytes() == originals['insurer_blind_audit.json'].read_bytes()
    assert [r['m'] for r in blind['insurers']] == list(range(2, 7))
    for row in blind['insurers']:
        m = row['m']
        nodes = sum(m ** d for d in range(m))
        assert row['node_action_checks'] == 2 * m * nodes
        assert row['modes']['compliant'] == {'path': [0] + [1] * (m - 1),
                                            'root_payoff': '2', 'nodes': nodes}
        assert row['modes']['punitive'] == {'path': [0, 0] + [1] * (m - 2),
                                          'root_payoff': '1', 'nodes': nodes}
    insurer_checks = sum(r['node_action_checks'] for r in blind['insurers'])
    assert insurer_checks == 120552
    product = blind['product']
    assert product == {'m': 4, 'old_scale': 2, 'delta': '1',
                       'actual': [[2, 0], [1, 1], [1, 1], [1, 1]],
                       'checks': 22620, 'old_gap': '-18', 'new_gap': '-21'}
    assert product['checks'] == 12 * sum(12 ** d for d in range(4))
    assert Fraction(product['new_gap']) == Fraction(product['old_gap']) - 3 * Fraction(product['delta'])
    assert sum([2, 5, 1, 4, 1]) * product['old_scale'] == 26
    assert 26 - 2 * 22 == -18
    assert (26 + 7) - 2 * (22 + 5) == -21
    sharp = json.loads(originals['insurer_three_sharp_audit.json'].read_text())
    assert sharp['case_count'] == len(sharp['cases']) == 34
    assert sum(r['outcome_pairs'] for r in sharp['cases']) == sharp['outcome_pairs'] == 750
    assert sum(r['positive_pairs'] for r in sharp['cases']) == sharp['positive_pairs'] == 90
    assert json.loads((base / 'runs/sharp/stdout.txt').read_text()) == {
        k: v for k, v in sharp.items() if k != 'cases'}
    for i, row in enumerate(sharp['cases']):
        assert set(row) == {'m', 'themes', 'customers', 'core', 'outcome_pairs', 'positive_pairs', 'max_delta'}
        assert 0 <= row['positive_pairs'] <= row['outcome_pairs']
        assert (Fraction(row['max_delta']) > 0) == (row['positive_pairs'] > 0)
        if i < 10:
            m = i // 2 + 2
            assert row['m'] == row['themes'] == m
            assert row['core'] == i % 2
            assert row['customers'] == 2 * m - 1 + i % 2
            assert row['max_delta'] == '1'
    be = json.loads((base / 'runs/blind/event.json').read_text())
    se = json.loads((base / 'runs/sharp/event.json').read_text())
    assert be['native_ordered_tree_BI_and_full_replay'] is True
    assert be['native_fixed_seed_generated_subtheme_cases'] == 0
    assert se['native_set_valued_count_BI'] is True
    assert se['native_fixed_seed_generated_subtheme_cases'] == 24
    assert se['native_seed'] == 7362129
    assert be['stdout_identical_to_report'] is True
    assert se['stdout_identical_to_report'] is False
    closure = json.loads((base / 'manifest.json').read_text())
    for row in closure['files']:
        assert fingerprint(base / row['path']) == (row['size'], row['sha256'])
    return {
        'status': 'passed-preserved-files-and-arithmetic-only',
        'primary_sources': 4, 'primary_bytes': 15810, 'comparison_snapshots': 7,
        'existing_execution_events_reused': events,
        'insurer_node_action_checks_reported': insurer_checks,
        'product_node_action_checks_reported': product['checks'],
        'combined_node_action_checks_reported': insurer_checks + product['checks'],
        'sharp_cases_reported': 34, 'sharp_ordered_outcome_pairs_reported': 750,
        'sharp_positive_delta_assertions_reported': 90,
        'source_imports': 0, 'original_entry_invocations_during_this_check': 0,
        'source_function_calls': 0, 'BI_calls': 0, 'random_input_generation_calls': 0,
        'canonical_solver_or_optimizer_calls': 0,
        'limitation': 'Checks byte/event binding and stored report arithmetic; does not rerun source assertions or establish universal mathematics.',
    }


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('--out', type=Path, default=Path(__file__).with_name('verification.json'))
    args = ap.parse_args()
    result = verify()
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
