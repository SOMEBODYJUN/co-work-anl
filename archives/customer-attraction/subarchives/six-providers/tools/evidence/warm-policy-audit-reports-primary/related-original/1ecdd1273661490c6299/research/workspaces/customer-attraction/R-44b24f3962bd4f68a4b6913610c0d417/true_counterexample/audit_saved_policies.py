"""Standalone unit-customer Fraction replay: no canonical package imports.
Only verifies the two saved key finite policies, not an all-policy bound.
"""
from fractions import Fraction
from itertools import product,combinations
import json
from pathlib import Path
HERE=Path(__file__).parent
rows=[]
for filename in ('warm_m5p7.json','warm_m5p7_41.json'):
    source=json.loads((HERE/filename).read_text());cert=source['exact_candidate'];p=source['milp']['topics'];m=source['milp']['players']
    actions={tuple(v['history']):v['action'] for v in cert['strategy']['actions']}
    histories={h for depth in range(m) for h in product(range(p),repeat=depth)}
    assert set(actions)==histories
    customers=[mask for mask,count in enumerate(cert['integer_clones'],1) for _ in range(count)]
    def terminal(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    def utility(h,a):
        counts=[h.count(b) for b in range(p)]
        return sum((Fraction(1,sum(counts[b] for b in range(p) if mask&(1<<b))) for mask in customers if mask&(1<<a)),Fraction(0))
    checks=0
    for h,a in actions.items():
        u=utility(terminal(h),a)
        for b in range(p):
            if b==a:continue
            assert u>=utility(terminal(h+(b,)),b),(filename,h,a,b)
            checks+=1
    path=terminal(());actualmask=sum(1<<a for a in set(path));W=sum(bool(mask&actualmask) for mask in customers)
    OPT=max(sum(bool(mask&sum(1<<a for a in J)) for mask in customers) for r in range(min(m,p)+1) for J in combinations(range(p),r))
    assert W==cert['welfare'] and OPT==cert['optimal_welfare']
    assert Fraction(OPT,W)==Fraction(cert['value'])
    covers=[frozenset(j for j,mask in enumerate(customers) if mask&(1<<a)) for a in range(p)]
    classes=list(dict.fromkeys(covers));projection=[classes.index(S) for S in covers];representatives=[projection.index(c) for c in range(len(classes))]
    quotient_actions={}
    def lift_tree(H,h):
        if len(H)==m:return
        chosen=actions[h];c=projection[chosen];quotient_actions[H]=c
        for d in range(len(classes)):
            b=chosen if d==c else representatives[d]
            lift_tree(H+(d,),h+(b,))
    lift_tree((),())
    def qt(H):
        while len(H)<m:H=H+(quotient_actions[H],)
        return H
    def qu(H,c):
        return sum((Fraction(1,sum(j in classes[d] for d in H)) for j in classes[c]),Fraction(0))
    qchecks=0
    for H,c in quotient_actions.items():
        for d in range(len(classes)):
            if d!=c:
                assert qu(qt(H),c)>=qu(qt(H+(d,)),d)
                qchecks+=1
    assert sum(bool(mask&actualmask) for mask in customers)==W
    rows.append({'distinct_coverages':len(classes),'quotient_nodes':len(quotient_actions),'quotient_deviations':qchecks,'file':filename,'unit_customers':len(customers),'root_path':path,'welfare':W,'optimum':OPT,'ratio':str(Fraction(OPT,W)),'nodes':len(actions),'nonself_deviations':checks,'half_margin':2*W-OPT})
out={'scope':'standalone unit-customer exact replay of two specified complete policies only','records':rows}
(HERE/'saved_policy_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
