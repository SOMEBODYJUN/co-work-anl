"""Designed insurance catalogue: five optimal singleton blocks and K5 pair covers.
Disjoint or overlapping banking themes may be added separately. This audit first
computes the exact SPE root minmax of pair insurance itself; no random sweep.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import sys,json,time
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver
edges=list(combinations(range(5),2))
inst=Instance(tuple('R'+str(e) for e in edges),tuple(CustomerType(frozenset(j for j,e in enumerate(edges) if x in e)) for x in range(5)),5)
t=time.time();s=ExactSPESolver(inst);out=s.outcomes(); root=(0,)*10
entry=[]
for a,e in enumerate(edges):
    child=(0,)*a+(1,)+(0,)*(9-a)
    R=s.outcomes(child)
    mn=min(inst.topic_payoffs(q)[a] for q in R)
    mx=max(inst.topic_payoffs(q)[a] for q in R)
    witnesses=[q for q in R if inst.topic_payoffs(q)[a]==mn]
    entry.append({'edge':e,'min_root':str(mn),'max_root':str(mx),'one_min_leaf':witnesses[0],'child_count':len(R)})
report={'scope':'five-player K5 two-block insurance, exact complete-history SPE outcome sets','elapsed':time.time()-t,'minimum_welfare':s.minimum_welfare(),'OPT':inst.optimal_welfare(),'stats':s.stats.__dict__,'entries':entry}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
