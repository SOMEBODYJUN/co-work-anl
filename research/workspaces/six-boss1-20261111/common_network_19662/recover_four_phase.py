"""Recover a rational common network/B4 measure on the new point.

The four-orientation LP is only a finite constructive family.  Its floating
result selects a support; all final margins and payoff inequalities are
reconstructed and checked over Fraction.  No infeasibility claim is made.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
sys.path.insert(0,str(WORK/'family_joint_19578'))
from build_common import Data, serial, digest
from phase_mix import make_orientation, old_queries, classes

PHASES=('RR','RZ','ZR','ZZ')
POINT=WORK/'union_augmented_lp/augmented_lp_exact.json'
INPUT_SHA='b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'

def solve(equations,n,seed):
    pivots={}
    for name,initial,rhs in equations:
        row={j:c for j,c in initial.items() if c};rhs=Q(rhs)
        while row:
            lead=min(row)
            if lead not in pivots:
                fac=row[lead]
                pivots[lead]=({j:c/fac for j,c in row.items()},rhs/fac)
                break
            old,b=pivots[lead];fac=row[lead];rhs-=fac*b
            for j,c in old.items():
                val=row.get(j,Q())-fac*c
                if val:row[j]=val
                elif j in row:del row[j]
        else:
            if rhs:return None,dict(rank=len(pivots),inconsistent_at=name,residual=str(rhs))
    ans=list(seed)
    for lead,(row,rhs) in sorted(pivots.items(),reverse=True):
        ans[lead]=rhs-sum((c*ans[j] for j,c in row.items() if j!=lead),Q())
    return ans,dict(rank=len(pivots),free=n-len(pivots))

def main():
    assert digest(POINT)==INPUT_SHA
    data=Data(POINT,HERE/'interval_A.json')
    raw=json.loads((HERE/'hist_four_phase_attempt.json').read_text())
    disc=raw['discovery']
    phases={p:make_orientation(data,p) for p in PHASES}
    old={p:{h:old_queries(data,phases[p],[h]) for h in data.hist} for p in PHASES}
    variables=[tuple(v) for v in disc['variables_in_order']]
    vmap={v:i for i,v in enumerate(variables)}
    n=len(variables)
    weights=[tuple(v) for v in disc['phase_weights_in_order']]
    wi={v:n+i for i,v in enumerate(weights)}
    eps=n+len(weights)
    floating=disc['floating_flow']+disc['floating_phase_weights']+[disc['floating_common_slack']]
    eq=[];ub=[]
    positive_hist=[h for h in data.hist if data.mass[h]]
    state_by_h={h:{s['column']:s for s in data.family['B4'][h]} for h in data.hist}
    for h in positive_hist:
        states=[s for s in data.family['B4'][h] if s['mass']]
        eq.append((['phase-simplex',h],{wi[h,p]:Q(1) for p in PHASES},Q(1)))
        for p in PHASES:
            for a in phases[p][h]:
                row={wi[h,p]:-a['mass']}
                row.update({vmap[h,p,a['index'],s['column']]:Q(1) for s in states})
                eq.append((['atom',h,p,a['index']],row,Q()))
        for s in states[:-1]:
            eq.append((['B4-state',h,s['column']],
                       {vmap[h,p,a['index'],s['column']]:Q(1) for p in PHASES for a in phases[p][h]},s['mass']))
    for k,sp in enumerate(data.specs('B4')):
        row={eps:Q(1)}
        for i,(h,p,ai,j) in enumerate(variables):
            val=data.cost(phases[p][h][ai],state_by_h[h][j],sp)
            if val:row[i]=val
        ub.append((['B4-IC',sp],row,data.budgets('B4')[k]))
    old_keys=list(old['RR'][next(iter(data.hist))])
    independent=[]
    for key in old_keys:
        invariant=all(old[p][h][key]==old['RR'][h][key] for h in positive_hist for p in PHASES)
        if invariant:
            val=sum((old['RR'][h][key] for h in positive_hist),Q())
            assert val>=0
            independent.append(dict(kind=key[0],orbit=key[1],slack=val))
        else:
            row={wi[h,p]:-old[p][h][key] for h in positive_hist for p in PHASES if old[p][h][key]}
            ub.append((['old-IC',key],row,Q()))
    assert len(eq)==disc['equalities']
    assert len(ub)==disc['B4_query_rows']+disc['nonconstant_old_query_rows']
    support=[i for i,x in enumerate(floating) if x>1e-10 or i==eps]
    smap={i:j for j,i in enumerate(support)}
    active=[i for i,(name,row,rhs) in enumerate(ub)
            if abs(float(rhs)-sum(float(c)*floating[j] for j,c in row.items()))<1e-9]
    equations=[(name,{smap[j]:c for j,c in row.items() if j in smap},rhs)
               for name,row,rhs in eq+[ub[i] for i in active]]
    equations.append((['epsilon-zero'],{smap[eps]:Q(1)},Q()))
    seed=[Q(str(floating[i])).limit_denominator(10**12) for i in support]
    exact,recovery=solve(equations,len(support),seed)
    report=dict(scope='Finite four-orientation constructive family; exact feasible atoms imply a common coverage layer, not SPE',
                point_sha256=INPUT_SHA,source_sha256=digest(Path(__file__)),support_size=len(support),
                active_rows=active,recovery=recovery)
    phase_summary=[]
    for p in PHASES:
        vv={key:sum((old[p][h][key] for h in data.hist),Q()) for key in old_keys}
        phase_summary.append(dict(phase=p,base_atoms=sum(map(len,phases[p].values())),
            negative_orbits=[dict(kind=k[0],orbit=k[1],slack=v) for k,v in vv.items() if v<0],
            minimum=min(vv.values())))
    report['phase_old_queries']=phase_summary
    if exact is None:
        (HERE/'four_phase_exact_recovery.json').write_text(json.dumps(serial(report),indent=2)+'\n')
        print(json.dumps(serial(report['recovery'])),flush=True)
        return
    x=[Q()]*(eps+1)
    for i,v in zip(support,exact):x[i]=v
    eqres=[sum((c*x[j] for j,c in row.items()),Q())-rhs for _,row,rhs in eq]
    slack=[rhs-sum((c*x[j] for j,c in row.items()),Q()) for _,row,rhs in ub]
    report.update(equality_check=not any(eqres),minimum_mass=min(x[:n]),minimum_phase=min(x[n:eps]),
                  minimum_slack=min(slack),epsilon=x[eps],
                  negative_rows=[dict(label=ub[i][0],slack=v) for i,v in enumerate(slack) if v<0])
    report['exact_feasible']=not any(eqres) and min(x[:eps])>=0 and min(slack)>=0
    report['inequality_values']=[dict(label=name,slack=s) for (name,_,_),s in zip(ub,slack)]
    report['exact_solution']=[str(v) for v in x]
    (HERE/'four_phase_exact_recovery.json').write_text(json.dumps(serial(report),indent=2)+'\n')
    print(json.dumps(serial({k:v for k,v in report.items() if k not in ('exact_solution','inequality_values','phase_old_queries','active_rows')})),flush=True)
    if not report['exact_feasible']:return
    blocks=[]
    for h in positive_hist:
        atoms=[]
        for i,(hh,p,ai,j) in enumerate(variables):
            if hh!=h or not x[i]:continue
            desc=data.cols[j]
            atoms.append(dict(mass=x[i],states=phases[p][h][ai]['states'],
                              B4_state=tuple(desc['hidden'])+(desc['ell']//6,),phase=p,phase_atom=ai))
        blocks.append(dict(hist_column=h,actual_bits=data.hist[h]['actual_bits'],hist=data.hist[h]['hist'],atoms=atoms))
    witness=dict(scope='One common measure for all old RZ nodes and the same B4 state; no SPE assertion',
        point_sha256=INPUT_SHA,source_sha256=digest(Path(__file__)),
        literal_node_order=[(f,i,j) for f in range(2) for i in range(6) for j in range(6) if f or i!=j],
        symmetrization='Each atom is copied with mass/720 to every pi in S6; pi moves old words and literal RZ node indices together, B4 unchanged',
        phase_weights=[dict(hist_column=h,weights={p:x[wi[h,p]] for p in PHASES}) for h in positive_hist],
        blocks=blocks,base_atoms=sum(len(b['atoms']) for b in blocks),expanded_atoms=720*sum(len(b['atoms']) for b in blocks))
    (HERE/'common_atoms.json').write_text(json.dumps(serial(witness),indent=2)+'\n')

if __name__=='__main__':main()
