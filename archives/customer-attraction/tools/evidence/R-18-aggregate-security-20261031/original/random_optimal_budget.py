"""Random exact-integer backward induction, followed by floating security LP."""
import json
from functools import lru_cache
from itertools import product,combinations_with_replacement
from pathlib import Path
from math import lcm
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parent

def trial(rng,n,m,kind):
    hit=((np.arange(1,1<<m)[:,None]>>np.arange(m))&1).astype(np.int64)
    L=lcm(*range(1,n+1))
    w=rng.integers(0,7,size=len(hit))
    w[rng.random(len(w))<(.8 if kind%3==0 else .4)]=0
    if kind%4==0:
        # Force an actual label symmetry, producing many rational tie histories.
        w=np.array([w[min(mask,((mask&1)<<1)|((mask&2)>>1)|(mask&~3))-1] for mask in range(1,1<<m)])
    if not sum(w):w[0]=1
    def util(z):
        load=hit[:,z].sum(axis=1)
        return (hit.T*(w*np.divide(L,load,out=np.zeros(len(w)),where=load>0))).sum(axis=1).round().astype(np.int64)
    actions={}
    @lru_cache(None)
    def term(h):
        if len(h)==n:return h
        tails=[term(h+(a,)) for a in range(m)]
        vals=[util(tails[a])[a] for a in range(m)]
        a=int(rng.choice(np.flatnonzero(np.array(vals)==max(vals))))
        actions[h]=a
        return tails[a]
    z=term(())
    c=(hit[:,z].sum(axis=1)>0).astype(float)
    Bs=list(combinations_with_replacement(range(m),n-1))
    F=np.array([hit.T/(1+hit[:,B].sum(axis=1)) for B in Bs])
    A=F@w
    lp=linprog(np.r_[np.zeros(m),-1.],A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),A_eq=[np.r_[np.ones(m),0]],b_eq=[1],bounds=[(0,None)]*m+[(None,None)],method='highs')
    assert lp.success
    p,v=lp.x[:-1],lp.x[-1]
    C=0.
    for i in range(n):
        h=z[:i]
        for b in range(m):
            q=term(h+(b,));B=q[:i]+q[i+1:]
            C+=p[b]*float((hit@p)/(1+hit[:,B].sum(axis=1))@w)
    W=float(c@w)
    return dict(n=n,m=m,w=w.tolist(),p=p.tolist(),v=v,W=W,budget=W-C,strong_gap=W-n*v,z=z,policy=[dict(history=h,action=a) for h,a in actions.items()])

def main(n,m,samples,seed):
    rng=np.random.default_rng(seed);best=None
    for it in range(samples):
        r=trial(rng,n,m,it)
        if best is None or r['budget']/sum(r['w'])<best['budget']/sum(best['w']):
            best=r;best['iteration']=it;best['seed']=seed
            (ROOT/f'best_random_optimal_budget_n{n}_m{m}.json').write_text(json.dumps(best,indent=2)+'\n')
            print(json.dumps({k:v for k,v in best.items() if k not in ['w','p','policy']}),flush=True)
        if r['budget']<-1e-7:
            print('NEGATIVE SECURITY-OPTIMAL BUDGET; check optimal-p face before conclusion',flush=True)
            break
    print(json.dumps(dict(samples=it+1,seed=seed,n=n,m=m,best_budget=best['budget'],best_strong_gap=best['strong_gap'])),flush=True)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4);ap.add_argument('--m',type=int,default=6);ap.add_argument('--samples',type=int,default=1000);ap.add_argument('--seed',type=int,default=131)
    a=ap.parse_args();main(a.n,a.m,a.samples,a.seed)
