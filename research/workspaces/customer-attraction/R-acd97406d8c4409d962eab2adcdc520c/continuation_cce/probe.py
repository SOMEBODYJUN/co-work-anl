"""Finite symmetric CCE benchmark; numeric discovery plus rational certificates.

Not a general SPE theorem. A count distribution is interpreted by uniformly
permuting all player labels, retaining every static unilateral deviation.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, CustomerType, ExactSPESolver


def counts(total, size):
    if size == 1:
        yield (total,)
    else:
        for q in range(total + 1):
            for tail in counts(total - q, size - 1):
                yield (q,) + tail


def benchmark(instance):
    m, k = instance.players, instance.topic_count
    profiles = list(counts(m, k))
    w = [F(instance.welfare(q)) for q in profiles]
    # m times each player's expected deviation payoff after random relabeling.
    mg = []
    for a in range(k):
        row = []
        for q in profiles:
            val = F(0)
            for c in instance.customers:
                if a not in c.topics:
                    continue
                load = sum(q[t] for t in c.topics)
                val += c.multiplicity * (F(m) if load == 0 else F(m + 1, load + 1))
            row.append(val)
        mg.append(row)
    regret = [[w[j] - mg[a][j] for j in range(len(profiles))] for a in range(k)]
    res = linprog([float(x) for x in w], A_ub=-np.array(regret, float),
                  b_ub=np.zeros(k), A_eq=np.ones((1, len(w))), b_eq=[1],
                  bounds=(0, None), method='highs')
    if not res.success:
        raise RuntimeError(res.message)
    p = [F(float(x)).limit_denominator(10**7) for x in res.x]
    lam = [F(float(-x)).limit_denominator(10**7) for x in res.ineqlin.marginals]
    gamma = F(float(res.eqlin.marginals[0])).limit_denominator(10**7)
    mass = sum(p)
    slacks = [sum(p[j] * row[j] for j in range(len(w))) for row in regret]
    dual = [w[j] - gamma - sum(lam[a] * regret[a][j] for a in range(k)) for j in range(len(w))]
    value = sum(p[j] * w[j] for j in range(len(w)))
    exact = (mass == 1 and min(p) >= 0 and min(slacks) >= 0 and
             min(lam) >= 0 and min(dual) >= 0 and value == gamma)
    return {'value': str(value), 'dual_value': str(gamma), 'exact_optimal': exact,
            'distribution': [[list(q), str(v)] for q, v in zip(profiles, p) if v],
            'deviation_multipliers': list(map(str, lam)),
            'regret_slacks': list(map(str, slacks)), 'minimum_dual_slack': str(min(dual)),
            'profile_count': len(profiles)}


def main():
    old = ROOT / 'research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c'
    raw = json.loads((old/'dynamic_security/strong_iid_472_five_topics.json').read_text())
    strong = Instance(tuple(map(str, raw['topics'])), tuple(
        CustomerType(frozenset(a for a in raw['topics'] if int(mask) >> a & 1), val)
        for mask, val in raw['weights'].items()), raw['players'])
    cases = {'pne_failure': Instance.from_dict(json.loads((ROOT/'examples/customer_attraction/worst_pne_welfare_failure.json').read_text())),
             'strong_iid': strong,
             'zero': Instance(('A', 'B'), (), 3),
             'single_player': Instance.from_topic_sets([{0}, {1, 2}], 1),
             'duplicate_empty': Instance.from_topic_sets([set(), {0}, {0}], 3)}
    out = {}
    for name, inst in cases.items():
        b = benchmark(inst)
        b['minimum_spe_welfare'] = ExactSPESolver(inst).minimum_welfare()
        b['optimum'] = inst.optimal_welfare()
        out[name] = b
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
