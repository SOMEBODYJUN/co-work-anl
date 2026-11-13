"""Exact structural and scalar review of the saved R3002 joint point.

This does not import any old row generator, run an LP, or certify an SPE.
The saved augmented audit is reused for the old 3889 rows.  Every column,
including zero-weight joint/overlap columns, is parsed and round-tripped.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import runpy

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'work.py').exists())
OUT = Path(__file__).resolve().parent
TASK = 'customer-attraction-3a-3a-326858ed708d0ac6'


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    task = read(f'research/operations/map-v2/tasks/{TASK}.json')['definition']
    refs = task['context_plan']['reading_refs']
    for ref in refs:
        assert sha(ref['path']) == ref['sha256'], ref['path']

    pointpath = 'archives/customer-attraction/tools/evidence/R-3002-batch-20261031/deps/root_rows_joint_point.json'
    duplicate = 'archives/customer-attraction/tools/evidence/R-3002-residual-20261031/source/root_rows_joint_point.json'
    assert (ROOT / pointpath).read_bytes() == (ROOT / duplicate).read_bytes()
    d = read(pointpath)
    codecpath = 'map/edges/customer-attraction-3a-3a-12b47f0d6e765343/point-readable-codec.py'
    codec = runpy.run_path(str(ROOT / codecpath))
    e = codec['encode'](d)
    assert codec['decode'](e) == d
    assert e == read('map/edges/customer-attraction-3a-3a-12b47f0d6e765343/point-readable.json')

    columns = d['certificate']['columns']
    weights = [F(c['weight']) for c in columns]
    assert all(w >= 0 for w in weights)
    assert len(columns) == d['columns'] == 1905
    assert sum(w > 0 for w in weights) == d['certificate']['positive_columns'] == 175
    hist = [(i, c, weights[i]) for i, c in enumerate(columns) if c['kind'] == 'hist']
    assert len(hist) == 16
    for _, c, _ in hist:
        assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0', '1'}
        assert type(c['d']) is int and c['d'] >= 0
        assert len(c['hist']) == 8 and all(type(v) is int and v >= 0 for v in c['hist'])
    capital = weights[0]
    assert columns[0]['kind'] == 'K'
    optimum = sum((w for _, c, w in hist if c['d'] > 0), F())
    welfare = sum((w for _, c, w in hist if '1' in c['actual_bits']), F())
    root = sum((w / c['actual_bits'].count('1') for _, c, w in hist if c['actual_bits'][0] == '1'), F())
    assert optimum == F(d['certificate']['O']) == 1
    assert welfare == F(d['certificate']['W']) == F(d['exact_verification']['W']) < F(1, 2)
    assert 1 - 2 * welfare == F(d['certificate']['strict_half_gap']) == F(d['exact_verification']['strict_half_gap'])
    saved = read('archives/customer-attraction/tools/evidence/R-3002-batch-20261031/source/augmented_point_audit.json')
    assert saved['input_sha256'] == sha(pointpath)
    assert saved['old_generator_replay']['verified_rows'] == 3889
    assert d['rows'] == d['exact_verification']['verified_rows'] == 3894
    audits = read('archives/customer-attraction/tools/evidence/R-3002-batch-20261031/replay/root_rows_audit.json')
    results = []
    for j, cut in enumerate(d['cuts']):
        certpath = 'archives/customer-attraction/tools/evidence/R-3002-batch-20261031/research_4/' + Path(cut['file']).name
        assert sha(certpath) == cut['sha256'] == audits[j]['sha256']
        c = read(certpath)
        nu = c['multipliers_numerators']
        den = c['denominator']
        assert type(den) is int and den > 0
        assert all(type(v) is int and v >= 0 for v in nu.values())
        alpha = F(sum(v for k, v in nu.items() if k.startswith(('LASTO:', 'PAIRO:'))), den)
        beta = F(c['equality_numerator'] - sum(v for k, v in nu.items() if k.startswith('CAP:')), den)
        assert alpha == F(cut['a']) == F(audits[j]['alpha']) == F(c['verification']['a'])
        assert beta == F(cut['beta']) == F(audits[j]['beta']) == F(c['verification']['beta'])
        for s, i, t in c['copy_edges']:
            assert c['paths'][s][:i] == c['paths'][t][:i]
            assert i >= c['first_genuine'][s] and c['first_genuine'][t] == i + 1
        bound = 60 * (den + abs(c['equality_numerator']) + 12 * sum(nu.values()))
        assert bound == audits[j]['integer_bound'] < 2**63
        slack = root - alpha * optimum - beta * capital
        assert slack >= 0
        assert str(slack) == d['exact_verification']['new_root_slacks'][j] == saved['exact_root_slacks'][j]
        assert root == alpha * optimum + beta * capital + slack
        results.append({'file': Path(cut['file']).name, 'sha256': sha(certpath),
                        'alpha': str(alpha), 'beta': str(beta), 'slack': str(slack),
                        'saved_full_cube_states': audits[j]['states'],
                        'saved_full_cube_min_residual': audits[j]['min_residual'],
                        'saved_full_cube_zero_states': audits[j]['zero_states'],
                        'independently_recomputed_integer_bound': bound})
    assert all(F(r['slack']) > 0 for r in results[:-1]) and F(results[-1]['slack']) == 0

    report = {
        'scope': 'all saved column fields and exact scalar reconstruction; old 3889-row and full-cube results explicitly reused, not rerun; no SPE certification',
        'input_sha256': sha(pointpath), 'equal_duplicate_bytes': True,
        'complete_lossless_column_roundtrip': True,
        'column_counts': dict(Counter(c['kind'] for c in columns)),
        'all_weights_nonnegative': True, 'positive_columns': sum(w > 0 for w in weights),
        'zero_columns': sum(w == 0 for w in weights),
        'weight_dictionary_size': len(e['weight_dictionary']), 'group_dictionary_size': len(e['group_dictionary']),
        'K': str(capital), 'O': str(optimum), 'formal_actual_root_profit': str(root),
        'W': str(welfare), 'one_minus_two_W': str(1 - 2 * welfare),
        'half_inequality_slack_W_minus_O_over_two': str(welfare - optimum / 2),
        'new_root_rows': results,
        'histograms_complete': [{'column': i, **c} for i, c, _ in hist],
        'saved_old_generator_rows': 3889, 'saved_augmented_rows': 3894,
        'current_old_generator_replay': False, 'current_full_cube_replay': False,
        'current_full_SPE_verification': False,
        'checked_refs': refs,
    }
    (OUT / 'point-scalars-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['checked_refs', 'histograms_complete', 'new_root_rows']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
