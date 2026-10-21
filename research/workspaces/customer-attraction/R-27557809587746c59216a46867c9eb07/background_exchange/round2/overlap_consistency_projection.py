"""Add a true-reply three-theme overlap consistency row to fresh-extrema LP.
Necessary projection only; no full SPE tree or exact LP optimum asserted.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog
from fresh_maxima_projection import build


def run(m=5):
    masks,rows,names,covered,opt=build(m,True)
    labels=2*m+2
    bits=((masks[None,:]>>np.arange(labels)[:,None])&1).astype(float)
    count=bits[:m].sum(axis=0)
    b=bits[:m-2].sum(axis=0);f=bits/(b+1)
    u=np.divide(bits[m-2],count,out=np.zeros_like(count),where=count>0)
    v=np.divide(bits[m-1],count,out=np.zeros_like(count),where=count>0)
    g=lambda a,c:bits[a]*bits[c]/((b+1)*(b+2))
    extra=[];extra_names=[]
    for T in range(labels):
        for S in range(labels):
            extra.append(3*f[T]+f[S]-g(T,S)-3*u-2*v-2*g(m-2,T))
            extra_names.append(f'true_reply_overlap:{T}:{S}')
    for T in range(labels):
        extra.append(2*f[T]-2*u-v-g(m-2,T))
        extra_names.append(f'true_reply_overlap_beta2:{T}')
    rows=np.vstack([rows,extra]);names+=extra_names
    result=linprog(-opt,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=covered[None,:],b_eq=[1],bounds=(0,None),method='highs')
    report={'scope':'Necessary full-membership projection with true-reply overlap, NOT SPE.','m':m,'status':result.status,'message':result.message,'variables':len(masks),'rows':len(rows)}
    if result.success:
        report.update(optimum_float=-result.fun,atoms_float=[{'mask':int(a),'mass':float(x)} for a,x in zip(masks,result.x) if x>1e-9],dual=[{'row':n,'weight':float(-v)} for n,v in zip(names,result.ineqlin.marginals) if v< -1e-9])
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--m',type=int,default=5);parser.add_argument('--output');args=parser.parse_args()
    report=run(args.m)
    if args.output:
        with Path(args.output).open('x') as output:output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['atoms_float','dual']},indent=2))
