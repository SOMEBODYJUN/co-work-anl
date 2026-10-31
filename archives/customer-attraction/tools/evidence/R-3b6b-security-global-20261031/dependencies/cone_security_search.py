"""Exploratory full-policy cone attack on aggregate static security.

No local security inequalities or frozen responses are imposed. A numerical
positive result would be a candidate only until exact reconstruction/replay.
"""
from __future__ import annotations
import argparse, json, random, time, sys
from fractions import Fraction
from functools import lru_cache
from itertools import product, combinations_with_replacement
from math import lcm
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType, Instance, ExactSPESolver

def make_policy(n,k,w,seed):
    rng=random.Random(seed)
    instance=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),int(v)) for mask,v in enumerate(w,1) if v),n)
    solver=ExactSPESolver(instance)
    cert=solver.certificate(min(solver.worst_outcomes()),action_selector=lambda h,A:rng.choice(A),continuation_selector=lambda h,C:rng.choice(C))
    return dict(cert.actions),instance

def geometry(n,k,policy):
    mask=np.arange(1,1<<k)
    incidence=((mask[:,None]>>np.arange(k))&1).astype(np.int16)
    scale=lcm(*range(1,n+1))
    @lru_cache(None)
    def end(h):
        if len(h)==n:return tuple(h.count(a) for a in range(k))
        return end(h+(policy[h],))
    @lru_cache(None)
    def row(a,c):
        d=incidence@np.array(c)
        return tuple(np.where(incidence[:,a],scale//np.maximum(d,1),0).tolist())
    rows=set()
    for h,a in policy.items():
        actual=np.array(row(a,end(h)))
        for b in range(k):
            if b!=a:rows.add(tuple(actual-np.array(row(b,end(h+(b,))))))
    rows.discard((0,)*(len(mask)))
    gamma=np.array(sorted(rows),float)/scale
    bg=[]
    for B in combinations_with_replacement(range(k),n-1):
        c=np.bincount(B,minlength=k)
        bg.append(1/(1+incidence@c))
    recip=np.array(bg)
    c=(incidence@np.array(end(()))>0).astype(float)
    return gamma,recip,incidence,c,end(())

def fixed_p(gamma,recip,incidence,c,p):
    beta=recip*(incidence@p)[None,:]
    A=-np.vstack((gamma,beta))
    b=np.r_[np.zeros(len(gamma)),-np.ones(len(beta))]
    lp=linprog(c,A_ub=A,b_ub=b,bounds=(0,None),method='highs')
    if not lp.success:raise RuntimeError(lp.message)
    return lp,beta

def security_p(recip,incidence,w):
    # max t s.t. expected reward in each competitor background >=t.
    rewards=(recip*w)@incidence
    k=incidence.shape[1]
    lp=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-rewards,np.ones(len(rewards))],b_ub=np.zeros(len(rewards)),A_eq=np.array([np.r_[np.ones(k),0]]),b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
    assert lp.success
    return lp.x[:-1],lp.x[-1]

def run(args):
    rng=random.Random(args.seed); records=[];start=time.time()
    for j in range(args.cases):
        n,k=args.players,args.topics
        # Sparse types, with both low and high interest frequencies.
        w=[0]*((1<<k)-1)
        for t in rng.sample(range(len(w)),min(len(w),args.types)):
            w[t]=rng.randint(1,20)
        policy,instance=make_policy(n,k,w,args.seed+j)
        gamma,recip,incidence,c,z=geometry(n,k,policy)
        best=n
        bestrec=None
        starts=[np.ones(k)/k]
        starts += [np.array([rng.expovariate(1) for a in range(k)]) for _ in range(args.starts-1)]
        for q,p in enumerate(starts):
            p=p/p.sum()
            for it in range(args.iterations):
                lp,beta=fixed_p(gamma,recip,incidence,c,p)
                ratio=lp.fun
                if ratio<best-1e-8:
                    best=ratio;bestrec=dict(p=p.tolist(),weights=lp.x.tolist(),objective=float(ratio),start=q,iteration=it)
                p,v=security_p(recip,incidence,lp.x)
        rec=dict(case=j,players=n,topics=k,ordered_histories=len(policy),unique_gamma_rows=len(gamma),root_counts=z,actual_W=instance.welfare(z),best_cone_W=best,gap=n-best,witness=bestrec)
        records.append(rec)
        print(json.dumps({x:rec[x] for x in ['case','players','topics','unique_gamma_rows','root_counts','best_cone_W','gap']}),flush=True)
        if best<n-1e-6:
            rec['policy']=[dict(history=h,action=a) for h,a in policy.items()]
            break
    return dict(scope='Numerical exploratory fixed-policy whole-cone search; every ordered history retained; not a universal proof.',seed=args.seed,elapsed=time.time()-start,cases=records)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--cases',type=int,default=10);ap.add_argument('--types',type=int,default=25);ap.add_argument('--starts',type=int,default=4);ap.add_argument('--iterations',type=int,default=3);ap.add_argument('--seed',type=int,default=20261021);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();result=run(args)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
