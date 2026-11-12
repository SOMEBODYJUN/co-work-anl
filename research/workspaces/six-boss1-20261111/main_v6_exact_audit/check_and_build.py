"""Main full raw primal/dual and face audit, then true ROOT5 substitution."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from hashlib import sha256
from decimal import Decimal, getcontext
import json

H=Path(__file__).resolve().parent
W=H.parent
S=W/'visible_maximum_joint_v6_solve_v2'
PINS={
    W/'visible_maximum_joint_v6/exact_input.json':'8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769',
    S/'exact_certificate.json':'bbacce728e8172049b52e8468e4e6921d316854a2113528e5c74d64d7372f028',
    S/'optimal_face.json':'7258aacace9180c43e8bc8a30a103bc3bd090eb6c19dd77f9a771c01d2c8be77',
    S/'independent_check_result.json':'daed49eecbec08d58884cff6c2b290e080e0bfcab81fd9ebb99921a2482dc18d',
    S/'optimal_face_check_result.json':'5e6e8d460f3ab98f09ec25f45f2f174a4302c21c9a591a2c2743a6943541b33b',
    W/'main_root_reweighting/freeze_manifest.json':'fb21377e83b3edfe8c1334dfd1aa63e48b2003e1f52aa73cda4e5d80796fedf3',
    W/'main_root_reweighting/exact_certificate.json':'3672605d4989e2c1970a1d902c514b4634558461e90c7e4f5c460f3a57716090',
}
def sha(path): return sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text())
def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x
def save(name,x):
    with (H/name).open('x') as out: out.write(json.dumps(encode(x),ensure_ascii=False,indent=2)+'\n')
def sparse(a):
    if isinstance(a,list): return {i:F(v) for i,v in enumerate(a) if F(v)}
    return {int(i):F(v) for i,v in a.items() if F(v)}
def dot(a,x): return sum((v*x[i] for i,v in a.items()),F(0))
def rank(matrix):
    m=[r[:] for r in matrix];n=len(m[0]);k=0
    for j in range(n):
        p=next((i for i in range(k,len(m)) if m[i][j]),None)
        if p is None: continue
        m[k],m[p]=m[p],m[k];pivot=m[k][j];m[k]=[v/pivot for v in m[k]]
        for i in range(k+1,len(m)):
            if m[i][j]:
                f=m[i][j];m[i]=[x-f*y for x,y in zip(m[i],m[k])]
        k+=1
        if k==len(m): break
    return k

for path,pin in PINS.items(): assert sha(path)==pin,str(path)
inp=read(W/'visible_maximum_joint_v6/exact_input.json')
cert=read(S/'exact_certificate.json');face=read(S/'optimal_face.json')
assert inp['variables']==513 and len(inp['raw_rows'])==4177 and len(inp['equalities'])==2
assert inp['K_column']==512 and inp['nonnegative_columns']==list(range(513))
assert len(inp['atom_columns'])==512
atoms=list(product((0,1),repeat=9))
for j,h in enumerate(atoms):
    a=inp['atom_columns'][j]
    assert a['index']==j and a['old_index']==j//2
    assert a['a']+[a['x'],a['o'],a['c']]==list(h)
rows=[sparse(r['a']) for r in inp['raw_rows']]
rhs=[F(r['rhs']) for r in inp['raw_rows']]
eq=[sparse(r['a']) for r in inp['equalities']]
eqrhs=[F(r['rhs']) for r in inp['equalities']]
obj=sparse(inp['objective']);x=list(map(F,cert['primal']))
y=list(map(F,cert['dual']['raw_row_weights']))
eta=list(map(F,cert['dual']['equality_multipliers']))
assert len(x)==len(cert['dual']['nonnegative_column_residual'])==513
assert len(y)==4177 and len(eta)==2
assert all(v>=0 for v in x+y)
assert sum(b==-1 for b in rhs)==30
assert all(b in (0,-1) for b in rhs)
assert not rows[45] and rhs[45]==0
slacks=[dot(r,x)-b for r,b in zip(rows,rhs)]
assert all(v>=0 for v in slacks)
assert slacks==list(map(F,cert['raw_row_slacks']))
assert all(v*w==0 for v,w in zip(y,slacks))
assert [dot(e,x) for e in eq]==eqrhs
positive=[i for i,v in enumerate(y) if v]
assert positive==cert['dual']['positive_raw_indices']==face['positive_dual_raw_indices']
resids=[]
for j in range(513):
    r=obj.get(j,F(0))-sum((y[i]*rows[i].get(j,F(0)) for i in positive),F(0))
    r-=sum((v*e.get(j,F(0)) for v,e in zip(eta,eq)),F(0))
    assert r>=0 and r*x[j]==0
    resids.append(r)
assert resids==list(map(F,cert['dual']['nonnegative_column_residual']))
alpha=dot(obj,x)
assert alpha==F(cert['objective'])==sum((v*b for v,b in zip(y,rhs)),F(0))+sum((v*b for v,b in zip(eta,eqrhs)),F(0))
assert all(rhs[i]==0 for i in positive)

# Independently establish the complete affine solution space.
zero=[j for j,r in enumerate(resids) if not r]
assert zero==face['zero_residual_columns'] and len(zero)==23
forced=[j for j,r in enumerate(resids) if r]
assert forced==face['forced_zero_columns']
params=face['parameters'];npar=len(params);assert npar==9
coords={r['column']:[F(r['constant'])]+list(map(F,r['parameter_coefficients'])) for r in face['coordinates']}
assert sorted(coords)==zero
assert all(len(v)==npar+1 for v in coords.values())
null=[F(0)]*(npar+1)
for j in forced: coords[j]=null[:]
for k,p in enumerate(params):
    assert p['position']==k
    assert coords[p['column']]==[F(0)]+[F(i==k) for i in range(npar)]
equations=eq+[rows[i] for i in positive]
equation_rhs=eqrhs+[rhs[i] for i in positive]
assert rank([[row.get(j,F(0)) for j in zero] for row in equations])==14
def affine(row,b=F(0)):
    out=[sum((v*coords[j][k] for j,v in row.items()),F(0)) for k in range(npar+1)]
    out[0]-=b
    return out
for row,b in zip(equations,equation_rhs): assert affine(row,b)==null
point_parameters=list(map(F,face['point_parameters']))
assert point_parameters==[x[p['column']] for p in params]
for j in range(513):
    v=coords[j];assert x[j]==v[0]+sum((a*b for a,b in zip(v[1:],point_parameters)),F(0))
    item=face['all513_nonnegative_coordinate_restrictions'][j]
    assert item['column']==j
    assert [F(item['constant'])]+list(map(F,item['parameter_coefficients']))==v
    assert item['forced_zero']==(j in forced)
assert len(face['all_raw_inequality_restrictions'])==4177
for i,(row,b,item) in enumerate(zip(rows,rhs,face['all_raw_inequality_restrictions'])):
    assert item['raw_index']==i and F(item['original_rhs'])==b
    assert affine(row,b)==[F(item['constant'])]+list(map(F,item['parameter_coefficients']))
assert affine(obj)==[alpha]+[F(0)]*npar
fixed={}
for key,row in [('K',{512:F(1)}),('C_outside_O',{j:F(h[8]*(1-h[7])) for j,h in enumerate(atoms)})]:
    fixed[key]=affine(row)
assert fixed['K'][0]>0 and fixed['K'][1:]==[F(0)]*npar
assert fixed['C_outside_O']==null
for i in range(6):
    row={j:F(h[i],sum(h[:6])) for j,h in enumerate(atoms) if sum(h[:6]) and h[i]}
    fixed['u'+str(i+1)]=affine(row)
    assert fixed['u'+str(i+1)][1:]==[F(0)]*npar

# Replace the actually positive ROOT270 row with the independently proved ROOT5.
strong=read(W/'main_root_reweighting/exact_certificate.json')
newroot=sparse(strong['overrides']['868'])
oldroot=rows[4176]
assert y[4176]>0
gain_K=oldroot[512]-newroot[512]
assert gain_K>0 and all(oldroot.get(j,F(0))==newroot.get(j,F(0)) for j in range(512))
cap={512:F(6)}
for j,h in enumerate(atoms):
    if h[7]:cap[j]=-F(1)
gain=y[4176]*gain_K/6
newalpha=alpha+gain
full_identity=[]
for j in range(513):
    rhs_value=resids[j]+eta[1]*eq[1].get(j,F(0))+gain*cap.get(j,F(0))
    for i in positive: rhs_value+=y[i]*(newroot if i==4176 else rows[i]).get(j,F(0))
    value=obj.get(j,F(0))-newalpha*eq[0].get(j,F(0))-rhs_value
    assert value==0,j
    full_identity.append(value)
face_newroot=affine(newroot)
assert face_newroot==[-gain_K*fixed['K'][0]]+[F(0)]*npar
assert face_newroot[0]<0
getcontext().prec=70
decimal=lambda q:str(Decimal(q.numerator)/Decimal(q.denominator))
for path,pin in PINS.items(): assert sha(path)==pin,str(path)
save('source_pins.json',[{'path':str(path.relative_to(W)),'sha256':pin,'bytes':path.stat().st_size} for path,pin in PINS.items()])
save('universal_ROOT5_certificate.json',{'status':'PASS_MAIN_V6_DUAL_WITH_TRUE_ROOT5_UNIVERSAL_GAIN',
    'base_v6_alpha':alpha,'alpha':newalpha,'alpha_decimal':decimal(newalpha),
    'gain':gain,'root_K_gain':gain_K,'all4177_raw_weights':y,'positive_raw_indices':positive,
    'root_row_override':{'raw_index':4176,'a':[newroot.get(j,F(0)) for j in range(513)],'rhs':'0'},
    'additional_true_six_query_cap':{'a':[cap.get(j,F(0)) for j in range(513)],'weight':gain,'rhs':'0'},
    'free_EC_multiplier':eta[1],'all513_nonnegative_residuals':resids,
    'all513_identity_residuals':full_identity,
    'scope':'Universal bound from actually positive true budgets and ROOT5; not the optimum after adding new rows.',
    'original_half_status':'OPEN','optimizer_calls':0})
save('full_face_root_exclusion.json',{'status':'PASS_MAIN_ENTIRE_NEW_V6_FACE_EXCLUDED_BY_TRUE_ROOT5',
    'all_zero_dual_columns':zero,'rank':14,'affine_free_columns':[p['column'] for p in params],
    'affine_dimension_is_not_feasible_relative_dimension_claim':True,
    'all4177_parameter_inequalities_checked':True,'all513_nonnegative_conditions_checked':True,
    'K_fixed':fixed['K'][0],'C_outside_O_fixed':F(0),
    'new_root_affine_slack':face_newroot,'strictly_negative_on_entire_face':True,
    'old_face_or_old_support_used':False,'optimizer_calls':0})
result={'status':'PASS_MAIN_V6_ALL4177_PRIMAL_ALL513_DUAL_COMPLETE_FACE_AND_NEW_UNIVERSAL_BOUND',
    'raw_rows_checked':4177,'nonnegative_columns_checked':513,'equalities_checked':2,
    'affine_rhs_minus_one_rows':30,'positive_raw_rows':positive,
    'base_exact_alpha':alpha,'base_alpha_decimal':decimal(alpha),
    'new_universal_alpha':newalpha,'new_alpha_decimal':decimal(newalpha),'new_gain':gain,
    'zero_dual_columns':zero,'restricted_rank':14,'affine_parameter_count':9,
    'whole_new_face_strictly_excluded':True,'root_gain_K':gain_K,'fixed_K':fixed['K'][0],
    'optimizer_calls':0,'half_status':'OPEN'}
save('check_result.json',result)
print(json.dumps(encode(result),ensure_ascii=False))
