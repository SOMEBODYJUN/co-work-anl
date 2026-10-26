"""Exact full catalog audit; the nominated path is deliberately NOT an SPE.

The input consists of unit-customer multiplicities, not provider weights.
All quantities below are scaled by lcm(1,...,6)=60; no LP solver is needed.
"""
from pathlib import Path
from itertools import combinations_with_replacement
import hashlib
import json

HERE = Path(__file__).resolve().parent
H = [0]
for j in range(1, 7):
    H.append(H[-1] + 60 // j)


def main():
    source = HERE / 'suffix_envelope_input.json'
    data = json.loads(source.read_text())
    types = []
    for row in data['mask_weights']:
        b, w = row['actual_mask'], row['multiplicity_per_T_index']
        assert isinstance(w, int) and w > 0
        for j in range(6):
            types.append((b | (1 << (6 + j)), w))
    actual = tuple(data['actual'])

    def load(mask, leaf):
        return sum((mask >> a) & 1 for a in leaf)

    def utility60(leaf, who):
        return sum(w * (60 // load(mask, leaf)) for mask, w in types
                   if (mask >> leaf[who]) & 1)

    profits = [utility60(actual, i) for i in range(6)]
    welfare = sum(w for mask, w in types if load(mask, actual))
    customers = sum(w for mask, w in types)
    assert sum(profits) == 60 * welfare
    safe_slacks = []
    for i in range(6):
        for topic in range(12):
            safe60 = sum(w * (60 // (load(mask, actual[:i]) + 6 - i))
                         for mask, w in types if (mask >> topic) & 1)
            safe_slacks.append(profits[i] - safe60)
    assert min(safe_slacks) >= 0

    suffix = []
    for start in range(6):
        credit60 = sum(profits[start:])
        for i in range(start, 6):
            credit60 += sum(w * ((60 // (load(mask, actual[:i]) + 1))
                                - (60 // (load(mask, actual[:i]) + 6 - i)))
                            for mask, w in types if (mask >> actual[i]) & 1)
        maximum = -1
        maximizing = None
        comparisons = 0
        for comparison in combinations_with_replacement(range(12), 6 - start):
            comparisons += 1
            phi60 = sum(w * (H[load(mask, actual[:start]) + load(mask, comparison)]
                                - H[load(mask, actual[:start])])
                        for mask, w in types)
            if phi60 > maximum:
                maximum, maximizing = phi60, comparison
        assert credit60 >= maximum, (start, credit60, maximum, maximizing)
        suffix.append({'start_index': start, 'remaining': 6 - start,
                       'comparison_multisets': comparisons,
                       'budget_scaled60': credit60,
                       'maximum_relative_potential_scaled60': maximum,
                       'minimum_slack_scaled60': credit60 - maximum,
                       'maximizing_comparison': maximizing})

    # A legitimate SPE would need to survive the actual penultimate node.
    # Every best final reply after a profitable deviation is checked.
    profitable = []
    for topic in range(12):
        leaves = [actual[:4] + (topic, last) for last in range(12)]
        best = max(utility60(leaf, 5) for leaf in leaves)
        replies = [leaf for leaf in leaves if utility60(leaf, 5) == best]
        floor = min(utility60(leaf, 4) for leaf in replies)
        if floor > profits[4]:
            profitable.append({'deviation': topic,
                               'best_final_replies': [leaf[-1] for leaf in replies],
                               'minimum_deviator_profit_scaled60': floor,
                               'actual_deviator_profit_scaled60': profits[4],
                               'strict_gain_scaled60': floor - profits[4]})
    assert profitable, 'Do not infer a genuine counterexample from envelope feasibility.'
    assert 2 * welfare < customers
    # The six T topics partition the entire customer set, so OPT6=customers.
    assert all(sum((mask >> (6+j)) & 1 for j in range(6)) == 1 for mask, w in types)
    report = {'status': 'EXACT_ENVELOPE_OBSTRUCTION_NOT_SPE',
              'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'unit_customers': customers, 'OPT6': customers, 'W': welfare,
              'W_over_OPT6': str(__import__('fractions').Fraction(welfare, customers)),
              'actual_profits_scaled60': profits,
              'prefix_safety_comparisons': len(safe_slacks),
              'minimum_safety_slack_scaled60': min(safe_slacks),
              'suffix_envelopes': suffix,
              'unavoidable_profitable_penultimate_deviations': profitable,
              'scope': 'All comparisons in this 12-topic catalog, all six actual suffixes; these inequalities are insufficient for half. No SPE realization or refutation of the potential candidate.'}
    (HERE / 'suffix_envelope_exact.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('suffix_envelopes','unavoidable_profitable_penultimate_deviations')}, indent=2))
    print('suffix margins60', [row['minimum_slack_scaled60'] for row in suffix])
    print('profitable penultimate deviations', len(profitable))


if __name__ == '__main__':
    main()
