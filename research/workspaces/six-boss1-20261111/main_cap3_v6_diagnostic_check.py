"""Main: all585 new-face values and the conditional same-C SAFE4 obstruction."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

W=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return sha256(p.read_bytes()).hexdigest()
def encode(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [encode(x) for x in v]
    return v
pins={
    'source2_cap3_full_delta_rows/exact_family.json':'4a31f3ff6847a355442807aa8d03fffad43c92c6849229f63299556da8c00c8b',
    'visible_maximum_joint_v6_solve_v2/exact_certificate.json':'bbacce728e8172049b52e8468e4e6921d316854a2113528e5c74d64d7372f028',
    'visible_maximum_joint_v6_solve_v2/optimal_face.json':'7258aacace9180c43e8bc8a30a103bc3bd090eb6c19dd77f9a771c01d2c8be77',
    'source2_cap3_v6_diagnostic/freeze_manifest.json':'3d599da54b36a492f46acd884d9185398a30541bf67dae618b52a7326cee435a'}
for p,s in pins.items():assert sha(W/p)==s
rows=read(W/'source2_cap3_full_delta_rows/exact_family.json')['rows']
cert=read(W/'visible_maximum_joint_v6_solve_v2/exact_certificate.json')
face=read(W/'visible_maximum_joint_v6_solve_v2/optimal_face.json')
x=list(map(F,cert['primal']))
coords={r['column']:[F(r['constant'])]+list(map(F,r['parameter_coefficients'])) for r in face['coordinates']}
assert len(coords)==23 and len(face['parameters'])==9
def affine(a):
    return [sum((a[j]*v[k] for j,v in coords.items() if a[j] and v[k]),F(0)) for k in range(10)]
counts={'positive':0,'zero':0,'negative':0};zero=[]
for r in rows:
    a=list(map(F,r['a']));v=affine(a)
    assert not any(v[1:]),r['id']
    point=sum((t*z for t,z in zip(a,x) if t and z),F(0))
    assert point==v[0]
    sign='positive' if point>0 else 'negative' if point<0 else 'zero';counts[sign]+=1
    if not point:zero.append(r['id'])
assert counts=={'positive':580,'zero':5,'negative':0}

# The two positive C budgets use the same actual forced C history.
tau4,tau5=F(5929,6912),F(65,72)
beta=[F(59881,497664),F(20035,20736),F(71,72)]
source_weights=[F(184969,6912),F(859,48)]
assert all(v>0 for v in beta+[tau4,tau5]+source_weights)
states=[];tails=list(product((0,1),repeat=4))
for p,c,o in product((0,1),repeat=3):
    weak=[];allcost=[]
    for a in source_weights:
        values=[]
        for r3,r4,r5,z in tails:
            L=p+c+r3+r4+r5+z
            v=F(a*c-tau4*r4-tau5*r5-z,L) if L else F(0)
            v+=beta[0]*r3+beta[1]*r4+beta[2]*r5+z
            v+=F(o,6*(p+c+r3+r4+r5+1))
            v+=tau4*F(o,6*(p+c+r3+3))+tau5*F(o,6*(p+c+r3+r4+2))
            values.append(v)
        m=min(values);weak.append([t for t,v in zip(tails,values) if v==m]);allcost.append(values)
    joint=[t for t in weak[0] if t in weak[1]]
    if c and o:
        assert joint==([(1,1,1,1)] if p==0 else [(1,1,0,1),(1,1,1,0)])
        assert all(t[0]==t[1]==1 and p+c+sum(t)==5 for t in joint)
    states.append({'p':p,'c':c,'o':o,'costs':allcost,'weak':weak,'intersection':joint})
atoms=list(product((0,1),repeat=9))
outside=[F(h[8]*(1-h[7])) for h in atoms]+[F(0)]
assert affine(outside)==[F(0)]*10
g=[F(h[7],6*(h[0]+2*h[8]+3)) for h in atoms]+[-F(1,5)]
value=affine(g)
expected=F(709638185136480929581839920970892210591292722310716,67588301606736414838046729267264655707163775139064531)
assert value==[expected]+[F(0)]*9
assert cert['dual']['positive_raw_indices'].count(4012)==cert['dual']['positive_raw_indices'].count(4067)==1
for p,s in pins.items():assert sha(W/p)==s
result={'status':'PASS_MAIN_585_CONSTANT_NEW_FACE_AND_TRUE_C_SAFE4_EQUALITY_OBSTRUCTION',
    'counts':counts,'all585_times9_parameter_coefficients_zero':True,'zero_rows':zero,
    'same_C_complete_costs_checked':256,'same_C_all_weak_states':states,
    'source_weights':source_weights,'strictly_positive_CAPs':beta,
    'C_outside_O_affine':[F(0)]*10,'conditional_N4_minus_K_over5_affine':value,
    'conditional_on_same_C_zero_true_payments':True,'unconditional_new_row_claimed':False,
    'optimizer_calls':0,'input_pins':pins}
with (W/'main_cap3_v6_diagnostic_check.json').open('x') as out:out.write(json.dumps(encode(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(encode({k:v for k,v in result.items() if k not in ['same_C_all_weak_states','input_pins']}),ensure_ascii=False))
