"""Independent deterministic source replay for the acyclic lemma review.

Uses only standard-library arithmetic plus this directory's pre-existing
definition-level certificate audit; never imports the proposed lemma's probe,
source audit, game solver, or canonical game package.
"""
from fractions import Fraction
import hashlib
from itertools import permutations
import json
from pathlib import Path

from audit_certificates import audit

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/model.py').is_file())


def load_strategy(instance, certificate):
    p, m = len(instance['topics']), instance['players']
    actions = {tuple(row['history']): row['action'] for row in certificate['actions']}

    def terminal(history):
        while len(history) < m:
            history += (actions[history],)
        return history

    def counts(history):
        return tuple(history.count(a) for a in range(p))

    def payoff(theme, terminal_profile, mask):
        if not mask & (1 << theme):
            return Fraction(0)
        return Fraction(1, sum(bool(mask & (1 << a)) for a in terminal_profile))

    def utility(theme, terminal_profile):
        return sum((c['multiplicity'] * payoff(theme, terminal_profile,
            sum(1 << a for a in c['topics'])) for c in instance['customers']), Fraction(0))

    return actions, terminal, counts, payoff, utility


def four_row_review():
    source = ROOT / 'research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
    obj = json.loads(source.read_text())
    inst, cert = obj['instance'], obj['certificate']
    certificate_result = audit(inst, cert)
    actions, terminal, counts, payoff, utility = load_strategy(inst, cert)
    actual = terminal(())
    assert actual == (3, 3, 2, 2)
    q = counts(actual)
    comparison = (0, 1, 4, 5)
    assigned = (2, 2, 3, 3)
    histories = ((3, 3), (3, 3), (), ())
    assert counts(assigned) == q
    earlier = [0] * len(q)
    rows, branches = [], []
    for j, (T, a, h) in enumerate(zip(comparison, assigned, histories)):
        assert h == actual[:len(h)] and actions[h] == a
        branch = terminal(h + (T,))
        upper = tuple(q[b] - int(b == a) + int(b == T) + earlier[b]
                      for b in range(len(q)))
        assert all(n <= v for n, v in zip(counts(branch), upper))
        rows.append({'j': j + 1, 'comparison': T, 'assigned': a, 'history': h,
                     'terminal': branch, 'counts': counts(branch), 'upper': upper,
                     'real_payoff': str(utility(T, branch)),
                     'budget': str(utility(a, actual))})
        branches.append(branch)
        earlier[T] += 1
    coefficients = []
    for mask in range(1, 1 << len(q)):
        owner = next((j for j, a in enumerate(comparison) if mask & (1 << a)), None)
        if owner is None:
            continue
        c = sum(bool(mask & (1 << a)) for a in actual)
        frozen_denominator = c + 1 - int(bool(mask & (1 << assigned[owner])))
        branch_load = sum(bool(mask & (1 << a)) for a in branches[owner])
        assert 1 <= branch_load <= frozen_denominator <= inst['players']
        frozen = Fraction(1, frozen_denominator)
        selected_query = payoff(comparison[owner], branches[owner], mask)
        all_queries = sum((payoff(T, branch, mask) for T, branch in
                           zip(comparison, branches)), Fraction(0))
        assert frozen <= selected_query <= all_queries
        coefficients.append({'mask': mask, 'earliest_owner': owner + 1,
                             'actual_load': c, 'real_owner_load': branch_load,
                             'frozen_denominator': frozen_denominator,
                             'frozen_share': str(frozen),
                             'real_owner_share': str(selected_query)})
    weights = [(sum(1 << a for a in c['topics']), c['multiplicity'])
               for c in inst['customers']]
    R_first = sum((n * Fraction(1, sum(bool(mask & (1 << a)) for a in actual) + 1
                         - int(bool(mask & (1 << assigned[j]))))
                   for mask, n in weights
                   for j in [next((j for j, a in enumerate(comparison)
                                  if mask & (1 << a)), None)] if j is not None), Fraction(0))
    query_sum = sum((utility(T, branch) for T, branch in zip(comparison, branches)), Fraction(0))
    assert R_first <= query_sum <= certificate_result['W']
    return {'source': str(source.relative_to(ROOT)),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'complete_strategy_audit': certificate_result, 'four_rows': rows,
            'all_nonempty_types': (1 << len(q)) - 1,
            'comparison_covered_types_checked': len(coefficients),
            'typewise_owner_checks': coefficients,
            'R_first': str(R_first), 'real_query_sum': str(query_sum)}


def no_universal_existence_review():
    source = ROOT / 'examples/customer_attraction/portfolio_matching_failure.json'
    cert_source = ROOT / 'evidence/certificates/customer_attraction/portfolio_matching_failure.json'
    inst = json.loads(source.read_text())
    cert = json.loads(cert_source.read_text())
    result = audit(inst, cert)
    actions, terminal, counts, payoff, utility = load_strategy(inst, cert)
    actual = terminal(())
    assert actual == (4, 0)
    histories = {4: (), 0: (4,)}
    q = counts(actual)
    rows = []
    for comparison in permutations((1, 3)):
        for assigned in permutations(actual):
            earlier = [0] * len(q)
            failed = []
            query_sum = Fraction(0)
            for j, (T, a) in enumerate(zip(comparison, assigned)):
                branch = terminal(histories[a] + (T,))
                query_sum += utility(T, branch)
                upper = tuple(q[b] - int(b == a) + int(b == T) + earlier[b]
                              for b in range(len(q)))
                failed.extend((j + 1, b, n, v) for b, (n, v)
                              in enumerate(zip(counts(branch), upper)) if n > v)
                earlier[T] += 1
            assert failed and query_sum == 41
            rows.append({'comparison_order': comparison, 'assigned_actual': assigned,
                         'real_query_sum': str(query_sum), 'failed_coordinates': failed})
    missed = sum(c['multiplicity'] for c in inst['customers']
                 if set(c['topics']).intersection({1, 3})
                 and not set(c['topics']).intersection(actual))
    assert missed == 42
    return {'source': str(source.relative_to(ROOT)),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'certificate_sha256': hashlib.sha256(cert_source.read_bytes()).hexdigest(),
            'complete_strategy_audit': result, 'missed_comparison_clients': missed,
            'all_four_order_matching_choices': rows}


def main():
    report = {'scope': 'independent deterministic exact source replay; no new sampling',
              'four_row_witness': four_row_review(),
              'universal_existence_counterexample': no_universal_existence_review()}
    (HERE / 'acyclic_independent_source_review.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: {a: b for a, b in v.items()
                         if a not in ('typewise_owner_checks', 'all_four_order_matching_choices')}
                      if isinstance(v, dict) else v for k, v in report.items()}, indent=2))


if __name__ == '__main__':
    main()
