"""Full-depth fixed-policy cone attacks on individual complete menus.
Counts select one Markov pure policy; all count states retain every IC row.
Any positive LP point must be rationally audited before a claim is made.
"""
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
import json, random
import numpy as np
from scipy.optimize import linprog

def add(p,a): return p[:a]+(p[a]+1,)+p[a+1:]
def build(d,m,w):
    masks=list(range(1,1<<d));bits=np.array([[b>>a&1 for b in masks] for a in range(d)])
    policy={};term={};rows=[]
    @lru_cache(None)
    def ur(a,q):
        counts=np.array(q)@bits
        return np.divide(bits[a],counts,out=np.zeros(len(masks)),where=counts!=0)
    @lru_cache(None)
    def rec(p):
        if sum(p)==m: term[p]=p;return p
        child=[rec(add(p,a)) for a in range(d)]
        a=max(range(d),key=lambda a:float(ur(a,child[a])@w))
        policy[p]=a;term[p]=child[a]
        for b in range(d): rows.append(ur(a,child[a])-ur(b,child[b]))
        return child[a]
    root=(0,)*d;rec(root)
    return masks,bits,policy,term,np.array(rows),ur

def trial(d,m,w,rng):
    masks,bits,policy,term,ic,ur=build(d,m,w)
    p=(0,)*d
    while sum(p)<m:
        a=policy[p];q=term[p];u=ur(a,q)
        if sum(p)<=m-3:
            columns=[term[add(p,b)] for b in range(d)]
            # Independent query is fixed while LP varies customer multiplicities.
            for pp in [np.ones(d)/d]+[rng.dirichlet(np.ones(d)) for _ in range(2)]:
                cb=[]
                for qb in columns:
                    load=np.array(qb)@bits
                    cb.append((pp@bits)/(1+load)-u)
                cb=np.array(cb)
                # max margin t, W=1, every complete-policy IC >=0.
                welfare=(np.array(q)@bits>0).astype(float)
                result=linprog([0.]*len(masks)+[-1.],
                    A_ub=np.vstack([np.column_stack([-ic,np.zeros(len(ic))]),
                                    np.column_stack([-cb,np.ones(d)])]),
                    b_ub=np.zeros(len(ic)+d),A_eq=[list(welfare)+[0.]],b_eq=[1.],
                    bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
                if result.success and result.x[-1]>1e-8:
                    return dict(d=d,m=m,masks=masks,weights=result.x[:-1].tolist(),
                                prefix=p,query=pp.tolist(),margin=float(result.x[-1]),
                                policy=[dict(prefix=p,action=a) for p,a in policy.items()],
                                target=q,columns=columns,current_action=a)
        p=add(p,a)

def main():
    rng=np.random.default_rng(987315)
    for t in range(300):
        d=int(rng.choice([4,5,6]));m=int(rng.choice([4,5,6,7]))
        w=rng.integers(0,30,size=(1<<d)-1).astype(float)
        w*=rng.random(len(w))<.5
        bad=trial(d,m,w,rng)
        if bad:
            out=dict(trial=t,**bad)
            Path(__file__).with_name('menu_cone_candidate.json').write_text(json.dumps(out,indent=2))
            print('LP CANDIDATE',t,d,m,bad['prefix'],bad['margin'],flush=True);return
        if t%10==0:print('checked',t,flush=True)
    print('No finite counterexample',flush=True)
if __name__=='__main__':main()
