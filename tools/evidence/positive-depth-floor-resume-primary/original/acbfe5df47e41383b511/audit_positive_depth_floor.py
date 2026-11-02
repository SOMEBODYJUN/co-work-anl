"""Independent definition-level Fraction audit of the positive-depth floor NO.

Imports no canonical model, SPE solver, certificate code, optimizer, or generator.
The saved policy is verified at every ordered history and every legal action.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
game=json.loads((HERE/'positive_depth_floor_game.json').read_text())
certificate=json.loads((HERE/'positive_depth_floor_certificate.json').read_text())
n,k=game['players'],len(game['topics'])
assert (n,k)==(4,7)
types=[(frozenset(x['topics']),x['multiplicity']) for x in game['customers']]
assert all(t and type(w) is int and w>0 for t,w in types)
assert sum(w for t,w in types)==53
policy={tuple(x['history']):x['action'] for x in certificate['strategy']['actions']}
histories=tuple(h for d in range(n) for h in product(range(k),repeat=d))
assert len(policy)==len(certificate['strategy']['actions'])==400
assert set(policy)==set(histories)
assert all(type(a) is int and 0<=a<k for a in policy.values())

@lru_cache(None)
def leaf(h):return h if len(h)==n else leaf(h+(policy[h],))

@lru_cache(None)
def counts(h):return tuple(h.count(a) for a in range(k))

@lru_cache(None)
def query(a,B):
    return sum((F(w,1+sum(B[b] for b in t)) for t,w in types if a in t),F())

def utility(i,z):return query(z[i],counts(z[:i]+z[i+1:]))
def welfare(z):return sum(w for t,w in types if any(a in t for a in z))

strict=tied=0
for h in histories:
    i=len(h);actual=utility(i,leaf(h))
    for a in range(k):
        slack=actual-utility(i,leaf(h+(a,)))
        assert slack>=0,(h,a,slack)
        if a!=policy[h]:
            strict+=slack>0
            tied+=slack==0

z=leaf(())
u=tuple(utility(i,z) for i in range(n))
assert z==(6,0,3,4)
assert u==(F(19),F(29,3),F(67,6),F(67,6))
W=welfare(z)
OPT=max(welfare(t) for t in combinations_with_replacement(range(k),n))
assert sum(u)==W==51 and OPT==53
assert certificate['strategy']['terminal_counts']==list(counts(z))

security=certificate['security']
p=tuple(map(F,security['primary']))
Q=tuple((tuple(row['rivals']),F(row['probability'])) for row in security['dual'])
assert len(p)==k and min(p)>=0 and sum(p)==1
assert all(len(B)==n-1 and min(B)>=0 and max(B)<k and q>0 for B,q in Q)
assert sum(q for B,q in Q)==1
# All 343 ordered competitor tuples, independent of the query realization.
minimum=min(sum((p[a]*query(a,counts(B)) for a in range(k)),F())
            for B in product(range(k),repeat=n-1))
dual_queries=tuple(sum((q*query(a,counts(B)) for B,q in Q),F()) for a in range(k))
v=F(security['value'])
assert minimum==max(dual_queries)==v==F(28481,2924)
assert len(set(dual_queries))==1
deficit=v-u[1]
assert deficit==F(647,8772)>0
assert W-n*v==F(8800,731)>0
assert 2*W-OPT==49>0
result={'status':'PASS','scope':'positive-depth security floor NO only',
        'players':n,'topics':k,'unit_customers':53,
        'ordered_histories':len(histories),'all_action_comparisons':len(histories)*k,
        'strict_nonself_comparisons':strict,'tied_nonself_comparisons':tied,
        'ordered_static_backgrounds':k**(n-1),'root':z,'utilities':list(map(str,u)),
        'W':W,'OPT':OPT,'security_value':str(v),'position_2_security_deficit':str(deficit),
        'strong_aggregate_margin':str(W-n*v),'half_margin':2*W-OPT}
print(json.dumps(result,indent=2))
(HERE/'positive_depth_floor_audit.json').write_text(json.dumps(result,indent=2)+'\n')
