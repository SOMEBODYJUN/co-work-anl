"""New data reading only: compare preserved reports; do not run clock audits.

No original cost evaluator is imported or reconstructed.  Exact fractions from
the two old full-state outputs are compared across their different layouts.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(path):
    return json.loads(path.read_text())


def unwrap(report):
    if isinstance(report.get('result'), dict) and 'source_sha256' in report:
        return report['result']
    return report


def differences(old, new, path=''):
    if type(old) is not type(new):
        return [{'path': path, 'frozen': old, 'reused': new}]
    if isinstance(old, dict):
        return [row for key in sorted(old.keys() | new.keys())
                for row in (differences(old[key], new[key], path + '/' + key)
                            if key in old and key in new else
                            [{'path': path + '/' + key,
                              'frozen': old.get(key), 'reused': new.get(key)}])]
    if isinstance(old, list):
        if len(old) != len(new):
            return [{'path': path, 'frozen': old, 'reused': new}]
        return [row for index, (a, b) in enumerate(zip(old, new))
                for row in differences(a, b, path + '/' + str(index))]
    return [] if old == new else [{'path': path, 'frozen': old, 'reused': new}]


def opposite(state):
    return ''.join(str(1 - int(bit)) for bit in state)


def flip(state, player):
    return state[:player] + str(1 - int(state[player])) + state[player + 1:]


def display_interval(value):
    # Display a rigorously enclosing rational interval, never a float.
    scale = 10**6
    lower = value.numerator * scale // value.denominator
    return [str(Q(lower, scale)), str(Q(lower + 1, scale))]


def main():
    dependency = load(ROOT / 'dependency-manifest.json')['sources']
    comparison = load(ROOT / 'reused-comparison.json')['cases']
    all_diff = []
    for entry in comparison:
        path = entry['frozen_report'].split('/original/', 1)[1]
        saved = next(row['saved_path'] for row in dependency if row['path'] == path)
        frozen = load(ROOT / saved)
        reused = load(ROOT / 'reused-output' / (entry['program'] + '.json'))
        delta = differences(unwrap(frozen), unwrap(reused))
        assert all(row['path'] in ('/command', '/invocation') for row in delta)
        all_diff.append({'program': entry['program'], 'differences': delta,
                         'frozen_wrapper_keys': list(frozen) if frozen is not unwrap(frozen) else None})

    a = load(ROOT / 'reused-output/verify_full_uniform_clock.json')
    b = load(ROOT / 'reused-output/independent_full_uniform_clock.json')
    alpha = Q(a['alpha'])
    assert alpha == Q(b['alpha']) == Q(21, 20)
    for left, right in [('base_B', 'B'), ('base_eta', 'eta'), ('amplitude_M', 'M')]:
        assert Q(a[left]) == Q(b[right])
    assert a['weights'] == b['weights']
    assert len(a['all_states']) == len(b['total_costs']) == 16
    rows = []
    costs_checked = 0
    for row in a['all_states']:
        state, player, target = row['state'], row['player'], row['post_state']
        assert target == flip(state, player)
        exit = b['canonical_exits'][state]
        assert player == exit['player'] and target == exit['destination']
        base_current = Q(b['base_costs'][state][player])
        base_post = Q(b['base_costs'][target][player])
        current = Q(b['total_costs'][state][player])
        post = Q(b['total_costs'][target][player])
        assert Q(row['base_current']) == base_current
        assert Q(row['base_post']) == base_post
        assert Q(row['clock_current']) == current - base_current
        assert Q(row['clock_post']) == post - base_post
        assert Q(row['total_current']) == current and Q(row['total_post']) == post
        assert Q(row['base_margin']) == base_current - alpha * base_post
        assert Q(row['clock_margin']) == (current - base_current) - alpha * (post - base_post)
        gap = current - alpha * post
        assert Q(row['combined_margin']) == gap == Q(exit['margin'])
        assert gap == Q(row['base_margin']) + Q(row['clock_margin'])
        assert gap > Q(1, 500)
        signs = []
        for record in row['all_player_costs_and_margins']:
            i = record['player']
            new_state = flip(state, i)
            old_cost = Q(b['total_costs'][state][i])
            new_cost = Q(b['total_costs'][new_state][i])
            margin = Q(b['deviation_margins'][state][i])
            assert Q(record['current']) == old_cost and Q(record['post']) == new_cost
            assert Q(record['margin']) == margin == old_cost - alpha * new_cost
            assert old_cost == Q(b['total_costs'][opposite(state)][i])
            assert margin == Q(b['deviation_margins'][opposite(state)][i])
            signs.append('+' if margin > 0 else '-' if margin < 0 else '0')
            costs_checked += 1
        if state in b['author_frozen_intervals']:
            interval = b['author_frozen_intervals'][state]
            assert interval['player'] == player
            assert Q(interval['lower']) < gap < Q(interval['upper'])
        rows.append({'state': state, 'kind': row['kind'], 'player': player,
                     'target': target, 'selected_margin_rational_display_interval': display_interval(gap),
                     'all_player_margin_signs': signs})
    budget = a['uniform_budget']
    assert Q(budget['threshold']) == Q(b['uniform_budget_threshold'])
    assert Q(budget['delta']) == Q(b['delta'])
    for degree in (80, 90, 91):
        power = Q(budget['delta_power_' + str(degree)])
        assert power == Q(b['uniform_budget_powers'][str(degree)])
        slack = 4 * alpha**2 * Q(b['B']) * b['L'] * power - Q(b['eta'])
        assert slack == Q(b['uniform_budget_backmultiply_slack'][str(degree)])
        assert (slack > 0) == (degree < 91)
    assert costs_checked == 64
    output = {'provenance': 'new exact comparison of already-executed reports; no original audit rerun',
              'unwrap_policy': 'Only an outer result-dict execution envelope is unwrapped; original bytes remain preserved.',
              'all_six_complete_differences': all_diff,
              'cross_report_actual_cost_and_margin_pairs': costs_checked,
              'all_sixteen_selected_rows': rows,
              'budget_degrees_compared': [80, 90, 91],
              'new_game_cases': 0,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
