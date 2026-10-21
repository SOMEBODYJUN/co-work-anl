"""Finite all-customer-type attack on uniform deviations in saved full cones."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone, payoff_row, coverage_row, dot, integer_clones, instance_from_clones, independently_verify


def attack(actions,m,p):
    cone=StrategyCone(p,m,actions)
    h=()
    path=[]
    while len(h)<m:
        a=actions[h];path.append(a);h+=(a,)
    costs=[]
    for a in range(p):
        rows=[payoff_row(p,cone.terminals[tuple(path[:i])+(a,)],a) for i in range(m)]
        costs.append(tuple(sum(col,F(0)) for col in zip(*rows)))
    best=0.0
    trials=0
    for comp in combinations_with_replacement(range(p),m):
        cov=coverage_row(p,set(comp))
        obj=tuple((m-1)*w+sum((costs[a][j] for a in comp),F(0))-m*o
                  for j,(w,o) in enumerate(zip(cone.welfare,cov)))
        res=linprog(np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),
                    A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
        trials+=1
        if not res.success:
            raise RuntimeError(res.message)
        best=min(best,float(res.fun))
        if res.fun < -1e-7:
            v=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
            if not cone.verify(v) or dot(cone.welfare,v)!=1:
                v=cone.recover_vertex(res.x)
            if v is not None and cone.verify(v) and dot(obj,v)<0:
                clones=integer_clones(v)
                assert independently_verify(cone,clones)
                game=instance_from_clones(p,m,clones)
                return {'failure':True,'gap':str(dot(obj,clones)),
                        'instance':game.to_dict(),'comparison':comp,
                        'strategy':{'terminal_counts':cone.root,'actions':[{'history':h,'action':a} for h,a in actions.items()]},
                        'LP_trials':trials}
    return {'failure':False,'minimum_float_gap':best,'LP_trials':trials}


def main():
    source=ROOT/'evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json'
    raw=json.loads(source.read_text())
    out={'scope':'saved full strategy cones only','source':str(source.relative_to(ROOT)),
         'cones':[],'general_claim_proved':False}
    for i,cp in enumerate(raw['cone_proofs']):
        actions={tuple(x['history']):x['action'] for x in cp['actions']}
        result=attack(actions,4,5)
        out['cones'].append(result)
        print(json.dumps({'cone':i,**{k:v for k,v in result.items() if k not in ('strategy','instance')}}),flush=True)
        if result['failure']:
            break
    Path(__file__).with_name('cone_results.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':
    main()
