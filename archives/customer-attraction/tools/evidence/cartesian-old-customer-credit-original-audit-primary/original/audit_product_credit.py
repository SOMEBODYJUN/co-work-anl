"""Independent ordered-history product check and exact obstruction arithmetic.

No canonical game model, solver or discoverer audit is imported. Small products
check implementation only. General product preservation is proved in the note.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from collections import Counter
from pathlib import Path
import json

class Game:
    def __init__(self,m,topics,customers):
        self.m=m;self.topics=topics;self.customers=customers;self.sigma={}
    def follow(self,h):
        while len(h)<self.m:h=(*h,self.sigma[h])
        return h
    def u(self,a,z):
        return sum((F(1,sum(t in c for t in z)) for c in self.customers if a in c),F(0))
    def check(self):
        slacks=[]
        for h,a in self.sigma.items():
            actual=self.u(a,self.follow(h))
            slacks.extend(actual-self.u(b,self.follow((*h,b))) for b in range(self.topics))
        assert min(slacks)>=0
        return {'ordered_nodes':len(self.sigma),'all_action_comparisons':len(slacks),'minimum_slack':str(min(slacks))}
    def F(self,h):
        r=self.m-len(h)
        def val(z):
            return sum((F(sum(a in c for a in z),sum(a in c for a in (*h,*z))) for c in self.customers if any(a in c for a in z)),F(0))
        return max(val(z) for z in combinations_with_replacement(range(self.topics),r))

def components(m):
    A=Game(m,m,[frozenset((0,))]*m+[frozenset((a,)) for a in range(1,m)])
    for depth in range(m):
        for h in product(range(m),repeat=depth):A.sigma[h]=0
    r=m-1
    B=Game(m,m,[frozenset((0,))]*2+[frozenset((1,))]*r+[frozenset((a,)) for a in range(2,m)])
    for depth in range(m-1,-1,-1):
        for h in product(range(m),repeat=depth):
            if 0 in h:chosen=1
            elif all(a==1 for a in h):chosen=0
            else:chosen=max(range(m),key=lambda a:B.u(a,B.follow((*h,a))))
            B.sigma[h]=chosen
    return A,B

def product_audit(m):
    A,B=components(m)
    checked=[A.check(),B.check()]
    choices=list(product(range(A.topics),range(B.topics)))
    lookup={v:i for i,v in enumerate(choices)}
    cs=[frozenset(i for i,v in enumerate(choices) if v[0] in c) for c in A.customers]
    cs += [frozenset(i for i,v in enumerate(choices) if v[1] in c) for c in B.customers]
    G=Game(m,len(choices),cs)
    for depth in range(m):
        for h in product(range(G.topics),repeat=depth):
            hA=tuple(choices[a][0] for a in h);hB=tuple(choices[a][1] for a in h)
            G.sigma[h]=lookup[A.sigma[hA],B.sigma[hB]]
    result=G.check();background_checks=0
    for depth in range(m):
        for h in product(range(G.topics),repeat=depth):
            hA=tuple(choices[a][0] for a in h);hB=tuple(choices[a][1] for a in h)
            assert G.F(h)==A.F(hA)+B.F(hB);background_checks+=1
    # Check tuple-to-union injectivity directly as customer-index subsets.
    sets=[frozenset(x for x,c in enumerate(cs) if a in c) for a in range(G.topics)]
    assert len(set(sets))==G.topics
    return {'m':m,'component_checks':checked,'product_checks':result,'all_prefix_F_additivity_checks':background_checks,'distinct_product_topics':len(set(sets))}

n=64;r=n-1
h=min(F(j)+F(n,j) for j in range(1,n+1));assert h==16
FA=2*n-h;PA=F(r);FB=F(2*r-1);PB=F(r)
FC=2*(n-1)*(n-2)+F(7*n-13,6);OC=2*n*n-2*n-2;delta=OC-FC;u=F(n)-F(1,n)
lo=63*(FA-2*PA)+2016*(FB-2*PB);hi=64*(2*u-delta)
LH=Counter({(1,r):63*n,(1,0):2016*2});UH=Counter({(1,r):64*r,(1,0):64*r})
assert LH==UH and lo==-2898 and hi==-3170 and lo-hi==272
# If b=0 clients were visible, the products would be distinguished.
low_b0={0:63*(n-1)+2016*(r-1),r:2016*r}
upper_b0={0:64*n*(n-2),r:64*n*(n-2)}
assert low_b0!=upper_b0
report={'scope':'Finite implementation checks plus exact arithmetic for the general analytical product proof; no universal half claim.','product_regressions':[product_audit(m) for m in (2,3)],'obstruction':{'remaining_players':r,'same_background_histogram':{str(k):v for k,v in LH.items()},'LOW_tail_P':str(63*PA+2016*PB),'LOW_tail_F':str(63*FA+2016*FB),'LOW_forced_G_lower':str(lo),'UPPER_root_u':str(64*u),'UPPER_root_delta':str(64*delta),'UPPER_forced_G_upper':str(hi),'strict_gap':str(lo-hi),'LOW_b_zero_histogram':low_b0,'UPPER_b_zero_histogram':upper_b0},'all_exact_checks_passed':True}
out=Path(__file__).with_name('product_credit_independent_audit.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
