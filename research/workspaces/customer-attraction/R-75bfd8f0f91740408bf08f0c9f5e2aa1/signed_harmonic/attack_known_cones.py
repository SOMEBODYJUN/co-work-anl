"""Attack two explicit budgets within inherited complete-strategy cones.

This is not a random SPE scan. A floating LP only proposes customer weights;
any claimed counterexample requires subsequent exact full-history replay.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
import math
import sys
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, CustomerType, StrategyCertificate, verify_certificate
from audit_known import all_minimal_optima, budgets


def attack(name, objective, strict=1e-6):
    inst = Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()))
    dat = json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    for key in ('strategy', 'certificate'):
        if key in dat and 'actions' in dat[key]:
            dat = dat[key]
            break
    actions = {tuple(row['history']): row['action'] for row in dat['actions']}
    m, p = inst.players, inst.topic_count
    masks = range(1, 1 << p)

    @lru_cache(None)
    def play(h):
        return h if len(h) == m else play(h+(actions[h],))

    @lru_cache(None)
    def utility(h, topic):
        return tuple(F(int(mask >> topic & 1), sum(mask >> a & 1 for a in h))
                     if mask >> topic & 1 else F(0) for mask in masks)

    rows, bounds = [], []
    for h, a in actions.items():
        actualU = utility(play(h), a)
        for b in range(p):
            if a != b:
                deviatingU = utility(play(h+(b,)), b)
                rows.append([float(v-u) for u, v in zip(actualU, deviatingU)])
                bounds.append(0.)
    actual = play(())
    origopt = list(all_minimal_optima(inst))
    # Choose inherited minimal-B comparator; for these files its support has m topics.
    _, q = min(origopt, key=lambda x: budgets(inst, inst.counts(actual), x[1])['B_gap'])
    support = tuple(a for a in range(p) if q[a])
    if len(support) != m:
        return {'name': name, 'skipped': 'inherited optimum support smaller than m'}
    optcover = np.array([int(any(mask >> a & 1 for a in support)) for mask in masks])
    for k in range(1, m+1):
        for other in combinations(range(p), k):
            if other != support:
                rows.append([int(any(mask >> a & 1 for a in other))-v for mask, v in zip(masks, optcover)])
                bounds.append(-strict)
    objectiveRow = []
    for mask in masks:
        c = sum(mask >> a & 1 for a in actual)
        d = sum(q[a] for a in range(p) if mask >> a & 1)
        value = (sum((F(1, c+j) for j in range(1, d+1)), F(0))
                 if objective == 'B' else F(d, c+1))
        objectiveRow.append(value-int(c > 0)-int(c > 0 and d == 0))
    result = linprog(-np.array(list(map(float, objectiveRow))), A_ub=np.array(rows),
                     b_ub=np.array(bounds), A_eq=[np.ones(len(masks))], b_eq=[1.],
                     bounds=(0, None), method='highs')
    report = {'name': name, 'objective': objective, 'strict_comparator_margin': strict,
              'status': result.message, 'comparator_counts': q,
              'float_violation': -result.fun if result.success else None}
    if result.success and -result.fun > 1e-7:
        rational = [F(float(w)).limit_denominator(10**7) for w in result.x]
        scale = math.lcm(*(x.denominator for x in rational))
        weights = [int(x*scale) for x in rational]
        divisor = math.gcd(*weights)
        weights = [w//divisor for w in weights]
        target = Instance(inst.topics,
                          tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1), w)
                                for mask, w in zip(masks, weights) if w), m)
        cert = StrategyCertificate(actions, target.counts(actual))
        verification = verify_certificate(target, cert)
        report.update(exact_spe=verification.valid, proposed_instance=target.to_dict(),
                      exact_fixed_comparator=budgets(target, target.counts(actual), q))
        if verification.valid:
            opts = [(qq, budgets(target, target.counts(actual), qq)) for _, qq in all_minimal_optima(target)]
            minbudget = min(opts, key=lambda v: v[1][objective+'_gap'])
            report.update(exact_optimum=target.optimal_welfare(), exact_all_optima_extrema=len(opts),
                          exact_minimum=dict(q=minbudget[0], **minbudget[1]))
            if minbudget[1][objective+'_gap'] > 0:
                report['status'] = 'EXACT COMPLETE-SPE COUNTEREXAMPLE'
                report['strategy'] = cert.to_dict()
    return report


if __name__ == '__main__':
    report = [attack(name, target) for name in ['optimal_last_query_failure',
                                               'portfolio_matching_failure',
                                               'prefix_balance_failure',
                                               'root_tax_failure']
              for target in ['B', 'D']]
    path = HERE/'known_cone_attack.json'
    path.write_text(json.dumps(report, indent=2, default=str)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k not in ('strategy', 'proposed_instance')}
                      for r in report], indent=2, default=str))
