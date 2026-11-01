"""Whole policy cone attack on the union of actual-node competitor menus.

Numerical exploration only.  The menu is strictly between a root menu and all
static backgrounds.  Each member is produced by one true deviation at an
actual prefix, removing the deviating player's own action from its leaf.
"""
from __future__ import annotations
import argparse, importlib.util, json, random, sys, time
from functools import lru_cache
from itertools import product
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_security_search.py'
spec=importlib.util.spec_from_file_location('base',BASE)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def menu_geometry(n,k,policy):
    gamma,_,inc,c,z=base.geometry(n,k,policy)
    @lru_cache(None)
    def end(h):
        return h if len(h)==n else end(h+(policy[h],))
    actual=end(())
    backgrounds=set()
    for i in range(n):
        h=actual[:i]
        for a in range(k):
            leaf=end(h+(a,))
            B=leaf[:i]+leaf[i+1:]
            backgrounds.add(tuple(B.count(t) for t in range(k)))
    bs=sorted(backgrounds)
    recip=np.array([1/(1+inc@np.array(B)) for B in bs])
    return gamma,recip,inc,c,z,bs

def run(args):
    rng=random.Random(args.seed); records=[]; start=time.time()
    for j in range(args.cases):
        n,k=args.players,args.topics
        w=[0]*((1<<k)-1)
        for t in rng.sample(range(len(w)),min(len(w),args.types)):
            w[t]=rng.randint(1,20)
        policy,instance=base.make_policy(n,k,w,args.seed+j)
        G,R,I,c,z,bs=menu_geometry(n,k,policy)
        best=n; witness=None
        starts=[np.ones(k)/k]+[np.array([rng.expovariate(1) for _ in range(k)]) for _ in range(args.starts-1)]
        for q,p in enumerate(starts):
            p=p/p.sum()
            for it in range(args.iterations):
                lp,_=base.fixed_p(G,R,I,c,p)
                ratio=lp.fun
                if ratio<best-1e-8:
                    best=ratio; witness=dict(p=p.tolist(),weights=lp.x.tolist(),objective=float(ratio),start=q,iteration=it)
                p,v=base.security_p(R,I,lp.x)
        rec=dict(case=j,n=n,k=k,histories=len(policy),rows=len(G),menus=len(bs),best_W_over_menu=best,gap=n-best)
        if witness is not None:
            rec.update(witness=witness,backgrounds=bs,policy=[dict(history=h,action=a) for h,a in policy.items()])
        records.append(rec)
        print(json.dumps({x:rec[x] for x in ['case','n','k','rows','menus','best_W_over_menu','gap']}),flush=True)
        if best<args.stop_ratio-1e-7:break
    return dict(scope='Numerical exploration, complete ordered policy constraints; actual-prefix menu union only.',elapsed=time.time()-start,seed=args.seed,cases=records)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--players',type=int,default=3);ap.add_argument('--topics',type=int,default=5)
    ap.add_argument('--cases',type=int,default=100);ap.add_argument('--types',type=int,default=15)
    ap.add_argument('--starts',type=int,default=8);ap.add_argument('--iterations',type=int,default=5)
    ap.add_argument('--stop-ratio',type=float,default=2.5);ap.add_argument('--seed',type=int,default=2026102108)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); a.output.write_text(json.dumps(run(a),indent=2)+'\n')
