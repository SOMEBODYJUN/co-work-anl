"""Definition-level Fraction audit of the exact last-two reserve identities."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

def audit(name,k,types,p,n=5):
    @lru_cache(None)
    def util(a,z):
        return sum((F(w,sum((t>>b)&1 for b in z)) for t,w in types if (t>>a)&1),F(0))
    @lru_cache(None)
    def finish(h):
        if len(h)==n:return h
        rows=[(util(a,finish(h+(a,))),a)for a in range(k)]
        a=max(rows)[1]
        return finish(h+(a,))
    z=finish(())
    all_ic=[]
    for d in range(n):
        for h in product(range(k),repeat=d):
            out=finish(h);chosen=out[d]
            all_ic.extend(util(chosen,out)-util(a,finish(h+(a,)))for a in range(k))
    assert min(all_ic)>=0
    def query(z):
        return sum((p[a]*sum((F(w,1+sum((t>>b)&1 for b in z))for t,w in types if (t>>a)&1),F(0))for a in range(k)),F(0))
    def up(a,b,prefix):
        return util(a,prefix+(a,b))
    h=z[:n-2];b={t:sum((t>>a)&1 for a in h)for t,w in types}
    leaves=[finish(h+(a,))for a in range(k)]
    last=[v[-1]for v in leaves]
    Qpen=sum((p[a]*query(leaves[a])for a in range(k)),F(0))
    upen=util(z[-2],z)
    gamma=sum((p[a]*(upen-util(a,leaves[a]))for a in range(k)),F(0))
    regrets=sum((p[a]*p[t]*(up(last[a],a,h)-up(last[t],a,h))for a in range(k)for t in range(k)),F(0))
    overlap=sum((p[a]*p[t]*sum((F(w,(b[mask]+1+((mask>>last[a])&1))*(b[mask]+2+((mask>>last[a])&1)))for mask,w in types if (mask>>a)&(mask>>t)&1),F(0))for a in range(k)for t in range(k)),F(0))
    assert upen-Qpen==gamma+regrets+overlap
    assert min(gamma,regrets,overlap)>=0
    q={t:sum((p[a]for a in range(k)if(t>>a)&1),F(0))for t,w in types}
    penlower=sum((F(w)*q[t]**2/F((b[t]+2)*(b[t]+3))for t,w in types),F(0))
    assert overlap>=penlower
    hlast=z[:n-1];blast={t:sum((t>>a)&1 for a in hlast)for t,w in types}
    Qlast=sum((p[a]*query(finish(hlast+(a,)))for a in range(k)),F(0))
    ulast=util(z[-1],z)
    glast=sum((p[a]*(ulast-util(a,finish(hlast+(a,))))for a in range(k)),F(0))
    curvature=sum((F(w)*q[t]**2/F((blast[t]+1)*(blast[t]+2))for t,w in types),F(0))
    assert ulast-Qlast==glast+curvature
    R=[(t,w)for t,w in types if not any((t>>a)&1 for a in z)]
    C=[(t,w)for t,w in types if any((t>>a)&1 for a in z)]
    Rlower=F(2,3)*sum((F(w)*q[t]**2 for t,w in R),F(0))
    Clower=F(1,15)*sum((F(w)*q[t]**2 for t,w in C),F(0))
    assert penlower+curvature>=Rlower+Clower
    return dict(name=name,n=n,k=k,actual=z,ordered_histories=sum(k**d for d in range(n)),ic_rows=len(all_ic),minimum_ic=str(min(all_ic)),penultimate=dict(actual_u=str(upen),Q=str(Qpen),difference=str(upen-Qpen),gamma=str(gamma),last_reply_regret=str(regrets),overlap=str(overlap),curvature_lower=str(penlower)),last=dict(actual_u=str(ulast),Q=str(Qlast),difference=str(ulast-Qlast),gamma=str(glast),curvature=str(curvature)),R_clients=sum(w for t,w in R),R_curvature_floor=str(Rlower),C_curvature_floor=str(Clower),all_checks=True)

fixtures=[
    ('four_genuine_overlap',4,[(t,1+(3*t)%7)for t in range(1,16)],[F(1,10),F(2,10),F(3,10),F(4,10)]),
    ('overlap_plus_empty',5,[(t,1+(5*t)%3)for t in range(1,16)],[F(1,15),F(2,15),F(3,15),F(4,15),F(5,15)]),
    ('six_disjoint_with_missed_client',6,[(1<<a,1)for a in range(6)],[F(1,6)]*6),
    ('all_zero_single_empty',1,[],[F(1)]),
]
out=[audit(*f)for f in fixtures]
path=Path(__file__).with_name('tail_reserves_audit.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
