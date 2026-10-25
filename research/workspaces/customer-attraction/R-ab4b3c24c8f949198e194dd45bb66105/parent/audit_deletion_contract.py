#!/usr/bin/env python3
"""Independent finite audit of the deletion induction contract; no general proof claim."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import json

def union(ts):
    result=0
    for t in ts: result |= t
    return result

def opt(cat,m):
    return max(union(ts).bit_count() for ts in combinations_with_replacement(cat,m)) if m else 0

def run():
    counts={"catalogues":0,"optimal_tuples":0,"anchor_checks":0,"slack_checks":0}
    for n in range(4):
        all_topics=range(1<<n)
        for bitcat in range(1,1<<len(all_topics)):
            cat=tuple(t for t in all_topics if bitcat>>t&1)
            counts["catalogues"]+=1
            for m in range(2,6):
                old=opt(cat,m-1)
                O=opt(cat,m)
                assert F(old)>=F(m-1,m)*O
                for ts in combinations_with_replacement(cat,m):
                    if union(ts).bit_count()!=O: continue
                    counts["optimal_tuples"]+=1
                    cu=union(ts)
                    ex=[(t & ~union(ts[:j]+ts[j+1:])).bit_count() for j,t in enumerate(ts)]
                    assert old>=O-min(ex)
                    for a in cat:
                        ns={j:0 for j in range(1,m+1)}
                        for x in range(n):
                            if cu>>x&1 and not a>>x&1:
                                ns[sum(t>>x&1 for t in ts)]+=1
                        gain=(a&~cu).bit_count()
                        cost=F(2*ns[1],m)+F(2*ns.get(2,0),m*(m-1))
                        exact=[]
                        for j,k in combinations(range(m),2):
                            swapped=tuple(t for z,t in enumerate(ts) if z not in (j,k))+(a,)
                            exact.append(union(swapped).bit_count())
                        expected=sum(map(F,exact))/len(exact)
                        assert expected==O+gain-cost
                        assert old>=expected
                        assert F(O-old)<=cost-gain
                        counts["anchor_checks"]+=1
    # Independently solve the account for rational signed drifts, then reverse it.
    for W,e,d,Om,delta in product(range(4),range(4),range(-3,4),range(4),range(4)):
        eta=F(W-e+d)
        O=Om+delta
        assert F(2*W-O)==2*eta-Om+2*e-2*d-delta
        for alpha in [F(0),F(1),F(1499,750),F(2),F(3)]:
            if F(Om)<=alpha*eta:
                assert F(O-2*W)<=delta-alpha*e+alpha*d-(2-alpha)*W
            counts["slack_checks"]+=1
    alpha=F(1499,750)
    pressure={"m":5,"alpha":str(alpha),"credit_coefficient":str(2-alpha),
              "known_upward_family_RHS":str(alpha-(2-alpha)*10)}
    assert pressure["credit_coefficient"]=="1/750"
    assert pressure["known_upward_family_RHS"]=="1489/750"
    return {"scope":"finite independent definition-level audit, not a proof of Q-CAG-HALF",
            "all_checks_passed":True,"counts":counts,"m5_pressure":pressure,
            "boundaries":["n=0", "empty topic", "nonempty catalogue", "repeated topics", "m=2", "signed drift"]}
if __name__=="__main__":
    out=run()
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(out,ensure_ascii=False))
