"""Attack aggregation after improved any-player exchange. Necessary rows, NOT SPE."""
from pathlib import Path
import importlib.util
import json
import argparse
import numpy as np
from scipy.optimize import linprog

SOURCE=Path(__file__).resolve().parents[2]/'R-31bbb6cfd6594bc8bb076db7b2950993'/'saturation'/'actual_ap_projection.py'
spec=importlib.util.spec_from_file_location('prior_projection',SOURCE)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def build(m=5):
    maxima=[[2,3,4,m],[4,m],[4,m],[m]]
    masks,covered,opt,rows,names=old.build(m,maxima)
    bits=((masks[None,:]>>np.arange(2*m)[:,None])&1).astype(float)
    count=bits[:m].sum(axis=0)
    size=bits
    coeff=(m-1)**2-m*m*(m-3)**2/(2*(3*m*m-7*m+2))
    newrows=[];newnames=[]
    rootCs=[2,3,4]+list(range(m,2*m))
    for i in range(m):
        u=np.divide(bits[i],count,out=np.zeros_like(count),where=count>0)
        for c in rootCs:
            for d in range(2*m):
                target=m*bits[d]*(1-bits[c])+bits[d]*bits[c]
                newrows.append(target+(coeff-1)*bits[c]-coeff*m*u)
                newnames.append(f'any_player_penultimate_exchange:{i}:{c}:{d}')
    rows=np.vstack([rows,newrows]);names+=newnames
    groups=np.array([[a+(1<<(m+t))-1 for t in range(m)] for a in range(1<<m)])
    rows=rows[:,groups].mean(axis=2)
    covered=covered[groups].mean(axis=1);opt=opt[groups].mean(axis=1)
    return rows,names,covered,opt,coeff


def run(m=5):
    rows,names,covered,opt,coeff=build(m)
    result=linprog(-opt,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=covered[None,:],b_eq=[1],bounds=(0,None),method='highs')
    data={'scope':'Necessary actual-path projection; NO SPE tree.','m':m,'status':result.status,'message':result.message,'exchange_coefficient':coeff,'rows':len(rows)}
    if result.success:
        data.update(optimum_float=-result.fun,atoms_float=[{'mask':a,'mass':float(x)} for a,x in enumerate(result.x) if x>1e-9],dual=[{'row':name,'weight':float(-x)} for name,x in zip(names,result.ineqlin.marginals) if x< -1e-9])
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output')
    args=parser.parse_args()
    data=run()
    if args.output:
        with Path(args.output).open('x') as output:
            output.write(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ['atoms_float','dual']}))
