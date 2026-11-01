import itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent

def lp_menu(tails,p,base=None):
    k=len(tails);r=len(tails[0])+1;masks=np.arange(1,1<<k)
    mem=np.array([[int(t>>a&1) for t in masks] for a in range(k)])
    bb=np.zeros(len(masks)) if base is None else np.array(base)@mem
    roots=[];follows=[]
    for i,tail in enumerate(tails):
        load=bb+mem[[i,*tail]].sum(axis=0)
        roots.append(mem[i]/np.maximum(load,1))
        follows.extend(mem[j]/np.maximum(load,1) for j in tail)
    px=np.array(p)@mem
    security=[px/(bb+1+mem[list(q)].sum(axis=0)) for q in itertools.combinations_with_replacement(range(k),r)]
    a=[np.r_[v,0] for v in roots]
    rhs=[1]*k
    for v in follows+security:a.append(np.r_[-v,1]);rhs.append(0)
    lp=linprog(np.r_[np.zeros(len(masks)),-1],A_ub=a,b_ub=rhs,bounds=(0,None),method='highs')
    return lp

if __name__=='__main__':
    tails=[(3,4)]*3+[(0,1)]*3
    out=lp_menu(tails,np.ones(6)/6)
    print(out.message,out.fun)
    if out.success:
        rec=dict(tails=tails,p=(np.ones(6)/6).tolist(),t=out.x[-1],weights=out.x[:-1].tolist())
        print(json.dumps(rec,indent=2));(HERE/'extra_one_menu_probe.json').write_text(json.dumps(rec,indent=2)+'\n')
