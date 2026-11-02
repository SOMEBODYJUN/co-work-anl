"""Targeted attack on the general Bellman squared-credit candidate; no proof."""
import json
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path

ROOT=Path(__file__).resolve().parents[6]

def test(name,power=2):
    inst=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    pol={tuple(row['history']): row['action'] for row in cert['strategy']['actions']}
    p=len(inst['topics']); m=inst['players']
    types=[(frozenset(row['topics']), row.get('multiplicity',1)) for row in inst['customers']]
    def counts(h):return tuple(h.count(a) for a in range(p))
    def load(q,B):return sum(q[a] for a in B)
    @lru_cache(None)
    def fv(q,r):
        best=F(0)
        for z in combinations_with_replacement(range(p),r):
            d=counts(z)
            val=sum((F(w*load(d,B),load(q,B)+load(d,B)) if load(d,B) else F(0)) for B,w in types)
            best=max(best,val)
        return best
    def leaf(h):
        h=list(h)
        while len(h)<m:h.append(pol[tuple(h)])
        return tuple(h)
    worst=None
    for h,A in pol.items():
        q=counts(h); r=m-len(h); z=leaf(h);tail=z[len(h)+1:];dt=counts(tail);qA=counts(h+(A,));zz=counts(z)
        u=sum((F(w,load(zz,B)) if A in B else F(0)) for B,w in types)
        deltaH=sum((w*(F(1,(load(q,B)+1)**power)-(F(1,(load(qA,B)+1)**power) if load(dt,B) else 0)) if A in B else 0) for B,w in types)
        slack=u+deltaH-fv(q,r)+fv(qA,r-1)
        row=(slack,h,A,z,u,deltaH,fv(q,r),fv(qA,r-1))
        if worst is None or row[0]<worst[0]:worst=row
    return {'instance':name,'power':power,'minimum_slack':str(worst[0]),'history':worst[1],'A':worst[2],'leaf':worst[3],'u':str(worst[4]),'deltaH':str(worst[5]),'F_r':str(worst[6]),'F_next':str(worst[7])}

if __name__=='__main__':
    import sys
    for name in sys.argv[1:] or ['root_tax_failure','individual_security_failure','aggregate_theta_failure','global_decorrelation_failure']:
        try: print(json.dumps(test(name),ensure_ascii=False))
        except Exception as e: print(name,repr(e))
