"""Standard-library coefficient audit for RESET's pointwise ingredients."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
counts={'omission_states':0,'deficit_states':0,'outside_states':0,'partition_states':0,'full_identity_states':0}
for p,a,b,e,h in product(range(3),*([(0,1)]*4)):
    last=F(e,p+a+b+e) if e else F(0)
    query=F(h,p+a+b+1)
    f=F(h*e,p+3)+F((1-h)*e,p+1)
    k=F(h,p+3)
    miss=int(p==a==b==e==0 and h==1)
    assert F(3,2)*(query+f-last-k)>=miss
    counts['omission_states']+=1
for p,h,q,r in product(range(3),*([(0,1)]*3)):
    v=F(h,p+h+q+r) if h else F(0)
    k=F(h,p+3);d=F(h*(2-q-r),p+3)
    assert 4*(v-k)>=d
    counts['deficit_states']+=1
    outside=F((1-h)*(q+r),p+3)
    fresh=int(p==0 and h==0 and (q or r))
    assert 3*outside>=fresh
    counts['outside_states']+=1
for p,a,b,e,h,q,r in product(range(3),*([(0,1)]*6)):
    src=bool(p+a+b+e); child=bool(p+h+q+r)
    new=int(child and not src)
    m=int(p==a==b==e==0 and h==1)
    fresh_out=int(p==0 and h==0 and (q or r))
    assert m+fresh_out>=new
    counts['partition_states']+=1
    last=F(e,p+a+b+e) if e else F(0)
    query=F(h,p+a+b+1)
    f=F(h*e,p+3)+F((1-h)*e,p+1)
    k=F(h,p+3); v=F(h,p+h+q+r) if h else F(0)
    eta=v-k;d=F(h*(2-q-r),p+3)
    G0=last-query;G1=k+8*eta-f
    GQ=k-F(q,p+3);GR=k-F(r,p+3);GD=4*eta-d
    rho0=F(3,2)*(query+f-last-k)-m
    rho1=3*F((1-h)*(q+r),p+3)-fresh_out
    rho2=m+fresh_out-new
    assert min(rho0,rho1,rho2,GD)>=0
    rhs=F(3,2)*G0+F(3,2)*G1+3*GQ+3*GR+3*GD+rho0+rho1+rho2
    assert 24*eta-new==rhs
    counts['full_identity_states']+=1
out={'status':'PASS_exact_pointwise_RESET_ingredients_not_HALF5','coefficient':24,'states':counts}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
