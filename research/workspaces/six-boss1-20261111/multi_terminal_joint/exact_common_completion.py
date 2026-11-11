"""An exact 66-node common R/Z completion for all 4290 nonself ZZ queries.

Phase A puts every R on the common initial interval.  Phase B puts family-0
R and family-1 Z on that interval.  Each phase preserves every own four-state
marginal.  Their exact rational mixture repairs A's sole negative orbit.
Uniformly expand all 720 comparison-index permutations; distinct labels stay
distinct even when their membership events happen to coincide.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode=True
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import permutations,product
from pathlib import Path
import json
from common import (HERE,NODES,STATES,dump,marginal,metadata,node_group,
                    pair_class,parse,sha,words)


def phase_atoms(phase,hi,h,masses,groups):
    H=masses[hi];ws=words(h)
    ng=[node_group(e,ws) for e in NODES]
    vals={g:marginal(hi,ids,masses) for g,ids in groups[hi].items()}
    moments={g:(p[2]+p[3],p[1]+p[3],p[3]) for g,p in vals.items()}
    endpoints={F(),H}
    defs=[]
    for e,g in zip(NODES,ng):
        q,v,t=moments[g]
        if phase=='A' or e[0]==0:
            r=((F(),q),);z=((F(),t),(q,q+v-t))
        else:
            r=((F(),t),(v,v+q-t));z=((F(),v),)
        assert sum((b-a for a,b in r),F())==q
        assert sum((b-a for a,b in z),F())==v
        assert all(0<=a<=b<=H for a,b in r+z)
        endpoints.update(x for interval in r+z for x in interval)
        defs.append((r,z))
    cuts=sorted(endpoints)
    atoms=[]
    for a,b in zip(cuts,cuts[1:]):
        u=(a+b)/2
        states=tuple((int(any(l<=u<r for l,r in rr)),
                      int(any(l<=u<r for l,r in zz))) for rr,zz in defs)
        atoms.append((b-a,states))
    assert sum((m for m,s in atoms),F())==H
    for k,g in enumerate(ng):
        actual=tuple(sum((m for m,s in atoms if s[k]==st),F()) for st in STATES)
        assert actual==vals[g]
    return atoms,ng,moments,cuts,defs


def audit_phase(phase,hist,masses,groups):
    totals=defaultdict(F);per_hist=defaultdict(dict);catalog=[]
    free=defaultdict(F)
    for hi,h in hist.items():
        atoms,ng,moments,cuts,defs=phase_atoms(phase,hi,h,masses,groups)
        p=sum(map(int,h['actual_bits'][:4]));D=(p+1)*(p+2)
        # Compute cross overlaps from the full joint atoms, not from a formula.
        overlaps=defaultdict(F)
        for mass,states in atoms:
            on_r=[i for i,st in enumerate(states) if st[0]]
            on_z=[i for i,st in enumerate(states) if st[1]]
            for i in on_r:
                for j in on_z:
                    overlaps[i,j]+=mass
        local=defaultdict(F)
        for i,e in enumerate(NODES):
            qe,ve,te=moments[ng[i]]
            assert overlaps[i,i]==te
            for j,f in enumerate(NODES):
                cl=pair_class(e,f)
                if i==j:
                    assert (ve-ve)/(p+1)+(overlaps[i,j]-te)/D==0
                    continue
                qf,vf,tf=moments[ng[j]]
                J=overlaps[i,j]
                assert max(F(),qe+vf-masses[hi])<=J<=min(qe,vf)
                if phase=='B' and e[0]==0 and f[0]==1:
                    assert J==min(qe,vf)
                value=(ve-vf)/(p+1)+(J-te)/D
                totals[cl]+=value;local[cl]+=value
                free[cl]+=(ve-vf)/(p+1)+(min(qe,vf)-te)/D
        for cl in set(pair_class(e,f) for e in NODES for f in NODES):
            per_hist[cl][hi]=local[cl]
        catalog.append({'hist_column':hi,'P':p,'actual_bits':h['actual_bits'],
                        'hist':h['hist'],'mass':str(masses[hi]),
                        'interval_breakpoints':[str(x) for x in cuts],
                        'node_intervals':[{'literal':e,
                                           'R':[[str(a),str(b)] for a,b in rr],
                                           'Z':[[str(a),str(b)] for a,b in zz]}
                                          for e,(rr,zz) in zip(NODES,defs)],
                        'atoms':[{'mass':str(m),'states':[2*r+z for r,z in s]} for m,s in atoms]})
    return totals,per_hist,catalog,free


def verify_full_orbits():
    counts=Counter(pair_class(e,f) for e in NODES for f in NODES)
    # Every literal ordered pair in a class occurs equally often under S6.
    # This verifies actual full literal orbits rather than group identities.
    reps={pair_class(e,f):(e,f) for e in NODES for f in NODES}
    records=[]
    for cl,(e,f) in sorted(reps.items()):
        orbit=Counter(((e[0],pi[e[1]],pi[e[2]]),
                       (f[0],pi[f[1]],pi[f[2]])) for pi in permutations(range(6)))
        assert len(orbit)==counts[cl]
        assert sum(orbit.values())==720
        assert set(orbit.values())=={720//counts[cl]}
        assert all(pair_class(ee,ff)==cl for ee,ff in orbit)
        records.append({'class':cl,'size':counts[cl],
                        'multiplicity_in_S6':720//counts[cl],
                        'literal_pairs':[[list(ee),list(ff)] for ee,ff in sorted(orbit)]})
    assert len(reps)==42
    return counts,records


def main():
    point,cols,masses,hist,groups=parse()
    counts,orbits=verify_full_orbits()
    A,Ah,Ac,freeA=audit_phase('A',hist,masses,groups)
    B,Bh,Bc,freeB=audit_phase('B',hist,masses,groups)
    bad=[cl for cl in counts if A[cl]<0]
    assert len(bad)==1
    target=bad[0]
    assert target==(0,1,(0,1,0,2))
    assert B[target]>0 and B[target]==freeB[target]
    # Calculate the full exact interval, then use the simple interior weight 1/2.
    lower=F();upper=F(1);lower_class=None;upper_class=None
    for cl in counts:
        delta=B[cl]-A[cl]
        if delta>0 and -A[cl]/delta>lower:
            lower=-A[cl]/delta;lower_class=cl
        elif delta<0 and A[cl]/(-delta)<upper:
            upper=A[cl]/(-delta);upper_class=cl
        elif delta==0:
            assert A[cl]>=0
    lam=F(1,2)
    assert lower<lam<upper
    totals={cl:(1-lam)*A[cl]+lam*B[cl] for cl in counts}
    assert totals[target]>0
    assert all(v>=0 for v in totals.values())
    assert all(totals[cl]>0 for cl in counts if not (
        cl in ((0,0,(0,1,0,1)),(1,1,(0,0,0,0)),(1,1,(0,1,0,1)))))
    records=[]
    for cl in sorted(counts):
        records.append({'class':cl,'literal_pairs':counts[cl],
            'phase_A_orbit_sum':str(A[cl]),'phase_B_orbit_sum':str(B[cl]),
            'mixture_orbit_sum':str(totals[cl]),
            'individual_IC_slack':str(totals[cl]/counts[cl]),
            'per_hist':[[hi,str((1-lam)*Ah[cl][hi]+lam*Bh[cl][hi])] for hi in hist]})
    witness=metadata()|{'source_path':str(Path(__file__)),'source_sha256':sha(Path(__file__)),
        'scope':'Exact common completion of 66 literal own (R,Z) marginals and every old-Z-to-old-Z terminal IC only; no SPE or full necessary graph completion claim',
        'states_encoding':{'0':'00','1':'01','2':'10','3':'11'},
        'literal_node_order':NODES,'W':point['W'],
        'phase_A_weight':str(1-lam),'phase_B_weight':str(lam),
        'phase_B_weight_float':float(lam),
        'feasible_phase_B_weight_interval':{'lower':str(lower),'upper':str(upper),
            'lower_active_class':lower_class,'upper_active_class':upper_class,
            'lower_float':float(lower),'upper_float':float(upper)},
        'symmetrization':{
            'permutations':list(permutations(range(6))),
            'mass_rule':'phase_weight * base_atom.mass / 720 for each listed permutation',
            'state_rule':'base state at (f,i,j) is assigned to literal (f,pi[i],pi[j]); likewise permute the six old words',
            'actual_bits_rule':'unchanged',
            'labels':'All 66 R and Z nodes stay literal; no equality is inferred from equal coverage or equal group'},
        'phases':{'A':Ac,'B':Bc},
        'base_atoms_A':sum(len(x['atoms']) for x in Ac),
        'base_atoms_B':sum(len(x['atoms']) for x in Bc),
        'positive_expanded_atoms':720*sum(len(x['atoms']) for x in Ac+Bc),
        'all_own_marginals_verified':True,
        'all_full_S6_literal_orbits_verified':True,
        'ordered_queries':4356,'nonself_queries':4290,
        'positive_nonself_queries':sum(counts[cl] for cl,v in totals.items() if v>0),
        'negative_queries':0,
        'minimum_nonself_IC_slack':str(min(totals[cl]/counts[cl] for cl in counts if totals[cl]>0)),
        'records':records,'full_literal_orbits':orbits,
        'finite_unit_customer_rule':'All base masses and phase weights are rational. Multiply all expanded atom masses by their common denominator to obtain finitely many distinct unit customers. This preserves homogeneous IC signs and normalized marginal ratios.'}
    dump(HERE/'common_completion_19556.json',witness)
    print(json.dumps({k:v for k,v in witness.items() if k not in ('phases','records','full_literal_orbits','symmetrization')},ensure_ascii=False))


if __name__=='__main__':
    main()
