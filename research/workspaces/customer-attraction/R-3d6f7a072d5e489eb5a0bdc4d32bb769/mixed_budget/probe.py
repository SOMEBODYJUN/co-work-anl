"""Attack the exact-tax fractional sufficient bridge in fixed full SPE cones.

Floating LP generates candidates; feasible primal witnesses are recomputed in
Fraction. A finite cone list proves no assertion for arbitrary pure SPE.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT / 'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone, dot, serializable


def inspect(path):
    obj = json.loads(path.read_text())
    if not isinstance(obj, dict):
        return None
    strategy = obj.get('strategy', obj)
    if 'actions' not in strategy:
        return None
    actions = {tuple(x['history']): x['action'] for x in strategy['actions']}
    if not actions:
        return None
    m = max(map(len, actions)) + 1
    p = max(max(actions.values()), max((max(h) for h in actions if h), default=0)) + 1
    if p > 8 or m > 6:
        return None
    cone = StrategyCone(p, m, actions)
    loads = [sum(cone.root[a] for a in range(p) if mask >> a & 1)
             for mask in range(1, 1 << p)]
    g_c = tuple(F(int(l > 0), 1) / (1 + F(m-1, m)*l) for l in loads)
    results = []
    for a in range(p):
        g_a = tuple(F(int(mask >> a & 1), 1) / (1 + F(m-1, m)*l)
                    for mask, l in zip(range(1, 1 << p), loads))
        objective = tuple(m*x-y-z for x,y,z in zip(g_a,cone.welfare,g_c))
        r = linprog(-np.array(objective, dtype=float), A_ub=-cone.matrix,
                    b_ub=np.zeros(len(cone.rows)), A_eq=[cone.welfare], b_eq=[1],
                    bounds=(0,None), method='highs')
        if not r.success:
            results.append({'query':a,'status':r.message})
            continue
        v = tuple(F(float(x)).limit_denominator(10**7) for x in r.x)
        if not cone.verify(v) or dot(cone.welfare,v) != 1:
            v = cone.recover_vertex(r.x)
        exact = v is not None and cone.verify(v) and dot(cone.welfare,v) == 1
        results.append({'query':a,'floating_gap':float(-r.fun),
                        'exact_primal':exact,
                        'exact_gap':dot(objective,v) if exact else None,
                        'weights':{i+1:x for i,x in enumerate(v) if x} if exact else None})
    return {'path':str(path.relative_to(ROOT)),'players':m,'topics':p,
            'root':cone.root,'nodes':len(actions),'records':results}


if __name__ == '__main__':
    paths = sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json'))
    paths += [Path(__file__).parents[1]/'true_spe_search/fractional_weak_m4_certificate.json']
    rows=[]
    for path in paths:
        try:
            r=inspect(path)
        except (KeyError,ValueError) as exc:
            print(json.dumps({'skipped':path.name,'reason':str(exc)}),flush=True)
            continue
        if r is not None:
            rows.append(r)
            best=max((v for v in r['records'] if v.get('exact_primal')),
                     key=lambda v:v['exact_gap'],default={})
            print(json.dumps(serializable({'name':path.name,'best':best})),flush=True)
    Path(__file__).with_name('results.json').write_text(json.dumps(serializable({
        'status':'finite fixed-cone attack only','universal_claim_proved':False,
        'rows':rows}),indent=2)+'\n')
