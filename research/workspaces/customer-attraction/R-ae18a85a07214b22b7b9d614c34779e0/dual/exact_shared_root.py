"""Exact recovery of the earlier shared-K floating certificate.

Author-layer certificate; independent active-row pricing is separate. Does not
claim HALF(5), nor a strategy realization of the relaxation primal point.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import hashlib,json,sys,time
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
SRC=ROOT/'research/workspaces/customer-attraction/R-a27734a8bba345cbb5fad186c120d0bf'
sys.path.insert(0,str(SRC))
import root_shared_max_pricing as old
sys.path.insert(0,str(old.source.old.ACTOR/'round3_closure'))
from frozen_pair_reoptimization import fraction_solve

def run():
    begin=time.monotonic();src=SRC/'root_shared_max_copy_cg.json';cg=json.loads(src.read_text());names=cg['row_names'];atoms=cg['atoms']
    U=old.source.Universe();assert names==U.names
    columns=[];w=[];o=[]
    for atom in atoms:
        rows=U.atom_rows(atom);columns.append([rows[n] for n in names]);w.append(int(any(map(int,atom['bits'][:5]))));o.append(int(any(atom['AB_hist'][4:])))
    kc=[F(old.KCO.get(n,0)) for n in names];columns.append(kc);w.append(0);o.append(0)
    mat=np.asarray(columns,dtype=float).T
    out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs');assert out.success
    pos=list(np.where(-out.ineqlin.marginals>1e-10)[0]);binding=list(np.where(out.lower.marginals<1e-7)[0])
    eq=[[F(w[k])]+[-columns[k][r] for r in pos] for k in binding]
    _,r,piv=qr(np.asarray(eq,dtype=float).T,pivoting=True,mode='economic');rank=np.count_nonzero(abs(np.diag(r))>1e-8);assert rank==1+len(pos),(rank,len(pos))
    pick=list(piv[:1+len(pos)]);dual=fraction_solve([eq[j] for j in pick],[F(o[binding[j]]) for j in pick]);beta=dual[0];lam=dual[1:];assert min(lam)>=0
    residual=[beta*w[k]-o[k]-sum((v*columns[k][r] for v,r in zip(lam,pos)),F()) for k in range(len(columns))];assert min(residual)>=0
    D=lcm(beta.denominator,*(v.denominator for v in lam));B=int(beta*D);ints=[0]*len(names)
    for r,v in zip(pos,lam):ints[r]=int(v*D)
    print(json.dumps({'recovered':True,'beta':str(beta),'float':float(beta),'multipliers':len(pos),'denominator_digits':len(str(D)),'seconds':time.monotonic()-begin}),flush=True)
    minimum,negative,ncache=U.price(ints,B,batch=20,integer='object',objective_scale=D)
    k_res=-sum((F(v)*c for v,c in zip(ints,kc)),F());assert k_res>=0
    report={'scope':'Exact author-layer full-type shared-K dual certificate, not HALF(5) or any SPE realization','dual_beta':str(beta),'beta_float':float(beta),'common_denominator':str(D),'beta_numerator':str(B),'integer_multipliers':{names[r]:str(ints[r]) for r in pos},'multipliers':{names[r]:str(v) for r,v in zip(pos,lam)},'minimum_scaled_integer_residual':str(minimum),'K_dual_residual':str(k_res),'full_pricing_nonnegative':minimum>=0,'fixed_masks':1024,'optimal_multiplicities':6,'third_histograms_per_family':792,'second_histograms':15504,'score_contexts':ncache,'negative_columns':[dict(a,scaled_integer_residual=str(v)) for v,a in negative],'generated_columns':len(atoms),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_path':str(src.relative_to(ROOT)),'seconds':time.monotonic()-begin}
    (HERE/'exact_shared_root.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('integer_multipliers','multipliers','negative_columns')},indent=2),flush=True)
    assert minimum>=0

if __name__=='__main__':run()
