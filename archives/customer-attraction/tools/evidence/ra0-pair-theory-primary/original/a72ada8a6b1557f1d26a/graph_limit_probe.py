"""Exploration of high-background pairwise limit, not a CAG certificate."""
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path
import argparse, json, random
import numpy as np
from scipy.optimize import linprog

def minimax(C):
    k=C.shape[1]
    lp=linprog(np.r_[np.zeros(k),1.], A_ub=np.c_[C,-np.ones(len(C))], b_ub=np.zeros(len(C)), A_eq=[np.r_[np.ones(k),0]], b_eq=[1], bounds=[(0,None)]*k+[(None,None)], method='highs')
    if not lp.success: raise RuntimeError(lp.message)
    return lp.x[-1],lp.x[:-1]

def run(M,n):
    k=len(M);M=np.array(M,dtype=int)
    terms=[]
    for t in combinations_with_replacement(range(k),n):
        terms.append(tuple(t.count(a) for a in range(k)))
    idx={q:j for j,q in enumerate(terms)}
    costs=np.array([M@q-np.diag(M) for q in terms])
    @lru_cache(None)
    def out(q):
        if sum(q)==n:return frozenset((idx[q],))
        children=[out(q[:a]+(q[a]+1,)+q[a+1:]) for a in range(k)]
        cap=min(max(int(costs[z,a]) for z in child) for a,child in enumerate(children))
        return frozenset(z for a,child in enumerate(children) for z in child if costs[z,a]<=cap)
    @lru_cache(None)
    def cap(q):
        return min(max(int(costs[z,a]) for z in out(q[:a]+(q[a]+1,)+q[a+1:])) for a in range(k))
    z,p=minimax(M)
    root=(0,)*k;rootout=out(root);c0=cap(root)
    best=None
    for a in range(k):
        q1=root[:a]+(1,)+root[a+1:]
        first=[t for t in rootout&out(q1) if costs[t,a]<=c0]
        if not first:continue
        c1=cap(q1)
        for b in range(k):
            q2=q1[:b]+(q1[b]+1,)+q1[b+1:]
            eligible=[t for t in first if t in out(q2) and costs[t,b]<=c1]
            if not eligible:continue
            # Static root cost is (n-1)z; tail cost includes two actual actions.
            tail,qp=minimax((n-3)*M+(M[:,a]+M[:,b])[None,:])
            t=max(eligible,key=lambda t:costs[t,a]+costs[t,b])
            excess=float(costs[t,a]+costs[t,b]+(n-2)*tail-n*(n-1)*z)
            data=dict(excess=excess,prefix=[a,b],terminal=terms[t],first_costs=[int(costs[t,a]),int(costs[t,b])],root=z,root_query=p.tolist(),tail=tail,tail_query=qp.tolist())
            if best is None or excess>best['excess']+1e-9:best=data
    return best

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=7);ap.add_argument('--n',type=int,default=5);ap.add_argument('--samples',type=int,default=3000);ap.add_argument('--seed',type=int,default=827391);ap.add_argument('--gram',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args()
    rng=random.Random(args.seed);best=None
    for i in range(args.samples):
        M=np.zeros((args.k,args.k),dtype=int)
        if args.gram:
            for j in range(25):
                inc=np.array([int(rng.random()<.6) for a in range(args.k)])
                M+=rng.randrange(1,11)*np.outer(inc,inc)
            d=max(np.diag(M))
            M+=np.diag(d-np.diag(M))
        else:
            for a in range(args.k):
                for b in range(a):M[a,b]=M[b,a]=rng.randrange(11) if rng.random()<.65 else 0
            d=max(M.sum(axis=1))+rng.randrange(1,10)
            M+=np.eye(args.k,dtype=int)*d
        z=run(M,args.n)
        if best is None or z['excess']>best['excess']+1e-8:
            best=dict(z,matrix=M.tolist(),sample=i);print(json.dumps(best),flush=True)
        if z['excess']>1e-7:break
    if args.output:args.output.write_text(json.dumps(dict(status='pairwise high-background limit exploration, not original model certificate',completed=i+1,best=best),indent=2))
