"""Fixed-policy attack on aggregated true-menu cap in symmetric potential games.

This is a deliberately broader game class than customer attraction:
u(a,B)=F(B+a)-G(B), where F,G are arbitrary anonymous tables.
All policies and menus retain ordered histories. Numerical LP is discovery only.
"""
import argparse
import itertools
import json
import random

import numpy as np
from scipy.optimize import linprog


def counts(h, p):
    return tuple(h.count(a) for a in range(p))


def multisets(r, p):
    return sorted({counts(h, p) for h in itertools.product(range(p), repeat=r)})


def solve(m, p, policy, query, nonnegative=False, individual=False):
    fs, gs = multisets(m, p), multisets(m-1, p)
    fi = {x:i for i,x in enumerate(fs)}
    gi = {x:len(fs)+i for i,x in enumerate(gs)}
    base = len(fs)+len(gs)
    n = base+(m if individual else 1)
    def outcome(h):
        h = tuple(h)
        while len(h)<m:
            h += (policy[h],)
        return h
    def payoff(a, h):
        z = np.zeros(n)
        z[fi[counts(h,p)]] = 1
        others = list(h)
        others.remove(a)
        z[gi[counts(others,p)]] = -1
        return z
    rows=[]
    for h, a0 in policy.items():
        actual=outcome(h)
        for a in range(p):
            branch=outcome(h+(a,))
            rows.append(payoff(a,branch)-payoff(a0,actual))
    actual=outcome(())
    w=sum((payoff(a,actual) for a in actual),start=np.zeros(n))
    menus=set(); menu_rows=[]
    for i in range(m):
        for a in range(p):
            branch=outcome(actual[:i]+(a,))
            b=counts(branch[:i]+branch[i+1:],p)
            menus.add(b)
            if individual:menu_rows.append((i,b))
    if not individual:menu_rows=[(0,b) for b in menus]
    for i,b in menu_rows:
        z=np.zeros(n)
        z[gi[b]]=1
        pi=query[i] if individual else query
        for a in range(p):
            b1=list(b);b1[a]+=1
            z[fi[tuple(b1)]]-=pi[a]
        z[base+i]=1
        rows.append(z)
    rhs=np.zeros(len(rows))
    if not individual:rhs[-len(menu_rows):]=-1/m
    if nonnegative:
        for h in itertools.product(range(p),repeat=m):
            for a in set(h):
                rows.append(-payoff(a,h))
        rhs=np.concatenate((rhs,np.zeros(len(rows)-len(rhs))))
    obj=np.zeros(n);obj[base:]=-1
    res=linprog(obj,A_ub=rows,b_ub=rhs,A_eq=[w],b_eq=[1],
                bounds=[(None,None)]*n,method='highs')
    return res,fs,gs,actual,menus


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--players',type=int,default=3)
    ap.add_argument('--topics',type=int,default=3)
    ap.add_argument('--samples',type=int,default=1000)
    ap.add_argument('--seed',type=int,default=317)
    ap.add_argument('--nonnegative',action='store_true')
    ap.add_argument('--exhaustive',action='store_true')
    ap.add_argument('--individual',action='store_true')
    ap.add_argument('--output')
    args=ap.parse_args();m,p=args.players,args.topics
    rng=random.Random(args.seed)
    histories=[h for k in range(m) for h in itertools.product(range(p),repeat=k)]
    if args.exhaustive:
        policies=itertools.product(range(p),repeat=len(histories))
    else:
        policies=(tuple(rng.randrange(p) for h in histories) for _ in range(args.samples))
    best=-float('inf');record=None
    for k,acts in enumerate(policies):
        policy=dict(zip(histories,acts))
        raw=[rng.expovariate(1) for _ in range(p)]
        queries=[[1/p]*p,[v/sum(raw) for v in raw]]
        if args.individual:
            queries=[[[1/p]*p for _ in range(m)]]
            pi=[]
            for i in range(m):
                raw=[rng.expovariate(1) for _ in range(p)]
                pi.append([v/sum(raw) for v in raw])
            queries.append(pi)
        for query in queries:
            res,fs,gs,actual,menus=solve(m,p,policy,query,args.nonnegative,args.individual)
            value=float('inf') if res.status==3 else (-res.fun-(1 if args.individual else 0) if res.success else -float('inf'))
            if value>best:
                best=value
                record=dict(players=m,topics=p,policy=[(list(h),a) for h,a in policy.items()],
                            query=query,status=res.status,message=res.message,
                            F=None if res.x is None else dict(zip(map(str,fs),res.x[:len(fs)])),
                            G=None if res.x is None else dict(zip(map(str,gs),res.x[len(fs):len(fs)+len(gs)])),
                            delta=best,actual=actual,menus=sorted(menus))
            if best>1e-7:
                print(json.dumps(record,allow_nan=True),flush=True)
                if args.output:
                    with open(args.output,'x') as f:json.dump(record,f,indent=2)
                return
        if (k+1)%100==0: print(json.dumps(dict(checked=k+1,best=best)),flush=True)
    print(json.dumps(dict(checked=k+1,best=best,nonnegative=args.nonnegative)),flush=True)

if __name__=='__main__':main()
