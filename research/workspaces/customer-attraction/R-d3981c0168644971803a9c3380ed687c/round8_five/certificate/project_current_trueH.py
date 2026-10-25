"""Adapt the complete actual-HQR projection oracle to a new retained-row point.

Every source is reconstructed with its own exact row evaluator. A strict
projected cut is restored rationally. No floating optimum is a certificate.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
import weighted_true_branch as tb
sys.path.insert(0,str(tb.cm.HERE.parent/'maxroot'))
import trueH_payment_pricing as tp
from exact_cross_primal import evaluator
from frozen_pair_reoptimization import fraction_solve


def restore(source,stem):
    raw=source.read_bytes();src=json.loads(raw);names=src['row_names']
    selected=[(a,v) for a,v in zip(src['atoms'],src['primal_float']) if v>1e-8]
    atoms=[a for a,v in selected];approx=np.array([v for a,v in selected])
    U=evaluator();U.__class__=tp.Universe;U.specs=tb.cm.mp.menu_specs()
    columns=[];w=[]
    for a in atoms:
        rr=U.atom_rows(a);assert set(rr)==set(names)
        columns.append([rr[n] for n in names]);w.append(int(any(map(int,a['bits'][:5]))))
    mat=np.array(columns,dtype=float).T;active=np.where(abs(mat@approx)<1e-7)[0]
    equations=[w]+[[columns[j][r] for j in range(len(atoms))] for r in active]
    _,r,piv=qr(np.array(equations,dtype=float).T,pivoting=True,mode='economic')
    rank=np.count_nonzero(abs(np.diag(r))>1e-8);assert rank==len(atoms),(rank,len(atoms))
    choices=list(piv[:len(atoms)])
    mass=fraction_solve([equations[j] for j in choices],[int(j==0) for j in choices]);assert min(mass)>0
    slacks=[sum((mass[j]*columns[j][r] for j in range(len(atoms))),F(0)) for r in range(len(names))];assert min(slacks)>=0
    atoms=[dict(a,exact_mass=str(m)) for a,m in zip(atoms,mass)]
    report={'scope':'Exact source reconstruction for actual-HQR projection only. No optimality, game or HALF(5) claim.',
            'source_sha256':hashlib.sha256(raw).hexdigest(),'source_rows':len(names),'positive_atoms':len(atoms),
            'minimum_source_exact_slack':str(min(slacks)),'atoms':atoms}
    path=tb.cm.HERE/f'exact_current_source_{stem}.json';path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='atoms'}),flush=True)
    return atoms,path


def run(source,stem):
    atoms,exact_path=restore(source,stem)
    allrows=[[tb.rows(a,state) for state in tb.STATES] for a in atoms];names=list(allrows[0][0]);width=8*len(atoms)
    mat=np.array([[float(allrows[j][s][n]) for j in range(len(atoms)) for s in range(8)] for n in names])
    eq=np.zeros((len(atoms),width))
    for j in range(len(atoms)):eq[j,8*j:8*j+8]=1
    rhs=np.array([float(F(a['exact_mass'])) for a in atoms])
    lp=linprog(np.zeros(width),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
    report={'scope':'Complete eight-state real-HQR projection diagnostic of an exactly feasible retained-row source. Not a welfare theorem or game.',
            'exact_source_sha256':hashlib.sha256(exact_path.read_bytes()).hexdigest(),'source_atoms':len(atoms),'new_rows':len(names),
            'floating_lift_feasible':bool(lp.success),'message':lp.message}
    if not lp.success:
        aux=linprog(np.r_[np.zeros(width),1.],A_ub=np.column_stack([-mat,-np.ones(len(names))]),b_ub=np.zeros(len(names)),
                    A_eq=np.column_stack([eq,np.zeros(len(atoms))]),b_eq=rhs,bounds=(0,None),method='highs');assert aux.success
        lam={n:F(float(-v)).limit_denominator(10**8) for n,v in zip(names,aux.ineqlin.marginals) if -v>1e-9}
        assert min(lam.values())>0
        projected=[];slack=F(0)
        for j,a in enumerate(atoms):
            scores=[sum((value*rr[n] for n,value in lam.items()),F(0)) for rr in allrows[j]]
            v=max(scores);slack+=F(a['exact_mass'])*v
            projected.append({'atom':a,'coefficient':str(v),'maximizing_state':tb.STATES[scores.index(v)]})
        assert slack<0
        report.update({'exact_projection_slack':str(slack),'negative_slack_float':float(slack),
                       'exact_nonnegative_row_multipliers':{n:str(v) for n,v in lam.items()},'projected_atoms':projected})
    report['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out=tb.cm.HERE/f'exact_current_trueH_projection_{stem}.json';out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('projected_atoms',)},indent=2),flush=True)


if __name__=='__main__':
    source=Path(sys.argv[1]) if len(sys.argv)>1 else tb.cm.HERE.parent/'maxroot/trueH_payment_fullpricing.json'
    stem=sys.argv[2] if len(sys.argv)>2 else 'payment_v1'
    run(source,stem)
