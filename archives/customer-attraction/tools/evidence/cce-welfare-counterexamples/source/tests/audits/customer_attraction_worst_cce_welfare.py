"""Independent unit-client audit of CA-WORST-CCE-WELFARE-NO.

Reads only the frozen instance and certificate. No project model, cone code,
optimization package, count-cache, or author discovery script is imported.
All payoffs, SPE comparisons, CCE constraints, and dual columns use Fraction.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import argparse
import json


def audit(instance_path, certificate_path):
    obj = json.loads(instance_path.read_text())
    cert = json.loads(certificate_path.read_text())
    k, n = len(obj['topics']), obj['players']
    assert (k, n) == (5, 3)
    assert all(isinstance(t['multiplicity'], int) and t['multiplicity'] >= 0
               for t in obj['customers'])
    clients = [frozenset(t['topics']) for t in obj['customers']
               for _ in range(t['multiplicity'])]
    assert len(clients) == 13
    themes = [frozenset(x for x, likes in enumerate(clients) if a in likes)
              for a in range(k)]
    assert len(set(themes)) == k
    policy = {tuple(row['history']): row['action'] for row in cert['actions']}
    assert len(policy) == len(cert['actions']), 'Duplicate ordered history.'
    histories = [h for depth in range(n) for h in product(range(k), repeat=depth)]
    assert set(policy) == set(histories)
    assert all(0 <= a < k for a in policy.values())

    def terminal(h):
        while len(h) < n:
            h = h + (policy[h],)
        return h

    def payoffs(z):
        result = [F(0) for _ in z]
        for likes in clients:
            covered = [i for i, a in enumerate(z) if a in likes]
            for i in covered:
                result[i] += F(1, len(covered))
        return tuple(result)

    def welfare(z):
        return sum(any(a in likes for a in z) for likes in clients)

    comparisons, spe_rows = [], []
    for h in histories:
        actual_leaf = terminal(h)
        actual = payoffs(actual_leaf)[len(h)]
        values = []
        for a in range(k):
            deviation_leaf = terminal(h + (a,))
            deviation = payoffs(deviation_leaf)[len(h)]
            slack = actual - deviation
            assert slack >= 0, (h, a, actual_leaf, deviation_leaf, slack)
            values.append(str(deviation))
            comparisons.append({'history': list(h), 'action': a,
                                'actual_leaf': list(actual_leaf),
                                'deviation_leaf': list(deviation_leaf),
                                'actual': str(actual), 'deviation': str(deviation),
                                'slack': str(slack)})
        spe_rows.append({'history': list(h), 'action': policy[h],
                         'deviation_values': values})

    path = terminal(())
    W = welfare(path)
    assert list(path) == cert['terminal_path'] == [0, 4, 4]
    assert W == cert['terminal_welfare'] == 9
    assert tuple(map(str, payoffs(path))) == tuple(cert['terminal_payoffs']) == ('3', '3', '3')
    ordered = list(product(range(k), repeat=n))
    profiles = list(combinations_with_replacement(range(k), n))
    assert len(ordered) == 125 and len(profiles) == 35
    opt = max(map(welfare, ordered))
    assert opt == cert['opt'] == 12

    def individual_regret(z, i, a):
        alt = z[:i] + (a,) + z[i + 1:]
        return payoffs(z)[i] - payoffs(alt)[i]

    def aggregate_regret(z, a):
        return sum((individual_regret(z, i, a) for i in range(n)), F(0))

    regrets = {z: tuple(aggregate_regret(z, a) for a in range(k)) for z in ordered}

    def check_dual(key):
        data = cert[key]
        lam = tuple(map(F, data['lambda']))
        assert len(lam) == k and min(lam) >= 0
        lower = F(data['lower'])
        values = {z: F(welfare(z)) - sum((lam[a] * regrets[z][a]
                                         for a in range(k)), F(0)) for z in ordered}
        assert min(values.values()) == lower
        assert lower > W
        # Independently verify the one-customer inverse-load identity.
        L = sum(lam)
        for z in ordered:
            inverse = F(0)
            for likes in clients:
                load = sum(a in likes for a in z)
                mass = sum((lam[a] for a in likes), F(0))
                inverse += ((1 - L) * bool(load)
                            + mass * (F(n + 1, load + 1) - (load == 0)))
            assert inverse == values[z]
        return lam, lower, values

    simple_lam, simple_lower, simple_values = check_dual('simple_cce_dual')
    opt_lam, cce_min, opt_values = check_dual('optimal_cce_dual')
    assert simple_lam == (0, F(1, 5), F(1, 5), F(1, 5), F(2, 5))
    assert simple_lower == F(137, 15)
    assert cce_min == F(2785, 297)
    # Verify all ten entries in the analytic reduction, separately from profile enumeration.
    f = (F(3), F(2), F(4, 3), F(1))
    split = tuple(min(f[c] + f[d] for c in range(4) for d in range(4) if c + d == r)
                  for r in range(4))
    assert split == (6, 5, 4, F(10, 3))
    ten_entries = []
    for a in range(4):
        for b in range(4 - a):
            value = (2 * f[a] + 6 * f[3 - b] + 8 * f[b]
                     + 12 * f[3 - a] + split[3 - a - b]) / 5
            candidates = [simple_values[z] for z in profiles if z.count(1) == a and z.count(4) == b]
            assert min(candidates) == value
            ten_entries.append({'q1': a, 'q4': b, 'minimum_D': str(value)})
    assert min(F(row['minimum_D']) for row in ten_entries) == simple_lower

    lifted = {}
    count_support = cert['optimal_cce_primal']['count_support']
    assert len(count_support) == 5
    assert sum((F(row['probability']) for row in count_support), F(0)) == 1
    for row in count_support:
        z, probability = tuple(row['profile']), F(row['probability'])
        assert len(z) == n and min(z) >= 0 and max(z) < k and probability >= 0
        all_permutations = set(permutations(z))
        for leaf in all_permutations:
            lifted[leaf] = lifted.get(leaf, F(0)) + probability / len(all_permutations)
    assert sum(lifted.values()) == 1
    cce_constraints = []
    for i in range(n):
        for a in range(k):
            regret = sum((prob * individual_regret(z, i, a) for z, prob in lifted.items()), F(0))
            assert regret >= 0
            cce_constraints.append({'player': i, 'fixed_deviation': a, 'regret': str(regret)})
    primal_value = sum((prob * welfare(z) for z, prob in lifted.items()), F(0))
    assert primal_value == cce_min
    assert len(lifted) == 18
    count_regrets = [sum((prob * regrets[z][a] for z, prob in lifted.items()), F(0))
                     for a in range(k)]
    assert tuple(count_regrets) == (F(277, 99), 0, 0, 0, 0)

    background = tuple(cert['static_security_cap']['background'])
    assert len(background) == n - 1
    query = tuple(payoffs(background + (a,))[-1] for a in range(k))
    assert query == tuple(map(F, cert['static_security_cap']['query_values'])) == (2, 3, 3, 3, 3)
    assert W >= n * max(query) and 2 * W >= opt
    return {
        'status': 'passed', 'claim_id': cert['claim_id'],
        'distinct_unit_clients': len(clients), 'distinct_topics': k, 'players': n,
        'complete_histories': len(histories), 'spe_comparisons_including_self': len(comparisons),
        'min_spe_slack': str(min(F(row['slack']) for row in comparisons)),
        'terminal_path': list(path), 'terminal_payoffs': list(map(str, payoffs(path))),
        'terminal_welfare': W, 'opt': opt, 'static_ordered_profiles': len(ordered),
        'static_count_profiles': len(profiles), 'simple_cce_lower': str(simple_lower),
        'simple_gap_above_spe': str(simple_lower - W),
        'exact_minimum_static_cce': str(cce_min), 'exact_gap_above_spe': str(cce_min - W),
        'lifted_cce_support': len(lifted), 'individual_cce_constraints': len(cce_constraints),
        'min_individual_cce_regret': str(min(F(row['regret']) for row in cce_constraints)),
        'inverse_load_identity_checks': 2 * len(ordered),
        'static_security_background': list(background), 'static_security_query_values': list(map(str, query)),
        'conclusion': 'SPE welfare 9 is below every static CCE expectation; minimum CCE is 2785/297.',
        'scope': 'Auxiliary welfare-replacement bridge fails. Half coverage and aggregate security are not refuted.',
        'spe_rows': spe_rows, 'spe_comparisons': comparisons,
        'analytic_ten_entries': ten_entries, 'individual_cce_rows': cce_constraints,
        'lifted_cce': [{'profile': list(z), 'probability': str(prob)} for z, prob in sorted(lifted.items())],
        'dual_count_columns': [{'profile': list(z), 'simple_D': str(simple_values[z]),
                                'simple_slack': str(simple_values[z] - simple_lower),
                                'optimal_D': str(opt_values[z]),
                                'optimal_slack': str(opt_values[z] - cce_min)} for z in profiles],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[2]
    parser.add_argument('--instance', type=Path,
                        default=root / 'examples/customer_attraction/worst_cce_welfare_failure.json')
    parser.add_argument('--certificate', type=Path,
                        default=root / 'evidence/certificates/customer_attraction/worst_cce_welfare_failure.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = audit(args.instance, args.certificate)
    if args.output:
        with args.output.open('x') as target:
            target.write(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    large = {'spe_rows', 'spe_comparisons', 'analytic_ten_entries',
             'individual_cce_rows', 'lifted_cce', 'dual_count_columns'}
    print(json.dumps({k: v for k, v in report.items() if k not in large}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
