"""Exact projected weighted-maximum hinge and a frozen-point separation.

The source point is reconstructed only to make the separation rational and
auditable. It is not a game and is not used as another decimal welfare bound.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib, time
import numpy as np
from scipy.linalg import qr
import max_indexed_coupling as cm
from exact_cross_primal import evaluator
from frozen_pair_reoptimization import fraction_solve


def breaks(k, maxprefix):
    """All coefficient breakpoints for all allowed (p,d) states."""
    L=4*(k-1)
    return sorted({F(0),F(L-1)}|{F(L-1)-F((k-1)*d,5*(p+1))
                  for p in range(maxprefix+1) for d in range(6)
                  if F(L-1)-F((k-1)*d,5*(p+1))>=0})


def coefficient(u,p,k,d,jcount,c):
    """One customer's exact coefficient; c is the cap multiplier."""
    L=4*(k-1);den=(p+1)*(p+k)
    return (5*L*u-c*F(jcount,p+k)-F(d,p+1)
            +max(F(0),F((k-1)*d)-5*(L-1-c)*(p+1))/den)


def atom_coefficient(a,c=F(33,5),tag='Sbranch',menu='mW',i=2):
    mb=tuple(map(int,a['max_bits']));p=sum(mb[:i]);k=5-i
    u=cm.lm.q(mb[i],sum(mb));d=sum(a['AB_hist'][4:]);j=cm.counts(a,tag)[menu]
    return coefficient(u,p,k,d,j,c)


def recover():
    start=time.time();source=cm.HERE/'coupled_discovery.json';src=json.loads(source.read_text())
    names=src['row_names'];chosen=[(a,v) for a,v in zip(src['atoms'],src['primal_float']) if v>1e-8]
    atoms=[a for a,v in chosen];approx=np.array([v for a,v in chosen])
    U=evaluator();U.__class__=cm.Universe;U.specs=cm.mp.menu_specs()
    columns=[];w=[];o=[]
    for a in atoms:
        rr=U.atom_rows(a);assert set(rr)==set(names)
        columns.append([rr[n] for n in names]);w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])))
    mat=np.array(columns,dtype=float).T
    active=list(np.where(abs(mat@approx)<1e-7)[0])
    equations=[w]+[[columns[j][r] for j in range(len(atoms))] for r in active]
    _,r,piv=qr(np.array(equations,dtype=float).T,pivoting=True,mode='economic')
    rank=np.count_nonzero(abs(np.diag(r))>1e-8);assert rank==len(atoms),(rank,len(atoms))
    picks=list(piv[:len(atoms)])
    mass=fraction_solve([equations[j] for j in picks],[int(j==0) for j in picks]);assert min(mass)>0
    slacks={n:sum((m*columns[j][r] for j,m in enumerate(mass)),F(0)) for r,n in enumerate(names)}
    assert min(slacks.values())>=0
    W=sum(m*v for m,v in zip(mass,w));O=sum(m*v for m,v in zip(mass,o));assert W==1 and O>2
    # The strict negative margin, not floating optimality, is the certificate.
    values=[atom_coefficient(a) for a in atoms]
    hinge=sum((m*v for m,v in zip(mass,values)),F(0));assert hinge<0
    # Independently recover h=0/1 combinations of the two original rows.
    import weighted_maximum_query as wm
    for a,v in zip(atoms,values):
        mb=tuple(map(int,a['max_bits']))
        score=[]
        for h in (0,1):
            rr=wm.rows(a,mb,h)
            score.append(rr['wmax:BNS:opt']+F(33,5)*rr['Sbranch:wmax:cap:mW'])
        assert v==max(score)
    report={'scope':'Exact separation of an explicitly reconstructed necessary-condition point by a universal projected weighted-maximum relation. Neither a game/SPE counterexample nor a factor-two certificate.',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'source_rows':len(names),'positive_atoms':len(atoms),'welfare':str(W),'comparison_cover':str(O),
            'minimum_source_exact_slack':str(min(slacks.values())),
            'source_zero_slacks':sum(v==0 for v in slacks.values()),
            'hinge_parameters':{'source':'max-third','k':3,'menu_family':'Sbranch','menu':'mW','cap_multiplier':'33/5'},
            'exact_hinge_slack':str(hinge),'exact_hinge_slack_scaled_by_5':str(5*hinge),
            'negative_hinge_slack_float':float(hinge),
            'atoms':[dict(a,exact_mass=str(m),hinge_coefficient=str(v)) for a,m,v in zip(atoms,mass,values)],
            'source_row_slacks':{n:str(v) for n,v in slacks.items()},
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.time()-start}
    (cm.HERE/'exact_projected_hinge.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('atoms','source_row_slacks')},indent=2))
    return report


def all_breakpoint_separation(report):
    atoms=report['atoms'];result={}
    for i in (1,2,3):
        k=5-i
        for tag,menus in cm.mp.MENUS.items():
            for menu in menus:
                for c in breaks(k,i):
                    slack=sum((F(a['exact_mass'])*atom_coefficient(a,c,tag,menu,i) for a in atoms),F(0))
                    if slack<0:result[f'max{i}:{tag}:{menu}:c={c}']=str(slack)
    out={'scope':'Exact finite breakpoint separation for every max-successor source and each old indexed menu. Completeness follows the piecewise affine proof, not numerical sampling.',
         'negative_breakpoint_rows':len(result),'negative_slacks':result,
         'source_sha256':hashlib.sha256((cm.HERE/'exact_projected_hinge.json').read_bytes()).hexdigest()}
    (cm.HERE/'exact_all_hinge_breakpoints.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'negative_breakpoint_rows':len(result),'minimum_exact_slack':str(min(map(F,result.values())))}))


if __name__=='__main__':all_breakpoint_separation(recover())
