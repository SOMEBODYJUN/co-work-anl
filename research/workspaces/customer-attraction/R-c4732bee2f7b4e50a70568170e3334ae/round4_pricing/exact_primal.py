"""Recover and independently verify rational >2 points of the full row system.

Numerical LP picks a basis only. Every delivered mass and every necessary-row
slack is subsequently checked with exact Fraction arithmetic.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,hashlib,time
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from full_pricing import HERE,ROOT,ACTOR,EX,terminal_rows,pair_rows
sys.path.insert(0,str(ACTOR/'round3_closure'))
from frozen_pair_reoptimization import fraction_solve

def verify_atom(atom):
    bits=tuple(map(int,atom['bits']));assert len(bits)==10 and all(v in (0,1) for v in bits)
    hs=[atom['AB_hist'],atom['AE_hist'],atom['second_hist']]
    assert [len(h) for h in hs]==[8,8,16]
    assert all(all(isinstance(v,int) and v>=0 for v in h) and sum(h)==5 for h in hs)
    d=sum(hs[0][4:]);assert d==sum(hs[1][4:])==sum(hs[2][8:])
    assert len(atom['menus_lh'])==3
    for ell,h in atom['menus_lh']:assert isinstance(ell,int) and isinstance(h,int) and 0<=h<=d and 0<=ell-h<=5-d
    return bits,hs,d

def exact_rows(atom,overlap):
    bits,hs,d=verify_atom(atom)
    rr=EX['evaluate'](bits,hs,atom['menus_lh'],True)
    rr.update(terminal_rows(atom));rr.update(pair_rows(atom,overlap=overlap))
    assert len(rr)==557
    return rr,int(any(bits[:5])),int(d>0)

def run(overlap=1,final=False):
    t0=time.time();src=HERE/f'cg_overlap{overlap}{"_final" if final else ""}.json';cg=json.loads(src.read_text())
    names=cg['row_names'];atoms=cg['atoms'];cols=[];w=[];o=[]
    for atom in atoms:
        rr,ww,oo=exact_rows(atom,overlap);assert set(rr)==set(names)
        cols.append([rr[n] for n in names]);w.append(ww);o.append(oo)
    mat=np.asarray(cols,dtype=float).T
    out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs')
    assert out.success and -out.fun>2
    support=list(np.where(out.x>1e-8)[0]);active=list(np.where(abs(mat@out.x)<1e-7)[0])
    equations=[[w[k] for k in support]]+[[cols[k][r] for k in support] for r in active]
    _,r,piv=qr(np.asarray(equations,dtype=float).T,pivoting=True,mode='economic')
    assert np.count_nonzero(abs(np.diag(r))>1e-8)==len(support)
    pick=list(piv[:len(support)])
    masses=fraction_solve([equations[j] for j in pick],[int(j==0) for j in pick])
    assert min(masses)>0
    assert sum(masses[j]*w[k] for j,k in enumerate(support))==1
    O=sum(masses[j]*o[k] for j,k in enumerate(support));assert O>2
    slack={n:sum((masses[j]*cols[k][r] for j,k in enumerate(support)),F(0)) for r,n in enumerate(names)}
    assert min(slack.values())>=0
    cert={'scope':'Exact feasible point for all 557 stated necessary rows over unrestricted histogram types. It is not a full SPE, and comparison cover is not certified OPT.','overlap_subtraction':overlap,'row_count':557,'welfare':'1','comparison_cover':str(O),'ratio_float':float(O),'gap_above_two':str(O-2),'positive_atoms':len(support),'minimum_primal_slack':str(min(slack.values())),'atoms':[dict(atoms[k],exact_mass=str(v)) for k,v in zip(support,masses)],'slacks':{n:str(v) for n,v in slack.items()},'basis_row_names':['normalization' if j==0 else names[active[j-1]] for j in pick],'source_cg_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_point_count':len(atoms),'seconds':time.time()-t0}
    dest=HERE/f'exact_{"optimum_" if final else ""}primal_overlap{overlap}.json';dest.write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({k:v for k,v in cert.items() if k not in ('atoms','slacks','basis_row_names')},indent=2),flush=True)

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 1,final='--final' in sys.argv)
