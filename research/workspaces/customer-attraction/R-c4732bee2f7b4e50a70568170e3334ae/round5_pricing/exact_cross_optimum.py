"""Exact final 717-row primal and full-universe dual, without modifying round4."""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
import sys,json,time,hashlib
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'round4_pricing'
sys.path.insert(0,str(OLD))
from cross_pair_pricing import CrossUniverse
from exact_cross_primal import evaluator
from exact_primal import verify_atom
from frozen_pair_reoptimization import fraction_solve

def run(terminal=False):
    t0=time.time();src=(HERE/'cg_terminal_cross_final.json') if terminal else (OLD/'cg_cross_pair_final.json');cg=json.loads(src.read_text());names=cg['row_names'];atoms=cg['atoms'];U=evaluator();cols=[];w=[];o=[]
    suffix='terminal_cross' if terminal else 'cross_pair'
    if terminal:
        from terminal_cross_pricing import TerminalUniverse
        U.__class__=TerminalUniverse;U.single=[(f'crossfinal:AB:{target}:{pos}{kind}',target,pos,kind) for target in ('AE','Sbranch') for pos in range(1,4 if target=='Sbranch' else 3) for kind in ('D','O')]
    for atom in atoms:
        bits,hs,d=verify_atom(atom);rr=U.atom_rows(atom);cols.append([rr[n] for n in names]);w.append(int(any(bits[:5])));o.append(int(d>0))
    mat=np.asarray(cols,dtype=float).T;out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs');assert out.success
    support=list(np.where(out.x>1e-8)[0]);active=list(np.where(abs(mat@out.x)<1e-7)[0]);eq=[[w[k] for k in support]]+[[cols[k][r] for k in support] for r in active]
    _,r,piv=qr(np.asarray(eq,dtype=float).T,pivoting=True,mode='economic');assert np.count_nonzero(abs(np.diag(r))>1e-8)==len(support)
    pick=list(piv[:len(support)]);mass=fraction_solve([eq[i] for i in pick],[int(i==0) for i in pick]);assert min(mass)>0
    O=sum(mass[j]*o[k] for j,k in enumerate(support));W=sum(mass[j]*w[k] for j,k in enumerate(support));assert W==1 and O>2
    sl={n:sum((mass[j]*cols[k][r] for j,k in enumerate(support)),F(0)) for r,n in enumerate(names)};assert min(sl.values())>=0
    primal={'scope':'Exact optimum primal of stated necessary-condition template; no full SPE or actual OPT claim','row_count':len(names),'welfare':str(W),'comparison_cover':str(O),'ratio_float':float(O),'atoms':[dict(atoms[k],exact_mass=str(m)) for k,m in zip(support,mass)],'slacks':{n:str(v) for n,v in sl.items()},'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
    (HERE/f'exact_optimum_primal_{suffix}.json').write_text(json.dumps(primal,indent=2)+'\n')
    pos=list(np.where(-out.ineqlin.marginals>1e-8)[0]);binding=list(np.where(out.lower.marginals<1e-7)[0]);eq=[[w[k]]+[-cols[k][r] for r in pos] for k in binding]
    _,r,piv=qr(np.asarray(eq,dtype=float).T,pivoting=True,mode='economic');assert np.count_nonzero(abs(np.diag(r))>1e-8)==1+len(pos)
    pick=list(piv[:1+len(pos)]);dual=fraction_solve([eq[j] for j in pick],[o[binding[j]] for j in pick]);beta=dual[0];lam=dual[1:];assert min(lam)>=0 and beta==O
    assert min(beta*w[k]-o[k]-sum((v*cols[k][r] for v,r in zip(lam,pos)),F(0)) for k in range(len(atoms)))>=0
    D=lcm(beta.denominator,*(v.denominator for v in lam));B=int(beta*D);ints=[0]*len(names)
    for r,v in zip(pos,lam):ints[r]=int(v*D)
    print(json.dumps({'beta':str(beta),'float':float(beta),'atoms':len(support),'multipliers':len(pos),'D_digits':len(str(D)),'recovery_seconds':time.time()-t0}),flush=True)
    U=TerminalUniverse() if terminal else CrossUniverse();minimum,negative,ncache=U.price(ints,B,batch=100,integer='object',objective_scale=D)
    report={'scope':'Exact full-universe dual of stated necessary-condition template; no full SPE or general-player theorem','row_count':len(names),'dual_beta':str(beta),'beta_float':float(beta),'common_denominator':str(D),'beta_numerator':str(B),'integer_multipliers':{names[r]:str(ints[r]) for r in pos},'multipliers':{names[r]:str(v) for r,v in zip(pos,lam)},'minimum_scaled_integer_residual':str(minimum),'full_pricing_nonnegative':minimum>=0,'fixed_masks':1024,'optimal_multiplicities':6,'third_histograms_per_family':792,'second_histograms':15504,'menu_overlap_corners_per_family':4,'score_contexts':ncache,'negative_columns':[dict(a,scaled_integer_residual=str(v)) for v,a in negative],'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'seconds':time.time()-t0}
    (HERE/f'exact_dual_{suffix}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('integer_multipliers','multipliers','negative_columns')},indent=2),flush=True)
if __name__=='__main__':run('--terminal' in sys.argv)
