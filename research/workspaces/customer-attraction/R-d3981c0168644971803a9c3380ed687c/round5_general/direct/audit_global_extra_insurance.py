"""Independent unit-client, complete-history audit of security's insurance family.

No imports from security, canonical BI, or the author's implementation. This
uses explicit fresh/fresh exits, whose legality is proved in the review.
The single default finite audit is m=4; the all-m theorem is analytic.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--players",type=int,default=4)
M=parser.parse_args().players
assert M>=2
BANKS=M-1
ACTIONS=tuple(product(range(M),range(BANKS)))
TOPICS={a:frozenset((a[0],M+2*a[1],M+2*a[1]+1)) for a in ACTIONS}
CLIENTS=tuple(range(3*M-2))

def state(h):
    assert h
    anchor_a,anchor_b=h[0]
    mode="BASE";target=None
    used_b={anchor_b}
    for j,a in enumerate(h[1:],start=1):
        assert j<M-1
        if mode=="BASE":
            prescribed=(anchor_a,min(set(range(BANKS))-used_b))
            if a!=prescribed:
                if a[1] in used_b:mode="EXIT"
                else:mode="PUNISH";target=a[1]
        elif mode=="PUNISH" and a[1] in used_b:
            mode="EXIT"
        used_b.add(a[1])
    return mode,anchor_a,anchor_b,target

@lru_cache(None)
def action(h):
    if not h:return (0,0)
    mode,aa,ab,target=state(h)
    used_a={a for a,b in h};used_b={b for a,b in h}
    free_a=set(range(M))-used_a;free_b=set(range(BANKS))-used_b
    assert len(free_a)>=M-len(h)
    last=len(h)==M-1
    if mode=="BASE":
        assert len(used_b)==len(h)
        return (min(free_a),ab) if last else (aa,min(free_b))
    if mode=="PUNISH":
        assert len(used_b)==len(h) and target in used_b
        return (min(free_a),target) if last else (min(free_a),min(free_b))
    assert len(free_b)>=M-len(h)
    return (min(free_a),min(free_b))

@lru_cache(None)
def finish(h):
    if len(h)==M:return h
    return finish(h+(action(h),))

@lru_cache(None)
def values(z):
    counts={x:sum(x in TOPICS[a] for a in z) for x in CLIENTS}
    us=tuple(sum((F(1,counts[x]) for x in TOPICS[a]),F(0)) for a in z)
    return us,sum(counts[x]>0 for x in CLIENTS)

nodes=0;comparisons=0;minimum=None;strict=0;by_mode={}
for depth in range(M):
    for h in product(ACTIONS,repeat=depth):
        nodes+=1
        key="ROOT" if not h else state(h)[0]
        by_mode[key]=by_mode.get(key,0)+1
        prescribed=values(finish(h))[0][depth]
        for a in ACTIONS:
            gap=prescribed-values(finish(h+(a,)))[0][depth]
            assert gap>=0,(h,a,gap)
            comparisons+=1;strict+=gap>0
            minimum=gap if minimum is None else min(minimum,gap)
z=finish(())
us,W=values(z)
OPT=max(values(y)[1] for y in product(ACTIONS,repeat=M))
tau=F(1,2)+F(2*(M-1),2*M-1)
delta=F(1)+F(M,2*M-1)
root_children=[values(finish((a,)))[0][0] for a in ACTIONS]
assert z==((0,0),)+tuple((0,b) for b in range(1,M-1))+((1,0),)
assert us==(F(M,M-1),)+(F(2)+F(1,M-1),)*(M-2)+(F(2),)
assert W==2*M and OPT==3*M-2
assert tau-us[0]==F(2*M*M-9*M+5,2*(2*M-1)*(M-1))
assert delta-us[0]==F(M*M-3*M+1,(2*M-1)*(M-1))
assert len(set(root_children))==1
report={"source":"Independent reconstruction of security insurance construction",
        "players":M,"unit_clients":len(CLIENTS),"common_topics":len(ACTIONS),
        "full_ordered_decision_histories":nodes,"full_IC_comparisons":comparisons,
        "strict_IC_comparisons":strict,"minimum_IC_gap":minimum,"history_modes":by_mode,
        "actual_profile":z,"utilities":us,"welfare":W,"OPT":OPT,
        "global_extra_fractional_value":tau,"extra_value_minus_root":tau-us[0],
        "standard_global_fractional_value":delta,"standard_value_minus_root":delta-us[0],
        "welfare_minus_m_standard_value":W-M*delta,
        "all_root_action_continuation_payoffs":root_children,
        "m5_symbolic_substitution_from_general_formulas":{
            "root_utility":F(5,4),"tau":F(25,18),"tau_minus_root":F(5,36),
            "welfare":10,"OPT":13,"OPT_over_2m_minus_root":F(1,20)},
        "scope":"Single finite boundary audit plus general analytic review. Individual standard floor fails m>=3, GEX m>=4; not HALF."}
print(json.dumps(report,default=str,indent=2))
