"""One new exact entry: loss layers, adjacent margins and selected69 point.

No original missing CLI, optimizer, old GO/HB/GX entry or full727/728/737
primal/dual pricing is run. The69-point calculation is literal definitions.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
import hashlib,json
E=Path(__file__).resolve().parent;OUT=E/'new-loss-layers-adjacent-and-727.json'
if OUT.exists():raise SystemExit('Successful definition entry exists; do not rerun')
def top(ds,k):return sum(sorted(ds,reverse=True)[:k],F(0))
def layer(d,tuples,weights):
    n=len(d);ks=[sum(t[j] for t in tuples) for j in range(len(weights))]
    scores=[sum(w*z for w,z in zip(weights,t)) for t in tuples]
    sd=sorted(d,reverse=True);ss=sorted(scores,reverse=True)
    separate=sum((w*top(d,k) for w,k in zip(weights,ks)),F(0))
    joint=sum((x*y for x,y in zip(sd,ss)),F(0));terms=[]
    for r in range(1,n):
        bracket=sum(w*min(k,r) for w,k in zip(weights,ks))-top(scores,r)
        jump=sd[r-1]-sd[r];assert bracket>=0 and jump>=0
        terms.append({'r':r,'jump':jump,'bracket':bracket,'term':jump*bracket})
    delta=sum((v['term'] for v in terms),F(0));assert separate-joint==delta
    return separate,joint,delta,terms

# Weighted multiple menus, O and complemented D rows; no generic point
# here is claimed to satisfy SPE IC. These are algebra/matching identities.
multi_cases=group_identities=literal_group_matchings=0
menus=list(product((0,1),repeat=3));weightsets=[(1,2,3),(0,1,2)]
for q in range(1,4):
    for config in range(2):
        loads=[(2*i+config)%3 for i in range(q)];labels=[0 if config==0 else i%2 for i in range(q)]
        for rawtuples in product(menus,repeat=q):
            for weights in weightsets:
                for Dmask in [(0,0,0),(1,0,1),(1,1,1)]:
                    transformed=[tuple(1-b if dc else b for b,dc in zip(t,Dmask)) for t in rawtuples]
                    for label in (0,1):
                        pos=[i for i,t in enumerate(labels) if t==label]
                        ds=[F(1,loads[i]+1) for i in pos];tt=[transformed[i] for i in pos]
                        separate,joint,delta,terms=layer(ds,tt,weights)
                        pp=set(permutations(tt));literal_group_matchings+=len(pp)
                        literal=max((sum((di*sum(w*z for w,z in zip(weights,t)) for di,t in zip(ds,p)),F(0)) for p in pp),default=F(0))
                        assert literal==joint;group_identities+=1
                    multi_cases+=1

# Trapezoid integer coefficient and two-level reduction, own finite domain.
integer_cases=twolevel_cases=0
for n in range(7):
    for k in range(n+1):
        for l in range(n+1):
            for h in range(max(0,k+l-n),min(k,l)+1):
                u=k+l-h
                for r in range(n+1):
                    bracket=min(k,r)+min(l,r)-min(h,r)-min(u,r)
                    trapezoid=max(0,min(r-h,k-h,l-h,u-r))
                    assert bracket==trapezoid>=0;integer_cases+=1
                    for p in (0,2):
                        ds=[F(1,p+1)]*r+[F(1,p+2)]*(n-r)
                        delta=top(ds,k)+top(ds,l)-top(ds,h)-top(ds,u)
                        assert delta==F(trapezoid,(p+1)*(p+2));twolevel_cases+=1

# Adjacent source loads: exhaustive indexed realizations and all margins in
# a deliberately bounded domain. The general recurrence is in the proof.
def comps(n,k):
    if k==1:yield(n,);return
    for j in range(n+1):
        for t in comps(n-j,k-1):yield(j,)+t
seen={};indexed=0
states=list(product(range(3),(0,1)))
for q in range(5):
    for v in product(states,repeat=q):
        indexed+=1;L=tuple(sum(p==c for p,a in v) for c in range(4));M=tuple(sum(p+a==c for p,a in v) for c in range(4))
        J=tuple(sum(p==c and a==b for p,a in v) for c in range(4) for b in (0,1));key=(q,L,M)
        if key in seen:assert seen[key]['joint']==J
        else:seen[key]={'joint':J,'witness':v}
margins=[];compatible=0
for q in range(5):
    for left in comps(q,3):
        L=left+(0,)
        for M in comps(q,4):
            X=[];Y=[];cumL=cumM=0;interlace=True
            for c in range(4):
                oldL=cumL;cumL+=L[c];cumM+=M[c]
                X.append(cumL-cumM);Y.append(L[c]-X[-1]);interlace &= oldL<=cumM<=cumL
            positive=all(v>=0 for v in X+Y)
            key=(q,L,M);assert positive==interlace==(key in seen)
            if positive:
                compatible+=1;assert tuple(v for pair in zip(Y,X) for v in pair)==seen[key]['joint']
            margins.append({'q':q,'L':L,'M':M,'X':X,'Y':Y,'compatible':positive,'witness':seen[key]['witness'] if positive else None})
assert compatible==len(seen)
wide1=[(0,1),(1,2)];wide2=[(0,2),(1,1)]
assert sorted(p for p,q in wide1)==sorted(p for p,q in wide2) and sorted(q for p,q in wide1)==sorted(q for p,q in wide2)
wide_costs=[sum((F(1,(p+1)*(q+1)) for p,q in pairs),F(0)) for pairs in (wide1,wide2)]
assert wide_costs[0]!=wide_costs[1]

# Exact new69 point. Verify its fields and selected joint-only separation,
# not every one of its727 source-reported slacks or any pricing dual.
P=E/'comparison/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_terminal_cross.json'
assert hashlib.sha256(P.read_bytes()).hexdigest()=='e2caa8f504da61dd41c6980671f2ce3d0c715f5d4dcce4b16dd656af25363acb'
data=json.loads(P.read_text());atoms=data['atoms'];assert len(atoms)==69
triples=list(product((0,1),repeat=3));quads=list(product((0,1),repeat=4))
W=O=SM=SN=SJ=LOSS=F(0);records=[];literal_assignments=positive_tax_atoms=0
for ai,atom in enumerate(atoms):
    bits=tuple(map(int,atom['bits']));assert len(bits)==10 and all(b in (0,1) for b in bits)
    his=[atom['AB_hist'],atom['AE_hist'],atom['second_hist']];types=[triples,triples,quads]
    for hist,tt in zip(his,types):assert len(hist)==len(tt) and sum(hist)==5 and all(type(x) is int and x>=0 for x in hist)
    ds=[sum(n*t[0] for n,t in zip(hist,tt)) for hist,tt in zip(his,types)];assert len(set(ds))==1;d=ds[0]
    for ell,h in atom['menus_lh']:assert 0<=h<=d and 0<=ell-h<=5-d
    mass=F(atom['exact_mass']);assert mass>0
    W+=mass*int(any(bits[:5]));O+=mass*int(d>0)
    source=[s for s,n in zip(triples,atom['AB_hist']) for _ in range(n)]
    target=[s for s,n in zip(quads,atom['second_hist']) for _ in range(n)]
    loads=[bits[0]+bits[1]+t+r for t,r,s in source];dd=[F(1,p+1) for p in loads]
    own=sum((di*s[2] for di,s in zip(dd,source)),F(0));D=sum(dd,F(0));K=sum(t[2] for t in target);L=sum(t[3] for t in target)
    cm=4*own-K*D;cn=4*own-L*D;joint=cm+cn;delta=F(0);groups=[];permlists=[]
    for t in (0,1):
        pos=[i for i,s in enumerate(source) if s[0]==t];dv=[dd[i] for i in pos];tuples=[(s[2],s[3]) for s in target if s[0]==t];assert len(pos)==len(tuples)
        k=sum(z for z,w in tuples);l=sum(w for z,w in tuples);h=sum(z*w for z,w in tuples);u=k+l-h
        cm+=top(dv,k);cn+=top(dv,l)
        separate,jmax,dt,terms=layer(dv,tuples,(1,1));joint+=jmax;delta+=dt
        r=sum(source[i][1]==0 for i in pos);p=bits[0]+bits[1]+t
        twolevel=F(max(0,min(r-h,k-h,l-h,u-r)),(p+1)*(p+2));assert dt==twolevel
        groups.append({'label':t,'source_positions':pos,'inverse_denominators':dv,'target_tuples':tuples,'k':k,'l':l,'h':h,'u':u,'high_slots':r,'loss':dt,'layer_terms':terms})
        permlists.append((pos,sorted(set(permutations(tuples)))))
    literal=[]
    for choices in product(*(v[1] for v in permlists)):
        assignment=[None]*5
        for (pos,_),values in zip(permlists,choices):
            for i,v in zip(pos,values):assignment[i]=v
        lm=ln=F(0)
        for i in range(5):
            for j in range(5):
                if i!=j:
                    lm+=F(source[i][2]-assignment[j][0],loads[i]+1)
                    ln+=F(source[i][2]-assignment[j][1],loads[i]+1)
        literal.append({'target_assignment':assignment,'M_offdiag':lm,'N_offdiag':ln,'joint':lm+ln});literal_assignments+=1
    assert max(v['M_offdiag'] for v in literal)==cm and max(v['N_offdiag'] for v in literal)==cn and max(v['joint'] for v in literal)==joint
    assert cm+cn-joint==delta>=0
    positive_tax_atoms+=delta>0
    SM+=mass*cm;SN+=mass*cn;SJ+=mass*joint;LOSS+=mass*delta
    records.append({'atom':ai,'mass':mass,'AB_hist':atom['AB_hist'],'second_hist':atom['second_hist'],'groups':groups,'M_upper':cm,'N_upper':cn,'joint_upper':joint,'loss':delta,'literal_matchings':literal})
assert W==F(data['welfare'])==1 and O==F(data['comparison_cover'])
assert SM>0 and SN>0 and SJ==F(-1986982543309346411409324987349550640449892779560449694465,14981334465482123235868977333713366662779525538289172031104)<0
assert LOSS==SM+SN-SJ and positive_tax_atoms==20
assert len(data['slacks'])==727 and all(F(v)>=0 for v in data['slacks'].values())

def enc(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {k:enc(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [enc(x) for x in v]
    return v
result={'status':'passed','new_math_entry_attempts':1,'new_math_entry_successes':1,'failed_math_attempts':0,'original_CLI_entries':0,'external_solver_calls':0,
 'generic_layers':{'q_values':[1,2,3],'menus':3,'source_load_configurations_per_q':2,'weight_vectors':weightsets,'D_complement_masks':[(0,0,0),(1,0,1),(1,1,1)],'combined_cases':multi_cases,'label_group_layer_identities':group_identities,'literal_label_group_matching_assignments':literal_group_matchings,'two_menu_integer_brackets':integer_cases,'twolevel_rational_identities':twolevel_cases,'two_menu_n_range':[0,6]},
 'adjacent':{'q_range':[0,4],'P_load_range':[0,2],'increments':[0,1],'indexed_lists':indexed,'all_margin_pairs':len(margins),'compatible_pairs':compatible,'all_margin_records':margins,'increments012_counterexample':{'joint1':wide1,'joint2':wide2,'reciprocal_joint_costs':wide_costs}},
 'point727':{'input_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'atoms':69,'positive_masses_and_domain_checked':True,'W':W,'comparison_cover':O,'M_separate_upper':SM,'N_separate_upper':SN,'joint_upper':SJ,'weighted_loss':LOSS,'strict_tax_atoms':positive_tax_atoms,'distinct_literal_matchings':literal_assignments,'atom_records':records,'stored727_slacks_nonnegative':True,'independently_recomputed727_slacks':False,'template_optimum_or_fulluniverse_dual_newly_verified':False,'fullSPE_completion_excluded_for_these_marginals':True},
 'not_newly_executed':['original9360/9008checks','originalparent217matchingCLI','65atom728pointseparation','fixedmarginalfloatingtransportLPs','727/728/737fulluniverseduals','oldGO/HB/GXsuccessfulmath'],
 'scope':'General layer/recovery proofs are analytic. Finite checks and selected69-point exact exclusion only; no root-welfare payment or global half result.'}
OUT.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({'status':'passed','multi_cases':multi_cases,'integer_brackets':integer_cases,'adjacent_indexed_lists':indexed,'margin_pairs':len(margins),'compatible_pairs':compatible,'point_atoms':69,'literal_matchings':literal_assignments,'tax_atoms':positive_tax_atoms,'M':SM,'N':SN,'joint':SJ,'new_entries':1,'original_entries':0,'solver_calls':0}),ensure_ascii=False))
