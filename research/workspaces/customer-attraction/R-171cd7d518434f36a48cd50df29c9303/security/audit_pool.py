"""Definition-level Fraction audit of the old 36-client SPE and pooled loads."""
from fractions import Fraction as F
from itertools import combinations,product
import json
from pathlib import Path

def choose(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    group=range(3) if h[1]<3 else range(3,6)
    return min(a for a in group if a not in h)

def finish(h):
    while len(h)<3:h=h+(choose(h),)
    return h

def main():
    customers=[]
    for x,y in product(range(3),range(3,6)):customers.append(frozenset([x,y]))
    for xx,yy in product(combinations(range(3),2),combinations(range(3,6),2)):
        customers.extend([frozenset(xx+yy)]*3)
    def payoff(a,z):return sum((F(1,sum(b in T for b in z)) for T in customers if a in T),F(0))
    comparisons=0
    for t in range(3):
        for h in product(range(6),repeat=t):
            z=finish(h);u=payoff(choose(h),z)
            for a in range(6):
                assert u>=payoff(a,finish(h+(a,)))
                comparisons+=1
    z=finish(());W=len([T for T in customers if any(a in T for a in z)])
    p={2:F(1,2),5:F(1,2)}
    backgrounds=[]
    for i in range(3):
        for b,pb in p.items():
            leaf=finish(z[:i]+(b,));B=leaf[:i]+leaf[i+1:]
            backgrounds.append((pb/3,B))
    loadmean=[sum((prob*sum(b in T for b in B) for prob,B in backgrounds),F(0)) for T in customers]
    t=[sum((pa for a,pa in p.items() if a in T),F(0)) for T in customers]
    pooled=sum((tx/(1+H) for tx,H in zip(t,loadmean)),F(0))
    unpooled=sum((prob*sum((tx/F(1+sum(b in T for b in B)) for tx,T in zip(t,customers)),F(0)) for prob,B in backgrounds),F(0))
    J=sum((tx*sum((prob*(F(sum(b in T for b in B))-H)**2/(F(1)+H)**2/F(1+sum(b in T for b in B)) for prob,B in backgrounds),F(0)) for tx,T,H in zip(t,customers,loadmean)),F(0))
    assert unpooled-pooled==J
    assert 3*unpooled>W
    assert 3*pooled<W
    report=dict(customers=len(customers),nodes=43,comparisons=comparisons,path=z,W=W,p={str(a):str(pa) for a,pa in p.items()},unpooled_total=str(3*unpooled),pooled_total=str(3*pooled),jensen_credit_total=str(3*J),old_balance=str(W-3*unpooled),pooled_balance=str(W-3*pooled))
    print(json.dumps(report,indent=2))
    out=Path(__file__).with_name('pool_audit.json');out.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
