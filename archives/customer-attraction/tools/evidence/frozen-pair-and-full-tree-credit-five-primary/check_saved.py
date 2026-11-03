"""Read preserved bytes and check report arithmetic only; never import the top-level audit."""
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
    sources = json.loads((base / 'source-manifest.json').read_text())
    assert sources['primary_count'] == len(sources['rows']) == 5
    assert sources['primary_bytes'] == sum(r['size'] for r in sources['rows']) == 25769
    originals = {}
    for row in sources['rows']:
        path = base / 'original' / row['path']
        raw = path.read_bytes()
        assert fingerprint(path) == (row['size'], row['sha256'])
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == row['blob']
        originals[path.name] = path
        if path.suffix == '.py':
            tree = ast.parse(path.read_text())
            assert not any(isinstance(node, ast.If) and '__name__' in ast.unparse(node.test) for node in tree.body)
        elif path.suffix == '.json':
            json.loads(path.read_text())
    compared = json.loads((base / 'comparison-manifest.json').read_text())
    assert compared['comparison_count'] == len(compared['rows']) == 21
    for row in compared['rows']:
        assert fingerprint(base / row['path']) == (row['size'], row['sha256'])
    report = json.loads(originals['frozen_pair_old_families_audit.json'].read_text())
    assert set(report) == {'candidate_status', 'two_player_old_certificates', 'PB_old_background_family'}
    assert report['candidate_status'] == 'OPEN; these old-family checks do not prove FROZEN-PAIR'
    two = report['two_player_old_certificates']
    assert len(two) == 2
    expected_two = [
        {'old_family': 'terminal_reply_transport: |A|=2h, |B|=h, h=1', 'last_after_A': 0,
         'complete_history_actions': {'empty': 0, 'A': 0, 'B': 0},
         'checked_IC_including_self': 6, 'actual_leaf': [0, 0], 'profits': ['1', '1'],
         'frozen_root_queries': ['1', '1'], 'pair_minus_max_query': '1'},
        {'old_family': 'terminal_reply_transport: |A|=2h, |B|=h, h=1', 'last_after_A': 1,
         'complete_history_actions': {'empty': 0, 'A': 1, 'B': 0},
         'checked_IC_including_self': 6, 'actual_leaf': [0, 1], 'profits': ['2', '1'],
         'frozen_root_queries': ['2', '1/2'], 'pair_minus_max_query': '1'},
    ]
    assert two == expected_two
    for row in two:
        assert len(row) == 8
        assert sum(map(Fraction, row['profits'])) - max(map(Fraction, row['frozen_root_queries'])) == Fraction(row['pair_minus_max_query'])
    pb = report['PB_old_background_family']
    assert len(pb) == 14
    assert pb['old_family'] == 'round5/menu/pair_attack.md fixed published constants'
    assert pb['scope'] == 'Only algebra of the already proved PB actual path; no new SPE certification'
    assert pb['parameters'] == {'k': 3, 'd': 20, 'q': 12, 't': 10, 'r': 2475, 'Q': 2063, 'H': 100000, 'M': 1000000000}
    assert pb['unused_real_blocks'] == 0
    assert pb['single_greedy_real_blocks_per_segment'] == 1648
    assert pb['double_greedy_real_blocks_per_segment'] == 412
    assert 1648 + 412 == pb['parameters']['Q'] - pb['parameters']['k']
    assert 1648 + 2 * 412 == pb['parameters']['r'] - 3
    u = Fraction(pb['first_three_payoff_u'])
    root_query = Fraction(pb['root_frozen_query_max'])
    upper = Fraction(pb['all_position_frozen_query_upper'])
    pair_lower = Fraction(pb['all_position_pair_lower'])
    assert pair_lower == 2 * u
    assert Fraction(pb['first_pair_margin']) == pair_lower - root_query > 0
    assert Fraction(pb['all_position_margin_lower']) == pair_lower - upper > 0
    assert 0 < root_query <= upper < pair_lower
    assert Fraction(pb['strict_root_IC_margin_per_segment']) > 0
    assert Fraction(pb['greedy_profit_lower_minus_u']) > 0
    return {
        'status': 'passed-source-fingerprints-syntax-and-frozen-report-arithmetic-only',
        'primary_sources': 5, 'primary_bytes': 25769, 'comparison_snapshots': 21,
        'original_report_top_level_fields': 3, 'two_player_record_fields_each': 8,
        'PB_record_fields': 14, 'PB_parameters': 8,
        'original_two_player_IC_checks_reported': 12,
        'original_two_player_IC_checks_reexecuted': 0,
        'PB_games_or_parameters_generated': 0, 'PB_f_or_g_function_evaluations': 0,
        'source_entry_invocations': 0, 'source_imports': 0, 'source_function_calls': 0,
        'BI_LP_random_or_large_tree_calls': 0,
        'limit': 'Checks the stored numbers against each other; does not reproduce the source audit, certify its historical process, prove the PB full tree, or decide the general frozen-pair bridge.',
    }


if __name__ == '__main__':
    result = verify()
    Path(__file__).with_name('verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
