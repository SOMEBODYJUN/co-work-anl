"""Discovery-only attack on background first-pair security through sacrificial groups.
No general proof is claimed; a positive float must be recovered exactly.
"""
from functools import lru_cache
from itertools import product,combinations_with_replacement
from pathlib import Path
import json,math
import numpy as np
from scipy.optimize import linprog

n=5;k=9;group_size=3
masks=list(range(1,1<<k))
member=np.array([[(mask>>a)&1 for mask in masks] for a in range(k)],dtype=np.int64)
keys=[tuple(sorted((sum((mask>>a)&1 for a in range(g*3,g*3+3)) for g in range(3)))) for mask in masks]
classes=sorted(set(keys));cl=np.array([classes.index(z) for z in keys]);d=len(classes)
# Boolean potential F is zero except n-1 sets having maximum group count n-3.
F=np.zeros(1<<k,dtype=np.int64)
for mask in masks:
    counts=[sum((mask>>a)&1 for a in range(g*3,g*3+3)) for g in range(3)]
    if sum(counts)==n-1 and max(counts)==n-3:F[mask]=-1
c=F.copy()
for a in range(k):
    for mask in masks:
        if mask&(1<<a):c[mask]-=c[mask^(1<<a)]
z=np.array([0]+[((-1)**(mask.bit_count()+1))*mask.bit_count()*int(c[mask]) for mask in masks],dtype=np.int64)
x=z.copy()
for a in range(k):
    for mask in range(1<<k):
        if not mask&(1<<a):x[mask]-=x[mask|(1<<a)]
base=4*sum(abs(v) for v in x[1:])+1
w0=np.array([int(x[1+keys.index(key)])+base for key in classes],dtype=np.int64)
assert all(len(set(int(x[mask]) for mask,key0 in zip(masks,keys) if key0==key))==1 for key in classes)
scale=math.lcm(*range(1,n+1))
@lru_cache(None)
def row(a,q):
    den=np.array(q)@member
    raw=member[a]*(scale//np.maximum(den,1))
    return np.bincount(cl,weights=raw,minlength=d).astype(np.int64)

def build_policy(second_same=False):
    actions={};gamma=[]
    def pref(h):
        fresh=[a for a in range(k) if a not in h]
        if not fresh:return list(range(k))
        if len(h)==0:return [0]+[a for a in fresh if a!=0]
        if len(h)==1:
            goal=(h[0]//3 if second_same else (h[0]//3+1)%3)
        else:
            used={a//3 for a in h[:2]}
            goal=next((g for g in range(3) if g not in used),0)
        return [a for a in fresh if a//3==goal]+[a for a in fresh if a//3!=goal]+[a for a in range(k) if a in h]
    def walk(h):
        if len(h)==n:return tuple(h.count(a) for a in range(k))
        children=[walk(h+(a,)) for a in range(k)]
        vals=[int(row(a,children[a])@w0) for a in range(k)]
        best=max(vals)
        a=next(a for a in pref(h) if vals[a]==best)
        actions[h]=a;q=children[a]
        gamma.extend(row(a,q)-row(b,children[b]) for b in range(k) if b!=a)
        return q
    q=walk(())
    actual=();h=()
    while len(h)<n:h+=(actions[h],)
    gamma=np.unique(np.array(gamma),axis=0)/scale
    pair=(row(h[0],q)+row(h[1],q))/scale
    return actions,gamma,pair,h

backgrounds=[];beta=[]
for B in combinations_with_replacement(range(k),n-1):
    load=sum((member[a] for a in B),start=np.zeros(len(masks),dtype=np.int64))
    b=member.sum(axis=0)/k/(1+load)
    beta.append(np.bincount(cl,weights=b,minlength=d));backgrounds.append(B)
beta=np.unique(np.array(beta),axis=0)
reports=[]
for same in [False,True]:
    actions,G,pair,path=build_policy(same)
    A=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[-beta,np.ones(len(beta))]])
    out=linprog(np.r_[np.zeros(d),-2.],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[pair,0]],b_eq=[1],bounds=[(0,None)]*d+[(None,None)],method='highs')
    rec={'n':n,'k':k,'group_size':group_size,'status':out.status,'message':out.message,'second_same_group':same,'classes':classes,'actual_path':path,'unique_incentives':len(G),'unique_backgrounds':len(beta),'K':int(base),'initial_signed_classes':[int(v-base) for v in w0]}
    if out.success:rec.update(pair_payment=1.,ratio_2v=-out.fun,weights=out.x[:-1].tolist(),static_security=float(out.x[-1]),gamma_min=float(np.min(G@out.x[:-1])))
    reports.append(rec);print(json.dumps(rec),flush=True)
Path(__file__).with_name('group_pair_numerical.json').write_text(json.dumps({'scope':'Floating discovery only; no universal certificate','reports':reports},indent=2)+'\n')
