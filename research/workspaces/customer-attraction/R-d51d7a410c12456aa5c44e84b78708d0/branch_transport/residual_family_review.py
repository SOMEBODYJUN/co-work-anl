"""Independent unit-customer reconstruction of the two-player residual family.

Does not import the proposed generator, canonical solver, or certificate code.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

def check(q):
    labels=('A','B','D','E')+tuple('T'+str(j) for j in range(1,q+1))
    customers=[]
    def add(mask,count):
        customers.extend([frozenset(mask) for _ in range(count)])
    add(('A',),2*q);add(('B',),2*q+1)
    add(('A','D','E'),2);add(('B','D','E'),2)
    for T in labels[4:]:
        add((T,),2*q-1);add((T,'D'),2);add((T,'E'),2)
    sets={a:{i for i,B in enumerate(customers) if a in B} for a in labels}
    def reply(a):return 'B' if a=='A' else 'E' if a=='D' else 'D'
    def utility(a,b):return sum((Fraction(1,2) if x in sets[b] else Fraction(1)) for x in sets[a])
    inequalities=[]
    for a in labels:
        inequalities.extend(utility(reply(a),a)-utility(b,a) for b in labels)
    inequalities.extend(utility('A','B')-utility(a,reply(a)) for a in labels)
    assert min(inequalities)>=0
    C=sets['A']|sets['B']; W=len(C)
    optimum=max(len(sets[a]|sets[b]) for a,b in product(labels,repeat=2))
    residual=max(len((sets[a]|sets[b])-C) for a,b in product(labels,repeat=2))
    assert W==4*q+5
    assert optimum==residual==4*q+6
    assert all(sets[T].isdisjoint(C) for T in labels[4:])
    assert len(sets['T1']|sets['T2'])==4*q+6
    assert 2*W>=optimum
    return dict(q=q,topics=len(labels),unit_customers=len(customers),ordered_nodes=len(labels)+1,
                action_comparisons=len(inequalities),W=W,OPT2=optimum,residual_OPT2=residual,
                least_SPE_slack=str(min(inequalities)))

if __name__=='__main__':
    records=[check(q) for q in range(2,41)]
    out=dict(status='independent exact definition-level finite audit; universal proof is in accompanying review',
             comparisons=sum(r['action_comparisons'] for r in records),records=records)
    p=Path(__file__).with_name('residual_family_review.json')
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],q_range=[2,40],comparisons=out['comparisons'])))
