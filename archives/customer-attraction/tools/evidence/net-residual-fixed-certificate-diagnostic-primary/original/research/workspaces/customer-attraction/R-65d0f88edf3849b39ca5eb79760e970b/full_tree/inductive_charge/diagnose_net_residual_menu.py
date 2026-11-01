r"""One targeted diagnostic for NRMAX and NRAVG, not a general proof.

NRMAX: sum_i max_T current payoff on O\C in actual-prefix deviation >= |O|-W.
NRAVG: (1/m)sum_(i,j) current payoff on O\C after T_j >= |O|-W.
Only previously saved complete ordered SPE certificates are inspected.
"""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
NAMES = ['residual_counterexample', 'root_tax_failure',
         'coverage_opportunity_failure', 'individual_security_failure',
         'global_decorrelation_failure', 'local_security_increment']
reports = []

def audit(name, inp, entries):
    m, q = inp['players'], len(inp['topics'])
    types = [(frozenset(x['topics']), x.get('multiplicity', 1))
             for x in inp['customers']]
    strat = {tuple(x['history']): x['action'] for x in entries}
    def leaf(h):
        h = tuple(h)
        while len(h) < m:
            h += (strat[h],)
        return h
    def payoff(y, i, selected=types):
        return sum((F(w, sum(t in B for t in y))
                    for B, w in selected if y[i] in B), F())
    comparisons = 0
    for i in range(m):
        for h in itertools.product(range(q), repeat=i):
            actual = leaf(h)
            for t in range(q):
                assert payoff(actual, i) >= payoff(leaf(h+(t,)), i)
                comparisons += 1
    z = leaf(())
    covered = [(B, w) for B, w in types if any(t in B for t in z)]
    missed = [(B, w) for B, w in types if not any(t in B for t in z)]
    W = sum(w for B, w in covered)
    tuples = list(itertools.combinations_with_replacement(range(q), m))
    cov = lambda ts: sum(w for B, w in types if any(t in B for t in ts))
    opt = max(map(cov, tuples))
    branches = [[leaf(z[:i]+(t,)) for t in range(q)] for i in range(m)]
    worst_max = worst_avg = None
    for ts in tuples:
        if cov(ts) != opt:
            continue
        residual = [(B, w) for B, w in missed if any(t in B for t in ts)]
        R = sum(w for B, w in residual)
        G = W - (opt - R)
        vals = [[payoff(y, i, residual) for y in branches[i]] for i in range(m)]
        lhs_max = sum(map(max, vals), F())
        lhs_avg = sum((vals[i][t] for i in range(m) for t in ts), F()) / m
        data = dict(comparison=ts, R=R, G=G, net=opt-W,
                    max_values=[str(max(v)) for v in vals],
                    max_gap=str(lhs_max-(opt-W)), avg_gap=str(lhs_avg-(opt-W)))
        if worst_max is None or lhs_max-(opt-W) < worst_max[0]:
            worst_max = (lhs_max-(opt-W), data)
        if worst_avg is None or lhs_avg-(opt-W) < worst_avg[0]:
            worst_avg = (lhs_avg-(opt-W), data)
    return dict(name=name, m=m, q=q, checked_IC=comparisons,
                actual=z, welfare=W, optimum=opt,
                NRMAX=worst_max[1], NRAVG=worst_avg[1])

for name in NAMES:
    inp = json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert = json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    entries = cert.get('strategy', cert)['actions']
    reports.append(audit(name, inp, entries))

# Existing 71-unit-customer counterexample, rewritten directly from its exact table.
labels = ['A', 'B', 'T', 'Q', 'R', 'S']
rows = [('A',10),('ARS',6),('B',13),('BRS',4),('BTRS',1),('BQRS',1),
        ('T',8),('TR',5),('TS',5),('Q',8),('QR',5),('QS',5)]
inp = dict(players=2,topics=labels,
           customers=[dict(topics=[labels.index(t) for t in B],multiplicity=w)
                      for B,w in rows])
entries = [dict(history=[],action=0)] + [dict(history=[i],action=t)
           for i,t in enumerate([1,5,4,5,5,4])]
reports.append(audit('existing_71_customer_omission', inp, entries))
report = dict(status='finite exact diagnostic only; no implication for untested inputs',
              reports=reports)
(OUT/'net_residual_diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
