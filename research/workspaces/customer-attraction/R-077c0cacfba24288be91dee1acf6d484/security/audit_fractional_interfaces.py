"""Exact finite checks supporting the written fractional-security interfaces.

The general statements are proved in free_fractional_security.md, not by
this finite audit. No optimizer, SPE solver or imported game verifier.
"""
from fractions import Fraction as Q
from itertools import product
import json

weights={2:1,5:2,6:2};k=3;m=2
def utility(a,leaf):
    return sum((Q(w,sum(bool(mask>>b&1) for b in leaf)) for mask,w in weights.items() if mask>>a&1),Q(0))
def action(h):return 0 if not h else (1 if h[0]==0 else 2)
def terminal(h):
    while len(h)<m:h=h+(action(h),)
    return h
comparisons=0
for depth in range(m):
    for h in product(range(k),repeat=depth):
        a=action(h);actual=utility(a,terminal(h))
        for b in range(k):
            assert actual>=utility(b,terminal(h+(b,)))
            comparisons+=1
assert terminal(())==(0,1)
assert [utility(a,(0,1)) for a in (0,1)]==[Q(2),Q(3)]
def g(a,q):
    return sum((Q(w)/(1+(m-1)*sum(q[b] for b in range(k) if mask>>b&1)) for mask,w in weights.items() if mask>>a&1),Q(0))
assert [g(a,(Q(0),Q(0),Q(1))) for a in range(k)]==[Q(1),Q(2),Q(2)]
for j in range(101):
    s=Q(j,100);value=g(2,(s,1-s,Q(0)))
    assert value-Q(8,3)==2*(2*s-1)**2/(3*(1+s)*(2-s))

# Test the exact rational tangent formula and the price dual cap on a
# background, for every rational simplex grid point in this finite audit.
r=3;bkg={mask:mask%3 for mask in weights};p=(Q(1,2),Q(1,3),Q(1,6));q0=(Q(1,4),Q(1,2),Q(1,4))
def alpha(mask,q):return sum(q[a] for a in range(k) if mask>>a&1)
def F(q):return sum(Q(w)*alpha(mask,p)/(bkg[mask]+1+(r-1)*alpha(mask,q)) for mask,w in weights.items())
H=[sum(Q(w)*alpha(mask,p)/(bkg[mask]+1+(r-1)*alpha(mask,q0))**2 for mask,w in weights.items() if mask>>a&1) for a in range(k)]
lower=F(q0)+(r-1)*(sum(q0[a]*H[a] for a in range(k))-max(H))
for i in range(21):
    for j in range(21-i):
        q=(Q(i,20),Q(j,20),Q(20-i-j,20))
        tangent=F(q0)-(r-1)*sum(H[a]*(q[a]-q0[a]) for a in range(k))
        assert F(q)>=tangent>=lower

q=(Q(1,5),Q(3,10),Q(1,2));den={mask:1+(r-1)*alpha(mask,q) for mask in weights}
gq=[sum(Q(w)/den[mask] for mask,w in weights.items() if mask>>a&1) for a in range(k)]
mass=sum(Q(w)*(den[mask]-1)/den[mask] for mask,w in weights.items())
assert mass==(r-1)*sum(q[a]*gq[a] for a in range(k))
assert mass<=(r-1)*max(gq)
print(json.dumps({'status':'exact finite audit passed','spe_comparisons':comparisons,'actual_payoffs':['2','3'],'restricted_cap_lower':'8/3','free_cap':'2','tangent_grid_points':231,'price_dual_identity':str(mass)}))
