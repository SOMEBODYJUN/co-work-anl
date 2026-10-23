#!/usr/bin/env python3
"""Independent exact audit: full SPE, true v4, and water-fill sharpness.

No solver, verifier, LP, or shared payoff routine is imported here. Water-fill
weights are generally irrational; Fraction bisection gives certified rational
brackets instead of silently treating floating approximations as exact weights.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement,product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ins=json.loads((HERE/"endogenous_53_instance.json").read_text())
cert=json.loads((HERE/"endogenous_53_strategy.json").read_text())
m=ins["players"];p=len(ins["topics"])
customers=tuple(frozenset(row["topics"]) for row in ins["customers"]
                for _ in range(row["multiplicity"]))
actions={tuple(row["history"]):row["action"] for row in cert["actions"]}
expected={h for depth in range(m) for h in product(range(p),repeat=depth)}
assert set(actions)==expected and len(actions)==400

@lru_cache(None)
def finish(h):
    return h if len(h)==m else finish(h+(actions[h],))

def payoff(z,a):
    return sum((F(1,sum(t in s for t in z)) for s in customers if a in s),F())

least=None;comparisons=0
for h in expected:
    z=finish(h);a=actions[h];u=payoff(z,a)
    for t in range(p):
        v=payoff(finish(h+(t,)),t)
        assert u>=v,(h,t,u,v)
        comparisons+=1;least=u-v if least is None else min(least,u-v)
z=finish(())
assert z==(6,0,3,4)
actual=tuple(payoff(z,a) for a in z)
assert actual==(F(19),F(29,3),F(67,6),F(67,6))

def query(a,B):
    return sum((F(1,1+sum(t in s for t in B)) for s in customers if a in s),F())

t0=F(28481,2924)
primary=(F(285,2924),F(285,2924),F(1197,5848),F(285,2924),
         F(285,2924),F(1197,5848),F(587,2924))
dual={ (0,1,2):F(37,1462), (0,1,6):F(3941,14620),
       (0,2,6):F(1481,14620), (1,2,6):F(1481,14620),
       (3,4,6):F(4089,14620), (3,5,6):F(1629,14620),
       (4,5,6):F(1629,14620)}
assert sum(primary)==sum(dual.values())==1
backgrounds=tuple(combinations_with_replacement(range(p),3))
primal=[sum((primary[a]*query(a,B) for a in range(p)),F()) for B in backgrounds]
assert min(primal)==t0
dual_values=tuple(sum((w*query(a,B) for B,w in dual.items()),F()) for a in range(p))
assert dual_values==(t0,)*p
D=t0-F(29,3)
assert D==F(647,8772)>0

def low_unit(w,core):
    return F(12,1+w)+F(11,2+w)+F(core,3+w)

def root_unit(w,core):
    return F(19)+F(core,3+w)

def case(core):
    threshold=t0+F(core,4)
    before=F(29,3)+F(core,4)
    assert threshold-before==D
    linear=before/threshold
    linear_after=low_unit(linear,core)
    assert linear_after<threshold
    # g(w) is strictly decreasing. The desired positive weight is the unique
    # root g(w)=threshold, bracketed on [lo,hi].
    lo=F(0);hi=F(1)
    assert low_unit(lo,core)>threshold>low_unit(hi,core)
    for _ in range(80):
        mid=(lo+hi)/2
        if low_unit(mid,core)>threshold:
            lo=mid
        else:
            hi=mid
    assert low_unit(lo,core)>=threshold>=low_unit(hi,core)
    original_root=F(19)+F(core,4)
    gamma_lo=root_unit(hi,core)-original_root
    gamma_hi=root_unit(lo,core)-original_root
    assert F(0)<=gamma_lo<=gamma_hi<=D
    if core:
        assert 1-hi<=F(16)*D/core
    return {"common_core":core,"threshold":str(threshold),"low_original":str(before),
            "deficit":str(D),"linear_retention":str(linear),
            "linear_final_unit":str(linear_after),"linear_shortfall":str(threshold-linear_after),
            "water_weight_interval":[str(lo),str(hi)],
            "root_gain_interval":[str(gamma_lo),str(gamma_hi)],
            "root_gain_over_deficit_interval":[str(gamma_lo/D),str(gamma_hi/D)]}

# Direct finite-difference identity checks for rational weighted profiles. A
# retained root always has weight one; zero-customer and empty-query terms are
# included. This is a regression, not the proof of the general lemma.
finite_checks=0
for b in range(4):
 for root_bit,query_bit,j_bit in product((0,1),repeat=3):
  for other in (F(0),F(1,3),F(2)):
   for old,new in ((F(1),F(2,3)),(F(2,3),F(1,5)),(F(1,5),F(0))):
    if not j_bit:
        continue
    old_den=b+root_bit+other+old
    new_den=b+root_bit+other+new
    if not new_den:
        continue  # this coordinate cannot be water-pruned to zero at finite t
    own_delta=1/new_den-1/old_den
    query_delta=query_bit*(1/(b+1+other+new)-1/(b+1+other+old))
    root_delta=root_bit*(1/new_den-1/old_den)
    assert 0<=root_delta<=own_delta and 0<=query_delta<=own_delta
    finite_checks+=1

report={"scope":"exact finite certificate plus arithmetic audit of an all-r analytical auxiliary lemma",
        "unit_customers_base":len(customers),"players":m,"topics":p,
        "complete_ordered_histories":len(expected),"checked_SPE_comparisons_including_self":comparisons,
        "minimum_SPE_slack":str(least),"actual_path":z,"actual_payoffs":[str(u) for u in actual],
        "true_v4":str(t0),"static_backgrounds_checked":len(backgrounds),
        "primal_minimum":str(min(primal)),"dual_all_queries":[str(v) for v in dual_values],
        "deficit":str(D),"finite_difference_checks":finite_checks,
        "cases":[case(c) for c in (0,1,10,1000,1000000)],
        "not_claimed":"fractionally pruned profile is not a unit-player SPE; no half or GAP-r proof"}
(HERE/"waterfill_exact.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k!="cases"},indent=2))
for row in report["cases"]:
    print(json.dumps({"core":row["common_core"],"Gamma_over_D_lower":row["root_gain_over_deficit_interval"][0]}))
