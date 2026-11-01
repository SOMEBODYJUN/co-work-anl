#!/usr/bin/env python3
"""Independent standard-library full-type verifier for maxroot certificates.

Imports no discovery code or numerical libraries. All rows are multiplied by
L=lcm(1,...,n), enlarged to include the two-player tax denominators.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,math

HERE=Path(__file__).resolve().parent

def geometry(n,copies):
    paths=[list(range(n))];d=n
    for i in range(1,copies+1):
        paths.append(list(range(i))+[n-1]+list(range(d,d+n-i-1)))
        d+=n-i-1
    return paths,d

def coefficients(mask,n,copies,keys):
    paths,d=geometry(n,copies)
    b=[(mask>>i)&1 for i in range(d)]
    L=math.lcm(*range(1,n+1),*((p+1)*(p+2) for p in range(n-1)))
    # PAIR has multiplier n/2.
    L*=2
    def share(k,i):
        path=paths[k]
        return L//sum(b[j] for j in path) if b[path[i]] else 0
    rows=[]
    for key in keys:
        z=key.split(':')
        if z[0]=='CAP':
            rows.append(L*(b[0]-b[int(z[1])]))
        elif z[0]=='COPY':
            i=int(z[1]);assert 1<=i<=copies
            rows.append(share(0,i)-share(i,i))
        elif z[0]=='FLOOR':
            k,i,j=map(int,z[1:]);assert i>=(1 if k==0 else k+1)
            p=sum(b[h] for h in paths[k][:i])
            rows.append(share(k,i)-(L//(p+n-i) if b[j] else 0))
        elif z[0]=='PAIR':
            k=int(z[1]);p=sum(b[h] for h in paths[k][:-2])
            H=share(k,n-2)+share(k,n-1)+L*b[paths[k][-2]]//((p+1)*(p+2))
            assert n*H%2==0
            rows.append(n*H//2+L*p//(p+1))
        elif z[0]=='LAST':
            k=int(z[1]);p=sum(b[h] for h in paths[k][:-1])
            rows.append(n*share(k,n-1)+L*p//(p+1))
        else:raise ValueError(key)
    return b,L,share(0,0),rows

def verify(c):
    n,copies=c['n'],c['copies']
    paths,d=geometry(n,copies)
    assert c['paths']==paths and c['bits']==d
    B,C=F(c['B']),F(c['C']);assert B>0
    lam={k:F(v) for k,v in c['multipliers'].items()};assert all(v>=0 for v in lam.values())
    assert sum((v for k,v in lam.items() if k.startswith(('PAIR:','LAST:'))),F(0))==1
    D=math.lcm(*(v.denominator for v in lam.values()),B.denominator,C.denominator)
    weights=[int(v*D) for v in lam.values()]
    bn,cn=int(B*D),int(C*D)
    minimum=None;zeros=0
    perbase={}
    for mask in range(1<<d):
        b,L,v,rows=coefficients(mask,n,copies,lam)
        residual=bn*v+cn*L*b[0]-sum(w*g for w,g in zip(weights,rows))
        assert residual>=0,(mask,residual)
        if minimum is None or residual<minimum:minimum=residual
        zeros+=residual==0
        base=mask&((1<<n)-1)
        perbase[base]=min(perbase.get(base,residual),residual)
        # The O column has coefficient -1 on each PAIR/LAST and cancels.
        with_o=residual-D*L+sum(int(lam[k]*D)*L for k in lam if k.startswith(('PAIR:','LAST:')))
        assert with_o==residual
    return dict(n=n,copies=copies,types=1<<d,B=str(B),C=str(C),minimum_numerator=minimum,zero_types=zeros,integer_denominator=str(D*L),base_minima=perbase,verified=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=HERE/'exact_cuts.json');p.add_argument('--output',type=Path,default=HERE/'exact_check.json');a=p.parse_args()
    report=[verify(c) for c in json.loads(a.input.read_text())]
    a.output.write_text(json.dumps(report,indent=2));print(json.dumps([{k:v for k,v in r.items() if k!='base_minima'} for r in report],indent=2))
