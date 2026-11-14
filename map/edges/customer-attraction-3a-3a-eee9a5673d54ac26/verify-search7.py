"""Check the saved Search7 endpoint from its original customer masks and full policy."""

from collections import Counter
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / 'archives/customer-attraction/tools/evidence'
LAST = EVIDENCE / 'r70-search7-program/last-point'
LOG = EVIDENCE / 'r70-search7-log'
LABELS = range(7)
PLAYERS = 6
SCALE = 60


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def counts(actions):
    return tuple(actions.count(a) for a in LABELS)


def child(count, action):
    return count[:action] + (count[action] + 1,) + count[action + 1:]


def masks(count):
    return sum(1 << a for a in LABELS if count[a])


def benefits(weight, count):
    values = []
    for action in LABELS:
        value = 0
        if count[action]:
            for mask, multiplicity in weight.items():
                if mask & (1 << action):
                    load = sum(count[a] for a in LABELS if mask & (1 << a))
                    assert load > 0 and SCALE % load == 0
                    value += multiplicity * (SCALE // load)
        values.append(value)
    return tuple(values)


def main():
    report = json.loads((LAST / 'point-audit.json').read_bytes())
    strategy_raw = (LAST / 'complete-strategy.json').read_bytes()
    detail_raw = (LAST / 'exact-details.json.gz').read_bytes()
    detail_json = gzip.decompress(detail_raw)
    details = json.loads(detail_json)
    log_raw = (LOG / 'original/scan_36155.txt').read_bytes()
    log_audit_raw = (LOG / 'log-audit.json').read_bytes()
    log_audit = json.loads(log_audit_raw)
    cover_raw = (LOG / 'static-coverages.json.gz').read_bytes()
    cover_json = gzip.decompress(cover_raw)
    cover_audit = json.loads(cover_json)
    assert digest(strategy_raw) == report['complete_strategy']['sha256']
    assert digest(detail_raw) == report['details_gzip']['sha256']
    assert digest(detail_json) == report['details_uncompressed_sha256']
    assert digest(log_raw) == log_audit['source_sha256']
    assert [digest(log_audit_raw), digest(cover_raw)] == [x['sha256'] for x in report['inputs']]
    assert digest(cover_raw) == log_audit['static_detail_gzip_sha256']
    assert digest(cover_json) == log_audit['static_detail_uncompressed_sha256']
    assert digest(cover_json) == report['coverage_uncompressed_sha256']

    lines = log_raw.decode().splitlines()
    records = log_audit['records']
    assert len(lines) == 24 and len(records) == len(cover_audit) == 12
    weights = []
    saved_ratios = []
    for index, (record, coverage) in enumerate(zip(records, cover_audit)):
        tokens = lines[2 * index].split()
        inputs = lines[2 * index + 1].split()
        assert tokens[::2][:6] == ['eval', 'ratio', 'W', 'OPT', 'margin', 'terminal']
        assert inputs[0] == 'weights' and len(tokens) == 18
        weight = dict(tuple(map(int, item.split(':'))) for item in inputs[1:])
        assert len(weight) == len(inputs) - 1
        assert all(1 <= mask <= 127 and mass > 0 for mask, mass in weight.items())
        assert weight == {row['mask']: row['unit_customers'] for row in record['positive_types']}
        assert all(row['topics'] == [a for a in LABELS if row['mask'] & (1 << a)] for row in record['positive_types'])
        assert int(tokens[1]) == record['evaluation'] == coverage['evaluation']
        assert tokens[3] == record['saved_ratio_token']
        assert list(map(int, tokens[11:])) == record['terminal_counts']
        terminal_mask = masks(record['terminal_counts'])
        welfare = sum(mass for mask, mass in weight.items() if mask & terminal_mask)
        optimum = sum(weight.values()) - min(weight[1 << a] for a in LABELS)
        margin = 2 * welfare - optimum
        assert int(tokens[5]) == record['W'] == welfare
        assert int(tokens[7]) == record['OPT6'] == optimum
        assert int(tokens[9]) == record['half_margin_2W_minus_OPT'] == margin > 0
        assert len(coverage['all_924_static_coverages']) == 924
        assert record['root_SPE_minimum_recomputed'] is False
        assert str(Fraction(welfare, optimum)) == record['exact_ratio']
        saved_ratios.append(Fraction(welfare, optimum))
        weights.append(weight)
    assert all(a > b for a, b in zip(saved_ratios, saved_ratios[1:]))
    weight = weights[-1]
    assert weight == weights[-2] | {48: 2} and 48 not in weights[-2]
    assert report['evaluation'] == records[-1]['evaluation'] == 47752
    assert records[-1]['positive_types'] == report['positive_types']
    assert len(weight) == 21 and sum(weight.values()) == 159
    private = [weight[1 << action] for action in LABELS]
    assert private == [3, 6, 6, 3, 7, 1, 6]

    count_layers = [[counts(t) for t in combinations_with_replacement(LABELS, depth)] for depth in range(7)]
    assert sum(map(len, count_layers)) == 1716 and len(count_layers[-1]) == 924
    payoff = {q: benefits(weight, q) for q in count_layers[-1]}
    assert len(details['payoffs']) == 924
    assert payoff == {tuple(row['counts']): tuple(row['scaled60_payoffs']) for row in details['payoffs']}
    cover = {q: sum(mass for mask, mass in weight.items() if mask & masks(q)) for q in count_layers[-1]}
    assert cover == {counts(row['sorted_labels']): row['coverage'] for row in cover_audit[-1]['all_924_static_coverages']}
    assert all(sum(a * b for a, b in zip(q, payoff[q])) == SCALE * cover[q] for q in payoff)
    assert max(cover.values()) == 158
    assert [q for q, value in cover.items() if value == 158] == [(1, 1, 1, 1, 1, 0, 1)]

    # Validate all rows of the set-valued recursion, independently of the saved policy.
    state_rows = details['all_1716_state_outcomes']
    saved_outcomes = {tuple(row['counts']): {tuple(q) for q in row['outcomes']} for row in state_rows}
    assert len(state_rows) == len(saved_outcomes) == 1716
    assert set(saved_outcomes) == {count for layer in count_layers for count in layer}
    assert all(len(row['outcomes']) == 1 for row in state_rows)
    for count in count_layers[-1]:
        assert saved_outcomes[count] == {count}
    for layer in reversed(count_layers[:-1]):
        for count in layer:
            menus = [saved_outcomes[child(count, a)] for a in LABELS]
            threshold = max(min(payoff[q][a] for q in menus[a]) for a in LABELS)
            computed = {q for a in LABELS for q in menus[a] if payoff[q][a] >= threshold}
            assert saved_outcomes[count] == computed
    terminal = (0, 2, 0, 0, 0, 0, 4)
    assert saved_outcomes[(0,) * 7] == {terminal}
    assert cover[terminal] == 131

    # Follow only the ordered policy and payoff table for the independent IC certificate.
    strategy = json.loads(strategy_raw)
    assert strategy['players'] == 6 and strategy['topics'] == 7
    actions = {tuple(row['history']): row['action'] for row in strategy['entries']}
    checks = {tuple(row['history']): row for row in details['all_19608_history_checks']}
    assert len(strategy['entries']) == len(details['all_19608_history_checks']) == 19608
    assert len(actions) == len(checks) == 19608
    assert set(actions) == set(checks) == {h for depth in range(6) for h in product(LABELS, repeat=depth)}
    assert all(type(a) is int and a in LABELS for a in actions.values())
    leaves = {h: h for h in product(LABELS, repeat=PLAYERS)}
    leaf_counts = {h: counts(h) for h in leaves}
    all_slacks = Counter()
    layer_results = []
    for depth in range(PLAYERS - 1, -1, -1):
        proper_slacks = []
        for h in product(LABELS, repeat=depth):
            action = actions[h]
            true_leaves = [leaves[h + (b,)] for b in LABELS]
            values = [payoff[leaf_counts[z]][b] for b, z in enumerate(true_leaves)]
            leaves[h] = true_leaves[action]
            slacks = [values[action] - value for value in values]
            row = checks[h]
            assert row['action'] == action
            assert tuple(row['actual_terminal']) == leaf_counts[leaves[h]]
            assert row['scaled60_payoff'] == values[action]
            assert row['scaled60_slacks'] == slacks
            assert slacks[action] == 0
            proper_slacks.extend(slacks[b] for b in LABELS if b != action)
            all_slacks.update(slacks)
        assert len(proper_slacks) == 6 * 7**depth and min(proper_slacks) > 0
        layer_results.append({'depth': depth, 'self_zero': 7**depth, 'nonself_strict': len(proper_slacks),
                              'minimum_nonself': str(Fraction(min(proper_slacks), SCALE))})
    root_path = leaves[()]
    assert root_path == tuple(report['actual_ordered_path']) == (6, 6, 6, 6, 1, 1)
    assert leaf_counts[root_path] == tuple(report['target_count']) == terminal
    root_payoffs = [Fraction(payoff[terminal][a], SCALE) for a in root_path]
    assert root_payoffs == [Fraction(269, 12)] * 4 + [Fraction(62, 3)] * 2
    assert list(map(str, root_payoffs)) == report['actual_payoffs'] and sum(root_payoffs) == 131
    assert all_slacks[0] == 19608 and all_slacks[6] > 0 and min(s for s in all_slacks if s) == 6
    assert sum(all_slacks.values()) == 137256
    assert sum(all_slacks.values()) - all_slacks[0] == 117648
    assert {str(Fraction(s, SCALE)): n for s, n in all_slacks.items()} == report['exact_slack_histogram']
    assert report['minimum_exact_slack'] == '0' and all(row['minimum_scaled60_slack'] == 0 for row in report['layers'])

    print(json.dumps({
        'status': 'PASS',
        'scope': 'Saved records checked for input and static quantities; exact SPE checked only for eval 47752.',
        'log_records': [row['evaluation'] for row in records],
        'unit_customers': sum(weight.values()),
        'private_counts': private,
        'recomputed_last_static_terminals': len(cover),
        'last_omit_coverages': [159 - n for n in private],
        'count_states_checked': len(saved_outcomes),
        'singleton_count_states': len(saved_outcomes),
        'ordered_histories_checked': len(actions),
        'all_comparisons': sum(all_slacks.values()),
        'nonself_strict': sum(all_slacks.values()) - all_slacks[0],
        'self_zero': all_slacks[0],
        'minimum_nonself': str(Fraction(6, SCALE)),
        'minimum_nonself_by_layer': list(reversed(layer_results)),
        'minimum_nonself_count': all_slacks[6],
        'root_path': root_path,
        'root_counts': terminal,
        'root_payoffs': list(map(str, root_payoffs)),
        'W': cover[terminal],
        'OPT6': max(cover.values()),
        'half_margin': 2 * cover[terminal] - max(cover.values()),
    }, indent=2))


if __name__ == '__main__':
    main()
