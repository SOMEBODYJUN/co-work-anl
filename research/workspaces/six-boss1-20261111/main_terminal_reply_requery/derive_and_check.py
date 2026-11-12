"""Main: uniform true terminal-reply requery rows for actual sources 1..5.

Reconstruct every hidden state.  Derive a complete explicit payment interval,
retain all weak states, materialize every target and C-only interface, then
evaluate only the explicitly pinned new v6 point and full affine face.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

H=Path(__file__).resolve().parent
W=H.parent
def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x
def save(name,x):
    with (H/name).open('x') as out:out.write(json.dumps(encode(x),ensure_ascii=False,indent=2)+'\n')
def read(path):return json.loads(path.read_text())
def sha(path):return sha256(path.read_bytes()).hexdigest()
source_pins={
    W/'visible_maximum_joint_v6/exact_input.json':'8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769',
    W/'visible_maximum_joint_v6_solve_v2/exact_certificate.json':'bbacce728e8172049b52e8468e4e6921d316854a2113528e5c74d64d7372f028',
    W/'visible_maximum_joint_v6_solve_v2/optimal_face.json':'7258aacace9180c43e8bc8a30a103bc3bd090eb6c19dd77f9a771c01d2c8be77'}
for path,pin in source_pins.items():assert sha(path)==pin
atoms=list(product((0,1),repeat=9))
all_states=[];profiles=[];cost_count=0
for source in range(1,6):
    n=7-source;lam=(n-1)**2;mid=n-2
    critical=[];profile_states=[]
    for p,t,o in product(range(source),(0,1),(0,1)):
        tails=list(product((0,1),repeat=n-1));q=F(o,6)
        base=[];direction=[]
        for tail in tails:
            middle=tail[:-1];z=tail[-1];k=sum(middle);L=p+t+k+z
            value=F(lam*t-z,L) if L else F(0)
            value+=F(k,12)+z+q/F(p+t+k+1)
            slope=F(z,p+n)-F(z,n)
            base.append(value);direction.append(slope)
        m=F(o,6*(p+1)) if not t else F(lam,p+n-1)+F(mid,12)+F(o,6*(p+n))
        assert min(base)==m,(source,p,t,o)
        at_endpoint=[v+n*d for v,d in zip(base,direction)]
        assert min(at_endpoint)==m
        assert all(v>=m for v in at_endpoint)
        for k,(v,d) in enumerate(zip(base,direction)):
            if d<0:critical.append(((v-m)/(-d),p,t,o,list(tails[k])))
        r={'source':source,'n':n,'p':p,'t':t,'o':o,
            'all_tails':tails,'base_costs':base,'direction':direction,'endpoint_costs':at_endpoint,
            'closed_minimum':m,
            'base_weak_tails':[tails[k] for k,v in enumerate(base) if v==m],
            'endpoint_weak_tails':[tails[k] for k,v in enumerate(at_endpoint) if v==m]}
        assert r['base_weak_tails']==r['endpoint_weak_tails']
        all_states.append(r);profile_states.append(r);cost_count+=len(tails)
    first=min(critical) if critical else None
    if source>1:assert first[0]==F(n*(n+4),5)>n
    else:assert first is None
    profiles.append({'source':source,'n':n,'lambda':lam,'theta_interval':[F(0),F(n)],
        'source_IC_weight':F(lam),'actual_source_SAFE_true_R6_weight':F(n),
        'middle_CAP_weights':[F(1,12)]*mid,'terminal_CAP_weight_at_endpoint':F(0),
        'terminal_menu_BR_weight':F(1),'final_actual_income_weight':F(lam+n),
        'final_K_weight':F(mid,12),'first_cost_change_after_endpoint':first,
        'full_payment_interval_limiter':'terminal_CAP coefficient 1-theta/n',
        'all_complete_condition_count':len(profile_states)})
assert cost_count==456 and len(all_states)==60

rows=[]
targets=[('A'+str(i+1),i) for i in range(6)]+[('X',6),('C',8)]
for pr in profiles:
    source,n,lam=pr['source'],pr['n'],pr['lambda']
    for target,ix in targets:
        for only in ([False,True] if target=='C' else [False]):
            mu=F(n-2,12) if only else F(0)
            coefficients=[]
            for atom in atoms:
                p=sum(atom[:source-1]);t=atom[ix];o=atom[7];L=sum(atom[:6])
                actual=F(atom[source-1],L) if L else F(0)
                m=F(o,6*(p+1)) if not t else F(lam,p+n-1)+F(n-2,12)+F(o,6*(p+n))
                coefficients.append((lam+n)*actual-m+mu*atom[8])
            coefficients.append(F(n-2,12)-mu)
            rows.append({'id':f'ACTUAL_SOURCE{source}_TRUE_REPLY6_REQUERY_{target}'+('_C_ONLY' if only else ''),
                'source':source,'target':target,'row_kind':'C-only' if only else 'general',
                'n':n,'lambda':str(lam),'theta':str(n),'a':coefficients,'rhs':'0','numerical_divisor':'1',
                'real_budget':pr,'free_EC':mu,'all_513_columns_preserved':True,
                'T_scope':'Any legal label; X is legal and no extra maximality is used here.'})
assert len(rows)==45
# The C-only interface must be exactly its general C row plus a free EC multiple.
for source in range(1,6):
    a=next(r for r in rows if r['source']==source and r['target']=='C' and r['row_kind']=='general')
    b=next(r for r in rows if r['source']==source and r['row_kind']=='C-only')
    mu=b['free_EC'];ec=[F(atom[8]) for atom in atoms]+[-F(1)]
    assert [v+mu*e for v,e in zip(a['a'],ec)]==b['a']

inp=read(W/'visible_maximum_joint_v6/exact_input.json')
for j,atom in enumerate(inp['atom_columns']):
    assert atom['a']+[atom['x'],atom['o'],atom['c']]==list(atoms[j])
def dense(raw):
    return list(map(F,raw)) if isinstance(raw,list) else [F(raw.get(str(j),'0')) for j in range(513)]
v3=next(r for r in rows if r['source']==3 and r['target']=='A5')
old3459=dense(inp['raw_rows'][3459]['a'])
diff=[F(4*atom[2],sum(atom[:6])) if sum(atom[:6]) else F(0) for atom in atoms]+[-F(1)]
assert v3['a']==[v+d for v,d in zip(old3459,diff)]
v4=next(r for r in rows if r['source']==4 and r['target']=='A5')
old3739=dense(inp['raw_rows'][3739]['a'])
diff4=[F(3*atom[3],sum(atom[:6])) if sum(atom[:6]) else F(0) for atom in atoms]+[-F(1)]
assert v4['a']==[v+d for v,d in zip(old3739,diff4)]

cert=read(W/'visible_maximum_joint_v6_solve_v2/exact_certificate.json')
face=read(W/'visible_maximum_joint_v6_solve_v2/optimal_face.json')
x=list(map(F,cert['primal']));npar=len(face['parameters'])
coords={r['column']:[F(r['constant'])]+list(map(F,r['parameter_coefficients'])) for r in face['coordinates']}
evaluations=[]
for row in rows:
    a=row['a'];slack=sum((v*t for v,t in zip(a,x)),F(0))
    affine=[sum((a[j]*v[k] for j,v in coords.items()),F(0)) for k in range(npar+1)]
    assert slack==affine[0]+sum((v*F(t) for v,t in zip(affine[1:],face['point_parameters'])),F(0))
    evaluations.append({'id':row['id'],'source':row['source'],'target':row['target'],
        'row_kind':row['row_kind'],'point_slack':slack,'affine_face_slack':affine,
        'constant_on_entire_affine_face':not any(affine[1:]),
        'strictly_excludes_entire_face':affine[0]<0 and not any(affine[1:])})
assert next(e for e in evaluations if e['id']==v3['id'])['strictly_excludes_entire_face']
for path,pin in source_pins.items():assert sha(path)==pin
save('source_pins.json',[{'path':str(path.relative_to(W)),'sha256':pin} for path,pin in source_pins.items()])
save('all_true_costs_and_weak_states.json',all_states)
save('complete_payment_profiles.json',profiles)
save('exact_family.json',{'schema':'all_actual_sources_true_terminal_reply_requery_v1',
    'row_count':45,'column_count':513,'original_scale':True,'rows':rows})
save('new_v6_point_and_face_diagnostic.json',{'status':'ALL45_EXACT_NEW_POINT_AND_FACE_VALUES',
    'point_sha256':source_pins[W/'visible_maximum_joint_v6_solve_v2/exact_certificate.json'],
    'face_sha256':source_pins[W/'visible_maximum_joint_v6_solve_v2/optimal_face.json'],
    'all_rows':evaluations})
result={'status':'PASS_MAIN_ALL_SOURCE_TRUE_REPLY6_REQUERY_FULL_COSTS_AND_ROWS',
    'actual_sources':5,'physical_conditions':60,'all_tail_costs_each_endpoint':456,
    'full_original_rows':45,'columns_each':513,'C_only_identities':5,
    'all_weak_states_preserved':True,'all_cost_change_thresholds_above_payment_endpoint':True,
    'point_negative_rows':[e['id'] for e in evaluations if e['point_slack']<0],
    'whole_face_excluding_rows':[e['id'] for e in evaluations if e['strictly_excludes_entire_face']],
    'raw3459_plus_4u3_minus_K_identity':True,'raw3739_plus_3u4_minus_K_identity':True,
    'optimizer_calls':0,'half_status':'OPEN'}
save('check_result.json',result)
print(json.dumps(encode(result),ensure_ascii=False))
