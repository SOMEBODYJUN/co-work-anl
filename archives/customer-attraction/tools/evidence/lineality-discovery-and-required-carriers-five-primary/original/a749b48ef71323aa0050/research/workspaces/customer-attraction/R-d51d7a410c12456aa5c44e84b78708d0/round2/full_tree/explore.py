from itertools import product
from fractions import Fraction as F
from math import comb
import json
import numpy as np
from scipy.optimize import linprog

def compositions(m,p):
 if p==1: yield (m,); return
 for k in range(m+1):
  for tail in compositions(m-k,p-1): yield (k,)+tail

def rank(rows):
 if not rows:return 0
 a=[list(map(F,r)) for r in rows]; r=0
 for j in range(len(a[0])):
  k=next((i for i in range(r,len(a)) if a[i][j]),None)
  if k is None: continue
  a[r],a[k]=a[k],a[r]
  x=a[r][j]; a[r]=[v/x for v in a[r]]
  for i in range(r+1,len(a)):
   if a[i][j]:
    x=a[i][j]; a[i]=[v-x*w for v,w in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r

def fv(q,a):
 p=len(q)
 return tuple(F(1,sum(q[j] for j in range(p) if b>>j&1)) if b>>a&1 else F(0) for b in range(1,1<<p))

def sccs(edges):
 vertices=set(v for e in edges for v in e); adj={v:[] for v in vertices}
 for u,v in edges:adj[u].append(v)
 ix=0; indices={}; low={}; st=[]; on=set(); out=[]
 def visit(v):
  nonlocal ix
  indices[v]=low[v]=ix;ix+=1;st.append(v);on.add(v)
  for w in adj[v]:
   if w not in indices:visit(w);low[v]=min(low[v],low[w])
   elif w in on:low[v]=min(low[v],indices[w])
  if low[v]==indices[v]:
   z=[]
   while True:
    w=st.pop();on.remove(w);z.append(w)
    if w==v:break
   out.append(z)
 for v in vertices:
  if v not in indices:visit(v)
 return out

def policy_data(m,p,policy):
 hist=[h for k in range(m) for h in product(range(p),repeat=k)]
 sigma=dict(zip(hist,policy)); counts={}
 for h in reversed(hist):
  t=h+(sigma[h],)
  counts[h]=counts[t] if len(t)<m else tuple(t.count(a) for a in range(p))
 edges=[];rows=[];witness=[]
 for h in hist:
  qa=counts[h];a=sigma[h]
  for b in range(p):
   t=h+(b,);qb=counts[t] if len(t)<m else tuple(t.count(j) for j in range(p))
   u=(qb,b);v=(qa,a)
   row=tuple(x-y for x,y in zip(fv(*v),fv(*u)))
   if any(row):edges.append((u,v));rows.append(row);witness.append((h,b))
 comps=sccs(edges); cix={v:i for i,c in enumerate(comps) for v in c}
 internal=[r for e,r in zip(edges,rows) if cix[e[0]]==cix[e[1]]]
 return hist,sigma,edges,rows,witness,comps,rank(internal)

def lineality_rank(rows):
 if not rows:return 0,[]
 A=np.array(rows,dtype=float).T; inds=[]
 for i,row in enumerate(rows):
  lp=linprog(np.zeros(len(rows)),A_eq=A,b_eq=-np.array(row,dtype=float),bounds=(0,None),method='highs')
  if lp.success:inds.append(i)
 return rank([rows[i] for i in inds]),inds

def extra_lineality():
 m,p=3,2
 for pol in product(range(p),repeat=sum(p**k for k in range(m))):
  h,s,e,r,w,c,hr=policy_data(m,p,pol)
  lr,inds=lineality_rank(r)
  if lr>hr:
   print('FOUND',dict(zip(map(str,h),pol)), 'SCC rank',hr,'image lin rank',lr)
   print('rows',[(w[i],list(map(str,r[i]))) for i in inds]);return
 print('none')

if __name__=='__main__':extra_lineality()
