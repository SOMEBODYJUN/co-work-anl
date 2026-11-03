"""One new exact check of the previously unverified 65-atom 728 point.

No discovery/transport program is imported. The mature 69-point computation
and all generic regression loops are deliberately not executed.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, permutations
import hashlib
import json

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'related/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_joint_terminal.json'
REPORT = HERE / 'B2-raw/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_coupling/exact_joint_728_separation.json'

def expand(hist, arity):
    assert len(hist) == 2**arity and all(type(n) is int and n >= 0 for n in hist)
    return [b for b,n in zip(product((0,1),repeat=arity),hist) for _ in range(n)]

def top(v,k):
    return sum(sorted(v,reverse=True)[:k],F(0))

raw = INPUT.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'b5ec102366191aea06e4a7a93073a7913bd625101c743cc5ccc8f9132d744b05'
doc = json.loads(raw); old = json.loads(REPORT.read_text())
assert len(doc['atoms']) == 65 and len(doc['slacks']) == doc['row_count'] == 728
stored = [F(v) for v in doc['slacks'].values()]
assert min(stored) >= 0
records=[]; W=F(0); O=F(0); singles=[F(0),F(0)]; joint=F(0); gap=F(0)
nonempty_matching_assignments=0; empty_group_assignments=0; literal_terms=0; positive_gap_atoms=0
for ai, atom in enumerate(doc['atoms']):
    assert set(atom) == {'bits','AB_hist','AE_hist','second_hist','menus_lh','exact_mass'}
    assert len(atom['bits'])==10 and set(atom['bits']) <= {'0','1'}
    bits=list(map(int,atom['bits'])); mass=F(atom['exact_mass']);assert mass>0
    families={label:expand(atom[label+'_hist'],4 if label=='second' else 3) for label in ('AB','AE','second')}
    assert {len(v) for v in families.values()}=={5}
    ds={sum(z[0] for z in v) for v in families.values()};assert len(ds)==1;dopt=next(iter(ds))
    assert len(atom['menus_lh'])==3
    for ell,h in atom['menus_lh']:
        assert type(ell) is int and type(h) is int and 0<=h<=dopt and 0<=ell-h<=5-dopt
    W+=mass*int(any(bits[:5]));O+=mass*int(dopt>0)
    src=families['AB'];tar=families['AE'];q=5;a,b=bits[:2]
    own=[F(z[2],a+b+z[0]+z[1]+1) for z in src]
    inv=[F(1,a+b+z[0]+z[1]+1) for z in src]
    K=[sum(z[p] for z in tar) for p in (1,2)]
    atom_singles=[F(0),F(0)];atom_joint=F(0);atom_gap=F(0);groups=[]
    canonical=[None]*q
    for t in (0,1):
        inds=[i for i,z in enumerate(src) if z[0]==t]
        target=[z for z in tar if z[0]==t];assert len(inds)==len(target)
        for i,z in zip(inds,target):canonical[i]=z
    for t in (0,1):
        inds=[i for i,z in enumerate(src) if z[0]==t]
        target=[z for z in tar if z[0]==t]
        candidates=[]
        for perm in sorted(set(permutations(target))):
            assigned=list(canonical)
            for i,z in zip(inds,perm):assigned[i]=z
            vals=[]
            for pos in (1,2):
                terms=[own[i]-inv[i]*assigned[j][pos]
                       for i in inds for j in range(q) if j!=i]
                vals.append(sum(terms,F(0)));literal_terms+=len(terms)
            candidates.append({'permutation':[list(z) for z in perm],
                               'single_literals':list(map(str,vals)),
                               'joint_literal':str(sum(vals,F(0)))})
            if inds:nonempty_matching_assignments+=1
            else:empty_group_assignments+=1
        best=[max(F(c['single_literals'][r]) for c in candidates) for r in (0,1)]
        best_joint=max(F(c['joint_literal']) for c in candidates)
        dv=[inv[i] for i in inds];scores=[z[1]+z[2] for z in target]
        k,l=[sum(z[p] for z in target) for p in (1,2)]
        h=sum(z[1]*z[2] for z in target);u=k+l-h
        base=[4*sum((own[i] for i in inds),F(0))-K[r]*sum(dv,F(0)) for r in (0,1)]
        assert best==[base[0]+top(dv,k),base[1]+top(dv,l)]
        assert best_joint==sum(base,F(0))+top(dv,h)+top(dv,u)
        layer=F(0);sorted_d=sorted(dv,reverse=True)
        for r in range(1,len(dv)):
            bracket=min(k,r)+min(l,r)-min(h,r)-min(u,r)
            assert bracket==max(0,min(r-h,k-h,l-h,u-r))
            layer+=(sorted_d[r-1]-sorted_d[r])*bracket
        assert sum(best,F(0))-best_joint==layer
        for r in (0,1):atom_singles[r]+=best[r]
        atom_joint+=best_joint;atom_gap+=layer
        groups.append({'t':t,'source_indices':inds,'inverse_denominators':list(map(str,dv)),
                       'target_tuples':[list(z) for z in target], 'candidates':candidates,
                       'single_maxima':list(map(str,best)), 'joint_maximum':str(best_joint),
                       'loss':str(layer)})
    assert sum(atom_singles,F(0))-atom_joint==atom_gap>=0
    if atom_gap>0:positive_gap_atoms+=1
    for r in (0,1):singles[r]+=mass*atom_singles[r]
    joint+=mass*atom_joint;gap+=mass*atom_gap
    records.append({'atom_index':ai,'bits':atom['bits'],'mass':str(mass),'groups':groups,
                    'single_coefficients':list(map(str,atom_singles)),
                    'joint_coefficient':str(atom_joint),'loss_coefficient':str(atom_gap)})
assert str(W)==doc['welfare'] and str(O)==doc['comparison_cover']
assert singles==list(map(F,old['separate_component_slacks']))
assert joint==F(old['joint_slack']) and gap==F(old['strict_shared_matching_gain'])
assert min(singles)>=0 and joint<0 and sum(singles,F(0))-joint==gap
out={'scope':'New fixed-65-point AB-to-AE positions1,2 exact literal offdiagonal audit only; no LP, no 728-row recomputation, no SPE/OPT certificate',
     'mathematical_entry_executions':1, 'source_sha256':hashlib.sha256(raw).hexdigest(),
     'original_report_sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),
     'atoms':65,'W':str(W),'comparison_cover':str(O),
     'stored_slacks_read_and_sign_checked_only':728,'stored_zero_slacks':sum(v==0 for v in stored),
     'nonempty_group_distinct_tuple_matchings':nonempty_matching_assignments,
     'empty_group_identity_matchings':empty_group_assignments,'literal_offdiagonal_terms':literal_terms,
     'positive_loss_atoms':positive_gap_atoms,'separate_slacks':list(map(str,singles)),
     'joint_slack':str(joint),'loss':str(gap),'all_original_exact_separation_values_equal':True,
     'records':records}
(HERE/'new-728-joint-only-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='records'},ensure_ascii=False,indent=2))
