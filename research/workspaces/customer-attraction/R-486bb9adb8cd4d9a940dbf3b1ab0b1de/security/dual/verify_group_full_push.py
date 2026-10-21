"""Exact whole-SPE-cone certificate for one six-topic, three-player policy.
Standard library only. Reconstructs all 43 ordered histories and all 63 types.
Certificate discovery used LP, but this verifier uses only Fraction identities.
"""
from fractions import Fraction as F
from itertools import product,combinations
from functools import lru_cache
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
N=3;K=6;TYPES=range(1,1<<K)
def act(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    return next(a for a in (range(3)if h[1]<3 else range(3,6))if a not in h)
@lru_cache(None)
def out(h):
    return h if len(h)==N else out(h+(act(h),))
def own(t,a,z):
    return F(1,sum((t>>b)&1 for b in z))if (t>>a)&1 else F(0)
def insert(t,a,z):
    return F((t>>a)&1,1+sum((t>>b)&1 for b in z))
HISTORIES=[h for dep in range(N)for h in product(range(K),repeat=dep)]
ROWS=[(h,a)for h in HISTORIES for a in range(K)if a!=act(h)]
def gamma(h,a,t):return own(t,act(h),out(h))-own(t,a,out(h+(a,)))
ROOT=out(())
def cover(t):return F(any((t>>b)&1 for b in ROOT))
def M(a,b,t):return sum((insert(t,a,out(ROOT[:i]+(b,)))for i in range(N)),F(0))
def verify():
    cert=json.loads((HERE/'group_crosscap_certificate.json').read_text())
    assert cert['policy']=='root0/opposite-group/min-unused-in-second-group'
    assert len(cert['pairs'])==15
    seen=set();terms=0;minimum=None
    for item in cert['pairs']:
        a,b=item['pair'];assert 0<=a<b<K and (a,b)not in seen;seen.add((a,b))
        lam=[]
        for term in item['lambda']:
            h=tuple(term['history']);q=term['action'];v=F(term['coefficient'])
            assert (h,q)in ROWS and v>=0;lam.append((h,q,v));terms+=1
        residual=[F(v)for v in item['residual']];assert len(residual)==63 and min(residual)>=0
        for t,r in zip(TYPES,residual):
            assert 2*cover(t)-M(a,b,t)-M(b,a,t)==sum((v*gamma(h,q,t)for h,q,v in lam),F(0))+r
        minimum=min(residual)if minimum is None else min(minimum,min(residual))
    # Diagonal certificate has coefficient one on each on-path deviation.
    # Self choices give the zero row and are omitted.
    for a in range(K):
        for t in TYPES:
            gs=sum((gamma(ROOT[:i],a,t)for i in range(N)),F(0))
            rs=sum((own(t,a,out(ROOT[:i]+(a,)))-insert(t,a,out(ROOT[:i]+(a,)))for i in range(N)),F(0))
            assert rs>=0 and cover(t)-M(a,a,t)==gs+rs
    return dict(status='EXACT VERIFIED',scope='one complete policy, all nonnegative customer multiplicities in its full SPE cone, all query distributions p',ordered_histories=len(HISTORIES),proper_deviation_rows=len(ROWS),customer_types=63,cross_pairs=15,diagonal_queries=6,cross_identities=15*63,diagonal_identities=6*63,nonzero_cross_multipliers=terms,minimum_cross_residual=str(minimum),root=list(ROOT),claim='W >= sum_i E_(a,b iid p) f_(full z_i(b))(a) for every p')
if __name__=='__main__':print(json.dumps(verify(),indent=2))
