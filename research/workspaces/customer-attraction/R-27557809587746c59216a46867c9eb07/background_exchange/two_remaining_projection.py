"""Compare exact-terminal exchange with true penultimate three-comparison tax.
Retained overlap is universal on the comparison branch, but earlier branches absent.
"""
from pathlib import Path
import json
import argparse
import numpy as np
from scipy.optimize import linprog
from middle_floor_projection import build


def run(m,mode):
    masks,bits,ksize,v,excess,target,rows,names=build(m, 'all' if mode=='allfloor_tax' else 'lasttwo')
    rows=list(rows);names=list(names)
    q=bits[:m].sum(axis=0)
    b=bits[:m-2].sum(axis=0)
    up=np.divide(bits[m-2],q,out=np.zeros_like(q),where=q>0)
    ul=np.divide(bits[m-1],q,out=np.zeros_like(q),where=q>0)
    f=bits/(b+1)
    g=lambda a,c:bits[a]*bits[c]/((b+1)*(b+2))
    for a in range(m+1):
        for c in range(a,m+1):
            rows.append(f[a]+f[c]-g(a,c)-up-ul-g(m-2,m-2))
            names.append(f'two_remaining_retained:{a}:{c}')
    result=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[excess],b_eq=[1],bounds=(0,None),method='highs')
    data={'m':m,'mode':mode,'status':result.status,'message':result.message}
    if result.success:
        data.update(coefficient=-result.fun,positive_atoms=[{'mask':int(a),'mass':float(x)} for a,x in zip(masks,result.x) if x>1e-8],dual=[{'row':n,'weight':float(-z)} for n,z in zip(names,result.ineqlin.marginals) if z< -1e-8],K=float(ksize@result.x),v=float(v@result.x))
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output')
    args=parser.parse_args()
    data=[run(m,mode) for m in range(3,10) for mode in ['lasttwo_tax','allfloor_tax']]
    if args.output:
        with Path(args.output).open('x') as output:
            output.write(json.dumps(data,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in d.items() if k not in ['positive_atoms','dual','message']} for d in data],indent=2))
