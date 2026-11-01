"""One new exact definition entry on the selected 60-atom input.

The original GO CLI/audits are absent. The preexisting original 437-row
evaluator's function prefix is reused on this NEW input, never its main,
old certificate, optimization or full-universe pricing loop. Added 120
within-family rows and selected cross-family checks are defined here.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, permutations, combinations_with_replacement
from collections import defaultdict
import ast, hashlib, json

E = Path(__file__).resolve().parent
OUT = E/'new-shared-matching-and-60point-check.json'
if OUT.exists():
    raise SystemExit('Successful definition entry already exists; do not rerun')
P = E/'comparison/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/exact_primal_overlap1.json'
raw = P.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825'
data = json.loads(raw)
atoms = data['atoms']
assert len(atoms) == 60
mass = [F(a['exact_mass']) for a in atoms]
assert all(w > 0 for w in mass)
SPEC = [('AB','AB_hist',3,(0,1)), ('AE','AE_hist',3,(0,4)), ('second','second_hist',4,(0,))]
patterns = ['all_equal','query_equal','first_branch','second_branch','all_distinct']

def expand(atom, spec):
    name,key,dim,fixed = spec
    states = list(product((0,1), repeat=dim))
    hist = atom[key]
    assert len(hist) == len(states) and sum(hist) == 5
    assert all(type(v) is int and v >= 0 for v in hist)
    return [s for s,n in zip(states,hist) for _ in range(n)]

def source(atom, spec, final=False):
    ss = expand(atom,spec)
    fixed = sum(int(atom['bits'][k]) for k in spec[3])
    p = [fixed+sum(s[:-1] if final else s[:-2]) for s in ss]
    if final:
        H = [F(s[-1],v+1) for s,v in zip(ss,p)]
    else:
        H = [(F(s[-2]+s[-1],v+s[-2]+s[-1]) if s[-2]+s[-1] else F(0))
             +F(s[-2],(v+1)*(v+2)) for s,v in zip(ss,p)]
    return ss,p,H

def pq(q,z,w,B,C,K):
    return [(1,z+w,z*w),(q-1,B-z+C-w,K-z*w),
            (q-1,(q-1)*z+C-w,z*(C-w)),
            (q-1,B-z+(q-1)*w,(B-z)*w),
            ((q-1)*(q-2),(q-2)*(B-z+C-w),(B-z)*(C-w)-(K-z*w))]

def pair_vector(p,H,tuples):
    q=len(p); B=sum(z for z,w in tuples); C=sum(w for z,w in tuples); K=sum(z*w for z,w in tuples)
    out=[F(0)]*5
    for pp,hh,(z,w) in zip(p,H,tuples):
        for r,(n,L,M) in enumerate(pq(q,z,w,B,C,K)):
            out[r] += n*hh-F(L,pp+1)+F(M,(pp+1)*(pp+2))
    return out

def literal_pair_vector(p,H,tuples):
    out=[F(0)]*5
    for i in range(len(p)):
        for j in range(len(p)):
            for k in range(len(p)):
                r=0 if i==j==k else 1 if j==k else 2 if i==j else 3 if i==k else 4
                z,w=tuples[j][0],tuples[k][1]
                out[r] += H[i]-F(z+w,p[i]+1)+F(z*w,(p[i]+1)*(p[i]+2))
    return out

def matchings(source_anchors,target_anchors,target_tuples):
    groups=[]
    for t in sorted(set(source_anchors)|set(target_anchors)):
        positions=[i for i,a in enumerate(source_anchors) if a==t]
        vals=[v for a,v in zip(target_anchors,target_tuples) if a==t]
        assert len(positions)==len(vals)
        groups.append((positions,sorted(set(permutations(vals)))))
    for choices in product(*(g[1] for g in groups)):
        out=[None]*len(source_anchors)
        for (positions,_),vs in zip(groups,choices):
            for i,v in zip(positions,vs): out[i]=v
        yield out

def tops(v,n): return sum(sorted(v,reverse=True)[:n],F(0))
def bottoms(v,n): return sum(sorted(v)[:n],F(0))

def final_exact(p,H,tuples):
    q=len(p); d=[F(1,x+1) for x in p]; A=sum(H,F(0)); D=sum(d,F(0))
    K=sum(z for z,w in tuples); L=sum(w for z,w in tuples)
    mz=sum(di*z for di,(z,w) in zip(d,tuples)); nw=sum(di*w for di,(z,w) in zip(d,tuples))
    return (2*(q-1)*A-(K+L)*D+mz+nw, 2*A-mz-nw, q*A-L*D+nw-mz)

def closed_final(p,H,anchors,tuples):
    q=len(p);d=[F(1,x+1) for x in p];A=sum(H,F(0));D=sum(d,F(0)); K=sum(z for z,w in tuples);L=sum(w for z,w in tuples)
    oo=2*(q-1)*A-(K+L)*D;dd=2*A;do=q*A-L*D
    for t in set(anchors):
        ds=[v for v,a in zip(d,anchors) if a==t]; tt=[v for v,a in zip(tuples,anchors) if a==t]
        k=sum(z for z,w in tt);l=sum(w for z,w in tt);h=sum(z*w for z,w in tt);u=k+l-h
        oo+=tops(ds,h)+tops(ds,u);dd-=bottoms(ds,h)+bottoms(ds,u);do+=tops(ds,l-h)-bottoms(ds,k-h)
    return (oo,dd,do)

def closed_pair(p,H,anchors,tuples):
    q=len(p);aa=[F(1,x+1) for x in p];ee=[F(1,x+2) for x in p];bb=[a-e for a,e in zip(aa,ee)]
    B=sum(z for z,w in tuples);C=sum(w for z,w in tuples);K=sum(z*w for z,w in tuples)
    e=(q-1)*sum(H,F(0))-(B+C)*sum(aa,F(0))+K*sum(bb,F(0));f=sum(H,F(0))
    for t in set(anchors):
        av=[a for a,s in zip(aa,anchors) if s==t];ev=[a for a,s in zip(ee,anchors) if s==t];tt=[v for v,s in zip(tuples,anchors) if s==t]
        h=sum(z*w for z,w in tt);u=sum(int(z or w) for z,w in tt)
        e+=tops(av,u)+tops(ev,h);f-=bottoms(av,u)+bottoms(ev,h)
    return e,f

# New selected input: check its domains and all 557 slacks. Reuse only the
# existing direct 437-row functions, not the original CLI or certificate.
helper=E/'formal-comparison/archives/customer-attraction/tools/evidence/five-player-indexed/tests/audits/customer_attraction_five_indexed.py'
tree=ast.parse(helper.read_text()); nodes=[]
for node in tree.body:
    if isinstance(node,ast.ImportFrom) and node.module=='pathlib': break
    nodes.append(node)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(helper),'exec'),ns)
slacks=defaultdict(F);W=O=F(0)
for atom,w in zip(atoms,mass):
    bits=tuple(map(int,atom['bits']));assert len(bits)==10 and all(x in (0,1) for x in bits)
    his=[atom[s[1]] for s in SPEC];expanded=[expand(atom,s) for s in SPEC];ds=[sum(s[0] for s in xs) for xs in expanded];assert len(set(ds))==1
    for ell,h in atom['menus_lh']:assert 0<=h<=ds[0] and 0<=ell-h<=5-ds[0]
    rows=ns['evaluate'](bits,his,atom['menus_lh'],include_second_correlations=True);assert len(rows)==437
    for spec in SPEC:
        ss,p,H=source(atom,spec,final=True);tag='Sbranch' if spec[0]=='second' else spec[0]
        for menu in range(spec[2]):
            B=sum(s[menu] for s in ss)
            rows[f'{tag}:5:offdiag:{menu}']=sum((4*h-F(B-s[menu],pp+1) for s,pp,h in zip(ss,p,H)),F(0))
        ss,p,H=source(atom,spec)
        for m,n in combinations_with_replacement(range(spec[2]),2):
            vals=pair_vector(p,H,[(s[m],s[n]) for s in ss])
            for pat,val in zip(patterns,vals):rows[f'{tag}:pair:{m}{n}:{pat}']=val
    assert len(rows)==557 and set(rows)==set(data['slacks'])
    for k,v in rows.items():slacks[k]+=w*v
    W+=w*int(any(bits[:5]));O+=w*int(ds[0]>0)
assert W==F(data['welfare'])==1 and O==F(data['comparison_cover'])>2
assert all(v>=0 for v in slacks.values()) and all(v==F(data['slacks'][k]) for k,v in slacks.items())

# Generic small cases: literal D/O identities and common-anchor extrema.
generic_assignments=generic_matching_assignments=literal_final_identities=literal_pair_identities=0
extrema_classes=set()
for q in range(1,5):
    for config in range(3):
        p=[(2*i+config)%3 for i in range(q)];anchors=[0 if config==0 else i%2 for i in range(q)];H=[F((i+config)%2,pp+1) for i,pp in enumerate(p)]
        for tup in product(product((0,1),repeat=2),repeat=q):
            generic_assignments+=1
            actual=final_exact(p,H,tup);A=sum(H,F(0)); literal=[F(0)]*3
            for i in range(q):
                for j in range(q):
                    if i!=j:literal[0]+=2*H[i]-F(tup[j][0]+tup[j][1],p[i]+1);literal[2]+=H[i]-F(tup[j][1],p[i]+1)
                literal[1]+=2*H[i]-F(sum(tup[i]),p[i]+1)
                literal[2]+=H[i]-F(tup[i][0],p[i]+1)
            assert actual==tuple(literal);literal_final_identities+=3
            pv=pair_vector(p,H,tup);lp=literal_pair_vector(p,H,tup);assert pv==lp;literal_pair_identities+=5
            opts=list(matchings(anchors,anchors,tup));generic_matching_assignments+=len(opts)
            final_opts=[final_exact(p,H,t) for t in opts];pair_opts=[pair_vector(p,H,t) for t in opts]
            assert closed_final(p,H,anchors,tup)==tuple(max(v[j] for v in final_opts) for j in range(3))
            e,f=closed_pair(p,H,anchors,tup);assert e==max(v[1] for v in pair_opts) and f==max(v[0] for v in pair_opts)
            counts=tuple((a,tuple(sorted(t for t,s in zip(tup,anchors) if s==a))) for a in sorted(set(anchors)))
            extrema_classes.add((q,config,counts))

# All 220 CROSS-family pair orbits on this new 60-atom point; maximization
# is per client. No global-topic matching or SPE completion is inferred.
cross=defaultdict(F);cross_coefficients=[];cross_assignments=closed_equalities=additive_equalities=0
selected_oo=F(0);component_M=component_N=F(0);selected_oo_atoms=[]
for ai,(atom,w) in enumerate(zip(atoms,mass)):
    for src in SPEC:
        ss,p,H=source(atom,src);anchor=[s[0] for s in ss]
        for target in SPEC:
            if src[0]==target[0]:continue
            ts=expand(atom,target);ta=[s[0] for s in ts]
            for m,n in combinations_with_replacement(range(target[2]),2):
                tt=[(s[m],s[n]) for s in ts]
                opts=list(matchings(anchor,ta,tt));values=[pair_vector(p,H,t) for t in opts];cross_assignments+=len(opts)
                mx=[max(v[j] for v in values) for j in range(5)]
                # Place target tuples in arbitrary same-anchor source order
                # for formulas which depend only on within-anchor counts.
                t0=opts[0];ce,cf=closed_pair(p,H,anchor,t0)
                assert mx[1]==ce and mx[0]==cf;closed_equalities+=2
                if src[0] in ('AB','AE'):
                    assert all(v==values[0] for v in values);additive_equalities+=5
                for pat,val in zip(patterns,mx):
                    key=f'{src[0]}:{target[0]}:{m}{n}:{pat}';cross[key]+=w*val
                    cross_coefficients.append({'atom':ai,'row':key,'upper_coefficient':val})
    # Source AB final nodes vs AE target lists R (1) and S (2), joint OO.
    ss,p,H=source(atom,SPEC[0],final=True);ts=expand(atom,SPEC[1]);tt=[(s[1],s[2]) for s in ts]
    opts=list(matchings([s[0] for s in ss],[s[0] for s in ts],tt))
    vals=[final_exact(p,H,t)[0] for t in opts];joint=max(vals);selected_oo+=w*joint
    d=[F(1,v+1) for v in p];A=sum(H,F(0));D=sum(d,F(0));B=sum(t[0] for t in tt);C=sum(t[1] for t in tt)
    cm=max(4*A-B*D+sum(di*t[0] for di,t in zip(d,vs)) for vs in opts)
    cn=max(4*A-C*D+sum(di*t[1] for di,t in zip(d,vs)) for vs in opts)
    component_M+=w*cm;component_N+=w*cn
    selected_oo_atoms.append({'atom':ai,'OO':joint,'M_offdiagonal':cm,'N_offdiagonal':cn})
assert len(cross)==220
negative={k:v for k,v in cross.items() if v<0};assert len(negative)==2
assert selected_oo==F(-1996456868586172483674258348477230789698004041227208957222543,8009267187464953266978610476016627605724079763575000300810190)
assert component_M<0 or component_N<0
assert cross['AB:second:23:query_equal']==F(-787666402463169489247192662090163381396856775798217752504989,8009267187464953266978610476016627605724079763575000300810190)

# Algebraic strictness is not an SPE example. The legal two-client example
# checks just two genuine final histories and all four legal final queries.
strict=closed_final([0,1],[F(0),F(1,2)],[0,0],[(0,1),(1,0)])[0]
assert strict==F(-1,2)
catalog=[set(),{0},{1},{0,1}];hist=[{1},{0}];brchecks=0
for bg in hist:
    actual=sum(F(1,1+int(x in bg)) for x in catalog[-1])
    for query in catalog:
        assert actual>=sum(F(1,1+int(x in bg)) for x in query);brchecks+=1
global_query_values=[F(3,2),F(3,2)];per_client_upper=F(2);assert max(global_query_values)<per_client_upper

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v) for v in x]
    return x
result={'status':'passed','new_definition_entries':1,'original_GO_CLI_entries':0,'original_437_CLI_entries':0,'external_solver_calls':0,
 'input_sha256':hashlib.sha256(raw).hexdigest(),'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),
 'helper_use':'AST function prefix only on the new 60-atom input; reused 437 evaluator, not independent reimplementation',
 'new60':{'atoms':len(atoms),'W':W,'comparison_cover':O,'all557_slacks_recomputed':dict(slacks),'zero_slacks':sum(v==0 for v in slacks.values()),'not_SPE_or_OPT_certificate':True},
 'generic':{'q_values':[1,2,3,4],'load_anchor_configurations_per_q':3,'literal_target_assignments':generic_assignments,'matching_assignments_examined':generic_matching_assignments,'final_identities':literal_final_identities,'pair_pattern_identities':literal_pair_identities,'extrema_classes':len(extrema_classes)},
 'cross_pairs':{'rows':len(cross),'atom_upper_coefficients':len(cross_coefficients),'deduplicated_allowed_assignments':cross_assignments,'closed_EF_equalities':closed_equalities,'constant_anchor_additive_row_equalities':additive_equalities,'negative_rows':negative,'totals':dict(cross),'atom_coefficients':cross_coefficients},
 'selected_joint_final':{'row':'AB:AE:1O+1*2O','OO':selected_oo,'M_separate_offdiag':component_M,'N_separate_offdiag':component_N,'at_least_one_component_already_negative':True,'atom_coefficients':selected_oo_atoms,'not_all_162_rows_reaudited':True},
 'examples':{'algebraic_joint_OO':strict,'algebraic_point_is_not_SPE_claim':True,'legal_two_client_final_BR_comparisons':brchecks,'global_query_contributions':global_query_values,'per_client_max_sum':per_client_upper,'no_full_policy_certificate_requested':True},
 'unverified_original_contracts':['full6144 final557 dual','67-atom optimum primal','61-atom717 primal','all162 final joint envelopes','old64 and42 point GO audits'],
 'scope':'Exact selected new input and finite sorting/assignment checks. General necessity proved analytically in accompanying text; no universal half or full SPE completion.'}
OUT.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({'status':'passed','new60_atoms':60,'new60_rows':557,'cross_rows':len(cross),'negative_cross_rows':negative,'selected_OO':selected_oo,'generic_assignments':generic_assignments,'cross_matching_assignments':cross_assignments,'new_entries':1,'original_GO_entries':0,'solver_calls':0}),ensure_ascii=False))
