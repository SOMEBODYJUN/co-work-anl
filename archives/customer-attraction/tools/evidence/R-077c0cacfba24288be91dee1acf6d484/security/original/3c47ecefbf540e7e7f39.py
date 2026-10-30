"""Floating discovery: cap true root payoff, maximize fractional-opponent minmax.
Fixed complete policy and p: w/t master LP with exact-oracle numerical convex cuts.
No positive witness is certified by this script.
"""
import itertools,json,argparse
import numpy as np
from scipy.optimize import linprog,minimize
P=argparse.ArgumentParser();P.add_argument('--background',type=float,default=0);P.add_argument('--rounds',type=int,default=15);P.add_argument('--seed',type=int,default=4);args=P.parse_args()
k=6;r=3;types=np.arange(1,2**k);X=((types[:,None]>>np.arange(k))&1).astype(float)
def term(h):
 h=tuple(h)
 if len(h)==0:return term((0,))
 if len(h)==1:return term((*h,3 if h[0]<3 else 0))
 if len(h)==2:
  grp=range(3) if h[1]<3 else range(3,6)
  return (*h,next(a for a in grp if a not in h))
 return h
def pay(z,i):return X[:,z[i]]/(args.background+X[:,list(z)].sum(axis=1).clip(min=1))
Gamma=[]
for l in range(r):
 for h in itertools.product(range(k),repeat=l):
  for a in range(k):Gamma.append(pay(term(h),l)-pay(term((*h,a)),l))
Gamma=np.array(Gamma);root=pay(term(()),0)
def oracle(w,p,q0=None):
 alpha=X@p
 def fg(q):
  den=args.background+1+(r-1)*(X@q);val=np.sum(w*alpha/den);grad=-(r-1)*(X.T@(w*alpha/den**2));return val,grad
 sol=minimize(lambda q:fg(q),np.ones(k)/k if q0 is None else q0,jac=True,bounds=[(0,1)]*k,constraints={'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(k)},method='SLSQP',options={'maxiter':500,'ftol':1e-12})
 return sol.fun,sol.x,sol.success
rng=np.random.default_rng(args.seed);best=None
for outer in range(args.rounds):
 p=np.array([10,10,21,10,10,21])/82 if outer==0 else rng.dirichlet(np.ones(k))
 qs=[np.eye(k)[i] for i in range(k)]+[np.ones(k)/k]
 for it in range(120):
  beta=np.array([(X@p)/(args.background+1+(r-1)*(X@q)) for q in qs])
  A=np.vstack([np.c_[-Gamma,np.zeros(len(Gamma))],np.c_[-beta,np.ones(len(beta))]])
  sol=linprog(np.r_[np.zeros(len(types)),-1],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[root,0]],b_eq=[1],bounds=[(0,args.background+3)]*(len(types)-1)+[(0,0),(0,args.background+3)],method='highs')
  if not sol.success:raise RuntimeError(sol.message)
  w=sol.x[:-1];ub=sol.x[-1];v,q,ok=oracle(w,p,qs[-1]);qs.append(q)
  if best is None or v>best['value']:
   best={'value':float(v),'upper':float(ub),'p':p.tolist(),'q':q.tolist(),'w':{int(mask):float(ww) for mask,ww in zip(types,w) if ww>1e-8},'outer':outer,'iterations':it,'root':float(root@w),'minGamma':float(np.min(Gamma@w))}
  if ub-v<1e-8:break
print(json.dumps(best,indent=2))
