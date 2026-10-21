"""Definition-level Fraction checks for TG-SEC-v1; no solver/LP imports."""
from fractions import Fraction as F
from itertools import combinations,product
from functools import lru_cache
from math import comb
import json,random

def policy(h,k):
    if not h:return 0
    group=(1-h[0]//k) if len(h)==1 else h[1]//k
    return next(a for a in range(group*k,(group+1)*k) if a not in h)

def check(m,k,weight,expect_spe):
    clients={mask:weight[(min((mask&((1<<k)-1)).bit_count(),(mask>>k).bit_count()),max((mask&((1<<k)-1)).bit_count(),(mask>>k).bit_count()))] for mask in range(1,1<<(2*k))}
    @lru_cache(None)
    def payoff(z,a):
        return sum((F(w,sum(bool(mask>>b&1) for b in z)) for mask,w in clients.items() if w and mask>>a&1),F(0))
    @lru_cache(None)
    def end(h):return h if len(h)==m else end(h+(policy(h,k),))
    root=end(());a=payoff(root,root[0]);b=payoff(root,root[1]);pure=tuple(range(k,k+m));t=payoff(pure,pure[-1]);bg=pure[:-1];r=payoff(bg+(bg[0],),bg[0]);W=sum(payoff(root,x) for x in root)
    assert all(payoff(root,x)==b for x in root[1:])
    assert t>=r
    beta=(a+t)/2-F(m-1,2*k)*(t-r)
    backgrounds=[z for g in (0,1) for z in combinations(range(g*k,(g+1)*k),m-1)]
    query=[sum((payoff(z+(q,),q) for z in backgrounds),F(0))/len(backgrounds) for q in range(2*k)]
    assert set(query)=={beta}
    assert W-m*beta==(m-1)*(b-t)+F(m-2,2)*(t-a)+F(m*(m-1),2*k)*(t-r)
    comparisons=0;failures=0
    for d in range(m):
        for h in product(range(2*k),repeat=d):
            u=payoff(end(h),policy(h,k))
            for q in range(2*k):
                comparisons+=1
                if u<payoff(end(h+(q,)),q):failures+=1
    if expect_spe:
        assert failures==0,(m,k,failures)
        assert b>=t>=a
        assert W>=m*beta
    return dict(m=m,k=k,customer_count=sum(clients.values()),comparisons=comparisons,failures=failures,expected_spe=expect_spe,a=str(a),b=str(b),t=str(t),r=str(r),W=str(W),beta=str(beta),margin=str(W-m*beta))

def allweights(k,f):return {(i,j):f(i,j) for i in range(k+1) for j in range(i,k+1) if i+j}

if __name__=='__main__':
    out=[]
    for m,k in [(3,3),(3,4),(4,4)]:
        out.append(check(m,k,allweights(k,lambda i,j:0),True))
        out.append(check(m,k,allweights(k,lambda i,j:1),True))
    out.append(check(3,3,allweights(3,lambda i,j:int((i,j)==(1,1))+3*int((i,j)==(2,2))),True))
    # Random nonnegative symmetric games need not make this fixed policy SPE;
    # only the typewise fresh inequality and the algebra/Q identities apply.
    rng=random.Random(20261021)
    for m,k in [(3,3),(3,4),(4,4)]:
        out.append(check(m,k,allweights(k,lambda i,j:rng.randrange(4)),False))
    print(json.dumps(dict(status='PASS',scope='Finite definition-level checks; general restricted-cone proof is in the note.',results=out),indent=2))
