"""Bind saved policies/instances and review versions; no new IC/BI/payoff run.

Aggregates only the already-computed B7 table and original B8 observed slacks.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import gzip
import hashlib
import json

BASE = Path(__file__).resolve().parent


def unique_object(items):
    obj = {}
    for key, value in items:
        assert key not in obj
        obj[key] = value
    return obj


def read(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def run(repo):
    manifest = read(BASE / 'source-manifest.json')
    for source in manifest:
        raw = (BASE / source['saved_path']).read_bytes()
        assert len(raw) == source['size'] and hashlib.sha256(raw).hexdigest() == source['sha256']
    static = read(BASE / 'original/independent/child_profit_state_audit.json')
    full = read(BASE / 'original/independent/child_profit_state_full_audit.json')
    assert set(full) - set(static) == {'original_complete_SPE'}
    for key in static:
        if key != 'branches':
            assert static[key] == full[key]
    for a, b in zip(static['branches'], full['branches']):
        assert set(b) - set(a) == {'tail_profit_over_F3'}
        assert all(a[key] == b[key] for key in a)
    b7dir = repo / 'archives/customer-attraction/tools/evidence/aggregate-profit-state-and-stationary-refund-boss3'
    old_values = read(b7dir / 'replay/all-1296-ordered-tail-values.json')
    old_result = read(b7dir / 'replay/six-child-menu-exact-review.json')
    optimizer_counts = []
    for index, row in enumerate(full['branches']):
        values = old_values[index]['all_216_ordered_tail_values']
        optimum = max(F(v['profit']) for v in values)
        optimizers = [v['tail'] for v in values if F(v['profit']) == optimum]
        assert len(optimizers) == row['F3_ordered_optimizer_count']
        assert str(optimum) == row['F3']
        assert [list('ABCDEF')[a] for a in optimizers[0]] == row['F3_one_optimizer']
        previous = old_result['menu_rows'][index]
        assert previous['root'] == row['root_action']
        assert previous['tail'] == ''.join(row['tail'])
        for left, right in [('root_payoff', 'root_payoff'), ('tail_profit', 'tail_profit'),
                            ('F3', 'F3'), ('tail_to_F3', 'tail_profit_over_F3'),
                            ('slack_above_3_over_5', 'profit_slack')]:
            assert previous[left] == row[right]
        assert F(row['three_fifths_floor']) == F(3, 5) * optimum
        assert F(row['terminal_welfare']) == F(row['root_payoff']) + F(row['tail_profit'])
        optimizer_counts.append(len(optimizers))
    genuine = full['original_complete_SPE']
    assert genuine['verified_ordered_nodes'] == 259
    assert genuine['verified_action_comparisons_including_self'] == 1554
    assert genuine['minimum_incentive_gap'] == '0'
    assert genuine['actual_payoffs'] == old_result['genuine_fields_newly_checked_statically']['payoffs']
    assert genuine['F3_after_A'] == old_result['genuine_fields_newly_checked_statically']['F3_after_A']
    assert genuine['opportunity_gap'] == '25' and genuine['twice_root_utility'] == '18'

    certificate = read(BASE / 'original/construction/partial_core_tail_certificate.json')
    generated = read(BASE / 'runtime/time/partial_core_independent_audit.json')
    frozen = read(BASE / 'original/time/partial_core_independent_audit.json')
    assert generated == frozen
    identity = read(BASE / 'replay/original-return-observation-identity.json')
    raw = gzip.decompress((BASE / 'replay/original-return-observation.json.gz').read_bytes())
    assert len(raw) == identity['uncompressed_size']
    assert hashlib.sha256(raw).hexdigest() == identity['uncompressed_sha256']
    observation = json.loads(raw, object_pairs_hook=unique_object)
    assert certificate['instance']['topics'] == observation['native_topics'] == generated['topics']
    def interests(items):
        c = Counter()
        for item in items:
            c[tuple(item['topics'])] += item['multiplicity']
        return c
    assert interests(certificate['instance']['customers']) == interests(observation['native_unit_interest_multiplicities'])
    assert sum(interests(certificate['instance']['customers']).values()) == 60
    assert certificate['instance']['players'] == generated['players'] == 6
    k = len(generated['topics'])
    assert k == 12
    expected = {h for t in range(3) for h in product(range(k), repeat=t)}
    def parse_policy(value):
        result = {}
        for key, action in value.items():
            h = tuple(map(int, key.split(','))) if key else ()
            assert h not in result and type(action) is int and 0 <= action < k
            result[h] = action
        assert set(result) == expected
        return result
    small = parse_policy(generated['small']['policy'])
    big = parse_policy(generated['big']['policy'])
    saved = {}
    for item in certificate['actions']:
        assert set(item) == {'history', 'action'}
        h, a = tuple(item['history']), item['action']
        assert h not in saved and type(a) is int and 0 <= a < k
        saved[h] = a
    assert set(saved) == expected and saved == small
    names = generated['topics']
    prefix = tuple(names.index(a) for a in generated['small']['prefix'])
    tail = tuple(names.index(a) for a in generated['small']['tail'])
    assert list(prefix) == certificate['fixed_prefix']
    assert list(tail) == certificate['on_path_suffix']
    actual = prefix + tail
    assert certificate['terminal'] == [actual.count(a) for a in range(k)]
    assert certificate['audit']['ordered_nodes'] == len(saved) == 157
    assert certificate['audit']['comparisons_including_self'] == generated['small']['all_legal_action_comparisons'] == 1884
    assert certificate['audit']['leader_payoff'] == generated['small']['root_payoffs'][0]
    assert certificate['audit']['responder_payoffs'] == generated['small']['root_payoffs'][3:]
    summaries = []
    for name, policy, capture in zip(('small', 'big'), (small, big), observation['captured_original_audits']):
        assert capture['prefix_names'] == generated[name]['prefix']
        assert capture['tail_names'] == generated[name]['tail']
        native = {tuple(row['history']): row['action'] for row in capture['policy']}
        assert native == policy
        suffix = tuple(names.index(a) for a in generated[name]['tail'])
        rule = {h: suffix[len(h)] if h == suffix[:len(h)] else names.index('D') for h in expected}
        assert policy == rule
        slacks = list(map(F, capture['slacks_in_original_order']))
        domination = list(map(F, capture['D_dominance_in_original_order']))
        assert len(slacks) == 1884 and len(domination) == 1728
        assert min(slacks) == min(domination) == 0
        item = {'name': name, 'complete_ordered_nodes': len(policy),
                'original_observed_IC': len(slacks), 'strict_IC': sum(v > 0 for v in slacks),
                'ties_including_self': sum(v == 0 for v in slacks),
                'original_observed_D_dominance': len(domination),
                'strict_D_dominance': sum(v > 0 for v in domination),
                'weak_D_dominance_equalities': sum(v == 0 for v in domination),
                'all_literal_policy_actions_match_observed_rule': True}
        summaries.append(item)
    assert summaries[0]['strict_IC'] == certificate['audit']['strict_comparisons'] == 1675
    result = {
        'scope': 'source/data identity binding only, no repeated game/payoff/IC search',
        'source_count': len(manifest), 'child_review_old_static_and_full_shared_fields_equal': True,
        'full_report_added_root_field': 'original_complete_SPE',
        'full_report_added_field_in_each_branch': 'tail_profit_over_F3',
        'ordered_F3_optimizer_counts_from_reused_B7_saved_table': optimizer_counts,
        '61_client_complete_IC_and_child_main_reruns': 0,
        'partial_60_unit_incidence_types_and_label_order_equal': True,
        'partial_constructor_saved_map_matches_newly_original_audited_small_map_at_all157_nodes': True,
        'small_prefix_suffix_terminal_and_all_saved_audit_fields_bound': True,
        'native_observation_summaries': summaries,
        'new_IC_BI_LP_runs_in_this_binding': 0,
        'new_original_partial_IC_runs_elsewhere_in_this_batch': 1,
        'B7_reused_files': [{'path': str(path.relative_to(repo)), 'size': len(path.read_bytes()),
                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                            for path in (b7dir / 'replay/all-1296-ordered-tail-values.json',
                                         b7dir / 'replay/six-child-menu-exact-review.json')],
    }
    (BASE / 'replay/source-and-policy-binding.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'sources_bound': len(manifest), 'partial_unit_clients': 60,
                      'small_literal_map_actions_bound': len(saved),
                      '61_client_new_IC_runs': 0, 'new_IC_runs_in_binding': 0,
                      'optimizer_counts_reused': optimizer_counts, 'all_passed': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    run(parser.parse_args().repo)
