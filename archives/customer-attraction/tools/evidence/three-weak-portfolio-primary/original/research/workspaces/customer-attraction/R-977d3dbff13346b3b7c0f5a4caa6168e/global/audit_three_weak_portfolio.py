"""Exact, definition-level universal audit; no solver or LP imported."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def u(x,y,z):return F(x,1+y+z)

def raw(a,b,c,T,L,Q,R):
    uc=u(c,a,b);w=int(a+b+c>0);o=int(any(T))
    target=3*w-3*o+sum(u(T[j],Q[j],R[j])+u(T[j],a,L[j])+u(T[j],a,b) for j in range(3))
    slacks=[sum(uc-u(t,a,b) for t in T),sum(uc-u(l,a,b) for l in L),
        sum(u(L[j],a,T[j])-u(L[k],a,T[j]) for j in range(3) for k in range(3)),
        sum(u(L[j],a,T[j])-u(Q[k],a,T[j]) for j in range(3) for k in range(3)),
        sum(uc-u(r,a,b) for r in R),
        sum(u(R[j],T[j],Q[j])-u(R[k],T[j],Q[j]) for j in range(3) for k in range(3))]
    coeff=[F(5,12),F(1,4),F(3,10),F(1,30),F(1,18),F(1,12)]
    return target-sum(v*k for v,k in zip(slacks,coeff))

def reduced(a,b,c,T,L,Q,R):
    d,l,q,r=map(sum,(T,L,Q,R));k=1+a+b;D=(1+a)*(2+a)
    return (3*int(a+b+c>0)-3*int(d>0)-F(13*c,6*k)
        +(F(17*d,12)+F(l,4)+F(r,18))/k+F(d,1+a)
        -(F(3*d*l,10)+F(d*q,30))/D-F(l-q,10*(1+a))
        +sum(u(T[j],Q[j],R[j]) for j in range(3))
        -F(1,12)*sum(F(3*R[j]-r,1+T[j]+Q[j]) for j in range(3)))

def compressed_min(a,b,c,d,q1,q0):
    k=1+a+b;D=(1+a)*(2+a);q=q1+q0
    n={(1,1):q1,(1,0):d-q1,(0,1):q0,(0,0):3-d-q0}
    inv=sum(F(count,1+t+v) for (t,v),count in n.items())
    constant=(3*int(a+b+c>0)-3*int(d>0)-F(13*c,6*k)+F(17*d,12*k)
        +F(d,1+a)-F(d*q,30*D)+F(q,10*(1+a))+d-F(q1,2))
    ell=F(1,4*k)-F(3*d,10*D)-F(1,10*(1+a))
    # Affine in ell=sum L, and separately affine in each R_j.
    value=constant+3*min(0,ell)
    for (t,v),count in n.items():
        rr=(F(1,18*k)-F(t,(1+v)*(2+v))-F(1,4*(1+t+v))+F(1,12)*inv)
        value+=count*min(0,rr)
    return value

def main():
    minima={(a,b,c,d):None for a,b,c in product([0,1],repeat=3) for d in range(4)}
    patterns=0
    for a,b,c in product([0,1],repeat=3):
        for T,L,Q,R in product(list(product([0,1],repeat=3)),repeat=4):
            exact=raw(a,b,c,T,L,Q,R);other=reduced(a,b,c,T,L,Q,R)
            if exact!=other:raise AssertionError(('expansion',a,b,c,T,L,Q,R,exact,other))
            if exact<0:raise AssertionError(('negative',a,b,c,T,L,Q,R,exact))
            key=(a,b,c,sum(T));minima[key]=exact if minima[key] is None else min(minima[key],exact)
            patterns+=1
    compressed={}
    for a,b,c in product([0,1],repeat=3):
        for d in range(4):
            value=min(compressed_min(a,b,c,d,q1,q0) for q1 in range(d+1) for q0 in range(4-d))
            if value!=minima[a,b,c,d]:raise AssertionError(('compression',a,b,c,d,value,minima[a,b,c,d]))
            compressed[''.join(map(str,(a,b,c)))+':'+str(d)]=str(value)
    report={'status':'exact_universal_identity_verified','membership_patterns':patterns,
        'minimum_residual':str(min(minima.values())),'compressed_minima':compressed,
        'scope':'m=3; weak true-portfolio interface; only named terminal BR nodes required',
        'arbitrary_m_proved':False}
    Path(__file__).with_name('three_weak_portfolio_exact.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
