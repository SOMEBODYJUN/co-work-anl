"""Specific analytical candidate attack: append a disjoint theme P to the
known 71-customer graph so O can absorb the actual penultimate theme.
The complete finite tree is constructed only to test that exact counterexample.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations_with_replacement
from pathlib import Path
import json

rows=[(1,21),(2,18),(4,26),(8,16),(17,2),(18,8),(24,10),
      (33,2),(34,8),(40,10),(49,10),(52,10),(54,2),(58,2)]
P_SIZE=34
rows.append((64,P_SIZE))
k=7;m=3
@lru_cache(None)
def pay(z):
    return tuple(sum((F(w,sum(bool(q>>a&1) for a in z)) for q,w in rows if q>>b&1),F(0)) for b in z)
@lru_cache(None)
def leaves(h):
    if len(h)==m:return frozenset([h])
    i=len(h)
    children=[leaves(h+(a,)) for a in range(k)]
    threshold=max(min(pay(z)[i] for z in child) for child in children)
    return frozenset(z for child in children for z in child if pay(z)[i]>=threshold)

def build(h,z,ad):
    if len(h)==m:return
    i=len(h);ad[h]=z[i]
    for a in range(k):
        child=h+(a,)
        chosen=z if a==z[i] else min(leaves(child),key=lambda y:(pay(y)[i],y))
        assert pay(z)[i]>=pay(chosen)[i]
        build(child,chosen,ad)

base=(6,0,1)
print('desired leaf available after P',base in leaves((6,)))
print('root child min profits',[(a,str(min(pay(z)[0] for z in leaves((a,))))) for a in range(k)])
print('desired complete SPE available',base in leaves(()))
if base in leaves(()):
    actions={};build((),base,actions)
    def finish(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    for h,a in actions.items():
        assert all(pay(finish(h))[len(h)]>=pay(finish(h+(b,)))[len(h)] for b in range(k))
    cover=lambda z:sum(w for q,w in rows if any(q>>a&1 for a in z))
    opts=list(combinations_with_replacement(range(k),m));op=max(map(cover,opts))
    optimal=[z for z in opts if cover(z)==op]
    result={'rows':rows,'path':base,'profits':list(map(str,pay(base))),
            'welfare':cover(base),'optimal':op,'optimal_tuples':optimal,
            'actions':[{'history':h,'action':a} for h,a in sorted(actions.items(),key=lambda v:(len(v[0]),v[0]))]}
    Path(__file__).with_name('prefixed_refund_counterexample.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({key:value for key,value in result.items() if key!='actions'},indent=2))
