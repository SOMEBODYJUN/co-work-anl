"""Floating LP attack on existential safety-optimal first-pair iid bridge.
Fixed p,Q at the original34 saddle; positivity/Q-rank must be checked exactly.
"""
from functools import lru_cache
from itertools import product,combinations_with_replacement
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

n=3;k=6;d=(1<<k)-1
M=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)],dtype=int)
@lru_cache(None)
def row(a,z):return M[a]/np.maximum(sum(M[b] for b in z),1)
def policy(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    return next(a for a in range((h[1]//3)*3,(h[1]//3)*3+3) if a not in h)
def terminal(h):
    while len(h)<n:h+=(policy(h),)
    return h
G=np.unique(np.array([row(policy(h),terminal(h))-row(a,terminal(h+(a,))) for s in range(n) for h in product(range(k),repeat=s) for a in range(k)]),axis=0)
z=terminal(());pair=row(z[0],z)+row(z[1],z)
p=np.array([10,10,21,10,10,21])/82
Bs=list(combinations_with_replacement(range(k),n-1))
U=np.array([M/(1+sum(M[b] for b in B)) for B in Bs])
beta=U.transpose(0,2,1)@p
Q=np.array([([23,9,9,23,9,9][[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)].index(B)]/82) if B in [(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)] else 0 for B in Bs])
cap=np.tensordot(Q,U,axes=1)
t=p@M
P=np.array([2*t*((1-t)/(1+M[b])+t/(2+M[b])) for b in range(k)])
# Variables w_1...w_d, value v, pair-iid lower bound s.
A=np.vstack([np.c_[-G,np.zeros((len(G),2))],np.c_[-beta,np.ones(len(beta)),np.zeros(len(beta))],np.c_[cap,-np.ones(k),np.zeros(k)],np.c_[-P,np.zeros(k),np.ones(k)]])
out=linprog(np.r_[np.zeros(d+1),-1.],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[pair,0.,0.]],b_eq=[1],bounds=[(0,None)]*d+[(None,None),(None,None)],method='highs')
rec={'status':out.status,'message':out.message,'scope':'Floating discovery only; fixed original34 p and Q'}
if out.success:
    w=out.x[:d];v=out.x[d];s=out.x[d+1]
    rec.update(P_pair_ratio=float(s),security=float(v),pair=1.,weights={str(i+1):float(x) for i,x in enumerate(w) if x>1e-8},min_gamma=float(np.min(G@w)),positive_gap=bool(s>1+1e-7),p=p.tolist(),Q=Q.tolist())
    active=U@w
    mat=np.c_[active[Q>0],-np.ones(sum(Q>0))]
    rec['active_safety_rank']=int(np.linalg.matrix_rank(np.vstack([mat,np.r_[np.ones(k),0.]])))
Path(__file__).with_name('first_pair_iid_numerical.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)
