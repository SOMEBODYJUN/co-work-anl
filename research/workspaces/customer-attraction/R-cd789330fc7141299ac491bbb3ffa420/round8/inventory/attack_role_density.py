"""Exact attack of a pure-flow aggregate-density candidate, not SPE search.
Candidate: per-client init caps plus the customer-preserving raw kernel force
sum of densities over ALL contexts of a fixed role to be <= source inventory.
The explicit deterministic policy below refutes this structure-only claim.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

P=Path(__file__).resolve().parent
m=4
# a contains x; b is empty. Every unlisted prescribed action is b.
sigma={h:'b' for r in range(m) for h in product('ab',repeat=r)}
sigma.update({('a',):'a',('a','a'):'b',('b','a'):'a',
              ('a','a','b'):'a',('b','a','a'):'b',('b','b','a'):'a'})
def finish(h):
    while len(h)<m:h=h+(sigma[h],)
    return h
def cover(z):return {i for i,a in enumerate(z) if a=='a'}
B=finish(())
W=finish(('a',))
assert B==tuple('bbbb') and W==tuple('aaba')
# One x source unit is initially divided uniformly among its actual query
# coverers, including source role0. This obeys strengthened per-edge cap p/cW.
incoming=defaultdict(F)
for j in cover(W)-{0}:incoming[W[:j]]+=F(1,len(cover(W)))
initial_current=F(1,len(cover(W)))
source_future=sum(incoming.values(),F())
rows=[]
current=defaultdict(F)
for i in range(1,m):
    for h in sorted(z for z in list(incoming) if len(z)==i):
        mass=incoming[h]
        if not mass:continue
        V=finish(h); A=finish(B[:i]+(sigma[h],))
        old,new=cover(V),cover(A)
        assert i in old & new
        positive=new-old
        density=len(old)*mass
        assert density<=1
        keep=mass*(1-F(len(positive),len(new)))
        assert keep>0
        current[i]+=keep
        for j in positive:
            assert j>i # fresh x, so no past actual coupon
            incoming[A[:j]]+=mass/len(new)
        rows.append({'history':''.join(h),'role_zero_based':i,
            'old_leaf':''.join(V),'reset_leaf':''.join(A),
            'incoming':str(mass),'density':str(density),
            'current':str(keep),'positive_recipients':sorted(positive)})
assert initial_current+sum(current.values(),F())==1
at3=[r for r in rows if r['role_zero_based']==3]
assert len(at3)==2
aggregate=sum((F(r['density']) for r in at3),F())
assert aggregate==F(7,6)>1
assert current[3]==F(5,12)
out={'candidate':'Pure-flow sum of per-client density over all fixed-role contexts <=1',
     'status':'refuted for arbitrary deterministic policy only',
     'not_SPE':True,'why_not_SPE':'actual bbbb has zero utility; a query has positive utility',
     'actual':''.join(B),'forced_initial_leaf':''.join(W),
     'source_inventory':'1','initial_current':str(initial_current),
     'initial_future':str(source_future),'rows':rows,
     'role3_density_sum':str(aggregate),
     'role3_same_action':'a','role3_current_sum':str(current[3]),
     'role3_actual_prefix_a_query_profit':'1',
     'scope':'Refutes structure-only aggregation of density, not same-action current capacity, not any SPE theorem, not HALF.'}
(P/'role_density_counter.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
