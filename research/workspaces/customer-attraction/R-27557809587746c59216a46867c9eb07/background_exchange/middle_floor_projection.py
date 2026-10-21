"""Exact-incidence branch projection with intermediate all-topic floors.
Numerical necessary-condition experiment; not full SPE credibility.
"""
from pathlib import Path
import json
import argparse
import numpy as np
from scipy.optimize import linprog


def build(m, mode='all'):
    masks=np.arange(1,1<<(m+1))
    bits=((masks[None,:]>>np.arange(m+1)[:,None])&1).astype(float)
    q=bits[:m].sum(axis=0)
    ksize=bits[0]
    v=np.divide(bits[0],q,out=np.zeros_like(q),where=q>0)
    excess=m*v-ksize
    target=m*bits[m]*(1-bits[0])+bits[m]*bits[0]-ksize
    rows=[]; names=[]
    for j in range(1,m+1):
        rows.append(bits[j]-ksize); names.append(f'maximum:{j}')
    for i in range(1,m):
        if mode=='last' and i != m-1: continue
        if mode=='lasttwo' and i < m-2: continue
        u=np.divide(bits[i],q,out=np.zeros_like(q),where=q>0)
        b=bits[:i].sum(axis=0)
        for j in range(m+1):
            rows.append(bits[j]/(b+m-i)-u); names.append(f'floor:{i}:{j}')
    return masks,bits,ksize,v,excess,target,np.array(rows),names

def run(m,mode):
    masks,bits,ksize,v,excess,target,rows,names=build(m,mode)
    result=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[excess],b_eq=[1],bounds=(0,None),method='highs')
    data={'m':m,'mode':mode,'status':result.status,'message':result.message}
    if result.success:
        data.update(coefficient=-result.fun,positive_atoms=[{'mask':int(a),'mass':float(x)} for a,x in zip(masks,result.x) if x>1e-8],dual=[{'row':n,'weight':float(-z)} for n,z in zip(names,result.ineqlin.marginals) if z< -1e-8],K=float(ksize@result.x),v=float(v@result.x))
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output')
    args=parser.parse_args()
    data=[run(m,mode) for m in range(2,10) for mode in ['last','lasttwo','all']]
    if args.output:
        with Path(args.output).open('x') as output:
            output.write(json.dumps(data,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in d.items() if k not in ['positive_atoms','dual','message']} for d in data],indent=2))
