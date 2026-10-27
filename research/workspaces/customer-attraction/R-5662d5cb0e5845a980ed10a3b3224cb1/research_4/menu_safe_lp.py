"""Diagnostics only: true aggregate menu plus simple safe deviations, m=6."""
from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import linprog

def rows(z,d,l,h):
    p=sum(z[:4]); a,b=z[4:]; c=sum(z)
    u=[F(v,c) if c else F(0) for v in z]
    D=(p+1)*(p+2)
    vals={
        'S':6*u[4]-F(d,p+1)+F(h,D),
        'Z':6*u[5]-F(l,p+a+1),
        'V':F(d*l-6*h,D),
        'last_opt':6*u[5]-F(d,p+a+1),
    }
    for j in range(6):
        vals['last_actual_%d'%j]=u[5]-F(z[j],p+a+1)
    for i in range(5):
        denom=sum(z[:i])+6-i
        vals['safe_opt_%d'%i]=6*u[i]-F(d,denom)
        for j in range(6):
            vals['safe_actual_%d_%d'%(i,j)]=u[i]-F(z[j],denom)
    return vals

def run(mode='all'):
    patterns=[]
    for z in product((0,1),repeat=6):
        if mode=='a_positive' and z[4] and not any(z[:4]): continue
        if mode=='a_twopositive' and z[4] and sum(z[:4])<2: continue
        for d in range(7):
            for l in range(7):
                for h in range(max(0,d+l-6),min(d,l)+1):
                    patterns.append((z,d,l,h))
    names=list(rows(*patterns[0]))
    A=np.array([[float(v) for v in rows(*q).values()] for q in patterns])
    t=np.array([2*int(any(q[0]))-int(q[1]>0) for q in patterns])
    sol=linprog(np.zeros(len(names)),A_ub=A,b_ub=t,bounds=(0,None),method='highs')
    print(mode,len(patterns),sol.message)
    if sol.success:
        print({n:str(F(float(v)).limit_denominator(1000000)) for n,v in zip(names,sol.x) if v>1e-8})
        print('min',float(np.min(t-A@sol.x)))
    else:
        # Maximize lower welfare at normalized optimum, the dual obstruction
        prim=linprog(np.array([2*int(any(q[0])) for q in patterns]),A_ub=-A.T,b_ub=np.zeros(len(names)),A_eq=np.array([[int(q[1]>0) for q in patterns]]),b_eq=[1],bounds=(0,None),method='highs')
        if prim.success:
            print('relaxed 2W',prim.fun)
            print([(patterns[k],str(F(float(v)).limit_denominator(100000))) for k,v in enumerate(prim.x) if v>1e-8])

if __name__=='__main__':
    for mode in ['all','a_positive','a_twopositive']: run(mode)
