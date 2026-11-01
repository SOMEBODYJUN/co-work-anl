"""Exploratory floats: attack on-path decoupled budget at security-optimal p.

Only fixed complete group-response strategies are used here. No result is a
proof until a separate exact reconstruction verifies every history and LP bound.
"""
import json
from functools import lru_cache
from itertools import product, combinations_with_replacement
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parent

def build(n=3,m=6,policy=None):
    masks=np.arange(1,1<<m)
    hit=((masks[:,None]>>np.arange(m))&1).astype(float)
    histories=[h for d in range(n) for h in product(range(m),repeat=d)]
    if policy is None:
        def policy(h):
            if not h:return 0
            if len(h)==1:return m//2 if h[0]<m//2 else 0
            group=range(0,m//2) if h[-1]<m//2 else range(m//2,m)
            return min(a for a in group if a not in h)
    @lru_cache(None)
    def term(h):
        return h if len(h)==n else term(h+(policy(h),))
    def row(a,z):
        den=hit[:,z].sum(axis=1)
        return np.divide(hit[:,a],den,out=np.zeros(len(masks)),where=den>0)
    G=np.unique(np.array([row(policy(h),term(h))-row(a,term(h+(a,)))
                         for h in histories for a in range(m)]),axis=0)
    z=term(())
    c=(hit[:,z].sum(axis=1)>0).astype(float)
    backgrounds=list(combinations_with_replacement(range(m),n-1))
    F=np.array([hit.T/(1+hit[:,B].sum(axis=1)) for B in backgrounds])
    M=[]
    for i in range(n):
        h=z[:i]
        M.append(np.array([hit.T/(1+hit[:,term(h+(b,))[:i]+term(h+(b,))[i+1:]].sum(axis=1)) for b in range(m)]))
    # M[i,b,a,T]: rivals after actual player i chooses b, queried at a.
    return G,c,F,np.array(M),z,hit

def security(F,w,rng=None):
    A=F@w
    m=A.shape[1]
    lp=linprog(np.r_[np.zeros(m),-1.],A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),A_eq=[np.r_[np.ones(m),0]],b_eq=[1],bounds=[(0,None)]*m+[(None,None)],method='highs')
    assert lp.success
    return lp.x[:-1],lp.x[-1]

def main(seed=741,samples=1500):
    rng=np.random.default_rng(seed)
    G,c,F,M,z,hit=build()
    k=len(c);n=3
    rows={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2}
    base=np.array([rows.get(i,0) for i in range(1,k+1)],float);base/=sum(base)
    best=None;ratios=[]
    for it in range(samples):
        objective=rng.normal(size=k)
        if it%3==0:objective=rng.exponential(size=k)*rng.choice([-1,1],size=k)
        lp=linprog(objective,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(k)],b_eq=[1],bounds=(0,None),method='highs')
        assert lp.success
        blend=[0,1e-4,.005,.05,.2][it%5]
        w=(1-blend)*lp.x+blend*base
        p,v=security(F,w)
        budget=float(c@w-np.einsum('b,a,ibat,t->',p,p,M,w))
        strong=float(c@w-n*v)
        if best is None or budget<best['budget']:
            best=dict(iteration=it,budget=budget,strong_gap=strong,w=w.tolist(),p=p.tolist(),v=v,W=float(c@w),min_spe_slack=float(np.min(G@w)),seed=seed)
            (ROOT/'best_optimal_budget.json').write_text(json.dumps(best,indent=2)+'\n')
            print(json.dumps({k:v for k,v in best.items() if k not in ['w','p']}),flush=True)
        ratios.append([budget,strong])
    report=dict(samples=samples,seed=seed,minimum_budget=min(r[0] for r in ratios),minimum_strong_gap=min(r[1] for r in ratios),negative_budgets=sum(r[0]<-1e-8 for r in ratios),root=z)
    (ROOT/'optimal_budget_search_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--samples',type=int,default=1500);p.add_argument('--seed',type=int,default=741)
    args=p.parse_args();main(args.seed,args.samples)
