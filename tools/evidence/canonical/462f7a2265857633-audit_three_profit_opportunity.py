#!/usr/bin/env python3
"""Exact audit of the three-remaining first-player opportunity certificate.

No discovery generator, solver, floating point or project game code is imported.
All 8^3 indexed menu memberships and all eight actual memberships are audited.
The infinite-background proof is the quadratic numerator with nonnegative
coefficients; p=3 is an extra implementation consistency check, not extrapolation.
"""
from fractions import Fraction as F
from itertools import product
import argparse,json
from pathlib import Path

WEIGHTS=(519972,117252,13770,56748,133446,11475,442,15623,14853,12558,31620,2295)
DEN=544124

def frac(num,den):return F(num,den) if num else F(0)

def data(p,a,b,c,seq):
    n=3;s=a+b+c;d=sum(t for t,q,r in seq)
    alpha=frac(a,p+s);beta=frac(b,p+s);gamma=frac(c,p+s)
    mids=[F(q,p+t+1+r) for t,q,r in seq]
    fins=[F(r,p+t+q+1) for t,q,r in seq]
    prices=[F(1,p+t+q+1) for t,q,r in seq]
    h=[mid+fin+F(q,(p+t+1)*(p+t+2))
       for mid,fin,(t,q,r) in zip(mids,fins,seq)]
    H0=beta+gamma+F(b,(p+a+1)*(p+a+2))
    def pair_branch(i,j,k,M,N):
        x,y=seq[j][M],seq[k][N];t=seq[i][0]
        return h[i]-F(x+y,p+t+1)+F(x*y,(p+t+1)*(p+t+2))
    def pair_actual(j,k,M,N):
        x,y=seq[j][M],seq[k][N]
        return H0-F(x+y,p+a+1)+F(x*y,(p+a+1)*(p+a+2))
    rows=[]
    # 0. Root deviates to T_i and follows the true Q_i,R_i continuation.
    rows.append(3*alpha-sum(F(t,p+1+q+r) for t,q,r in seq))
    # 1. Root deviates to each R_i; each client denominator is at most p+3.
    rows.append(3*alpha-sum(F(r,p+3) for t,q,r in seq))
    # 2. Terminal (T_i,Q_i), compared with all R_j.
    rows.append(sum(fins[i]-seq[j][2]*prices[i] for i in range(3) for j in range(3)))
    # 3. The same terminal sources compared with the actual final topic C.
    rows.append(sum(fins[i]-c*prices[i] for i in range(3)))
    # 4. Actual terminal at (A,B), compared with T_i.
    rows.append(3*gamma-F(d,p+a+b+1))
    # 5. Terminal (T_i,Q_i), compared with Q_j, i != j.
    rows.append(sum(fins[i]-seq[j][1]*prices[i] for i in range(3) for j in range(3) if i!=j))
    # 6. Two-player retained-overlap tax after T_i, queried T_j,T_k, distinct indices.
    rows.append(sum(pair_branch(i,j,k,0,0) for i,j,k in product(range(3),repeat=3) if len({i,j,k})==3))
    # 7. The same tail tax queried Q_j,R_j, j != i.
    rows.append(sum(pair_branch(i,j,j,1,2) for i,j in product(range(3),repeat=2) if i!=j))
    # 8,9. Actual tail tax after A, queried T_i,Q_j / T_i,R_j, i != j.
    rows.append(sum(pair_actual(i,j,0,1) for i,j in product(range(3),repeat=2) if i!=j))
    rows.append(sum(pair_actual(i,j,0,2) for i,j in product(range(3),repeat=2) if i!=j))
    # 10. Actual tail tax queried Q_i,R_i.
    rows.append(sum(pair_actual(i,i,1,2) for i in range(3)))
    # 11. Actual tail tax queried R_i,R_j, i != j.
    rows.append(sum(pair_actual(i,j,2,2) for i,j in product(range(3),repeat=2) if i!=j))
    residual=frac(s,p+s)+3*alpha-frac(d,p+d)-sum(F(w,DEN)*r for w,r in zip(WEIGHTS,rows))
    return rows,residual

def run():
    minima=[None,None,None];abc_min={};states=0;zero_counts=[0,0,0]
    patterns=list(product(range(2),repeat=3))
    for a,b,c in product(range(2),repeat=3):
        local=[None,None,None]
        for seq in product(patterns,repeat=3):
            vv=[]
            for p in range(4):
                _,r=data(p,a,b,c,seq);vv.append(r*(p+1)*(p+2)*(p+3))
            c0=vv[0];c2=(vv[2]-2*vv[1]+vv[0])/2;c1=vv[1]-vv[0]-c2
            coeff=(c0,c1,c2)
            assert vv[3]==c0+3*c1+9*c2,(a,b,c,seq,'not quadratic')
            assert min(coeff)>=0,(a,b,c,seq,coeff)
            for j,x in enumerate(coeff):
                minima[j]=x if minima[j] is None else min(minima[j],x)
                local[j]=x if local[j] is None else min(local[j],x)
                zero_counts[j]+=int(x==0)
            states+=1
        abc_min[''.join(map(str,(a,b,c)))]=list(map(str,local))
    return {'claim':'three-remaining first-player profit opportunity <= 3u_A',
            'status':'exact finite coefficient audit; infinite p follows from quadratic formula',
            'states':states,'coefficients':3*states,'common_multiplier_denominator':DEN,
            'multiplier_numerators':list(WEIGHTS),'min_coefficients':list(map(str,minima)),
            'zero_coefficient_counts':zero_counts,'abc_coefficient_minima':abc_min,
            'third_background_identity_checks':states,'negative_coefficients':0}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    result=run();text=json.dumps(result,indent=2,ensure_ascii=False)+'\n';print(text,end='')
    if args.output:
        with Path(args.output).open('x') as f:f.write(text)
