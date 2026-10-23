import itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent

def search(k,r,strict_tail=False):
    masks=np.arange(1,1<<k)
    mem=np.array([[int(t>>a&1) for t in masks] for a in range(k)])
    opts=[list(itertools.combinations_with_replacement([j for j in range(k) if j!=i],r-1)) for i in range(k)]
    p=np.ones(k)/k;px=p@mem;best=(-1,None);total=0
    for tails in itertools.product(*opts):
        total+=1
        roots=[];follows=[];loads=[]
        for i,tail in enumerate(tails):
            load=mem[[i,*tail]].sum(axis=0)
            roots.append(mem[i]/np.maximum(load,1))
            follows.extend(mem[j]/np.maximum(load,1) for j in tail)
            loads.append(load)
        obj=np.mean([px/(1+load) for load in loads],axis=0)
        a=np.array([*roots,*[-x for x in follows]])
        rhs=np.array([1]*k+[-(1+1e-4 if strict_tail else 1)]*(k*(r-1)))
        lp=linprog(-obj,A_ub=a,b_ub=rhs,bounds=(0,None),method='highs')
        if lp.success and -lp.fun>best[0]+1e-8:
            best=(-lp.fun,dict(k=k,r=r,tails=tails,weights=lp.x.tolist(),obj=-lp.fun))
            if best[0]>1+1e-7:break
    return dict(total=total,best=best[0],witness=best[1])

if __name__=='__main__':
    out=search(4,3)
    print(json.dumps(out,indent=2))
    (HERE/'menu_probe.json').write_text(json.dumps(out,indent=2)+'\n')
