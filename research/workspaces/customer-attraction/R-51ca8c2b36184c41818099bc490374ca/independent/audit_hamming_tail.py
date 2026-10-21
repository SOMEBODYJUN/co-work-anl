"""Independent exact checker of the Hamming/tail local-row obstruction.

No imports from the proposed construction or its proof.  Themes are disjoint;
integer theme sizes encode that many separate unit customers.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm
import json

class Game:
    def __init__(self,m,k,r):
        assert m>k>=1
        self.m=m;self.k=k;self.n=m-k;self.r=r;self.d=self.n-r
        assert 0<=r<self.n
        self.L=lcm(*range(1,self.d+1))
        # A themes are 0,...,n-1, B themes n,...,n+m-1.
        self.K=self.n+m
        self.sizes=tuple(self.L//max(self.d-i,1) for i in range(self.n))+(self.L,)*m
    def move(self,h):
        t=len(h)
        if t>=self.n:return next(a for a in range(self.n,self.K) if a not in h)
        wrong=[j for j,a in enumerate(h) if a!=j]
        if not wrong:return t
        if len(wrong)<=self.r:return next(a for a in range(self.n,self.K) if a not in h)
        return h[wrong[0]]
    def finish(self,h):
        h=tuple(h)
        while len(h)<self.m:h=h+(self.move(h),)
        return h
    def utility(self,h,a):
        z=self.finish(h+(a,))
        return F(self.sizes[a],z.count(a))
    def margins(self,h):
        chosen=self.move(h);u=self.utility(h,chosen)
        return tuple(u-self.utility(h,a) for a in range(self.K))
    def root(self):
        z=self.finish(())
        W=sum(self.sizes[a] for a in set(z))
        expected=self.L*(sum((F(1,j) for j in range(1,self.d+1)),F(0))+self.r+self.k)
        assert W==expected
        assert max(self.sizes)==self.L
        # m disjoint B themes attain the upper bound m*max theme size.
        OPT=self.m*self.L
        return dict(path=z,W=W,OPT=OPT,ratio=str(F(OPT,W)))

def audit(m,k,r):
    g=Game(m,k,r);near=tail=0;future_near=0;lowest=F(0)
    for t in range(m):
        for h in product(range(g.K),repeat=t):
            s=sum(a!=j for j,a in enumerate(h)) if t<g.n else None
            if t>=g.n:tail+=g.K
            elif s<=r:
                near+=g.K
                future_near+=int(any(a<g.n and a>j for j,a in enumerate(h)))
            else:continue
            margins=g.margins(h)
            assert min(margins)>=0,(m,k,r,h,margins)
            lowest=min(lowest,min(margins))
    out=dict(m=m,k=k,r=r,d=g.d,L=g.L,near_comparisons=near,
             tail_comparisons=tail,near_histories_with_future_A=future_near,
             minimum_margin=str(lowest),root=g.root())
    if g.d>=2:
        h=tuple(range(g.n,g.n+r+1))
        chosen=g.move(h);fresh=g.n+r+1
        actual=g.utility(h,chosen);deviation=g.utility(h,fresh)
        assert actual==F(g.L,g.d) and deviation==g.L
        out['far_violation']=dict(history=h,chosen=chosen,deviation=fresh,
             actual=str(actual),deviation_utility=str(deviation),margin=str(actual-deviation))
    return out

def main():
    reports=[audit(m,k,r) for m in range(2,6) for k in range(1,m) for r in range(m-k)]
    print(json.dumps(dict(status='PASS',instances=len(reports),reports=reports),indent=2))
if __name__=='__main__':main()
