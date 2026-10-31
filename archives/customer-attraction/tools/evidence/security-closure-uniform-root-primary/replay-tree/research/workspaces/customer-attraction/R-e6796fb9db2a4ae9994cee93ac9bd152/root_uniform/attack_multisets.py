"""Attack the true-query uniform interface, including repeated comparisons.

Floating LPs only discover candidates; a discovered positive point must pass
exact cone verification before export. No finite search proves the interface.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json
import sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path[:0] = [str(ROOT), str(ROOT / 'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone, payoff_row, coverage_row, integer_clones


def attack(source):
    document = json.loads(source.read_text())
    data = document['strategy']
    actions = {tuple(v['history']): v['action'] for v in data['actions']}
    p = 1 + max([a for a in actions.values()] + [a for h in actions for a in h])
    m = max(map(len, actions)) + 1
    cone = StrategyCone(p, m, actions)
    path = ()
    columns = [[F(0)] * ((1 << p) - 1) for _ in range(p)]
    for i in range(m):
        for a in range(p):
            columns[a] = [x+y for x,y in zip(columns[a],payoff_row(p,cone.terminals[path+(a,)],a))]
        path += (actions[path],)
    best = {'normalized_violation': -1e30}
    checked = 0
    for k in range(1,min(m,p)+1):
        for support in combinations(range(p), k):
            cov = coverage_row(p,support)
            # With a fixed support the comparison counts form a simplex.
            # Its vertices place all m-k surplus copies on one theme.
            for filler in (support if k < m else (support[0],)):
                counts = tuple(int(a in support) + (m-k if a == filler else 0) for a in range(p))
                obj = tuple(m*cov[j]-(m-1)*cone.welfare[j]-sum(counts[a]*columns[a][j] for a in support) for j in range(len(cov)))
                res = linprog(-np.array(obj,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[np.array(cone.welfare,dtype=float)],b_eq=[1],bounds=(0,None),method='highs')
                if not res.success:
                    raise RuntimeError(res.message)
                checked += 1
                if -res.fun > best['normalized_violation']:
                    best = {'normalized_violation': float(-res.fun),'comparison_counts':counts}
                if -res.fun > 1e-7:
                    values = tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
                    if not cone.verify(values) or sum(x*y for x,y in zip(values,cone.welfare)) != 1:
                        values = cone.recover_vertex(res.x)
                    if values is None or not cone.verify(values):
                        raise RuntimeError('exact recovery failed')
                    clones = integer_clones(values)
                    violation = sum(x*y for x,y in zip(obj,clones))
                    assert violation > 0
                    return {'source': str(source.relative_to(ROOT)),'players':m,'topics':p,'LPs':checked,'candidate':{'multiplicities':{str(i):c for i,c in enumerate(clones,1) if c},'comparison_counts':counts,'violation':str(violation),'strategy':data}}
    return {'source':str(source.relative_to(ROOT)),'players':m,'topics':p,'LPs':checked,'best':best,'scope':'finite floating observations only'}


if __name__ == '__main__':
    out = Path(__file__).with_name('multisets_report.json')
    if out.exists():
        raise FileExistsError(out)
    names = sys.argv[1:] or ['individual_security_failure','aggregate_theta_failure','root_tax_failure','global_decorrelation_failure']
    records = []
    for name in names:
        record = attack(ROOT / 'evidence/certificates/customer_attraction' / (name+'.json'))
        records.append(record)
        out.write_text(json.dumps(records,indent=2)+'\n')
        print(json.dumps({k:v for k,v in record.items() if k != 'candidate'}),flush=True)
        if 'candidate' in record:
            print('EXACT CANDIDATE EXPORTED',flush=True)
            break
