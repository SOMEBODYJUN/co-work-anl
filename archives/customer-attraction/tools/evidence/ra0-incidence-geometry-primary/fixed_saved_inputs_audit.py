"""New fixed-input audit, not a replay of either random probe.

Only the two distinct worst_ratio.instance objects saved by the three frozen
reports are evaluated. No random generation, floating optimizer or C5 replay.
"""
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--package-root', type=Path, required=True)
    p.add_argument('--source-dir', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    sys.path.insert(0, str(args.package_root.resolve()))
    from customer_attraction import Instance, ExactSPESolver, verify_certificate

    specifications = [
        ('99e9f78edbbf9350bd08', 'rank_two_probe_300.json'),
        ('109ec795dc221774a6bc', 'rank_two_probe_20000.json'),
        ('cb437b3a2665be27751e', 'rank_two_probe_root_5000.json'),
    ]
    saved = [json.loads((args.source_dir / i / name).read_text())['worst_ratio']
             for i, name in specifications]
    assert saved[1] == saved[2]
    results = []
    for record, (source_id, _) in zip(saved[:2], specifications[:2]):
        instance = Instance.from_dict(record['instance'])
        assert all(1 <= len(c.topics) <= 2 for c in instance.customers)
        solver = ExactSPESolver(instance)
        outcomes = sorted(solver.outcomes())
        minimum = min(instance.welfare(q) for q in outcomes)
        optimum = instance.optimal_welfare()
        assert minimum == record['minimum_welfare']
        assert optimum == record['optimum']
        assert Fraction(optimum, minimum) == Fraction(record['ratio'])
        target = min(q for q in outcomes if instance.welfare(q) == minimum)
        certificate = solver.certificate(target)
        verification = verify_certificate(instance, certificate)
        verification.assert_valid()

        def finish(h):
            while len(h) < instance.players:
                h += (certificate.actions[h],)
            return h

        def utility(h, who):
            return sum((Fraction(c.multiplicity, sum(a in c.topics for a in h))
                        for c in instance.customers if h[who] in c.topics), Fraction())

        strict = ties = 0
        for depth in range(instance.players):
            for h in product(range(instance.topic_count), repeat=depth):
                chosen = utility(finish(h), depth)
                for a in range(instance.topic_count):
                    value = utility(finish(h + (a,)), depth)
                    assert chosen >= value
                    strict += chosen > value
                    ties += chosen == value
        backgrounds = list(compositions(instance.players - 1, instance.topic_count))
        last_values = [max(sum((Fraction(c.multiplicity,
                           1 + sum(q[b] for b in c.topics))
                           for c in instance.customers if a in c.topics), Fraction())
                          for a in range(instance.topic_count)) for q in backgrounds]
        theta = min(last_values)
        root = verification.terminal_history
        root_threshold = solver.threshold((0,) * instance.topic_count)
        results.append({
            'source_id': source_id, 'historical_case_label': record['case'],
            'instance': instance.to_dict(),
            'unit_customers': sum(c.multiplicity for c in instance.customers),
            'root_outcomes': [{'counts': list(q), 'welfare': instance.welfare(q),
                               'topic_payoffs': list(map(str, instance.topic_payoffs(q)))}
                              for q in outcomes],
            'minimum_welfare': minimum, 'optimum': optimum,
            'optimum_over_minimum': str(Fraction(optimum, minimum)),
            'root_threshold': str(root_threshold), 'theta': str(theta),
            'last_background_count_vectors': len(backgrounds),
            'theta_minimizers': [list(q) for q, v in zip(backgrounds, last_values) if v == theta],
            'all_outcomes_aggregate_theta': minimum >= instance.players * theta,
            'selected_worst_terminal': list(root),
            'selected_worst_payoffs': [str(utility(root, i)) for i in range(instance.players)],
            'complete_certificate': certificate.to_dict(),
            'verification': {
                'valid': verification.valid, 'histories': verification.checked_histories,
                'nonself_deviations': verification.checked_deviations,
                'all_comparisons_including_self': strict + ties,
                'strict_comparisons': strict, 'ties_including_self': ties,
                'errors': list(verification.errors), 'violations': len(verification.violations),
            },
        })
    report = {'identity': 'new exact audit of two distinct frozen saved inputs',
              'random_cases_generated': 0, 'LP_or_MILP_calls': 0,
              'source_mains_executed': 0, 'C5_replays': 0,
              'third_saved_input_equals_second': True, 'results': results}
    with args.output.open('x') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'PASS': True, 'distinct_inputs': len(results),
                      'summary': [{k: r[k] for k in [
                          'source_id', 'unit_customers', 'minimum_welfare', 'optimum',
                          'optimum_over_minimum', 'root_threshold', 'theta',
                          'selected_worst_terminal', 'selected_worst_payoffs', 'verification']}
                                  for r in results]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
