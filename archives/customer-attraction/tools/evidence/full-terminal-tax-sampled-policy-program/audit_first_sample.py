"""Definition-level unit-client audit of the newly captured first policy.

Uses neither the author's payoff helpers nor the canonical solver. Validate the
new seed and one post-hoc rationalized positive LP point; do not rerun any LP.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import gzip
import json
import math

HERE = Path(__file__).resolve().parent
capture = json.loads((HERE/'first-sample/capture.json').read_text())
sigma = {tuple(x['history']): x['action'] for x in capture['sigma']}
gamma = [[F(x) for x in row] for row in json.loads(gzip.decompress(
    (HERE/'first-sample/original-gamma.json.gz').read_bytes()))]
histories = []


def collect(h=()):
    if len(h) == 4:
        return
    histories.append(h)
    for a in range(6):
        collect(h+(a,))


collect()
assert len(histories) == 259 and set(histories) == set(sigma)
assert len(gamma) == 1554


@lru_cache(None)
def end(h):
    return h if len(h) == 4 else end(h+(sigma[h],))


def audit_game(types):
    clients = [frozenset(x['topics']) for x in types for _ in range(x['multiplicity'])]
    utilities = {}
    for z in product(range(6), repeat=4):
        u = [F(0)]*4
        for interest in clients:
            coverers = [j for j, action in enumerate(z) if action in interest]
            if coverers:
                share = F(1, len(coverers))
                for j in coverers:
                    u[j] += share
        utilities[z] = tuple(u)
    weights = {sum(1 << a for a in x['topics']): x['multiplicity'] for x in types}
    rows = []
    for h in histories:
        chosen = sigma[h]
        z0 = end(h)
        actual = utilities[z0][len(h)]
        for alternative in range(6):
            z1 = end(h+(alternative,))
            deviation = utilities[z1][len(h)]
            slack = actual-deviation
            j = len(rows)
            author_weighted = sum(gamma[j][mask-1]*amount for mask, amount in weights.items())
            assert slack == author_weighted
            assert slack >= 0
            rows.append({'history': list(h), 'chosen': chosen, 'alternative': alternative,
                         'actual': str(actual), 'deviation': str(deviation), 'slack': str(slack)})
    root = end(())
    counts = [root.count(a) for a in range(6)]
    loads = [sum(a in interest for a in root) for interest in clients]
    welfare = sum(c > 0 for c in loads)
    tax = sum((F(c, c+1) for c in loads if c), F(0))
    coverages = [{'support': list(s), 'coverage': sum(bool(set(s)&x) for x in clients)}
                 for s in combinations(range(6), 4)]
    optimum = max(x['coverage'] for x in coverages)
    return {'unit_clients': len(clients), 'types': types, 'ordered_terminal_leaves': 1296,
            'checked_histories': 259, 'checked_rows_including_self': len(rows),
            'minimum_slack': str(min(F(r['slack']) for r in rows)),
            'positive_rows': sum(F(r['slack']) > 0 for r in rows),
            'zero_rows': sum(F(r['slack']) == 0 for r in rows),
            'root': list(root), 'root_counts': counts, 'root_payoffs': list(map(str, utilities[root])),
            'W': welfare, 'full_terminal_tax': str(tax), 'OPT4': optimum,
            'W_plus_tax_minus_OPT': str(F(welfare)+tax-optimum),
            'all_static_comparisons': coverages, 'all_rows': rows}


seed = audit_game(capture['seed_game']['customers'])
assert seed['root_counts'] == capture['selected_terminal_counts']
chosen = capture['selected_result']
w = {mask: F(float(x)).limit_denominator(1000000)
     for mask, x in enumerate(chosen['weights'], start=1) if x > 1e-8}
den = math.lcm(*(x.denominator for x in w.values()))
assert sum(w.values()) == 1
posthoc = audit_game([{'topics': [a for a in range(6) if mask >> a & 1],
                      'multiplicity': int(value*den)} for mask, value in w.items()])
assert posthoc['root'] == chosen['root']
assert posthoc['W'] == 4 and posthoc['OPT4'] == 7
assert F(posthoc['full_terminal_tax']) == F(16, 5)
assert F(posthoc['W_plus_tax_minus_OPT']) == F(1, 5)
assert F(posthoc['W_plus_tax_minus_OPT'])/den == F(1, 35)
report = {'status': 'PASS', 'method': 'explicit separate unit clients and complete ordered strategy',
          'original_helper_calls': 0, 'canonical_solver_calls': 0, 'lp_calls': 0,
          'new_seed': seed, 'posthoc_positive_point': posthoc,
          'normalization_total_mass': den,
          'posthoc_point_is_original_FOUND_output': False,
          'candidate_file_written_by_original': False,
          'scope': 'two new fixed-policy feasible points; no exact cone optimum or full 80-sample replay'}
(HERE/'first-sample/unit-client-audit.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'seed_clients': seed['unit_clients'],
                  'new_point_clients': posthoc['unit_clients'], 'rows_per_case': 1554,
                  'new_point_W': 4, 'new_point_OPT4': 7, 'new_point_full_tax': '16/5',
                  'new_point_normalized_gap': '1/35', 'lp_calls': 0}))
