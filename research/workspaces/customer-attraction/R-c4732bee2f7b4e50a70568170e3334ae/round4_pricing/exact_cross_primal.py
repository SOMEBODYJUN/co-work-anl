"""Exact feasible primal recovery for the717-row additive cross-pair system."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json,time
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import qr
from full_pricing import HERE
from cross_pair_pricing import CrossUniverse,PARTITIONS
from exact_primal import verify_atom
from frozen_pair_reoptimization import fraction_solve

def evaluator():
    U=CrossUniverse.__new__(CrossUniverse);U.overlap=1;U.ty={k:np.asarray(list(product((0,1),repeat=k)),dtype=int) for k in (3,4)};U.cross=[]
    for source in ('AB','AE'):
        for target in ('AB','AE','Sbranch'):
            if source==target:continue
            for u,v in combinations_with_replacement(range(4 if target=='Sbranch' else 3),2):
                for orb in PARTITIONS:U.cross.append((f'crosspair:{source}:{target}:{u}{v}:{orb}',source,target,u,v,orb))
    return U

def run():
    t0=time.time();src=json.loads((HERE/'cg_cross_pair.json').read_text());names=src['row_names'];atoms=src['atoms'];U=evaluator();cols=[];w=[];o=[]
    for a in atoms:
        bits,hs,d=verify_atom(a);rr=U.atom_rows(a);assert len(rr)==717 and set(rr)==set(names)
        cols.append([rr[n] for n in names]);w.append(int(any(bits[:5])));o.append(int(d>0))
    mat=np.asarray(cols,dtype=float).T;lp=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success and -lp.fun>2
    support=list(np.where(lp.x>1e-8)[0]);active=list(np.where(abs(mat@lp.x)<1e-7)[0]);eq=[[w[k] for k in support]]+[[cols[k][r] for k in support] for r in active]
    _,r,piv=qr(np.asarray(eq,dtype=float).T,pivoting=True,mode='economic');assert np.count_nonzero(abs(np.diag(r))>1e-8)==len(support)
    pick=list(piv[:len(support)]);mass=fraction_solve([eq[i] for i in pick],[int(i==0) for i in pick]);assert min(mass)>0
    W=sum(mass[j]*w[k] for j,k in enumerate(support));O=sum(mass[j]*o[k] for j,k in enumerate(support));assert W==1 and O>2
    sl={n:sum((mass[j]*cols[k][r] for j,k in enumerate(support)),F(0)) for r,n in enumerate(names)};assert min(sl.values())>=0
    report={'scope':'Exact717-row necessary-condition feasible point only; no SPE or trueOPT claim','row_count':717,'welfare':'1','comparison_cover':str(O),'gap_above_two':str(O-2),'ratio_float':float(O),'positive_atoms':len(support),'atoms':[dict(atoms[k],exact_mass=str(m)) for k,m in zip(support,mass)],'slacks':{n:str(v) for n,v in sl.items()},'minimum_primal_slack':str(min(sl.values())),'source_point_count':len(atoms),'seconds':time.time()-t0}
    (HERE/'exact_primal_cross_pair.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('atoms','slacks')},indent=2),flush=True)

if __name__=='__main__':run()
