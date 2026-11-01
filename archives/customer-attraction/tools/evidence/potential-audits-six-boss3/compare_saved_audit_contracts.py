"""Compare three original audit reports to already pushed exact evidence.

No discovery or original audit is imported or run. The old 84-state/43-history
definition checks and 2520 terminal comparisons are not recomputed. The only
new payoff arithmetic concerns 15 two-support identities and six weak pure
states; all original reports are compared field for field.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import math
import platform
import time


HERE = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text())


def verified_file(path, expected):
    raw = path.read_bytes()
    assert len(raw) == expected['size'], str(path)
    assert hashlib.sha256(raw).hexdigest() == expected['sha256'], str(path)
    return json.loads(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.time()
    clock = time.perf_counter()
    source_rows = read_json(HERE / 'source-manifest.json')
    original = {}
    for row in source_rows:
        path = HERE / 'original' / row['id'] / Path(row['path']).name
        data = path.read_bytes()
        assert len(data) == row['size']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
        if path.suffix == '.json':
            original[path.name] = json.loads(data)
    inputs = {}
    for row in read_json(HERE / 'related-input-manifest.json'):
        path = HERE / 'related-inputs' / row['id'] / Path(row['path']).name
        inputs[path.name] = verified_file(path, row)
    previous = {}
    dependencies = read_json(HERE / 'prior-evidence-dependencies.json')
    for row in dependencies:
        previous[Path(row['path']).name] = verified_file(args.repository / row['path'], row)
    old_event = previous['event.json']
    assert old_event['checker_invocations'] == 1
    assert old_event['original_imports_CLI_LP_MIP_BI_random_search'] == 0
    previous_review = {x['file']: x for x in previous['review.json']['candidates']}
    old_rows = previous['all-exact-rows.json']
    weak_name = 'candidate_potential_individual.json'
    strong_name = 'candidate_potential_strong_individual.json'
    w = previous_review[weak_name]
    s = previous_review[strong_name]
    wr, sr = old_rows[weak_name], old_rows[strong_name]

    def make_phi(name):
        data = inputs[name]
        assert data['players'] == 3 and data['topics'] == 6
        assert data['actual_counts'] == previous_review[name]['actual_counts']
        assert F(data['safety_lower_bound']) == F(previous_review[name]['exact_fixed_query_minimum'])
        return {tuple(x['counts']): F(x['value']) for x in data['potential']}

    weak_phi, strong_phi = make_phi(weak_name), make_phi(strong_name)

    def payoff(phi, q, a):
        assert q[a] > 0
        r = list(q)
        r[a] -= 1
        return phi[tuple(q)] - phi[tuple(r)]

    def cross_self(rows):
        return [x for x in rows['self_congestion'] if x['a'] != x['b']]

    def minimum(rows, key='slack'):
        return str(min(F(x[key]) for x in rows))

    weak_pure = [payoff(weak_phi, [3 * int(i == a) for i in range(6)], a) for a in range(6)]
    assert weak_pure == [F(0)] * 6
    violations = []
    for a, utility in zip(w['actual_path'], w['profits']):
        if w['actual_counts'][a] * F(utility) > 3 * weak_pure[a]:
            violations.append({'topic': a, 'terminal_payoff': utility,
                               'pure_payoff': str(weak_pure[a]),
                               'harmonic_dilution_slack': str(3 * weak_pure[a] - w['actual_counts'][a] * F(utility))})
    weak_report = {
        'status': 'independent_exact_audit_passed_ABSTRACT_NOT_CAG',
        'potential_domain': 'all count vectors with total at most 3',
        'potential_entries': w['potential_states'],
        'ordered_decision_nodes': w['complete_histories'],
        'checks': {'monotonicity': len(wr['monotonicity']), 'unit_DR': len(wr['DR']),
                   'self_congestion_all_positive_levels': len(cross_self(wr)),
                   'full_history_SPE': len(wr['SPE']), 'unordered_static_backgrounds': len(wr['static_safety'])},
        'minimum_slacks': {'monotonicity': minimum(wr['monotonicity']), 'DR': minimum(wr['DR']),
                           'self_congestion': minimum(cross_self(wr)), 'SPE': minimum(wr['SPE'])},
        'actual_path': w['actual_path'], 'actual_payoffs': w['profits'],
        'welfare': w['W'], 'fixed_query_guarantee': w['exact_fixed_query_minimum'],
        'welfare_minus_n_guarantee': w['gap'],
        'CAG_exclusion_by_sharp_same_theme_dilution': violations,
        'full_domain_extension_not_claimed': True}

    totals = {tuple(x['q']): F(x['Wq']) for x in sr['common_support_efficiency']}
    mismatches, pair_failures, pair_rows = [], [], []
    for a, b in combinations(range(6), 2):
        ea, eb = tuple(int(i == a) for i in range(6)), tuple(int(i == b) for i in range(6))
        qa = tuple(2 * ea[i] + eb[i] for i in range(6))
        qb = tuple(ea[i] + 2 * eb[i] for i in range(6))
        pa = payoff(strong_phi, tuple(3 * x for x in ea), a)
        pb = payoff(strong_phi, tuple(3 * x for x in eb), b)
        error = payoff(strong_phi, qa, a) - payoff(strong_phi, qb, b) - F(3, 2) * (pa - pb)
        delta = totals[qb] - totals[qa]
        Ra = strong_phi[tuple(2 * x for x in ea)] - F(9, 2) * pa
        Rb = strong_phi[tuple(2 * x for x in eb)] - F(9, 2) * pb
        assert delta + 3 * error == Ra - Rb
        assert Ra == Rb == 0
        if delta:
            mismatches.append({'support': [a, b], 'q': list(qa), 'r': list(qb),
                               'q_total': str(totals[qa]), 'r_total': str(totals[qb]), 'difference': str(delta)})
        if error:
            pair_failures.append({'a': a, 'b': b, 'common_signed_identity_error': str(error)})
        pair_rows.append({'a': a, 'b': b, 'q': list(qa), 'r': list(qb),
                          'pure_a': str(pa), 'pure_b': str(pb), 'R_a': str(Ra), 'R_b': str(Rb),
                          'efficiency_difference': str(delta), 'two_support_identity_error': str(error),
                          'difference_plus_three_error': str(delta + 3 * error)})
    assert len(mismatches) == len(pair_failures) == 9
    assert all(F(x['error']) == 0 for x in sr['pure_harmonic'])
    strong_report = {
        'status': 'independent_strong_finite_potential_audit_passed_NOT_CAG',
        'domain': 'all |q|<=3 only; no global extension asserted',
        'checks': {'potential_entries': s['potential_states'], 'ordered_nodes': s['complete_histories'],
                   'monotone': len(sr['monotonicity']), 'DR': len(sr['DR']), 'self_congestion': len(cross_self(sr)),
                   'one_step_sharp_dilution': len(sr['sharp_transfer']), 'pure_harmonic': len(sr['pure_harmonic']),
                   'full_history_SPE': len(sr['SPE']), 'static_backgrounds': len(sr['static_safety'])},
        'minimum_slacks': {'monotone': minimum(sr['monotonicity']), 'DR': minimum(sr['DR']),
                           'self_congestion': minimum(cross_self(sr)), 'sharp': minimum(sr['sharp_transfer']),
                           'SPE': minimum(sr['SPE'])},
        'welfare': s['W'], 'query_lower_bound': s['exact_fixed_query_minimum'], 'gap': s['gap'],
        'actual_payoffs': s['profits'], 'same_support_efficiency_mismatches': mismatches,
        'two_support_identity_failures': pair_failures, 'common_signed_customer_realization_excluded': True}

    # This only reads the already computed exact comparison records.
    K_real = F(w['least_common_nonnegative_shift_for_all_terminal_sharp'])
    K = math.ceil(K_real)
    sharp = wr['all_terminal_sharp']
    witness_rows = [x for x in sharp if x['required_shift'] is not None and F(x['required_shift']) == K_real]
    assert witness_rows
    witness = min(witness_rows, key=lambda x: (tuple(-v for v in x['q']), x['a'], tuple(-v for v in x['r'])))
    old_weak_totals = {tuple(x['q']): F(x['Wq']) for x in wr['common_support_efficiency']}
    shifted_mismatches = []
    for a, b in combinations(range(6), 2):
        qa = tuple(2 * int(i == a) + int(i == b) for i in range(6))
        qb = tuple(int(i == a) + 2 * int(i == b) for i in range(6))
        v, z = old_weak_totals[qa] + 3 * K, old_weak_totals[qb] + 3 * K
        if v != z:
            shifted_mismatches.append({'support': [a, b], 'first_counts': list(qa), 'second_counts': list(qb),
                                       'first_total': str(v), 'second_total': str(z), 'difference': str(z - v)})
    shift_report = {
        'status': 'exact_abstract_counterexample_with_ALL_terminal_sharp_dilution_NOT_CAG',
        'domain': 'all count vectors of total at most 3; no global extension claimed',
        'common_linear_shift_K': K, 'exact_minimum_shift': str(K_real),
        'sharp_dilution_constraints': len(sharp), 'unit_ratio_constraints': sum(F(x['gamma']) == 1 for x in sharp),
        'minimum_dilution_slack': minimum(sharp, 'slack_after_minimum_shift'),
        'tight_shift_witness': {'q': witness['q'], 'r': witness['r'], 'topic': witness['a'], 'gamma': witness['gamma']},
        'shifted_welfare': str(F(w['W']) + 3 * K),
        'fixed_query_guarantee': str(F(w['exact_fixed_query_minimum']) + K),
        'welfare_minus_n_guarantee': w['gap'],
        'same_support_efficiency_mismatch_count': len(shifted_mismatches),
        'same_support_efficiency_first_mismatch': shifted_mismatches[0],
        'excluded_even_by_common_signed_customer_representation': True}
    reports = {'potential_candidate_independent_audit.json': weak_report,
               'strong_potential_independent_audit.json': strong_report,
               'shifted_potential_dilution_audit.json': shift_report}
    for name, report in reports.items():
        assert report == original[name], name
    result = {'all_three_original_reports_field_equal_to_reused_evidence_and_new_identity_arithmetic': True,
              'original_audit_imports_and_CLI_runs': 0, 'LP_MIP_BI_random_discovery_runs': 0,
              'previous_full_definition_checker_reexecutions': 0,
              'new_strong_two_support_pair_count': len(pair_rows),
              'new_weak_pure_state_count': len(weak_pure),
              'strong_identity_error_equals_minus_one_third_efficiency_difference_on_all_15_pairs': True,
              'source_count': len(source_rows), 'source_bytes': sum(x['size'] for x in source_rows),
              'reused_proof_dependencies': dependencies,
              'derived_reports': reports, 'all_15_two_support_rows': pair_rows}
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / 'contract-comparison.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    event = {'started_unix': started, 'elapsed_seconds': time.perf_counter() - clock,
             'python': platform.python_version(), 'assertions_enabled': __debug__,
             'new_checker_invocations': 1,
             'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'output_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
             'original_audit_imports_CLI_LP_MIP_BI_random_search': 0,
             'previous_full_definition_checker_reexecutions': 0}
    (args.output / 'event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'all_three_reports_equal': True, 'new_identity_pairs': len(pair_rows),
                      'original_audit_runs': 0, 'elapsed_seconds': event['elapsed_seconds']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
