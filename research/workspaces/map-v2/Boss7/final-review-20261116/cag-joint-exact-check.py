from fractions import Fraction as F
from itertools import combinations
from math import comb
import json
from pathlib import Path

# Finite independent audit of fixed-root q-slot objectives. This does not
# enumerate SPE and does not discharge the all-instance SUMmin premise.
def counts(total, slots):
    if slots == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in counts(total-first,slots-1):
                yield (first,)+tail

def profit(c,q,a,b):
    result=F(0)
    for i,j in combinations(range(2*q),2):
        d=c[i]+c[j]
        if not d:
            continue
        mu=a if (i<q)==(j<q) else b
        result+=mu*F(d,d+int(i==0 or j==0))
    return result

def expected_supports(q,a,b):
    if a==0:
        return {tuple(range(q)),tuple(range(q,2*q))}
    if a<b:
        return {tuple(range(q,2*q))}
    return set(combinations(range(1,2*q),q))

rows=[]
for q in range(2,7):
    compositions=list(counts(q,2*q))
    for a,b in [(0,1),(1,1),(1,2)]:
        best=None
        maximizers=[]
        for c in compositions:
            val=profit(c,q,a,b)
            if best is None or val>best:
                best,maximizers=val,[c]
            elif val==best:
                maximizers.append(c)
        formula=q*((q-F(1,2))*b+F(q-1,2)*a)
        supports={tuple(i for i,k in enumerate(c) if k) for c in maximizers}
        assert best==formula
        assert all(max(c)==1 for c in maximizers)
        assert supports==expected_supports(q,a,b)
        rows.append(dict(q=q,a=a,b=b,multisets=len(compositions),
                         maximum=str(best),formula=str(formula),
                         maximizing_multisets=len(maximizers),
                         equality_supports_match=True))

q,a,b=5,1,2
L=F(q*b,2)+(q-1)*a
H=(q-F(1,2))*b+F(q-1,2)*a
W=q*q*b+F((q-1)*(q+2),2)*a
N=q*q*b+q*(q-1)*a
assert (L,H,q*H,L-H,W,N)==(9,11,55,-2,64,70)
# Both themes are disjoint singletons, m=1. Every action is a complete SPE.
# Uniform p gives min_A E K=3/4, but E min_A K=1/2.
exchange=dict(m=1,clients=2,topics=2,W=1,
              min_expected=str(F(3,4)),expected_min=str(F(1,2)),
              strict_gap=str(F(1,4)),summin_holds=True,
              is_half_counterexample=False)
result=dict(description='Independent exact finite objective audit; not a universal proof or a new SPE search.',
            degree_two=rows,
            six_player_example=dict(q=5,a=1,b=2,L=str(L),H=str(H),V=str(q*H),
                                     stationary_gap=str(L-H),W=str(W),OPT=str(W),N=str(N)),
            min_expectation_exchange=exchange)
out=Path(__file__).with_name('cag-joint-exact-check.json')
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(checks=len(rows),distinct_multisets=sum(comb(3*q-1,2*q-1) for q in range(2,7)),
                     parameter_multiset_pairs=sum(r['multisets'] for r in rows),
                     output=str(out),all_passed=True),ensure_ascii=False))
