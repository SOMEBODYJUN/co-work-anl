"""General full-atom actual-path projection with two-player true-reply cap.
Any SPE gives such incidence rows, but no converse or SPE is claimed.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'R-31bbb6cfd6594bc8bb076db7b2950993'/'saturation'/'actual_ap_projection.py'
SPEC=importlib.util.spec_from_file_location('old_projection',SOURCE)
OLD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(OLD)


def build(m=5,maxf=5,maxK=None):
    masks,covered,opt,rows,names=OLD.build(m)
    bits=((masks[None,:]>>np.arange(2*m)[:,None])&1).astype(float)
    count=bits[:m].sum(axis=0);i=m-2;b=bits[:i].sum(axis=0)
    u=np.divide(bits[i],count,out=np.zeros_like(count),where=count>0)
    fs=bits/(b+1)
    extra=[];extra_names=[]
    for a in range(2*m):
        extra.append(fs[a]-fs[maxf]);extra_names.append(f'maximum_f:{a}')
    for a in range(2*m):
        for c in range(a,2*m):
            g=bits[a]*bits[c]/((b+1)*(b+2))
            extra.append(fs[a]+fs[c]-g-u-fs[maxf]);extra_names.append(f'true_reply_cap:{a}:{c}')
    if maxK is not None:
        for a in range(2*m):
            extra.append(bits[a]-bits[maxK]);extra_names.append(f'maximum_size:{a}')
        coefficient=(m-1)**2-m*m*(m-3)**2/(2*(3*m*m-7*m+2))
        for i in range(m):
            u=np.divide(bits[i],count,out=np.zeros_like(count),where=count>0)
            for d in range(2*m):
                target=m*bits[d]*(1-bits[maxK])+bits[d]*bits[maxK]
                extra.append(target+(coefficient-1)*bits[maxK]-coefficient*m*u)
                extra_names.append(f'improved_exchange:{i}:{maxK}:{d}')
    return masks,np.vstack([rows,extra]),names+extra_names,covered,opt


def run(m,maxf,maxK):
    masks,rows,names,covered,opt=build(m,maxf,maxK)
    result=linprog(-opt,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=covered[None,:],b_eq=[1],bounds=(0,None),method='highs')
    report={'scope':'Full-atom necessary projection, NOT full SPE.','m':m,'maximizer_f_at_penultimate':maxf,'maximizer_size':maxK,'status':result.status,'message':result.message,'rows':len(rows)}
    if result.success:
        report.update(optimum_float=-result.fun,atoms_float=[{'mask':int(a),'mass':float(x)} for a,x in zip(masks,result.x) if x>1e-9],dual=[{'row':n,'weight':float(-v)} for n,v in zip(names,result.ineqlin.marginals) if v< -1e-9])
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--m',type=int,default=5);parser.add_argument('--with-maxK',action='store_true');parser.add_argument('--output');args=parser.parse_args()
    pairs=[(None,a) for a in range(args.m+1)]
    if args.with_maxK:
        pairs=[(c,f) for c in range(args.m+1) for f in range(args.m+1)]
        pairs.append((args.m,args.m+1))
    reports=[run(args.m,f,c) for c,f in pairs]
    if args.output:
        with Path(args.output).open('x') as output:output.write(json.dumps(reports,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in d.items() if k not in ['atoms_float','dual']} for d in reports],indent=2))
