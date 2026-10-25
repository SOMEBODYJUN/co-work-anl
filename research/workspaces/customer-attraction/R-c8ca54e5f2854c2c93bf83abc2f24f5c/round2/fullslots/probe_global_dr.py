"""Targeted test: all-layer monotone DR, exact marginal payoffs, SUMmin-full.
Finite box [0,4]^4 with coordinate saturation gives an infinite-domain DR potential.
"""
from itertools import product
import json
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
k=4;m=3;actual=(0,1,2);M=10

def addcount(q,a):r=list(q);r[a]+=1;return tuple(r)
def count(h):return tuple(h.count(a) for a in range(k))
cap=m+1
counts=list(product(range(cap+1),repeat=k))
vars=[];idx={};lb=[];ub=[];integer=[]
def var(key,lo=0,hi=4,i=0):
 idx[key]=len(vars);vars.append(key);lb.append(lo);ub.append(hi);integer.append(i);return idx[key]
for q in counts:var(('F',q),0,sum(q))
hist=[h for d in range(m+1) for h in product(range(k),repeat=d)]
for h in hist:
 var(('Q',h),0,1)
 for j in range(len(h)):var(('U',h,j),0,1)
 if len(h)<m:
  var(('V',h),0,1)
  for a in range(k):var(('Y',h,a),0,1,1)
for i in range(m):var(('R',i),0,1)
rows=[];rlo=[];rhi=[]
def row(d,lo=-np.inf,hi=np.inf):rows.append(d);rlo.append(lo);rhi.append(hi)
def eq(d,r=0):row(d,r,r)
def put(d,key,v):d[key]=d.get(key,0)+v
for q in counts:
 for a in range(k):
  if q[a]<cap:row({idx[('F',addcount(q,a))]:1,idx[('F',q)]:-1},lo=0,hi=1)
 for a in range(k):
  for b in range(a,k):
   if q[a]+1+(a==b)<=cap and q[b]+1<=cap:
    qa=addcount(q,a);qb=addcount(q,b);qab=addcount(qa,b)
    r={};put(r,idx[('F',qa)],1);put(r,idx[('F',qb)],1);put(r,idx[('F',q)],-1);put(r,idx[('F',qab)],-1);row(r,lo=0)
for h in hist:
 d=len(h)
 if d==m:
  q=count(h);r={idx[('Q',h)]:1};put(r,idx[('F',q)],1)
  for a in range(k):put(r,idx[('F',addcount(q,a))],-1/k)
  eq(r)
  for j in range(m):
   qminus=list(q);qminus[h[j]]-=1
   eq({idx[('U',h,j)]:1,idx[('F',q)]:-1,idx[('F',tuple(qminus))]:1})
 else:
  eq({idx[('Y',h,a)]:1 for a in range(k)},1)
  for a in range(k):
   child=h+(a,);y=idx[('Y',h,a)]
   row({idx[('V',h)]:1,idx[('U',child,d)]:-1},lo=0)
   row({idx[('V',h)]:1,idx[('U',child,d)]:-1,y:M},hi=M)
   for key1,key2 in [(('Q',h),('Q',child))]+[(('U',h,j),('U',child,j)) for j in range(d)]:
    x=idx[key1];z=idx[key2];row({x:1,z:-1,y:M},hi=M);row({z:1,x:-1,y:M},hi=M)
for i,a in enumerate(actual):
 h=actual[:i];eq({idx[('Y',h,a)]:1},1)
 for b in range(k):row({idx[('R',i)]:1,idx[('Q',h+(b,))]:-1},hi=0)
c=np.zeros(len(vars))
for i in range(m):c[idx[('R',i)]]=-1
q=count(actual)
for a in actual:
 c[idx[('F',q)]]+=1
 qm=list(q);qm[a]-=1;c[idx[('F',tuple(qm))]]-=1
A=lil_matrix((len(rows),len(vars)))
for n,r in enumerate(rows):
 for j,v in r.items():A[n,j]=v
res=milp(c,integrality=np.array(integer),bounds=Bounds(lb,ub),constraints=LinearConstraint(A.tocsr(),rlo,rhi),options={'time_limit':45,'mip_rel_gap':1e-9})
out={'status':int(res.status),'message':res.message,'gap_float':None if res.fun is None else -res.fun,'mip_dual_bound':getattr(res,'mip_dual_bound',None),'actual':actual,'k':k,'m':m}
if res.x is not None:
 out['potential']={','.join(map(str,q)):float(res.x[idx[('F',q)]]) for q in counts}
 out['strategy']={','.join(map(str,h)):int(np.argmax([res.x[idx[('Y',h,a)]] for a in range(k)])) for h in hist if len(h)<m}
print(json.dumps(out,indent=2))
