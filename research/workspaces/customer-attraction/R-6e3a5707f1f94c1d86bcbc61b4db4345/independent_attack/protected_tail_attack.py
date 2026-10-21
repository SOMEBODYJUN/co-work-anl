"""Attack the conjectured sharp protected two-tail price inequality.

For a complete-history two-tail subgame and D outside its final union, test
B_D(uA) <= max(0,uB-uA). Floating LP proposes, rational rows verify witnesses.
"""
from __future__ import annotations
import importlib.util,itertools,json,math,random,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('cone_audit',ROOT/'tests/audits/customer_attraction_strategy_lp.py')
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F())

def game_data(p,h,actions):
    A=actions[h];B=actions[h+(A,)]
    n=(1<<p)-1
    def pay(seq,a):return mod.payoff_row(p,tuple(seq.count(j) for j in range(p)),a)
    ua=pay(h+(A,B),A);ub=pay(h+(A,B),B)
    rows=[]
    for T in range(p):
        R=actions[h+(T,)]
        rows.append(tuple(x-y for x,y in zip(ua,pay(h+(T,R),T))))
        for Q in range(p):
            rows.append(tuple(x-y for x,y in zip(pay(h+(T,R),R),pay(h+(T,Q),Q))))
    rows.append(tuple(y-x for x,y in zip(ua,ub)))
    finalmask=sum(1<<a for a in set(h+(A,B)))
    D=np.array([not (mask&finalmask) for mask in range(1,1<<p)],dtype=float)
    inc=np.array([[(mask>>a)&1 for mask in range(1,1<<p)] for a in range(p)],dtype=float)
    return A,B,ua,ub,tuple(rows),D,inc

def portfolio(r,ua,D,inc):
    p,n=inc.shape
    # y<=D and y<=membership sums; max r.y-price.sum(z).
    price=float(dot(r,ua))
    lp=linprog(np.r_[np.repeat(price,p),-np.asarray(r,float)],
               A_ub=np.hstack((-inc.T,np.eye(n))),b_ub=np.zeros(n),
               bounds=[(0,1)]*p+[(0,int(v)) for v in D],method='highs')
    if not lp.success:return None
    z=tuple(F(float(x)).limit_denominator(100000) for x in lp.x[:p])
    coverage=tuple(F(int(d))*min(F(1),sum((z[a] for a in range(p) if inc[a,j]),F())) for j,d in enumerate(D))
    return z,coverage

def attack(p,h,actions,initial,rng,source):
    A,B,ua,ub,rows,D,inc=game_data(p,h,actions)
    matrix=np.array(rows,float);norm=np.array([float(x+y) for x,y in zip(ua,ub)])
    # If the original endpoint does not have uA<=uB, obtain an arbitrary feasible endpoint.
    r=np.array(initial,float)
    if dot(r,ua)>dot(r,ub)+1e-9:
        lp=linprog(rng.random()*np.ones(len(r)),A_ub=-matrix,b_ub=np.zeros(len(rows)),A_eq=[norm],b_eq=[1],bounds=(0,None),method='highs')
        if not lp.success:return None
        r=lp.x
    best=None
    available=[a for a in range(p) if a not in h+(A,B)]
    seeds=[]
    for size in range(1,min(4,len(available))+1):
        for J in itertools.combinations(available,size):
            seeds.append(tuple(F(int(a in J)) for a in range(p)))
            if size>=3:seeds.append(tuple(F(int(a in J),2) for a in range(p)))
    for iteration,z in enumerate(seeds):
        cov=tuple(F(int(d))*min(F(1),sum((z[a] for a in range(p) if inc[a,j]),F())) for j,d in enumerate(D))
        tau=sum(z,F())
        objective=tuple(c-(tau-1)*a-b for c,a,b in zip(cov,ua,ub))
        lp=linprog(-np.array(objective,float),A_ub=-matrix,b_ub=np.zeros(len(rows)),A_eq=[norm],b_eq=[1],bounds=(0,None),method='highs')
        if not lp.success:break
        r=lp.x
        values=tuple(F(float(x)).limit_denominator(1000000) for x in r)
        exact=None
        if min(values)>=0 and all(dot(row,values)>=0 for row in rows) and dot(tuple(a+b for a,b in zip(ua,ub)),values)==1:
            exact=dot(objective,values)
        rec={'source':source,'prefix':h,'A':A,'B':B,'proposal':float(-lp.fun),'exact_gap':str(exact) if exact is not None else None,'z':[str(x) for x in z]}
        if best is None or rec['proposal']>best['proposal']:best=rec
        if exact is not None and exact>0:
            scale=math.lcm(*(v.denominator for v in values));clones=[int(v*scale) for v in values]
            witness={'scope':'auxiliary sharp protected two-tail price failure, not main half counterexample',**rec,
                     'clones':clones,'topics':p,'actions':[{'history':list(hh),'action':a} for hh,a in actions.items() if hh==h or (len(hh)==len(h)+1 and hh[:len(h)]==h)],
                     'uA':str(dot(ua,values)),'uB':str(dot(ub,values)),'scale':scale}
            (HERE/'protected_tail_counterexample.json').write_text(json.dumps(witness,indent=2)+'\n')
            print(json.dumps(witness),flush=True)
            return best
    return best

if __name__=='__main__':
    rng=random.Random(2026102142);records=[]
    for path in sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json')):
        obj=json.loads(path.read_text())
        if not isinstance(obj,dict):continue
        lst=obj.get('actions')
        if not isinstance(lst,list) or not lst or not all(isinstance(x,dict) and 'history' in x and 'action' in x for x in lst):continue
        actions={tuple(x['history']):x['action'] for x in lst}
        m=max(map(len,actions))+1;p=max([a for h,a in actions.items()]+[a for h in actions for a in h])+1
        if p>7 or m>5:continue
        # Original customer data is not required: start from a feasible cone LP.
        for h in itertools.product(range(p),repeat=m-2):
            initial=[1]*((1<<p)-1)
            result=attack(p,h,actions,initial,rng,str(path.relative_to(ROOT)))
            if result:
                records.append(result);print(json.dumps(result),flush=True)
                (HERE/'protected_tail_run.json').write_text(json.dumps(records,indent=2)+'\n')
                if result['exact_gap'] and F(result['exact_gap'])>0:sys.exit(0)
