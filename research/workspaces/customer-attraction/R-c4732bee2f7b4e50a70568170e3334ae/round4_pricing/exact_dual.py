"""Recover exact dual and price the full histogram universe in integers."""
from fractions import Fraction as F
from math import lcm
import json,sys,time,hashlib
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from full_pricing import HERE,ROOT,ACTOR,Universe
from exact_primal import exact_rows
sys.path.insert(0,str(ACTOR/'round3_closure'))
from frozen_pair_reoptimization import fraction_solve

def run(overlap=1):
    t0=time.time();src=HERE/f'cg_overlap{overlap}_final.json';cg=json.loads(src.read_text());names=cg['row_names'];atoms=cg['atoms']
    columns=[];w=[];o=[]
    for atom in atoms:
        rr,ww,oo=exact_rows(atom,overlap);columns.append([rr[n] for n in names]);w.append(ww);o.append(oo)
    mat=np.asarray(columns,dtype=float).T
    out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs')
    assert out.success
    pos=list(np.where(-out.ineqlin.marginals>1e-8)[0]);binding=list(np.where(out.lower.marginals<1e-7)[0])
    eq=[[w[k]]+[-columns[k][r] for r in pos] for k in binding]
    _,r,piv=qr(np.asarray(eq,dtype=float).T,pivoting=True,mode='economic');assert np.count_nonzero(abs(np.diag(r))>1e-8)==1+len(pos)
    pick=list(piv[:1+len(pos)]);dual=fraction_solve([eq[j] for j in pick],[o[binding[j]] for j in pick]);beta=dual[0];lam=dual[1:]
    assert min(lam)>=0
    residual=[beta*w[k]-o[k]-sum((v*columns[k][r] for v,r in zip(lam,pos)),F(0)) for k in range(len(atoms))]
    assert min(residual)>=0
    D=lcm(beta.denominator,*(v.denominator for v in lam));B=int(beta*D);ints=[0]*len(names)
    for r,v in zip(pos,lam):ints[r]=int(v*D)
    print(json.dumps({'dual_basis_recovered':True,'beta':str(beta),'float':float(beta),'multipliers':len(pos),'denominator_digits':len(str(D)),'seconds':time.time()-t0}),flush=True)
    U=Universe(overlap)
    minimum,negative,ncache=U.price(ints,B,batch=100,integer='object',objective_scale=D)
    report={'scope':'Exact integer full-universe dual pricing of the stated557-row necessary-condition relaxation only; no full SPE or general-player theorem','overlap_subtraction':overlap,'row_count':557,'dual_beta':str(beta),'beta_float':float(beta),'common_denominator':str(D),'beta_numerator':str(B),'integer_multipliers':{names[r]:str(ints[r]) for r in pos},'multipliers':{names[r]:str(v) for r,v in zip(pos,lam)},'minimum_scaled_integer_residual':str(minimum),'full_pricing_nonnegative':minimum>=0,'fixed_masks':1024,'optimal_multiplicities':6,'third_histograms_per_family':792,'second_histograms':15504,'menu_overlap_corners_per_family':4,'score_contexts':ncache,'negative_columns':[dict(a,scaled_integer_residual=str(v)) for v,a in negative],'generated_columns':len(atoms),'source_cg_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'seconds':time.time()-t0}
    (HERE/f'exact_dual_overlap{overlap}.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('integer_multipliers','multipliers','negative_columns')},indent=2),flush=True)

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 1)
