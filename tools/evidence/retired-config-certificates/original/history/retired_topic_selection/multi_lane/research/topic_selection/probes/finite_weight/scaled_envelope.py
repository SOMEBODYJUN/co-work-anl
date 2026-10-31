"""Quasiconvex LP: alpha fixed, free heavy-player scaling h>0.
Weights are {1,2}; resource latency L**2. No randomization.
This is only a sufficient resource-separable approximate potential template.
"""
import json
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

def feasible(N,alpha,return_solution=False):
    states=[(k,l) for k in range(N+1) for l in range(N+1)]
    ix={s:i for i,s in enumerate(states)}
    h=len(states); edges=[]
    for k,l in states:
        L=k+2*l
        if k<N: edges.append((ix[k,l],ix[k+1,l],(L+1)**2,False))
        if l<N: edges.append((ix[k,l],ix[k,l+1],(L+2)**2,True))
    A=lil_matrix((2*len(edges),h+1)); b=np.zeros(2*len(edges))
    for j,(u,v,c,heavy) in enumerate(edges):
        A[2*j,u]=1; A[2*j,v]=-1
        A[2*j+1,u]=-1; A[2*j+1,v]=1
        if heavy:
            A[2*j,h]=c; A[2*j+1,h]=-alpha*c
        else:
            b[2*j]=-c; b[2*j+1]=alpha*c
    obj=np.zeros(h+1)
    bounds=[(None,None)]*(h+1);bounds[0]=(0,0);bounds[h]=(1e-8,None)
    r=linprog(obj,A_ub=A.tocsr(),b_ub=b,bounds=bounds,method='highs')
    if return_solution and r.success:
        return dict(N=N,alpha=alpha,h=r.x[h],h_fraction=str(Fraction(r.x[h]).limit_denominator(10**6)),F=r.x[:h].reshape((N+1,N+1)).tolist(),max_constraint_violation=float(max(A@r.x-b)))
    return r.success

def solve(N):
    lo=1.;hi=37/33
    for _ in range(42):
        mid=(lo+hi)/2
        if feasible(N,mid):hi=mid
        else:lo=mid
    r=feasible(N,hi+1e-7,True)
    r['alpha_bisection']=hi
    r['alpha_fraction_guess']=str(Fraction(hi).limit_denominator(10**6))
    return r

if __name__=='__main__':
    results=[]
    for N in [1,2,3,5,10,20,35]:
        r=solve(N);results.append(r)
        print({k:v for k,v in r.items() if k!='F'},flush=True)
    Path(__file__).with_name('scaled_envelope_results.json').write_text(json.dumps(results,indent=2))
