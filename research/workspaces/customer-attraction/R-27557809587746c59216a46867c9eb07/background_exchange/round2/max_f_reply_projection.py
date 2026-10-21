"""True two-player reply-cap condition added to old actual-path projection.
Necessary incidence conditions only: no full SPE tree is claimed.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('strengthened_global_projection',HERE.parent/'strengthened_global_projection.py')
PRIOR=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(PRIOR)


def build(maximizer,m=5):
    rows,names,covered,opt,coefficient=PRIOR.build(m)
    # Work in full atoms, then project each row to comparison-topic symmetry.
    masks=np.arange(1,1<<(2*m))
    bits=((masks[None,:]>>np.arange(2*m)[:,None])&1).astype(float)
    count=bits[:m].sum(axis=0)
    i=m-2;b=bits[:i].sum(axis=0)
    u=np.divide(bits[i],count,out=np.zeros_like(count),where=count>0)
    fs=bits/(b+1)
    extra=[];extra_names=[]
    for a in range(2*m):
        extra.append(fs[a]-fs[maximizer]);extra_names.append(f'maximum_f:{a}')
    for a in range(2*m):
        for c in range(a,2*m):
            g=bits[a]*bits[c]/((b+1)*(b+2))
            extra.append(fs[a]+fs[c]-g-u-fs[maximizer]);extra_names.append(f'true_reply_cap:{a}:{c}')
    groups=np.array([[a+(1<<(m+t))-1 for t in range(m)] for a in range(1<<m)])
    extra=np.asarray(extra)[:,groups].mean(axis=2)
    return np.vstack([rows,extra]),names+extra_names,covered,opt


def run(maximizer,m=5):
    rows,names,covered,opt=build(maximizer,m)
    result=linprog(-opt,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=covered[None,:],b_eq=[1],bounds=(0,None),method='highs')
    report={'scope':'Necessary projection only, NOT full SPE.','m':m,'maximizer_f_at_penultimate':maximizer,'status':result.status,'message':result.message,'rows':len(rows)}
    if result.success:
        report.update(optimum_float=-result.fun,atoms_float=[{'mask':a,'mass':float(x)} for a,x in enumerate(result.x) if x>1e-9],dual=[{'row':n,'weight':float(-v)} for n,v in zip(names,result.ineqlin.marginals) if v< -1e-9])
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    report=[run(a) for a in range(6)]
    if args.output:
        with Path(args.output).open('x') as output:output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in d.items() if k not in ['atoms_float','dual']} for d in report],indent=2))
