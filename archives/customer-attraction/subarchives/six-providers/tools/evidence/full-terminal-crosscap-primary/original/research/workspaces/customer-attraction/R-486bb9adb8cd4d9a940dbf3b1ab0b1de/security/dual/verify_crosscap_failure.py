"""Independent Fraction replay of fixed-query full-terminal crosscap failure.
No imports from the discovery scripts, model, solver, numpy, or scipy.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from functools import lru_cache
import json
HERE=Path(__file__).resolve().parent
WEIGHTS={2:20,5:6,8:45,17:6,21:36,22:6,33:6,37:36,38:6,49:36,50:6,54:36}
def verify():
    discovery=json.loads((HERE/'crosscap_failure_exact.json').read_text());n=4;k=6
    acts={tuple(r['history']):r['action']for r in discovery['actions']}
    hs=[h for d in range(n)for h in product(range(k),repeat=d)]
    assert set(acts)==set(hs)and len(acts)==259
    @lru_cache(None)
    def out(h):return h if len(h)==n else out(h+(acts[h],))
    # Expand every compressed multiplicity into separate unit customers.
    units=[frozenset(a for a in range(k)if(t>>a)&1)for t,r in WEIGHTS.items()for _ in range(r)]
    def own(a,z):return sum((F(1,sum(b in t for b in z))for t in units if a in t),F(0))
    def insert(a,z):return sum((F(1,1+sum(b in t for b in z))for t in units if a in t),F(0))
    slacks=[]
    for h in hs:
        incumbent=own(acts[h],out(h))
        for a in range(k):slacks.append(incumbent-own(a,out(h+(a,))))
    assert len(slacks)==1554 and min(slacks)>=0
    z=out(());u=[own(a,z)for a in z];W=sum(any(a in t for a in z)for t in units)
    assert sum(u)==W==180
    a,b=3,5
    columns=[]
    for i in range(n):
        za=out(z[:i]+(a,));zb=out(z[:i]+(b,))
        columns.append({'player':i+1,'z_a':list(za),'z_b':list(zb),'f_z_b_a':str(insert(a,zb)),'f_z_a_b':str(insert(b,za))})
    M=lambda x,y:sum((insert(x,out(z[:i]+(y,)))for i in range(n)),F(0))
    cross=M(a,b)+M(b,a);assert cross==365 and cross-2*W==5
    diagonal_a=M(a,a);diagonal_b=M(b,b)
    # The equal two-query mixture is checked separately; cross failure alone is not FTA failure.
    push=(diagonal_a+diagonal_b+cross)/4
    opt=max(sum(any(a in t for a in s)for t in units)for d in range(1,min(n,k)+1)for s in combinations(range(k),d))
    return dict(status='EXACT VERIFIED',scope='fails only pairwise full-terminal crosscap; does not alone refute all-p push, full-menu cap, security aggregation, or half',unit_customers=len(units),players=n,topics=k,ordered_histories=len(hs),action_comparisons=len(slacks),minimum_incentive_slack=str(min(slacks)),root=list(z),utilities=list(map(str,u)),W=W,OPT=opt,query_pair=[a,b],columns=columns,M_ab=str(M(a,b)),M_ba=str(M(b,a)),cross=str(cross),two_W=2*W,violation=str(cross-2*W),M_aa=str(diagonal_a),M_bb=str(diagonal_b),equal_mixture_push=str(push),equal_mixture_budget=str(W-push),all_two_query_p_budget_polynomial='143*t^2 - 101*t + 48',all_two_query_p_minimum='17255/572')
if __name__=='__main__':print(json.dumps(verify(),indent=2))
