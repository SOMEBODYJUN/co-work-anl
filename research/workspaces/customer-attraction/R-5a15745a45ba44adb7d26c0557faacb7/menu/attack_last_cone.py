"""Finite attack on LAST, not on the half theorem.

Keep every ordered-history IC of one supplied complete strategy, vary all
nonnegative customer-type multiplicities, and test a finite family of fixed
query laws. A positive result requires exact rational rechecking separately.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
import numpy as np
from scipy.optimize import linprog


source = Path(sys.argv[1])
data = json.loads(source.read_text())
k = len(data['instance']['topics'])
m = data['instance']['players']
actions = {tuple(z['history']): z['action'] for z in data['certificate']['actions']}
types = list(range(1, 1 << k))


def terminal(h):
    h = tuple(h)
    while len(h) < m:
        h += (actions[h],)
    return h


def payoff(z, i):
    return [F(1, sum(bool(mask & (1 << a)) for a in z))
            if mask & (1 << z[i]) else F(0) for mask in types]


z = terminal(())
coverage = [F(any(mask & (1 << a) for a in z)) for mask in types]
rows = []
for depth in range(m):
    for h in product(range(k), repeat=depth):
        prescribed = payoff(terminal(h), depth)
        for a in range(k):
            alternate = payoff(terminal(h + (a,)), depth)
            rows.append([x-y for x, y in zip(prescribed, alternate)])
gamma = np.array([[float(x) for x in row] + [0.] for row in rows])
best = None
checked = 0
for support_mask in range(1, 1 << k):
    support = [a for a in range(k) if support_mask & (1 << a)]
    p = [F(a in support, len(support)) for a in range(k)]
    price_rows = []
    for a in range(k):
        price_rows.append([sum((p[t] for t in range(k) if mask & (1 << t)), F(0)) /
                           (1 + sum(bool(mask & (1 << t)) for t in z[:-1]) +
                            bool(mask & (1 << a))) - coverage[j]/m
                           for j, mask in enumerate(types)])
    # t <= p K_b(:,a)-W/m for every possible last column a.
    aub = np.concatenate([-gamma, np.array([[-float(x) for x in row]+[1.]
                                            for row in price_rows])])
    result = linprog([0.]*len(types)+[-1.], A_ub=aub,
                     b_ub=np.zeros(len(aub)),
                     A_eq=[[float(x) for x in coverage]+[0.]], b_eq=[1.],
                     bounds=[(0,None)]*len(types)+[(None,None)], method='highs')
    checked += 1
    if result.success and (best is None or result.x[-1] > best['gap']):
        best = {'gap':float(result.x[-1]), 'query':[str(x) for x in p],
                'weights':[float(x) for x in result.x[:-1]],
                'price_rows':[[str(x) for x in row] for row in price_rows]}
report = {'scope':'Explicit LAST candidate only; fixed complete strategy cone and fixed queries.',
          'source':str(source), 'players':m, 'topics':k, 'actual':z,
          'IC_rows':len(rows), 'queries':checked, 'best':best}
if len(sys.argv)>2:
    Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:val for key,val in report.items() if key!='best'}))
print({key:val for key,val in best.items() if key not in ('weights','price_rows')})
