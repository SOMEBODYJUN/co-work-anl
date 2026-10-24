"""Exact candidate diagnosis using one named, already existing full SPE.

No games or policies are generated.  Optimal tuples and first-owner assignments
are tried only until an exact NET witness is obtained.  Fixed-choice failures
are not failures of the free-owner general candidate.  Floating LP proposes;
Fraction primal+dual identities certify every reported optimum.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]


def frac(value):
    return F(float(value)).limit_denominator(10**8)


def exact_lp(c,Aeq,beq,Aub,bub,upper):
    n=len(c)
    eq=np.array(Aeq,dtype=float).reshape((-1,n))
    ub=np.array(Aub,dtype=float).reshape((-1,n))
    res=linprog(np.array(c,dtype=float),A_eq=eq if len(Aeq) else None,
                b_eq=np.array(beq,dtype=float) if len(Aeq) else None,
                A_ub=ub if len(Aub) else None,
                b_ub=np.array(bub,dtype=float) if len(Aub) else None,
                bounds=[(0,v) if v is not None else (None,None) for v in upper],method='highs')
    assert res.success,res.message
    x=list(map(frac,res.x))
    for row,b in zip(Aeq,beq):assert sum((a*v for a,v in zip(row,x)),F())==b
    for row,b in zip(Aub,bub):assert sum((a*v for a,v in zip(row,x)),F())<=b
    for v,cap in zip(x,upper):
        if cap is not None:assert 0<=v<=cap
    yi=list(map(frac,res.ineqlin.marginals)) if Aub else []
    ye=list(map(frac,res.eqlin.marginals)) if Aeq else []
    yl=list(map(frac,res.lower.marginals));yu=list(map(frac,res.upper.marginals))
    assert all(y<=0 for y in yi)
    assert all(y>=0 for y in yl) and all(y<=0 for y in yu)
    for j in range(n):
        assert c[j]==sum((row[j]*y for row,y in zip(Aub,yi)),F())+sum((row[j]*y for row,y in zip(Aeq,ye)),F())+yl[j]+yu[j]
        if upper[j] is None:assert yl[j]==yu[j]==0
    primal=sum((a*v for a,v in zip(c,x)),F())
    dual=sum((b*y for b,y in zip(bub,yi)),F())+sum((b*y for b,y in zip(beq,ye)),F())+sum((cap*y for cap,y in zip(upper,yu) if cap is not None),F())
    assert primal==dual
    return x,primal,dict(inequality=list(map(str,yi)),equality=list(map(str,ye)),
                         lower=list(map(str,yl)),upper=list(map(str,yu)))


def diagnose(name):
    raw=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    cert=cert.get('strategy',cert)
    policy={tuple(r['history']):r['action'] for r in cert['actions']}
    X=[frozenset(r['topics']) for r in raw['customers'] for _ in range(r['multiplicity'])]
    m=raw['players'];k=len(raw['topics']);N=len(X)
    expected={h for d in range(m) for h in product(range(k),repeat=d)}
    assert set(policy)==expected
    @lru_cache(None)
    def finish(h):
        return h if len(h)==m else finish(h+(policy[h],))
    def pay(z,i):
        return sum((F(1,sum(a in likes for a in z)) for likes in X if z[i] in likes),F())
    checks=0
    for h in policy:
        z=finish(h);i=len(h)
        for a in range(k):
            assert pay(z,i)>=pay(finish(h+(a,)),i)
            checks+=1
    actual=finish(())
    u=[pay(actual,i) for i in range(m)]
    C={x for x in range(N) if any(a in X[x] for a in actual)}
    def coverage(T):return frozenset(x for x in range(N) if any(a in X[x] for a in T))
    values=[(coverage(T),T) for T in combinations_with_replacement(range(k),m)]
    opt=max(len(O) for O,T in values)
    optimal=[T for O,T in values if len(O)==opt]
    @lru_cache(None)
    def price(x,i,a):
        assert a in X[x] and all(actual[j] not in X[x] for j in range(i))
        z=finish(actual[:i]+(a,))
        future=[j for j in range(i+1,m) if z[j] in X[x]]
        c=1+len(future);D=pay(z,i)
        assert D>0 and u[i]>=D
        row=[F() for _ in range(m)]
        row[i]=u[i]/(c*D)
        for j in future:
            child=price(x,j,z[j])
            row=[v+w/c for v,w in zip(row,child)]
        assert sum(row,F())>=1
        return tuple(row)
    trials=[]
    for multiset in optimal:
        for T in sorted(set(permutations(multiset))):
            O=coverage(T);R=sorted(O-C);I=sorted(O&C);G=C-O
            owner={x:next(i for i,a in enumerate(T) if a in X[x]) for x in O}
            prices=[price(x,owner[x],T[owner[x]]) for x in R]
            v=[sum(row,F()) for row in prices]
            Iprofit=[sum((F(1,sum(a in X[x] for a in actual)) for x in I if actual[i] in X[x]),F()) for i in range(m)]
            g=[u[i]-Iprofit[i] for i in range(m)]
            cap=defaultdict(F)
            for x in I:
                covers=[i for i,a in enumerate(actual) if a in X[x]]
                for i in covers:
                    if i!=owner[x]:cap[owner[x],i]+=F(1,len(covers))
            edges=sorted(cap)
            d=len(R);base_n=d+len(edges)
            Aeq=[]
            for i in range(m):
                row=[F(int(owner[x]==i)) for x in R]
                row += [F(int(a==i)-int(b==i)) for a,b in edges]
                Aeq.append(row)
            beq=g
            upper=[F(1)]*d+[cap[e] for e in edges]
            # Total-price optimization, independently certified against greedy rank.
            if base_n:
                tx,tobj,tdual=exact_lp([-z for z in v]+[F()]*len(edges),Aeq,beq,[],[],upper)
            else:
                assert sum(g,F())==0
                tx=[];tobj=F();tdual={}
            min_total=sum(v,F())+tobj
            def rank(S):
                return min(sum((g[i] for i in range(m) if not ((mask>>i)&1)),F())
                           +sum((c for (a,b),c in cap.items() if ((mask>>a)&1) and not ((mask>>b)&1)),F())
                           +sum(x in S and ((mask>>owner[x])&1) for x in R)
                           for mask in range(1<<m))
            assert rank(set())==0 and rank(set(R))==len(G)
            order=sorted(range(d),key=lambda j:(-v[j],R[j]))
            prefix=set();last=F();greedy=[F()]*d;layers=[]
            for j in order:
                prefix.add(R[j]);r=rank(prefix)
                greedy[j]=r-last;assert 0<=greedy[j]<=1
                layers.append(dict(client=R[j],price=str(v[j]),rank=str(r),deficit=str(len(prefix)-r)))
                last=r
            assert sum(greedy,F())==len(G)
            for mask in range(1<<m):
                out=sum((c for (a,b),c in cap.items() if ((mask>>a)&1) and not ((mask>>b)&1)),F())
                outside_source=sum((g[i] for i in range(m) if not ((mask>>i)&1)),F())
                stock=sum((greedy[j] for j,x in enumerate(R) if (mask>>owner[x])&1),F())
                assert outside_source+out+stock>=len(G)
            assert sum((v[j]*(1-greedy[j]) for j in range(d)),F())==min_total
            # NET minimizes one shared maximum row violation.
            nc=base_n+1
            neq=[row+[F()] for row in Aeq]
            nub=[];nb=[]
            for i in range(m):
                nub.append([-prices[j][i]-F(int(owner[x]==i)) for j,x in enumerate(R)]+[F()]*len(edges)+[F(-1)])
                nb.append(Iprofit[i]-sum((prices[j][i] for j in range(d)),F()))
            nx,nobj,ndual=exact_lp([F()]*base_n+[F(1)],neq,beq,nub,nb,upper+[None])
            gamma=nx[:d]
            K=[sum((prices[j][i]*(1-gamma[j]) for j in range(d)),F()) for i in range(m)]
            eta=[Iprofit[i]+sum((gamma[j] for j,x in enumerate(R) if owner[x]==i),F()) for i in range(m)]
            assert sum(eta,F())==len(C)
            assert max((a-b for a,b in zip(K,eta)),default=F())==nobj
            trial=dict(optimal_tuple=list(T),owner_rule='first optimal slot containing each unit customer',
                       R=len(R),I=len(I),G=len(G),net_margin=str(nobj),minimum_total_price=str(min_total),
                       W=len(C),K=list(map(str,K)),eta=list(map(str,eta)),gamma_clients=R,
                       gamma=list(map(str,gamma)),I_edges=[dict(tail=a,head=b,capacity=str(cap[a,b]),flow=str(nx[d+j])) for j,(a,b) in enumerate(edges)],
                       net_dual=ndual,total_dual=tdual,rank_price_layers=layers)
            trials.append(trial)
            if nobj<=0:
                return dict(case=name,status='one exact integral-owner NET witness; no general conclusion',
                            players=m,topics=k,customers=N,actual=list(actual),payoffs=list(map(str,u)),
                            original_IC_checks=checks,OPT=opt,optimal_multisets=len(optimal),trials=trials)
    return dict(case=name,status='first-owner choices exhausted; unrestricted owners not diagnosed',
                players=m,topics=k,customers=N,actual=list(actual),payoffs=list(map(str,u)),
                original_IC_checks=checks,OPT=opt,optimal_multisets=len(optimal),trials=trials)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('case')
    args=ap.parse_args()
    out=diagnose(args.case)
    dest=HERE/f'net_diagnostic_{args.case}.json'
    with dest.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k!='trials'},indent=2))
    print(json.dumps({k:out['trials'][-1][k] for k in ('optimal_tuple','net_margin','minimum_total_price','K','eta')},indent=2))
