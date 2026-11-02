"""Static 61-unit six-background F3/menu check; no old SPE IC rerun.

Only AST literal extraction from original code. No original module import,
canonical solver, complete-policy verifier, LP, BI, or random input.
"""
import ast
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def run():
    manifest = json.loads((BASE / 'source-manifest.json').read_text())
    for q in manifest:
        raw = (BASE / q['saved_path']).read_bytes()
        assert len(raw) == q['size'] and hashlib.sha256(raw).hexdigest() == q['sha256']
    source = BASE / 'original/aggregate_profit_state_obstruction.py'
    literals = {}
    for node in ast.parse(source.read_text()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('LABELS', 'TYPES'):
                literals[node.targets[0].id] = ast.literal_eval(node.value)
    labels, types = literals['LABELS'], literals['TYPES']
    assert labels == 'ABCDEF'
    customers = [frozenset(labels.index(a) for a in membership)
                 for membership, number in types for _ in range(number)]
    assert len(customers) == 61
    frozen = json.loads((BASE / 'original/aggregate_profit_state_obstruction.json').read_text())

    def profits(profile):
        result = []
        for a in profile:
            result.append(sum((F(1, sum(b in liked for b in profile))
                               for liked in customers if a in liked), F(0)))
        return result

    def residual(prefix, tail):
        value = F(0)
        for liked in customers:
            past = sum(a in liked for a in prefix)
            count = sum(a in liked for a in tail)
            if count:
                value += F(count, past + count)
        return value

    tails = ((0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 4, 4), (0, 5, 5))
    all_values, results = [], []
    for a, actual_tail in enumerate(tails):
        candidates = [(tail, residual((a,), tail)) for tail in product(range(6), repeat=3)]
        assert len(candidates) == 216
        optimum = max(value for _, value in candidates)
        maximizer = min(tail for tail, value in candidates if value == optimum)
        pay = profits((a,) + actual_tail)
        total = sum(pay[1:])
        computed = {'root': labels[a], 'tail': ''.join(labels[b] for b in actual_tail),
                    'root_payoff': str(pay[0]), 'tail_profit': str(total),
                    'F3': str(optimum), 'F3_maximizer': ''.join(labels[b] for b in maximizer),
                    'tail_to_F3': str(total / optimum),
                    'slack_above_3_over_5': str(total - F(3, 5) * optimum)}
        assert computed == frozen['non_SPE_menu'][a]
        assert total >= F(5, 8) * optimum
        results.append(computed)
        all_values.append({'root': labels[a], 'all_216_ordered_tail_values': [
            {'tail': tail, 'profit': str(value)} for tail, value in candidates]})
    assert all(F(row['root_payoff']) <= F(15, 2) for row in results)
    assert min(F(row['tail_to_F3']) for row in results) == F(5, 8)
    # A,B,C,D are a unit-customer partition, certifying F4(0)=OPT4=61.
    assert all(sum(a in liked for a in (0, 1, 2, 3)) == 1 for liked in customers)
    actual_profits = profits((0, 0, 0, 5))
    assert actual_profits == [F(9), F(9), F(9), F(11)]
    f3_a = F(results[0]['F3'])
    new_static_genuine = {
        'payoffs': list(map(str, actual_profits)), 'welfare': int(sum(actual_profits)),
        'F4': '61', 'F3_after_A': str(f3_a), 'local_loss': str(61 - f3_a),
        'twice_root_payoff': str(2 * actual_profits[0]),
        'local_bridge_deficit': str(61 - f3_a - 2 * actual_profits[0]),
        'actual_child_half_slack': str(2 * sum(actual_profits[1:]) - f3_a),
        'whole_half_slack': str(2 * sum(actual_profits) - 61)}
    for key, value in new_static_genuine.items():
        assert frozen['genuine_complete_SPE'][key] == value
    prescribed = profits((0, 0, 0, 0))[-1]
    deviation = profits((0, 0, 0, 2))[-1]
    assert prescribed == F(frozen['last_chosen_payoff']) == F(15, 2)
    assert deviation == F(frozen['last_deviation_payoff']) == F(11)
    assert 2 * sum(profits((0, 0, 0, 0))) == 60 < 61
    output = {
        'scope': 'six fixed backgrounds and static menus only; mature AAAF full-SPE IC inherited, not rerun',
        'expanded_unit_customers': len(customers), 'distinct_type_rows': len(types),
        'ordered_three_slot_comparisons': 1296, 'backgrounds': 6,
        'all_menu_rows_match_original_report': True, 'menu_rows': results,
        'genuine_fields_newly_checked_statically': new_static_genuine,
        'old_complete_IC_counts_not_executed_here': {'nodes': 259, 'comparisons_including_chosen': 1554},
        'non_SPE_prescribed_last_profit': str(prescribed), 'non_SPE_last_deviation_profit': str(deviation),
        'non_SPE_strict_deviation_gain': str(deviation - prescribed),
        'menu_welfare': '30', 'menu_twice_welfare_minus_F4': '-1',
        'current_original_aggregate_main': 0, 'current_original_six_case_probe': 0,
        'current_SPE_IC_BI_LP_RNG': 0, 'new_static_audit_runs': 1}
    (BASE / 'replay/six-child-menu-exact-review.json').write_text(json.dumps(output, indent=2) + '\n')
    (BASE / 'replay/all-1296-ordered-tail-values.json').write_text(json.dumps(all_values, separators=(',', ':')) + '\n')
    print(json.dumps({'expanded_unit_customers': 61, 'backgrounds': 6,
                      'ordered_tail_comparisons': 1296, 'menu_ratios_minimum': '5/8',
                      'L_bridge_deficit': '7', 'S_menu_strict_last_deviation_gain': '7/2',
                      'all_passed': True}))


if __name__ == '__main__':
    run()
