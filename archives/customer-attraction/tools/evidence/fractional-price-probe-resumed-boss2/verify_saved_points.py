"""Check the two frozen saved policies and explicitly new small-rational points.

No LP, set-valued BI, random discovery, or full fractional-menu optimization.
The input float point is interpreted as its actual Python binary64 value.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import collections
import hashlib
import json
import math
import time

BASE = Path(__file__).resolve().parent


def analyze(data, weights):
    p, m = data['topics'], data['players']
    pairs = data['best']['strategy']
    actions = {tuple(h): a for h, a in pairs}
    domain = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert len(actions) == len(pairs) and set(actions) == domain
    assert all(type(a) is int and 0 <= a < p for a in actions.values())

    def finish(prefix):
        h = tuple(prefix)
        while len(h) < m:
            h += (actions[h],)
        return h

    def utility(leaf, topic):
        return sum((r / sum((mask >> a) & 1 for a in leaf)
                    for mask, r in weights.items() if (mask >> topic) & 1), F(0))

    minimum = None
    minimum_at = None
    negative = 0
    checked = 0
    for h in sorted(domain, key=lambda x: (len(x), x)):
        a = actions[h]
        prescribed = utility(finish(h), a)
        for b in range(p):
            if b == a:
                continue
            difference = prescribed - utility(finish(h + (b,)), b)
            checked += 1
            negative += difference < 0
            if minimum is None or difference < minimum:
                minimum, minimum_at = difference, [list(h), a, b]
    leaf = finish(())
    counts = [leaf.count(a) for a in range(p)]
    record = data['best']['record']
    assert counts == record['counts'] and counts[record['topic']] > 0
    welfare = sum((r for mask, r in weights.items()
                   if any((mask >> a) & 1 for a in leaf)), F(0))
    support = record['menu_support']
    weight = F(record['menu_weight'])
    cover = sum((r * min(F(1), weight * sum((mask >> a) & 1 for a in support))
                 for mask, r in weights.items()), F(0))
    tau = len(support) * weight
    value = utility(leaf, record['topic'])
    denominator = math.lcm(*(r.denominator for r in weights.values()))
    return {
        'histories': len(domain), 'nonself_comparisons': checked,
        'negative_comparisons': negative, 'minimum_ic': str(minimum),
        'minimum_at': minimum_at, 'is_complete_history_SPE': negative == 0,
        'root_path': list(leaf), 'root_counts': counts,
        'root_welfare': str(welfare), 'selected_player_profit': str(value),
        'fixed_menu_cover': str(cover), 'fixed_menu_mass': str(tau),
        'fixed_menu_gap': str(cover - tau * value - welfare),
        'unit_scale': denominator,
        'unit_type_counts': {str(k): int(r * denominator) for k, r in weights.items()},
        'unit_total_customers': int(sum(weights.values()) * denominator),
        'scope': 'one saved full policy and one specified fractional comparison menu',
    }


def main():
    started = time.perf_counter()
    results = []
    for filename in ('fractional_m3p5.json', 'fractional_m4p6.json'):
        path = BASE / 'original' / filename
        raw = path.read_bytes()
        data = json.loads(raw)
        assert set(data) == {'claim', 'status', 'seed', 'topics', 'players', 'log', 'best'}
        assert set(data['best']) == {'record', 'weights_float', 'strategy'}
        p, m = data['topics'], data['players']
        assert len(data['best']['weights_float']) == (1 << p) - 1
        expected_keys = {'iteration', 'source', 'violation_float', 'counts', 'topic',
                         'menu_support', 'menu_weight', 'rows', 'elapsed'}
        for row in data['log']:
            assert set(row) == expected_keys
            assert len(row['counts']) == p and sum(row['counts']) == m
            assert row['counts'][row['topic']] > 0
            assert list(row['menu_support']) == sorted(set(row['menu_support']))
            assert all(0 <= a < p for a in row['menu_support'])
            assert row['rows'] > 0 and row['elapsed'] >= 0
            assert row['violation_float'] <= 0
        assert data['best']['record'] in data['log']
        floats = {i + 1: r for i, r in enumerate(data['best']['weights_float']) if r}
        binary = {k: F.from_float(v) for k, v in floats.items()}
        rounded = {k: F(v).limit_denominator(10**6) for k, v in floats.items()}
        menu_count = sum(math.comb(p, n) * (n - 2) for n in range(3, p + 1))
        results.append({
            'file': filename, 'sha256': hashlib.sha256(raw).hexdigest(),
            'topics': p, 'players': m, 'seed': data['seed'],
            'saved_log_rows': len(data['log']),
            'saved_iterations': [r['iteration'] for r in data['log']],
            'fixed_menu_count_per_selected_policy': menu_count,
            'saved_rows_range': [min(r['rows'] for r in data['log']),
                                 max(r['rows'] for r in data['log'])],
            'saved_best_record': data['best']['record'],
            'policy_actions': dict(collections.Counter(a for h, a in data['best']['strategy'])),
            'binary64_input': analyze(data, binary),
            'new_small_rational_input': {
                'definition': 'each positive saved float independently limited to denominator <= 1000000',
                'weights': {str(k): str(v) for k, v in rounded.items()},
                **analyze(data, rounded),
            },
        })
    report = {
        'new_verifier_runs': 1, 'old_probe_main_runs': 0, 'LP_or_BI_runs': 0,
        'fixed_saved_point_interpretations_checked': 4,
        'results': results, 'elapsed_seconds': time.perf_counter() - started,
        'universal_B_bridge_or_half_proved': False,
    }
    output = BASE / 'saved-point-check.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
