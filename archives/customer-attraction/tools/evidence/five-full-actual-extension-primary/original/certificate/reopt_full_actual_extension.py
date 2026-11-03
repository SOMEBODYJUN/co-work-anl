"""Append sparsely priced columns to the explicit actual-HQR RMP.

If the extended RMP crosses two, restore a rational feasible witness of all
7497 rows and an old-state projection with an explicit actual-HQR lift.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib,time
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import qr
import two_real_weighted_branches as two
cm=two.cm
sys.path.insert(0,str(cm.HERE.parent/'maxroot'))
import trueH_own_index_pricing as original
from exact_cross_primal import evaluator
from frozen_pair_reoptimization import fraction_solve


def key(a):return cm.mp.atom_key(a)+(a['max_bits'],a['actual_HQR_bits'])
def clean(a):return {k:a[k] for k in ('bits','AB_hist','AE_hist','second_hist','menus_lh','max_bits','actual_HQR_bits')}


def run(negative_path,stem,seed_path=None):
    start=time.time();seed_path=seed_path or cm.HERE/'full_actual_extension_discovery.json'
    seed=json.loads(seed_path.read_text());new=json.loads(negative_path.read_text())
    incoming=new['atoms'] if 'atoms' in new else [entry['atom'] for entry in new['new_columns']]
    atoms=[];seen=set()
    for a in seed['atoms']+incoming:
        kk=key(a)
        if kk not in seen:atoms.append(clean(a));seen.add(kk)
    names=seed['row_names'];oldnames=[n for n in names if not n.startswith('actual-extension:')];newnames=[n.removeprefix('actual-extension:') for n in names if n.startswith('actual-extension:')]
    assert len(oldnames)==6750 and len(newnames)==747
    U=evaluator();U.__class__=original.Universe;U.specs=cm.mp.menu_specs()
    oldcache={};columns=[];w=[];o=[]
    for a in atoms:
        oldkey=cm.mp.atom_key(a)+(a['max_bits'],)
        if oldkey not in oldcache:
            rr=U.atom_rows(a);assert set(rr)==set(oldnames)
            oldcache[oldkey]=[float(rr[n]) for n in oldnames]
        newrr=two.rows(a,tuple(map(int,a['actual_HQR_bits'])),'actual')
        columns.append(oldcache[oldkey]+[float(newrr[n]) for n in newnames])
        w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(columns,dtype=float).T
    lp=linprog(-np.array(o,float),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    beta=-float(lp.fun)
    discovery={'scope':'Explicit actual-HQR extended RMP after sparse known-pool columns. No full-type certificate, SPE or welfare theorem.',
               'row_names':names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':beta,
               'dual_multipliers_float':{n:float(-v) for n,v in zip(names,lp.ineqlin.marginals) if -v>1e-10},
               'minimum_slack_float':float(min(mat@lp.x)),
               'seed_sha256':hashlib.sha256(seed_path.read_bytes()).hexdigest(),'negative_columns_sha256':hashlib.sha256(negative_path.read_bytes()).hexdigest(),
               'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target=cm.HERE/f'full_actual_extension_{stem}_discovery.json';target.write_text(json.dumps(discovery,indent=2)+'\n')
    print(json.dumps({'discovery':target.name,'columns':len(atoms),'old_types':len(oldcache),'restricted_beta_float':beta,'seconds':time.time()-start}),flush=True)
    if beta<=2+1e-7:return target
    support=list(np.where(lp.x>1e-9)[0]);active=list(np.where(abs(mat@lp.x)<1e-7)[0]);exact=[];ecache={}
    for i in support:
        a=atoms[i];oldkey=cm.mp.atom_key(a)+(a['max_bits'],)
        if oldkey not in ecache:ecache[oldkey]=U.atom_rows(a)
        nr=two.rows(a,tuple(map(int,a['actual_HQR_bits'])),'actual')
        exact.append([ecache[oldkey][n] for n in oldnames]+[nr[n] for n in newnames])
    eq=[[w[i] for i in support]]+[[exact[j][r] for j in range(len(support))] for r in active]
    _,r,piv=qr(np.array(eq,dtype=float).T,pivoting=True,mode='economic');rank=np.count_nonzero(abs(np.diag(r))>1e-8)
    assert rank==len(support),(rank,len(support));picks=list(piv[:len(support)])
    mass=fraction_solve([eq[j] for j in picks],[int(j==0) for j in picks]);assert min(mass)>0
    slacks={n:sum((m*exact[j][r] for j,m in enumerate(mass)),F(0)) for r,n in enumerate(names)};assert min(slacks.values())>=0
    W=sum(m*w[i] for i,m in zip(support,mass));O=sum(m*o[i] for i,m in zip(support,mass));assert W==1 and O>2
    extended=[];projected={}
    for i,m in zip(support,mass):
        a=atoms[i];extended.append(dict(a,exact_mass=str(m)));oldkey=cm.mp.atom_key(a)+(a['max_bits'],)
        if oldkey not in projected:projected[oldkey]=[{k:v for k,v in a.items() if k!='actual_HQR_bits'},F(0)]
        projected[oldkey][1]+=m
    report={'scope':'Exact above-two source with a simultaneous witness of all explicit actual-HQR rows. Not an original game/SPE, full-type optimum, or half counterexample.',
            'source_rows':len(names),'welfare':str(W),'comparison_cover':str(O),'gap_above_two':str(O-2),
            'positive_extended_atoms':len(extended),'positive_projected_atoms':len(projected),
            'minimum_exact_slack':str(min(slacks.values())),'atoms':[dict(a,exact_mass=str(m)) for a,m in projected.values()],
            'actual_HQR_lift':extended,'row_slacks':{n:str(v) for n,v in slacks.items()},
            'discovery_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.time()-start}
    exact_path=cm.HERE/f'exact_full_actual_extension_{stem}.json';exact_path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('atoms','actual_HQR_lift','row_slacks')},indent=2),flush=True)
    return exact_path


if __name__=='__main__':run(Path(sys.argv[1]),sys.argv[2] if len(sys.argv)>2 else 'known_v1',Path(sys.argv[3]) if len(sys.argv)>3 else None)
