"""Small-base linear attack compiled into large Cartesian-product SPEs.

Root continuation mixtures and the actual mixture are fixed from a seed;
all last replies, second-stage floors and root budgets remain constrained.
No finite full SPE or negative claim follows until exact recovery succeeds.
"""
from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
sp=importlib.util.spec_from_file_location('cl',Path(__file__).with_name('cartesian_limit.py'));cl=importlib.util.module_from_spec(sp);sp.loader.exec_module(cl)

def cone(seed):
    k=seed['k'];d=(1<<k)-1;w=np.array(seed['weights']);inc=np.array([[(t>>a)&1 for a in range(k)] for t in range(1,1<<k)],np.int64)
    P={};V={}
    for z in product(range(k),repeat=3):
        load=inc[:,z].sum(axis=1);inv=np.array([1/x if x else 0 for x in load]);P[z]=inv[None,:]*inc.T;V[z]=P[z]@w
    last={};needed=set()
    for a,b in product(range(k),repeat=2):
        br=[c for c in range(k) if abs(V[a,b,c][c]-max(V[a,b,x][x] for x in range(k)))<1e-6]
        c=min(br,key=lambda x:(V[a,b,x][b],V[a,b,x][a]));last[a,b]=c;needed.add((a,b,c))
    rmix=seed['root_minimizers'];actual=[(tuple(z['terminal']),z['probability']) for z in seed['actual_mix']]
    for mix in rmix:
        for z,p in mix:needed.add(tuple(z))
    for z,p in actual:needed.add(z)
    rows=[]
    def add(wrow,ph=None,g=0,t=0):
        row=np.zeros(d+k+2);row[:d]=wrow
        if ph is not None:row[d:d+k]=ph
        row[-2]=g;row[-1]=t;rows.append(row)
    for a,b,c in needed:
        for x in range(k):add(P[a,b,x][x]-P[a,b,c][c])
    for (a,b),c in last.items():
        ph=np.zeros(k);ph[a]=-1;add(P[a,b,c][b],ph=ph)
    for a,mix in enumerate(rmix):
        first=sum(p*P[tuple(z)][z[0]] for z,p in mix);second=sum(p*P[tuple(z)][z[1]] for z,p in mix)
        ph=np.zeros(k);ph[a]=1;add(-second,ph=ph);add(first,g=-1)
    first=sum(p*P[z][z[0]] for z,p in actual);second=sum(p*P[z][z[1]] for z,p in actual);W=sum(p*sum(P[z][x] for x in z) for z,p in actual)
    ph=np.zeros(k)
    for z,p in actual:ph[z[0]]+=p
    add(-second,ph=ph);add(-first,g=1)
    p=np.array(seed['query']);B=list(combinations_with_replacement(range(k),2))
    for b in B:add(-(p@inc.T)/(1+inc[:,b].sum(axis=1)),t=1)
    obj=np.r_[W,np.zeros(k+1),-3.]
    eq=np.r_[np.ones(d),np.zeros(k+2)];bounds=[(0,None)]*(d+k+2);bounds[d-1]=(0,0)
    ans=linprog(obj,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[eq],b_eq=[1],bounds=bounds,method='highs')
    result=dict(status='numerical Cartesian-compiler cone only; no finite SPE certificate',success=ans.success,message=ans.message,k=k,rows=len(rows),seed=seed)
    if ans.success:result.update(gap=ans.fun,weights=ans.x[:d].tolist(),second_floors=ans.x[d:d+k].tolist(),root_cap=ans.x[-2],security_lower=ans.x[-1],actual_first_margin=float(first@ans.x[:d]-ans.x[-2]))
    return result

if __name__=='__main__':
    src=Path(__file__).with_name('cartesian_convexification_k4.json');seed=json.loads(src.read_text())['analysis'];z=cone(seed);Path(__file__).with_name('cartesian_compiler_cone_k4.json').write_text(json.dumps(z,indent=2)+'\n');print(json.dumps({k:v for k,v in z.items() if k not in ('seed','weights')}))
