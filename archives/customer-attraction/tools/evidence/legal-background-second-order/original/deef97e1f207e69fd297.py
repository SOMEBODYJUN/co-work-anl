#!/usr/bin/env python3
"""Exploratory necessary-row certificate, NOT a complete SPE search.

Try W + t*u_A >= sum min(1,d) for a three-player tail and real query
weights of total t>=1. The d/ell bilinear vertices suffice after exact
cancellation of the query/reply diagonal. p is integer background load.
All rows are from the SAME full-history strategy; only their aggregate
membership necessary conditions are imposed. Failed feasibility of this
dual template has no implication for the actual game.
"""
import argparse
import itertools
import json
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog

NAMES = ["KQ", "KR", "P", "Z", "S+V/t", "F", "J", "KB", "KC", "LCA", "LCB", "KT", "KL"]

def atom(p, bits, t, d, ell):
    a,b,c,q,r = bits
    s=a+b+c
    alpha=F(a,p+s) if s else F(0)
    gamma=F(c,p+s) if s else F(0)
    beta=F(b,p+s) if s else F(0)
    zc=F(c,p+c+q+r) if c else F(0)
    zr=F(r,p+c+q+r) if r else F(0)
    rows=[alpha-F(q,p+3), alpha-F(r,p+3),
          t*gamma-F(d,p+a+b+1), t*gamma-F(ell,p+a+b+1),
          t*beta-F(d,p+a+1)+F(d*ell,t*(p+a+1)*(p+a+2)),
          alpha-zc, t*zr-F(d,p+c+q+1),
          alpha-F(b,p+3), alpha-F(c,p+3),
          gamma-F(a,p+a+b+1), gamma-F(b,p+a+b+1),
          t*alpha-F(d,p+3),t*alpha-F(ell,p+3)]
    target=int(p+s>0)+t*alpha-min(1,d)
    return rows,target

def run(t,pmax):
    labels=[]; matrix=[]; target=[]
    for p,bits,d,ell in itertools.product(range(pmax+1),itertools.product(range(2),repeat=5),[0,1,t],[0,t]):
        row,y=atom(p,bits,t,d,ell)
        labels.append([p,list(bits),d,ell]);matrix.append(list(map(float,row)));target.append(float(y))
    res=linprog(np.ones(len(NAMES)),A_ub=matrix,b_ub=target,bounds=(0,None),method="highs")
    out={"query_weight":t,"pmax":pmax,"rows":len(labels),"status":int(res.status),"message":res.message}
    if res.success:
        coeff=[F(float(x)).limit_denominator(1000000) for x in res.x]
        slacks=[atom(p,tuple(bits),t,d,ell)[1]-sum(x*y for x,y in zip(coeff,atom(p,tuple(bits),t,d,ell)[0])) for p,bits,d,ell in labels]
        out.update(coefficients=dict(zip(NAMES,map(str,coeff))),exact_min_slack=str(min(slacks)),exact_pass=min(slacks)>=0)
    return out

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--max",type=int,default=12);args=parser.parse_args()
    print(json.dumps([run(t,max(0,t-3)) for t in range(3,args.max+1)],indent=2))
