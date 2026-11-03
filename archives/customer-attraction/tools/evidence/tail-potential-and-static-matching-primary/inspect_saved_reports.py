"""Inspect saved report arithmetic and matrix minima, without running a game solver.

This does not reconstruct the reported payoff matrices from customers, enumerate
new SPE endpoints, or verify any saved full policy. Historical events stay historical.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SRC = HERE / 'source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/adversary'

def main():
    fixed = json.loads((SRC / 'static_matching_frozen.json').read_text())
    allout = json.loads((SRC / 'static_matching_all_outcomes.json').read_text())
    one = json.loads((SRC / 'one_gap_named_exact.json').read_text())
    checks = []
    total_permutations = 0
    for row in fixed['reports']:
        m, p = row['players'], row['topics']
        M = [[F(v) for v in rr] for rr in row['cost_matrix_for_worst_optimal_multiset']]
        assert len(M) == m and all(len(rr) == m for rr in M)
        vals = [sum((M[i][pi[i]] for i in range(m)), F()) for pi in permutations(range(m))]
        total_permutations += len(vals)
        value = min(vals)
        assert value == F(row['max_over_optimal_multisets_of_minimum_matching'])
        assert value - row['W'] == F(row['gap_above_W'])
        assert sum(map(F, row['actual_payoffs'])) == row['W']
        assert row['verified_histories'] == sum(p**i for i in range(m))
        assert row['verified_deviations'] == row['verified_histories'] * (p-1)
        themes = row['worst_optimal_multiset']
        left = list(range(m)); cost = F()
        for i, t in enumerate(row['minimizing_assignment_to_positions']):
            j = next(j for j in left if themes[j] == t)
            left.remove(j); cost += M[i][j]
        assert cost == value
        checks.append({'instance': row['instance'], 'recorded_matrix_minimum': str(value),
                       'slot_permutations': len(vals), 'gap': row['gap_above_W']})
    for row in allout['reports']:
        assert sum(row['worst_terminal_counts']) == row['players']
        assert row['pairs_checked'] == row['all_SPE_terminal_counts'] * row['all_optimal_multisets']
        assert F(row['worst_matching_value']) - row['worst_actual_W'] == F(row['worst_matching_gap_above_actual_W'])
        assert sorted(row['minimizing_assignment_to_positions']) == row['worst_optimal_multiset']
    assert sum(map(F, one['actual_u'][:3])) == F(one['U123'])
    assert F(one['U123']) + F(one['Gamma2']) - 3*F(one['true_integer_security_v5']) == F(one['minimum_ONE_GAP_residual'])
    cp = HERE / 'source-root/evidence/certificates/customer_attraction/five_individual_security.json'
    sec = json.loads(cp.read_text())['security']
    assert len(sec['primary']) == 10 and sum(map(F, sec['primary'])) == 1
    assert min(map(F, sec['primary'])) >= 0
    assert sum(F(x['probability']) for x in sec['dual']) == 1
    assert all(F(x['probability']) >= 0 and len(x['rivals']) == 4
               and all(type(a) is int and 0 <= a < 10 for a in x['rivals']) for x in sec['dual'])
    out = {'scope': __doc__, 'status': 'passed', 'fixed_report_rows': len(checks),
           'recorded_matrix_slot_permutations': total_permutations, 'matrix_checks': checks,
           'historical_histories_sum': sum(x['verified_histories'] for x in fixed['reports']),
           'historical_nonself_deviations_sum': sum(x['verified_deviations'] for x in fixed['reports']),
           'all_endpoint_inputs': len(allout['reports']),
           'historical_endpoint_counts_sum': sum(x['all_SPE_terminal_counts'] for x in allout['reports']),
           'historical_endpoint_optimal_pairs_sum': sum(x['pairs_checked'] for x in allout['reports']),
           'one_gap_saved_arithmetic': one['minimum_ONE_GAP_residual'],
           'actual_security_dual_domain_and_simplex_checked': True,
           'new_SPE_or_security_payoff_enumerations': 0,
           'new_original_entrypoints': 0}
    (HERE/'saved-report-inspection.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('scope','matrix_checks')},ensure_ascii=False))

if __name__ == '__main__':
    main()
