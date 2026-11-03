"""Bounded all-history fixed-policy cone falsification of precise netROW."""
import json, math, random, sys
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from attack_netrow import run

def cone(data):
    m,k,L=data['m'],data['k'],data['scale']; masks=list(range(1,1<<k))
    policy={tuple(map(int,h.split(','))) if h else ():a for h,a in data['policy'].items()}
    @lru_cache(None)
    def finish(h):
        if len(h)==m:return h
        return finish(h+(policy[h],))
    @lru_cache(None)
    def coeff(z,i):
        return np.array([L//sum(bool(mask>>a&1) for a in z) if mask>>z[i]&1 else 0
                         for mask in masks],dtype=np.int64)
    rows=[]
    for h in policy:
        z=finish(h);i=len(h)
        for a in range(k):
            if h: rows.append(coeff(z,i)-coeff(finish(h+(a,)),i))
    z=finish(());bmask=sum(1<<a for a in set(z))
    cover_actual=np.array([L*int(bool(mask&bmask)) for mask in masks],dtype=np.int64)
    queries=[[coeff(finish(z[:i]+(a,)),i) for a in range(k)] for i in range(m)]
    Gamma=np.array(rows,dtype=np.int64)
    best=(0,None)
    for ts in combinations_with_replacement(range(k),m):
        cmask=sum(1<<a for a in set(ts))
        oc=np.array([L*int(bool(mask&cmask)) for mask in masks],dtype=np.int64)
        for i in range(m-2):
            objective=cover_actual-oc+sum(queries[i][a] for a in ts)
            sol=linprog(objective,A_ub=-Gamma,b_ub=np.zeros(len(Gamma)),
                        A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
            if sol.success and sol.fun<best[0]-1e-9:
                best=(float(sol.fun),dict(i=i,ts=ts,x=sol.x.tolist()))
            if sol.success and sol.fun< -1e-7:
                w=[Fraction(float(x)).limit_denominator(10**6) for x in sol.x]
                ic=[sum(int(a)*b for a,b in zip(row,w)) for row in Gamma]
                gap=-sum(int(a)*b for a,b in zip(objective,w))
                if min(ic)>=0 and gap>0:
                    ints=math.lcm(*(x.denominator for x in w))
                    exact={mask:int(x*ints) for mask,x in zip(masks,w) if x}
                    return dict(data=data,role=i,comparator=ts,weights=exact,
                                gap=str(gap*ints/L),ic_min=str(min(ic)*ints/L),
                                IC=len(ic),ordered_histories=len(policy))
    return best

if __name__=='__main__':
    rng=random.Random(110112);trials=int(sys.argv[1]) if len(sys.argv)>1 else 12
    global_best=(0,None)
    for trial in range(trials):
        m,k=rng.choice([(3,5),(4,5),(3,6)])
        weights={mask:rng.randrange(1,10) for mask in range(1,1<<k) if rng.random()<0.18}
        if not weights: weights={1:1}
        _,data=run(m,k,weights,rng.randrange(1<<30))
        out=cone(data)
        if isinstance(out,dict):
            p=Path(__file__).with_name('root_free_netrow_counterexample.json');p.write_text(json.dumps(out,indent=2))
            print('EXACT_COUNTEREXAMPLE',str(p),out['gap'],flush=True);break
        if out[0]<global_best[0]:global_best=(out[0],trial)
        print('policy',trial,'m',m,'k',k,'best',out[0],'global',global_best,flush=True)
