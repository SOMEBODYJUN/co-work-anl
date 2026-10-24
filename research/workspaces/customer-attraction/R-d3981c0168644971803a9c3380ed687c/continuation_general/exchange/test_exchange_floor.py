"""Attack only: test the general relative-exclusive exchange floor on fixed certificates."""
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[6]

def test(name):
    inst=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    pol={tuple(row['history']):row['action'] for row in cert['strategy']['actions']}
    p=len(inst['topics']);m=inst['players']
    types=[(frozenset(row['topics']),row.get('multiplicity',1)) for row in inst['customers']]
    def leaf(h):
        h=list(h)
        while len(h)<m:h.append(pol[tuple(h)])
        return tuple(h)
    worst=None
    checks=0
    for h,A in pol.items():
        r=m-len(h);z=leaf(h)
        u=sum((F(w,sum(a in B for a in z)) if A in B else F(0)) for B,w in types)
        forbidden=set(h)|{A}
        residual=[(B,w) for B,w in types if B.isdisjoint(forbidden)]
        for comp in combinations(range(p),r):
            private=[sum(w for B,w in residual if a in B and len(B.intersection(comp))==1) for a in comp]
            loss=min(private)
            checks+=1
            row=(F(loss)-u,h,A,z,comp,private,u)
            if worst is None or row[0]>worst[0]:worst=row
    return {'instance':name,'checks':checks,'max_violation':str(worst[0]),'history':worst[1],'A':worst[2],'leaf':worst[3],'comparison':worst[4],'private':worst[5],'u':str(worst[6])}
if __name__=='__main__':
    import sys
    for name in sys.argv[1:] or ['root_tax_failure','individual_security_failure','aggregate_theta_failure','global_decorrelation_failure']:
        try:print(json.dumps(test(name),ensure_ascii=False))
        except Exception as e:print(name,repr(e))
