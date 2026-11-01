#!/usr/bin/env python3
"""Discover exact Farkas witnesses for the five failed route LPs.

This uses SciPy only to locate a small support.  The resulting witnesses are
written as exact rational coefficients and checked by audit_route_obstruction.py.
The rows are the legal seven-maxima n=6 mixed-floor, final BR and two-tail-tax
slacks; target is W-(U-|X_6|)/2 (six-max optimum omits maximal label 6).
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

N,S=6,7
FAILED=[(0,0,0,0,0,0),(0,0,0,0,1,0),(0,0,1,0,1,0),(0,1,0,0,1,0),(0,1,1,1,0,1)]

def rgs(length,labels):
 def rec(pre,hi):
  if len(pre)==length:
   yield tuple(pre);return
  for j in range(min(hi+1,labels-1)+1): yield from rec(pre+[j],max(hi,j))
 yield from rec([0],0)

def floors(n,s):
 A=[Q(n+t,(t+1)*(s*n-(s-2)*t)) for t in range(n-1)]+[Q(1,n+s-1)]
 B=[Q(2,s*n-(s-2)*t) for t in range(n-1)]+[Q(n+1,n*(n+s-1))]
 return [min(A[t:]) for t in range(n)],[min(B[t:]) for t in range(n)]

def rows(inc,true):
 count=true.bit_count(); pay=[Q((true>>t)&1,count) if count else Q(0) for t in range(N)]
 alpha,beta=floors(N,S); bits=inc.bit_count()
 mixed=[pay[t]-(Q(1,N) if bits==S else alpha[t] if bits==1 else beta[t]) for t in range(N)]
 prior=(true&((1<<(N-1))-1)).bit_count()
 last=[pay[-1]-Q((inc>>j)&1,prior+1) for j in range(S)]
 pref=(true&((1<<(N-2))-1)).bit_count(); suff=pay[-2]+pay[-1]
 tax=Q((true>>(N-2))&1,(pref+1)*(pref+2)); pair=[]
 for a,b in combinations_with_replacement(range(S),2):
  c=((inc>>a)&1)+((inc>>b)&1)
  pair.append(suff+tax-(Q(c,pref+c) if c else Q(0)))
 return mixed+last+pair

def columns(route):
 final=route[-1]; out=[]
 for inc in range(1,1<<S):
  req=(inc>>final)&1; elig=sum(1<<t for t,j in enumerate(route) if inc>>j&1); tr=elig
  while True:
   if ((tr>>(N-1))&1)==req:
    target=Q(int(tr!=0))-Q(1,2)+Q(int(inc==(1<<6)),2)
    out.append((inc,tr,target,rows(inc,tr)))
   if tr==0: break
   tr=(tr-1)&elig
 return out

def solve(route):
 cols=columns(route); A=np.array([[float(v) for v in row] for _,_,_,row in cols]); b=np.array([float(t) for _,_,t,_ in cols])
 # Farkas y>=0, A^T y>=0, sum y=1, minimize b'y.
 lp=linprog(b,A_ub=-A.T,b_ub=np.zeros(A.shape[1]),A_eq=np.ones((1,len(cols))),b_eq=[1],bounds=[(0,None)]*len(cols),method='highs')
 if not lp.success or lp.fun >= -1e-9: raise RuntimeError((route,lp.message,lp.fun if lp.success else None))
 ys=lp.x; support=[i for i,v in enumerate(ys) if v>1e-8]; az=A.T@ys; zero=[j for j,v in enumerate(az) if abs(v)<1e-8]
 M=[[cols[i][3][j] for i in support] for j in zero]+[[Q(1) for _ in support]]; rhs=[Q(0)]*len(zero)+[Q(1)]
 # Fraction Gauss-Jordan. Use all zero-column equations plus normalization.
 aug=[M[i][:]+[rhs[i]] for i in range(len(M))]; row=0; piv=[]
 for c in range(len(support)):
  p=next((i for i in range(row,len(aug)) if aug[i][c]),None)
  if p is None: continue
  aug[row],aug[p]=aug[p],aug[row]; q=aug[row][c]; aug[row]=[x/q for x in aug[row]]
  for i in range(len(aug)):
   if i!=row and aug[i][c]:
    q=aug[i][c]; aug[i]=[aug[i][j]-q*aug[row][j] for j in range(len(aug[0]))]
  piv.append(c);row+=1
 if row != len(support): raise RuntimeError(('rank',route,row,len(support)))
 sol=[Q(0)]*len(support)
 for i,c in enumerate(piv): sol[c]=aug[i][-1]
 y=[Q(0)]*len(cols)
 for i,v in zip(support,sol): y[i]=v
 at=[sum(y[r]*cols[r][3][j] for r in range(len(cols))) for j in range(A.shape[1])]
 obj=sum(y[i]*cols[i][2] for i in range(len(cols)))
 if min(at)<0 or obj>=0: raise RuntimeError(('exact-check',route,min(at),obj))
 support_data=[]
 for i,v in zip(support,sol):
  inc,tr,tar,_=cols[i]
  support_data.append({'column':i,'incidence':inc,'true_membership':tr,'weight_num':v.numerator,'weight_den':v.denominator,'target':str(tar)})
 return {'route':list(route),'column_count':len(cols),'support':support_data,'objective':str(obj),'minimum_AT':str(min(at)),'row_count':41}

out={'scope':'Exact Farkas obstructions to the specified mixed-floor + final-BR + two-tail-tax certificate family, route-conditioned, for seven maxima and six providers. These do not imply a Q-CAG-HALF-6 counterexample.','target':'W-(U-|X_{6}|)/2; label 6 is omitted from the six-maximal comparison portfolio.','rows':'M_t (seven-maxima mixed private/shared/core suffix floors), L_j (j=0..6), T_jk (all 28 unordered pairs including repeats).','routes':[]}
for route in FAILED:
 print('solving',route,flush=True); out['routes'].append(solve(route))
Path(__file__).with_name('farkas_witnesses.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
