"""Exploratory cone LP attack on the conjectural uniform portfolio interface.

Imports only floating LP machinery; exact fractions independently recheck any
reported integer candidate. No numerical infeasibility claim is a theorem.
"""
import json
import math
import sys
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent

def main():
    source=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'evidence/certificates/customer_attraction/individual_security_failure.json')
    data=json.loads(source.read_text())['strategy']
    actions={tuple(v['history']):v['action'] for v in data['actions']}
    p=1+max([a for a in actions.values()]+[a for h in actions for a in h]); m=max(map(len,actions))+1
    masks=list(range(1,1<<p))
    def terminal(h):
        while len(h)<m:
            h=h+(actions[h],)
        return h
    def payoff(a,h):
        return [F(1,sum((mask>>b)&1 for b in h)) if (mask>>a)&1 else F(0) for mask in masks]
    def sub(x,y):return [a-b for a,b in zip(x,y)]
    rows=[]
    for h,a in actions.items():
        prescribed=payoff(a,terminal(h))
        for b in range(p):
            if b!=a:rows.append(sub(prescribed,payoff(b,terminal(h+(b,)))))
    root=terminal(())
    cov=[F(any((mask>>a)&1 for a in root)) for mask in masks]
    deviations={(i,j):payoff(j,terminal(root[:i]+(j,))) for i in range(m) for j in range(p)}
    ans=[]
    for J in combinations(range(p),min(m,p)):
        obj=[m*F(any((mask>>j)&1 for j in J))-(m-1)*cov[k]-sum(deviations[i,j][k] for i in range(m) for j in J) for k,mask in enumerate(masks)]
        res=linprog(-np.array(obj,dtype=float), A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),A_eq=np.array([cov],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
        if not res.success: raise RuntimeError(res.message)
        value=-res.fun
        if value>1e-8:
            rational=[F(float(x)).limit_denominator(1000000) for x in res.x]
            denominator=math.lcm(*(x.denominator for x in rational))
            integer=[int(x*denominator) for x in rational]
            gcd=math.gcd(*integer); integer=[x//gcd for x in integer]
            slacks=[sum(x*y for x,y in zip(row,integer)) for row in rows]
            exact=sum(x*y for x,y in zip(obj,integer))
            if min(slacks)<0: raise RuntimeError('Candidate rounding violates SPE')
            witness={'status':'exact integer complete-SPE candidate','source':str(source.relative_to(ROOT)),'players':m,'topics':p,'actual':root,'comparison':J,'multiplicities':{str(mask):weight for mask,weight in zip(masks,integer) if weight},'min_spe_slack':str(min(slacks)),'uniform_violation':str(exact),'float_normalized_violation':value,'actions':data['actions']}
            path=OUT/('uniform_candidate_'+source.stem+'_'+''.join(map(str,J))+'.json')
            path.write_text(json.dumps(witness,indent=2)+'\n')
            ans.append({'comparison':J,'value':value,'exact':str(exact),'path':str(path.relative_to(ROOT))})
    print(json.dumps({'source':str(source.relative_to(ROOT)),'cones':1,'comparison_sets':math.comb(p,min(m,p)),'exact_candidates':ans},indent=2))

if __name__=='__main__':main()
