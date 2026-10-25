"""Necessary local two-order three-tail SPE envelope; kernels are not SPEs."""
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

def build(mode='tail'):
    bits=np.array(list(product((0,1),repeat=8)),dtype=float)
    b=bits[:,0]+bits[:,1]
    rows=[]; names=[]
    v=[]; old=[]
    for leaf,ix in enumerate(((2,3,4),(5,6,7))):
        load=b+bits[:,ix].sum(axis=1)
        safe=np.maximum(load,1)
        v.append(bits[:,ix].sum(axis=1)/safe)
        old.append((bits[:,0]/safe,bits[:,1]/safe))
        for j,qcur in enumerate(ix):
            pref=b+bits[:,ix[:j]].sum(axis=1) if j else b
            rem=3-j
            cur=bits[:,qcur]/safe
            for q in range(8):
                floor=bits[:,q]/(pref+rem)
                rows.append(floor-cur); names.append(f'leaf{leaf}:node{j}:floor{q}')
        if mode in ('tax','tail'):
            pref=b+bits[:,ix[0]]
            h=(bits[:,ix[1]]+bits[:,ix[2]])/safe+bits[:,ix[1]]/((pref+1)*(pref+2))
            for qs in combinations_with_replacement(range(8),2):
                c=bits[:,qs].sum(axis=1)
                comp=np.divide(c,pref+c,out=np.zeros_like(c),where=pref+c>0)
                rows.append(comp-h); names.append(f'leaf{leaf}:tail2:{qs}')
        if mode=='tail':
            for qs in combinations_with_replacement(range(8),3):
                c=bits[:,qs].sum(axis=1)
                comp=np.divide(c,b+c,out=np.zeros_like(c),where=b+c>0)
                rows.append(comp-(5/3)*v[-1]); names.append(f'leaf{leaf}:tail3:{qs}')
    for q in range(8):
        rows.append(bits[:,q]-bits[:,1]); names.append(f'maxC:{q}')
    target=old[0][0]+old[1][1]-old[0][1]-old[1][0]
    return bits,np.array(rows),names,v,old,target

if __name__=='__main__':
    outputs=[]
    for mode in ('floor','tax','tail'):
        bits,rows,names,v,old,target=build(mode)
        r=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[v[0]+v[1]],b_eq=[1],bounds=(0,None),method='highs')
        o={'mode':mode,'status':'floating_necessary_relaxation_only','success':bool(r.success),'message':r.message,'types':len(bits),'rows':len(rows)}
        if r.success:
            o.update(value=float(-r.fun),dual_norm=float(-r.eqlin.marginals[0]),mults={n:float(-z) for n,z in zip(names,r.ineqlin.marginals) if abs(z)>1e-8},support=[{'bits':''.join(str(int(z)) for z in b),'mass':float(x)} for b,x in zip(bits,r.x) if x>1e-8])
        outputs.append(o)
    p=Path(__file__).with_suffix('.json'); p.write_text(json.dumps(outputs,indent=2))
    print(json.dumps([{k:v for k,v in o.items() if k not in ('mults','support','message')} for o in outputs],indent=2))
