"""Exact replay of uploaded root-tax and global-security certificates.

Uses compressed unit-customer types, the entire ordered policy table, and
Fraction arithmetic. No solver, optimizer, or uploaded verifier is imported.
The static-security certificates are checked against every ordered rival tuple.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def require(value, context):
    if not value:
        raise AssertionError(context)


def replay(game, certificate):
    n, m = game['players'], len(game['topics'])
    require(n >= 1 and m >= 1, 'positive dimensions')
    types = []
    for row in game['customers']:
        likes = frozenset(row['topics'])
        multiplicity = row['multiplicity']
        require(likes and all(0 <= a < m for a in likes), 'valid nonempty type')
        require(isinstance(multiplicity, int) and multiplicity > 0, 'unit clones')
        types.append((likes, multiplicity))
    histories = tuple(h for depth in range(n)
                      for h in product(range(m), repeat=depth))
    rows = certificate['strategy']['actions']
    policy = {tuple(row['history']): row['action'] for row in rows}
    require(len(policy) == len(rows) and set(policy) == set(histories),
            'complete ordered policy without duplicate histories')
    require(all(0 <= a < m for a in policy.values()), 'legal policy actions')

    @lru_cache(None)
    def terminal(history):
        require(len(history) <= n, 'history length')
        if len(history) == n:
            return history
        return terminal(history + (policy[history],))

    @lru_cache(None)
    def utilities(profile):
        values = [F(0) for _ in profile]
        for likes, multiplicity in types:
            coverers = [i for i, a in enumerate(profile) if a in likes]
            if coverers:
                share = F(multiplicity, len(coverers))
                for i in coverers:
                    values[i] += share
        return tuple(values)

    def coverage(profile):
        return sum(k for likes, k in types if any(a in likes for a in profile))

    def query(a, rivals):
        return sum((F(k, 1 + sum(b in likes for b in rivals))
                    for likes, k in types if a in likes), F(0))

    slacks = []
    for h in histories:
        i = len(h)
        own = utilities(terminal(h))[i]
        for a in range(m):
            altered = utilities(terminal(h + (a,)))[i]
            require(own >= altered, ('SPE violation', h, a, str(own), str(altered)))
            slacks.append(own - altered)
    outcome = terminal(())
    u = utilities(outcome)
    W = coverage(outcome)
    OPT = max(coverage(z) for z in combinations_with_replacement(range(m), n))
    tau = sum((F(k * sum(a in likes for a in outcome[:-1]),
                 1 + sum(a in likes for a in outcome[:-1]))
               for likes, k in types), F(0))
    require(sum(u) == W, 'equal-share conservation')
    signatures = [frozenset(i for i, (likes, _) in enumerate(types) if a in likes)
                  for a in range(m)]
    result = {
        'unit_customers': sum(k for _, k in types), 'topics': m, 'players': n,
        'ordered_decision_histories': len(histories),
        'all_action_comparisons': len(slacks),
        'nontrivial_action_deviations': len(histories) * (m - 1),
        'minimum_SPE_slack': str(min(slacks)), 'outcome': list(outcome),
        'utilities': list(map(str, u)), 'W': W, 'OPT': OPT, 'tau': str(tau),
        'root_tax_violation_OPT_minus_W_minus_tau': str(OPT - W - tau),
        'half_coverage_margin': 2 * W - OPT,
        'distinct_topic_coverages': len(set(signatures)) == m,
    }
    security = certificate.get('security')
    if security:
        p = tuple(map(F, security['primary']))
        Q = [(tuple(row['rivals']), F(row['probability'])) for row in security['dual']]
        require(len(p) == m and sum(p) == 1 and min(p) >= 0, 'primary distribution')
        require(sum(q for _, q in Q) == 1 and all(q >= 0 for _, q in Q), 'dual distribution')
        require(all(len(B) == n - 1 and all(0 <= a < m for a in B)
                    for B, _ in Q), 'legal static rivals')
        lower = min(sum((p[a] * query(a, B) for a in range(m)), F(0))
                    for B in product(range(m), repeat=n - 1))
        upper_rows = [sum((q * query(a, B) for B, q in Q), F(0)) for a in range(m)]
        require(lower == max(upper_rows) == F(security['value']),
                'matching exact static security certificates')
        result['security'] = {'value': str(lower),
            'ordered_rival_tuples': m ** (n - 1),
            'dual_query_values': list(map(str, upper_rows)),
            'W_minus_n_v': str(W - n * lower),
            'individual_margins': [str(value - lower) for value in u]}

    comparisons = []
    for raw_p in certificate.get('query_distributions', []):
        p = tuple(map(F, raw_p['probabilities']))
        require(len(p) == m and min(p) >= 0 and sum(p) == 1, 'query distribution')
        rows = []
        for i in range(n):
            rivals = {}
            for b in range(m):
                off = terminal(outcome[:i] + (b,))
                rivals[b] = off[:i] + off[i + 1:]
            D = sum((p[a] * query(a, rivals[a]) for a in range(m)), F(0))
            C = sum((p[a] * p[b] * query(a, rivals[b])
                     for a in range(m) for b in range(m)), F(0))
            require(u[i] >= D, 'on-path incentive slack')
            rows.append((D, C, D - C, u[i] - D))
        total_kappa = sum(row[2] for row in rows)
        total_slack = sum(row[3] for row in rows)
        gap = W - sum(row[1] for row in rows)
        require(gap == total_kappa + total_slack, 'global budget identity')
        p_floor = min(sum((p[a] * query(a, B) for a in range(m)), F(0))
                      for B in product(range(m), repeat=n - 1))
        comparisons.append({'name': raw_p['name'],
            'rows_D_C_kappa_slack': [list(map(str, row)) for row in rows],
            'aggregate_kappa': str(total_kappa), 'aggregate_incentive_slack': str(total_slack),
            'compensated_budget_W_minus_sum_C': str(gap),
            'security_of_query_distribution': str(p_floor)})
    result['query_budgets'] = comparisons
    for key, expected in certificate.get('expected', {}).items():
        require(result[key] == expected, ('expected field mismatch', key, expected, result[key]))
    return result


def run():
    inputs = [
        ('root_tax_61', 'examples/customer_attraction/root_tax_failure.json',
         'evidence/certificates/customer_attraction/root_tax_failure.json'),
        ('decorrelation_89', 'examples/customer_attraction/global_decorrelation_failure.json',
         'evidence/certificates/customer_attraction/global_decorrelation_failure.json'),
        ('compensated_budget_36', 'examples/customer_attraction/aggregate_theta_failure.json',
         'evidence/certificates/customer_attraction/onpath_budget_failure.json'),
    ]
    results = {}
    files = [Path(__file__)]
    for name, game_path, certificate_path in inputs:
        game_file, certificate_file = ROOT / game_path, ROOT / certificate_path
        files.extend((game_file, certificate_file))
        results[name] = replay(json.loads(game_file.read_text()), json.loads(certificate_file.read_text()))
    require(results['root_tax_61']['root_tax_violation_OPT_minus_W_minus_tau'] == '1/2', 'RT refuted')
    require(results['decorrelation_89']['query_budgets'][0]['aggregate_kappa'] == '-1/48', 'aggregate decorrelation refuted')
    require(results['compensated_budget_36']['query_budgets'][0]['compensated_budget_W_minus_sum_C'] == '-1/2', 'all-p compensated budget refuted')
    require(all(F(row['security']['W_minus_n_v']) > 0 for row in results.values()), 'no BR counterexample')
    # Degenerate dimensions, duplicate coverage labels, and rejection of a
    # genuine profitable off-path deviation are separate verifier contracts.
    boundary = [
        ({'players': 1, 'topics': ['A'], 'customers': []}, {( ): 0}),
        ({'players': 2, 'topics': ['A', 'B'], 'customers': [{'topics': [0, 1], 'multiplicity': 1}]}, {(): 0, (0,): 1, (1,): 0}),
    ]
    for game, policy in boundary:
        replay(game, {'strategy': {'actions': [{'history': list(h), 'action': a} for h, a in policy.items()]}})
    bad_game = {'players': 2, 'topics': ['A', 'B'], 'customers': [
        {'topics': [0], 'multiplicity': 1}, {'topics': [1], 'multiplicity': 1}]}
    rejected = False
    try:
        replay(bad_game, {'strategy': {'actions': [
            {'history': [], 'action': 0}, {'history': [0], 'action': 0}, {'history': [1], 'action': 0}]}})
    except AssertionError:
        rejected = True
    require(rejected, 'non-SPE policy must be rejected')
    return {'status': 'PASS', 'scope': 'three complete certificates, not a universal BR proof',
        'cases': results, 'boundary_checks': 'zero customers, n=1, duplicate coverage, non-SPE rejection',
        'sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    output = json.dumps(run(), ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(output)
    else:
        print(output, end='')
