"""Targeted falsification of full-slot SUMmin for monotone quadratic DR potentials.
Not a CAG oracle or theorem; only a positive exact rational recheck is evidence.
"""
from itertools import product,combinations_with_replacement
import json
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix

k=4;m=3;actual=(0,1,2);M=20
pairs=list(combinations_with_replacement(range(k),2));pi={p:i for i,p in enumerate(pairs)}
vars=[];idx={};lb=[];ub=[];integrality=[]
def var(key,lo=-100,hi=100,integer=0):
    idx[key]=len(vars);vars.append(key);lb.append(lo);ub.append(hi);integrality.append(integer);return idx[key]
for a,b in pairs:var(('w',a,b),0,1)
def wi(a,b):return idx[('w',*sorted((a,b)))]
hist=[h for d in range(m+1) for h in product(range(k),repeat=d)]
for h in hist:
    var(('S',h),0,m)
    for j in range(len(h)):var(('C',h,j),0,m-1)
    if len(h)<m:
        var(('V',h),0,m-1)
        for a in range(k):var(('Y',h,a),0,1,1)
for i in range(m):var(('R',i),0,m)
rows=[];rlo=[];rhi=[]
def row(d,lo=-np.inf,hi=np.inf):rows.append(d);rlo.append(lo);rhi.append(hi)
def eq(d,r=0):row(d,r,r)
def add(d,key,v):d[key]=d.get(key,0)+v
for h in hist:
    d=len(h)
    if d==m:
        r={idx[('S',h)]:1}
        for a in h:
            for t in range(k):add(r,wi(t,a),-1/k)
        eq(r)
        for j,a in enumerate(h):
            r={idx[('C',h,j)]:1}
            for l,b in enumerate(h):
                if l!=j:add(r,wi(a,b),-1)
            eq(r)
    else:
        eq({idx[('Y',h,a)]:1 for a in range(k)},1)
        for a in range(k):
            child=h+(a,);y=idx[('Y',h,a)]
            # Chosen current action minimizes full terminal own interaction cost.
            row({idx[('V',h)]:1,idx[('C',child,d)]:-1},hi=0)
            row({idx[('C',child,d)]:1,idx[('V',h)]:-1,y:M},hi=M)
            # Past costs and final query collision score follow chosen child.
            for key1,key2 in [(('S',h),('S',child))]+[(('C',h,j),('C',child,j)) for j in range(d)]:
                x=idx[key1];z=idx[key2]
                row({x:1,z:-1,y:M},hi=M);row({z:1,x:-1,y:M},hi=M)
for i,a in enumerate(actual):
    h=actual[:i];eq({idx[('Y',h,a)]:1},1)
    for b in range(k):row({idx[('R',i)]:1,idx[('S',h+(b,))]:-1},lo=0)
c=np.zeros(len(vars))
for i in range(m):c[idx[('R',i)]]=1
for i in range(m):
    for j in range(i):c[wi(actual[i],actual[j])]-=2
A=lil_matrix((len(rows),len(vars)))
for n,r in enumerate(rows):
    for j,v in r.items():A[n,j]=v
res=milp(c,integrality=np.array(integrality),bounds=Bounds(lb,ub),constraints=LinearConstraint(A.tocsr(),rlo,rhi),options={'time_limit':45,'mip_rel_gap':1e-9})
out={'status':int(res.status),'message':res.message,'objective_gap_float':None if res.fun is None else -res.fun,'actual':actual,'k':k,'m':m}
if res.x is not None:
    out['weights']={f'{a},{b}':float(res.x[wi(a,b)]) for a,b in pairs}
    out['strategy']={','.join(map(str,h)):int(np.argmax([res.x[idx[('Y',h,a)]] for a in range(k)])) for h in hist if len(h)<m}
print(json.dumps(out,indent=2))
