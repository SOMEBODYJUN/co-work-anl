"""Necessary SPE rows / sufficient customerwise certificates for m=6.

Experimental only. Rows are true prefix deviation floors and the common
penultimate menu identity. Nonexistence of this certificate says nothing about
the desired game theorem.
"""
from itertools import product
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

def qfrac(n,d):
    return F(n,d) if n else F(0)

def states(min_a_load=0):
    for bits in product(range(2),repeat=6):
        p=sum(bits[:4]); a,b=bits[4:]
        if a and p<min_a_load: continue
        c=sum(bits); w=int(c>0)
        for d,l in product(range(7),repeat=2):
            o=int(d>0)
            g=6*qfrac(a,c)+qfrac(b,2*c)-F(d,p+1)-F(l,12*(p+a+1))+F(d*l,6*(p+1)*(p+2))
            vals=[g]; names=['G']
            for i in range(6):
                old=sum(bits[:i]); denom=6-i+old
                for j in range(6):
                    vals.append(qfrac(bits[i],c)-F(bits[j],denom))
                    names.append(f'floor:{i+1}:{j+1}')
                vals.append(6*qfrac(bits[i],c)-F(d,denom))
                names.append(f'optfloor:{i+1}')
            yield (bits,d,l),F(2*w-o),vals,names

def solve(min_a_load=0):
    ss=list(states(min_a_load))
    names=ss[0][3]
    mat=np.array([[float(v) for v in x[2]] for x in ss]); rhs=np.array([float(x[1]) for x in ss])
    lp=linprog(np.ones(len(names)),A_ub=mat,b_ub=rhs,bounds=(0,None),method='highs')
    out={'min_a_load':min_a_load,'status':lp.message,'states':len(ss)}
    if lp.success:
        coeff=[F(float(t)).limit_denominator(10**6) for t in lp.x]
        bad=[]; low=None
        for key,target,vs,_ in ss:
            r=target-sum(x*y for x,y in zip(coeff,vs))
            if low is None or r<low: low=r
            if r<0: bad.append((key,str(r)))
        out.update(coefficients={n:str(v) for n,v in zip(names,coeff) if v},minimum=str(low),negative_count=len(bad),negative_examples=bad[:5])
    return out

if __name__=='__main__':
    print(json.dumps([solve(j) for j in range(5)],indent=2))
