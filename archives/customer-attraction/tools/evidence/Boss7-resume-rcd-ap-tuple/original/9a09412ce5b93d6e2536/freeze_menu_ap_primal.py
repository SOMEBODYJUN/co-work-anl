"""Exact rational obstruction for the explicitly stated menu-AP row system.

An exact primal above two rules out a factor-two proof from these rows alone.
It does not assert that the atoms extend to any original complete SPE.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,hashlib,argparse
import numpy as np
from scipy.linalg import qr
import menu_ap_pricing as mp
from exact_cross_primal import evaluator
from frozen_pair_reoptimization import fraction_solve
HERE=Path(__file__).resolve().parent

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--joint',action='store_true');ap.add_argument('--tuple',action='store_true');args=ap.parse_args()
    stem='max_menu_tuple' if args.tuple else 'max_menu_joint' if args.joint else 'menu_ap'
    start=time.time();source=HERE/(stem+'_discovery.json');src=json.loads(source.read_text());names=src['row_names']
    chosen=[(a,v) for a,v in zip(src['atoms'],src['primal_float']) if v>1e-8];atoms=[a for a,v in chosen];approx=np.array([v for a,v in chosen]);U=evaluator();U.__class__=mp.Universe;U.specs=mp.menu_specs()
    if args.tuple:
        from max_menu_tuple_pricing import Universe
        U.__class__=Universe
    elif args.joint:
        from max_menu_joint_pricing import Universe
        U.__class__=Universe
    cols=[];w=[];o=[]
    for a in atoms:
        rr=U.atom_rows(a);assert set(rr)==set(names)
        cols.append([rr[n] for n in names]);w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])))
    mat=np.array(cols,dtype=float).T;active=list(np.where(abs(mat@approx)<1e-7)[0]);eq=[w]+[[cols[k][r] for k in range(len(atoms))] for r in active]
    _,r,piv=qr(np.array(eq,dtype=float).T,pivoting=True,mode='economic');rank=np.count_nonzero(abs(np.diag(r))>1e-8);assert rank==len(atoms),(rank,len(atoms))
    pick=list(piv[:len(atoms)]);mass=fraction_solve([eq[i] for i in pick],[int(i==0) for i in pick]);assert min(mass)>0
    W=sum(m*v for m,v in zip(mass,w));O=sum(m*v for m,v in zip(mass,o));assert W==1 and O>2
    sl={name:sum((mass[k]*cols[k][r] for k in range(len(atoms))),F(0)) for r,name in enumerate(names)};assert min(sl.values())>=0
    report={'scope':'Exact feasible point of the explicitly stated necessary rows. Not a complete SPE, actual OPT, global welfare counterexample, or full-universe dual.','row_count':len(names),'welfare':str(W),'comparison_cover':str(O),'gap_above_two':str(O-2),'ratio_float':float(O),'positive_atoms':len(atoms),'minimum_exact_slack':str(min(sl.values())),'zero_slacks':sum(v==0 for v in sl.values()),'atoms':[dict(a,exact_mass=str(m)) for a,m in zip(atoms,mass)],'slacks':{n:str(v) for n,v in sl.items()},'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256((HERE/'menu_ap_pricing.py').read_bytes()).hexdigest(),'seconds':time.time()-start}
    (HERE/('exact_'+stem+'_primal.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('atoms','slacks')},indent=2))
if __name__=='__main__':run()
