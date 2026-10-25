"""Four genuine followers of a legal binary-background root: discovery only."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json,numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
PEER=ROOT/'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent'
sys.path.insert(0,str(PEER))
from binary_tail_pareto import coefficients as old,quotient as Q

def coefficients(p,eta,e):
    names,rows,target,V=old(p,eta,e)
    a,b,c,d,q,r,s=eta
    for pn,path,indices in [('actual',(a,b,c,d),range(4)),('off',(d,q,r,s),range(1,4))]:
        for i in indices:
            u=Q(path[i],p+sum(path));den=p+sum(path[:i])+4-i
            names.append(f'{pn}:{i}:legal-background');rows.append(u-Q(p,den))
        pref=p+sum(path[:2]);H=Q(path[2]+path[3],p+sum(path))+Q(path[2],(pref+1)*(pref+2))
        names.append(pn+':pair-opt-background')
        rows.append(4*H-Q(e*(1-p)+(4-e)*p,pref+1)-Q(2*e*p,pref+2))
        names.append(pn+':pair-background-background');rows.append(H-Q(2*p,pref+2))
        for label,x in zip('abcdqrs',eta):
            names.append(pn+':pair-background-'+label)
            rows.append(H-Q(p+x-2*p*x,pref+1)-Q(2*p*x,pref+2))
    return names,rows,target,V

def solve(beta0):
    cols=[];rhs=[]
    for p,eta,e in product(range(2),product(range(2),repeat=7),range(5)):
        names,rows,target,V=coefficients(p,eta,e)
        cols.append([float(x) for x in rows]+[-float(V) if p else 0.])
        rhs.append(float((beta0*V if not p else 0)-target))
    out=linprog([0.]*len(names)+[1.],A_ub=np.asarray(cols),b_ub=rhs,bounds=(0,None),method='highs')
    result={'scope':'floating all-type certificate discovery, not a proved coefficient','beta0':str(beta0),'success':out.success}
    if out.success:result.update(beta1=out.fun,multipliers={n:float(x) for n,x in zip(names,out.x[:-1]) if x>1e-9},min_residual=float(np.min(np.asarray(rhs)-np.asarray(cols)@out.x)))
    return result
if __name__=='__main__':
    results=[solve(x) for x in [F(2),F(1499,750),F(1999,1000),F(21,10)]]
    Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in x.items() if k!='multipliers'} for x in results],indent=2))
