#!/usr/bin/env python3
"""Screen the full-support signed-column expansion of the three-player gadget.
Floating MILP is discovery only. Any positive candidate needs Fraction verification.
"""
from itertools import product
import json,time,argparse
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix


def basis(n,q,degrees):
    weights=np.asarray([q**i for i in range(n)])
    masks=[(0,)+tuple([1]*(n-1))]
    for j in range(1,n):
        m=[1]*n;m[j]=2;masks.append(tuple(m))
    states=list(product((0,1),repeat=n))
    terms=[(mask,k) for mask in masks for k in degrees]
    out=np.zeros((len(states),n,len(terms)))
    for st,s in enumerate(states):
        for t,(mask,k) in enumerate(terms):
            for f in (0,1):
                us=[i for i in range(n) if mask[i] and s[i]==((mask[i]-1)^f)]
                v=(sum(weights[i] for i in us)/sum(weights[i] for i in range(n) if mask[i]))**k
                for i in us:out[st,i,t]+=v
    rows=[]
    index={s:j for j,s in enumerate(states)}
    for st,s in enumerate(states):
        if s[0]:continue
        for i in range(n):
            alt=list(s);alt[i]^=1
            rows.append((out[st,i],out[index[tuple(alt)],i]))
    return weights,terms,np.array([r[0] for r in rows]),np.array([r[1] for r in rows])

def solve(n,q,d,alpha,limit):
    deg=sorted(set([0,1,2]+list(range(4,d+1,4))+[d]))
    w,terms,old,new=basis(n,q,deg)
    D=old-alpha*new;nr,m=D.shape
    # variables: basis coefficient simplex; witness per state/player; epsilon
    mat=lil_matrix((nr+nr//n+1,m+nr+1))
    low=np.full(mat.shape[0],-np.inf);high=np.full(mat.shape[0],np.inf)
    for row in range(nr):
        M=max(0.,-float(np.min(D[row])))+1
        mat[row,:m]=D[row];mat[row,m+row]=-M;mat[row,-1]=-1;low[row]=-M
    for st in range(nr//n):
        mat[nr+st,m+st*n:m+(st+1)*n]=1;low[nr+st]=1
    mat[-1,:m]=1;low[-1]=high[-1]=1
    c=np.zeros(m+nr+1);c[-1]=-1
    lower=np.zeros(m+nr+1);upper=np.ones(m+nr+1)
    integ=np.zeros(m+nr+1);integ[m:m+nr]=1
    start=time.time()
    res=milp(c,integrality=integ,bounds=Bounds(lower,upper),constraints=LinearConstraint(mat.tocsr(),low,high),options={'time_limit':limit,'mip_rel_gap':0.0001})
    ans={'n':n,'q':q,'d':d,'degrees':deg,'alpha':alpha,'status':res.message,'elapsed':time.time()-start,'margin': None if res.x is None else float(res.x[-1])}
    if res.x is not None and res.x[-1]>1e-8:
        ans['coefficients']=[{'mask':list(terms[j][0]),'degree':terms[j][1],'normalized_coefficient':float(res.x[j])} for j in range(m) if res.x[j]>1e-10]
        C=old@res.x[:m];N=new@res.x[:m];rat=np.divide(C,N,out=np.full_like(C,np.inf),where=N>0)
        ans['actual_minmax']=float(np.min(np.max(rat.reshape(-1,n),axis=1)))
    return ans
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4);ap.add_argument('--q',type=float,default=0.5);ap.add_argument('--d',type=int,default=8);ap.add_argument('--alpha',type=float,default=1.2);ap.add_argument('--seconds',type=float,default=20);a=ap.parse_args()
    print(json.dumps(solve(a.n,a.q,a.d,a.alpha,a.seconds),indent=2))
