"""Independent K5 full-history SPE / integer-demand-cover verification."""
from fractions import Fraction as F
from itertools import product,combinations,combinations_with_replacement
from pathlib import Path
import json
k=5;clients=list(map(set,combinations(range(k),2)))
def utility(a,z):
    return sum((F(1,sum(t in e for t in z)) for e in clients if a in e),F())
def choose(h):
    if not h:return 0
    if len(h)==1:return (h[0]+1)%k
    a,b=h
    if b==(a+1)%k:return (a-1)%k
    return next(j for j in range(k) if j not in h)
def end(h):
    while len(h)<3:h=h+(choose(h),)
    return h
checks=0
for d in range(3):
    for h in product(range(k),repeat=d):
        a=choose(h);z=end(h)
        for b in range(k):
            assert utility(a,z)>=utility(b,end(h+(b,)))
            checks+=1
root_payoffs=[utility(i,end((i,))) for i in range(k)]
assert set(root_payoffs)=={F(3)}
q=2
dem={tuple(sorted(e)):max(sum(j in e for j in end((i,))[1:]) for i in e) for e in clients}
active={e for e,v in dem.items() if v}
assert active=={tuple(sorted((i,(i+1)%k))) for i in range(k)}
static=[p for p in product(range(4),repeat=k) if sum(p)<=3]
minimum=min(sum(p) for p in static if all(sum(p[i] for i in e)>=v for e,v in dem.items()))
assert minimum==3
theta=min(max(utility(a,b+(a,)) for a in range(k)) for b in combinations_with_replacement(range(k),q))
assert theta==3
out={'independent_unit_check':True,'histories':sum(k**i for i in range(3)),'comparisons':checks,'theta':str(theta),'root_payoffs':list(map(str,root_payoffs)),'demand_edges':sorted(active),'minimum_integer_crowding_cover':minimum,'available_slots':q}
Path(__file__).with_name('static_crowding_review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
