"""Self-contained unit-customer/full-ordered-tree audit of the padded repair.

No repository model, solver, or verifier imports. The base instance has empty
root and one m-customer old theme. Its unique positive-depth behavior is the
big old theme, and its root defect is exactly 1. Thus s=1 repairs a real defect.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from functools import lru_cache
import json

HERE=Path(__file__).resolve().parent

def audit(m):
    p=2*m
    masses=(2,m-1)+tuple(1 for _ in range(m-2))
    def icounts(h):return tuple(h.count(a) for a in range(m))
    @lru_cache(None)
    def bi(k):
        if sum(k)==m:return k
        children=[]
        for a in range(m):
            child=bi(tuple(x+int(j==a) for j,x in enumerate(k)))
            children.append((F(masses[a],child[a]),-a,child))
        return max(children)[2]
    def biact(h):
        k=icounts(h)
        children=[]
        for a in range(m):
            child=bi(tuple(x+int(j==a) for j,x in enumerate(k)))
            children.append((F(masses[a],child[a]),-a))
        return -max(children)[1]
    def iact(h,mode):
        if mode=='H':return 1
        if mode=='LX':return 0 if len(h)==1 else 1
        if mode=='LZ':return biact(h)
        assert mode=='LY'
        first=next((a for a in h if a!=1),None)
        if first is None:return 0
        if first==0:return 1
        return biact(h)
    A={():0}
    for d in range(1,m):
        for h in product(range(p),repeat=d):
            root=h[0]
            old,ins=divmod(root,m)
            mode=('H' if old==0 else 'LX') if ins==0 else 'LY' if ins==1 else 'LZ'
            A[h]=m+iact(tuple(a%m for a in h),mode)
    assert len(A)==sum(p**d for d in range(m))
    # Explicit individual customers, represented by their topic-interest sets.
    units=[frozenset(range(m,p)) for _ in range(m)]
    for a,w in enumerate(masses):units.extend([frozenset((a,m+a)) for _ in range(w)])
    @lru_cache(None)
    def end(h):
        if len(h)==m:return h
        return end(h+(A[h],))
    @lru_cache(None)
    def U(z,a):
        return sum((F(1,sum(t in B for t in z)) for B in units if a in B),F(0))
    def W(z):return sum(bool(B.intersection(z)) for B in units)
    minimum=None;comparisons=0
    for h,a in A.items():
        actual=U(end(h),a)
        for b in range(p):
            slack=actual-U(end(h+(b,)),b)
            minimum=slack if minimum is None else min(minimum,slack)
            assert slack>=0,(m,h,a,b,slack)
            comparisons+=1
    z=end(())
    opt=max(W(J) for J in combinations(range(p),m))
    assert z==(0,)+(m+1,)*(m-1)
    assert U(z,0)==2
    assert W(z)==m+(m+1)
    assert opt==m+(2*m-1)
    assert opt-2*W(z)==m-2*m-3
    ds=[U(end((b,)),b) for b in range(p)]
    # Every nonprescribed root has insurer payoff <= 1, directly from units.
    for b in range(1,p):
        ins=b%m;terminal=end((b,))
        insurer=F(masses[ins],sum(t%m==ins for t in terminal))
        assert insurer<=1,(m,b,terminal,insurer)
    cert=dict(scope='Complete pure SPE from a root-defective old policy; all ordered histories and legal tuple deviations audited.',
              m=m,p=p,unit_customer_interests=[sorted(B) for B in units],
              actions=[dict(history=list(h),action=a) for h,a in sorted(A.items())],
              path=list(z),W=W(z),OPT=opt,root_payoff=str(U(z,0)),root_deviations=list(map(str,ds)))
    (HERE/f'padded_insurer_m{m}_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    return dict(m=m,old_root_defect='1',s='1',topics=p,unit_customers=len(units),
                ordered_decision_histories=len(A),comparisons=comparisons,minimum_slack=str(minimum),
                root_payoff=str(U(z,0)),old_W=m,old_OPT=m,W=W(z),OPT=opt,
                insurer_W=m+1,insurer_OPT=2*m-1,insurer_half_dilution=3,
                BI_count_states=bi.cache_info().currsize)

def main():
    report=dict(scope='Finite full-tree exact audits; universal theorem rests on the analytic proof.',cases=[])
    for m in range(2,6):
        rec=audit(m);report['cases'].append(rec);print(json.dumps(rec),flush=True)
        (HERE/'padded_insurer_audit.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
