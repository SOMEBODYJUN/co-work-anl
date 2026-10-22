"""Independent definition-level verification of the announced 34-customer witness.
Uses only standard library, announced customer types, and complete strategy rules.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

TYPES={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,
       51:3,53:3,54:3,59:2}
UNITS=[frozenset(a for a in range(6) if mask>>a&1)
       for mask,n in TYPES.items() for _ in range(n)]
S=[frozenset(x for x,t in enumerate(UNITS) if a in t) for a in range(7)]
E=6

def pay(path,i):
    return sum((F(1,sum(x in S[a] for a in path)) for x in S[path[i]]),F(0))

def action(h):
    if len(h)==0:return 0
    if len(h)==1:return 3 if h[0] in (0,1,2) else 0
    if E not in h:
        group=range(3) if h[1]<3 else range(3,6)
        return min(a for a in group if a not in h)
    values=[pay(h+(a,),2) for a in range(7)]
    return max(range(7),key=lambda a:(values[a],-a))

def finish(h):
    while len(h)<3:h=h+(action(h),)
    return h

def main():
    gaps=[]
    for i in range(3):
        for h in product(range(7),repeat=i):
            orig=pay(finish(h),i)
            for a in range(7):
                delta=orig-pay(finish(h+(a,)),i)
                assert delta>=0,(h,a,delta)
                gaps.append(delta)
    p={2:F(1,10),E:F(9,10)}
    branch={a:finish((a,)) for a in range(7)}
    D=sum((p[a]*pay(branch[a],0) for a in p),F(0))
    entries={}
    for a in p:
        for b in p:
            z=branch[b]
            entries[a,b]=sum((F(1,1+sum(x in S[t] for t in z))
                              for x in S[a]),F(0))
    C=sum((p[a]*p[b]*entries[a,b] for a in p for b in p),F(0))
    root_u=pay(finish(()),0)
    assert len(UNITS)==34 and len(gaps)==399
    assert branch[E]==(6,0,1) and branch[2]==(2,3,4)
    assert entries[2,E]==F(32,3) and entries[2,2]==F(13,2)
    assert D==F(29,30) and C==F(41,40)
    assert D-C==F(-7,120) and root_u-C==F(1037,120)
    covers=[len(set().union(*(S[a] for a in z))) for z in product(range(7),repeat=3)]
    actual=finish(())
    result={'status':'PASS','customers':len(UNITS),'topics':7,'players':3,
      'decision_nodes':57,'comparisons_including_self':len(gaps),'true_deviations':342,
      'min_gap':str(min(gaps)),'p':{str(a):str(v) for a,v in p.items()},
      'root_path':actual,'root_payoffs':[str(pay(actual,i)) for i in range(3)],
      'W':len(set().union(*(S[a] for a in actual))),'OPT':max(covers),
      'D':str(D),'C':str(C),'D_minus_C':str(D-C),'root_u_minus_C':str(root_u-C),
      'branches':{str(a):z for a,z in branch.items()},
      'all_actions':[{'history':list(h),'action':action(h)} for i in range(3)
                     for h in product(range(7),repeat=i)]}
    Path(__file__).with_name('integer_push_34_independent_audit.json').write_text(
      json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','customers','decision_nodes','comparisons_including_self','D','C','D_minus_C','root_u_minus_C','W','OPT')}))

if __name__=='__main__':main()
