"""Bind common saved fields only; no customer extraction or mathematical enumeration."""
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent-report', type=Path, required=True)
    parser.add_argument('--direct-report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    parent_raw = args.parent_report.read_bytes()
    direct_raw = args.direct_report.read_bytes()
    p, d = json.loads(parent_raw), json.loads(direct_raw)
    assert p['unit_customers'] == d['customer_count'] == 6000
    assert p['W'] == d['welfare'] == 2940
    assert p['OPT6'] == d['optimum'] == 6000
    assert [F(x, 60) for x in p['actual_profits_scaled60']] == list(map(F, d['actual_profit_vector']))
    assert p['prefix_safety_comparisons'] == d['safe_rows'] == 72
    assert F(p['minimum_safety_slack_scaled60'], 60) == F(d['minimum_safe_slack'])
    suffixes = []
    assert len(p['suffix_envelopes']) == len(d['suffixes']) == 6
    for one, two in zip(p['suffix_envelopes'], d['suffixes']):
        assert one['start_index'] + 1 == two['position']
        assert one['remaining'] == two['remaining']
        assert one['comparison_multisets'] == two['comparisons']
        assert F(one['budget_scaled60'], 60) == F(two['budget'])
        assert F(one['maximum_relative_potential_scaled60'], 60) == F(two['maximum_relative_potential'])
        assert F(one['minimum_slack_scaled60'], 60) == F(two['minimum_envelope_slack'])
        assert one['maximizing_comparison'] == two['one_maximizer']
        assert F(two['suffix_profit']) + F(two['self_copy_tax']) == F(two['budget'])
        suffixes.append({'position': two['position'], 'all_common_fields_exactly_equal': True,
                         'saved_profit_plus_saved_tax_equals_budget': True})
    assert sum(x['comparisons'] for x in d['suffixes']) == d['suffix_comparisons'] == 18563
    table = {x['query']: x for x in d['penultimate_deviations']}
    assert len(table) == 12 and set(table) == set(range(12))
    for q, row in table.items():
        assert F(row['minimum_current_payoff']) <= F(row['maximum_current_payoff'])
        assert F(row['strict_gain_for_every_last_best_reply']) == F(row['minimum_current_payoff']) - F(d['actual_profit_vector'][4])
    positive = [q for q in range(12) if F(table[q]['strict_gain_for_every_last_best_reply']) > 0]
    assert positive == d['profitable_penultimate_queries']
    assert positive == [x['deviation'] for x in p['unavoidable_profitable_penultimate_deviations']]
    for row in p['unavoidable_profitable_penultimate_deviations']:
        same = table[row['deviation']]
        assert row['best_final_replies'] == same['all_last_best_replies']
        assert F(row['minimum_deviator_profit_scaled60'], 60) == F(same['minimum_current_payoff'])
        assert F(row['strict_gain_scaled60'], 60) == F(same['strict_gain_for_every_last_best_reply'])
    result = {
        'scope': 'Saved-report field identity and internal arithmetic only; no customer-level, potential, or best-reply recomputation.',
        'parent_report_sha256': hashlib.sha256(parent_raw).hexdigest(),
        'direct_report_sha256': hashlib.sha256(direct_raw).hexdigest(),
        'direct_top_level_keys': list(d),
        'direct_top_level_field_count': len(d),
        'shared_customer_welfare_profit_safe_fields_match': True,
        'all_six_shared_suffix_records_match_after_dividing_parent_by_60': suffixes,
        'all_seven_shared_profitable_queries_match': positive,
        'direct_only_unprofitable_queries_not_customer_reverified': [0, 1, 2, 3, 4],
        'direct_only_last_values_and_current_maxima_not_customer_reverified': list(range(12)),
        'all_twelve_saved_gain_differences_internally_consistent': True,
        'direct_historical_input_fingerprint_not_available': True,
        'current_original_direct_runs': 0,
        'current_safe_or_suffix_enumerations': 0,
        'current_best_reply_recomputations': 0,
    }
    with args.output.open('x') as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'shared_suffixes': 6, 'shared_profitable_queries': len(positive),
                      'direct_only_unprofitable_queries_not_recomputed': 5,
                      'customer_level_enumerations': 0}, indent=2))


if __name__ == '__main__':
    main()
