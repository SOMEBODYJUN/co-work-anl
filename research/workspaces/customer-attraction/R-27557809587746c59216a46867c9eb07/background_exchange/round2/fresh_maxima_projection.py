"""Full membership projection with independent fresh f-max and size-max topics.
Every real SPE yields a feasible projection; converse is not asserted.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog


def build(m=5,with_size_max=True):
    labels=2*m+1+int(with_size_max)
    fmax=2*m;Kmax=2*m+1 if with_size_max else None
    masks=np.arange(1,1<<labels,dtype=np.int64)
    bits=((masks[None,:]>>np.arange(labels)[:,None])&1).astype(float)
    count=bits[:m].sum(axis=0)
    covered=(count>0).astype(float)
    comparison=(bits[m:2*m].sum(axis=0)>0).astype(float)
    rows=[];names=[]
    actualu=[]
    for i in range(m):
        k=m-i;b=bits[:i].sum(axis=0)
        u=np.divide(bits[i],count,out=np.zeros_like(count),where=count>0);actualu.append(u)
        sizes=bits/(b+k)
        for a in range(labels):
            rows.append(sizes[a]-u);names.append(f'floor:{i}:{a}')
        if k>=2:
            p=(k-1)*(m-1)+k*k/2
            for c in range(labels):
                for d in range(labels):
                    target=bits[d]*(bits[c]/(b+k)+(1-bits[c])/(b+1))
                    rows.append(target+(p-1)*sizes[c]-p*u);names.append(f'AP:{i}:{c}:{d}')
    i=m-2;b=bits[:i].sum(axis=0);fs=bits/(b+1)
    for a in range(labels):
        rows.append(fs[a]-fs[fmax]);names.append(f'fmax:{a}')
    for a in range(labels):
        for c in range(a,labels):
            g=bits[a]*bits[c]/((b+1)*(b+2))
            rows.append(fs[a]+fs[c]-g-actualu[m-2]-fs[fmax]);names.append(f'reply_cap:{a}:{c}')
    if with_size_max:
        for a in range(labels):
            rows.append(bits[a]-bits[Kmax]);names.append(f'sizemax:{a}')
        coefficient=(m-1)**2-m*m*(m-3)**2/(2*(3*m*m-7*m+2))
        for i in range(m):
            for d in range(labels):
                Q=m*bits[d]*(1-bits[Kmax])+bits[d]*bits[Kmax]
                rows.append(Q+(coefficient-1)*bits[Kmax]-coefficient*m*actualu[i]);names.append(f'improved_exchange:{i}:{d}')
    return masks,np.array(rows),names,covered,comparison


def run(m=5,with_size_max=True):
    masks,rows,names,covered,comparison=build(m,with_size_max)
    result=linprog(-comparison,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=covered[None,:],b_eq=[1],bounds=(0,None),method='highs')
    report={'scope':'Necessary full-membership projection with fresh independent extrema, NOT full SPE.','m':m,'with_size_max':with_size_max,'variables':len(masks),'rows':len(rows),'status':result.status,'message':result.message}
    if result.success:
        report.update(optimum_float=-result.fun,atoms_float=[{'mask':int(a),'mass':float(x)} for a,x in zip(masks,result.x) if x>1e-9],dual=[{'row':n,'weight':float(-v)} for n,v in zip(names,result.ineqlin.marginals) if v< -1e-9])
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--m',type=int,default=5);parser.add_argument('--without-size-max',action='store_true');parser.add_argument('--output');args=parser.parse_args()
    report=run(args.m,not args.without_size_max)
    if args.output:
        with Path(args.output).open('x') as output:output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['atoms_float','dual']},indent=2))
